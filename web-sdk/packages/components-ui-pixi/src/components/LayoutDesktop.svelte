<script lang="ts">
	import { stateUi, stateBet } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';

	import { getContext } from '../context';
	import type { LayoutUiProps } from '../types';

	const props: LayoutUiProps = $props();
	const context = getContext();

	// Reference kit: two edge columns. Each column reads top -> bottom as
	// single / single(or big) / 2-button row / corner pill.
	const width = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const height = $derived(context.stateLayoutDerived.mainLayoutStandard().height);

	const LEFT_X = $derived(width * 0.072);
	const RIGHT_X = $derived(width * 0.916); // turbo + spin singles
	const RIGHT_EDGE = $derived(width * 0.94); // the paired row hugs the edge
	const PAIR_DX = $derived(width * 0.092); // gap between the two paired buttons
	const SPIN_X = $derived(width * 0.908);
	const BET_X = $derived(width * 0.135);
	const BALANCE_X = $derived(width * 0.845);

	const Y_TOP = $derived(height * 0.285);
	const Y_MID = $derived(height * 0.465);
	const SPIN_Y = $derived(height * 0.5);
	const Y_ROW = $derived(height * 0.66);
	const Y_PILL = $derived(height * 0.855);
</script>

<Container x={20}>
	{@render props.gameName()}
</Container>

<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
	{@render props.logo()}
</Container>

<MainContainer standard>
	<!-- LEFT column: crown, menu, (sound + coins), BET pill -->
	<Container x={LEFT_X} y={Y_TOP} scale={0.9}>
		{@render props.buttonBuyBonus({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X} y={Y_MID} scale={0.9}>
		{@render props.buttonMenu({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X} y={Y_ROW} scale={0.9}>
		{@render props.buttonSoundSwitch({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X + PAIR_DX} y={Y_ROW} scale={0.9}>
		{@render props.buttonPayTable({ anchor: 0.5 })}
	</Container>

	<Container x={BET_X} y={Y_PILL} scale={0.66}>
		{@render props.amountBet({ stacked: true })}
	</Container>

	<!-- RIGHT column: turbo, SPIN, (autoSpin + settings), BALANCE pill -->
	<Container x={RIGHT_X} y={Y_TOP} scale={0.9}>
		{@render props.buttonTurbo({ anchor: 0.5 })}
	</Container>

	<Container x={SPIN_X} y={SPIN_Y} scale={1.2}>
		{@render props.buttonBet({ anchor: 0.5 })}
	</Container>

	<Container x={RIGHT_EDGE - PAIR_DX} y={Y_ROW} scale={0.9}>
		{@render props.buttonAutoSpin({ anchor: 0.5 })}
	</Container>

	<Container x={RIGHT_EDGE} y={Y_ROW} scale={0.9}>
		{@render props.buttonSettings({ anchor: 0.5 })}
	</Container>

	<Container x={BALANCE_X} y={Y_PILL} scale={0.66}>
		{@render props.amountBalance({ stacked: true })}
	</Container>

	<!-- WIN surfaces centred only during a win; the reference keeps it clear -->
	{#if stateBet.winBookEventAmount > 0}
		<Container x={width * 0.5} y={Y_PILL} scale={0.66}>
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
		<!-- drawer opens upward from the menu button in the left column -->
		<Container x={LEFT_X} y={Y_MID}>
			<Container scale={0.85} y={-160 * 3}>
				{@render props.buttonPayTable({ anchor: 0.5 })}
			</Container>

			<Container scale={0.85} y={-160 * 2}>
				{@render props.buttonGameRules({ anchor: 0.5 })}
			</Container>

			<Container scale={0.85} y={-160}>
				{@render props.buttonSettings({ anchor: 0.5 })}
			</Container>

			<Container scale={0.85}>
				{@render props.buttonMenuClose({ anchor: 0.5 })}
			</Container>
		</Container>
	</MainContainer>
{/if}
