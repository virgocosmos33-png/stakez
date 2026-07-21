<script lang="ts">
	import { stateUi } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';

	import { getContext } from '../context';
	import type { LayoutUiProps } from '../types';

	const props: LayoutUiProps = $props();
	const context = getContext();

	// Tablet is a square (1920x1920) design space; the same reference two-column
	// structure applies, with the vertical rhythm pulled toward the lower half so
	// the columns frame the board instead of floating.
	const width = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const height = $derived(context.stateLayoutDerived.mainLayoutStandard().height);

	// Fit the two HUD columns to the reel frame's width. BoardFrame publishes the
	// frame's outer width (main-layout design px); convert it into this layout's
	// local (standard) px via the two layout scales, then anchor each column to a
	// frame edge (a small EDGE_INSET keeps the button ornament just inside the
	// gold). Every position keeps its original offset from its column's edge, so
	// internal spacing and element sizes/heights are untouched. Falls back to the
	// original width-fraction positions until the frame publishes its width.
	const frameLocalW = $derived(
		stateUi.boardFrameWidth > 0
			? (stateUi.boardFrameWidth * context.stateLayoutDerived.mainLayout().scale) /
					context.stateLayoutDerived.mainLayoutStandard().scale
			: 0,
	);
	const EDGE_INSET = $derived(width * 0.02);
	const leftEdge = $derived(
		frameLocalW > 0 ? width / 2 - frameLocalW / 2 + EDGE_INSET : width * 0.072,
	);
	const rightEdge = $derived(
		frameLocalW > 0 ? width / 2 + frameLocalW / 2 - EDGE_INSET : width * 0.94,
	);

	const LEFT_X = $derived(leftEdge);
	const RIGHT_EDGE = $derived(rightEdge);
	const RIGHT_X = $derived(rightEdge - width * 0.024);
	const PAIR_DX = $derived(width * 0.092);
	const SPIN_X = $derived(rightEdge - width * 0.032);
	const BET_X = $derived(leftEdge + width * 0.063);
	const BALANCE_X = $derived(rightEdge - width * 0.095);

	// Vertical rhythm, tightened so the bigger controls sit closer together
	// (roughly halves the previous inter-row gaps) while the columns stay
	// anchored to the frame edges (horizontal span preserved).
	const Y_TOP = $derived(height * 0.4);
	const Y_MID = $derived(height * 0.52);
	const SPIN_Y = $derived(height * 0.55);
	const Y_ROW = $derived(height * 0.64);
	const Y_PILL = $derived(height * 0.78);
</script>

<Container x={20}>
	{@render props.gameName()}
</Container>

<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
	{@render props.logo()}
</Container>

<MainContainer standard>
	<!-- LEFT column: crown, menu, (sound + coins), BET pill -->
	<Container x={LEFT_X} y={Y_TOP} scale={1.05}>
		{@render props.buttonBuyBonus({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X} y={Y_MID} scale={1.05}>
		{@render props.buttonMenu({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X} y={Y_ROW} scale={1.05}>
		{@render props.buttonSoundSwitch({ anchor: 0.5 })}
	</Container>

	<Container x={LEFT_X + PAIR_DX} y={Y_ROW} scale={1.05}>
		{@render props.buttonPayTable({ anchor: 0.5 })}
	</Container>

	<!-- BET readout flanked by −/+ steppers. The pill centres its text row at
	     pillH/2 * scale below its origin, so the medallions sit at Y_PILL+32 to
	     line up with the "BET $value" baseline; ±width*0.095 clears the widest value. -->
	<Container x={BET_X - width * 0.095} y={Y_PILL + 32} scale={0.55}>
		{@render props.buttonDecrease({ anchor: 0.5 })}
	</Container>

	<Container x={BET_X} y={Y_PILL} scale={0.8}>
		{@render props.amountBet({ stacked: true })}
	</Container>

	<Container x={BET_X + width * 0.095} y={Y_PILL + 32} scale={0.55}>
		{@render props.buttonIncrease({ anchor: 0.5 })}
	</Container>

	<!-- RIGHT column: turbo, SPIN, (autoSpin + settings), BALANCE pill -->
	<Container x={RIGHT_X} y={Y_TOP} scale={1.05}>
		{@render props.buttonTurbo({ anchor: 0.5 })}
	</Container>

	<Container x={SPIN_X} y={SPIN_Y} scale={1.05}>
		{@render props.buttonBet({ anchor: 0.5 })}
	</Container>

	<Container x={RIGHT_EDGE - PAIR_DX} y={Y_ROW} scale={1.05}>
		{@render props.buttonAutoSpin({ anchor: 0.5 })}
	</Container>

	<Container x={RIGHT_EDGE} y={Y_ROW} scale={1.05}>
		{@render props.buttonSettings({ anchor: 0.5 })}
	</Container>

	<Container x={BALANCE_X} y={Y_PILL} scale={0.8}>
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
