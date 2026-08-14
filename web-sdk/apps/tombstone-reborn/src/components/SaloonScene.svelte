<script lang="ts" module>
	import { SCENE_ART as SCENE_ART_SRC } from '../game/saloonLamps';

	export const SCENE_ART = SCENE_ART_SRC;
	export type EmitterEventSaloon = { type: 'saloonCheers' };
</script>

<script lang="ts">
	/**
	 * Live saloon room: plate + the FULL lady-spine lamp layers (not a
	 * silhouette crop) cover-fitted as ONE unit. Swing from the chain mount.
	 *
	 * idle = slow sway. A multiplier detonation plays cheers (the shake)
	 * once, then returns to idle.
	 */
	import { onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';

	import { SALOON_LAMPS } from '../game/saloonLamps';
	import { getContext } from '../game/context';

	const context = getContext();

	const IDLE_PERIOD_MS = 4000;
	const IDLE_AMP_L = (4.4 * Math.PI) / 180;
	const IDLE_AMP_R = (3.6 * Math.PI) / 180;
	const CHEERS_MS = 2400;
	const DEG = Math.PI / 180;
	const CHEERS_L = [
		{ t: 0, deg: 0 },
		{ t: 0.55, deg: 6.2 },
		{ t: 1.3, deg: -4.8 },
		{ t: 2.4, deg: 0 },
	] as const;
	const CHEERS_R = [
		{ t: 0, deg: 0 },
		{ t: 0.4, deg: -5.4 },
		{ t: 1.15, deg: 4.6 },
		{ t: 2.4, deg: 0 },
	] as const;

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
			Boolean(context.stateApp.loadedAssets?.['saloonLampL']) &&
			Boolean(context.stateApp.loadedAssets?.['saloonLampR']),
	);

	let clip = $state<'idle' | 'cheers'>('idle');
	let clipOrigin = $state(performance.now());
	let rotL = $state(0);
	let rotR = $state(0);

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

	context.eventEmitter.subscribeOnMount({
		saloonCheers: () => {
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
					rotR = 0;
				} else {
					const sec = elapsed / 1000;
					rotL = sampleDeg(CHEERS_L, sec) * DEG;
					rotR = sampleDeg(CHEERS_R, sec) * DEG;
				}
			} else {
				const phase = ((now - clipOrigin) / IDLE_PERIOD_MS) * Math.PI * 2;
				rotL = Math.sin(phase) * IDLE_AMP_L;
				rotR = -Math.sin(phase) * IDLE_AMP_R;
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
		<Sprite
			key="saloonLampL"
			x={SALOON_LAMPS.L.x}
			y={SALOON_LAMPS.L.y}
			width={SALOON_LAMPS.L.width}
			height={SALOON_LAMPS.L.height}
			anchor={{ x: SALOON_LAMPS.L.anchorX, y: SALOON_LAMPS.L.anchorY }}
			rotation={rotL}
		/>
		<Sprite
			key="saloonLampR"
			x={SALOON_LAMPS.R.x}
			y={SALOON_LAMPS.R.y}
			width={SALOON_LAMPS.R.width}
			height={SALOON_LAMPS.R.height}
			anchor={{ x: SALOON_LAMPS.R.anchorX, y: SALOON_LAMPS.R.anchorY }}
			rotation={rotR}
		/>
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
