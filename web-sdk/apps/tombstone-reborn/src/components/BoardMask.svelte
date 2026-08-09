<script lang="ts">
	import { Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, MAX_ROWS } from '../game/constants';
	import { getReelRows } from '../game/utils';

	type Props = { debug?: boolean };

	const props: Props = $props();
	const context = getContext();

	// A STRETCH grows a reel past MAX_ROWS; let the mask breathe symmetrically so
	// the stretched reel overflows the nominal board a bit (per-reel SymbolWrap
	// culling keeps the other, un-stretched reels from spilling padding).
	const extra = $derived.by(() => {
		let maxRows = MAX_ROWS;
		for (let i = 0; i < context.stateGame.board.length; i++) {
			maxRows = Math.max(maxRows, getReelRows(i));
		}
		return Math.max(0, (maxRows - MAX_ROWS) * SYMBOL_SIZE);
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
	y={-extra / 2}
	width={context.stateGameDerived.boardLayout().width + SYMBOL_SIZE * 2}
	height={context.stateGameDerived.boardLayout().height + extra}
/>
