<script lang="ts">
	import SymbolSpine from './SymbolSpine.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import { getSymbolInfo } from '../game/utils';
	import type { SymbolState, RawSymbol } from '../game/types';
	import { getContext } from '../game/context';
	import { Container, Graphics, Sprite } from 'pixi-svelte';
	import { SYMBOL_SIZE, HIGH_SYMBOLS } from '../game/constants';

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

	// haunted-mirror glass: a real symbol trapped behind a glass overlay until
	// the burst shatters it (HM art only appears as spin-by filler)
	const glassed = $derived(props.rawSymbol.glass === true || props.rawSymbol.name === 'HM');
	// high symbols wear an ornate frame so they read as premium at a glance
	const isHigh = $derived(HIGH_SYMBOLS.includes(props.rawSymbol.name));

	const drawHighBorder = (graphics: import('pixi.js').Graphics) => {
		const s = SYMBOL_SIZE;
		// dark separation edge
		graphics.roundRect(-s / 2, -s / 2, s, s, 9);
		graphics.stroke({ color: 0x120b04, width: 6, alpha: 0.85 });
		// aged gold frame
		graphics.roundRect(-s / 2 + 1.5, -s / 2 + 1.5, s - 3, s - 3, 8);
		graphics.stroke({ color: 0xc9a34a, width: 3.5, alpha: 0.95 });
		// pale bone inner line
		graphics.roundRect(-s / 2 + 6, -s / 2 + 6, s - 12, s - 12, 6);
		graphics.stroke({ color: 0xf0e3c0, width: 1.4, alpha: 0.6 });
		// corner studs
		const inset = s / 2 - 7;
		for (const cornerX of [-inset, inset]) {
			for (const cornerY of [-inset, inset]) {
				graphics.circle(cornerX, cornerY, 3);
				graphics.fill({ color: 0xe3c06a, alpha: 0.95 });
			}
		}
	};

</script>

{#if isSprite}
	<SymbolSprite
		{symbolInfo}
		state={props.state}
		x={props.x}
		y={props.y}
		oncomplete={props.oncomplete}
	/>
	{#if isHigh}
		<Container x={props.x ?? 0} y={props.y ?? 0}>
			<Graphics draw={drawHighBorder} />
		</Container>
	{/if}
	{#if glassed}
		<Container x={props.x ?? 0} y={props.y ?? 0}>
			<Sprite
				key="glassIntact"
				anchor={0.5}
				width={SYMBOL_SIZE}
				height={SYMBOL_SIZE}
				alpha={0.92}
			/>
		</Container>
	{/if}
{:else}
	<SymbolSpine
		loop={props.loop}
		{symbolInfo}
		x={props.x}
		y={props.y}
		showWinFrame={props.state === 'win' && !['S', 'M'].includes(props.rawSymbol.name)}
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
