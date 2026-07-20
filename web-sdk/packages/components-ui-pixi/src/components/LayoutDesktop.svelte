<script lang="ts">
	import { stateUi, stateBet } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';

	import { getContext } from '../context';
	import type { LayoutUiProps } from '../types';
	import { HUD_EDGE_PAD, HUD_PAIR_STEP, HUD_SCALE, stackHudColumn } from '../layoutSpacing';

	const props: LayoutUiProps = $props();
	const context = getContext();

	const width = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const height = $derived(context.stateLayoutDerived.mainLayoutStandard().height);

	// same pad on left / right / bottom — columns and BET/BALANCE hug the edges equally
	const LEFT_EDGE = HUD_EDGE_PAD;
	const RIGHT_EDGE = $derived(width - HUD_EDGE_PAD);
	const PAIR_STEP = HUD_PAIR_STEP;
	const LEFT_ANCHOR = { x: 0, y: 0.5 } as const;
	const RIGHT_ANCHOR = { x: 1, y: 0.5 } as const;

	const stack = $derived(stackHudColumn(height));
</script>

<Container x={20}>
	{@render props.gameName()}
</Container>

<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
	{@render props.logo()}
</Container>

<MainContainer standard>
	<!-- LEFT column: menu → pair → BET (same gap throughout) -->
	<Container x={LEFT_EDGE} y={stack.yMenu} scale={HUD_SCALE.menu}>
		{@render props.buttonMenu({ anchor: LEFT_ANCHOR })}
	</Container>

	<Container x={LEFT_EDGE} y={stack.yPair} scale={HUD_SCALE.pair}>
		{@render props.buttonSoundSwitch({ anchor: LEFT_ANCHOR })}
	</Container>

	<Container x={LEFT_EDGE + PAIR_STEP} y={stack.yPair} scale={HUD_SCALE.pair}>
		{@render props.buttonBetMenu({ anchor: LEFT_ANCHOR })}
	</Container>

	<Container x={LEFT_EDGE} y={stack.yLabel} scale={HUD_SCALE.label}>
		{@render props.amountBet({ stacked: true, align: 'left' })}
	</Container>

	<!-- RIGHT column: BUY → SPIN → pair → BALANCE (same gap throughout) -->
	<Container x={RIGHT_EDGE} y={stack.yBuy} scale={HUD_SCALE.buy}>
		{@render props.buttonBuyBonus({ anchor: RIGHT_ANCHOR })}
	</Container>

	<Container x={RIGHT_EDGE} y={stack.ySpin} scale={HUD_SCALE.spin}>
		{@render props.buttonBet({ anchor: RIGHT_ANCHOR })}
	</Container>

	<Container x={RIGHT_EDGE - PAIR_STEP} y={stack.yPair} scale={HUD_SCALE.pair}>
		{@render props.buttonAutoSpin({ anchor: RIGHT_ANCHOR })}
	</Container>

	<Container x={RIGHT_EDGE} y={stack.yPair} scale={HUD_SCALE.pair}>
		{@render props.buttonTurbo({ anchor: RIGHT_ANCHOR })}
	</Container>

	<Container x={RIGHT_EDGE} y={stack.yLabel} scale={HUD_SCALE.label}>
		{@render props.amountBalance({ stacked: true, align: 'right' })}
	</Container>

	{#if stateBet.winBookEventAmount > 0}
		<Container x={width * 0.5} y={stack.yLabel} scale={HUD_SCALE.label}>
			{@render props.amountWin({ stacked: true })}
		</Container>
	{/if}
</MainContainer>

{#if stateUi.menuOpen}
	<Rectangle
		eventMode="static"
		cursor="pointer"
		alpha={0.5}
		anchor={0.5}
		backgroundColor={BLACK}
		width={context.stateLayoutDerived.canvasSizes().width}
		height={context.stateLayoutDerived.canvasSizes().height}
		x={context.stateLayoutDerived.canvasSizes().width * 0.5}
		y={context.stateLayoutDerived.canvasSizes().height * 0.5}
		onpointerup={() => (stateUi.menuOpen = false)}
	/>

	<MainContainer standard>
		<Container x={LEFT_EDGE} y={stack.yMenu}>
			<Container scale={0.85} y={-160 * 3}>
				{@render props.buttonPayTable({ anchor: LEFT_ANCHOR })}
			</Container>

			<Container scale={0.85} y={-160 * 2}>
				{@render props.buttonGameRules({ anchor: LEFT_ANCHOR })}
			</Container>

			<Container scale={0.85} y={-160}>
				{@render props.buttonSettings({ anchor: LEFT_ANCHOR })}
			</Container>

			<Container scale={0.85}>
				{@render props.buttonMenuClose({ anchor: LEFT_ANCHOR })}
			</Container>
		</Container>
	</MainContainer>
{/if}
