<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { Container, Rectangle } from 'pixi-svelte';
	import type { Filter } from 'pixi.js';

	import Symbol from './Symbol.svelte';
	import SymbolWrap from './SymbolWrap.svelte';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getReelYOffset, getCardHeight } from '../game/utils';
	import { SYMBOL_CARD_W } from '../game/constants';
	import { fxDur } from '../game/fxTiming';
	import { createGlassDentFilter } from '../game/glassDentFilter';
	import { CRUSH_IN_MS, CRUSH_OUT_MS, DENT_PUNCH_MS, DENT_RESIDUAL, DENT_SETTLE_MS } from '../game/gunsmokeSpin';
	import type { ReelSymbol } from '../game/stateGame.svelte';

	type Props = {
		reelIndex: number;
		row: number;
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
	const laneSwap = $derived(
		props.reelIndex === lastReel && props.row === 1 ? context.stateGame.laneCardSwap : 0,
	);
	const pocketH = $derived(getCardHeight(props.reelIndex));

	const NO_FILTERS: Filter[] = [];
	type Dent = ReturnType<typeof createGlassDentFilter>;
	let dent = $state<Dent | null>(null);
	let dentOn = $state(false);
	const dentAmt = new Tween(0);
	const crush = new Tween(0);
	const dentFilters = $derived(dentOn && dent ? [dent.filter] : NO_FILTERS);
	const crushX = $derived(1 + 0.1 * crush.current);
	const crushY = $derived(1 - 0.18 * crush.current);

	$effect(() => {
		if (!dent) return;
		dent.uniforms.uStrength = dentAmt.current;
	});

	const ensureDent = () => {
		if (dent) return dent;
		dent = createGlassDentFilter();
		return dent;
	};

	const punchGlass = (hitX: number, hitY: number, seed: number) => {
		const live = ensureDent();
		live.uniforms.uHit[0] = hitX;
		live.uniforms.uHit[1] = hitY;
		live.uniforms.uSeed = seed;
		dentOn = true;
		void dentAmt.set(1, { duration: fxDur(DENT_PUNCH_MS), easing: backOut }).then(() => {
			void dentAmt.set(DENT_RESIDUAL, { duration: fxDur(DENT_SETTLE_MS), easing: cubicOut });
		});
		void crush.set(1, { duration: fxDur(CRUSH_IN_MS), easing: backOut }).then(() => {
			void crush.set(0, { duration: fxDur(CRUSH_OUT_MS), easing: cubicOut });
		});
	};

	const clearDent = () => {
		dentOn = false;
		dentAmt.set(0, { duration: 0 });
		crush.set(0, { duration: 0 });
	};

	context.eventEmitter.subscribeOnMount({
		gunsmokeCellDent: ({ reel, row, hitX, hitY, seed }) => {
			if (reel !== props.reelIndex || row !== props.row) return;
			punchGlass(hitX, hitY, seed);
		},
		gunsmokeWoundsClear: () => clearDent(),
		featureFxFallOut: () => clearDent(),
	});

	onDestroy(() => {
		dent?.filter.destroy();
		dent = null;
	});
</script>

<SymbolWrap
	reelIndex={props.reelIndex}
	x={getSymbolX(props.reelIndex)}
	y={props.reelSymbol.symbolY.current + getReelYOffset(props.reelIndex)}
	animating={symbolInfo.type === 'spine' &&
		(props.reelSymbol.symbolState === 'land' || props.reelSymbol.symbolState === 'win')}
>
	<Container alpha={hide ? 0 : 1} scale={{ x: crushX, y: crushY }}>
		{#if props.reelIndex === lastReel && props.row === 1}
			<Rectangle isMask anchor={0.5} width={SYMBOL_CARD_W} height={pocketH} backgroundColor={0xffffff} />
		{/if}
		<Container y={laneSwap * pocketH} filters={dentFilters}>
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
	</Container>
</SymbolWrap>
