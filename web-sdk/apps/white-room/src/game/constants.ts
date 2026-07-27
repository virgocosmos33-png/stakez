import _ from 'lodash';

import type { RawSymbol, SymbolState } from './types';
// Parametric board: reels/rows/symbol-size come from the game-builder config
// (game-builder/config/<game>.config.json -> board.generated.ts). Editing the
// config + `node game-builder/src/cli.mjs gen-frontend` reshapes the board.
import {
	GEN_SYMBOL_SIZE,
	GEN_REEL_PADDING,
	GEN_HIGH_SYMBOLS,
	GEN_NUM_ROWS,
	buildInitialBoard,
} from './board.generated';
import { CHASSIS_BOTTOM_EXTENT } from './chassisArt';

// 140 keeps the 5-wide board (+ ornate frame) inside the 800-wide portrait
// canvas without clipping the edge symbols, and reads smaller/comfortable on
// desktop (was 172, which overflowed portrait and dominated the desktop view).
export const SYMBOL_SIZE = GEN_SYMBOL_SIZE;

// The grid pitch above is square, but the CARD painted inside each cell is
// portrait — see tools/make_symbols_portrait.py, which bakes that shape (and a
// thin bezel) into the static and spine atlases alike. The leftover width is the
// gap that keeps neighbouring symbols from merging into one block.
//
// Anything that slices, masks or frames a symbol has to use these rather than
// the cell pitch, or it will cut through transparent margin instead of art.
export const SYMBOL_CARD_H = SYMBOL_SIZE * (292 / 300);
export const SYMBOL_CARD_W = SYMBOL_CARD_H * 0.775;

export const REEL_PADDING = GEN_REEL_PADDING;

// per-reel visible row counts (diamond board: e.g. [4,3,2,3,4])
export const NUM_ROWS: number[] = GEN_NUM_ROWS;
// the tallest reel defines the board's vertical extent (mask/frame height)
export const MAX_ROWS = Math.max(...NUM_ROWS);

// Full-reel-column WILD art pool: each premium inmate (H1..H5) standing in a
// padded cell. A Wild Reel drop (WildReelSlide) and a Stretch (StretchFx) each
// pick ONE of these at random per appearance, so the risen wild column varies.
// `width`/`height` are the source PNG dims used for cover-fit (never squished).
export const WILD_REEL_ARTS = [
	{ key: 'wrReelH1', width: 512, height: 1680 },
	{ key: 'wrReelH2', width: 512, height: 1680 },
	{ key: 'wrReelH3', width: 512, height: 1680 },
	{ key: 'wrReelH4', width: 512, height: 1680 },
	{ key: 'wrReelH5', width: 512, height: 1680 },
] as const;

export type WildReelArt = (typeof WILD_REEL_ARTS)[number];

export const pickWildReelArt = (): WildReelArt =>
	WILD_REEL_ARTS[Math.floor(Math.random() * WILD_REEL_ARTS.length)];

// How far the reserved cells reach below the board. The cells are openings in
// the generated cell-block chassis now, so the beam's own height is the real
// extent — see chassisArt.ts. Kept under the old name because FrameMorphHud
// drops the WAYS/WIN rail by exactly this much.
export const LOCKED_SLOTS_BOTTOM_EXTENT = CHASSIS_BOTTOM_EXTENT;

// initial board derived from config: numRows[reel] visible + top/bottom padding.
export const INITIAL_BOARD: RawSymbol[][] = buildInitialBoard();

// x = reel count, y = tallest reel (short reels are vertically CENTERED into
// this height to form the diamond - see getReelYOffset in utils.ts).
export const BOARD_DIMENSIONS = { x: INITIAL_BOARD.length, y: MAX_ROWS };

export const BOARD_SIZES = {
	width: SYMBOL_SIZE * BOARD_DIMENSIONS.x,
	height: SYMBOL_SIZE * BOARD_DIMENSIONS.y,
};

export const BACKGROUND_RATIO = 2039 / 1000;
export const PORTRAIT_BACKGROUND_RATIO = 1242 / 2208;
const PORTRAIT_RATIO = 800 / 1422;
const LANDSCAPE_RATIO = 1600 / 900;
const DESKTOP_RATIO = 1422 / 800;

const DESKTOP_HEIGHT = 800;
const LANDSCAPE_HEIGHT = 900;
const PORTRAIT_HEIGHT = 1422;
export const DESKTOP_MAIN_SIZES = { width: DESKTOP_HEIGHT * DESKTOP_RATIO, height: DESKTOP_HEIGHT };
export const LANDSCAPE_MAIN_SIZES = {
	width: LANDSCAPE_HEIGHT * LANDSCAPE_RATIO,
	height: LANDSCAPE_HEIGHT,
};
export const PORTRAIT_MAIN_SIZES = {
	width: PORTRAIT_HEIGHT * PORTRAIT_RATIO,
	height: PORTRAIT_HEIGHT,
};

export const HIGH_SYMBOLS = GEN_HIGH_SYMBOLS;

export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

