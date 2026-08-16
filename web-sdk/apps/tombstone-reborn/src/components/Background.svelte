<script lang="ts">
	import type { Texture, VideoSource } from 'pixi.js';
	import { Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { SECOND } from 'constants-shared/time';

	import { getContext } from '../game/context';
	import SaloonScene, { SCENE_ART } from './SaloonScene.svelte';

	const context = getContext();

	// ONE ambient SCENE. Base and bonus both use the saloon — this game has no
	// White Room free-spin painting. Drop a seamless loop at
	// static/assets/sprites/scene/scene_bg.mp4 and register it as `sceneBgAnim`
	// to replace the still room with video.
	const videoTextureOf = (key: string) =>
		context.stateApp.loadedAssets?.[key] as Texture | undefined;

	$effect(() => {
		const source = videoTextureOf('sceneBgAnim')?.source as VideoSource | undefined;
		const video = source?.resource as HTMLVideoElement | undefined;
		if (video) {
			video.loop = true;
			video.muted = true;
			if (video.paused) video.play().catch(() => {});
		}
	});

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
</script>

<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />

<FadeContainer show={true} duration={SECOND} zIndex={-2}>
	{#if sceneVideoReady}
		<Sprite key="sceneBgAnim" {...coverProps(SCENE_ART)} />
	{:else}
		<SaloonScene />
	{/if}
</FadeContainer>
