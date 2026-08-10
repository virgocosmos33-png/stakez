import { onDestroy } from 'svelte';
import { stateUi } from 'state-shared';

import { getContext } from './context';

/**
 * Publish the top edge of the bottom control bar so the game can keep clear.
 *
 * A game may draw its own furniture under the board (Tombstone's WAYS / info /
 * WIN console) and has no way to work out where the controls start: the HUD is
 * laid out in the STANDARD design box, the game in its own, the two are fitted
 * to the window independently, and which layout is mounted depends on the
 * window's shape. Canvas px is the one space both can agree on — so the layout
 * that owns the bar measures it there and the game converts it back.
 *
 * `getLocalTop` gives the bar's top edge in this layout's own design px.
 * `alignBottom` must match the MainContainer the bar renders in, since that is
 * what decides how the design box maps onto the canvas.
 *
 * Layouts whose controls do NOT form a full-width bottom bar (tablet, which
 * runs them up the sides of the board) must not call this: there is no bar to
 * clear, and a floor taken off a side column would shove the game's furniture
 * halfway up the screen.
 */
export const publishHudBarTop = (
	getLocalTop: () => number,
	options: { alignBottom?: boolean } = {},
) => {
	const context = getContext();

	$effect(() => {
		const { height, scale } = context.stateLayoutDerived.mainLayoutStandard();
		const canvasHeight = context.stateLayoutDerived.canvasSizes().height;
		const top = getLocalTop();

		stateUi.hudBarTopScreenY = options.alignBottom
			? canvasHeight - (height - top) * scale
			: canvasHeight * 0.5 + (top - height * 0.5) * scale;
	});

	// Resizing across a breakpoint swaps the whole layout. Clear the reading on
	// the way out so nothing keeps clearing a bar that is no longer mounted —
	// the incoming layout publishes its own before the frame is drawn.
	onDestroy(() => {
		stateUi.hudBarTopScreenY = 0;
	});
};
