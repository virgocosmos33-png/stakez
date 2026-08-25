<script lang="ts">
	/**
	 * Full TR2 Spine Background scene
	 * (https://github.com/brandnitions-dev/TR2-Spine-Background-scene).
	 * Skeleton root is bottom-left, Y-up. spine-pixi sets Skeleton.yDown, so
	 * the instance sits on the plate's bottom-left and draws upward.
	 * Track 0 = idle. Track 1 = barrel_on only in bonus.
	 * Chains stay on this skeleton. Plaque wood / lamps do not — those have
	 * live HUD and HangingLamps copies.
	 */
	import { SpineProvider, SpineTrack } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { isBonusAtmosphere } from '../game/atmosphere.svelte';
	import { SCENE_ART } from '../game/saloonLamps';
	import {
		isWesternSceneSkeleton,
		WESTERN_FREE_SPINS_CHAIN_SLOTS,
		WESTERN_LAMP_SLOTS,
		WESTERN_PLAQUE_SLOTS,
	} from '../game/westernScene';
	import HideSpineAttachment from './HideSpineAttachment.svelte';

	const context = getContext();
	const hasScene = $derived(isWesternSceneSkeleton(context.stateApp.loadedAssets?.westernScene));
	const barrelOn = $derived(isBonusAtmosphere(context.stateGame.atmosphere));
</script>

{#if hasScene}
	<SpineProvider
		key="westernScene"
		x={0}
		y={SCENE_ART.height}
		scale={2}
		anchor={0}
		zIndex={1}
	>
		<HideSpineAttachment slotName="background" hidden={true} />
		<HideSpineAttachment slotNames={WESTERN_PLAQUE_SLOTS} hidden={true} />
		<HideSpineAttachment slotNames={WESTERN_LAMP_SLOTS} hidden={true} />
		<HideSpineAttachment slotNames={WESTERN_FREE_SPINS_CHAIN_SLOTS} hidden={!barrelOn} />
		<SpineTrack trackIndex={0} animationName="idle" loop={true} />
		{#if barrelOn}
			<SpineTrack trackIndex={1} animationName="barrel_on" loop={true} />
		{/if}
	</SpineProvider>
{/if}
