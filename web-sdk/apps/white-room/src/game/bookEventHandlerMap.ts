import _ from 'lodash';
import { backOut } from 'svelte/easing';

import { recordBookEvent, checkIsMultipleRevealEvents, type BookEventHandlerMap } from 'utils-book';
import { stateBet, stateBetDerived } from 'state-shared';
import { sequence } from 'utils-shared/sequence';
import { waitForTimeout } from 'utils-shared/wait';

import { SYMBOL_SIZE } from './constants';
import { eventEmitter } from './eventEmitter';
import { playBookEvent, getReelRows } from './utils';
import { winLevelMap, type WinLevel, type WinLevelData } from './winLevelMap';
import { getWinCelebration } from './winCelebrationMap';
import type { MusicName, SoundEffectName } from './sound';
import { stateGame, stateGameDerived } from './stateGame.svelte';
import { shakeBoard } from './stateShake.svelte';
import { isMegaWin } from './winConnection';
import type { BookEvent, BookEventOfType, BookEventContext } from './typesBookEvent';
import type { Position } from './types';

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
		// Kill Madam-era winlevel beds before starting the White Room celeb stage
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
	// no coin loop / no sfx_celeb_* layer — WinCelebration owns the evolving bed
};

const winLevelSoundsStop = () => {
	eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_bigwin_coinloop' });
	if (stateBet.activeBetModeKey === 'SUPERSPIN' || stateGame.gameType === 'freegame') {
		// check if SUPERSPIN, when finishing a bet.
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_freespin' });
	} else {
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_main' });
	}
	eventEmitter.broadcastAsync({ type: 'uiShow' });
};

const animateSymbols = async ({ positions }: { positions: Position[] }) => {
	eventEmitter.broadcast({ type: 'boardShow' });
	await eventEmitter.broadcastAsync({
		type: 'boardWithAnimateSymbols',
		symbolPositions: positions,
	});
};

