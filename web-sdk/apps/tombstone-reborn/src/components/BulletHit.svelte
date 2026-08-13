<script lang="ts">
	/**
	 * One shattered-glass bullet hole. Snaps in with a quick scale pop then holds
	 * (it lives until the board leaves idle — the parent clears the whole set on
	 * spin). `size` is the target width/height in board design px.
	 */
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { Sprite } from 'pixi-svelte';

	let {
		x,
		y,
		size,
		rotation = 0,
		spriteKey,
	}: { x: number; y: number; size: number; rotation?: number; spriteKey: string } = $props();

	const POP_MS = 150;
	const pop = new Tween(0, { duration: POP_MS, easing: backOut });

	onMount(() => {
		pop.set(1);
	});

	// impact snap: overshoot slightly bigger, settle to `size`
	const dim = $derived(size * (0.55 + 0.45 * pop.current));
	const alpha = $derived(0.35 + 0.65 * pop.current);
</script>

<Sprite key={spriteKey} {x} {y} {rotation} anchor={0.5} width={dim} height={dim} {alpha} />
