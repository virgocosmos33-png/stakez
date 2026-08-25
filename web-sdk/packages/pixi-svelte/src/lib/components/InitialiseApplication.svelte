<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { onMount, onDestroy, type Snippet } from 'svelte';
	import { devicePixelRatio } from 'svelte/reactivity/window';

	import { getContextApp } from '../context.svelte';
	import { preloadFont } from '../utils.svelte';

	type Props = { children: Snippet };

	const props: Props = $props();
	const context = getContextApp();

	let wrap: HTMLDivElement;
	let initialised = $state(false);

	const initialiseApplication = async () => {
		// Game art is authored ABOVE display size (board frame ~1.4x, symbol
		// cards ~1.5x) so sprites are always minified. Plain bilinear
		// minification undersamples — it blends only 4 texels per output pixel
		// regardless of how much detail is being squeezed — which reads as
		// pixelated/crunchy edges on the timber frame and symbol linework.
		// Mipmaps give proper trilinear minification (what commercial slots
		// ship). Must be set before Assets.load creates any TextureSource.
		PIXI.TextureSource.defaultOptions.autoGenerateMipmaps = true;
		// …but NOT for filter/effect render textures: those re-render every
		// frame and pixi never regenerates their mip chain, so keep the pool
		// on plain level-0 sampling (also what pixi's docs recommend).
		PIXI.TexturePool.textureOptions.autoGenerateMipmaps = false;
		PIXI.TexturePool.textureOptions.mipLevelCount = 1;
		// Anisotropic filtering: extra probes when a texture is scaled, sharper
		// result than plain (tri)linear at no meaningful GPU cost on 2D scenes.
		PIXI.TextureStyle.defaultOptions.maxAnisotropy = 16;

		PIXI.Assets.reset();

		await preloadFont();
		// Keep the Application on a local so App.svelte's onMount reset() cannot
		// null context.stateApp.pixiApplication mid-init and leave Storybook on
		// a black "Initialising..." canvas.
		const app = new PIXI.Application<PIXI.Renderer<HTMLCanvasElement>>();
		await app.init({
			autoDensity: true,
			backgroundAlpha: 0,
			hello: true,
			multiView: false,
			antialias: true,
			clearBeforeRender: true,
			// WebGL, not WebGPU: Pixi v8's WebGPU backend on Windows/Chrome hits a
			// depth-stencil vs colour attachment size-rounding mismatch (e.g.
			// 1621 vs 1620px) at fractional devicePixelRatios, which invalidates
			// the command buffer every frame and leaves the canvas blank. WebGL is
			// the stable, universally-supported path for the game.
			preference: 'webgl',
			powerPreference: 'high-performance',
			// Supersample low-DPI displays: on Windows desktops dPR is often
			// 1–1.5, which forces game art (authored ~1.5–2x display size) deep
			// into minification where trilinear mips look mushy and raw
			// bilinear looks crunchy. Rendering the backing store at >=2x puts
			// texture sampling near 1:1 (crisp), and the browser compositor
			// downscales the canvas to CSS size with high quality — the same
			// thing a genuine 2x hidpi screen does. True hidpi phones
			// (dPR 2–3) keep their native ratio.
			resolution: Math.min(Math.max(devicePixelRatio.current ?? 1, 2), 3),
			resizeTo: window,
		});

		wrap.appendChild(app.canvas);

		// to prevent that you can't scroll the page with touch on the canvas. https://github.com/pixijs/pixijs/issues/4824
		app.renderer.events.autoPreventDefault = false;
		app.renderer.canvas.style.touchAction = 'auto';
		context.stateApp.pixiApplication = app;
	};

	onMount(async () => {
		try {
			if (!initialised) await initialiseApplication();
			initialised = true;
		} catch (error) {
			console.error(error);
		}
	});

	onDestroy(() => {
		if (context.stateApp.pixiApplication) {
			context.stateApp.pixiApplication.destroy();
		}
	});
</script>

<div bind:this={wrap}>
	{#if initialised}
		{@render props.children()}
	{/if}
</div>
