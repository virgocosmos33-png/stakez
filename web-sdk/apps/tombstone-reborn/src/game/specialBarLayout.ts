/**
 * Shared geometry so two components agree on ONE truth:
 *   - SpecialBar.svelte draws stacked WAYS / MULTI / WIN nameplates on the
 *     right when the side margin is wide enough.
 *   - FrameMorphHud.svelte shows the same stack under the board when it is not.
 *
 * Keeping the vertical decision here stops the two from drifting — if the left
 * rail ever stops standing upright, WAYS/WIN move under the board, and vice-versa.
 */
import { SYMBOL_SIZE, SYMBOL_CARD_W, BOARD_PLATE_PAD } from './constants';
import { stateLayoutDerived } from './stateLayout';

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

/**
 * Desktop / landscape: WAYS+MULTI hang on the skull wall, WIN on the bar.
 * Portrait / tablet: FrameMorphHud shows the same boxes under the board.
 */
export const isSpecialBarVertical = (_board?: BoardBox): boolean => {
	const { width, height } = stateLayoutDerived.canvasSizes();
	return width / Math.max(height, 1) >= 1.15;
};
