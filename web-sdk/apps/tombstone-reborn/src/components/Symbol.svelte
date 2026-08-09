<script lang="ts">
	import SymbolSpine from './SymbolSpine.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import { getSymbolInfo } from '../game/utils';
	import type { SymbolState, RawSymbol } from '../game/types';
	import { getContext } from '../game/context';

	type Props = {
		x?: number;
		y?: number;
		state: SymbolState;
		rawSymbol: RawSymbol;
		oncomplete?: () => void;
		loop?: boolean;
	};

	const props: Props = $props();
	const context = getContext();
	const symbolInfo = $derived(getSymbolInfo({ rawSymbol: props.rawSymbol, state: props.state }));
	const isSprite = $derived(symbolInfo.type === 'sprite');

	// No runtime outline frame: every card carries its own thin portrait bezel,
	// baked by tools/make_symbols_portrait.py into both the static atlas and the
	// spine atlas so the border survives win/land animations. A square overlay
	// here would cut straight across that portrait silhouette.
</script>

{#if isSprite}
	<SymbolSprite
		{symbolInfo}
		state={props.state}
		x={props.x}
		y={props.y}
		oncomplete={props.oncomplete}
	/>
{:else}
	<!-- win/land run once and report complete; postWin is the looping mesh
	ripple that keeps the winning card alive while it rests -->
	<SymbolSpine
		loop={props.loop || props.state === 'postWin'}
		{symbolInfo}
		x={props.x}
		y={props.y}
		listener={{
			complete: props.oncomplete,
			event: (_, event) => {
				if (event.data?.name === 'wildExplode') {
					context.eventEmitter?.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
				}
			},
		}}
	/>
{/if}
