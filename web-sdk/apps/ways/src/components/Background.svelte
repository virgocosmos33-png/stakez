<script lang="ts">
	import type { Texture, VideoSource } from 'pixi.js';
	import { Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { SECOND } from 'constants-shared/time';

	import { getContext } from '../game/context';

	const context = getContext();

	// Every room is an ambient video loop rendered from the painting itself
	// (tools/build_bg_video.py): candle flicker, crystal-ball pulses and dust
	// motes are baked at exact painting coordinates, so they ride the same
	// cover-fit transform as the artwork and stay glued to their candles at
	// any window size. The static painting only shows until the video is up.
	const LANDSCAPE_ART = { width: 1536, height: 1024 };
	const PORTRAIT_ART = { width: 1024, height: 1536 };
	const FREESPIN_VIDEO_ART = { width: 1176, height: 780 };

	const videoTextureOf = (key: string) =>
		context.stateApp.loadedAssets?.[key] as Texture | undefined;

	// keep every ambient loop looping and playing (autoplay can be interrupted
	// by the browser; mp4 loops are seamless by construction)
	$effect(() => {
		for (const key of ['mirrorBgBaseAnim', 'mirrorBgBaseAnimPortrait', 'mirrorBgFreespinAnim']) {
			const source = videoTextureOf(key)?.source as VideoSource | undefined;
			const video = source?.resource as HTMLVideoElement | undefined;
			if (video) {
				video.loop = true;
				video.muted = true;
				if (video.paused) video.play().catch(() => {});
			}
		}
	});

	// cover-fit the artwork to the canvas, cropping the overflow
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

	const isPortrait = $derived(context.stateLayoutDerived.layoutType() === 'portrait');
	const baseVideoKey = $derived(isPortrait ? 'mirrorBgBaseAnimPortrait' : 'mirrorBgBaseAnim');
	const baseStaticKey = $derived(isPortrait ? 'mirrorBgBasePortrait' : 'mirrorBgBase');
	const baseArt = $derived(isPortrait ? PORTRAIT_ART : LANDSCAPE_ART);
	const baseVideoReady = $derived(videoTextureOf(baseVideoKey) !== undefined);
	const freespinVideoReady = $derived(videoTextureOf('mirrorBgFreespinAnim') !== undefined);

	const showBaseBackground = $derived(context.stateGame.gameType === 'basegame');
	const showFeatureBackground = $derived(context.stateGame.gameType === 'freegame');
</script>

<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />

<FadeContainer show={showBaseBackground} duration={SECOND} zIndex={-2}>
	{#if baseVideoReady}
		<Sprite key={baseVideoKey} {...coverProps(baseArt)} />
	{:else}
		<Sprite key={baseStaticKey} {...coverProps(baseArt)} />
	{/if}
</FadeContainer>

<FadeContainer show={showFeatureBackground} duration={SECOND} zIndex={-1}>
	{#if freespinVideoReady}
		<Sprite key="mirrorBgFreespinAnim" {...coverProps(FREESPIN_VIDEO_ART)} />
	{:else}
		<Sprite key="mirrorBgFreespin" {...coverProps(LANDSCAPE_ART)} />
	{/if}
</FadeContainer>
