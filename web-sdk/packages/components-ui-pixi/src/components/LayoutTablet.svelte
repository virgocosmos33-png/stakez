<script lang="ts">
	import { stateUi, stateBet } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';

	import { getContext } from '../context';
	import type { LayoutUiProps } from '../types';
	import LabelFreeSpinCounter from './LabelFreeSpinCounter.svelte';

	const props: LayoutUiProps = $props();
	const context = getContext();

	// Tablet is a square (1920x1920) design space; the same reference two-column
	// structure applies, with the vertical rhythm pulled toward the lower half so
	// the columns frame the board instead of floating.
	const width = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const height = $derived(context.stateLayoutDerived.mainLayoutStandard().height);

	const LEFT_X = $derived(width * 0.072);
	const RIGHT_X = $derived(width * 0.916);
	const RIGHT_EDGE = $derived(width * 0.94);
	const PAIR_DX = $derived(width * 0.092);
	const SPIN_X = $derived(width * 0.908);
	const BET_X = $derived(width * 0.135);
	const BALANCE_X = $derived(width * 0.845);

	const Y_TOP = $derived(height * 0.4);
	const Y_MID = $derived(height * 0.54);
	const SPIN_Y = $derived(height * 0.57);
	const Y_ROW = $derived(height * 0.68);
	const Y_PILL = $derived(height * 0.82);
</script>

<Container x={20}>
	{@render props.gameName()}
</Container>

<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
	{@render props.logo()}
</Container>

<MainContainer standard>
	<!-- LEFT column: crown, menu, (sound + coins), BET pill -->
	<Container x={LEFT_X} y={Y_TOP} scale={0.95}>
		{@render props.buttonBuyBonus({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X} y={Y_MID} scale={0.95}>
		{@render props.buttonMenu({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X} y={Y_ROW} scale={0.95}>
		{@render props.buttonSoundSwitch({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X + PAIR_DX} y={Y_ROW} scale={0.95}>
		{@render props.buttonPayTable({ anchor: 0.5 })}
	</Container>

	<Container x={BET_X} y={Y_PILL} scale={0.72}>
		{@render props.amountBet({ stacked: true })}
	</Container>

	<!-- RIGHT column: turbo, SPIN, (autoSpin + settings), BALANCE pill -->
	<Container x={RIGHT_X} y={Y_TOP} scale={0.95}>
		{@render props.buttonTurbo({ anchor: 0.5 })}
	</Container>

	<Container x={SPIN_X} y={SPIN_Y} scale={1.25}>
		{@render props.buttonBet({ anchor: 0.5 })}
	</Container>

	<Container x={RIGHT_EDGE - PAIR_DX} y={Y_ROW} scale={0.95}>
		{@render props.buttonAutoSpin({ anchor: 0.5 })}
	</Container>

	<Container x={RIGHT_EDGE} y={Y_ROW} scale={0.95}>
		{@render props.buttonSettings({ anchor: 0.5 })}
	</Container>

	<Container x={BALANCE_X} y={Y_PILL} scale={0.72}>
		{@render props.amountBalance({ stacked: true })}
	</Container>

	{#if stateBet.winBookEventAmount > 0}
		<Container x={width * 0.5} y={Y_PILL} scale={0.72}>
			{@render props.amountWin({ stacked: true })}
		</Container>
	{/if}

	{#if stateUi.freeSpinCounterShow}
		<Container x={width * 0.5} y={Y_TOP} scale={0.9}>
			<LabelFreeSpinCounter />
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
		<Container x={LEFT_X} y={Y_MID}>
			<Container scale={0.9} y={-175 * 3}>
				{@render props.buttonPayTable({ anchor: 0.5 })}
			</Container>

			<Container scale={0.9} y={-175 * 2}>
				{@render props.buttonGameRules({ anchor: 0.5 })}
			</Container>

			<Container scale={0.9} y={-175}>
				{@render props.buttonSettings({ anchor: 0.5 })}
			</Container>

			<Container scale={0.9}>
				{@render props.buttonMenuClose({ anchor: 0.5 })}
			</Container>
		</Container>
	</MainContainer>
{/if}
