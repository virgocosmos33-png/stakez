<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { stateShake } from '../game/stateShake.svelte';
	import { fxNum } from '../game/fx.generated';
	import { drawFlameBorder, type FlamePalette, type FlameSample } from '../game/flameDraw';

	const context = getContext();
	const POSITION_ADJUSTMENT = 1.01;

	// parametric FX (panel-editable via game-builder config → fx.framePlasma)
	const ENVELOPE_MS = fxNum('framePlasma', 'envelopeMs', 420);
	const FLAME_HEIGHT_MIN = fxNum('framePlasma', 'flameHeightMin', 7);
	const FLAME_HEIGHT_MAX = fxNum('framePlasma', 'flameHeightMax', 30);
	const LICK_SCALE = fxNum('framePlasma', 'lickScale', 2.5);
	const LICK_EVERY = fxNum('framePlasma', 'lickEvery', 7);
	const UP_BIAS = fxNum('framePlasma', 'upBias', 0.5);
	const INSET = fxNum('framePlasma', 'inset', 5);
	const MARGIN_SCALE = fxNum('framePlasma', 'marginScale', 0.16);

	const frameX = $derived(
		context.stateGameDerived.boardLayout().x * POSITION_ADJUSTMENT + stateShake.x,
	);
	const frameY = $derived(
		context.stateGameDerived.boardLayout().y * POSITION_ADJUSTMENT + stateShake.y,
	);

	// purple mirror-fire ramp: deep violet body -> lavender -> white-hot base
	const FIRE: FlamePalette = {
		body: 0x6d3fd6,
		mid: 0xa678f5,
		hot: 0xd0aeff,
		core: 0xf3ecff,
	};

	// A living ring of purple FLAME licking off the board-frame perimeter
	// (ragged flame bands via flameDraw.ts - no neon tube, no dot motes).
	// Ignites on free-spin start, dies on exit, drawn ABOVE the reels.
	const envelope = new Tween(0, { duration: ENVELOPE_MS, easing: cubicOut });
	let glowActive = $state(false);
	let time = $state(0);

	context.eventEmitter.subscribeOnMount({
		boardFrameGlowShow: () => {
			glowActive = true;
			envelope.set(1);
		},
		boardFrameGlowHide: async () => {
			await envelope.set(0);
			glowActive = false;
		},
	});

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

	// a point + outward normal at fraction f (0..1) around a sharp W x H rect
	const perimeterPoint = (f: number, hw: number, hh: number): [number, number, number, number] => {
		const w = hw * 2;
		const h = hh * 2;
		const perim = 2 * (w + h);
		let d = f * perim;
		if (d < w) return [-hw + d, -hh, 0, -1]; // top
		d -= w;
		if (d < h) return [hw, -hh + d, 1, 0]; // right
		d -= h;
		if (d < w) return [hw - d, hh, 0, 1]; // bottom
		d -= h;
		return [-hw, hh - d, -1, 0]; // left
	};

	const drawFrameFire = (
		graphics: import('pixi.js').Graphics,
		hw: number,
		hh: number,
		timeValue: number,
		env: number,
	) => {
		if (env <= 0.005) return;
		const perim = 4 * (hw + hh);
		const count = Math.max(80, Math.round(perim / 11));
		const samples: FlameSample[] = [];
		for (let k = 0; k < count; k++) {
			const [x, y, nx, ny] = perimeterPoint(k / count, hw, hh);
			samples.push({ x, y, nx, ny });
		}
		// the whole border IS fire: ragged licking bands, taller on top,
		// envelope scales the flame reach so it grows in / dies down
		drawFlameBorder(graphics, samples, FIRE, {
			seed: 7.3,
			time: timeValue,
			alpha: env,
			heightMin: FLAME_HEIGHT_MIN * env,
			heightMax: FLAME_HEIGHT_MAX * env,
			lickScale: LICK_SCALE,
			lickEvery: LICK_EVERY,
			upBias: UP_BIAS,
			inset: INSET,
		});
	};
</script>

<!-- MainContainer is ALWAYS mounted (only the flame Graphics is conditional) so
	this layer keeps its z-order slot below the WIN/WAYS plaques. Wrapping the
	MainContainer itself in {#if} made it mount LATE on free-spin start, which
	appended it on top of the gameplay readouts (stable-sort late-mount bug). -->
<MainContainer>
	{#if glowActive}
		{@const bw = context.stateGameDerived.boardLayout().width}
		{@const bh = context.stateGameDerived.boardLayout().height}
		<Container x={frameX} y={frameY}>
			<Graphics
				draw={(graphics) =>
					drawFrameFire(
						graphics,
						bw * 0.5 + SYMBOL_SIZE * MARGIN_SCALE,
						bh * 0.5 + SYMBOL_SIZE * MARGIN_SCALE,
						time,
						envelope.current,
					)}
			/>
		</Container>
	{/if}
</MainContainer>
