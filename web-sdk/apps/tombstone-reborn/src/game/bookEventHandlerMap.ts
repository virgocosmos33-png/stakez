import _ from 'lodash';
import { tick } from 'svelte';

import { recordBookEvent, checkIsMultipleRevealEvents, type BookEventHandlerMap } from 'utils-book';
import { stateBet, stateBetDerived } from 'state-shared';
import { fxWait, fxDur, fxHold } from './fxTiming';

import { SYMBOL_SIZE } from './constants';
import { eventEmitter } from './eventEmitter';
import { playBookEvent } from './utils';
import { filterGunsmokeCells, filterSplitCells, filterVisibleCells, isNudgeCoveredReel } from './boardCells';
import { isHighPaySymbol, planWoundRhythm, volleySeed } from './gunsmokeSpin';
import { LANE_DOOR_OPEN_MS } from './laneDoor';
import { musicForBonusTier, restoreBaseMusic, resumeModeBeds, stopBonusBgm } from './bonusBgm';
import { getWinCelebration } from './winCelebrationMap';
import type { MusicName, SoundEffectName } from './sound';
import { stateGame, stateGameDerived } from './stateGame.svelte';
import { atmosphereFromMode, syncAtmosphere } from './atmosphere.svelte';
import { shakeBoard } from './stateShake.svelte';
import { isMegaWin } from './winConnection';
import type { BookEvent, BookEventOfType, BookEventContext } from './typesBookEvent';
import type { Position, RawSymbol, SymbolName } from './types';

/** Nudge events that belong to this reveal — not the first one in a 10-spin book. */
const nudgeWaysInReveal = (
	reveal: BookEventOfType<'reveal'>,
	bookEvents: BookEvent[],
): BookEventOfType<'nudgeWays'>[] => {
	let start = bookEvents.indexOf(reveal);
	if (start < 0) {
		start = bookEvents.findIndex((event) => event.type === 'reveal' && event.index === reveal.index);
	}
	if (start < 0) return [];
	const rest = bookEvents.slice(start + 1);
	const nextReveal = rest.findIndex((event) => event.type === 'reveal');
	const window = nextReveal < 0 ? rest : rest.slice(0, nextReveal);
	return window.filter((event): event is BookEventOfType<'nudgeWays'> => event.type === 'nudgeWays');
};

/** Every nudgeWays that belongs to the same reveal as this one. */
const nudgeWaysInSameReveal = (
	event: BookEventOfType<'nudgeWays'>,
	bookEvents: BookEvent[],
): BookEventOfType<'nudgeWays'>[] => {
	const at = bookEvents.findIndex((item) => item.type === 'nudgeWays' && item.index === event.index);
	if (at < 0) return [event];
	const reveal = bookEvents.slice(0, at + 1).findLast((item) => item.type === 'reveal');
	if (!reveal || reveal.type !== 'reveal') return [event];
	return nudgeWaysInReveal(reveal, bookEvents);
};

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
	if (winLevelData?.sound?.bgm && winLevelData.type !== 'big') {
		// Big-win plates own their scene tracks inside WinCelebration so a
		// rollup always starts at scene 1. Playing the final tier here would
		// start the wrong song for one frame.
		eventEmitter.broadcast({ type: 'soundMusic', name: winLevelData.sound.bgm });
	}
};

