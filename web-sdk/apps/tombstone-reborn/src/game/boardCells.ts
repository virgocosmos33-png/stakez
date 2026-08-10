/**
 * Diamond-board cell validity.
 *
 * Book events use PADDED row indices (row 1 = first visible). Reels are short
 * of MAX_ROWS and SymbolWrap culls anything outside each reel's window — but
 * overlays (target lock, split panes, morphs) sit above the board and will
 * happily paint brackets in the empty graveyard gaps if handed a pad row or an
 * out-of-range index. Every feature overlay must go through these helpers.
 */
import { stateGame } from './stateGame.svelte';

export type BoardCell = { reel: number; row: number };

/** True when (reel, row) is a live visible socket on the current board. */
export const isVisibleBoardCell = (reel: number, row: number): boolean => {
	if (!Number.isFinite(reel) || !Number.isFinite(row)) return false;
	if (reel < 0 || row < 0) return false;
	const symbols = stateGame.board[reel]?.reelState.symbols;
	if (!symbols || symbols.length < 3) return false;
	// padded strip: index 0 and length-1 are off-window pads
	return row >= 1 && row <= symbols.length - 2;
};

/** Drop pad / OOB / missing-reel cells from a book position list. */
export const filterVisibleCells = <T extends BoardCell>(cells: T[]): T[] =>
	cells.filter((cell) => isVisibleBoardCell(cell.reel, cell.row));
