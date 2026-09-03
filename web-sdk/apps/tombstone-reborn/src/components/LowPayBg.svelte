<script lang="ts">
	import CellPocketBg from './CellPocketBg.svelte';

	const props: { reelIndex?: number; x?: number; y?: number } = $props();
</script>

<CellPocketBg assetKey="lowPayBg" reelIndex={props.reelIndex} x={props.x} y={props.y} />
