<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicInOut } from 'svelte/easing';

	import { stateUi } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';
	import { waitForResolve } from 'utils-shared/wait';

	import ButtonDrawer from './ButtonDrawer.svelte';
	import ControlInfoBar, { INFO_BAR_SIZE } from './ControlInfoBar.svelte';
	import type { LayoutUiProps } from '../types';
	import { getContext } from '../context';
	import { UI_BASE_SIZE } from '../constants';

	const props: LayoutUiProps = $props();
	const context = getContext();

	const W = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const H = $derived(context.stateLayoutDerived.mainLayoutStandard().height);

	// Fit the bottom control + BET rows to the reel frame's width. BoardFrame
	// publishes the frame's outer width (main-layout design px); convert it into
	// this layout's local (standard) px via the two layout scales. The outermost
	// element centre then sits BTN_HALF inside the frame edge and every horizontal
	// offset scales proportionally (spacing preserved; element sizes/heights are
	// untouched). Falls back to the original design offsets until it's published.
	const frameLocalW = $derived(
		stateUi.boardFrameWidth > 0
			? (stateUi.boardFrameWidth * context.stateLayoutDerived.mainLayout().scale) /
					context.stateLayoutDerived.mainLayoutStandard().scale
			: 0,
	);
	const OUTER_BASE = 430; // original outermost offset (design px from centre)
	const BTN_HALF = 85; // ~half a control button at scale 0.95 (edge inset)
	const rowHalf = $derived(
		frameLocalW > 0 ? Math.max(OUTER_BASE, frameLocalW / 2 - BTN_HALF) : OUTER_BASE,
	);
	const fitX = $derived(rowHalf / OUTER_BASE);

	// Align the unified BALANCE|BET panel EXACTLY to the control-row width: its
	// left edge lands on the buy-bonus coin's left edge and its right edge on the
	// menu badge's right edge. The control row is drawn at CTRL_SCALE with the
	// outermost centres at ±CTRL_OUTER·fitX; the buy coin is 1.2× the base size,
	// the menu badge is 1× — so the two half-widths differ and the span is
	// asymmetric. Uniform-scaling a 500-wide card to that exact span keeps the
	// desktop proportions while matching the buttons' outer edges pixel-for-pixel.
	const CTRL_SCALE = 1.06;
	const CTRL_OUTER = 415;
	const buyHalf = (UI_BASE_SIZE * 1.2 * CTRL_SCALE) / 2;
	const badgeHalf = (UI_BASE_SIZE * CTRL_SCALE) / 2;
	const rowLeftX = $derived(W * 0.5 - CTRL_OUTER * fitX - buyHalf);
	const rowRightX = $derived(W * 0.5 + CTRL_OUTER * fitX + badgeHalf);
	const infoBarScale = $derived((rowRightX - rowLeftX) / INFO_BAR_SIZE.width);
	const infoBarCenterY = $derived(H - 150);

	const DRAWER_Y = {
		unfold: 0,
		fold: 550,
	};
	const drawerTween = new Tween(stateUi.drawerFold ? DRAWER_Y.fold : DRAWER_Y.unfold, {
		easing: cubicInOut,
	});

	const DRAWER_BUTTON_Y = {
		unfold: 0,
		fold: 50,
	};
	const drawerButtonTween = new Tween(
		stateUi.drawerFold ? DRAWER_BUTTON_Y.fold : DRAWER_BUTTON_Y.unfold,
		{
			easing: cubicInOut,
		},
	);

	let drawerButtonFadeComplete = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		drawerButtonShow: async () => {
			if (!stateUi.drawerButtonShow) {
				stateUi.drawerButtonShow = true;
				await waitForResolve((resolve) => (drawerButtonFadeComplete = resolve));
			}
		},
		drawerButtonHide: async () => {
			if (stateUi.drawerButtonShow) {
				stateUi.drawerButtonShow = false;
				await waitForResolve((resolve) => (drawerButtonFadeComplete = resolve));
			}
		},
		drawerUnfold: async () => {
			if (stateUi.drawerFold) {
				drawerButtonTween.set(DRAWER_BUTTON_Y.unfold);
				await drawerTween.set(DRAWER_Y.unfold);
			}
		},
		drawerFold: async () => {
			if (!stateUi.drawerFold) {
				drawerButtonTween.set(DRAWER_BUTTON_Y.fold);
				await drawerTween.set(DRAWER_Y.fold);
			}
		},
	});
