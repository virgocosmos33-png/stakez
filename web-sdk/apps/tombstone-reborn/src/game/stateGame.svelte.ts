import _ from 'lodash';
import { Tween } from 'svelte/motion';

import { stateBet, stateUi } from 'state-shared';
import { createEnhanceBoard, createReelForCascading, stateSlots } from 'utils-slots';
import { createGetWinLevelDataByWinLevelAlias } from 'utils-shared/winLevel';

import type { GameType, RawSymbol, SymbolState, SymbolName } from './types';
import type { Atmosphere } from './atmosphere.svelte';
import { stateLayoutDerived } from './stateLayout';
import { winLevelMap } from './winLevelMap';
import { eventEmitter } from './eventEmitter';
import {
	SYMBOL_SIZE,
	BOARD_SIZES,
	BOARD_FRAME_OUTER,
	INITIAL_BOARD,
	BOARD_DIMENSIONS,
	SPIN_OPTIONS_DEFAULT,
	SPIN_OPTIONS_FAST,
	SPIN_OPTIONS_SUPER,
	INITIAL_SYMBOL_STATE,
	SCATTER_LAND_SOUND_MAP,
} from './constants';
import { COLUMN_ROW_OFFSET } from './chassisArt';
import { isSpecialBarVertical } from './specialBarLayout';
import { getReelRows, getReelYOffset } from './utils';

/** Must match FrameMorphHud rail height + plate clearance. */
const HUD_RAIL_H = 56;
const HUD_PLATE_CLEAR = 14;
/** Desktop: air between the tall timber and the HUD. WIN hangs in the short-reel step, not below the whole board. */
const HUD_WIN_HANG = 28;
const HUD_CLEAR_PX = 12;
/** Extra main-space pad under the published HUD top — spin cluster + Storybook chrome. */
const HUD_EXTRA_CLEAR = 8;
/** When the HUD has not published yet, assume this much main-space is the control bar. */
const HUD_FALLBACK_MAIN = 120;
/** Breathing room above the timber (Storybook action toast + logo). */
const BOARD_TOP_MARGIN = 20;
const onSymbolLand = ({ rawSymbol }: { rawSymbol: RawSymbol }) => {
	if (rawSymbol.name === 'S' || rawSymbol.name === 'SU') {
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
			name: 'sfx_wild_land',
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
			const last = BOARD_DIMENSIONS.x - 1;
			const mode = (stateBet.activeBetModeKey ?? 'base').toLowerCase();
			// Last reel is boarded on a normal spin — no drop thud. Keep it for
			// the feature buy (bonus_small) and super bonus (buy or open lane).
			const lastReelDrop =
				reelIndex !== last ||
				stateGame.laneSuper ||
				mode === 'bonus_small' ||
				mode === 'bonus_super' ||
				mode === 'superspins';
			if (lastReelDrop) {
				eventEmitter.broadcast({
					type: 'soundOnce',
					name: 'sfx_reel_stop_1',
					forcePlay: !stateBet.isTurbo,
				});
			}
			const pendingIndex = stateGame.pendingNudges.findIndex((pending) => pending.reel === reelIndex);
			if (pendingIndex >= 0) {
				const pending = stateGame.pendingNudges[pendingIndex];
				stateGame.pendingNudges = stateGame.pendingNudges.filter((_, i) => i !== pendingIndex);
				eventEmitter.broadcast({ type: 'nudgeWaysPark', ...pending });
			}
		},
		onSymbolLand,
	});

	reel.reelState.spinOptions = () => {
		if (stateBet.isSuperTurbo) return SPIN_OPTIONS_SUPER;
		if (reel.reelState.spinType === 'fast') return SPIN_OPTIONS_FAST;
		return SPIN_OPTIONS_DEFAULT;
	};

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
	/** True from playBet start until the book finishes (base + bonus spins).
	 *  Storybook keeps xstate idle during Action, so idle+!spinning is not
	 *  enough to know the board is waiting on the player. */
	roundLive: false,
	atmosphere: 'base' as Atmosphere,
	// TOMBSTONE REBORN: the special bar's revealed cards this spin (one entry per
	// non-empty bar cell). Set by the specialBar book event, cleared on reveal.
	specialBar: [] as { reel: number; kind: string }[],
	// which bar card's EFFECT is currently resolving — its plaque lights up on
	// the rail while the feature plays (top-to-bottom, in book order). Null when
	// nothing is firing. Set/cleared by the feature book event handlers.
	specialBarActiveKind: null as string | null,
	// LAST-REEL LANE lock. The lane is boarded shut (LaneLidLock cover) on every
	// base/small-bonus spin until a DIG UP card blasts it open mid-spin; the
	// super bonus digs it up for the whole round. `laneSuper` persists that
	// whole-bonus unlock across reveals (reset on a base-game reveal).
	lidOpen: false,
	laneSuper: false,
	/** 0 = last-reel symbol in the pocket, 1 = gold lane card in the pocket. */
	laneCardSwap: 0,
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
	// NUDGE WAYS: look-ahead from THIS spin's reveal so the column can park
	// the instant that reel stops — not after the individual NW cards land.
	// Must be this spin only: a 10-spin book has many nudgeWays, and finding
	// the first in the whole book parked a ghost totem on every other spin.
	pendingNudges: [] as {
		reel: number;
		fullReel: boolean;
		startRow: number;
		initialWays: number;
	}[],
	// while set, Board hides only the cells the totem currently covers — not
	// the whole reel, or a bottom-cell land blanks the column above it.
	nudgeCoverReel: null as number | null,
	nudgeCoverReels: [] as number[],
	nudgeCoverCells: [] as { reel: number; row: number }[],
	// Rows being shoved off the pocket bottom while the totem grows. `t` is
	// 0–1; each sliding symbol travels from its seat to just below the clip.
	nudgePush: board.map(() => ({
		rows: [] as number[],
		bumpRows: [] as number[],
		t: new Tween(0),
	})),
});

