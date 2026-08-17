<script lang="ts">
	import { type Texture, type VideoSource } from 'pixi.js';
	import { Container, Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { SECOND } from 'constants-shared/time';

	import { getContext } from '../game/context';
	import SaloonScene, { BG_PLATE_FILTERS, SCENE_ART, tickBgGrade } from './SaloonScene.svelte';
	import AtmosphereFx from './AtmosphereFx.svelte';
	import SeamlessVideoLoop from './SeamlessVideoLoop.svelte';

	const context = getContext();

	// ONE ambient SCENE. Base and bonus both use the saloon — this game has no
	// White Room free-spin painting. Drop a seamless loop at
	// static/assets/sprites/scene/scene_bg.mp4 and register it as `sceneBgAnim`
	// to replace the still room with video.
	const videoTextureOf = (key: string) =>
		context.stateApp.loadedAssets?.[key] as Texture | undefined;

	const playLoop = (key: string) => {
		const source = videoTextureOf(key)?.source as VideoSource | undefined;
		const video = source?.resource as HTMLVideoElement | undefined;
		if (!video) return;
		video.loop = true;
		video.muted = true;
		if (video.paused) video.play().catch(() => {});
	};

	const coverProps = (art: { width: number; height: number }) => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const scale = Math.max(canvas.width / art.width, canvas.height / art.height);
		return {
			anchor: 0.5,
			x: canvas.width / 2,
			y: canvas.height / 2,
			width: art.width * scale,
			height: art.height * scale,
		};
	};

	const sceneVideoReady = $derived(videoTextureOf('sceneBgAnim') !== undefined);
	const atmosphere = $derived(context.stateGame.atmosphere);
	const emberReady = $derived(videoTextureOf('emberRise') !== undefined);
	const smokeReady = $derived(videoTextureOf('roomSmoke') !== undefined);
	const FX_ART = { width: 1280, height: 720 };

	$effect(() => {
		playLoop('sceneBgAnim');
	});

	$effect(() => {
		if (atmosphere !== 'super') return;
		playLoop('emberRise');
	});

	// Snap grade to the atmosphere target. Do not tick uTime every frame —
	// that used to keep the full-screen blur stack dirty for no visual gain.
	$effect(() => {
		const sat = atmosphere === 'base' ? 0 : 1;
		tickBgGrade(0, sat, 0, 0);
	});
</script>

<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />

<FadeContainer show={true} duration={SECOND} zIndex={-2}>
	{#if sceneVideoReady}
		<Container filters={BG_PLATE_FILTERS}>
			<Sprite key="sceneBgAnim" {...coverProps(SCENE_ART)} />
		</Container>
	{:else}
		<SaloonScene />
	{/if}
	<AtmosphereFx />
	{#if atmosphere === 'super' && smokeReady}
		<SeamlessVideoLoop assetKey="roomSmoke" {...coverProps(FX_ART)} alpha={0.62} zIndex={0} />
	{/if}
	{#if atmosphere === 'super' && emberReady}
		<Sprite
			key="emberRise"
			{...coverProps(FX_ART)}
			blendMode="add"
			alpha={0.82}
			zIndex={1}
		/>
	{/if}
</FadeContainer>
