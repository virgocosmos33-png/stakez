<script lang="ts">
	/**
	 * Ready room from
	 * C:/Users/Emex33/Documents/fire frame vfx/backgroundSPINE/spine-scene.
	 * Skeleton root is bottom-left, Y-up. spine-pixi sets Skeleton.yDown, so
	 * the instance sits on the plate's bottom-left and draws upward.
	 * Track 0 = idle. Barrel glow is BarrelLampGlow, not this skeleton.
	 * Chains stay on this skeleton. Plaque wood / hanging lamps do not —
	 * those have live HUD and HangingLamps copies.
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
		WESTERN_SIGN_SLOTS,
		WESTERN_STREET_SLOTS,
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
		<HideSpineAttachment slotNames={WESTERN_STREET_SLOTS} hidden={true} />
		<HideSpineAttachment slotNames={WESTERN_PLAQUE_SLOTS} hidden={true} />
		<HideSpineAttachment slotNames={WESTERN_LAMP_SLOTS} hidden={true} />
		<HideSpineAttachment slotNames={WESTERN_SIGN_SLOTS} hidden={true} />
		<HideSpineAttachment slotNames={WESTERN_FREE_SPINS_CHAIN_SLOTS} hidden={!barrelOn} />
		<SpineTrack trackIndex={0} animationName="idle" loop={true} />
	</SpineProvider>
{/if}
