<script lang="ts">
	import { type Texture, type VideoSource } from 'pixi.js';
	import { Rectangle } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { SECOND } from 'constants-shared/time';

	import { getContext } from '../game/context';
	import SaloonScene from './SaloonScene.svelte';

	const context = getContext();

	// Ready backgroundSPINE western room. Color, red_filter, smoke, and fire
	// all live on that scene. Do not grade it to grey.
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

	$effect(() => {
		playLoop('sceneBgAnim');
	});
</script>

<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />

<FadeContainer show={true} duration={SECOND} zIndex={-2}>
	<SaloonScene />
</FadeContainer>
