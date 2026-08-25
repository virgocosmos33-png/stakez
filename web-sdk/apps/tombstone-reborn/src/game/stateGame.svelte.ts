import _ from 'lodash';
import { Tween } from 'svelte/motion';

import { stateBet } from 'state-shared';
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
import { boardContentBox } from './boardFrameBox';
import { FRAME_SEATS } from './frameSeats.generated';
import { getReelRows, getReelYOffset } from './utils';
import { sceneToMain } from './saloonLamps';

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
	const canvas = stateLayoutDerived.canvasSizes();
	const pivotX = BOARD_SIZES.width / 2;
	const pivotY = BOARD_SIZES.height / 2;
	const box = boardContentBox();
	const seat = FRAME_SEATS.pocket;
	const tl = sceneToMain(seat.left, seat.top, canvas, main);
	const br = sceneToMain(seat.right, seat.bottom, canvas, main);
	const tw = Math.max(1, br.x - tl.x);
	const th = Math.max(1, br.y - tl.y);
	// Letterbox the authored windows INTO the FRAME hole. Cover (max) overflowed
	// under the planks — cards must stay in the opening, not on opaque wood.
	const scale = Math.min(tw / box.w, th / box.h);
	const ox = (tw - box.w * scale) / 2;
	const oy = (th - box.h * scale) / 2;
	const x = tl.x + ox - (box.x - pivotX) * scale;
	const y = tl.y + oy - (box.y - pivotY) * scale;

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

	return {
		x,
		y,
		scale,
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: pivotX, y: pivotY },
		visualTop: y + (contentTop - pivotY) * scale,
		visualBottom: y + (contentBot - pivotY) * scale,
		visualLeft: x - pivotX * scale,
		visualRight: x + (BOARD_SIZES.width - pivotX) * scale,
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
