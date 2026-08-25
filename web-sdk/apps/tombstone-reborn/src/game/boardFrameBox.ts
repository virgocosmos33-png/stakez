import { CELL_PITCH_X, REEL_PADDING, SYMBOL_SIZE, NUM_ROWS, MAX_ROWS } from './constants';

const cellLeft = (reel: number) => CELL_PITCH_X * (reel + REEL_PADDING) - CELL_PITCH_X / 2;

const authoredReelTop = (i: number) => {
	const rows = NUM_ROWS[i] ?? MAX_ROWS;
	if (i === NUM_ROWS.length - 1) {
		const neighbor = NUM_ROWS[i - 1] ?? rows;
		return ((MAX_ROWS - neighbor) / 2 + (neighbor - rows) / 2) * SYMBOL_SIZE;
	}
	return ((MAX_ROWS - rows) / 2) * SYMBOL_SIZE;
};

/** Authored card windows — letterboxed into FRAME_SEATS.pocket (MAIN FRAME hole). */
export const boardContentBox = () => {
	const tops = NUM_ROWS.map((_, i) => authoredReelTop(i));
	const bottoms = tops.map((top, i) => top + NUM_ROWS[i] * SYMBOL_SIZE);
	const x = cellLeft(0);
	const y = Math.min(...tops);
	return {
		x,
		y,
		w: cellLeft(NUM_ROWS.length - 1) + CELL_PITCH_X - x,
		h: Math.max(...bottoms) - y,
	};
};
