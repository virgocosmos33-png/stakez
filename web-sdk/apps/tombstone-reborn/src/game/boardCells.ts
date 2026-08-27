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

/** Reel a parked nudge totem already owns. Pending look-ahead is not cover —
 *  that blanked the whole reel while it was still spinning. */
export const isNudgeCoveredReel = (reel: number): boolean =>
	stateGame.nudgeCoverReel === reel || stateGame.nudgeCoverReels.includes(reel);

/** Cell currently under a parked / growing totem. */
export const isNudgeCoveredCell = (reel: number, row: number): boolean =>
	stateGame.nudgeCoverCells.some((cell) => cell.reel === reel && cell.row === row);

/** Cell whose reel face is hidden while WildFlip owns the card. */
export const isWildFlipCovered = (reel: number, row: number): boolean =>
	stateGame.wildFlipCover.some((cell) => cell.reel === reel && cell.row === row);

/** Cell sliding out the pocket bottom this nudge step. */
export const isNudgeSliding = (reel: number, row: number): boolean =>
	stateGame.nudgePush[reel]?.rows.includes(row) ?? false;

/** Cell below the totem, shoved down with the evicted stack this step. */
export const isNudgeBumping = (reel: number, row: number): boolean =>
	stateGame.nudgePush[reel]?.bumpRows.includes(row) ?? false;

/** Visible cells that are not mid-shove. A parked nudge stack CAN be split. */
export const filterSplitCells = <T extends BoardCell>(cells: T[]): T[] =>
	filterVisibleCells(cells).filter(
		(cell) => !isNudgeSliding(cell.reel, cell.row) && !isNudgeBumping(cell.reel, cell.row),
	);

/** Gunsmoke cannot shoot the totem or the rows it already swallowed. */
export const filterGunsmokeCells = <T extends BoardCell>(cells: T[]): T[] =>
	filterVisibleCells(cells).filter(
		(cell) =>
			!isNudgeCoveredCell(cell.reel, cell.row) &&
			!isNudgeSliding(cell.reel, cell.row) &&
			!isNudgeBumping(cell.reel, cell.row),
	);
