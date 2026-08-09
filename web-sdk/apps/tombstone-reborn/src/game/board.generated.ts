// TOMBSTONE REBORN board geometry. Mirrors the math board:
//   num_reels = 6, num_rows = [3, 4, 4, 2, 2, 1]
// Short reels are vertically CENTRED into the tallest reel's window so the
// board reads as a coffin/diamond silhouette (see getReelYOffset in utils.ts).
import type { RawSymbol } from './types';

export const GEN_NUM_REELS = 6;
export const GEN_NUM_ROWS: number[] = [3, 4, 4, 2, 2, 1];
export const GEN_SYMBOL_SIZE = 128;
export const GEN_REEL_PADDING = 0.53;
export const GEN_HIGH_SYMBOLS = ['H1', 'H2', 'H3', 'H4', 'H5'];

const FILL_POOL = ['H1', 'H2', 'H3', 'H4', 'H5', 'L1', 'L2', 'L3', 'L4', 'L5'];

// Deterministic starting board: numRows[reel] visible + top/bottom padding
// (2 extra entries per reel), matching the engine's padded strips.
export function buildInitialBoard(): RawSymbol[][] {
	return GEN_NUM_ROWS.map((rows, reel) => {
		const total = rows + 2;
		const out: RawSymbol[] = [];
		for (let i = 0; i < total; i++) {
			out.push({ name: FILL_POOL[(reel * 3 + i) % FILL_POOL.length] as RawSymbol['name'] });
		}
		return out;
	});
}
