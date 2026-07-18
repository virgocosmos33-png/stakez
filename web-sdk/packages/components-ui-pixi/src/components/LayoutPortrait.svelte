<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicInOut } from 'svelte/easing';

	import { stateUi, stateBet } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { FadeContainer } from 'components-pixi';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle } from 'pixi-svelte';
	import { waitForResolve } from 'utils-shared/wait';

	import LabelFreeSpinCounter from './LabelFreeSpinCounter.svelte';
	import ButtonDrawer from './ButtonDrawer.svelte';
	import type { LayoutUiProps } from '../types';
	import { getContext } from '../context';

	const props: LayoutUiProps = $props();
	const context = getContext();

	const W = $derived(context.stateLayoutDerived.mainLayoutStandard().width);
	const H = $derived(context.stateLayoutDerived.mainLayoutStandard().height);

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
	<!-- foldable control row: crown | autoSpin | SPIN | turbo | menu -->
	<Container y={drawerTween.current}>
		<Container x={W * 0.5 - 430} y={H - 360} scale={0.95}>
			{@render props.buttonBuyBonus({ anchor: 0.5 })}
		</Container>

		<Container x={W * 0.5 - 235} y={H - 360} scale={0.95}>
			{@render props.buttonAutoSpin({ anchor: 0.5 })}
		</Container>

		<Container x={W * 0.5} y={H - 360} scale={1.2}>
			{@render props.buttonBet({ anchor: 0.5 })}
		</Container>

		<Container x={W * 0.5 + 235} y={H - 360} scale={0.95}>
			{@render props.buttonTurbo({ anchor: 0.5 })}
		</Container>

		<Container x={W * 0.5 + 430} y={H - 360} scale={0.95}>
			{@render props.buttonMenu({ anchor: 0.5 })}
		</Container>
	</Container>

	<Container y={Math.min(drawerTween.current, 350)}>
		{#if stateBet.winBookEventAmount > 0}
			<Container x={W * 0.5} y={H - 620}>
				{@render props.amountWin({ stacked: true })}
			</Container>
		{/if}
	</Container>
</MainContainer>

<MainContainer standard alignVertical="bottom">
	<!-- always-visible pills at the bottom corners -->
	{#if stateUi.freeSpinCounterShow}
		<Container x={W * 0.5} y={H - 140}>
			<LabelFreeSpinCounter stacked />
		</Container>
	{:else}
		<Container x={W * 0.5 - 250} y={H - 150} scale={0.95}>
			{@render props.amountBet({ stacked: true })}
		</Container>

		<Container x={W * 0.5 + 250} y={H - 150} scale={0.95}>
			{@render props.amountBalance({ stacked: true })}
		</Container>
	{/if}

	<!-- drawer button -->
	<FadeContainer
		persistent
		show={stateUi.drawerButtonShow}
		oncomplete={drawerButtonFadeComplete}
		y={drawerButtonTween.current}
	>
		<Container x={W * 0.5 + 430} y={H - 300}>
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
		<Container x={W * 0.5 + 430} y={H - 360}>
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
