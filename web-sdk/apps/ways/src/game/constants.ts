import _ from 'lodash';

import type { RawSymbol, SymbolState } from './types';

export const SYMBOL_SIZE = 145;

export const REEL_PADDING = 0.53;

// initial board: 4 visible rows + top/bottom padding = 6 entries per reel
export const INITIAL_BOARD: RawSymbol[][] = [
	[{ name: 'H1' }, { name: 'H1' }, { name: 'L4' }, { name: 'L4' }, { name: 'L4' }, { name: 'L1' }],
	[{ name: 'H1' }, { name: 'H1' }, { name: 'L4' }, { name: 'L4' }, { name: 'H3' }, { name: 'L2' }],
	[{ name: 'L2' }, { name: 'L2' }, { name: 'L3' }, { name: 'L3' }, { name: 'H2' }, { name: 'L1' }],
	[{ name: 'L3' }, { name: 'H2' }, { name: 'H2' }, { name: 'H4' }, { name: 'H4' }, { name: 'L3' }],
	[{ name: 'L3' }, { name: 'H2' }, { name: 'H2' }, { name: 'L2' }, { name: 'L2' }, { name: 'L4' }],
];

export const BOARD_DIMENSIONS = { x: INITIAL_BOARD.length, y: INITIAL_BOARD[0].length - 2 };

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

export const HIGH_SYMBOLS = ['H1', 'H2', 'H3', 'H4', 'H5'];

export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

const HIGH_SYMBOL_SIZE = 0.9;
const LOW_SYMBOL_SIZE = 0.9;
const SPECIAL_SYMBOL_SIZE = 1;

const SPIN_OPTIONS_SHARED = {
	reelFallInDelay: 80,
	reelPaddingMultiplierNormal: 1.25,
	reelPaddingMultiplierAnticipated: 18,
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
	symbolFallInSpeed: 7,
	symbolFallInInterval: 0,
	symbolFallInBounceSpeed: 0.3,
	symbolFallInBounceSizeMulti: 0.25,
	symbolFallOutSpeed: 7,
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
const wStatic = { type: 'sprite', assetKey: 'w.png', sizeRatios: { width: 1, height: 1 } };
// Haunted Mirror: intact while on the reels, cracked once it bursts/resolves
const hmIntactStatic = { type: 'sprite', assetKey: 'hm_intact.png', sizeRatios: { width: 1, height: 1 } };
const hmCrackedStatic = { type: 'sprite', assetKey: 'hm_cracked.png', sizeRatios: { width: 1, height: 1 } };

// All symbol states use our full-bleed card art; win/land motion is handled
// by SymbolSprite (pulse/pop) instead of the old sample spine animations.
const cardStates = (card: { type: string; assetKey: string; sizeRatios: { width: number; height: number } }) => ({
	explosion,
	win: card,
	postWinStatic: card,
	static: card,
	spin: card,
	land: card,
});

export const SYMBOL_INFO_MAP = {
	H1: cardStates(h1Static),
	H2: cardStates(h2Static),
	H3: cardStates(h3Static),
	H4: cardStates(h4Static),
	H5: cardStates(h5Static),
	L1: cardStates(l1Static),
	L2: cardStates(l2Static),
	L3: cardStates(l3Static),
	L4: cardStates(l4Static),
	L5: cardStates(l5Static),
	W: cardStates(wStatic),
	S: cardStates(sStatic),
	// Haunted Mirror: intact on the reels, cracked once it bursts and resolves
	HM: {
		explosion,
		postWinStatic: hmCrackedStatic,
		static: hmIntactStatic,
		spin: hmIntactStatic,
		win: hmCrackedStatic,
		land: hmIntactStatic,
	},
} as const;

export const SCATTER_LAND_SOUND_MAP = {
	1: 'sfx_scatter_stop_1',
	2: 'sfx_scatter_stop_2',
	3: 'sfx_scatter_stop_3',
	4: 'sfx_scatter_stop_4',
	5: 'sfx_scatter_stop_5',
} as const;
