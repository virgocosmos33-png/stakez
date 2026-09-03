import { CELL_PITCH_X } from './constants';

/**
 * board_slot_frame.png is 300×375. Inner opening measured from the pixels.
 * Use the width and bottom radius so square art cannot poke past the gold
 * lip. Leave the top open so Spine can rise under the top rail.
 */
export const SLOT_FRAME_SRC_W = 300;
export const SLOT_FRAME_SRC_H = 375;
export const SLOT_HOLE_SRC_W = 264;
export const SLOT_HOLE_SRC_H = 347;
export const SLOT_HOLE_SRC_R = 26;
export const SLOT_HOLE_W_FRAC = SLOT_HOLE_SRC_W / SLOT_FRAME_SRC_W;
export const SLOT_HOLE_H_FRAC = SLOT_HOLE_SRC_H / SLOT_FRAME_SRC_H;
export const SLOT_HOLE_R_FRAC = SLOT_HOLE_SRC_R / SLOT_FRAME_SRC_W;

export const slotFrameHole = (frameH: number) => ({
	w: CELL_PITCH_X * SLOT_HOLE_W_FRAC,
	h: frameH * SLOT_HOLE_H_FRAC,
	r: CELL_PITCH_X * SLOT_HOLE_R_FRAC,
});
