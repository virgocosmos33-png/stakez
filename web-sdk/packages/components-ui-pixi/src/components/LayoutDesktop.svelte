<script lang="ts">
	import { stateUi, stateBet } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';

	import { getContext } from '../context';
	import type { LayoutUiProps } from '../types';
	import { UI_BASE_SIZE } from '../constants';
	import ControlInfoBar, { INFO_BAR_SIZE } from './ControlInfoBar.svelte';

	const props: LayoutUiProps = $props();
	const context = getContext();

	const W = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const H = $derived(context.stateLayoutDerived.mainLayoutStandard().height);

	// ---- compact centred bottom control cluster ----
	// buy | menu | [ balance | bet ▲▼ ] | (turbo) SPIN (autoplay)
	const BAR_SCALE = 0.84;
	const BUY = UI_BASE_SIZE * 1.2;
	const SPIN = UI_BASE_SIZE * 1.2;
	const BADGE_SCALE = 0.6;
	const BADGE = UI_BASE_SIZE * BADGE_SCALE;
	const INFO = INFO_BAR_SIZE.width;
	const G1 = 14;
	const G2 = 16;
	const G3 = 22;
	const SIDE_GAP = 10; // clear gap between turbo/auto badges and spin
	const spinClusterW = BADGE + SIDE_GAP + SPIN + SIDE_GAP + BADGE;
	const TW = BUY + G1 + BADGE + G2 + INFO + G3 + spinClusterW;

	// local coords inside the scaled bar (origin = bar centre)
	const buyC = -TW / 2 + BUY / 2;
	const menuC = -TW / 2 + BUY + G1 + BADGE / 2;
	const infoL = -TW / 2 + BUY + G1 + BADGE + G2;
	const infoC = infoL + INFO / 2;
	const spinClusterL = infoL + INFO + G3;
	const turboC = spinClusterL + BADGE / 2;
	const spinC = turboC + BADGE / 2 + SIDE_GAP + SPIN / 2;
	const autoC = spinC + SPIN / 2 + SIDE_GAP + BADGE / 2;

	// hug the bottom: leave a small pad under the scaled spin coin
	const BOTTOM_PAD = 22;
	const barY = $derived(H - BOTTOM_PAD - (SPIN * BAR_SCALE) / 2);
	const barX = $derived(W / 2);
</script>

<Container x={20}>
	{@render props.gameName()}
</Container>

<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
	{@render props.logo()}
</Container>

<MainContainer standard>
	<Container x={barX} y={barY} scale={BAR_SCALE}>
		<!-- buy bonus coin -->
		<Container x={buyC} y={0}>
			{@render props.buttonBuyBonus({ anchor: 0.5 })}
		</Container>

		<!-- menu badge -->
		<Container x={menuC} y={0} scale={BADGE_SCALE}>
			{@render props.buttonMenu({ anchor: 0.5 })}
		</Container>

		<!-- unified balance / bet panel -->
		<Container x={infoC} y={0}>
			<Container x={-INFO / 2} y={-INFO_BAR_SIZE.height / 2}>
				<ControlInfoBar />
			</Container>
		</Container>

		<!-- spin first, then side badges on top -->
		<Container x={spinC} y={0}>
			{@render props.buttonBet({ anchor: 0.5 })}
		</Container>
		<Container x={turboC} y={0} scale={BADGE_SCALE}>
			{@render props.buttonTurbo({ anchor: 0.5 })}
		</Container>
		<Container x={autoC} y={0} scale={BADGE_SCALE}>
			{@render props.buttonAutoSpin({ anchor: 0.5 })}
		</Container>

		<!-- win amount (only while resolving a win) -->
		{#if stateBet.winBookEventAmount > 0}
			<Container x={0} y={-140}>
				{@render props.amountWin({ stacked: true })}
			</Container>
		{/if}
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

	<!-- submenu pops UP from the menu badge -->
	<MainContainer standard>
		<Container x={barX} y={barY} scale={BAR_SCALE}>
			<Container x={menuC} y={0} scale={BADGE_SCALE}>
				<Container y={-160 * 3}>
					{@render props.buttonPayTable({ anchor: 0.5 })}
				</Container>
				<Container y={-160 * 2}>
					{@render props.buttonGameRules({ anchor: 0.5 })}
				</Container>
				<Container y={-160}>
					{@render props.buttonSettings({ anchor: 0.5 })}
				</Container>
				<Container>
					{@render props.buttonMenuClose({ anchor: 0.5 })}
				</Container>
			</Container>
		</Container>
	</MainContainer>
{/if}
