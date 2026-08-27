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
	import { FadeContainer, WinCountUpProvider } from 'components-pixi';
	import { waitForResolveOrTimeout, waitForTimeout } from 'utils-shared/wait';
	import { CanvasSizeRectangle, MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnMount, OnHotkey } from 'components-shared';

	import WinCoins from './WinCoins.svelte';
	import WinCelebration from './WinCelebration.svelte';
	import WinChip from './WinChip.svelte';
	import PressToContinue from './PressToContinue.svelte';
	import { getContext } from '../game/context';
	import { celebrationRollupMs, getWinCelebration } from '../game/winCelebrationMap';

	const context = getContext();

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
			const CELEB_CONTINUE_PAD_MS = 20_000;
			const safetyMs =
				tier.type === 'big'
					? celebrationRollupMs(emitterEvent.amount) + CELEB_CONTINUE_PAD_MS
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
			<!-- western hero-plate takeover: WinCelebration listens to stopButtonClick
				(TapToSkip Space / reel tap / HUD stop / full-screen press below) -->
			<!-- not a full black-out: the graveyard and reels stay faintly legible
				behind the takeover instead of cutting to a void -->
			<CanvasSizeRectangle backgroundColor={0x07060a} backgroundAlpha={0.88} />
			<!-- Bounty payout raining behind the panel. The big tiers used to get no
				scatter at all — only the small-win branch emitted — so the whole
				coin-and-cartridge layer was missing from every celebration. It stops
				when the max-win CONTINUE gate takes over. -->
			<WinCoins emit={!gateUp} levelAlias={celebration.alias} />
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
							<WinChip amount={countUpAmount} {ways} />
						</Container>
					</MainContainer>

					<WinCoins emit={!countUpCompleted} levelAlias={celebration.alias} />

					<PressToContinue />
				{/snippet}
			</WinCountUpProvider>
		{/if}
	{/if}
</FadeContainer>
