<script lang="ts">
	/**
	 * Ready-made backgroundSPINE western scene via SpineProvider
	 * (same path as symbols / hanging lamps). Barrel glow on in bonus.
	 */
	import { SpineProvider, SpineTrack } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SCENE_ART } from '../game/saloonLamps';

	const context = getContext();
	const hasScene = $derived.by(() => {
		const data = context.stateApp.loadedAssets?.westernScene as
			| { bones?: unknown; animations?: unknown }
			| undefined;
		return Array.isArray(data?.bones) && Array.isArray(data?.animations);
	});
	const barrelOn = $derived(context.stateGame.atmosphere !== 'base');
</script>

{#if hasScene}
	<SpineProvider
		key="westernScene"
		x={0}
		y={0}
		width={SCENE_ART.width}
		height={SCENE_ART.height}
		anchor={0}
		zIndex={1}
	>
		<SpineTrack trackIndex={0} animationName="idle" loop={true} />
		{#if barrelOn}
			<SpineTrack trackIndex={1} animationName="barrel_on" loop={true} />
		{/if}
	</SpineProvider>
{/if}
