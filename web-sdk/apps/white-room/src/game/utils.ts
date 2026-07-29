import _ from 'lodash';
import { stateBet } from 'state-shared';
import { createPlayBookUtils } from 'utils-book';
import { createGetEmptyPaddedBoard } from 'utils-slots';

import {
	SYMBOL_SIZE,
	CELL_PITCH_X,
	REEL_PADDING,
	SYMBOL_INFO_MAP,
	BOARD_DIMENSIONS,
	NUM_ROWS,
	MAX_ROWS,
} from './constants';
import { eventEmitter } from './eventEmitter';
import type { Bet, BookEventOfType } from './typesBookEvent';
import { bookEventHandlerMap } from './bookEventHandlerMap';
import { stateGame } from './stateGame.svelte';
import type { RawSymbol, SymbolState } from './types';

// general utils
export const { getEmptyBoard } = createGetEmptyPaddedBoard({
	reelsDimensions: BOARD_DIMENSIONS,
	rows: NUM_ROWS,
});
export const { playBookEvent, playBookEvents } = createPlayBookUtils({ bookEventHandlerMap });
export const playBet = async (bet: Bet) => {
	stateBet.winBookEventAmount = 0;
	await playBookEvents(bet.state);
	eventEmitter.broadcast({ type: 'stopButtonEnable' });
};

// resume bet
const BOOK_EVENT_TYPES_TO_RESERVE_FOR_SNAPSHOT = [
	'updateGlobalMult',
	'freeSpinTrigger',
	'updateFreeSpin',
	'setTotalWin',
];

export const convertTorResumableBet = (betToResume: Bet) => {
	const resumingIndex = Number(betToResume.event);
	const bookEventsBeforeResume = betToResume.state.filter(
		(_, eventIndex) => eventIndex < resumingIndex,
	);
	const bookEventsAfterResume = betToResume.state.filter(
		(_, eventIndex) => eventIndex >= resumingIndex,
	);

	const bookEventToCreateSnapshot: BookEventOfType<'createBonusSnapshot'> = {
		index: 0,
		type: 'createBonusSnapshot',
		bookEvents: bookEventsBeforeResume.filter((bookEvent) =>
			BOOK_EVENT_TYPES_TO_RESERVE_FOR_SNAPSHOT.includes(bookEvent.type),
		),
	};

	const stateToResume = [bookEventToCreateSnapshot, ...bookEventsAfterResume];

	return { ...betToResume, state: stateToResume };
};

// other utils
// SINGLE SOURCE OF TRUTH for column x. Columns step by CELL_PITCH_X (narrower
// than the square cell pitch, so the gutter around a portrait card matches the
// row gutter); rows still step by SYMBOL_SIZE. Every overlay that positions by
// (reel, row) must go through these instead of multiplying SYMBOL_SIZE itself,
// or it drifts off the symbols.
export const getSymbolX = (reelIndex: number) => CELL_PITCH_X * (reelIndex + REEL_PADDING);
export const getSymbolY = (symbolIndexOfBoard: number) => (symbolIndexOfBoard + 0.5) * SYMBOL_SIZE;
/** left edge of a reel column in board-local space */
export const getCellLeft = (reelIndex: number) => getSymbolX(reelIndex) - CELL_PITCH_X / 2;

// CURRENT visible row count of a reel. Normally the authored diamond height
// (NUM_ROWS), but Wild Reel grows a middle reel at runtime - the live board
// reel is the source of truth (padded array length - 2). Reading the reactive
// board here makes every offset/window recompute the moment a reel grows.
export const getReelRows = (reelIndex: number) => {
	// STRETCH in progress: use the animated display height so the reel grows
	// smoothly (mask, per-reel centering offset and culling window all follow it).
	const stretch = stateGame.reelStretch[reelIndex];
	if (stretch != null) return stretch.current;
	const live = stateGame.board[reelIndex]?.reelState.symbols.length;
	if (live && live >= 2) return live - 2;
	return NUM_ROWS[reelIndex] ?? MAX_ROWS;
};

// DIAMOND board: a reel with fewer than MAX_ROWS rows is centered vertically
// inside the tallest reel's window. Everything positioned by (reel,row) - the
// symbols themselves and every overlay - must add this per-reel offset so the
// shorter reels line up in the middle. A grown (Wild Reel) reel reaches
// MAX_ROWS, so its offset falls to 0 and its symbols push up to the top.
//
// A RACKED (STRETCH) reel is the exception: its BOTTOM edge stays bolted to the
// authored position (the bottom special cells live right under it) and all the
// extra height goes UP past the board top - the top chain pulls, the bottom
// clamp holds.
export const getReelYOffset = (reelIndex: number) => {
	const stretch = stateGame.reelStretch[reelIndex];
	if (stretch != null) {
		const live = stateGame.board[reelIndex]?.reelState.symbols.length;
		const authored = live && live >= 2 ? live - 2 : (NUM_ROWS[reelIndex] ?? MAX_ROWS);
		const authoredBottom = ((MAX_ROWS - authored) / 2 + authored) * SYMBOL_SIZE;
		return authoredBottom - stretch.current * SYMBOL_SIZE;
	}
	return ((MAX_ROWS - getReelRows(reelIndex)) / 2) * SYMBOL_SIZE;
};

// visible vertical window [top, bottom] of a reel in board-local space, used to
// clip/cull symbols to that reel's own centered window (confined diamond spin).
export const getReelWindow = (reelIndex: number) => {
	const top = getReelYOffset(reelIndex);
	return { top, bottom: top + getReelRows(reelIndex) * SYMBOL_SIZE };
};

// VERTICAL pitch between this reel's rows. SYMBOL_SIZE everywhere, except on a
// RACKED (STRETCH) reel, where the same rows are spread over the taller window
// so the distance between symbols grows.
export const getRowPitch = (reelIndex: number) => {
	const stretch = stateGame.reelStretch[reelIndex];
	if (stretch == null) return SYMBOL_SIZE;
	const live = stateGame.board[reelIndex]?.reelState.symbols.length;
	const rows = live && live >= 2 ? live - 2 : (NUM_ROWS[reelIndex] ?? MAX_ROWS);
	return rows > 0 ? (getReelRows(reelIndex) * SYMBOL_SIZE) / rows : SYMBOL_SIZE;
};

// Centre y of a cell in board-local space, by PADDED row index (row 1 = first
// visible row — the indexing every book event uses). EVERY overlay that
// positions on a (reel, row) cell must use this instead of multiplying
// SYMBOL_SIZE itself, or it lands on the pre-stretch position the moment a
// reel is racked (STRETCH) and the rows spread apart.
export const getCellCenterY = (reelIndex: number, rowIndex: number) =>
	getReelYOffset(reelIndex) + (rowIndex - 0.5) * getRowPitch(reelIndex);

export const getSymbolInfo = ({
	rawSymbol,
	state,
}: {
	rawSymbol: RawSymbol;
	state: SymbolState;
}) => {
	return SYMBOL_INFO_MAP[rawSymbol.name][state];
};
