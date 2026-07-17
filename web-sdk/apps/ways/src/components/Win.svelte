<script lang="ts" module>
	export type EmitterEventWin =
		| { type: 'winShow' }
		| { type: 'winHide' }
		| { type: 'winUpdate'; amount: number }
		// press anywhere during a big-win celebration: skip to the next scene
		| { type: 'celebrationSkip' }
		// the MAX WIN continue gate is up: stop catching full-screen presses
		| { type: 'celebrationGate'; waiting: boolean };
</script>

<script lang="ts">
	import { Container } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider, ResponsiveBitmapText } from 'components-pixi';
	import { waitForResolve, waitForTimeout } from 'utils-shared/wait';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { CanvasSizeRectangle, MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnMount, OnHotkey } from 'components-shared';

	import WinCoins from './WinCoins.svelte';
	import WinCelebration from './WinCelebration.svelte';
	import PressToContinue from './PressToContinue.svelte';
	import { SYMBOL_SIZE } from '../game/constants';
	import { getContext } from '../game/context';
	import { getWinCelebration } from '../game/winCelebrationMap';

	const context = getContext();

	let show = $state(false);
	let amount = $state(0);
	let hasWin = $state(false);
	let gateUp = $state(false);
	let oncomplete = $state(() => {});
	let onCountUpComplete = $state(() => {});

	// celebration tier is derived from the win amount in bet multiples
	const celebration = $derived(getWinCelebration(amount));

	context.eventEmitter.subscribeOnMount({
		winShow: () => (show = true),
		winHide: () => {
			show = false;
			hasWin = false;
			gateUp = false;
		},
		winUpdate: async (emitterEvent) => {
			amount = emitterEvent.amount;
			hasWin = true;
			gateUp = false;
			await waitForResolve((resolve) => (oncomplete = resolve));
		},
		celebrationGate: ({ waiting }) => (gateUp = waiting),
	});
</script>

<FadeContainer {show}>
	{#if hasWin}
		{#if celebration.type === 'big'}
			<!-- film-reel takeover: the celebration owns its own staged counter,
				tier triggers, glitch transitions, and the MAX WIN continue gate -->
			<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.94} />
			<MainContainer>
				<!-- centered on the canvas, not the board, so nothing hangs off-screen -->
				<Container
					x={context.stateLayoutDerived.mainLayout().width * 0.5}
					y={context.stateLayoutDerived.mainLayout().height * 0.5}
				>
					<WinCelebration finalAmount={amount} oncomplete={() => oncomplete()} />
				</Container>
			</MainContainer>
			<!-- top-level press catcher: covers the whole screen unaffected by
				the centered container transform; removed while the CONTINUE
				gate is up so the button can take the click -->
			{#if !gateUp}
				<OnHotkey
					hotkey="Space"
					onpress={() => context.eventEmitter.broadcast({ type: 'celebrationSkip' })}
				/>
				<OnPressFullScreen
					onpress={() => context.eventEmitter.broadcast({ type: 'celebrationSkip' })}
				/>
			{/if}
		{:else}
			<WinCountUpProvider {amount} duration={celebration.presentDuration} oncomplete={() => onCountUpComplete()}>
				{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
					<OnMount
						onmount={async () => {
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
							<ResponsiveBitmapText
								anchor={0.5}
								maxWidth={context.stateLayoutDerived.canvasSizes().width /
									context.stateLayoutDerived.mainLayout().scale}
								text={bookEventAmountToCurrencyString(countUpAmount)}
								style={{
									fontFamily: 'gold',
									fontSize: SYMBOL_SIZE,
									align: 'center',
									fontWeight: 'bold',
									letterSpacing: 0,
								}}
							/>
						</Container>
					</MainContainer>

					<WinCoins emit={!countUpCompleted} levelAlias={celebration.alias} />

					<PressToContinue
						onpress={() => (countUpCompleted ? oncomplete() : finishCountUp())}
					/>
				{/snippet}
			</WinCountUpProvider>
		{/if}
	{/if}
</FadeContainer>
