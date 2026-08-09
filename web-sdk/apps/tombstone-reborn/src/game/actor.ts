import _ from 'lodash';

import { stateBet } from 'state-shared';
import { checkIsMultipleRevealEvents } from 'utils-book';
import { createPrimaryMachines, createIntermediateMachines, createGameActor } from 'utils-xstate';

import type { Bet } from './typesBookEvent';
import { eventEmitter } from './eventEmitter';
import { stateXstateDerived } from './stateXstate';
import { playBet, convertTorResumableBet } from './utils';
import { stateGameDerived } from './stateGame.svelte';

const primaryMachines = createPrimaryMachines<Bet>({
	onResumeGameActive: (betToResume) => convertTorResumableBet(betToResume),
	onResumeGameInactive: (betToResume) => {
		const lastRevealEvent = _.findLast(
			betToResume.state,
			(emitterEvent) => emitterEvent?.type === 'reveal',
		);

		if (lastRevealEvent) stateGameDerived.enhancedBoard.settle(lastRevealEvent.board);
	},
	onNewGameStart: async () => {
		// clear the win presentation (dim overlay, glint cycle) the moment the
		// next spin starts - the reveal event only arrives after the RGS responds
		eventEmitter.broadcast({ type: 'winCycleStop' });
		// Same reason the wild columns, split panes, clone morphs and stretch
		// racks leave NOW: they are painted over the reels rather than being part
		// of them, so without this they hang over an already-spinning board for
		// the whole RGS round trip. Started here rather than awaited first, so
		// they ride out alongside the symbols instead of after them.
		const featuresLeaving = eventEmitter.broadcastAsync({ type: 'featureFxFallOut' });
		if ((stateBet.isTurbo && stateXstateDerived.isAutoBetting()) || stateBet.isSpaceHold) {
			await featuresLeaving;
			return;
		}
		stateBet.winBookEventAmount = 0;
		await Promise.all([featuresLeaving, stateGameDerived.enhancedBoard.preSpin({})]);
	},
	onNewGameError: () => stateGameDerived.enhancedBoard.settle(),
	onPlayGame: async (bet) => await playBet(bet),
	checkIsBonusGame: (bet) => checkIsMultipleRevealEvents({ bookEvents: bet.state }),
});

const intermediateMachines = createIntermediateMachines(primaryMachines);

export const gameActor = createGameActor(intermediateMachines);
