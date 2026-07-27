<script lang="ts">
	import { Container, Sprite, ParticleEmitter } from 'pixi-svelte';
	import { FadeContainer, LoadingProgress } from 'components-pixi';

	import { getContext } from '../game/context';
	import IntroCarousel from './IntroCarousel.svelte';

	type Props = {
		onloaded: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	let loadingType = $state<'start' | 'transition'>('start');

	// Full-bleed padded-cell still (bg_base → loading.webp). Keep cover-fit in sync.
	const LOADING_ART = { width: 2560, height: 1440 };

	// THE WHITE ROOM: falling clinical debris (ceramic chips / pills / PATIENT 404
	// paper / lint / fluorescent dust / buckle scraps) — ZERO Madam glass shards.
	const LOADING_FALL = {
		alpha: { start: 0.9, end: 0.05 },
		scale: { start: 0.28, end: 0.42, minimumScaleMultiplier: 0.55 },
		color: { start: '#f4f1ec', end: '#8a8680' },
		speed: { start: 40, end: 120, minimumSpeedMultiplier: 0.7 },
		acceleration: { x: 0, y: 140 },
		maxSpeed: 0,
		startRotation: { min: 0, max: 360 },
		noRotation: false,
		rotationSpeed: { min: -80, max: 80 },
		lifetime: { min: 4.5, max: 7.5 },
		blendMode: 'normal',
		frequency: 0.12,
		emitterLifetime: -1,
		maxParticles: 48,
		pos: { x: 0, y: 0 },
		addAtBack: false,
		spawnType: 'rect',
		spawnRect: { x: -420, y: -40, w: 840, h: 20 },
	} as const;

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
	<!-- falling White Room debris across the loading painting -->
	{#if !context.stateApp.loaded}
		<Container
			x={context.stateLayoutDerived.canvasSizes().width * 0.5}
			y={context.stateLayoutDerived.canvasSizes().height * 0.08}
		>
			<ParticleEmitter config={LOADING_FALL} key="loadingParticles" emit />
		</Container>
	{/if}
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
