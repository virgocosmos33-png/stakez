import _ from 'lodash';
import { tick } from 'svelte';

import { recordBookEvent, checkIsMultipleRevealEvents, type BookEventHandlerMap } from 'utils-book';
import { stateBet, stateBetDerived } from 'state-shared';
import { fxWait, fxDur, fxHold } from './fxTiming';

import { SYMBOL_SIZE } from './constants';
import { eventEmitter } from './eventEmitter';
import { playBookEvent } from './utils';
import { filterVisibleCells, isVisibleBoardCell } from './boardCells';
import { getWinCelebration } from './winCelebrationMap';
import type { MusicName, SoundEffectName } from './sound';
import { stateGame, stateGameDerived } from './stateGame.svelte';
import { shakeBoard } from './stateShake.svelte';
import { isMegaWin } from './winConnection';
import type { BookEvent, BookEventOfType, BookEventContext } from './typesBookEvent';
import type { Position, RawSymbol, SymbolName } from './types';

type WinSoundsData = {
	alias: string;
	type: string;
	sound: { sfx?: SoundEffectName; bgm?: MusicName };
};

const winLevelSoundsPlay = ({ winLevelData }: { winLevelData: WinSoundsData }) => {
	if (winLevelData?.alias === 'max') eventEmitter.broadcastAsync({ type: 'uiHide' });
	if (winLevelData?.sound?.sfx) {
		eventEmitter.broadcast({ type: 'soundOnce', name: winLevelData.sound.sfx });
	}
	if (winLevelData?.sound?.bgm) {
		// stop any celebration stage bed already running so the incoming one
		// starts from its downbeat instead of stacking
		for (const name of [
			'bgm_celeb_1',
			'bgm_celeb_2',
			'bgm_celeb_3',
			'bgm_celeb_4',
			'bgm_celeb_5',
			'bgm_celeb_6',
		] as MusicName[]) {
			eventEmitter.broadcast({ type: 'soundStop', name });
		}
		eventEmitter.broadcast({ type: 'soundMusic', name: winLevelData.sound.bgm });
	}
};

const winLevelSoundsStop = () => {
	eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_bigwin_coinloop' });
	eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_main' });
	eventEmitter.broadcastAsync({ type: 'uiShow' });
};

const animateSymbols = async ({ positions }: { positions: Position[] }) => {
	eventEmitter.broadcast({ type: 'boardShow' });
	await eventEmitter.broadcastAsync({
		type: 'boardWithAnimateSymbols',
		symbolPositions: positions,
	});
};

/** a fresh copy of the live raw board, safe to mutate and settle back */
const rawBoardCopy = (): RawSymbol[][] =>
	stateGameDerived.boardRaw().map((reel) => reel.map((rawSymbol) => ({ ...rawSymbol })));

/** `boardSettle` swaps raw symbols but leaves symbolY alone — park each touched
 * cell back at its rest position so a swapped symbol is never left off-screen. */
const parkCells = (cells: Position[]) => {
	cells.forEach(({ reel, row }) => {
		const reelSymbol = stateGame.board[reel]?.reelState.symbols[row];
		if (!reelSymbol) return;
		const restY = (row - 0.5) * SYMBOL_SIZE;
		if (reelSymbol.symbolY.current !== restY) {
			reelSymbol.symbolY.set(restY, { duration: 0 });
		}
	});
};

/** After a reel grows/shrinks, every padded index needs its rest Y — not only
 * the newly added cell. Otherwise older symbols keep a pre-grow tween Y and
 * fall outside SymbolWrap's live window (blank sockets after the add anim). */
const parkReel = (reelIndex: number) => {
	const symbols = stateGame.board[reelIndex]?.reelState.symbols;
	if (!symbols) return;
	symbols.forEach((reelSymbol, row) => {
		const restY = (row - 0.5) * SYMBOL_SIZE;
		reelSymbol.symbolY.set(restY, { duration: 0 });
	});
};

/** Drop a buried symbol into place (land → static). Avoids win/postWinStatic,
 * which is for pay celebration and can leave the cell looking cleared. */
