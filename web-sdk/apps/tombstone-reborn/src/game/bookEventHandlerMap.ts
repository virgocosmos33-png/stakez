import _ from 'lodash';
import { tick } from 'svelte';

import { recordBookEvent, checkIsMultipleRevealEvents, type BookEventHandlerMap } from 'utils-book';
import { stateBet, stateBetDerived } from 'state-shared';
import { fxWait, fxDur } from './fxTiming';

import { SYMBOL_SIZE } from './constants';
import { eventEmitter } from './eventEmitter';
import { playBookEvent } from './utils';
import { getWinCelebration } from './winCelebrationMap';
import type { MusicName, SoundEffectName } from './sound';
import { stateGame, stateGameDerived } from './stateGame.svelte';
import { shakeBoard } from './stateShake.svelte';
import { isMegaWin } from './winConnection';
import type { BookEvent, BookEventOfType, BookEventContext } from './typesBookEvent';
import type { Position, RawSymbol } from './types';

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
		for (const name of [
			'bgm_winlevel_big',
			'bgm_winlevel_superwin',
			'bgm_winlevel_mega',
			'bgm_winlevel_epic',
			'bgm_winlevel_max',
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
const visibleWinPositions = (positions: Position[]): Position[] =>
	positions.filter(({ reel, row }) => {
		const len = stateGame.board[reel]?.reelState.symbols.length ?? 0;
		return len >= 3 && row >= 1 && row <= len - 2;
	});

// How many ways actually connected this spin (summed in winInfo, shown in setWin).
let connectedWays = 0;

/** shared by splitGang / splitOutlaws: mark the targets, stamp the per-cell
 * ways multipliers, tear the panes apart, climb the WAYS rail. */
const applySplit = async (
	bookEvent: BookEventOfType<'splitGang'> | BookEventOfType<'splitOutlaws'>,
	tone: 'split' | 'stretch' | 'clone',
) => {
	eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });

	await eventEmitter.broadcastAsync({
		type: 'targetLockShow',
		cells: bookEvent.cells.map(({ reel, row }) => ({ reel, row })),
		tone,
	});

	const newBoard = rawBoardCopy();
	bookEvent.cells.forEach(({ reel, row, multiplier }) => {
		if (newBoard[reel]?.[row]) {
			newBoard[reel][row] = { ...newBoard[reel][row], multiplier };
		}
	});
	eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });

	await eventEmitter.broadcastAsync({
		type: 'splitPanesShow',
		cells: bookEvent.cells.map(({ reel, row, multiplier }) => ({
			reel,
			row,
			count: multiplier,
		})),
	});

	eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
	await fxWait(150);
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
	eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });

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
		stateGame.slotWinPositions = [];
		stateGame.featureCells = [];
		stateGame.reelStretch = stateGame.reelStretch.map(() => null);
		eventEmitter.broadcast({ type: 'splitPanesHide' });
		eventEmitter.broadcast({ type: 'cloneMorphHide' });
		eventEmitter.broadcast({ type: 'stretchWaysHide' });
		eventEmitter.broadcast({ type: 'cellLightningHide' });
		stateGame.revealNonce += 1;
		stateGame.slotsReleased = false;

		connectedWays = 0;
		eventEmitter.broadcast({ type: 'waysCounterHide' });

		const spinning = stateGameDerived.enhancedBoard.spin({ revealEvent: bookEvent });
		await tick();
		stateGame.slotsReleased = true;
		await spinning;
	},
	winInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
		const betCost = stateBetDerived.betCost();
		const megaWin = bookEvent.wins.find((win) => isMegaWin(win.win, betCost));

		// every way that paid, across all winning symbols
		connectedWays = bookEvent.wins.reduce((total, win) => total + (win.meta?.ways ?? 0), 0);
		if (connectedWays > 0) {
			eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: connectedWays });
		}

		if (!megaWin) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
		}

		// Feature glass has done its job — clear it so the win dim/sweep reads
		// the board symbols, not White Room pane overlays on top of them.
		eventEmitter.broadcast({ type: 'splitPanesHide' });

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
	// The top special bar resolves its cards. The cards themselves are shown by
	// the SpecialBar component (reads stateGame.specialBar); each card's EFFECT
	// plays in its own following event.
	specialBar: async (bookEvent: BookEventOfType<'specialBar'>) => {
		stateGame.specialBar = bookEvent.cells;
		if (bookEvent.cells.length > 0) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
			shakeBoard({ intensity: 4, duration: fxDur(180) });
			await fxWait(650);
		}
	},
	// DIG UP — the last-reel lane cracks open for this spin
	digUp: async (bookEvent: BookEventOfType<'digUp'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		shakeBoard({ intensity: 7, duration: fxDur(260) });
		await animateSymbols({ positions: [{ reel: bookEvent.reel, row: 1 }] });
		await fxWait(200);
	},
	// TOMBSTONE OPEN — the reel under each coffin card grows by at most +1.
	// The last-reel special lane is never grown. Grown height + buried symbol
	// stay on the board until the next reveal resets authored heights.
	coffinOpen: async (bookEvent: BookEventOfType<'coffinOpen'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		const last = stateGame.board.length - 1;

		const newBoard = rawBoardCopy();
		const grown: Position[] = [];
		const grownReels = new Set<number>();
		bookEvent.reels.forEach(({ reel, newCells }) => {
			if (reel === last) return; // special lane — never expand
			const strip = newBoard[reel];
			if (!strip) return;
			// clamp to a single extra symbol even if an old book asks for more
			const added = newCells.slice(0, 1);
			if (!added.length) return;
			const bottomPad = strip[strip.length - 1];
			const body = strip.slice(0, strip.length - 1);
			newBoard[reel] = [...body, ...added.map(({ name }) => ({ name })), bottomPad];
			grown.push({ reel, row: body.length }); // padded row of the new cell
			grownReels.add(reel);
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
		await tick();

		// park the WHOLE grown reel so every row's Y matches the new length;
		// SymbolWrap culls anything outside the live window.
		grownReels.forEach((reel) => parkReel(reel));

		await eventEmitter.broadcastAsync({
			type: 'targetLockShow',
			cells: grown,
			tone: 'stretch',
		});
		shakeBoard({ intensity: 9, duration: fxDur(280) });
		await landCells(grown);

		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await fxWait(150);
	},
	// GUNSMOKE — every copy of one symbol type morphs into the revolver WILD
	gunsmoke: async (bookEvent: BookEventOfType<'gunsmoke'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });

		// mark every copy while it is still the old symbol
		await eventEmitter.broadcastAsync({
			type: 'targetLockShow',
			cells: bookEvent.cells.map(({ reel, row }) => ({ reel, row })),
			tone: 'clone',
		});

		// swap underneath, hidden by the morph overlay (keep any split multiplier)
		const newBoard = rawBoardCopy();
		bookEvent.cells.forEach(({ reel, row }) => {
			if (newBoard[reel]?.[row]) {
				newBoard[reel][row] = { ...newBoard[reel][row], name: 'W' };
			}
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
		parkCells(bookEvent.cells);

		// play the morph: every copy charges, flashes and becomes the revolver
		await eventEmitter.broadcastAsync({
			type: 'cloneMorphShow',
			cells: bookEvent.cells.map(({ reel, row }) => ({ reel, row })),
			from: bookEvent.symbol,
			to: 'W',
		});
		eventEmitter.broadcast({ type: 'cloneMorphHide' });
		await animateSymbols({ positions: bookEvent.cells });

		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await fxWait(160);
	},
	// SPLIT-GANG — every premium on the board splits (+factor ways each)
	splitGang: async (bookEvent: BookEventOfType<'splitGang'>) => {
		await applySplit(bookEvent, 'split');
	},
	// SPLIT-OUTLAWS — every low on the board splits (+factor ways each)
	splitOutlaws: async (bookEvent: BookEventOfType<'splitOutlaws'>) => {
		await applySplit(bookEvent, 'stretch');
	},
	// SUPERSPLIT — the last-reel lane turns wild (stays 1-high) and every
	// paying symbol on the board splits
	superSplit: async (bookEvent: BookEventOfType<'superSplit'>) => {
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
		const splitCells = bookEvent.cells.filter(({ reel }) => reel !== last);
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
		await fxWait(150);
	},
	// BOUNTY — a premium drops into the last-reel lane with a WIN multiplier
	bounty: async (bookEvent: BookEventOfType<'bounty'>) => {
		await applyBounty(bookEvent);
		await fxWait(150);
	},
	// NUDGE — premium lifts out of the last lane and slides LEFT; WIN mult
	// climbs for every premium it passes, and each hit cell is left as a WILD
	// (NudgeSlide swaps the board symbols mid-slide).
	nudge: async (bookEvent: BookEventOfType<'nudge'>) => {
		const reel = stateGame.board.length - 1;
		const cell = { reel, row: 1 };

		// land the premium in the lane first (base mult), then slide
		const newBoard = rawBoardCopy();
		if (newBoard[reel]?.[1]) {
			newBoard[reel][1] = { ...newBoard[reel][1], name: bookEvent.symbol };
		}
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });
		parkCells([cell]);

		// derive a hit path from the live board if the book is older and has no hits
		let hits = bookEvent.hits?.map(({ reel: r, row }) => ({ reel: r, row })) ?? [];
		if (!hits.length) {
			const premiums = new Set(['H1', 'H2', 'H3', 'H4', 'H5']);
			for (let r = reel - 1; r >= 0; r--) {
				const strip = stateGameDerived.boardRaw()[r] ?? [];
				for (let row = 1; row < strip.length - 1; row++) {
					if (premiums.has(strip[row]?.name)) hits.push({ reel: r, row });
				}
			}
		}

		await eventEmitter.broadcastAsync({
			type: 'nudgeSlideShow',
			symbol: bookEvent.symbol,
			baseMult: bookEvent.baseMult,
			winMult: bookEvent.winMult,
			hits,
		});

		// leave the final WIN mult badge on the lane
		await eventEmitter.broadcastAsync({
			type: 'stretchWaysShow',
			cells: [{ ...cell, multiplier: bookEvent.winMult }],
		});
		await fxWait(120);
	},
	// the 99,999x cap — the celebration itself is driven by setWin's win level
	wincap: async (_bookEvent: BookEventOfType<'wincap'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_thunder' });
	},
	setTotalWin: async (bookEvent: BookEventOfType<'setTotalWin'>) => {
		stateBet.winBookEventAmount = bookEvent.amount;
	},
	setWin: async (bookEvent: BookEventOfType<'setWin'>) => {
		// the celebration tier is chosen by win amount in bet multiples
		const celebration = getWinCelebration(bookEvent.amount);

		if (connectedWays > 0) {
			eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: connectedWays });
		}

		eventEmitter.broadcast({ type: 'winShow' });
		winLevelSoundsPlay({ winLevelData: celebration });
		await eventEmitter.broadcastAsync({
			type: 'winUpdate',
			amount: bookEvent.amount,
			ways: connectedWays,
		});
		winLevelSoundsStop();
		eventEmitter.broadcast({ type: 'winHide' });

		eventEmitter.broadcast({ type: 'winCycleStart' });
	},
	finalWin: async (bookEvent: BookEventOfType<'finalWin'>) => {
		// Do nothing — setWin owns the celebration
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
