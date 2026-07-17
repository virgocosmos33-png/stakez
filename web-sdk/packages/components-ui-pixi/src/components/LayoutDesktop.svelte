<script lang="ts">
	import { stateUi } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';

	import { getContext } from '../context';
	import type { LayoutUiProps } from '../types';

	const props: LayoutUiProps = $props();
	const context = getContext();

	// NLC-style chrome: buy/menu on the left edge, spin cluster on the right
	// edge, slim amounts bar along the bottom
	const SIDE_MARGIN = 150;
	const width = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const height = $derived(context.stateLayoutDerived.mainLayoutStandard().height);
</script>

<Container x={20}>
	{@render props.gameName()}
</Container>

<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
	{@render props.logo()}
</Container>

<MainContainer standard>
	<!-- left column -->
	<Container x={SIDE_MARGIN} y={height * 0.42} scale={0.9}>
		{@render props.buttonBuyBonus({ anchor: 0.5 })}
	</Container>

	<Container x={SIDE_MARGIN} y={height * 0.42 + 190} scale={0.75}>
		{@render props.buttonMenu({ anchor: 0.5 })}
	</Container>

	<!-- right column: autoplay above, big spin center, turbo below -->
	<Container x={width - SIDE_MARGIN} y={height * 0.5 - 210} scale={0.75}>
		{@render props.buttonAutoSpin({ anchor: 0.5 })}
	</Container>

	<Container x={width - SIDE_MARGIN} y={height * 0.5}>
		{@render props.buttonBet({ anchor: 0.5 })}
	</Container>

	<Container x={width - SIDE_MARGIN} y={height * 0.5 + 210} scale={0.75}>
		{@render props.buttonTurbo({ anchor: 0.5 })}
	</Container>
</MainContainer>

<MainContainer standard alignVertical="bottom">
	<!-- slim bottom bar: bet with +/- on the left, win center, balance right -->
	<Container x={SIDE_MARGIN + 60} y={height - 65} scale={0.55}>
		{@render props.buttonDecrease({ anchor: 0.5 })}
	</Container>

	<Container x={SIDE_MARGIN + 210} y={height - 65} scale={0.62}>
		{@render props.amountBet({ stacked: true })}
	</Container>

	<Container x={SIDE_MARGIN + 360} y={height - 65} scale={0.55}>
		{@render props.buttonIncrease({ anchor: 0.5 })}
	</Container>

	<Container x={width * 0.5} y={height - 65} scale={0.62}>
		{@render props.amountWin({ stacked: true })}
	</Container>

	<Container x={width - SIDE_MARGIN - 210} y={height - 65} scale={0.62}>
		{@render props.amountBalance({ stacked: true })}
	</Container>
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
		<Container x={SIDE_MARGIN} y={height * 0.42 + 190}>
			<Container scale={0.75} y={-170 * 4}>
				{@render props.buttonPayTable({ anchor: 0.5 })}
			</Container>

			<Container scale={0.75} y={-170 * 3}>
				{@render props.buttonGameRules({ anchor: 0.5 })}
			</Container>

			<Container scale={0.75} y={-170 * 2}>
				{@render props.buttonSettings({ anchor: 0.5 })}
			</Container>

			<Container scale={0.75} y={-170}>
				{@render props.buttonSoundSwitch({ anchor: 0.5 })}
			</Container>

			<Container scale={0.75}>
				{@render props.buttonMenuClose({ anchor: 0.5 })}
			</Container>
		</Container>
	</MainContainer>
{/if}
