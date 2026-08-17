import { stateBet, stateBetDerived } from 'state-shared';

import { playBet } from '../game/utils';
import { bookByLabel } from './data/tombstone_books';

/** Storybook shares `stateBet` across stories. Unlock and force a speed so a
 * leftover turbo click (or the dedicated turbo banner story) cannot leak. */
export const forceStorySpeed = (turbo = false) => {
	stateBetDerived.updateIsTurbo(turbo, { persistent: true });
	stateBet.isSuperTurbo = false;
};

export const playStory = (label: string, opts?: { turbo?: boolean }) => async () => {
	forceStorySpeed(!!opts?.turbo);
	const data = bookByLabel(label);
	stateBet.activeBetModeKey = data.mode ?? 'base';
	console.log(`Running the "${label}" showcase book (${data.payoutMultiplier}x)`);
	await playBet({ ...data, state: data.events } as never);
};