const landCells = async (cells: Position[]) => {
	eventEmitter.broadcast({ type: 'boardShow' });
	await Promise.all(
		cells.map(async ({ reel, row }) => {
			const reelSymbol = stateGame.board[reel]?.reelState.symbols[row];
			if (!reelSymbol) return;
			reelSymbol.symbolState = 'land';
			await Promise.race([
				new Promise<void>((resolve) => {
					reelSymbol.oncomplete = resolve;
				}),
				fxWait(900),
			]);
			reelSymbol.symbolState = 'static';
		}),
	);
};

/** Keep win overlays on live visible cells only (skip pads / out-of-range). */
const visibleWinPositions = (positions: Position[]): Position[] => filterVisibleCells(positions);

// How many ways actually connected this spin (summed in winInfo, shown in setWin).
let connectedWays = 0;
// Whether this spin already ran a win presentation, so finalWin can back up a
// capped book (no setWin) without double-celebrating a normal one.
let winPresented = false;

/** The one win presentation: pick the tier from the amount, run the takeover.
 *  `waysOverride` lets the COMPONENTS/WinCelebration Storybook stories drive this
 *  exact live path (tier art, coins, sound bed, staged rollup) with a chosen ways
 *  count. Real play leaves it undefined so the connected-ways total is used. */
export const presentWinCelebration = async (amount: number, waysOverride?: number) => {
	if (amount <= 0) return;
	winPresented = true;

	// the celebration tier is chosen by win amount in bet multiples
	const celebration = getWinCelebration(amount);
	const ways = waysOverride ?? connectedWays;

	eventEmitter.broadcast({ type: 'winShow' });
	winLevelSoundsPlay({ winLevelData: celebration });
	await eventEmitter.broadcastAsync({
		type: 'winUpdate',
		amount,
		ways,
	});
	winLevelSoundsStop();
	eventEmitter.broadcast({ type: 'winHide' });

	eventEmitter.broadcast({ type: 'winCycleStart' });
};

/** shared by split / splitGang / splitOutlaws: mark the targets, stamp the
 * per-cell ways multipliers, tear the panes apart, climb the WAYS rail. */
const applySplit = async (
	bookEvent:
		| BookEventOfType<'split'>
		| BookEventOfType<'splitGang'>
		| BookEventOfType<'splitOutlaws'>,
	tone: 'split' | 'stretch' | 'clone',
) => {
	eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
	// Never lock / tear pad rows or cells past a short reel's window — those
	// sockets are empty graveyard, not symbols (diamond board).
	const cells = filterVisibleCells(bookEvent.cells);
	if (!cells.length) {
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		return;
	}

	await eventEmitter.broadcastAsync({
		type: 'targetLockShow',
		cells: cells.map(({ reel, row }) => ({ reel, row })),
		tone,
	});

	const newBoard = rawBoardCopy();
	cells.forEach(({ reel, row, multiplier }) => {
		if (newBoard[reel]?.[row]) {
			newBoard[reel][row] = { ...newBoard[reel][row], multiplier };
		}
	});
	eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });

	await eventEmitter.broadcastAsync({
		type: 'splitPanesShow',
		cells: cells.map(({ reel, row, multiplier }) => ({
			reel,
			row,
			count: multiplier,
		})),
	});

	eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
	await fxHold();
};

/** Settle those cells to WILD, then flip each card so the bottle is on the back. */
const playWildFlip = async (
	cells: { reel: number; row: number; from?: SymbolName }[],
	opts?: { shoot?: boolean },
) => {
	const visible = filterVisibleCells(cells);
	if (!visible.length) return;
	const faces = visible.map((cell) => ({
		reel: cell.reel,
		row: cell.row,
		from: (cell.from ??
			stateGameDerived.boardRaw()[cell.reel]?.[cell.row]?.name ??
			'L1') as SymbolName,
	}));
	const newBoard = rawBoardCopy();
	faces.forEach(({ reel, row }) => {
		if (newBoard[reel]?.[row]) {
			newBoard[reel][row] = { ...newBoard[reel][row], name: 'W' };
		}
	});
	eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
	parkCells(faces);
	await eventEmitter.broadcastAsync({
		type: 'wildFlipShow',
		cells: faces,
		shoot: opts?.shoot,
	});
};

/** Landed GS cards the revolver sits on. Prefer the live board so row is real. */
const findGunsmokeOrigins = (): { reel: number; row: number }[] => {
	const raw = stateGameDerived.boardRaw();
	const found: { reel: number; row: number }[] = [];
	for (let reel = 0; reel < raw.length; reel++) {
		const col = raw[reel] ?? [];
		for (let row = 0; row < col.length; row++) {
			if (col[row]?.name === 'GS' && isVisibleBoardCell(reel, row)) {
				found.push({ reel, row });
			}
		}
	}
	return found;
};