</script>

<Container x={20}>
	{@render props.gameName()}
</Container>

<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
	{@render props.logo()}
</Container>

<MainContainer standard alignVertical="bottom">
	<!-- foldable control row: crown | autoSpin | SPIN | turbo | menu.
	     Controls are bumped ~11% bigger and the inner offset is pulled in
	     (235 → 215) so the wide centre gaps roughly halve, while the outer
	     offset (430 → 415) keeps the row spanning the frame without overflow. -->
	<Container y={drawerTween.current}>
		<Container x={W * 0.5 - 415 * fitX} y={H - 360} scale={1.06}>
			{@render props.buttonBuyBonus({ anchor: 0.5 })}
		</Container>

		<Container x={W * 0.5 - 215 * fitX} y={H - 360} scale={1.06}>
			{@render props.buttonAutoSpin({ anchor: 0.5 })}
		</Container>

		<Container x={W * 0.5} y={H - 360} scale={1.06}>
			{@render props.buttonBet({ anchor: 0.5 })}
		</Container>

		<Container x={W * 0.5 + 215 * fitX} y={H - 360} scale={1.06}>
			{@render props.buttonTurbo({ anchor: 0.5 })}
		</Container>

		<Container x={W * 0.5 + 415 * fitX} y={H - 360} scale={1.06}>
			{@render props.buttonMenu({ anchor: 0.5 })}
		</Container>
	</Container>

</MainContainer>

<MainContainer standard alignVertical="bottom">
	<!-- Unified BALANCE | BET · −/+ panel — the SAME ControlInfoBar the desktop
	     layout uses, so mobile wears the identical themed card (stacked
	     BALANCE/BET + steel steppers) instead of the old inline pills. Scaled to
	     span the fitted control-row width and centred under it. Free-spin tally
	     lives in the game's RailPlaque, not this HUD. -->
	<Container
		x={rowLeftX}
		y={infoBarCenterY - (INFO_BAR_SIZE.height / 2) * infoBarScale}
		scale={infoBarScale}
	>
		<ControlInfoBar />
	</Container>

	<!-- drawer (collapse-HUD) button. It only shows during free spins; sit it
		EXACTLY on the menu slot (same x/y/scale as the control-row menu badge) so
		when the HUD is pulled back up it reads as ONE clean dark-steel chevron
		button in the far-right slot — no gold button overlapping the burger with a
		sliver peeking out. When folded it rides up via drawerButtonTween as the
		pull-up tab. -->
	<FadeContainer
		persistent
		show={stateUi.drawerButtonShow}
		oncomplete={drawerButtonFadeComplete}
		y={drawerButtonTween.current}
	>
		<!-- The drawer sits ON the menu slot, so when it's hidden (base game) it
			MUST stop hit-testing or it swallows the menu button's taps (a disabled
			pixi Button is still eventMode:static). eventMode 'none' makes the whole
			subtree ignore interaction so taps fall through to the menu behind;
			'passive' re-enables it during free spins when the drawer is shown. -->
		<Container
			x={W * 0.5 + 415 * fitX}
			y={H - 360}
			scale={1.06}
			eventMode={stateUi.drawerButtonShow ? 'passive' : 'none'}
		>
			<ButtonDrawer disabled={!stateUi.drawerButtonShow} anchor={0.5} />
		</Container>
	</FadeContainer>
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

	<MainContainer standard alignVertical="bottom">
		<Container x={W * 0.5 + 415 * fitX} y={H - 360}>
			<Container y={-190 - 210 * 3}>
				{@render props.buttonPayTable({ anchor: 0.5 })}
			</Container>

			<Container y={-190 - 210 * 2}>
				{@render props.buttonGameRules({ anchor: 0.5 })}
			</Container>

			<Container y={-190 - 210 * 1}>
				{@render props.buttonSettings({ anchor: 0.5 })}
			</Container>

			<Container y={-190}>
				{@render props.buttonSoundSwitch({ anchor: 0.5 })}
			</Container>

			<Container>
				{@render props.buttonMenuClose({ anchor: 0.5 })}
			</Container>
		</Container>
	</MainContainer>
{/if}
