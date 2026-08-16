<script lang="ts" module>
	import { SCENE_ART as SCENE_ART_SRC } from '../game/saloonLamps';

	export const SCENE_ART = SCENE_ART_SRC;
	export type EmitterEventSaloon = { type: 'saloonCheers' };
</script>

<script lang="ts">
	/**
	 * Live saloon room: plate + the LEFT hanging lamp. A click swaps the lit
	 * lantern for the unlit PNG until the next spin.
	 */
	import { onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';

	import { SALOON_LAMPS } from '../game/saloonLamps';
	import { saloonLamp } from '../game/saloonLamp.svelte';
	import { LAMP_GLOBE } from '../game/saloonLampSmash';
	import { getContext } from '../game/context';

	const context = getContext();

	const IDLE_PERIOD_MS = 4000;
	const IDLE_AMP_L = (4.4 * Math.PI) / 180;
	const CHEERS_MS = 2400;
	const DEG = Math.PI / 180;
	const CHEERS_L = [
		{ t: 0, deg: 0 },
		{ t: 0.55, deg: 6.2 },
		{ t: 1.3, deg: -4.8 },
		{ t: 2.4, deg: 0 },
	] as const;

	const L = SALOON_LAMPS.L;
	const FLAME = { x: LAMP_GLOBE.x, y: LAMP_GLOBE.y };

	const fit = $derived.by(() => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const scale = Math.max(canvas.width / SCENE_ART.width, canvas.height / SCENE_ART.height);
		return {
			x: canvas.width / 2,
			y: canvas.height / 2,
			scale: { x: scale, y: scale },
			pivot: { x: SCENE_ART.width / 2, y: SCENE_ART.height / 2 },
		};
	});

	const hasRoom = $derived(
		Boolean(context.stateApp.loadedAssets?.['saloonPlate']) &&
			Boolean(context.stateApp.loadedAssets?.['saloonLampL']),
	);

	let clip = $state<'idle' | 'cheers'>('idle');
	let clipOrigin = $state(performance.now());
	let rotL = $state(0);

	const sampleDeg = (keys: readonly { t: number; deg: number }[], sec: number) => {
		if (sec <= keys[0].t) return keys[0].deg;
		const last = keys[keys.length - 1];
		if (sec >= last.t) return last.deg;
		for (let i = 1; i < keys.length; i += 1) {
			if (sec <= keys[i].t) {
				const a = keys[i - 1];
				const b = keys[i];
				const u = (sec - a.t) / (b.t - a.t);
				const s = u * u * (3 - 2 * u);
				return a.deg + (b.deg - a.deg) * s;
			}
		}
		return 0;
	};

	$effect(() => {
		if (!context.stateXstateDerived.isIdle() && saloonLamp.smashed) {
			saloonLamp.smashed = false;
		}
	});

	context.eventEmitter.subscribeOnMount({
		saloonCheers: () => {
			if (saloonLamp.smashed) return;
			clip = 'cheers';
			clipOrigin = performance.now();
		},
	});

	onMount(() => {
		let raf = 0;
		const tick = (now: number) => {
			if (clip === 'cheers') {
				const elapsed = now - clipOrigin;
				if (elapsed >= CHEERS_MS) {
					clip = 'idle';
					clipOrigin = now;
					rotL = 0;
				} else {
					rotL = sampleDeg(CHEERS_L, elapsed / 1000) * DEG;
				}
			} else if (saloonLamp.smashed) {
				rotL = 0;
			} else {
				const phase = ((now - clipOrigin) / IDLE_PERIOD_MS) * Math.PI * 2;
				rotL = Math.sin(phase) * IDLE_AMP_L;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

</script>

<Container x={fit.x} y={fit.y} scale={fit.scale} pivot={fit.pivot}>
	{#if hasRoom}
		<Sprite
			key="saloonPlate"
			x={SCENE_ART.width / 2}
			y={SCENE_ART.height / 2}
			width={SCENE_ART.width}
			height={SCENE_ART.height}
			anchor={0.5}
		/>
		<Container x={L.x} y={L.y} rotation={rotL}>
			<Sprite
				key="saloonLampGlow"
				x={FLAME.x}
				y={FLAME.y + 80}
				anchor={0.5}
				width={980}
				height={1100}
				alpha={saloonLamp.smashed ? 0 : 0.38}
				blendMode="add"
				eventMode="none"
			/>
			<Sprite
				key="saloonLampL"
				x={-L.anchorX * L.width}
				y={-L.anchorY * L.height}
				width={L.width}
				height={L.height}
				anchor={0}
				alpha={saloonLamp.smashed ? 0 : 1}
			/>
			<Sprite
				key="saloonLampLSmashed"
				x={-L.anchorX * L.width}
				y={-L.anchorY * L.height}
				width={L.width}
				height={L.height}
				anchor={0}
				alpha={saloonLamp.smashed ? 1 : 0}
			/>
		</Container>
	{:else}
		<Sprite
			key="sceneBg"
			x={SCENE_ART.width / 2}
			y={SCENE_ART.height / 2}
			width={SCENE_ART.width}
			height={SCENE_ART.height}
			anchor={0.5}
		/>
	{/if}
</Container>
