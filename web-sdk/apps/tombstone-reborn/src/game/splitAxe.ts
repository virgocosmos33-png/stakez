import { SYMBOL_CARD_H } from './constants';

/**
 * Live split weapon: workspace `axe split.png`.
 * Tip = left bit. Knob = right handle. Native angle is pommel → tip.
 * Tint is board_frame bright grain (0x5b4e44) lifted so steel reads as
 * warm timber, not a black multiply.
 */
export const SPLIT_AXE = {
	artW: 1536,
	artH: 1024,
	tip: { x: 30 / 1536, y: 387 / 1024 },
	knob: { x: 1514 / 1536, y: 173 / 1024 },
	nativeBlade: 2.998375094188178,
	tint: 0xb69c88,
} as const;

export const SPLIT_AXE_W = SYMBOL_CARD_H * 1.08;
export const SPLIT_AXE_H = SPLIT_AXE_W * (SPLIT_AXE.artH / SPLIT_AXE.artW);
