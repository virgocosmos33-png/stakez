<script lang="ts">
	/**
	 * Ready room from assets/spines/western_scene (the folder the user edits).
	 * Skeleton root is bottom-left, Y-up. spine-pixi sets Skeleton.yDown, so
	 * the instance sits on the plate's bottom-left and draws upward.
	 * Track 0 = idle (rotate-only). Sky / clouds / town stay on this skeleton
	 * in PSD Z order. CloudsMarquee slides the cloud slots right → left.
	 * Sitting barrel lantern stays on this skeleton. Street hanging lamps do not.
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
	import CloudsMarquee from './CloudsMarquee.svelte';
	import HideSpineAttachment from './HideSpineAttachment.svelte';
	import WesternRedFilter from './WesternRedFilter.svelte';

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
		<WesternRedFilter />
		<CloudsMarquee />
		<SpineTrack trackIndex={0} animationName="idle" loop={true} />
	</SpineProvider>
{/if}
