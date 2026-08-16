<script lang="ts">
	import { Container } from 'pixi-svelte';

	import Symbol from './Symbol.svelte';
	import SymbolWrap from './SymbolWrap.svelte';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getReelYOffset } from '../game/utils';
	import type { ReelSymbol } from '../game/stateGame.svelte';

	type Props = {
		reelIndex: number;
		reelSymbol: ReelSymbol;
	};

	const props: Props = $props();
	const context = getContext();
	const symbolInfo = $derived(
		getSymbolInfo({ rawSymbol: props.reelSymbol.rawSymbol, state: props.reelSymbol.symbolState }),
	);
	const spinning = $derived(props.reelSymbol.symbolState === 'spin');
	const covered = $derived(context.stateGame.nudgeCoverReel === props.reelIndex);
	const lastReel = context.stateGame.board.length - 1;
	const laneShut = $derived(props.reelIndex === lastReel && !context.stateGame.lidOpen);
	const hide = $derived(
		covered || laneShut || (props.reelSymbol.rawSymbol.name === 'NW' && !spinning),
	);
</script>

<SymbolWrap
	reelIndex={props.reelIndex}
	x={getSymbolX(props.reelIndex)}
	y={props.reelSymbol.symbolY.current + getReelYOffset(props.reelIndex)}
	animating={symbolInfo.type === 'spine' &&
		(props.reelSymbol.symbolState === 'land' || props.reelSymbol.symbolState === 'win')}
>
	<Container alpha={hide ? 0 : 1}>
		<Symbol
			state={props.reelSymbol.symbolState}
			rawSymbol={props.reelSymbol.rawSymbol}
			oncomplete={() => {
				if (props.reelSymbol.symbolState === 'win') props.reelSymbol.oncomplete();
				if (props.reelSymbol.symbolState === 'land') {
					props.reelSymbol.symbolState = 'static';
					props.reelSymbol.oncomplete();
				}
			}}
		/>
	</Container>
</SymbolWrap>
