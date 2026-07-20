<script lang="ts">
	import { Container, Sprite } from 'pixi-svelte';
	import { FadeContainer, LoadingProgress } from 'components-pixi';

	import { getContext } from '../game/context';
	import IntroCarousel from './IntroCarousel.svelte';

	type Props = {
		onloaded: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	let loadingType = $state<'start' | 'transition'>('start');

	const LOADING_ART = { width: 1536, height: 1024 };

	// cover-fit the loading painting to the canvas, cropping the overflow
	const coverProps = () => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const scale = Math.max(canvas.width / LOADING_ART.width, canvas.height / LOADING_ART.height);
		return {
			anchor: 0.5,
			x: canvas.width / 2,
			y: canvas.height / 2,
			width: LOADING_ART.width * scale,
			height: LOADING_ART.height * scale,
		};
	};
</script>

<!-- loading art and progress -->
<FadeContainer show={loadingType === 'start'}>
	<Sprite key="mirrorLoading" {...coverProps()} />
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

<!-- feature walkthrough carousel, shown once everything is loaded -->
<!-- CONTINUE jumps straight to the game (the "enter the mirror" intro video is
     intentionally skipped) -->
<FadeContainer show={loadingType === 'start' && context.stateApp.loaded}>
	<IntroCarousel oncontinue={props.onloaded} />
</FadeContainer>
