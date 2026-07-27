<script lang="ts">
	/**
	 * Bonus ENTER/EXIT shower (freeSpinTrigger + freeSpinEnd → type:'transition').
	 * Atlas: spines/transition — rock1..rock8 MUST be White Room clinical debris
	 * (ceramic/pills/PATIENT 404 paper/lint/buckles). ZERO purple diamonds.
	 * Regen: regenerate_assets scope=transition → tools/make_transition_debris.py
	 */
	import { SpineProvider, SpineTrack } from 'pixi-svelte';
	import { getContext } from '../game/context';

	type Props = {
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();
</script>

<SpineProvider
	key="transition"
	x={context.stateLayoutDerived.canvasSizes().width * 0.5}
	y={context.stateLayoutDerived.canvasSizes().height * 0.5}
	height={context.stateLayoutDerived.canvasSizes().height * 1.7}
>
	<SpineTrack
		trackIndex={0}
		animationName={'animation'}
		listener={{
			complete: props.oncomplete,
		}}
	/>
</SpineProvider>
