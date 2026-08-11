import _ from 'lodash';
import type { Tween } from 'svelte/motion';

import { stateBet, stateUi } from 'state-shared';
import { createEnhanceBoard, createReelForCascading } from 'utils-slots';
import { createGetWinLevelDataByWinLevelAlias } from 'utils-shared/winLevel';

import type { GameType, RawSymbol, SymbolState, SymbolName } from './types';
import { stateLayoutDerived } from './stateLayout';
import { winLevelMap } from './winLevelMap';
import { eventEmitter } from './eventEmitter';
import {
	SYMBOL_SIZE,
	BOARD_SIZES,
	BOARD_PLATE_PAD,
	INITIAL_BOARD,
	BOARD_DIMENSIONS,
	SPIN_OPTIONS_DEFAULT,
	SPIN_OPTIONS_FAST,
	INITIAL_SYMBOL_STATE,
	SCATTER_LAND_SOUND_MAP,
} from './constants';
import { COLUMN_ROW_OFFSET } from './chassisArt';

/** Must match FrameMorphHud rail height + plate clearance. */
const HUD_RAIL_H = 56;
const HUD_PLATE_CLEAR = 14;
const HUD_CLEAR_PX = 12;

const onSymbolLand = ({ rawSymbol }: { rawSymbol: RawSymbol }) => {
	if (rawSymbol.name === 'S') {
		eventEmitter.broadcast({ type: 'soundScatterCounterIncrease' });
		eventEmitter.broadcast({
			type: 'soundOnce',
			name: SCATTER_LAND_SOUND_MAP[scatterLandIndex()],
		});
	}

	if (rawSymbol.name === 'ME') {
		// the top special symbol drops with its own cinematic graveyard toll
		eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_tombstone_toll',
		});
	} else if (rawSymbol.name === 'W') {
		eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_multiplier_landing',
		});
	}
};

const board = _.range(BOARD_DIMENSIONS.x).map((reelIndex) => {
	const reel = createReelForCascading({
		// stagger slot 1..5, NOT 0..4: reelIndex only drives the pre-spin
		// fall-out delay, and the LEFT special column reels out first in slot 0
		// (the right column takes the slot after the last reel) — see
		// LockedSlots. Components position by the board ARRAY index, never this.
		reelIndex: reelIndex + 1,
		symbolHeight: SYMBOL_SIZE,
		initialSymbols: INITIAL_BOARD[reelIndex],
		initialSymbolState: INITIAL_SYMBOL_STATE,
		onReelStopping: () => {
			eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_reel_stop_1',
				forcePlay: !stateBet.isTurbo,
			});
		},
		onSymbolLand,
	});

	reel.reelState.spinOptions = () =>
		reel.reelState.spinType === 'fast' ? SPIN_OPTIONS_FAST : SPIN_OPTIONS_DEFAULT;

	return reel;
});

export type Reel = (typeof board)[number];
export type ReelSymbol = Reel['reelState']['symbols'][number];

export type MultiplierSymbol = {
	initX: number;
	initY: number;
	symbolX: Tween<number>;
	symbolY: Tween<number>;
	rawSymbol: RawSymbol;
	symbolState: SymbolState;
	oncomplete: () => void;
};

