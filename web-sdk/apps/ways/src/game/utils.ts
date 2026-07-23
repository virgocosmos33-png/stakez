import _ from 'lodash';
import { stateBet } from 'state-shared';
import { createPlayBookUtils } from 'utils-book';
import { createGetEmptyPaddedBoard } from 'utils-slots';
import { waitForTimeout } from 'utils-shared/wait';

import { SYMBOL_SIZE, REEL_PADDING, SYMBOL_INFO_MAP, BOARD_DIMENSIONS } from './constants';
import { eventEmitter } from './eventEmitter';
import type { Bet, BookEventOfType } from './typesBookEvent';
import { bookEventHandlerMap } from './bookEventHandlerMap';
import { trace, traceBookHandlers } from './debugTrace';
import type { RawSymbol, SymbolState } from './types';

// general utils
export const { getEmptyBoard } = createGetEmptyPaddedBoard({ reelsDimensions: BOARD_DIMENSIONS });
export const { playBookEvent, playBookEvents } = createPlayBookUtils({
	// dev-only: logs start/finish/duration of every book event so a frozen
	// round shows exactly which event never completed
	bookEventHandlerMap: traceBookHandlers(bookEventHandlerMap),
});
export const playBet = async (bet: Bet) => {
	stateBet.winBookEventAmount = 0;
	trace('playBet start', `${bet.state.length} events`);
	try {
		await playBookEvents(bet.state);
		// super turbo: ALWAYS hold the settled board for a beat before the next
		// spin can start - empty spins otherwise chain instantly and read as
		// "the game skipped my spin". Win spins already pause for the count-up,
		// so the extra beat is imperceptible there.
		if (stateBet.isSuperTurbo) {
			await waitForTimeout(300);
		}
	} catch (error) {
		// a presentation error must NEVER strand the bet state machine outside
		// idle (that permanently disables the whole HUD) - log it and let the
		// round resolve; the next reveal re-settles the board from the book
		console.error('playBet: book presentation failed', error);
	} finally {
		trace('playBet done');
		eventEmitter.broadcast({ type: 'stopButtonEnable' });
	}
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

export const getSymbolInfo = ({
	rawSymbol,
	state,
}: {
	rawSymbol: RawSymbol;
	state: SymbolState;
}) => {
	return SYMBOL_INFO_MAP[rawSymbol.name][state];
};