const HIGH_SYMBOL_SIZE = 0.9;
const LOW_SYMBOL_SIZE = 0.9;
const SPECIAL_SYMBOL_SIZE = 1;

const SPIN_OPTIONS_SHARED = {
	reelFallInDelay: 80,
	reelPaddingMultiplierNormal: 1.25,
	// was 18 (an ~18x drawn-out scatter tension hang). Kept short so the
	// scatter "anticipation" is a quick beat, not a slow crawl — and it's now
	// fully skippable with a tap / space.
	reelPaddingMultiplierAnticipated: 4,
	reelFallOutDelay: 145,
};

export const SPIN_OPTIONS_DEFAULT = {
	...SPIN_OPTIONS_SHARED,
	symbolFallInSpeed: 3.5,
	symbolFallInInterval: 30,
	symbolFallInBounceSpeed: 0.15,
	symbolFallInBounceSizeMulti: 0.5,
	symbolFallOutSpeed: 3.5,
	symbolFallOutInterval: 20,
};

export const SPIN_OPTIONS_FAST = {
	...SPIN_OPTIONS_SHARED,
	// turbo drops: much snappier fall + near-instant settle (hacksaw-style)
	symbolFallInSpeed: 12,
	symbolFallInInterval: 0,
	symbolFallInBounceSpeed: 0.6,
	symbolFallInBounceSizeMulti: 0.2,
	symbolFallOutSpeed: 12,
	symbolFallOutInterval: 0,
};

export const MOTION_BLUR_VELOCITY = 31;

export const zIndexes = {
	background: {
		backdrop: -3,
		normal: -2,
		feature: -1,
	},
};

const explosion = {
	type: 'spine',
	assetKey: 'explosion',
	animationName: 'explosion',
	sizeRatios: { width: 1, height: 1 },
};

const h1Static = { type: 'sprite', assetKey: 'h1.webp', sizeRatios: { width: 1, height: 1 } };
const h2Static = { type: 'sprite', assetKey: 'h2.webp', sizeRatios: { width: 1, height: 1 } };
const h3Static = { type: 'sprite', assetKey: 'h3.webp', sizeRatios: { width: 1, height: 1 } };
const h4Static = { type: 'sprite', assetKey: 'h4.webp', sizeRatios: { width: 1, height: 1 } };
const h5Static = { type: 'sprite', assetKey: 'h5.webp', sizeRatios: { width: 1, height: 1 } };

const l1Static = { type: 'sprite', assetKey: 'l1.webp', sizeRatios: { width: 1, height: 1 } };
const l2Static = { type: 'sprite', assetKey: 'l2.webp', sizeRatios: { width: 1, height: 1 } };
const l3Static = { type: 'sprite', assetKey: 'l3.webp', sizeRatios: { width: 1, height: 1 } };
const l4Static = { type: 'sprite', assetKey: 'l4.webp', sizeRatios: { width: 1, height: 1 } };
const l5Static = { type: 'sprite', assetKey: 'l5.webp', sizeRatios: { width: 1, height: 1 } };

const sStatic = { type: 'sprite', assetKey: 's.png', sizeRatios: { width: 1, height: 1 } };
// WILD: bespoke White Room straitjacket "WILD" card (standalone transparent PNG,
// asset key 'wrWild'). Sprite-only in every state so it reads identically on the
// board, in unlocked slots and as a risen Wild Reel.
const wStatic = { type: 'sprite', assetKey: 'wrWild', sizeRatios: { width: 1, height: 1 } };
// New special-cell symbols (bonus every spin + rare base-game unlock). Sprite-only
// White Room cards, keyed transparent PNGs. They only ever appear inside the
// reserved cells (LockedSlots), never on the reel strips.
const stretchStatic = { type: 'sprite', assetKey: 'wrStretch', sizeRatios: { width: 1, height: 1 } };
const splitStatic = { type: 'sprite', assetKey: 'wrSplit', sizeRatios: { width: 1, height: 1 } };
const cloneStatic = { type: 'sprite', assetKey: 'wrClone', sizeRatios: { width: 1, height: 1 } };
// Madam's Eye: turns every split symbol wild for the spin, then resolves to a wild
const meStatic = { type: 'sprite', assetKey: 'me.png', sizeRatios: { width: 1, height: 1 } };
// Haunted Mirror: intact while on the reels, cracked once it bursts/resolves
const hmIntactStatic = { type: 'sprite', assetKey: 'hm_intact.png', sizeRatios: { width: 1, height: 1 } };
const hmCrackedStatic = { type: 'sprite', assetKey: 'hm_cracked.png', sizeRatios: { width: 1, height: 1 } };

