<script lang="ts">
	import { Container, Sprite, ParticleEmitter } from 'pixi-svelte';
	import { FadeContainer, LoadingProgress } from 'components-pixi';

	import { getContext } from '../game/context';

	type Props = {
		onloaded: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// Full-bleed graveyard still. Keep cover-fit in sync with scene art.
	const LOADING_ART = { width: 1920, height: 1088 };

	// Dust / embers over the loading painting — no White Room clinical debris.
	const LOADING_FALL = {
		alpha: { start: 0.7, end: 0.05 },
		scale: { start: 0.2, end: 0.35, minimumScaleMultiplier: 0.55 },
		color: { start: '#c9a45c', end: '#3a2a18' },
		speed: { start: 30, end: 90, minimumSpeedMultiplier: 0.7 },
		acceleration: { x: 0, y: 110 },
		maxSpeed: 0,
		startRotation: { min: 0, max: 360 },
		noRotation: false,
		rotationSpeed: { min: -60, max: 60 },
		lifetime: { min: 4, max: 7 },
		blendMode: 'normal',
		frequency: 0.14,
		emitterLifetime: -1,
		maxParticles: 36,
		pos: { x: 0, y: 0 },
		addAtBack: false,
		spawnType: 'rect',
		spawnRect: { x: -420, y: -40, w: 840, h: 20 },
	} as const;

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
	<Sprite key="sceneBg" {...coverProps()} />
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