const showGunsmokeGun = async (cells?: { reel: number; row: number }[]) => {
	const origins = filterVisibleCells(cells ?? findGunsmokeOrigins());
	if (!origins.length) return;
	await eventEmitter.broadcastAsync({ type: 'gunsmokeGunShow', cells: origins });
};

const aimGunsmokeGun = async (cell: { reel: number; row: number }) => {
	await eventEmitter.broadcastAsync({
		type: 'gunsmokeGunAim',
		reel: cell.reel,
		row: cell.row,
	});
	await eventEmitter.broadcastAsync({ type: 'gunsmokeGunFire' });
};

/** GUNSMOKE: shoot each copy into a WILD. One-by-one at normal speed; one volley in turbo. */
const playGunsmokeShoot = async (
	cells: { reel: number; row: number }[],
	from: SymbolName,
) => {
	const visible = filterVisibleCells(cells);
	if (!visible.length) return;
	await showGunsmokeGun();
	const together = stateBet.isTurbo || stateBet.isSuperTurbo;
	const first = visible[0];
	if (together && first) {
		await aimGunsmokeGun(first);
		await playWildFlip(
			visible.map((cell) => ({ ...cell, from })),
			{ shoot: true },
		);
		await eventEmitter.broadcastAsync({ type: 'gunsmokeGunHide' });
		return;
	}
	for (const cell of visible) {
		await aimGunsmokeGun(cell);
		await playWildFlip([{ ...cell, from }], { shoot: true });
	}
	await eventEmitter.broadcastAsync({ type: 'gunsmokeGunHide' });
};

/** BOUNTY: the premium lands in the last-reel lane wearing its WIN multiplier. */
const applyBounty = async ({
	reel,
	symbol,
	winMult,
}: {
	reel: number;
	symbol: string;
	winMult: number;
}) => {
	const cell = { reel, row: 1 }; // the lane is 1 visible row: padded row 1
	// the gunsight snap comes from TargetLock itself, so nothing is fired here

	await eventEmitter.broadcastAsync({
		type: 'targetLockShow',
		cells: [cell],
		tone: 'clone',
	});

	const newBoard = rawBoardCopy();
	if (newBoard[reel]?.[1]) {
		newBoard[reel][1] = { ...newBoard[reel][1], name: symbol as RawSymbol['name'] };
	}
	eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
	parkCells([cell]);

	await eventEmitter.broadcastAsync({
		type: 'featureBurstShow',
		kind: 'bounty',
		cells: filterVisibleCells([cell]),
	});
	await eventEmitter.broadcastAsync({
		type: 'stretchWaysShow',
		cells: [{ ...cell, multiplier: winMult }],
	});
	await animateSymbols({ positions: [cell] });
};