export const stateGame = $state({
	board,
	gameType: 'basegame' as GameType,
	// TOMBSTONE REBORN: the special bar's revealed cards this spin (one entry per
	// non-empty bar cell). Set by the specialBar book event, cleared on reveal.
	specialBar: [] as { reel: number; kind: string }[],
	multiplierBoard: [] as (MultiplierSymbol | undefined)[][],
	scatterCounter: 0,
	// bumped on every reveal. Drives LockedSlots to re-roll and re-drop the
	// symbols that reel behind the reserved "cell" slots each spin (both base
	// game, behind closed bars, and bonus, behind open bars).
	revealNonce: 0,
	// middle reels (1/2/3) currently grown by a Wild Reel this spin. Drives the
	// bottom locked-slot art: an active reel's slot reads UNLOCKED (its special
	// symbol rose into a wild) instead of padlocked. Cleared on the next reveal.
	wildReelReels: [] as number[],
	// subset of the above: reels whose OWN bottom cell holds the wild card. A
	// cage wild turns a main reel from across the board, so that reel gets a
	// column without its bottom cell opening or showing a card — only these
	// reels do. Cleared on the next reveal.
	wildCardReels: [] as number[],
	// reels currently covered by a STRETCH wild column this spin. A split landing
	// on one of these reels feeds its extra ways into the reel (the WAYS counter
	// reflects it) but must NOT paint split panes over the wild column — the reel
	// reads as wild. Cleared on the next reveal.
	stretchedReels: [] as number[],
	// Unlocked Slots (bonus board expansion). Set by the unlockedSlots book
	// event; drives LockedSlots to open the unlocked groups and drop the
	// premium/wild symbols into their slots. Cleared on the next reveal.
	unlockedSlots: null as null | {
		level: number;
		unlocked: ('bottom' | 'right' | 'left')[];
		// a W in a bottom cell is a plain PAYING wild carrying its multiplier
		bottom: { reel: number; row: number; name: SymbolName; multiplier?: number }[];
		sides: {
			side: 'left' | 'right';
			reel: number;
			cells: { row: number; slotRow: number; name: SymbolName; multiplier?: number }[];
		}[];
	},
	// winning board positions that live in an unlocked slot (side columns /
	// bottom premiums). These aren't on the core reel board, so LockedSlots
	// lights them up instead. Cleared on the next reveal.
	slotWinPositions: [] as { reel: number; row: number }[],
	// bottom cells that dropped a feature symbol this spin (Stretch / Split /
	// Clone). Drives LockedSlots to open that cell and show the feature card
	// (base game unlocks just this cell; bonus cells are already open). Cleared
	// on the next reveal.
	featureCells: [] as {
		reel?: number;
		side?: 'left' | 'right';
		slotRow?: number;
		name: SymbolName;
	}[],
	// which slot groups are unlocked for the WHOLE current bonus (by level: L1
	// bottom, L2 +right, L3 +left). Unlike `unlockedSlots` (per-spin content,
	// cleared each reveal) this PERSISTS across the bonus so LockedSlots knows a
	// cell is open the instant it reveals — the real slot symbol reels straight
	// in, with no cosmetic teaser flashing first. Reset to [] on a base-game reveal.
	unlockedGroups: [] as ('bottom' | 'right' | 'left')[],
	// per-reel ANIMATED display height (in rows) while a STRETCH grows a reel.
	// When set, getReelRows reads this tween instead of the raw board length, so
	// the reel visibly stretches over time — extending past the board's top AND
	// bottom edges from its centre — rather than snapping to full height. The
	// board already holds the final (taller) symbols; this just paces how much of
	// it is revealed. Cleared (per reel) on the next reveal.
	reelStretch: board.map(() => null) as (Tween<number> | null)[],
	// gates the special-cell (LockedSlots) symbol reel-in. Set false at the very
	// start of a reveal (before the main board spins) so every slot symbol parks
	// ABOVE its cell (hidden by its mask); flipped true once the MAIN board has
	// finished dropping, so all the special-cell symbols then reel in together in
	// one synchronised drop — a natural "land after the board" reel-in. Starts true
	// so the idle board shows its cells at rest; each reveal parks then releases.
	slotsReleased: true,
});

const boardLayout = () => {
	const main = stateLayoutDerived.mainLayout();
	// Slight upward nudge so logo / special-bar strip clear the top; may lift
	// further so BoardPlate + WAYS/WIN console never collide with bet/spin HUD.
	const preferredY = main.height * 0.5 - 36;
	let y = preferredY;
	const hudTopScreen = stateUi.hudBarTopScreenY;
	if (hudTopScreen > 0) {
		const canvasH = stateLayoutDerived.canvasSizes().height;
		const railFloor =
			main.height / 2 + (hudTopScreen - HUD_CLEAR_PX - canvasH / 2) / main.scale - HUD_RAIL_H / 2;
		// When the console is clamped to railFloor, keep plateBottom + CLEAR
		// at or above the console top (railFloor - HUD_RAIL_H/2).
		const maxBoardY =
			railFloor - HUD_RAIL_H / 2 - BOARD_SIZES.height / 2 - BOARD_PLATE_PAD - HUD_PLATE_CLEAR;
		y = Math.min(preferredY, maxBoardY);
	}
	return {
		// centres the seven columns of CARDS, not the box they live in — see
		// COLUMN_ROW_OFFSET
		x: main.width * 0.5 - COLUMN_ROW_OFFSET,
		y,
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
		...BOARD_SIZES,
	};
};

const boardRaw = () =>
	board.map((reel) => reel.reelState.symbols.map((reelSymbol) => reelSymbol.rawSymbol));

const scatterLandIndex = () => {
	if (stateGame.scatterCounter > 5) return 5;
	if (stateGame.scatterCounter < 1) return 1;
	return stateGame.scatterCounter as 1 | 2 | 3 | 4 | 5;
};

const { enhanceBoard } = createEnhanceBoard();
const enhancedBoard = enhanceBoard({ board: stateGame.board });

export const { getWinLevelDataByWinLevelAlias } = createGetWinLevelDataByWinLevelAlias({
	winLevelMap,
});

export const stateGameDerived = {
	onSymbolLand,
	boardLayout,
	boardRaw,
	scatterLandIndex,
	enhancedBoard,
	getWinLevelDataByWinLevelAlias,
};
