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
	const inFrame = $derived(props.y >= window.top && props.y <= window.bottom);
</script>

{#if props.debug || (show && inFrame)}
	<Container x={props.x} y={props.y}>
		{@render props.children()}
	</Container>
{/if}
