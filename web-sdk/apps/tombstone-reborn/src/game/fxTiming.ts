// Feature + presentation timing under the three speed tiers.
//
// Shared `timeScale` (1.35 / 1.8) is too close to feel like turbo vs super
// turbo. This game uses its own present scale so:
//   normal       1x   — every beat is readable, one after another
//   turbo        2x   — same sequence, cut in half
//   super turbo  3.2x — same sequence, slammed
import { stateBet } from 'state-shared';
import { waitForTimeout } from 'utils-shared/wait';

import { SPIN_OPTIONS_DEFAULT, SPIN_OPTIONS_FAST, SPIN_OPTIONS_SUPER } from './constants';

const presentScale = () => {
	if (stateBet.isSuperTurbo) return 3.2;
	if (stateBet.isTurbo) return 2;
	return 1;
};

/** a tween/animation length in ms, shortened by the active speed tier */
export const fxDur = (ms: number) => ms / presentScale();

/** a pause between feature beats, shortened by the active speed tier */
export const fxWait = (ms: number) => waitForTimeout(fxDur(ms));

/** hold after a feature resolves so the next event does not pile on */
export const fxHold = () => fxWait(400);

/** reel / plaque fall speeds for the active tier */
export const currentSpinOptions = () => {
	if (stateBet.isSuperTurbo) return SPIN_OPTIONS_SUPER;
	if (stateBet.isTurbo) return SPIN_OPTIONS_FAST;
	return SPIN_OPTIONS_DEFAULT;
};
