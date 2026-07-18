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
	import { BitmapText, Container, Graphics, Sprite } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider, ResponsiveBitmapText } from 'components-pixi';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { waitForResolve } from 'utils-shared/wait';
	import { CanvasSizeRectangle, MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnMount, OnHotkey } from 'components-shared';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { drawGlassPill } from '../game/glassChrome';
	import WinCoins from './WinCoins.svelte';

	const context = getContext();

	// amethyst palette matching the panel painting
	const VIOLET = 0xb887ff;
	const DEEP_VIOLET = 0x3d1f6e;
	const WHITE = 0xffffff;

	// panel art is 1024x1024; YOU WON / TOTAL WIN are baked into the painting,
	// the empty band between them holds the runtime amount
	const PANEL_RATIO = 1;
	const AMOUNT_Y = 0.03;

	let show = $state(false);
	let amount = $state(0);
	let winLevelData = $state<WinLevelData>();
	let oncomplete = $state(() => {});
	let onCountUpComplete = $state(() => {});

	const scale = new Tween(0);

	context.eventEmitter.subscribeOnMount({
		freeSpinOutroShow: async () => {
			scale.set(0, { duration: 0 });
			show = true;
			await scale.set(1, { duration: 420, easing: backOut });
		},
		freeSpinOutroHide: async () => (show = false),
		freeSpinOutroCountUp: async (emitterEvent) => {
			amount = emitterEvent.amount;
			winLevelData = emitterEvent.winLevelData;
			await waitForResolve((resolve) => (oncomplete = resolve));
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

	const continuePulse = $derived(1 + 0.04 * Math.sin(time * 4.2));
	const amountBreath = $derived(1 + 0.025 * Math.sin(time * 2.6));

	// violet aura swelling behind the amount band
	const drawAmountGlow = (g: import('pixi.js').Graphics, t: number) => {
		const base = SYMBOL_SIZE * (0.5 + 0.09 * Math.sin(t * 2.6));
		for (let i = 4; i >= 1; i--) {
			g.ellipse(0, 0, base * i * 0.62, base * i * 0.3);
			g.fill({ color: i % 2 ? VIOLET : DEEP_VIOLET, alpha: 0.06 });
		}
		g.ellipse(0, 0, base * 0.85, base * 0.4);
		g.fill({ color: WHITE, alpha: 0.04 });
	};

	// amethyst sparkle motes drifting up around the frame
	const MOTES = Array.from({ length: 14 }, (_, i) => ({
		period: 3.4 + rand(i * 7 + 1) * 2.6,
		delay: rand(i * 13 + 5) * 5,
		lane: (rand(i * 17 + 3) - 0.5) * 2,
		size: 1.4 + rand(i * 23 + 2) * 2.4,
		sway: 0.4 + rand(i * 29 + 9) * 0.8,
	}));
	const drawMotes = (g: import('pixi.js').Graphics, t: number) => {
		const halfW = panelWidth * 0.46;
		const halfH = panelHeight * 0.42;
		MOTES.forEach((m, i) => {
			const local = (t + m.delay) / m.period;
			const cycle = local - Math.floor(local);
			const y = halfH - cycle * (halfH * 2);
			const x = m.lane * halfW * 0.5 + Math.sin(t * m.sway + i) * halfW * 0.1;
			const edgeFade = Math.min(cycle / 0.16, (1 - cycle) / 0.24, 1);
			g.circle(x, y, m.size);
			g.fill({ color: i % 4 === 0 ? WHITE : VIOLET, alpha: 0.42 * Math.max(edgeFade, 0) });
		});
	};
</script>

<FadeContainer {show}>
	{#if winLevelData}
		{@const duration = winLevelData.presentDuration}
		<WinCountUpProvider {amount} {duration} oncomplete={() => onCountUpComplete()}>
			{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
				<OnMount onmount={() => startCountUp()} />

				<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.72} />

				<MainContainer>
					<Container
						x={context.stateGameDerived.boardLayout().x}
						y={context.stateGameDerived.boardLayout().y}
						scale={scale.current}
					>
						<!-- ornate amethyst panel; YOU WON / TOTAL WIN baked into the art -->
						<Sprite key="mirrorFsOutro" anchor={0.5} width={panelWidth} height={panelHeight} />

						<Graphics draw={(g) => drawMotes(g, time)} />

						<!-- the counted amount, glowing amethyst in the empty band -->
						<Container y={panelHeight * AMOUNT_Y}>
							<Graphics draw={(g) => drawAmountGlow(g, time)} />
							<Container scale={amountBreath}>
								<ResponsiveBitmapText
									anchor={0.5}
									style={{ fontFamily: 'amethyst', fontSize: SYMBOL_SIZE * 0.72, fontWeight: 'bold' }}
									text={bookEventAmountToCurrencyString(countUpAmount)}
									maxWidth={panelWidth * 0.6}
								/>
							</Container>
						</Container>

						<!-- themed press-anywhere banner matching the HUD scrying-glass chrome -->
						<Container y={panelHeight * 0.53} scale={continuePulse}>
							<Graphics
								eventMode="static"
								cursor="pointer"
								onpointerup={() => (countUpCompleted ? oncomplete() : finishCountUp())}
								draw={(g) => drawGlassPill(g, { width: SYMBOL_SIZE * 4.4, height: SYMBOL_SIZE * 0.52 })}
							/>
							<BitmapText
								anchor={0.5}
								text="PRESS ANYWHERE TO CONTINUE"
								eventMode="none"
								style={{ fontFamily: 'amethyst', fontSize: SYMBOL_SIZE * 0.19, letterSpacing: 2 }}
							/>
						</Container>
					</Container>
				</MainContainer>

				<WinCoins emit={!countUpCompleted} levelAlias={winLevelData?.alias} />

				<OnHotkey
					hotkey="Space"
					onpress={() => (countUpCompleted ? oncomplete() : finishCountUp())}
				/>
				<OnPressFullScreen onpress={() => (countUpCompleted ? oncomplete() : finishCountUp())} />
			{/snippet}
		</WinCountUpProvider>
	{/if}
</FadeContainer>
