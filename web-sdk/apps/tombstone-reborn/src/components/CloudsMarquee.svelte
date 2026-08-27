<script lang="ts">
	/**
	 * Slides the existing Spine cloud slots (PSD "clouds marquee") right → left.
	 * Draw order stays Layer_12 → clouds → Layer_11. Idle does not translate.
	 */
	import { onMount } from 'svelte';
	import { getContextSpine } from 'pixi-svelte';

	import { WESTERN_CLOUD_MARQUEE as CLOUD } from '../game/westernScene';

	type CloudAttach = { x: number; updateOffset?: () => void };

	const spine = getContextSpine();
	let offset = 0;

	const place = () => {
		const shift = ((offset % CLOUD.artW) + CLOUD.artW) % CLOUD.artW;
		for (let i = 0; i < CLOUD.slots.length; i += 1) {
			const slot = spine.skeleton.findSlot(CLOUD.slots[i]);
			const att = slot?.attachment as CloudAttach | null;
			if (!att) continue;
			att.x = CLOUD.homeX + i * CLOUD.artW - shift;
			att.updateOffset?.();
		}
	};

	onMount(() => {
		let last = performance.now();
		const prev = spine.beforeUpdateWorldTransforms;
		spine.beforeUpdateWorldTransforms = () => {
			prev?.();
			const now = performance.now();
			offset += CLOUD.speed * Math.min(0.033, (now - last) / 1000);
			last = now;
			place();
		};
		return () => {
			spine.beforeUpdateWorldTransforms = prev;
		};
	});
</script>
