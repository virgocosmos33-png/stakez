/**
 * Shared geometry so two components agree on ONE truth:
 *   - Live plaques are FRAME_SEATS.plaques (PSD box + pallet) via sceneToMain.
 *   - isSpecialBarVertical decides SpecialBar vs FrameMorphHud — both use those seats.
 *
 * Keeping the vertical decision here stops the two from drifting — if the left
 * rail ever stops standing upright, WAYS/WIN move under the board, and vice-versa.
 */
import { SYMBOL_SIZE, SYMBOL_CARD_W, BOARD_PLATE_PAD } from './constants';

/** plaques sit inside the wood field, clear of the iron rivet band */
export const PLAQUE_WIDTH_FRACTION = 0.7;
/** one card wide, like the reels it belongs to */
export const MAX_RAIL_W = SYMBOL_CARD_W / PLAQUE_WIDTH_FRACTION;
/** below this the side margin cannot hold a readable cell — lie the rail down */
export const MIN_SIDE_WIDTH = MAX_RAIL_W * 0.8;

export const BOARD_GAP = SYMBOL_SIZE * 0.12;
/** BoardPlate's wooden face overhangs the board box by its own PAD */
export const PLATE_OVERHANG = BOARD_PLATE_PAD;
export const EDGE_MARGIN = 6;

type BoardBox = { x: number; width: number; scale?: number; pivot?: { x: number; y: number } };

/** clear room the layout leaves to the LEFT of the wooden plate, in board units */
export const specialBarSideWidth = (board: BoardBox): number => {
	const scale = board.scale ?? 1;
	const pivotX = board.pivot?.x ?? board.width * 0.5;
	const visualLeft = board.x - pivotX * scale;
	const railRight = visualLeft - PLATE_OVERHANG * scale - BOARD_GAP * scale;
	return railRight - EDGE_MARGIN;
};

/** Same overlap the top WAYS / MULTI pair uses. */
export const HANG_PAIR_GAP = -0.16;

/** Left / right centres of a two-plate hang, matching the sky pair. */
export const hangPairXs = (cx: number, wellW: number) => {
	const gap = wellW * HANG_PAIR_GAP;
	return {
		left: cx - (wellW + gap) / 2,
		right: cx + (wellW + gap) / 2,
		gap,
	};
};

/**
 * WAYS+MULTI hang above the short right reels, WIN on that timber lip,
 * on every layout. Portrait used to dump the boxes under the board
 * (FrameMorphHud); that path is unused now.
 */
export const isSpecialBarVertical = (_board?: BoardBox): boolean => true;
