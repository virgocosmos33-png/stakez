// Feature animation timing, under turbo.
//
// The clone morph, the split claw, the wild column, the stretch rack and the
// beats between them were all written as fixed millisecond durations, so turbo
// sped the REELS up and left every feature running at its full leisurely length
// — the faster you span, the larger the share of the round spent watching a
// clone charge up.
//
// Everything with a duration now goes through here, so both turbo tiers
// (1.35x and 1.8x, from stateBetDerived.timeScale) shorten the features by the
// same factor they shorten everything else.
import { stateBetDerived } from 'state-shared';
import { waitForTimeout } from 'utils-shared/wait';

/** a tween/animation length in ms, shortened by the active turbo tier */
export const fxDur = (ms: number) => ms / stateBetDerived.timeScale();

/** a pause between feature beats, shortened by the active turbo tier */
export const fxWait = (ms: number) => waitForTimeout(fxDur(ms));
