import _ from 'lodash';
import { stateBet } from 'state-shared';
import { createPlayBookUtils } from 'utils-book';
import { createGetEmptyPaddedBoard } from 'utils-slots';

import {
	SYMBOL_SIZE,
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
export const getSymbolX = (reelIndex: number) => SYMBOL_SIZE * (reelIndex + REEL_PADDING);
export const getSymbolY = (symbolIndexOfBoard: number) => (symbolIndexOfBoard + 0.5) * SYMBOL_SIZE;

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
export const getReelYOffset = (reelIndex: number) =>
	((MAX_ROWS - getReelRows(reelIndex)) / 2) * SYMBOL_SIZE;

// visible vertical window [top, bottom] of a reel in board-local space, used to
// clip/cull symbols to that reel's own centered window (confined diamond spin).
export const getReelWindow = (reelIndex: number) => {
	const top = getReelYOffset(reelIndex);
	return { top, bottom: top + getReelRows(reelIndex) * SYMBOL_SIZE };
};

export const getSymbolInfo = ({
	rawSymbol,
	state,
}: {
	rawSymbol: RawSymbol;
	state: SymbolState;
}) => {
	return SYMBOL_INFO_MAP[rawSymbol.name][state];
};
