<script lang="ts">
	/**
	 * Full TR2 Spine Background scene
	 * (https://github.com/brandnitions-dev/TR2-Spine-Background-scene).
	 * Skeleton root is bottom-left, Y-up. spine-pixi sets Skeleton.yDown, so
	 * the instance sits on the plate's bottom-left and draws upward.
	 * Track 0 = idle. Track 1 = barrel_on only in bonus.
	 */
	import { SpineProvider, SpineTrack } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SCENE_ART } from '../game/saloonLamps';
	import { isWesternSceneSkeleton } from '../game/westernScene';
	import HideSpineAttachment from './HideSpineAttachment.svelte';

	const context = getContext();
	const hasScene = $derived(isWesternSceneSkeleton(context.stateApp.loadedAssets?.westernScene));
	const barrelOn = $derived(context.stateGame.atmosphere !== 'base');
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
		<HideSpineAttachment slotName="background" />
		<SpineTrack trackIndex={0} animationName="idle" loop={true} />
		{#if barrelOn}
			<SpineTrack trackIndex={1} animationName="barrel_on" loop={true} />
		{/if}
	</SpineProvider>
{/if}
