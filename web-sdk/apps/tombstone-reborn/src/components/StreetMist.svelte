<script lang="ts">
	/**
	 * Low bone-white street mist. Sibling above the plate, below Spine lamps.
	 * Locked to SCENE_ART so cover-fit matches SaloonScene / lamps.
	 */
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { linear } from 'svelte/easing';
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SCENE_ART } from '../game/saloonLamps';

	const context = getContext();
	const ready = $derived(Boolean(context.stateApp.loadedAssets?.['streetMist']));

	const MIST_H = SCENE_ART.height * 0.4;
	const MIST_W = SCENE_ART.width * 1.12;
	const DRIFT = 36;
	const drift = new Tween(0);

	onMount(() => {
		let live = true;
		const loop = async () => {
			while (live) {
				await drift.set(DRIFT, { duration: 14000, easing: linear });
				if (!live) return;
				await drift.set(0, { duration: 14000, easing: linear });
			}
		};
		void loop();
		return () => {
			live = false;
		};
	});

	const shift = $derived(drift.current - DRIFT / 2);
</script>

{#if ready}
	<Container zIndex={1} eventMode="none">
		<Sprite
			key="streetMist"
			x={SCENE_ART.width / 2 + shift}
			y={SCENE_ART.height}
			width={MIST_W}
			height={MIST_H}
			anchor={{ x: 0.5, y: 1 }}
			alpha={0.32}
			tint={0xf3ece2}
		/>
		<Sprite
			key="streetMist"
			x={SCENE_ART.width / 2 + shift + DRIFT}
			y={SCENE_ART.height}
			width={MIST_W}
			height={MIST_H}
			anchor={{ x: 0.5, y: 1 }}
			alpha={0.18}
			tint={0xefe6d8}
		/>
	</Container>
{/if}