export const bookEventHandlerMap: BookEventHandlerMap<BookEvent, BookEventContext> = {
	reveal: async (bookEvent: BookEventOfType<'reveal'>, { bookEvents }: BookEventContext) => {
		const isBonusGame = checkIsMultipleRevealEvents({ bookEvents });
		if (isBonusGame) {
			eventEmitter.broadcast({ type: 'stopButtonEnable' });
			recordBookEvent({ bookEvent });
		}

		eventEmitter.broadcast({ type: 'cellSealHide' });
		eventEmitter.broadcast({ type: 'winCycleStop' });
		stateGame.gameType = bookEvent.gameType;

		// ride last spin's feature art off the board before the reset below
		await eventEmitter.broadcastAsync({ type: 'featureFxFallOut' });

		// TOMBSTONE OPEN may have grown reels last spin — restore the authored
		// 3/4/4/2/2/1 heights before this fresh reveal so the board spins in clean.
		stateGame.board.forEach((reel) => reel.resetToInitialHeight());
		stateGame.specialBar = [];
		stateGame.specialBarActiveKind = null;
		// the lane relocks every spin unless the SUPER bonus dug it up for the
		// whole round; leaving the bonus drops that too
		if (bookEvent.gameType === 'basegame') {
			stateGame.laneSuper = false;
			eventEmitter.broadcast({ type: 'winMultUpdate', value: 1 });
		}
		stateGame.lidOpen = stateGame.laneSuper;
		stateGame.slotWinPositions = [];
		stateGame.featureCells = [];
		stateGame.reelStretch = stateGame.reelStretch.map(() => null);
		eventEmitter.broadcast({ type: 'stretchWaysHide' });
		eventEmitter.broadcast({ type: 'cellLightningHide' });
		stateGame.revealNonce += 1;
		stateGame.slotsReleased = false;

		connectedWays = 0;
		winPresented = false;
		eventEmitter.broadcast({ type: 'waysCounterHide' });

		stateGame.nudgeCoverReel = null;
		const nudgeEv = bookEvents.find((event) => event.type === 'nudgeWays');
		stateGame.pendingNudge =
			nudgeEv && nudgeEv.type === 'nudgeWays'
				? {
						reel: nudgeEv.reel,
						fullReel: nudgeEv.fullReel,
						startRow: nudgeEv.startRow,
						initialWays: nudgeEv.initialWays,
					}
				: null;

		const spinning = stateGameDerived.enhancedBoard.spin({ revealEvent: bookEvent });
		await tick();
		stateGame.slotsReleased = true;
		await spinning;
	},
	winInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
		const betCost = stateBetDerived.betCost();
		const megaWin = bookEvent.wins.find((win) => isMegaWin(win.win, betCost));

		// every way that paid, across all winning symbols — used by the
		// celebration only. The hanging WAYS plaque stays on the full-board count.
		connectedWays = bookEvent.wins.reduce((total, win) => total + (win.meta?.ways ?? 0), 0);

		if (!megaWin) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
		}

		// Split holes, badges and cell fire stay up through the shine — they
		// are this spin's state. Fall-out on the next reveal is what clears them.

		// The pre-money shine never holds the count-up hostage: each type's beat
		// is capped, and a click/tap fast-forwards straight to the money.
		const SHINE_CAP_MS = 750;
		let skipped = false;
		let resolveSkip: () => void = () => {};
		const skipPromise = new Promise<void>((resolve) => (resolveSkip = resolve));
		const onSkip = () => {
			skipped = true;
			resolveSkip();
		};
		window.addEventListener('pointerdown', onSkip, { capture: true });

		try {
			for (const win of bookEvent.wins) {
				if (skipped) break;
				const positions = visibleWinPositions(win.positions);
				if (positions.length === 0) continue;
				eventEmitter.broadcast({ type: 'winDimShow', positions });
				eventEmitter.broadcast({ type: 'winSweep', positions });
				await Promise.race([
					animateSymbols({ positions }),
					fxWait(SHINE_CAP_MS),
					skipPromise,
				]);
			}

			// mega-win lightning telegraph — after symbol anims, before the money
			if (megaWin && !skipped) {
				// Tombstone: no White Room clinical whiteout — just the thunder sting
				eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_thunder' });
				shakeBoard({ intensity: 10, duration: fxDur(280) });
				await Promise.race([fxWait(320), skipPromise]);
			}
		} finally {
			window.removeEventListener('pointerdown', onSkip, { capture: true });
		}

		const allWins = bookEvent.wins.map((win) => visibleWinPositions(win.positions));
		// hold every winning cell lit through the money count-up
		eventEmitter.broadcast({
			type: 'winDimShow',
			positions: allWins.flat(),
		});
		eventEmitter.broadcast({
			type: 'winCycleSet',
			wins: allWins.filter((positions) => positions.length > 0),
		});
	},
	// ------------------------------------------------------------------
	// TOMBSTONE REBORN custom events
	// ------------------------------------------------------------------
	// The special bar resolves its cards. The cards themselves are shown by
	// the SpecialBar component (reads stateGame.specialBar); each card's EFFECT
	// plays in its own following event.
	specialBar: async (bookEvent: BookEventOfType<'specialBar'>) => {
		stateGame.specialBar = bookEvent.cells;
		if (bookEvent.barMode === 'super') {
			stateGame.laneSuper = true;
			stateGame.lidOpen = true;
		}
		if (bookEvent.cells.length > 0) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_special_hit' });
			shakeBoard({ intensity: 4, duration: fxDur(180) });
			await fxWait(350);
		}
	},
	boardSpecials: async (bookEvent: BookEventOfType<'boardSpecials'>) => {
		stateGame.specialBar = bookEvent.cells.map(({ reel, kind }) => ({ reel, kind }));
		if (bookEvent.lastUnlocked || bookEvent.barMode === 'super') {
			stateGame.lidOpen = true;
		}
		if (bookEvent.barMode === 'super') {
			stateGame.laneSuper = true;
		}
		if (bookEvent.cells.length > 0) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_special_hit' });
			shakeBoard({ intensity: 4, duration: fxDur(180) });
			const guns = bookEvent.cells.filter((cell) => cell.kind === 'gunsmoke');
			if (guns.length) {
				void showGunsmokeGun(guns);
			}
			// Do not lock every planted card here — each following feature
			// locks its own targets. A board-wide lock then a second lock is
			// the stacked-reticle glitch.
			await fxHold();
		}
	},
	// SUPER scatter opened the last-reel lane this spin. A spade is driven
	// into the boarded cover (FeatureBurst, kind 'digUp').
	tombstone: async (bookEvent: BookEventOfType<'tombstone'>) => {
		stateGame.specialBarActiveKind = 'tombstone';
		// the shovel strikes themselves are scheduled by FeatureBurst, which
		// knows the per-cell stagger; nothing else announces the dig
		shakeBoard({ intensity: 7, duration: fxDur(260) });
		// the spade blasts the boarded cover off the lane — LaneLidLock plays
		// its break-away the moment this flips
		stateGame.lidOpen = true;
		const lane = filterVisibleCells([{ reel: bookEvent.reel, row: 1 }]);
		await eventEmitter.broadcastAsync({ type: 'featureBurstShow', kind: 'digUp', cells: lane });
		await animateSymbols({ positions: [{ reel: bookEvent.reel, row: 1 }] });
		await fxHold();
		stateGame.specialBarActiveKind = null;
	},
	digUp: async (bookEvent: BookEventOfType<'digUp'>) => {
		await playBookEvent({ ...bookEvent, type: 'tombstone' }, { bookEvents: [] });
	},
	// TOMBSTONE OPEN — removed. Older books still emit this; ignore the grow.
	coffinOpen: async (_bookEvent: BookEventOfType<'coffinOpen'>) => {
		return;
	},
	// GUNSMOKE — every copy of one symbol type morphs into the revolver WILD
	gunsmoke: async (bookEvent: BookEventOfType<'gunsmoke'>) => {
		stateGame.specialBarActiveKind = 'gunsmoke';
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		const cells = filterVisibleCells(bookEvent.cells);
		if (!cells.length) {
			eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
			return;
		}

		// mark every copy while it is still the old symbol
		await eventEmitter.broadcastAsync({
			type: 'targetLockShow',
			cells: cells.map(({ reel, row }) => ({ reel, row })),
			tone: 'clone',
		});

		await playGunsmokeShoot(cells, bookEvent.symbol as SymbolName);
		await animateSymbols({ positions: cells });

		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await fxHold();
		stateGame.specialBarActiveKind = null;
	},
	// SPLIT — one symbol type on the board gains extra ways
	split: async (bookEvent: BookEventOfType<'split'>) => {
		stateGame.specialBarActiveKind = 'split';
		await applySplit(bookEvent, 'split');
		stateGame.specialBarActiveKind = null;
	},
	splitGang: async (bookEvent: BookEventOfType<'splitGang'>) => {
		stateGame.specialBarActiveKind = 'split';
		await applySplit(bookEvent, 'split');
		stateGame.specialBarActiveKind = null;
	},
	splitOutlaws: async (bookEvent: BookEventOfType<'splitOutlaws'>) => {
		stateGame.specialBarActiveKind = 'split';
		await applySplit(bookEvent, 'stretch');
		stateGame.specialBarActiveKind = null;
	},
	// NUDGE WAYS — reel 2 or 3 slams down, doubling ways on every notch
	nudgeWays: async (bookEvent: BookEventOfType<'nudgeWays'>) => {
		stateGame.specialBarActiveKind = 'nudge';
		const cells = filterVisibleCells(bookEvent.cells);
		const newBoard = rawBoardCopy();
		cells.forEach(({ reel, row, multiplier }) => {
			if (newBoard[reel]?.[row]) {
				newBoard[reel][row] = {
					...newBoard[reel][row],
					name: 'W',
					multiplier,
				};
			}
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
		parkCells(cells);
		await eventEmitter.broadcastAsync({
			type: 'nudgeWaysShow',
			reel: bookEvent.reel,
			fullReel: bookEvent.fullReel,
			startRow: bookEvent.startRow,
			initialWays: bookEvent.initialWays,
			finalWays: bookEvent.finalWays,
			steps: bookEvent.steps,
		});
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await fxHold();
		stateGame.specialBarActiveKind = null;
	},
	// SUPERSPLIT — the last-reel lane turns wild (stays 1-high) and every
	// paying symbol on the board splits
	superSplit: async (bookEvent: BookEventOfType<'superSplit'>) => {
		stateGame.lidOpen = true; // the lane fired, so it can't still be boarded
		// the lane announces itself: golden crossed revolvers flash in the cell
		await eventEmitter.broadcastAsync({ type: 'laneCardShow', kind: 'supersplit' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		const last = stateGame.board.length - 1;

		const newBoard = rawBoardCopy();
		// only the visible lane cell becomes wild — never grow the last reel
		bookEvent.wildCells
			.filter(({ reel, row }) => reel === last && row === 1)
			.forEach(({ reel, row }) => {
				if (newBoard[reel]?.[row]) {
					newBoard[reel][row] = { ...newBoard[reel][row], name: 'W' };
				}
			});
		if (newBoard[last]?.[1]) {
			newBoard[last][1] = { ...newBoard[last][1], name: 'W' };
		}
		bookEvent.cells.forEach(({ reel, row, multiplier }) => {
			if (reel === last) return;
			if (newBoard[reel]?.[row]) {
				newBoard[reel][row] = { ...newBoard[reel][row], multiplier };
			}
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
		const splitCells = filterVisibleCells(bookEvent.cells.filter(({ reel }) => reel !== last));
		parkCells([{ reel: last, row: 1 }, ...splitCells]);

		await eventEmitter.broadcastAsync({
			type: 'targetLockShow',
			cells: [{ reel: last, row: 1 }],
			tone: 'clone',
		});
		shakeBoard({ intensity: 12, duration: fxDur(320) });
		await animateSymbols({ positions: [{ reel: last, row: 1 }] });

		await eventEmitter.broadcastAsync({
			type: 'splitPanesShow',
			cells: splitCells.map(({ reel, row, multiplier }) => ({
				reel,
				row,
				count: multiplier,
			})),
		});

		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await fxHold();
	},
	// BOUNTY — a premium drops into the last-reel lane with a WIN multiplier
	bounty: async (bookEvent: BookEventOfType<'bounty'>) => {
		stateGame.lidOpen = true;
		await eventEmitter.broadcastAsync({ type: 'laneCardShow', kind: 'bounty' });
		eventEmitter.broadcast({ type: 'winMultUpdate', value: bookEvent.winMult });
		await applyBounty(bookEvent);
		await fxHold();
	},
	// MARK — last-reel shooter fires at every premium, +1 stacked WIN multi each
	shooter: async (bookEvent: BookEventOfType<'shooter'>) => {
		stateGame.lidOpen = true;
		await eventEmitter.broadcastAsync({ type: 'laneCardShow', kind: 'shooter' });
		const last = stateGame.board.length - 1;
		const origin = { reel: last, row: 1 };
		const hits = filterVisibleCells(bookEvent.hits);
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_gunshot' });
		if (hits.length) {
			await eventEmitter.broadcastAsync({
				type: 'targetLockShow',
				cells: hits,
				tone: 'clone',
			});
		}
		const start = Math.max(1, bookEvent.winMult - bookEvent.added);
		eventEmitter.broadcast({ type: 'winMultUpdate', value: start });
		let running = start;
		for (const cell of hits) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_gunshot' });
			shakeBoard({ intensity: 6, duration: fxDur(140) });
			await eventEmitter.broadcastAsync({
				type: 'featureBurstShow',
				kind: 'gunsmoke',
				cells: [cell],
			});
			running += 1;
			eventEmitter.broadcast({ type: 'winMultUpdate', value: running });
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up' });
		}
		eventEmitter.broadcast({ type: 'winMultUpdate', value: bookEvent.winMult });
		await eventEmitter.broadcastAsync({
			type: 'stretchWaysShow',
			cells: [{ ...origin, multiplier: bookEvent.winMult }],
		});
		await fxHold();
	},
	specialsWild: async (bookEvent: BookEventOfType<'specialsWild'>) => {
		const cells = filterVisibleCells(bookEvent.cells);
		if (!cells.length) return;
		await eventEmitter.broadcastAsync({ type: 'gunsmokeGunHide' });
		await playWildFlip(cells);
		await fxHold();
	},
	winMult: async (bookEvent: BookEventOfType<'winMult'>) => {
		eventEmitter.broadcast({ type: 'winMultUpdate', value: bookEvent.winMult });
	},
	// NUDGE — xNudge sideways. The NUDGE WILD (its own card) drops into the last
	// lane, then racks LEFT one mechanical notch per reel, stepping onto exactly
	// one cell of each column (half-steps and diagonals where the diamond rows
	// don't line up) and coming to rest on the FIRST reel's middle cell. Every
	// cell it steps through is left as a nudge-branded WILD, and every premium
	// it crushes bumps the WIN multiplier. Like gunsmoke, the board is swapped
	// UP FRONT and NudgeSlide covers each cell with a ghost of the old card
	// until the rider's impact knocks that card out.
	nudge: async (bookEvent: BookEventOfType<'nudge'>) => {
		stateGame.lidOpen = true; // the lane fired, so it can't still be boarded
		// the golden spur flashes in the lane before the rider is blasted out
		await eventEmitter.broadcastAsync({ type: 'laneCardShow', kind: 'nudge' });
		const reel = stateGame.board.length - 1;
		const cell = { reel, row: 1 };
		const premiums = new Set(['H1', 'H2', 'H3', 'H4', 'H5']);

		// the NUDGE WILD lands in the lane wearing its own face (the lane cell
		// is the rider's origin, so its wild is part of the wake too)
		const newBoard = rawBoardCopy();
		if (newBoard[reel]?.[1]) {
			newBoard[reel][1] = { ...newBoard[reel][1], name: 'W', nudged: true };
		}
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
		parkCells([cell]);

		// the walk comes from the book; for older books (premium hits only)
		// derive a straight-as-possible walk that still visits every reel
		let rawSteps = bookEvent.steps?.map((s) => ({ ...s })) ?? [];
		if (!rawSteps.length) {
			const byReel = new Map((bookEvent.hits ?? []).map((h) => [h.reel, h]));
			for (let r = reel - 1; r >= 0; r--) {
				const strip = stateGameDerived.boardRaw()[r] ?? [];
				const mid = Math.floor((strip.length - 1) / 2);
				const hit = byReel.get(r);
				rawSteps.push({ reel: r, row: hit?.row ?? mid, name: hit?.name });
			}
		}

		// the diamond board pads short reels — only step on cells that exist
		const stepCells = rawSteps.filter(
			({ reel: r, row }) => filterVisibleCells([{ reel: r, row }]).length && r !== reel,
		);
		const steps = stepCells.map((s) => {
			const from = (stateGameDerived.boardRaw()[s.reel]?.[s.row]?.name ??
				'H1') as RawSymbol['name'];
			return {
				reel: s.reel,
				row: s.row,
				from,
				premium: s.premium ?? premiums.has(from),
			};
		});

		// swap the whole wake to nudge wilds before the ride; each one stays
		// hidden behind its ghost card until the rider knocks that card out
		if (steps.length) {
			const wildBoard = rawBoardCopy();
			steps.forEach(({ reel: r, row }) => {
				if (wildBoard[r]?.[row]) {
					wildBoard[r][row] = { ...wildBoard[r][row], name: 'W', nudged: true };
				}
			});
			eventEmitter.broadcast({ type: 'boardSettle', board: wildBoard });
			parkCells(steps);
		}

		await eventEmitter.broadcastAsync({
			type: 'nudgeSlideShow',
			baseMult: bookEvent.baseMult,
			winMult: bookEvent.winMult,
			steps,
		});

		// leave the final WIN mult badge where the rider came to rest
		const rest = steps[steps.length - 1] ?? cell;
		await eventEmitter.broadcastAsync({
			type: 'stretchWaysShow',
			cells: [{ reel: rest.reel, row: rest.row, multiplier: bookEvent.winMult }],
		});
		await fxHold();
	},
	// ------------------------------------------------------------------
	// BONUS ROUNDS: 3 scatters -> SMALL BONUS (bar awake all round),
	// 4+ -> BIG BONUS (grave lane open all round on top)
	// ------------------------------------------------------------------
	freeSpinTrigger: async (bookEvent: BookEventOfType<'freeSpinTrigger'>) => {
		const tier = bookEvent.positions.length >= 4 ? 'superspins' : 'freespins';

		// celebrate the scatters that did it
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_special_hit' });
		shakeBoard({ intensity: 5, duration: fxDur(220) });
		await animateSymbols({ positions: filterVisibleCells(bookEvent.positions) });

		// the BIG BONUS keeps the grave lane dug up for the whole round —
		// the reveal handler drops laneSuper again when base game resumes
		if (tier === 'superspins') {
			stateGame.laneSuper = true;
			stateGame.lidOpen = true;
		}

		// announce the round. A BOUGHT round already showed this exact banner
		// at round start (presentBonusEntry awaits it before the first reveal),
		// so only NATURAL triggers banner here.
		const buyKey = stateBet.activeBetModeKey?.toLowerCase();
		if (buyKey !== 'freespins' && buyKey !== 'superspins') {
			await eventEmitter.broadcastAsync({ type: 'bonusEntryShow', tier });
		}

		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: 0,
			total: bookEvent.totalFs,
		});
		eventEmitter.broadcast({ type: 'winMultUpdate', value: 1 });
	},
	updateFreeSpin: async (bookEvent: BookEventOfType<'updateFreeSpin'>) => {
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: bookEvent.amount,
			total: bookEvent.total,
		});
	},
	freeSpinEnd: async (_bookEvent: BookEventOfType<'freeSpinEnd'>) => {
		// the round total is celebrated by setWin/finalWin like every book —
		// this only strikes the round chrome
		eventEmitter.broadcast({ type: 'freeSpinCounterHide' });
		eventEmitter.broadcast({ type: 'winMultUpdate', value: 1 });
		stateGame.gameType = 'basegame';
		stateGame.laneSuper = false;
	},
	// the 1-in-100 UPGRADE: a 4th scatter dropped mid small-bonus round — the
	// lane blasts open for the rest of the round and the spins top back up
	bonusUpgrade: async (bookEvent: BookEventOfType<'bonusUpgrade'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_special_hit' });
		await animateSymbols({ positions: filterVisibleCells([bookEvent.position]) });

		// the boarded lane cover breaks away (LaneLidLock) and STAYS off
		shakeBoard({ intensity: 8, duration: fxDur(300) });
		stateGame.laneSuper = true;
		stateGame.lidOpen = true;
		const lane = filterVisibleCells([{ reel: stateGame.board.length - 1, row: 1 }]);
		await eventEmitter.broadcastAsync({
			type: 'featureBurstShow',
			kind: 'digUp',
			cells: lane,
		});

		// the upgrade IS an entry into the big bonus — full takeover banner
		await eventEmitter.broadcastAsync({ type: 'bonusEntryShow', tier: 'superspins' });

		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: bookEvent.spin,
			total: bookEvent.totalFs,
		});
	},
	// the 99,999x cap — the celebration itself rides on the win amount below
	wincap: async (_bookEvent: BookEventOfType<'wincap'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_thunder' });
	},
	setTotalWin: async (bookEvent: BookEventOfType<'setTotalWin'>) => {
		stateBet.winBookEventAmount = bookEvent.amount;
	},
	setWin: async (bookEvent: BookEventOfType<'setWin'>) => {
		await presentWinCelebration(bookEvent.amount);
	},
	finalWin: async (bookEvent: BookEventOfType<'finalWin'>) => {
		// A capped book pays out through wincap + setTotalWin and carries NO
		// setWin, so the biggest wins in the game used to present nothing at all.
		// finalWin is the backstop: celebrate the round total whenever this spin
		// never presented, and stay silent when setWin already did.
		if (winPresented) return;
		await presentWinCelebration(bookEvent.amount);
	},
	// customised
	createBonusSnapshot: async (bookEvent: BookEventOfType<'createBonusSnapshot'>) => {
		const { bookEvents } = bookEvent;
		const lastSetTotalWinEvent = _.findLast(
			bookEvents,
			(event) => event.type === 'setTotalWin',
		) as BookEventOfType<'setTotalWin'> | undefined;
		if (lastSetTotalWinEvent) playBookEvent(lastSetTotalWinEvent, { bookEvents });
	},
};