const boardLayout = () => {
	const main = stateLayoutDerived.mainLayout();
	// centres the seven columns of CARDS, not the box they live in — see
	// COLUMN_ROW_OFFSET
	const x = main.width * 0.5 - COLUMN_ROW_OFFSET;

	// The under-board WAYS/WIN cluster (FrameMorphHud) only renders when the
	// special bar is laid FLAT (narrow/portrait). When the bar stands vertical
	// (desktop/landscape) nothing sits under the board, so reserving a rail's
	// worth of space there just pins the board against the top edge — only
	// reserve it when the cluster is actually shown.
	const barVertical = isSpecialBarVertical({ x, width: BOARD_SIZES.width });

	const pivotX = BOARD_SIZES.width / 2;
	const pivotY = BOARD_SIZES.height / 2;

	let contentTop = pivotY;
	let contentBot = pivotY;
	for (let i = 0; i < board.length; i++) {
		const top = getReelYOffset(i);
		const bottom = top + getReelRows(i) * SYMBOL_SIZE;
		if (top < contentTop) contentTop = top;
		if (bottom > contentBot) contentBot = bottom;
	}
	contentTop -= BOARD_FRAME_OUTER;
	contentBot += BOARD_FRAME_OUTER;

	// floorY = the lowest line the timber may reach, in main-space y.
	const hudTopScreen = stateUi.hudBarTopScreenY;
	let floorY = main.height - HUD_FALLBACK_MAIN;
	if (hudTopScreen > 0) {
		const canvasH = stateLayoutDerived.canvasSizes().height;
		const hudTopMain =
			main.height / 2 + (hudTopScreen - HUD_CLEAR_PX - canvasH / 2) / main.scale;
		const reserve = (barVertical ? HUD_WIN_HANG : HUD_RAIL_H + HUD_PLATE_CLEAR) + HUD_EXTRA_CLEAR;
		floorY = hudTopMain - reserve;
	}

	// Grow to fill the safe band — past authored size if the window has room.
	// Width leaves a strip on the right for the WAYS/MULTI/WIN plaques.
	const available = Math.max(1, floorY - BOARD_TOP_MARGIN);
	const liveH = Math.max(1, contentBot - contentTop);
	const liveW = BOARD_SIZES.width + BOARD_FRAME_OUTER * 2;
	const plaqueCol = barVertical ? 0 : 48;
	const scaleH = available / liveH;
	const scaleW = Math.max(0.2, (main.width - plaqueCol) / liveW);
	const scale = Math.min(scaleH, scaleW);

	// Centre the LIVE timber in the safe band (not the authored 4-row box).
	const yMin = BOARD_TOP_MARGIN - (contentTop - pivotY) * scale;
	const yMax = floorY - (contentBot - pivotY) * scale;
	// Sit on the HUD floor so leftover height is above the timber, not a gap under it.
	let y = yMax;
	y = Math.min(Math.max(y, yMin), yMax);

	const visualTop = y + (contentTop - pivotY) * scale;
	const visualBottom = y + (contentBot - pivotY) * scale;
	const visualLeft = x - pivotX * scale;
	const visualRight = x + (BOARD_SIZES.width - pivotX) * scale;

	return {
		x,
		y,
		scale,
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: pivotX, y: pivotY },
		visualTop,
		visualBottom,
		visualLeft,
		visualRight,
		...BOARD_SIZES,
	};
};

/** Board-local (lx, ly) → main-space, honouring boardLayout scale around pivot.
 *  Every overlay that used to do `origin + local` must go through this or it
 *  desyncs the moment the expanded board shrinks to fit under the HUD. */
const boardToWorld = (lx: number, ly: number) => {
	const b = boardLayout();
	return {
		x: b.x + (lx - b.pivot.x) * b.scale,
		y: b.y + (ly - b.pivot.y) * b.scale,
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

/** Reels are in flight: pre-spin stagger, fall-out, hang, or fall-in.
 *  Storybook Action keeps xstate idle during playBet, so callers must not
 *  treat isIdle() as "the board is at rest". */
const reelsSpinning = () =>
	stateSlots.isPreSpinning ||
	stateGame.board.some((reel) => reel.reelState.motion !== 'stopped');

export const { getWinLevelDataByWinLevelAlias } = createGetWinLevelDataByWinLevelAlias({
	winLevelMap,
});

export const stateGameDerived = {
	onSymbolLand,
	boardLayout,
	boardToWorld,
	boardRaw,
	scatterLandIndex,
	reelsSpinning,
	enhancedBoard,
	getWinLevelDataByWinLevelAlias,
};
