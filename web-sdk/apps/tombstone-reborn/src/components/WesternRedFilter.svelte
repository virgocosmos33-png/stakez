<script lang="ts">
	/**
	 * Ready TR2 red_filter.png. Spine slot blend is multiply.
	 * Base 45% / bonus 80% from red_filter.json. PNG stays full strength.
	 */
	import { onMount } from 'svelte';
	import { Sprite, type Texture } from 'pixi.js';
	import { getContextParent } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { isBonusAtmosphere } from '../game/atmosphere.svelte';
	import { SCENE_ART } from '../game/saloonLamps';
	import { WESTERN_RED_FILTER } from '../game/westernScene';

	const context = getContext();
	const parent = getContextParent();
	const amount = $derived(
		isBonusAtmosphere(context.stateGame.atmosphere)
			? WESTERN_RED_FILTER.bonusOpacity
			: WESTERN_RED_FILTER.baseOpacity,
	);

	const sprite = new Sprite();
	sprite.eventMode = 'none';
	sprite.zIndex = 0.25;
	sprite.blendMode = WESTERN_RED_FILTER.blend;
	sprite.width = SCENE_ART.width;
	sprite.height = SCENE_ART.height;
	sprite.alpha = WESTERN_RED_FILTER.baseOpacity;
	parent.addToParent(sprite);

	$effect(() => {
		const tex = context.stateApp.loadedAssets?.westernSceneRedFilter as Texture | undefined;
		if (tex && sprite.texture !== tex) sprite.texture = tex;
		sprite.visible = Boolean(tex);
		sprite.alpha = amount;
	});

	onMount(() => {
		return () => {
			sprite.parent?.removeChild(sprite);
			sprite.destroy();
		};
	});
</script>
