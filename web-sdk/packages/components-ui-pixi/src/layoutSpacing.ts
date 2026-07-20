import { UI_BASE_SIZE, UI_BASE_FONT_SIZE } from './constants';

/** Unscaled intrinsic sizes of HUD pieces (matches each Button* / UiLabel). */
export const HUD_SIZE = {
	round: UI_BASE_SIZE,
	spin: UI_BASE_SIZE * 1.3,
	buyH: UI_BASE_SIZE * 0.55,
	/** UiLabel layout box (taller than the glyphs — do not use for edge padding). */
	labelBoxH: UI_BASE_FONT_SIZE * 2,
	/** Approximate rendered value glyph height in UiLabel. */
	labelGlyphH: UI_BASE_FONT_SIZE * 0.92,
} as const;

/** Layout scales used by Desktop / Landscape HUD. */
export const HUD_SCALE = {
	menu: 0.68,
	pair: 0.6,
	spin: 1,
	buy: 1,
	label: 0.58,
} as const;

/**
 * Single outer margin used on LEFT, RIGHT and BOTTOM so the HUD hugs the
 * canvas with equal padding on every side that has chrome.
 */
export const HUD_EDGE_PAD = 14;

/** Horizontal gap between the two buttons in a pair row. */
export const HUD_PAIR_STEP = UI_BASE_SIZE * HUD_SCALE.pair * 1.12;

/**
 * Bottom-up column stack with a constant EDGE gap between every neighbour.
 *
 * Button ys are centres. Label y is UiLabel's local origin (top of its box).
 * BET/BALANCE are positioned so the *visible glyphs* sit HUD_EDGE_PAD above
 * the bottom — matching the left/right column edge pad.
 */
export function stackHudColumn(height: number, gap = 18) {
	const hMenu = HUD_SIZE.round * HUD_SCALE.menu;
	const hPair = HUD_SIZE.round * HUD_SCALE.pair;
	const hSpin = HUD_SIZE.spin * HUD_SCALE.spin;
	const hBuy = HUD_SIZE.buyH * HUD_SCALE.buy;

	const s = HUD_SCALE.label;
	const boxH = HUD_SIZE.labelBoxH;
	const glyphH = HUD_SIZE.labelGlyphH;
	// UiLabel centres the Text at local y = boxH/2
	const topToVisualTop = (boxH / 2 - glyphH / 2) * s;
	const topToVisualBottom = (boxH / 2 + glyphH / 2) * s;

	// visible text bottom == canvas bottom - EDGE_PAD
	const yLabel = height - HUD_EDGE_PAD - topToVisualBottom;
	const labelVisualTop = yLabel + topToVisualTop;

	// pair sits above the *visible* BET/BALANCE text, not the empty label box
	const yPair = labelVisualTop - gap - hPair / 2;
	const ySpin = yPair - hPair / 2 - gap - hSpin / 2;
	const yMenu = yPair - hPair / 2 - gap - hMenu / 2;
	const yBuy = ySpin - hSpin / 2 - gap - hBuy / 2;

	return { yLabel, yPair, ySpin, yMenu, yBuy, gap, edgePad: HUD_EDGE_PAD };
}
