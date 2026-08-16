<script lang="ts">
	/**
	 * One Kenney gunsmoke puff at the muzzle. Plays the dusty whitePuff flipbook
	 * once, drifting up and fading. Lives in WORLD space at the shot point.
	 * Parent removes it via `oncomplete`.
	 */
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut, quadIn } from 'svelte/easing';
	import { Container, SpriteSheet } from 'pixi-svelte';
	import { getContext } from '../game/context';

	const context = getContext();
	const ready = $derived(Boolean(context.stateApp.loadedAssets?.['muzzleSmoke']));

	let {
		x,
		y,
		size,
		oncomplete,
	}: { x: number; y: number; size: number; oncomplete?: () => void } = $props();

	const LIFE_MS = 620;
	const DRIFT = 36;
	const rise = new Tween(0);
	const fade = new Tween(1);

	onMount(() => {
		void rise.set(1, { duration: LIFE_MS, easing: cubicOut });
		void fade.set(0, { duration: LIFE_MS, easing: quadIn }).then(() => oncomplete?.());
	});

	const cy = $derived(y - DRIFT * rise.current);
	const dim = $derived(size * (0.55 + 0.9 * rise.current));
	const alpha = $derived(0.82 * fade.current);
</script>

{#if ready}
	<Container x={x} y={cy} eventMode="none" zIndex={9} alpha={alpha}>
		<SpriteSheet
			key="muzzleSmoke"
			anchor={0.5}
			width={dim}
			height={dim}
			animationSpeed={0.72}
			loop={false}
			play={true}
			eventMode="none"
		/>
	</Container>
{/if}