// Symbol states:
//   static  -> the PURE static card sprite (no idle shimmer/sheen/breathe)
//   spin    -> baked SMEAR frame (vertical motion blur, 300x480) so the
//              falling reels streak; board mask clips at board edges
//   land    -> '<id>_land' spine: weighty bottom-pinned squash-and-stretch
//   win     -> '<id>' spine: punch + wobble + glow flash + sheen + shards
//              (the green plasma border around the connected combination is
//              drawn by PlasmaLiner as ONE merged outline, not per symbol)
//   postWin -> '<id>_postwin' spine: a LOOPING mesh-deform ripple of the
//              card's own artwork (the symbol itself gently undulates like a
//              living/haunted photograph) - winners keep animating while they
//              rest, no green overlay or baked fire ring.
// postWinStatic stays the crisp card sprite (the apparition pane slicing
// needs a deterministic plain frame).
// Spine asset keys match assets.ts (e.g. 'H1'), animations the skeleton ids.
const spineState = (assetKey: string, animationName: string) => ({
	type: 'spine',
	assetKey,
	animationName,
	sizeRatios: { width: 1, height: 1 },
});

// smear frames bleed above/below the cell so a spinning reel reads as one
// continuous streak (board mask clips the top/bottom board edges)
const blurState = (cardAssetKey: string) => ({
	type: 'sprite',
	assetKey: cardAssetKey.replace('.', '_blur.'),
	sizeRatios: { width: 1, height: 1.6 },
});

const cardStates = (
	card: { type: string; assetKey: string; sizeRatios: { width: number; height: number } },
	spineKey: string,
	id: string,
) => ({
	explosion,
	win: spineState(spineKey, id),
	postWin: spineState(spineKey, `${id}_postwin`),
	postWinStatic: card,
	static: card,
	spin: blurState(card.assetKey),
	land: spineState(spineKey, `${id}_land`),
});

export const SYMBOL_INFO_MAP = {
	H1: cardStates(h1Static, 'H1', 'h1'),
	H2: cardStates(h2Static, 'H2', 'h2'),
	H3: cardStates(h3Static, 'H3', 'h3'),
	H4: cardStates(h4Static, 'H4', 'h4'),
	H5: cardStates(h5Static, 'H5', 'h5'),
	L1: cardStates(l1Static, 'L1', 'l1'),
	L2: cardStates(l2Static, 'L2', 'l2'),
	L3: cardStates(l3Static, 'L3', 'l3'),
	L4: cardStates(l4Static, 'L4', 'l4'),
	L5: cardStates(l5Static, 'L5', 'l5'),
	// WILD is sprite-only (like HM/ME): the generated straitjacket card is shown
	// in every state; the pulse/land squash comes from SymbolSprite, and the
	// wild-rise / explode FX are owned by the wildReel/madamsEye handlers.
	W: {
		explosion,
		postWin: wStatic,
		postWinStatic: wStatic,
		static: wStatic,
		spin: wStatic,
		win: wStatic,
		land: wStatic,
	},
	// STRETCH / SPLIT / CLONE: sprite-only special-cell symbols (like W). The
	// feature FX are owned by their book-event handlers; here every state is the
	// same card so the drop-in / land squash reads cleanly in the cell.
	STRETCH: {
		explosion,
		postWin: stretchStatic,
		postWinStatic: stretchStatic,
		static: stretchStatic,
		spin: stretchStatic,
		win: stretchStatic,
		land: stretchStatic,
	},
	SPLIT: {
		explosion,
		postWin: splitStatic,
		postWinStatic: splitStatic,
		static: splitStatic,
		spin: splitStatic,
		win: splitStatic,
		land: splitStatic,
	},
	CLONE: {
		explosion,
		postWin: cloneStatic,
		postWinStatic: cloneStatic,
		static: cloneStatic,
		spin: cloneStatic,
		win: cloneStatic,
		land: cloneStatic,
	},
	S: cardStates(sStatic, 'S', 's'),
	// Haunted Mirror: intact on the reels, cracked once it bursts and resolves.
	// HM keeps deterministic sprite states because the burst visuals are owned
	// by MirrorShatter/ApparitionOverlay and the intact->cracked swap must be
	// frame-exact with them. Its Spine (assetKey 'HM', anims hm/hm_land/
	// hm_break) ships in the mm_symbols atlas for future use. No burn frame:
	// HM always resolves to its revealed symbol before a win can rest.
	HM: {
		explosion,
		postWin: hmCrackedStatic,
		postWinStatic: hmCrackedStatic,
		static: hmIntactStatic,
		spin: blurState('hm_intact.png'),
		win: hmCrackedStatic,
		land: hmIntactStatic,
	},
	// Madam's Eye: sprite-only states like HM - the conversion visuals are owned
	// by the madamsEye book event handler (flash + split cells turning wild),
	// and ME always resolves into a wild before a win can rest on it.
	ME: {
		explosion,
		postWin: meStatic,
		postWinStatic: meStatic,
		static: meStatic,
		spin: blurState('me.png'),
		win: meStatic,
		land: meStatic,
	},
} as const;

export const SCATTER_LAND_SOUND_MAP = {
	1: 'sfx_scatter_stop_1',
	2: 'sfx_scatter_stop_2',
	3: 'sfx_scatter_stop_3',
	4: 'sfx_scatter_stop_4',
	5: 'sfx_scatter_stop_5',
} as const;
