<script lang="ts">
	import { onMount } from 'svelte';
	import type { Texture, VideoSource } from 'pixi.js';
	import { Graphics, Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer } from 'components-pixi';
	import { SECOND } from 'constants-shared/time';

	import { getContext } from '../game/context';

	const context = getContext();

	const LANDSCAPE_ART = { width: 1536, height: 1024 };
	const PORTRAIT_ART = { width: 1024, height: 1536 };
	const VIDEO_ART = { width: 1176, height: 780 };

	// candle flames live at normalized (u, v) points in the artwork; they run
	// through the same cover-fit transform as the background sprite, so they
	// stay glued to their candles at any window size
	type Flame = { u: number; v: number; size: number; palette: 'violet' | 'green' | 'amber' };
	const LANDSCAPE_FLAMES: Flame[] = [
		{ u: 0.095, v: 0.528, size: 1.1, palette: 'violet' },
		{ u: 0.075, v: 0.573, size: 0.85, palette: 'violet' },
		{ u: 0.118, v: 0.571, size: 0.8, palette: 'violet' },
		{ u: 0.048, v: 0.628, size: 0.65, palette: 'violet' },
		{ u: 0.066, v: 0.657, size: 0.4, palette: 'violet' },
		{ u: 0.934, v: 0.612, size: 1.05, palette: 'green' },
	];
	const PORTRAIT_FLAMES: Flame[] = [
		{ u: 0.385, v: 0.048, size: 0.9, palette: 'amber' },
		{ u: 0.605, v: 0.042, size: 0.9, palette: 'amber' },
		{ u: 0.06, v: 0.74, size: 0.8, palette: 'green' },
		{ u: 0.105, v: 0.755, size: 0.65, palette: 'green' },
		{ u: 0.705, v: 0.752, size: 0.7, palette: 'green' },
		{ u: 0.945, v: 0.8, size: 0.85, palette: 'green' },
	];
	const PALETTES = {
		violet: { glow: 0xb887ff, body: 0xd9b3ff, core: 0xffffff },
		green: { glow: 0x2bff66, body: 0x8dffab, core: 0xeafff0 },
		amber: { glow: 0xffb347, body: 0xffd27a, core: 0xfff3d6 },
	};

	let time = $state(0);
	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const drawFlames = (
		graphics: import('pixi.js').Graphics,
		flames: Flame[],
		art: { width: number; height: number },
		timeValue: number,
	) => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const scale = Math.max(canvas.width / art.width, canvas.height / art.height);

		flames.forEach((flame, index) => {
			const x = canvas.width / 2 + (flame.u - 0.5) * art.width * scale;
			const y = canvas.height / 2 + (flame.v - 0.5) * art.height * scale;
			const palette = PALETTES[flame.palette];
			const base = 9 * flame.size * scale;

			// organic flicker: layered sines + per-chunk noise, unique per flame
			const flickerNoise = rand(Math.floor(timeValue * 16) * 7 + index * 31);
			const breath =
				0.75 +
				0.2 * Math.sin(timeValue * 6.3 + index * 2.4) +
				0.12 * Math.sin(timeValue * 11.7 + index * 5.1) +
				0.18 * flickerNoise;
			const sway =
				Math.sin(timeValue * 3.1 + index * 1.9) * 1.6 +
				Math.sin(timeValue * 7.7 + index * 4.2) * 0.8;
			const stretch = 1 + 0.25 * Math.sin(timeValue * 9.2 + index * 3.3) + 0.2 * flickerNoise;

			// soft halo breathing on the wall
			graphics.circle(x, y, base * 3.2 * breath);
			graphics.fill({ color: palette.glow, alpha: 0.07 + 0.05 * breath });
			graphics.circle(x, y, base * 1.9 * breath);
			graphics.fill({ color: palette.glow, alpha: 0.1 + 0.07 * breath });

			// flame body: teardrop leaning with the sway
			graphics.ellipse(x + sway * scale * 0.6, y, base * 0.55 * breath, base * stretch);
			graphics.fill({ color: palette.glow, alpha: 0.5 });
			graphics.ellipse(
				x + sway * scale * 0.75,
				y - base * stretch * 0.18,
				base * 0.34 * breath,
				base * stretch * 0.66,
			);
			graphics.fill({ color: palette.body, alpha: 0.75 });

			// hot core
			graphics.ellipse(
				x + sway * scale * 0.85,
				y - base * stretch * 0.05,
				base * 0.16,
				base * stretch * 0.34,
			);
			graphics.fill({ color: palette.core, alpha: 0.95 });
		});
	};

	// the free-spin room is an ambient video loop; make sure it loops and
	// keeps playing (the mp4 is a ping-pong loop so the seam is invisible)
	const videoTexture = $derived(
		context.stateApp.loadedAssets?.mirrorBgFreespinAnim as Texture | undefined,
	);
	$effect(() => {
		const source = videoTexture?.source as VideoSource | undefined;
		const video = source?.resource as HTMLVideoElement | undefined;
		if (video) {
			video.loop = true;
			video.muted = true;
			if (video.paused) video.play().catch(() => {});
		}
	});

	// cover-fit the painting to the canvas, cropping the overflow
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
	const baseKey = $derived(isPortrait ? 'mirrorBgBasePortrait' : 'mirrorBgBase');
	const baseArt = $derived(isPortrait ? PORTRAIT_ART : LANDSCAPE_ART);
	const showBaseBackground = $derived(context.stateGame.gameType === 'basegame');
	const showFeatureBackground = $derived(context.stateGame.gameType === 'freegame');
</script>

<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />

<FadeContainer show={showBaseBackground} duration={SECOND} zIndex={-2}>
	<Sprite key={baseKey} {...coverProps(baseArt)} />
	<Graphics
		draw={(graphics) =>
			drawFlames(graphics, isPortrait ? PORTRAIT_FLAMES : LANDSCAPE_FLAMES, baseArt, time)}
	/>
</FadeContainer>

<FadeContainer show={showFeatureBackground} duration={SECOND} zIndex={-1}>
	{#if videoTexture}
		<Sprite key="mirrorBgFreespinAnim" {...coverProps(VIDEO_ART)} />
	{:else}
		<Sprite key="mirrorBgFreespin" {...coverProps(LANDSCAPE_ART)} />
	{/if}
</FadeContainer>
