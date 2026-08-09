<script lang="ts">
	import type { Texture, VideoSource } from 'pixi.js';
	import { Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { SECOND } from 'constants-shared/time';

	import { getContext } from '../game/context';

	const context = getContext();

	// ONE ambient SCENE (candle flames, crystal-ball glow, veiled mirror, green
	// lamp + drifting fog are all baked INTO the artwork) cover-scaled to the
	// viewport as a single unit. Because the whole scene rides one cover-fit
	// transform, the ambience can never drift / misalign on resize the way the
	// old coordinate-pinned FX layers did. The reel grid + frame sit over the
	// dark centre and stay unobstructed at every aspect ratio.
	//
	// SOURCE-AGNOSTIC SWAP POINT: this layer renders a still today. Drop a
	// seamless loop at static/assets/sprites/scene/scene_bg.mp4 and register it
	// as `sceneBgAnim` in assets.ts — the layer switches to the video texture
	// automatically (the still stays as the poster / fallback), no structural
	// change. Same pattern as the free-spin room below.
	const SCENE_ART = { width: 1536, height: 1024 };
	const FREESPIN_ART = { width: 1176, height: 780 };
	const FREESPIN_STATIC_ART = { width: 1536, height: 1024 };

	const videoTextureOf = (key: string) =>
		context.stateApp.loadedAssets?.[key] as Texture | undefined;

	// keep every ambient loop looping + playing (browser autoplay can pause it;
	// mp4/webm loops are seamless by construction from the ffmpeg step)
	$effect(() => {
		for (const key of ['sceneBgAnim', 'mirrorBgFreespinAnim']) {
			const source = videoTextureOf(key)?.source as VideoSource | undefined;
			const video = source?.resource as HTMLVideoElement | undefined;
			if (video) {
				video.loop = true;
				video.muted = true;
				if (video.paused) video.play().catch(() => {});
			}
		}
	});

	// cover-fit the artwork to the canvas, cropping the overflow. ONE transform
	// for the whole scene => nothing inside it can drift relative to anything else.
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
	const freespinVideoReady = $derived(videoTextureOf('mirrorBgFreespinAnim') !== undefined);

	const showBaseBackground = $derived(context.stateGame.gameType === 'basegame');
	const showFeatureBackground = $derived(context.stateGame.gameType === 'freegame');
</script>

<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />

<!-- idle / base game: the single Lady-Mirror séance scene -->
<FadeContainer show={showBaseBackground} duration={SECOND} zIndex={-2}>
	{#if sceneVideoReady}
		<Sprite key="sceneBgAnim" {...coverProps(SCENE_ART)} />
	{:else}
		<Sprite key="sceneBg" {...coverProps(SCENE_ART)} />
	{/if}
</FadeContainer>

<!-- free-spin room (unchanged gameplay state) -->
<FadeContainer show={showFeatureBackground} duration={SECOND} zIndex={-1}>
	{#if freespinVideoReady}
		<Sprite key="mirrorBgFreespinAnim" {...coverProps(FREESPIN_ART)} />
	{:else}
		<Sprite key="mirrorBgFreespin" {...coverProps(FREESPIN_STATIC_ART)} />
	{/if}
</FadeContainer>
