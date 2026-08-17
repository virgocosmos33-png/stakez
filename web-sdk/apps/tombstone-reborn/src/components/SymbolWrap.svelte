<script lang="ts">
	import type { Snippet } from 'svelte';

	import { Container } from 'pixi-svelte';
	import { getContextBoard } from 'components-shared';

	import { getReelWindow } from '../game/utils';

	type Props = {
		debug?: boolean;
		reelIndex: number;
		x: number;
		y: number;
		animating: boolean;
		/** keep the node mounted while it travels out of the reel window */
		stay?: boolean;
		zIndex?: number;
		children: Snippet;
	};

	const props: Props = $props();
	const boardContext = getContextBoard();
	const show = $derived(
		(boardContext.animate && props.animating) || (!boardContext.animate && !props.animating),
	);
	// clip to THIS reel's centered window so a shorter diamond reel doesn't spill
	// symbols into the empty space above/below it (props.y already includes the
	// per-reel vertical offset).
	const window = $derived(getReelWindow(props.reelIndex));
	const inFrame = $derived(
		!!props.stay || (props.y >= window.top && props.y <= window.bottom),
	);
</script>

{#if props.debug || (show && inFrame)}
	<Container x={props.x} y={props.y} zIndex={props.zIndex ?? 0}>
		{@render props.children()}
	</Container>
{/if}
