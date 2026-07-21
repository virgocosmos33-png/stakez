<script lang="ts">
	import { stateUi } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';

	import { getContext } from '../context';
	import type { LayoutUiProps } from '../types';
	import { UI_BASE_SIZE } from '../constants';
	import ControlInfoBar, { INFO_BAR_SIZE } from './ControlInfoBar.svelte';
	import ActionPod from './ActionPod.svelte';

	// REVERSIBLE TRIAL: fuse the turbo · SPIN · autoplay cluster into one liquid
	// pod. Set to `false` to fully revert (removes the pod, buttons unchanged).
	const MORPH_BUTTONS = true;

	const props: LayoutUiProps = $props();
	const context = getContext();

	const W = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const H = $derived(context.stateLayoutDerived.mainLayoutStandard().height);

	// ---- compact centred bottom control cluster ----
	// buy | menu | [ balance | bet ▲▼ ] | (turbo) SPIN (autoplay)
	const BAR_SCALE = 0.84;
	// Buy/Spin coins are drawn at UI_BASE_SIZE * 1.2 internally. Render them at the
	// same scale as the badges so they read only slightly bigger than the other
	// HUD components instead of towering over the bar.
	const COIN_SCALE = 0.6;
	const COIN = UI_BASE_SIZE * 1.2 * COIN_SCALE;
	const BUY = COIN;
	const SPIN = COIN;
	const BADGE_SCALE = 0.6;
	const BADGE = UI_BASE_SIZE * BADGE_SCALE;
	const INFO = INFO_BAR_SIZE.width;

	// Base (design) gaps. The row is FITTED to the ornate reel frame's width above.
	// Previously ALL the fit slack grew these outer gaps, which left cavernous
	// space between the controls. Now the fit slack is SPLIT: the gaps keep only
	// GAP_KEEP of it (≈ half the previous gaps) and the ELEMENTS grow to absorb
	// the rest, so the controls read bigger and the gaps roughly halve while the
	// row still spans exactly the gold frame. SIDE_GAP (inside the fused
	// turbo·SPIN·auto pod) scales with the elements so the pod keeps its shape.
	const G1_BASE = 14;
	const G2_BASE = 16;
	const G3_BASE = 22;
	const SIDE_GAP = 10; // clear gap between turbo/auto badges and spin (scales w/ elements)
	const GAP_KEEP = 0.5; // gaps keep this fraction of the fit slack; elements absorb the rest

	// design footprints (before the fit-driven element bump)
	const elementsW = BUY + BADGE + INFO + BADGE + SPIN + BADGE;
	const fixedGapsW = 2 * SIDE_GAP;
	const baseOuterGapsW = G1_BASE + G2_BASE + G3_BASE;
	const naturalTW = elementsW + fixedGapsW + baseOuterGapsW;

	// The frame's outer width is published by the game (BoardFrame) in main-layout
	// design px. Convert it into THIS layout's local (standard) px via the two
	// layout scales, then divide by BAR_SCALE (the row is rendered at BAR_SCALE),
	// giving the target total row width in bar-local coords.
	const frameLocalW = $derived(
		stateUi.boardFrameWidth > 0
			? (stateUi.boardFrameWidth * context.stateLayoutDerived.mainLayout().scale) /
					context.stateLayoutDerived.mainLayoutStandard().scale
			: 0,
	);
	const targetTW = $derived(frameLocalW > 0 ? frameLocalW / BAR_SCALE : naturalTW);
	// gap width if the gaps absorbed the whole fit (the old, cavernous behaviour);
	// never below their design sum (guards very wide screens).
	const fittedGapsW = $derived(Math.max(baseOuterGapsW, targetTW - elementsW - fixedGapsW));
	// gaps keep GAP_KEEP of that (≈ half); the freed width grows the element
	// footprints via ELEM_SCALE so the row still spans the frame exactly.
	const outerGapsW = $derived(fittedGapsW * GAP_KEEP);
	const freedW = $derived(fittedGapsW - outerGapsW);
	const ELEM_SCALE = $derived((elementsW + fixedGapsW + freedW) / (elementsW + fixedGapsW));

	// bumped footprints
	const buyW = $derived(BUY * ELEM_SCALE);
	const spinW = $derived(SPIN * ELEM_SCALE);
	const badgeW = $derived(BADGE * ELEM_SCALE);
	const infoW = $derived(INFO * ELEM_SCALE);
	const sideGap = $derived(SIDE_GAP * ELEM_SCALE);

	// keep the G1:G2:G3 ratio; total = outerGapsW
	const gapScale = $derived(outerGapsW / baseOuterGapsW);
	const G1 = $derived(G1_BASE * gapScale);
	const G2 = $derived(G2_BASE * gapScale);
	const G3 = $derived(G3_BASE * gapScale);
	const spinClusterW = $derived(badgeW + sideGap + spinW + sideGap + badgeW);
	const TW = $derived(buyW + G1 + badgeW + G2 + infoW + G3 + spinClusterW);

	// local coords inside the scaled bar (origin = bar centre)
	const buyC = $derived(-TW / 2 + buyW / 2);
	const menuC = $derived(-TW / 2 + buyW + G1 + badgeW / 2);
	const infoL = $derived(-TW / 2 + buyW + G1 + badgeW + G2);
	const infoC = $derived(infoL + infoW / 2);
	const spinClusterL = $derived(infoL + infoW + G3);
	const turboC = $derived(spinClusterL + badgeW / 2);
	const spinC = $derived(turboC + badgeW / 2 + sideGap + spinW / 2);
	const autoC = $derived(spinC + spinW / 2 + sideGap + badgeW / 2);

	// element render scales (design sub-scale × the fit-driven element bump)
	const coinScale = $derived(COIN_SCALE * ELEM_SCALE);
	const badgeScale = $derived(BADGE_SCALE * ELEM_SCALE);

	// hug the bottom: leave a small pad under the scaled spin coin
	const BOTTOM_PAD = 22;
	const barY = $derived(H - BOTTOM_PAD - (spinW * BAR_SCALE) / 2);
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
		<Container x={buyC} y={0} scale={coinScale}>
			{@render props.buttonBuyBonus({ anchor: 0.5 })}
		</Container>

		<!-- menu badge -->
		<Container x={menuC} y={0} scale={badgeScale}>
			{@render props.buttonMenu({ anchor: 0.5 })}
		</Container>

		<!-- unified balance / bet panel -->
		<Container x={infoC} y={0} scale={ELEM_SCALE}>
			<Container x={-INFO / 2} y={-INFO_BAR_SIZE.height / 2}>
				<ControlInfoBar />
			</Container>
		</Container>

		<!-- morphed pod behind the action cluster (turbo · SPIN · autoplay) -->
		{#if MORPH_BUTTONS}
			<ActionPod
				circles={[
					{ x: turboC, y: 0, r: badgeW / 2 },
					{ x: spinC, y: 0, r: spinW / 2 },
					{ x: autoC, y: 0, r: badgeW / 2 },
				]}
			/>
		{/if}

		<!-- spin first, then side badges on top -->
		<Container x={spinC} y={0} scale={coinScale}>
			{@render props.buttonBet({ anchor: 0.5 })}
		</Container>
		<Container x={turboC} y={0} scale={badgeScale}>
			{@render props.buttonTurbo({ anchor: 0.5 })}
		</Container>
		<Container x={autoC} y={0} scale={badgeScale}>
			{@render props.buttonAutoSpin({ anchor: 0.5 })}
		</Container>

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
			<Container x={menuC} y={0} scale={badgeScale}>
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
