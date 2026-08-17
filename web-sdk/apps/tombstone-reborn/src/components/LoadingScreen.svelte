<script lang="ts">
	import { Container, Sprite } from 'pixi-svelte';
	import { FadeContainer, LoadingProgress } from 'components-pixi';

	import { getContext } from '../game/context';
	import SaloonScene from './SaloonScene.svelte';

	type Props = {
		onloaded: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// Skip the White Room intro carousel — once assets are loaded, enter the game.
	let entered = $state(false);
	$effect(() => {
		if (context.stateApp.loaded && !entered) {
			entered = true;
			props.onloaded();
		}
	});
</script>

<FadeContainer show={!context.stateApp.loaded}>
	<SaloonScene />
	<Container
		x={context.stateLayoutDerived.canvasSizes().width * 0.5}
		y={context.stateLayoutDerived.canvasSizes().height * 0.88}
	>
		{#if !context.stateApp.loaded}
			<LoadingProgress width={1967 * 0.2} height={346 * 0.2}>
				{#snippet background(sizes)}
					<Sprite key="progressBarBackground.png" {...sizes} />
				{/snippet}
				{#snippet progress(sizes)}
					<Sprite key="progressBar.png" {...sizes} />
				{/snippet}
				{#snippet frame(sizes)}
					<Sprite key="progressBarFrame.png" {...sizes} />
				{/snippet}
			</LoadingProgress>
		{/if}
	</Container>
</FadeContainer>
