<script lang="ts">
	import { type SpineTrackProps } from 'pixi-svelte';

	import { getSymbolInfo } from '../game/utils';
	import SymbolSpineMain from './SymbolSpineMain.svelte';

	// The template's gold 'payframe' win overlay was dropped with the Madam
	// Mirror spine set: the win skeletons carry their own additive glow flash.
	type Props = {
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		x?: number;
		y?: number;
		listener: SpineTrackProps['listener'];
		loop?: boolean;
	};

	const props: Props = $props();
</script>

<SymbolSpineMain
	x={props.x}
	y={props.y}
	symbolInfo={props.symbolInfo}
	listener={props.listener}
	loop={props.loop}
/>
