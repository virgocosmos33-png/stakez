import type { RawSymbol, SymbolState } from './types';
import { GEN_NUM_ROWS, GEN_SYMBOL_SIZE, GEN_REEL_PADDING, GEN_HIGH_SYMBOLS, buildInitialBoard } from './board.generated';

export const SYMBOL_SIZE = GEN_SYMBOL_SIZE;
export const REEL_PADDING = GEN_REEL_PADDING;

// per-reel visible row counts (coffin board: [3,4,4,2,2,1])
export const NUM_ROWS: number[] = GEN_NUM_ROWS;
// the tallest reel defines the board's vertical extent (mask/frame height)
export const MAX_ROWS = Math.max(...NUM_ROWS);

export const INITIAL_BOARD: RawSymbol[][] = buildInitialBoard();

// x = reel count, y = tallest reel (short reels are vertically CENTRED into
// this height to form the coffin silhouette - see getReelYOffset in utils.ts).
export const BOARD_DIMENSIONS = { x: INITIAL_BOARD.length, y: MAX_ROWS };
export const BOARD_SIZES = {
	width: SYMBOL_SIZE * BOARD_DIMENSIONS.x,
	height: SYMBOL_SIZE * BOARD_DIMENSIONS.y,
};

export const HIGH_SYMBOLS = GEN_HIGH_SYMBOLS;
export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

// ---------------------------------------------------------------------------
// Symbol art. Sprite cards drive static/spin; the win state plays each symbol's
// spine. Spine asset keys match assets.ts.
// ---------------------------------------------------------------------------
const sprite = (assetKey: string) => ({ type: 'sprite', assetKey, sizeRatios: { width: 1, height: 1 } });
const spine = (assetKey: string, animationName: string) => ({
	type: 'spine',
	assetKey,
	animationName,
	sizeRatios: { width: 1, height: 1 },
});

const cardStates = (staticKey: string, spineKey: string, id: string) => ({
	static: sprite(staticKey),
	spin: sprite(staticKey),
	land: spine(spineKey, `${id}_land`),
	win: spine(spineKey, id),
	postWin: spine(spineKey, `${id}_postwin`),
	postWinStatic: sprite(staticKey),
});

const spriteOnly = (assetKey: string) => ({
	static: sprite(assetKey),
	spin: sprite(assetKey),
	land: sprite(assetKey),
	win: sprite(assetKey),
	postWin: sprite(assetKey),
	postWinStatic: sprite(assetKey),
});

export const SYMBOL_INFO_MAP = {
	H1: cardStates('h1.webp', 'H1', 'h1'), // The Gunslinger
	H2: cardStates('h2.webp', 'H2', 'h2'), // The Duchess
	H3: cardStates('h3.webp', 'H3', 'h3'), // The Butcher
	H4: cardStates('h4.webp', 'H4', 'h4'), // The Card Shark
	H5: cardStates('h5.webp', 'H5', 'h5'), // The Preacher
	L1: cardStates('l1.webp', 'L1', 'l1'), // bullet
	L2: cardStates('l2.webp', 'L2', 'l2'), // whiskey
	L3: cardStates('l3.webp', 'L3', 'l3'), // spur
	L4: cardStates('l4.webp', 'L4', 'l4'), // horseshoe
	L5: cardStates('l5.webp', 'L5', 'l5'), // playing card
	W: spriteOnly('w.webp'), // the revolver
} as const;

export const zIndexes = {
	background: { backdrop: -3, normal: -2, feature: -1 },
};