// track the running free-spin total so a retrigger can announce the delta
// ("+N SPINS") — the book only sends the new grand total, never the increment
let lastFreeSpinTotal = 0;

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

		// Wild Reel may have grown middle reels last spin - restore their authored
		// diamond heights before this fresh reveal so the board spins in clean,
		// and re-lock the bottom special slots.
		stateGame.board.forEach((reel) => reel.resetToInitialHeight());
		stateGame.wildReelReels = [];
		stateGame.stretchedReels = [];
		stateGame.unlockedSlots = null;
		stateGame.slotWinPositions = [];
		stateGame.featureCells = [];
		// leaving the bonus (base-game reveal) re-locks every group; inside the
		// bonus the groups persist so open cells never flash a cosmetic teaser.
		if (bookEvent.gameType === 'basegame') stateGame.unlockedGroups = [];
		// drop any STRETCH display-height overrides so reels spin in at their
		// authored diamond heights (the board itself was already reset above).
		stateGame.reelStretch = stateGame.reelStretch.map(() => null);
		eventEmitter.broadcast({ type: 'wildReelSlideHide' });
		eventEmitter.broadcast({ type: 'splitPanesHide' });
		eventEmitter.broadcast({ type: 'cloneMorphHide' });
		eventEmitter.broadcast({ type: 'stretchFxHide' });
		eventEmitter.broadcast({ type: 'stretchWaysHide' });
		eventEmitter.broadcast({ type: 'cellLightningHide' });
		// new spin: LockedSlots re-rolls + re-drops the symbols reeling behind
		// each reserved cell (closed bars in base, open bars once unlocked).
		stateGame.revealNonce += 1;
		// park every special-cell symbol above its cell; they only reel in once the
		// MAIN board has finished dropping (released below), all together.
		stateGame.slotsReleased = false;

		await stateGameDerived.enhancedBoard.spin({ revealEvent: bookEvent });

		// Pre-fill EVERY special cell this spin will use — wild cards, unlocked-slot
		// premiums AND the feature cards (STRETCH / CLONE / SPLIT, bottom or side) —
		// by peeking at this spin's remaining book events. They all mount parked
		// (slotsReleased is still false), so when we release below the WHOLE frame
		// of special symbols reels in TOGETHER, right after the main board. The
		// feature EFFECTS (wild column slide, stretch, clone morph, split panes)
		// still play afterwards in their own events.
		const revealIndex = bookEvents.indexOf(bookEvent);
		for (let i = revealIndex + 1; i < bookEvents.length; i++) {
			const e = bookEvents[i];
			if (e.type === 'reveal') break;
			if (e.type === 'wildReel') {
				// events fire one per cell now, so accumulate across them
				stateGame.wildReelReels = [
					...new Set([...stateGame.wildReelReels, ...e.reels.map((r) => r.reel)]),
				];
			} else if (e.type === 'unlockedSlots') {
				stateGame.unlockedSlots = {
					level: e.level,
					unlocked: e.unlocked,
					bottom: e.bottom,
					sides: e.sides,
				};
				stateGame.unlockedGroups = e.unlocked;
			} else if (e.type === 'stretchReel') {
				stateGame.featureCells = [
					...stateGame.featureCells,
					...e.reels.map(({ reel }) => ({ reel, name: 'STRETCH' as const })),
				];
			} else if (e.type === 'cloneSymbol' || e.type === 'splitSymbols') {
				const c = e.cell;
				if (c && (c.reel != null || c.side != null)) {
					stateGame.featureCells = [
						...stateGame.featureCells,
						{
							reel: c.reel,
							side: c.side,
							slotRow: c.slotRow,
							name: e.type === 'cloneSymbol' ? ('CLONE' as const) : ('SPLIT' as const),
						},
					];
				}
			}
		}

		// main board landed -> release: ALL the special-cell symbols drop in together.
		stateGame.slotsReleased = true;
		eventEmitter.broadcast({ type: 'soundScatterCounterClear' });
	},
	winInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
		const betCost = stateBetDerived.betCost();
		const megaWin = bookEvent.wins.find((win) => isMegaWin(win.win, betCost));

		if (!megaWin) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
		}

		// Unlocked-slot cells (side columns / bottom premiums) are NOT on the core
		// reel board, so split their winning positions out: the core board gets the
		// reel positions, LockedSlots lights up the slot positions.
		const slotKeys = new Set<string>();
		const u = stateGame.unlockedSlots;
		if (u) {
			for (const c of u.bottom) slotKeys.add(`${c.reel}:${c.row}`);
			for (const s of u.sides) for (const c of s.cells) slotKeys.add(`${s.reel}:${c.row}`);
		}
		const isSlot = (p: Position) => slotKeys.has(`${p.reel}:${p.row}`);
		const boardPositions = (positions: Position[]) =>
			slotKeys.size ? positions.filter((p) => !isSlot(p)) : positions;

		stateGame.slotWinPositions = slotKeys.size
			? bookEvent.wins.flatMap((win) => win.positions.filter(isSlot))
			: [];

		await sequence(bookEvent.wins, async (win) => {
			// non-winning symbols dim so only the connecting combination pops;
			// a golden sweep runs left-to-right over it
			const positions = boardPositions(win.positions);
			eventEmitter.broadcast({ type: 'winDimShow', positions });
			eventEmitter.broadcast({ type: 'plasmaWinIgnite', positions });
			eventEmitter.broadcast({ type: 'winSweep', positions });
			await animateSymbols({ positions });
			eventEmitter.broadcast({ type: 'plasmaWinRelease' });
		});

		// mega-win lightning telegraph — after symbol anims, before money celebration (setWin)
		if (megaWin) {
			// thunder clap fired with the lightning burst so the visual has impact
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_thunder' });
			await eventEmitter.broadcastAsync({
				type: 'winLightning',
				winGroups: bookEvent.wins.map((win) => win.positions),
				winAmount: megaWin.win,
			});
		}

		// hold EVERY winning cell lit (union) under the overlay through the
		// money count-up - the glass glint sweep is deferred to the very end
		// (setWin, after the count-up) so it only plays once the spin settles
		eventEmitter.broadcast({
			type: 'winDimShow',
			positions: boardPositions(bookEvent.wins.flatMap((win) => win.positions)),
		});
		eventEmitter.broadcast({
			type: 'winCycleSet',
			wins: bookEvent.wins.map((win) => boardPositions(win.positions)),
		});
	},
	// customised: Wild Reel — a bottom-slot symbol grows its middle reel into a
	// rising wild. The reel extends to baseRows + added rows (top-aligned), the
	// existing symbols push up, and the risen WILD cells carry a multiplier.
	wildReel: async (bookEvent: BookEventOfType<'wildReel'>) => {
		const reels = bookEvent.reels.map(({ reel }) => reel);

		// this cell's feature is now ACTIVE: electrify its border for the whole run
		eventEmitter.broadcast({ type: 'cellLightningOn', cells: reels.map((reel) => ({ reel })) });

		// 1) a WILD drops INTO the bottom special slot cell of each triggered reel
		//    (LockedSlots opens that cell and plays the wild's drop-in). Events now
		//    fire ONE PER CELL in activation order, so ACCUMULATE the reels.
		stateGame.wildReelReels = [...new Set([...stateGame.wildReelReels, ...reels])];
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		await waitForTimeout(420);

		// 2) that WILD turns the reel above it wild: the full straitjacket "WILD"
		//    column slides down from the top while it PUSHES the reel's normal
		//    symbols down and off the bottom edge, then settles.
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		const anims: Promise<unknown>[] = [];
		reels.forEach((reel) => {
			const reelObj = stateGame.board[reel];
			if (!reelObj) return;
			// PUSH: the whole reel shoves down as ONE rigid stack, glued to the
			// descending wild column (same backOut curve + duration as the slide in
			// WildReelSlide) so it reads as being physically pushed off the bottom —
			// not each symbol free-falling on its own timing.
			const drop = (getReelRows(reel) + 2) * SYMBOL_SIZE;
			reelObj.reelState.symbols.forEach((symbol) => {
				symbol.symbolState = 'land';
				anims.push(symbol.symbolY.set(symbol.symbolY.current + drop, { duration: 560, easing: backOut }));
			});
		});
		anims.push(
			eventEmitter.broadcastAsync({
				type: 'wildReelSlideShow',
				// carry each risen wild's multiplier through so the column can stamp it
				reels: bookEvent.reels.map(({ reel, ways }) => ({ reel, ways })),
			}),
		);
		await Promise.all(anims);

		// feature finished -> the lightning fades and moves on to the next cell
		eventEmitter.broadcast({ type: 'cellLightningOff' });
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await waitForTimeout(250);
	},
	// customised: Unlocked Slots — the reserved slots open (by bonus level) and
	// premiums/wilds drop into them, expanding the board toward 6/7 reels.
	unlockedSlots: async (bookEvent: BookEventOfType<'unlockedSlots'>) => {
		stateGame.unlockedSlots = {
			level: bookEvent.level,
			unlocked: bookEvent.unlocked,
			bottom: bookEvent.bottom,
			sides: bookEvent.sides,
		};
		// keep the open groups for the rest of the bonus so a cell reads unlocked
		// the moment it reveals (no cosmetic reel flashing before the real drop-in)
		stateGame.unlockedGroups = bookEvent.unlocked;

		const hasWild =
			bookEvent.sides.some((s) => s.cells.some((c) => c.name === 'W')) ||
			bookEvent.bottom.some((c) => c.name === 'W');
		const hasFill = bookEvent.bottom.length > 0 || bookEvent.sides.some((s) => s.cells.length > 0);

		if (hasFill) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
			if (hasWild) eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
			// let the slot symbols play their drop-in (land) animation
			await waitForTimeout(560);
		}

		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await waitForTimeout(150);
	},
	// customised: STRETCH — a stretch cell drops into the bottom slot and grows
	// its reel taller (overflowing the board), appending rows so ways go up for
	// every symbol on the reel.
	stretchReel: async (bookEvent: BookEventOfType<'stretchReel'>) => {
		// this cell's feature is now ACTIVE: electrify its border for the whole run
		eventEmitter.broadcast({
			type: 'cellLightningOn',
			cells: bookEvent.reels.map(({ reel }) => ({ reel })),
		});

		// 1) drop the STRETCH card into each triggered bottom cell
		stateGame.featureCells = [
			...stateGame.featureCells,
			...bookEvent.reels.map(({ reel }) => ({ reel, name: 'STRETCH' as const })),
		];
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		await waitForTimeout(360);

		// 1b) mark the symbols on the reels about to be stretched, so the reel the
		//     feature picked is readable before it starts moving.
		await eventEmitter.broadcastAsync({
			type: 'targetLockShow',
			cells: bookEvent.reels.flatMap(({ reel, cells }) =>
				cells.map(({ row }) => ({ reel, row })),
			),
			tone: 'stretch',
		});

		// 2) stamp the per-symbol multipliers onto every stretched reel so the ways
		//    engine reflects the extra x-ways (count_board_ways counts multiplier=m as
		//    m symbols on the reel).
		const newBoard = stateGameDerived
			.boardRaw()
			.map((reel) => reel.map((rawSymbol) => ({ ...rawSymbol })));
		bookEvent.reels.forEach(({ reel, cells }) => {
			cells.forEach(({ row, multiplier }) => {
				if (newBoard[reel]?.[row]) {
					newBoard[reel][row] = { ...newBoard[reel][row], multiplier };
				}
			});
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });

		const wildReels = bookEvent.reels.filter((r) => r.mode === 'wild');
		const normalReels = bookEvent.reels.filter((r) => r.mode !== 'wild');
		const anims: Promise<unknown>[] = [];

		// 3a) WILD-reel stretch: the full-reel WILD column rises, shoving the reel's
		//     symbols off the bottom, with a single centred "N WAYS" total.
		if (wildReels.length) {
			const stretched = wildReels.map(({ reel, reelWays, baseRows }) => ({
				reel,
				ways: reelWays,
				baseRows,
			}));
			// mark wild-covered so a later SPLIT on these reels only feeds ways in (no
			// panes drawn over the wild column)
			stateGame.stretchedReels = [
				...stateGame.stretchedReels,
				...stretched.map(({ reel }) => reel),
			];
			stretched.forEach(({ reel }) => {
				const reelObj = stateGame.board[reel];
				if (!reelObj) return;
				const drop = (getReelRows(reel) + 2) * SYMBOL_SIZE;
				reelObj.reelState.symbols.forEach((symbol) => {
					symbol.symbolState = 'land';
					anims.push(
						symbol.symbolY.set(symbol.symbolY.current + drop, { duration: 520, easing: backOut }),
					);
				});
			});
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
			anims.push(eventEmitter.broadcastAsync({ type: 'stretchFxShow', reels: stretched }));
		}

		// 3b) NORMAL-reel stretch: each real symbol stretches a little in its own cell
		//     (overflow clipped) and, when big (> 5x), shows its per-symbol x-ways.
		if (normalReels.length) {
			anims.push(
				eventEmitter.broadcastAsync({
					type: 'stretchWaysShow',
					cells: normalReels.flatMap(({ reel, cells }) =>
						cells.map(({ row, multiplier }) => ({ reel, row, multiplier })),
					),
				}),
			);
		}

		await Promise.all(anims);
		shakeBoard({ intensity: 9, duration: 240 });

		// feature finished -> the lightning fades and moves on to the next cell
		eventEmitter.broadcast({ type: 'cellLightningOff' });
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await waitForTimeout(200);
	},
	// customised: CLONE — a clone cell converts every copy of one symbol into a
	// premium.
	cloneSymbol: async (bookEvent: BookEventOfType<'cloneSymbol'>) => {
		// this cell's feature is now ACTIVE: electrify its border for the whole run
		if (bookEvent.cell && (bookEvent.cell.reel != null || bookEvent.cell.side != null)) {
			eventEmitter.broadcast({ type: 'cellLightningOn', cells: [bookEvent.cell] });
			// 1) drop the CLONE card into its special cell (bottom reel or side slot)
			const c = bookEvent.cell;
			stateGame.featureCells = [
				...stateGame.featureCells,
				{ reel: c.reel, side: c.side, slotRow: c.slotRow, name: 'CLONE' },
			];
		}
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		await waitForTimeout(360);

		// 1b) mark every copy of `from` before it morphs, so the player sees which
		//     symbols the clone picked while they are still the old symbol.
		await eventEmitter.broadcastAsync({
			type: 'targetLockShow',
			cells: bookEvent.cells.map(({ reel, row }) => ({ reel, row })),
			tone: 'clone',
		});

		// 2) convert every matching cell to the target premium underneath, but hide
		//    it under the CloneMorph overlay so the swap is only ever seen as a morph
		const newBoard = stateGameDerived
			.boardRaw()
			.map((reel) => reel.map((rawSymbol) => ({ ...rawSymbol })));
		bookEvent.cells.forEach(({ reel, row }) => {
			// keep the rest of the raw symbol (notably a split's `multiplier`):
			// a clone converting an already-split cell must not strip its ways
			if (newBoard[reel]?.[row]) {
				newBoard[reel][row] = { ...newBoard[reel][row], name: bookEvent.to };
			}
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });

		// 2b) Park the morphing symbols back on their cells. `boardSettle` swaps the
		//     raw symbols but deliberately leaves symbolY alone, and features that
		//     ran earlier this spin (wild reel, wild stretch) shove a whole reel's
		//     symbols down and off the bottom edge without ever putting them back.
		//     A clone landing on such a reel would then morph a symbol that is no
		//     longer under the overlay — the old art shows through beside the new
		//     one, and the win pulse afterwards plays off-screen.
		bookEvent.cells.forEach(({ reel, row }) => {
			const reelSymbol = stateGame.board[reel]?.reelState.symbols[row];
			if (!reelSymbol) return;
			const restY = (row - 0.5) * SYMBOL_SIZE;
			if (reelSymbol.symbolY.current !== restY) {
				reelSymbol.symbolY.set(restY, { duration: 0 });
			}
		});

		// 3) PLAY the clone morph: every copy of `from` charges, flashes and morphs
		//    into `to` (the overlay covers the cells so the instant swap is unseen)
		await eventEmitter.broadcastAsync({
			type: 'cloneMorphShow',
			cells: bookEvent.cells.map(({ reel, row }) => ({ reel, row })),
			from: bookEvent.from,
			to: bookEvent.to,
		});
		// drop the overlay onto the identical (already-settled) board, then let the
		// freshly-morphed premiums pulse on the real board
		eventEmitter.broadcast({ type: 'cloneMorphHide' });
		await animateSymbols({ positions: bookEvent.cells });

		// feature finished -> the lightning fades and moves on to the next cell
		eventEmitter.broadcast({ type: 'cellLightningOff' });
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await waitForTimeout(160);
	},
	// customised: SPLIT — a split cell ADDS +1..+10 ways to the winning cells of
	// one winning symbol type (and to any risen wild column). Never a multiplier.
	splitSymbols: async (bookEvent: BookEventOfType<'splitSymbols'>) => {
		// this cell's feature is now ACTIVE: electrify its border for the whole run
		if (bookEvent.cell && (bookEvent.cell.reel != null || bookEvent.cell.side != null)) {
			eventEmitter.broadcast({ type: 'cellLightningOn', cells: [bookEvent.cell] });
			// 1) drop the SPLIT card into its special cell (bottom reel or side slot)
			const c = bookEvent.cell;
			stateGame.featureCells = [
				...stateGame.featureCells,
				{ reel: c.reel, side: c.side, slotRow: c.slotRow, name: 'SPLIT' },
			];
		}
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		await waitForTimeout(340);

		// Cells on a wild column belong to the wild reel overlay, which hides the
		// board symbols underneath it — so the paying-symbol pane overlay can't
		// paint them. The wild column itself handles the Madam-Mirror tear (and
		// the ways badge climb) via wildReelWaysUpdate.
		const symbolCells = bookEvent.cells.filter(({ wild }) => !wild);
		// per wild reel: the resulting per-cell ways count drives how many panes
		// the column tears into (same rule as a paying symbol's split count).
		const wildSplitByReel = new Map<number, number>();
		for (const c of bookEvent.cells) {
			if (!c.wild) continue;
			wildSplitByReel.set(c.reel, Math.max(wildSplitByReel.get(c.reel) ?? 0, c.multiplier));
		}

		// 1b) mark the chosen symbols BEFORE anything happens to them, so the
		//     player reads which cells the split picked rather than only seeing
		//     the aftermath.
		await eventEmitter.broadcastAsync({
			type: 'targetLockShow',
			cells: symbolCells.map(({ reel, row }) => ({ reel, row })),
			tone: 'split',
		});

		// 2) stamp the multiplier onto each split cell so the ways engine + board
		//    reflect the split (the pane overlay then renders on top of these cells)
		const newBoard = stateGameDerived
			.boardRaw()
			.map((reel) => reel.map((rawSymbol) => ({ ...rawSymbol })));
		bookEvent.cells.forEach(({ reel, row, multiplier }) => {
			if (newBoard[reel]?.[row]) {
				newBoard[reel][row] = { ...newBoard[reel][row], multiplier };
			}
		});
		eventEmitter.broadcast({ type: 'boardSettle', board: newBoard });

		// 3) VISUALLY split each winning symbol into N center-cropped panes that
		//    snap apart (Madam-Mirror style), leaving a slim-seam XN cell, while
		//    any wild column the split tore through tears into panes AND climbs
		//    to its new worth.
		await Promise.all([
			eventEmitter.broadcastAsync({
				type: 'splitPanesShow',
				cells: symbolCells.map(({ reel, row, multiplier }) => ({
					reel,
					row,
					count: multiplier,
				})),
			}),
			bookEvent.wildReels?.length
				? eventEmitter.broadcastAsync({
						type: 'wildReelWaysUpdate',
						reels: bookEvent.wildReels.map((w) => ({
							...w,
							split: wildSplitByReel.get(w.reel) ?? bookEvent.mult,
						})),
					})
				: Promise.resolve(),
		]);

		// feature finished -> the lightning fades and moves on to the next cell
		eventEmitter.broadcast({ type: 'cellLightningOff' });
		eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: bookEvent.totalWays });
		await waitForTimeout(150);
	},
	// customised: announces which of the three bonus levels was awarded
	bonusLevel: async (bookEvent: BookEventOfType<'bonusLevel'>) => {
		// open the groups this level grants up front so the very first bonus spin's
		// cells already read unlocked (L1 bottom, L2 +right, L3 +left).
		const byLevel: Record<number, ('bottom' | 'right' | 'left')[]> = {
			1: ['bottom'],
			2: ['bottom', 'right'],
			3: ['bottom', 'right', 'left'],
		};
		const activeGroups = byLevel[bookEvent.level] ?? [];
		stateGame.unlockedGroups = activeGroups;
		await eventEmitter.broadcastAsync({ type: 'bonusLevelShow', level: bookEvent.level });
	},
	setTotalWin: async (bookEvent: BookEventOfType<'setTotalWin'>) => {
		stateBet.winBookEventAmount = bookEvent.amount;
	},
	freeSpinTrigger: async (bookEvent: BookEventOfType<'freeSpinTrigger'>) => {
		// the bonusLevel event follows in the same book and shows the level banner
		eventEmitter.broadcast({ type: 'winCycleStop' });
		// animate scatters
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });
		await animateSymbols({ positions: bookEvent.positions });
		// go straight to the bonus level banner (the old mirror intro screen was removed)
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_superfreespin' });
		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		await eventEmitter.broadcastAsync({ type: 'transition' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'jng_intro_fs' });
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_freespin' });
		stateGame.gameType = 'freegame';
		// boardFrameGlowShow KILLED — BoardFramePlasma unmounted; glow was not the
		// dashed-lip source (baked PNG quilt stitches) and must not reappear.
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		lastFreeSpinTotal = bookEvent.totalFs;
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: undefined,
			total: bookEvent.totalFs,
		});
		await eventEmitter.broadcastAsync({ type: 'uiShow' });
		await eventEmitter.broadcastAsync({ type: 'drawerButtonShow' });
		eventEmitter.broadcast({ type: 'drawerFold' });
	},
	updateFreeSpin: async (bookEvent: BookEventOfType<'updateFreeSpin'>) => {
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		lastFreeSpinTotal = bookEvent.total;
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: bookEvent.amount,
			total: bookEvent.total,
		});
	},
	// extra scatters during free spins: animate them and bump the total
	freeSpinRetrigger: async (bookEvent: BookEventOfType<'freeSpinRetrigger'>) => {
		eventEmitter.broadcast({ type: 'winCycleStop' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });
		await animateSymbols({ positions: bookEvent.positions });

		// how many spins this retrigger actually added (book only sends the total)
		const added = bookEvent.totalFs - lastFreeSpinTotal;
		lastFreeSpinTotal = bookEvent.totalFs;

		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: undefined,
			total: bookEvent.totalFs,
		});

		// announce the award with a themed "+N SPINS" banner before continuing
		if (added > 0) {
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fs_respins' });
			await eventEmitter.broadcastAsync({ type: 'retriggerBannerShow', amount: added });
		}
	},
	freeSpinEnd: async (bookEvent: BookEventOfType<'freeSpinEnd'>) => {
		const winLevelData = winLevelMap[bookEvent.winLevel as WinLevel];

		eventEmitter.broadcast({ type: 'waysCounterHide' });
		eventEmitter.broadcast({ type: 'winCycleStop' });
		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		stateGame.gameType = 'basegame';
		// boardFrameGlowHide no-op (plasma unmounted)
		eventEmitter.broadcast({ type: 'freeSpinOutroShow' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_youwon_panel' });
		winLevelSoundsPlay({ winLevelData });
		await eventEmitter.broadcastAsync({
			type: 'freeSpinOutroCountUp',
			amount: bookEvent.amount,
			winLevelData,
		});
		winLevelSoundsStop();
		eventEmitter.broadcast({ type: 'freeSpinOutroHide' });
		eventEmitter.broadcast({ type: 'freeSpinCounterHide' });
		await eventEmitter.broadcastAsync({ type: 'transition' });
		await eventEmitter.broadcastAsync({ type: 'uiShow' });
		await eventEmitter.broadcastAsync({ type: 'drawerUnfold' });
		eventEmitter.broadcast({ type: 'drawerButtonHide' });
	},
	setWin: async (bookEvent: BookEventOfType<'setWin'>) => {
		// the celebration tier is chosen by win amount in bet multiples
		const celebration = getWinCelebration(bookEvent.amount);

		// winners stay lit under the overlay while the amount counts up (no glint)
		eventEmitter.broadcast({ type: 'winShow' });
		winLevelSoundsPlay({ winLevelData: celebration });
		await eventEmitter.broadcastAsync({
			type: 'winUpdate',
			amount: bookEvent.amount,
		});
		winLevelSoundsStop();
		eventEmitter.broadcast({ type: 'winHide' });

		// end of spin: NOW sweep the glass glint across each winning way (loops
		// through idle until the next spin clears it)
		eventEmitter.broadcast({ type: 'winCycleStart' });
	},
	finalWin: async (bookEvent: BookEventOfType<'finalWin'>) => {
		// Do nothing
	},
	// customised
	createBonusSnapshot: async (bookEvent: BookEventOfType<'createBonusSnapshot'>) => {
		const { bookEvents } = bookEvent;

		function findLastBookEvent<T>(type: T) {
			return _.findLast(bookEvents, (bookEvent) => bookEvent.type === type) as
				| BookEventOfType<T>
				| undefined;
		}

		const lastFreeSpinTriggerEvent = findLastBookEvent('freeSpinTrigger' as const);
		const lastUpdateFreeSpinEvent = findLastBookEvent('updateFreeSpin' as const);
		const lastSetTotalWinEvent = findLastBookEvent('setTotalWin' as const);
		const lastUpdateGlobalMultEvent = findLastBookEvent('updateGlobalMult' as const);

		if (lastFreeSpinTriggerEvent) await playBookEvent(lastFreeSpinTriggerEvent, { bookEvents });
		if (lastUpdateFreeSpinEvent) playBookEvent(lastUpdateFreeSpinEvent, { bookEvents });
		if (lastSetTotalWinEvent) playBookEvent(lastSetTotalWinEvent, { bookEvents });
		if (lastUpdateGlobalMultEvent) playBookEvent(lastUpdateGlobalMultEvent, { bookEvents });
	},
};
