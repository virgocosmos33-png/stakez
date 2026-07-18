<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { stateShake } from '../game/stateShake.svelte';
	import { drawFlameBorder, type FlamePalette, type FlameSample } from '../game/flameDraw';

	const context = getContext();
	const POSITION_ADJUSTMENT = 1.01;

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
	const envelope = new Tween(0, { duration: 420, easing: cubicOut });
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
			heightMin: 7 * env,
			heightMax: 30 * env,
			lickScale: 2.5,
			lickEvery: 7,
			upBias: 0.5,
			inset: 5,
		});
	};
</script>

{#if glowActive}
	{@const bw = context.stateGameDerived.boardLayout().width}
	{@const bh = context.stateGameDerived.boardLayout().height}
	<MainContainer>
		<Container x={frameX} y={frameY}>
			<Graphics
				draw={(graphics) =>
					drawFrameFire(
						graphics,
						bw * 0.5 + SYMBOL_SIZE * 0.16,
						bh * 0.5 + SYMBOL_SIZE * 0.16,
						time,
						envelope.current,
					)}
			/>
		</Container>
	</MainContainer>
{/if}