const winLevelSoundsStop = () => {
	eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_bigwin_coinloop' });
	resumeModeBeds();
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

/** Keep win overlays on live visible cells only (skip pads / nudge totem). */
const visibleWinPositions = (positions: Position[]): Position[] => filterGunsmokeCells(positions);

/** One paying face per beat — merge every way of the same symbol. */
const groupWinsBySymbol = (
	wins: BookEventOfType<'winInfo'>['wins'],
): Position[][] => {
	const bySymbol = new Map<string, Position[]>();
	for (const win of wins) {
		const positions = visibleWinPositions(win.positions);
		if (!positions.length) continue;
		const existing = bySymbol.get(win.symbol) ?? [];
		const seen = new Set(existing.map((cell) => `${cell.reel}-${cell.row}`));
		for (const cell of positions) {
			const key = `${cell.reel}-${cell.row}`;
			if (seen.has(key)) continue;
			seen.add(key);
			existing.push(cell);
		}
		bySymbol.set(win.symbol, existing);
	}
	return [...bySymbol.values()];
};

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
	// Bought single-spin bonuses are basegame books. Kill the bonus bed
	// before the plate so resumeModeBeds comes back on bgm_main, not Showdown.
	if (stateGame.gameType !== 'freegame') stopBonusBgm();

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

/** SPLIT cards still on the board — they get cut into a split wild too. */
const splitCardCells = (): Position[] => {
	const found: Position[] = [];
	stateGame.board.forEach((reel, reelIndex) => {
		reel.reelState.symbols.forEach((symbol, row) => {
			if (symbol.rawSymbol.name === 'SP') found.push({ reel: reelIndex, row });
		});
	});
	return filterSplitCells(found);
};

/** Climb a parked nudge totem when a later split doubles its stack. */
const punchNudgeWays = (cells: { reel: number; multiplier?: number }[]) => {
	const byReel = new Map<number, number>();
	for (const cell of cells) {
		if (cell.multiplier == null || !isNudgeCoveredReel(cell.reel)) continue;
		byReel.set(cell.reel, Math.max(byReel.get(cell.reel) ?? 0, cell.multiplier));
	}
	for (const [reel, ways] of byReel) {
		eventEmitter.broadcast({ type: 'nudgeWaysPunch', reel, ways });
	}
};

/** shared by split / splitGang / splitOutlaws: mark the targets, stamp the
 * per-cell ways multipliers, tear the panes apart, climb the WAYS rail.
 * The SPLIT card itself is slashed into a stacked wild with the same factor. */
const applySplit = async (
	bookEvent:
		| BookEventOfType<'split'>
		| BookEventOfType<'splitGang'>
		| BookEventOfType<'splitOutlaws'>,
	tone: 'split' | 'stretch' | 'clone',
) => {
	eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
	// Pad / mid-shove cells stay out. A parked nudge stack is a legal split
	// target — the book already doubled those ways.
	const cells = filterSplitCells(bookEvent.cells);
	const factor = Math.max(2, bookEvent.factor ?? 2);
	const sources = splitCardCells();
	if (!cells.length && !sources.length) {
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		return;
	}

	const lockCells = [
		...cells.map(({ reel, row }) => ({ reel, row })),
		...sources,
	];
	await eventEmitter.broadcastAsync({
		type: 'targetLockShow',
		cells: lockCells,
		tone,
	});

	const newBoard = rawBoardCopy();
	cells.forEach(({ reel, row, multiplier }) => {
		if (newBoard[reel]?.[row]) {
			newBoard[reel][row] = { ...newBoard[reel][row], multiplier };
		}
	});
	sources.forEach(({ reel, row }) => {
		if (newBoard[reel]?.[row]) {
			newBoard[reel][row] = { ...newBoard[reel][row], name: 'W', multiplier: factor };
		}
	});
	eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
	parkCells(sources);

	await eventEmitter.broadcastAsync({
		type: 'splitPanesShow',
		cells: [
			...cells.map(({ reel, row, multiplier }) => ({
				reel,
				row,
				count: multiplier,
			})),
			...sources.map(({ reel, row }) => ({
				reel,
				row,
				count: factor,
				name: 'W' as const,
			})),
		],
	});

	eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
	punchNudgeWays(cells);
	if ('added' in bookEvent && (bookEvent.added ?? 0) > 0 && bookEvent.winMult != null) {
		tickWinMultHud(bookEvent.winMult);
	}
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

/** GUNSMOKE: each pistol hit stamps that cell and flips it to WILD, then the next. */
const playGunsmokeShoot = async (
	cells: { reel: number; row: number }[],
	from: SymbolName,
	opts?: { onShot?: () => void },
) => {
	const visible = filterVisibleCells(cells);
	if (!visible.length) return;
	const blood = isHighPaySymbol(from);
	const rhythm = planWoundRhythm(visible.length, volleySeed(visible));
	for (let i = 0; i < visible.length; i += 1) {
		const cell = visible[i];
		if (!cell) continue;
		const shot = rhythm[i];
		shakeBoard({ intensity: 4 + (shot?.flightScale ?? 1) * 2, duration: fxDur(90) });
		opts?.onShot?.();
		await eventEmitter.broadcastAsync({
			type: 'gunsmokeWound',
			reel: cell.reel,
			row: cell.row,
			blood,
			name: from,
			beatMs: 0,
			flightScale: shot?.flightScale,
			side: shot?.side,
		});
		await playWildFlip([{ ...cell, from }], { shoot: false });
		if ((shot?.beatMs ?? 0) > 0) await fxWait(shot.beatMs);
	}
};

/** Last-reel premium WAYS badge — HUD WIN multi is a separate stack. */
const showLanePremiumWays = async (ways: number, cells?: { reel: number; row: number; multiplier: number }[]) => {
	const last = stateGame.board.length - 1;
	const shown = cells?.length
		? cells
		: [{ reel: last, row: 1, multiplier: ways }];
	const newBoard = rawBoardCopy();
	shown.forEach(({ reel, row, multiplier }) => {
		if (newBoard[reel]?.[row]) {
			newBoard[reel][row] = { ...newBoard[reel][row], multiplier };
		}
	});
	eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
	await eventEmitter.broadcastAsync({
		type: 'stretchWaysShow',
		cells: shown,
	});
};

const setWinMultHud = (value: number) => {
	eventEmitter.broadcast({ type: 'winMultUpdate', value: Math.max(1, value) });
};

const tickWinMultHud = (value: number) => {
	setWinMultHud(value);
	eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_up', forcePlay: true });
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
			setWinMultHud(1);
		} else if (bookEvent.gameType === 'freegame' && !stateGame.laneSuper) {
			// SMALL bonus: reset the WIN stack every spin. SUPER keeps it.
			setWinMultHud(1);
		}
		if (bookEvent.gameType === 'freegame') {
			syncAtmosphere(stateGame.laneSuper ? 'super' : 'small');
		} else {
			syncAtmosphere(atmosphereFromMode(stateBet.activeBetModeKey) ?? 'base');
		}
		stateGame.lidOpen = stateGame.laneSuper;
		stateGame.laneCardSwap = 0;
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
		stateGame.nudgeCoverReels = [];
		stateGame.nudgeCoverCells = [];
		stateGame.pendingNudges = nudgeWaysInReveal(bookEvent, bookEvents).map((nudgeEv) => ({
			reel: nudgeEv.reel,
			fullReel: nudgeEv.fullReel,
			startRow: nudgeEv.startRow,
			initialWays: nudgeEv.initialWays,
		}));

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

		// Shine stays silent. The gold ways / amount overlay plays the dramatic
		// sting once in presentWinCelebration — a harmonica chirp here used to
		// fire first and make a small win sound cheerful.

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

		const winGroups = groupWinsBySymbol(bookEvent.wins);

		try {
			for (const positions of winGroups) {
				if (skipped) break;
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

		// Hold the last shine group. Do NOT start the idle cycle here — it used
		// to run under the celebration overlay (lantern sweep + dim every beat)
		// and hitch every winning Storybook. presentWinCelebration starts it
		// after the takeover closes.
		eventEmitter.broadcast({ type: 'winCycleSet', wins: winGroups });
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
			syncAtmosphere('super');
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
			syncAtmosphere('super');
		}
		if (bookEvent.cells.length > 0) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_special_hit' });
			shakeBoard({ intensity: 4, duration: fxDur(180) });
			// Do not lock every planted card here — each following feature
			// locks its own targets. A board-wide lock then a second lock is
			// the stacked-reticle glitch.
			await fxHold();
		}
	},
	// SUPER scatter opened the last-reel lane this spin. The door swings
	// open (LaneLidLock + door-creak). No shovel plant.
	tombstone: async (bookEvent: BookEventOfType<'tombstone'>) => {
		stateGame.specialBarActiveKind = 'tombstone';
		shakeBoard({ intensity: 7, duration: fxDur(260) });
		stateGame.lidOpen = true;
		await fxWait(LANE_DOOR_OPEN_MS);
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
		const cells = filterGunsmokeCells(bookEvent.cells);
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

		const added = bookEvent.added ?? 0;
		const endMult = bookEvent.winMult ?? 1;
		let running = Math.max(1, endMult - added);
		if (added > 0) setWinMultHud(running);
		await playGunsmokeShoot(cells, bookEvent.symbol as SymbolName, {
			onShot: () => {
				if (added <= 0) return;
				running = Math.min(endMult, running + 1);
				tickWinMultHud(running);
			},
		});
		if (added > 0) setWinMultHud(endMult);
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
	// NUDGE WAYS — each landed cell grows down a notch at a time. Two on the
	// same spin drop together; the second event is a no-op after the batch.
	// Do NOT wild the rows below the totem up front — those faces stay as
	// they landed and get shoved off. Stamp the stack only after the totem
	// has covered them.
	nudgeWays: async (bookEvent: BookEventOfType<'nudgeWays'>, { bookEvents }: BookEventContext) => {
		const batch = nudgeWaysInSameReveal(bookEvent, bookEvents);
		if (batch[0]?.index !== bookEvent.index) return;

		stateGame.specialBarActiveKind = 'nudge';
		const stampWilds = (cells: (Position & { multiplier?: number })[]) => {
			const visible = filterVisibleCells(cells);
			if (!visible.length) return;
			const newBoard = rawBoardCopy();
			for (const cell of visible) {
				if (!newBoard[cell.reel]?.[cell.row]) continue;
				newBoard[cell.reel][cell.row] = {
					...newBoard[cell.reel][cell.row],
					name: 'W',
					...(cell.multiplier != null ? { multiplier: cell.multiplier } : {}),
				};
			}
			eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
			parkCells(visible);
		};

		for (const nudge of batch) {
			await eventEmitter.broadcastAsync({
				type: 'nudgeWaysShow',
				reel: nudge.reel,
				fullReel: nudge.fullReel,
				startRow: nudge.startRow,
				initialWays: nudge.initialWays,
				finalWays: nudge.finalWays,
				steps: nudge.steps,
				added: nudge.added ?? 0,
				winMult: nudge.winMult ?? 1,
			});
		}
		stampWilds(batch.flatMap((nudge) => nudge.cells));
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: batch[batch.length - 1].totalWays });
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
		const splitCells = filterSplitCells(bookEvent.cells.filter(({ reel }) => reel !== last));
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
		punchNudgeWays(splitCells);
		if ((bookEvent.added ?? 0) > 0 && bookEvent.winMult != null) {
			tickWinMultHud(bookEvent.winMult);
		}
		await fxHold();
	},
	// Last-reel premium: WAYS on the cell, not the HUD WIN stack.
	lanePremium: async (bookEvent: BookEventOfType<'lanePremium'>) => {
		stateGame.lidOpen = true;
		await showLanePremiumWays(bookEvent.ways, bookEvent.cells);
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await fxHold();
	},
	// Old books still emit `bounty`. Ignore the star — the following winMult
	// tick puts the multi on the HUD and the landed premium.
	bounty: async () => {
		stateGame.lidOpen = true;
	},
	// MARK — last-reel shooter fires at every premium, +1 WIN multi once
	shooter: async (bookEvent: BookEventOfType<'shooter'>) => {
		stateGame.lidOpen = true;
		const last = stateGame.board.length - 1;
		const newBoard = rawBoardCopy();
		if (newBoard[last]?.[1]) {
			newBoard[last][1] = { ...newBoard[last][1], name: 'W' };
		}
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
		parkCells([{ reel: last, row: 1 }]);
		await eventEmitter.broadcastAsync({ type: 'laneCardShow', kind: 'shooter' });
		const hits = filterVisibleCells(bookEvent.hits);
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_gunshot' });
		if (hits.length) {
			await eventEmitter.broadcastAsync({
				type: 'targetLockShow',
				cells: hits,
				tone: 'clone',
			});
		}
		for (const cell of hits) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_gunshot', forcePlay: true });
			shakeBoard({ intensity: 6, duration: fxDur(140) });
			await eventEmitter.broadcastAsync({
				type: 'featureBurstShow',
				kind: 'gunsmoke',
				cells: [cell],
			});
		}
		tickWinMultHud(bookEvent.winMult);
		await fxHold();
	},
	specialsWild: async (bookEvent: BookEventOfType<'specialsWild'>) => {
		const cells = filterVisibleCells(bookEvent.cells).filter(({ reel, row }) => {
			const name = stateGame.board[reel]?.reelState.symbols[row]?.rawSymbol.name;
			return name != null && name !== 'W';
		});
		if (!cells.length) return;
		await playWildFlip(cells);
		await fxHold();
	},
	winMult: async (bookEvent: BookEventOfType<'winMult'>) => {
		if (bookEvent.source === 'premium' || bookEvent.source === 'bounty') {
			// legacy books: this used to be a WIN tick. Treat it as WAYS only.
			stateGame.lidOpen = true;
			await showLanePremiumWays(bookEvent.winMult);
			return;
		}
		setWinMultHud(bookEvent.winMult);
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
		syncAtmosphere(tier === 'superspins' ? 'super' : 'small');

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

		eventEmitter.broadcast({
			type: 'soundMusic',
			name: musicForBonusTier(tier === 'superspins' ? 'superspins' : 'freespins'),
		});

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
		restoreBaseMusic();
		syncAtmosphere('base');
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
		syncAtmosphere('super');
		await fxWait(LANE_DOOR_OPEN_MS);

		// the upgrade IS an entry into the big bonus — full takeover banner
		eventEmitter.broadcast({ type: 'soundMusic', name: musicForBonusTier('superspins') });
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
