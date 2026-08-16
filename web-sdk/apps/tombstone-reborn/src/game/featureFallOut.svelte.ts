// Feature art leaving the board with the reels.
//
// The wild columns, split panes, clone morphs and the stretch rack are painted
// OVER the reels rather than being part of them, so they don't fall out when the
// reels do. They used to be dropped instantly instead: on a fresh spin that
// happens only once the reveal arrives, which is after the RGS has answered, so
// a standing wild column hung over an already-spinning board for as long as the
// round trip took. In the bonus it popped out of existence instead.
//
// Every overlay now rides this offset down and off the bottom edge on the same
// curve the symbols use, then clears itself.
import { Tween } from 'svelte/motion';

import { SYMBOL_SIZE } from './constants';
import { currentSpinOptions } from './fxTiming';

/** matches the push the wild column gives a reel: clear of the bottom edge
 * whatever the reel's height, without measuring each one */
const FALL_ROWS = 6;

const spinOptions = () => currentSpinOptions();

/** how far the art travels, in pixels */
export const fallOutDistance = () => FALL_ROWS * SYMBOL_SIZE;

/** the reels solve their fall-out as distance / speed (pixels per ms), so the
 * art matches simply by doing the same sum */
export const fallOutDuration = () => fallOutDistance() / spinOptions().symbolFallOutSpeed;

/**
 * Ride the art down and off the board, then hand back so the caller can clear
 * it. Resolves immediately when `showing` is false, which keeps a plain spin
 * with no feature art on screen from paying for any of this.
 */
export const fallOutFeatureFx = async (offset: Tween<number>, showing: boolean) => {
	if (!showing) return;
	await offset.set(fallOutDistance(), { duration: fallOutDuration() });
};
