<script lang="ts" module>
	export type EmitterEventBonusLevelBanner = {
		type: 'bonusLevelShow';
		level: 1 | 2 | 3;
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { Rectangle as HitRectangle } from 'pixi.js';
	import { CanvasSizeRectangle, MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnHotkey } from 'components-shared';
	import { Container, Sprite, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	// Same chrome language as paytable / buy-confirm (blank plates + labels).
	const BRAND_FAMILY = 'Impact, "Arial Black", "Arial Narrow", Arial, sans-serif';
	const BRAND_INK = 0x0a0a0a;
	const BRAND_COPY = 0xece8df;

	// panel art is 1536x1024; the level title is baked into each painting
	const LEVEL_PANELS = {
		1: 'mirrorIntroSeance',
		2: 'mirrorIntroOtherside',
		3: 'mirrorIntroBloodmoon',
	} as const;
	// Mechanic copy from config/design — split title vs body for brand plates.
	// Do not invent new rules text.
	const LEVEL_COPY = {
		1: {
			title: 'THE INTAKE',
			body: 'INCREASED CHANCE TO LAND OBSERVATION PANE',
		},
		2: {
			title: 'HER SIDE',
			body: 'FRACTURES SURVIVE ONE EXTRA SPIN\nAND STACK WHEN HIT AGAIN.',
		},
		3: {
			title: 'WHITEOUT',
			body: 'FRACTURES ARE STICKY AND STACK ENDLESSLY,\nUNTIL THE END OF HER SIDE.',
		},
	} as const;
	const PANEL_RATIO = 1024 / 1536;
	const CTA_RATIO = 282 / 780;
	const SECTION_RATIO = 150 / 1100;

	let show = $state(false);
	let level = $state<1 | 2 | 3>(1);
	const scale = new Tween(0);
	const alpha = new Tween(1);
	let oncontinue = $state(() => {});

	const dismiss = () => {
		if (!show) return;
		// Resolve the bonusLevelShow await directly. Also ping the shared bus so
		// HUD stop / Space stay consistent — handler is idempotent once cleared.
		oncontinue();
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	// FS intro panel — dismiss via the shared stopButtonClick bus
	// (TapToSkip Space / full-screen tap / HUD stop / CONTINUE plate).
	// Storybook Action runs playBet while xstate stays idle (TapToSkip off),
	// and the iframe often steals clicks — never wait forever.
	const CONTINUE_SAFETY_MS = 12_000;

	context.eventEmitter.subscribeOnMount({
		bonusLevelShow: async (emitterEvent) => {
			level = emitterEvent.level;
			alpha.set(1, { duration: 0 });
			scale.set(0, { duration: 0 });
			show = true;
			let settled = false;
			const waited = new Promise<void>((resolve) => {
				oncontinue = () => {
					if (settled) return;
					settled = true;
					resolve();
				};
			});
			const safety = window.setTimeout(() => {
				console.warn('[BonusLevelBanner] CONTINUE not pressed — forcing resolve');
				oncontinue();
			}, CONTINUE_SAFETY_MS);
			// don't await scale — tap can dismiss during the pop-in
			scale.set(1, { duration: 350, easing: backOut });
			try {
				await waited;
			} finally {
				window.clearTimeout(safety);
			}
			await alpha.set(0, { duration: 280, easing: cubicOut });
			show = false;
			oncontinue = () => {};
		},
		stopButtonClick: () => {
			if (!show) return;
			oncontinue();
		},
	});

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
	const continuePulse = $derived(1 + 0.04 * Math.sin(time * 4.2));

	const panelWidth = $derived(context.stateGameDerived.boardLayout().width * 0.98);
	const panelHeight = $derived(panelWidth * PANEL_RATIO);
	const copy = $derived(LEVEL_COPY[level]);

	const sectionW = $derived(Math.min(panelWidth * 0.72, SYMBOL_SIZE * 5.2));
	const sectionH = $derived(sectionW * SECTION_RATIO);
	const ctaW = $derived(Math.min(panelWidth * 0.42, SYMBOL_SIZE * 3.1));
	const ctaH = $derived(ctaW * CTA_RATIO);
</script>

<!-- pixi appends children on mount, so the dim and the panel must mount
	together (dim first) or the dim lands on top of the panel -->
{#if show}
	<Container alpha={alpha.current}>
		<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.78} />
	</Container>
	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
			scale={scale.current}
			alpha={alpha.current}
		>
			<Sprite key={LEVEL_PANELS[level]} anchor={0.5} width={panelWidth} height={panelHeight} />

			<!-- Level name on blank magenta section plate (paytable / SPECIAL SYMBOLS family).
				Sits high on the painting so the plate never crowds the body copy. -->
			<Container y={-panelHeight * 0.28}>
				<Sprite
					key="uiSectionMagentaWide"
					anchor={0.5}
					width={sectionW}
					height={sectionH}
					eventMode="none"
				/>
				<Text
					anchor={0.5}
					text={copy.title}
					eventMode="none"
					style={{
						fontFamily: BRAND_FAMILY,
						fontWeight: '800',
						fontSize: sectionH * 0.52,
						fill: BRAND_INK,
						align: 'center',
						letterSpacing: 2,
					}}
				/>
			</Container>

			<!-- Mechanic body — pale copy over a bright painting, so it carries a thin
				black outline to stay legible against the blown-out cell walls -->
			<Text
				anchor={0.5}
				y={-panelHeight * 0.02}
				text={copy.body}
				eventMode="none"
				style={{
					fontFamily: BRAND_FAMILY,
					fontWeight: '700',
					fontSize: SYMBOL_SIZE * 0.145,
					fill: BRAND_COPY,
					align: 'center',
					lineHeight: SYMBOL_SIZE * 0.2,
					letterSpacing: 1,
					stroke: { color: 0x000000, width: SYMBOL_SIZE * 0.022 },
				}}
			/>

			<!-- Magenta CTA plate (same asset as buy-confirm CONFIRM) -->
			<Container
				y={panelHeight * 0.3}
				scale={continuePulse}
				eventMode="static"
				cursor="pointer"
				hitArea={new HitRectangle(-ctaW / 2, -ctaH / 2, ctaW, ctaH)}
				onpointerup={dismiss}
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
						fontSize: ctaH * 0.42,
						fill: BRAND_INK,
						align: 'center',
						letterSpacing: 3,
					}}
				/>
			</Container>

			<Container y={panelHeight * 0.42} alpha={0.7 + 0.15 * Math.sin(time * 3.2)}>
				<Text
					anchor={0.5}
					text="TAP TO SKIP"
					eventMode="none"
					style={{
						fontFamily: BRAND_FAMILY,
						fontWeight: '700',
						fontSize: SYMBOL_SIZE * 0.13,
						fill: BRAND_COPY,
						align: 'center',
						letterSpacing: 3,
						stroke: { color: 0x000000, width: SYMBOL_SIZE * 0.02 },
					}}
				/>
			</Container>
		</Container>
	</MainContainer>
	<!-- overlay covers reel hit-area — same dismiss path as CONTINUE.
	     Space works even when Storybook Action left xstate idle (TapToSkip off). -->
	<OnPressFullScreen onpress={dismiss} />
	<OnHotkey hotkey="Space" onpress={dismiss} />
{/if}
