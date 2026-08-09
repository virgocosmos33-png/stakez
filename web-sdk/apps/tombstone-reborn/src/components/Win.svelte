<script lang="ts" module>
	export type EmitterEventWin =
		| { type: 'winShow' }
		| { type: 'winHide' }
		| { type: 'winUpdate'; amount: number; ways?: number }
		// MAX WIN continue gate is up — remove full-screen catcher so CONTINUE can receive clicks
		| { type: 'celebrationGate'; waiting: boolean };
</script>

<script lang="ts">
	import { Container } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider, ResponsiveBitmapText } from 'components-pixi';
	import { waitForResolveOrTimeout, waitForTimeout } from 'utils-shared/wait';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { CanvasSizeRectangle, MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnMount, OnHotkey } from 'components-shared';

	import WinCoins from './WinCoins.svelte';
	import WinCelebration from './WinCelebration.svelte';
	import PressToContinue from './PressToContinue.svelte';
	import { getContext } from '../game/context';
	import { getWinCelebration } from '../game/winCelebrationMap';
	import { winFontFamily, winFontSize, winFontTint } from '../game/winFont';

	const context = getContext();

	// Over-board win amount: config.fx.winAmountFont (panel FX tab + DramaStudioMCP).
	const WIN_FONT_FAMILY = winFontFamily();
	const WIN_FONT_TINT = winFontTint();
	const WIN_FONT_SIZE = winFontSize(1);

	let show = $state(false);
	let amount = $state(0);
	// how many ways paid this spin — sits above the money as it counts up
	let ways = $state(0);
	let hasWin = $state(false);
	let gateUp = $state(false);
	let oncomplete = $state(() => {});
	let onCountUpComplete = $state(() => {});
	// small-win skip action (finish count-up or dismiss) — driven by stopButtonClick
	let smallWinSkip = $state(() => {});

	// celebration tier is derived from the win amount in bet multiples
	const celebration = $derived(getWinCelebration(amount));

	const broadcastSkip = () => {
		// Always fire while a big-win presentation is mounted — do NOT gate on
		// isIdle() (xstate can flicker idle and silently kill tap-to-skip).
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	context.eventEmitter.subscribeOnMount({
		winShow: () => (show = true),
		winHide: () => {
			show = false;
			hasWin = false;
			ways = 0;
			gateUp = false;
			smallWinSkip = () => {};
		},
		winUpdate: async (emitterEvent) => {
			amount = emitterEvent.amount;
			ways = emitterEvent.ways ?? 0;
			hasWin = true;
			gateUp = false;
			const tier = getWinCelebration(emitterEvent.amount);
			// Big/MAX wait on CONTINUE; Storybook iframe often steals those clicks.
			const safetyMs =
				tier.type === 'big'
					? Math.max(tier.presentDuration + 12_000, 28_000)
					: tier.presentDuration + 5_000;
			await waitForResolveOrTimeout(
				(resolve) => (oncomplete = resolve),
				safetyMs,
				'Win.winUpdate',
			);
		},
		celebrationGate: ({ waiting }) => (gateUp = waiting),
		// small wins only — big wins are handled in WinCelebration on the same bus
		stopButtonClick: () => {
			if (!hasWin || celebration.type === 'big') return;
			smallWinSkip();
		},
	});
</script>

<FadeContainer {show}>
	{#if hasWin}
		{#if celebration.type === 'big'}
			<!-- film-reel takeover: WinCelebration listens to stopButtonClick
				(TapToSkip Space / reel tap / HUD stop / full-screen press below) -->
			<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.94} />
			<MainContainer>
				<!-- centered on the canvas, not the board, so nothing hangs off-screen -->
				<Container
					x={context.stateLayoutDerived.mainLayout().width * 0.5}
					y={context.stateLayoutDerived.mainLayout().height * 0.5}
				>
					<WinCelebration finalAmount={amount} {ways} oncomplete={() => oncomplete()} />
				</Container>
			</MainContainer>
			<!-- Always keep Space + full-screen skip. MAX CONTINUE also listens on
				stopButtonClick now; iframe click-steal must not wedge Action. -->
			<OnHotkey hotkey="Space" onpress={broadcastSkip} />
			{#if !gateUp}
				<OnPressFullScreen onpress={broadcastSkip} />
			{/if}
		{:else}
			<WinCountUpProvider {amount} duration={celebration.presentDuration} oncomplete={() => onCountUpComplete()}>
				{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
					<!-- Wire the skip bus from inside an effect (onmount), NOT a template
						expression: mutating $state during render throws state_unsafe_mutation,
						which aborts the count-up mount and hangs the whole book at this win. -->
					<OnMount
						onmount={async () => {
							smallWinSkip = () => (countUpCompleted ? oncomplete() : finishCountUp());
							await startCountUp();
							await waitForTimeout(300);
							oncomplete();
						}}
					/>

					<MainContainer>
						<Container
							x={context.stateGameDerived.boardLayout().x}
							y={context.stateGameDerived.boardLayout().y}
						>
							<!-- how many ways paid, riding above the money as it counts -->
							{#if ways > 0}
								<Container y={-WIN_FONT_SIZE * 0.72}>
									<ResponsiveBitmapText
										anchor={0.5}
										maxWidth={context.stateLayoutDerived.canvasSizes().width /
											context.stateLayoutDerived.mainLayout().scale}
										text={ways === 1 ? '1 WAY' : `${ways} WAYS`}
										tint={WIN_FONT_TINT}
										style={{
											fontFamily: WIN_FONT_FAMILY,
											fontSize: WIN_FONT_SIZE * 0.36,
											align: 'center',
											fontWeight: 'bold',
											letterSpacing: 2,
										}}
									/>
								</Container>
							{/if}
							<ResponsiveBitmapText
								anchor={0.5}
								maxWidth={context.stateLayoutDerived.canvasSizes().width /
									context.stateLayoutDerived.mainLayout().scale}
								text={bookEventAmountToCurrencyString(countUpAmount)}
								tint={WIN_FONT_TINT}
								style={{
									fontFamily: WIN_FONT_FAMILY,
									fontSize: WIN_FONT_SIZE,
									align: 'center',
									fontWeight: 'bold',
									letterSpacing: 0,
								}}
							/>
						</Container>
					</MainContainer>

					<WinCoins emit={!countUpCompleted} levelAlias={celebration.alias} />

					<PressToContinue />
				{/snippet}
			</WinCountUpProvider>
		{/if}
	{/if}
</FadeContainer>
