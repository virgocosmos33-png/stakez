<script lang="ts" module>
	import type { WinLevelData } from '../game/winLevelMap';

	export type EmitterEventFreeSpinOutro =
		| { type: 'freeSpinOutroShow' }
		| { type: 'freeSpinOutroHide' }
		| { type: 'freeSpinOutroCountUp'; amount: number; winLevelData: WinLevelData };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { Container, Graphics, Sprite, Text } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider, ResponsiveBitmapText } from 'components-pixi';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { waitForResolveOrTimeout, waitForTimeout } from 'utils-shared/wait';
	import { CanvasSizeRectangle, MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnMount, OnHotkey } from 'components-shared';
	import { Rectangle as HitRectangle } from 'pixi.js';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { winFontFamily, winFontSize, winFontTint } from '../game/winFont';
	import WinCoins from './WinCoins.svelte';

	const context = getContext();

	// clinical white/silver — NOT amethyst séance palette
	const BONE = 0xf4f1ec;
	const STEEL = 0x8a8680;
	const WHITE = 0xffffff;
	const AMOUNT_FAMILY = winFontFamily();
	const AMOUNT_TINT = winFontTint();

	// Same chrome language as paytable / buy-confirm (blank plates + labels).
	const BRAND_FAMILY = 'Impact, "Arial Black", "Arial Narrow", Arial, sans-serif';
	const BRAND_INK = 0x0a0a0a;

	// panel art is 1024x1024; YOU WON / TOTAL WIN are baked into the painting,
	// the empty band between them holds the runtime amount
	const PANEL_RATIO = 1;
	const AMOUNT_Y = 0.03;
	const CTA_RATIO = 282 / 780;

	let show = $state(false);
	let amount = $state(0);
	let winLevelData = $state<WinLevelData>();
	let oncomplete = $state(() => {});
	let onCountUpComplete = $state(() => {});
	// skip action wired from WinCountUpProvider snippet → stopButtonClick bus
	let outroSkip = $state(() => {});

	const scale = new Tween(0);

	const broadcastSkip = () => {
		if (!show) return;
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	context.eventEmitter.subscribeOnMount({
		freeSpinOutroShow: async () => {
			scale.set(0, { duration: 0 });
			show = true;
			await scale.set(1, { duration: 420, easing: backOut });
		},
		freeSpinOutroHide: async () => {
			show = false;
			outroSkip = () => {};
		},
		freeSpinOutroCountUp: async (emitterEvent) => {
			amount = emitterEvent.amount;
			winLevelData = emitterEvent.winLevelData;
			const present = emitterEvent.winLevelData?.presentDuration ?? 3000;
			await waitForResolveOrTimeout(
				(resolve) => (oncomplete = resolve),
				present + 12_000,
				'FreeSpinOutro.freeSpinOutroCountUp',
			);
		},
		// Same bus as TapToSkip / HUD stop — finish count-up or dismiss
		stopButtonClick: () => {
			if (!show || !winLevelData) return;
			outroSkip();
		},
	});

	// per-frame clock for glow/motes/pulse (same idiom as FreeSpinIntro)
	let time = $state(0);
	$effect(() => {
		if (!show) return;
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const panelWidth = $derived(context.stateGameDerived.boardLayout().width * 0.94);
	const panelHeight = $derived(panelWidth * PANEL_RATIO);
	const ctaW = $derived(Math.min(panelWidth * 0.55, SYMBOL_SIZE * 4.2));
	const ctaH = $derived(ctaW * CTA_RATIO);

	const continuePulse = $derived(1 + 0.04 * Math.sin(time * 4.2));
	const amountBreath = $derived(1 + 0.025 * Math.sin(time * 2.6));

	// fluorescent clinical bloom behind the amount (strobe pulse, not violet aura)
	const drawAmountGlow = (g: import('pixi.js').Graphics, t: number) => {
		const flicker = 0.7 + 0.3 * Math.sin(t * 14);
		const base = SYMBOL_SIZE * (0.45 + 0.06 * Math.sin(t * 3.1));
		for (let i = 4; i >= 1; i--) {
			g.ellipse(0, 0, base * i * 0.55, base * i * 0.22);
			g.fill({ color: i % 2 ? BONE : STEEL, alpha: 0.05 * flicker });
		}
		g.ellipse(0, 0, base * 0.7, base * 0.28);
		g.fill({ color: WHITE, alpha: 0.06 * flicker });
	};

	// falling ceramic dust (not rising amethyst sparkles)
	const MOTES = Array.from({ length: 18 }, (_, i) => ({
		period: 2.2 + rand(i * 7 + 1) * 1.8,
		delay: rand(i * 13 + 5) * 4,
		lane: (rand(i * 17 + 3) - 0.5) * 2,
		size: 1.2 + rand(i * 23 + 2) * 2.8,
		sway: 0.5 + rand(i * 29 + 9) * 1.1,
	}));
	const drawMotes = (g: import('pixi.js').Graphics, t: number) => {
		const halfW = panelWidth * 0.46;
		const halfH = panelHeight * 0.42;
		MOTES.forEach((m, i) => {
			const local = (t + m.delay) / m.period;
			const cycle = local - Math.floor(local);
			const y = -halfH + cycle * (halfH * 2);
			const x = m.lane * halfW * 0.5 + Math.sin(t * m.sway + i) * halfW * 0.08;
			const edgeFade = Math.min(cycle / 0.12, (1 - cycle) / 0.2, 1);
			g.circle(x, y, m.size);
			g.fill({ color: i % 3 === 0 ? WHITE : BONE, alpha: 0.4 * Math.max(edgeFade, 0) });
		});
	};
</script>

<FadeContainer {show}>
	{#if winLevelData}
		{@const duration = winLevelData.presentDuration}
		<WinCountUpProvider {amount} {duration} oncomplete={() => onCountUpComplete()}>
			{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
				<!-- Auto-dismiss after count-up (like base Win) so Storybook Action
					cannot hang when CONTINUE clicks never reach the canvas. Wire the skip
					bus here (an effect), NOT a template expression — mutating $state during
					render throws state_unsafe_mutation and hangs the outro. -->
				<OnMount
					onmount={async () => {
						outroSkip = () => (countUpCompleted ? oncomplete() : finishCountUp());
						await startCountUp();
						await waitForTimeout(400);
						oncomplete();
					}}
				/>

				<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.72} />

				<MainContainer>
					<Container
						x={context.stateGameDerived.boardLayout().x}
						y={context.stateGameDerived.boardLayout().y}
						scale={scale.current}
					>
						<!-- YOU WON panel; amount = config.fx.winAmountFont (clinical face) -->
						<Sprite key="mirrorFsOutro" anchor={0.5} width={panelWidth} height={panelHeight} />

						<Graphics draw={(g) => drawMotes(g, time)} />

						<Container y={panelHeight * AMOUNT_Y}>
							<Graphics draw={(g) => drawAmountGlow(g, time)} />
							<Container scale={amountBreath}>
								<ResponsiveBitmapText
									anchor={0.5}
									tint={AMOUNT_TINT}
									style={{ fontFamily: AMOUNT_FAMILY, fontSize: winFontSize(0.72), fontWeight: 'bold' }}
									text={bookEventAmountToCurrencyString(countUpAmount)}
									maxWidth={panelWidth * 0.6}
								/>
							</Container>
						</Container>

						<!-- Magenta CTA plate (buy-confirm CONFIRM family) — no glass capsule -->
						<Container
							y={panelHeight * 0.53}
							scale={continuePulse}
							eventMode="static"
							cursor="pointer"
							hitArea={new HitRectangle(-ctaW / 2, -ctaH / 2, ctaW, ctaH)}
							onpointerup={broadcastSkip}
						>
							<Sprite
								key="uiCtaActivate"
								anchor={0.5}
								width={ctaW}
								height={ctaH}
								eventMode="none"
							/>
							<Text
								anchor={0.5}
								text="CONTINUE"
								eventMode="none"
								style={{
									fontFamily: BRAND_FAMILY,
									fontWeight: '800',
									fontSize: ctaH * 0.38,
									fill: BRAND_INK,
									align: 'center',
									letterSpacing: 3,
								}}
							/>
						</Container>
					</Container>
				</MainContainer>

				<WinCoins emit={!countUpCompleted} levelAlias={winLevelData?.alias} />

				<!-- Space + full-screen → stopButtonClick (works with idle Storybook Action) -->
				<OnPressFullScreen onpress={broadcastSkip} />
				<OnHotkey hotkey="Space" onpress={broadcastSkip} />
			{/snippet}
		</WinCountUpProvider>
	{/if}
</FadeContainer>
