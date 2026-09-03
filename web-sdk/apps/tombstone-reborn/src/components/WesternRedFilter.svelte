<script lang="ts">
	/**
	 * Spine red_filter slot. Same as backgroundSPINE/scene-viewer.html:
	 * keep the attachment, set alpha to Base 45% / Bonus 80%.
	 */
	import { onMount } from 'svelte';
	import { getContextSpine } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { isBonusAtmosphere } from '../game/atmosphere.svelte';
	import { WESTERN_RED_FILTER } from '../game/westernScene';

	const context = getContext();
	const spine = getContextSpine();
	const amount = $derived(
		isBonusAtmosphere(context.stateGame.atmosphere)
			? WESTERN_RED_FILTER.bonusOpacity
			: WESTERN_RED_FILTER.baseOpacity,
	);

	const apply = () => {
		const slot = spine.skeleton.findSlot('red_filter');
		if (!slot) return;
		slot.color.a = amount;
	};

	$effect(() => {
		void amount;
		apply();
	});

	onMount(() => {
		const prev = spine.beforeUpdateWorldTransforms;
		spine.beforeUpdateWorldTransforms = () => {
			prev?.();
			apply();
		};
		return () => {
			spine.beforeUpdateWorldTransforms = prev;
		};
	});
</script>
