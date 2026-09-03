<script lang="ts">
	import { Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SLOT_FRAME_LIP, SYMBOL_SIZE } from '../game/constants';
	import { getReelRows, getReelYOffset } from '../game/utils';

	type Props = { debug?: boolean };

	const props: Props = $props();
	const context = getContext();

	/** How far live reels stick out past the authored board box. Stretch grows
	 * UP (bottom bolted), so extraTop covers that; extraBot only if a reel's
	 * window actually crosses the floor. NEVER split extra symmetrically — that
	 * opened the mask under the board and dropped cards into the HUD. */
	const extras = $derived.by(() => {
		const boxH = context.stateGameDerived.boardLayout().height;
		let extraTop = 0;
		let extraBot = 0;
		for (let i = 0; i < context.stateGame.board.length; i++) {
			const top = getReelYOffset(i);
			const bottom = top + getReelRows(i) * SYMBOL_SIZE;
			extraTop = Math.max(extraTop, -top);
			extraBot = Math.max(extraBot, bottom - boxH);
		}
		return {
			extraTop: extraTop + SLOT_FRAME_LIP,
			extraBot: extraBot + SLOT_FRAME_LIP,
		};
	});
</script>

{#if props.debug}
	<Rectangle
		alpha={0.5}
		backgroundColor={0xffffff}
		width={context.stateGameDerived.boardLayout().width}
		height={context.stateGameDerived.boardLayout().height}
	/>
{/if}

<Rectangle
	isMask
	x={-SYMBOL_SIZE}
	y={-extras.extraTop}
	width={context.stateGameDerived.boardLayout().width + SYMBOL_SIZE * 2}
	height={context.stateGameDerived.boardLayout().height + extras.extraTop + extras.extraBot}
/>
