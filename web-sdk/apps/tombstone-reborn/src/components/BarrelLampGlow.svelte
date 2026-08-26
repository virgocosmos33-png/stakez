<script lang="ts">
	/**
	 * Ready lantern_dim_light.png at the Spine barrel seat.
	 * Bonus / freegame / laneSuper: on at Glow 0.40x, additive.
	 */
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { isBarrelLampOn } from '../game/atmosphere.svelte';
	import { WESTERN_BARREL_GLOW, WESTERN_BARREL_LUMEN } from '../game/westernScene';

	const context = getContext();
	const on = $derived.by(() => {
		void context.stateGame.atmosphere;
		void context.stateGame.gameType;
		void context.stateGame.laneSuper;
		return isBarrelLampOn();
	});
	const ready = $derived(Boolean(context.stateApp.loadedAssets?.westernSceneBarrelLight));
</script>

{#if on && ready}
	<Sprite
		key="westernSceneBarrelLight"
		x={WESTERN_BARREL_GLOW.x}
		y={WESTERN_BARREL_GLOW.y}
		anchor={0.5}
		width={WESTERN_BARREL_GLOW.w}
		height={WESTERN_BARREL_GLOW.h}
		alpha={WESTERN_BARREL_LUMEN}
		blendMode="add"
		zIndex={15}
		eventMode="none"
	/>
{/if}
