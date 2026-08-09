<script lang="ts" module>
	export type EmitterEventFreeSpinIntro =
		| { type: 'freeSpinIntroShow'; level?: 1 | 2 | 3 }
		| { type: 'freeSpinIntroHide' }
		| { type: 'freeSpinIntroUpdate'; totalFreeSpins: number };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { CanvasSizeRectangle, MainContainer, OnPressFullScreen } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { BitmapText, Container, Graphics, Sprite, Text } from 'pixi-svelte';
	import { waitForResolveOrTimeout } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { winFontFamily, winFontSize, winFontTint } from '../game/winFont';

	const context = getContext();

	const WHITE = 0xffffff;
	const AMOUNT_FAMILY = winFontFamily();
	const AMOUNT_TINT = winFontTint();

	// Same chrome language as paytable / buy-confirm (blank plates + labels).
	const BRAND_FAMILY = 'Impact, "Arial Black", "Arial Narrow", Arial, sans-serif';
	const BRAND_INK = 0x0a0a0a;
	const BRAND_COPY = 0xece8df;

	// clinical fluorescent / sparse-blood palette per White Room bonus level
	const LEVEL_THEME = {
		1: { panel: 'mirrorFsIntro', title: 'THE INTAKE', glow: 0xf4f1ec, glowDeep: 0x5c5854 },
		2: { panel: 'mirrorFsIntroOtherside', title: 'HER SIDE', glow: 0xc8c4bc, glowDeep: 0x3a3632 },
		3: { panel: 'mirrorFsIntroBloodmoon', title: 'WHITEOUT', glow: 0xe8d4d2, glowDeep: 0x6b2a28 },
	} as const;

	// mirror centrepiece art is 1024x1024; the dark glass oval sits at centre
	const PANEL_RATIO = 1;
	const CTA_RATIO = 282 / 780;
	const SECTION_RATIO = 150 / 1100;

	let show = $state(false);
	let level = $state<1 | 2 | 3>(1);
	let freeSpinsFromEvent = $state(0);
	let oncomplete = $state(() => {});

	const theme = $derived(LEVEL_THEME[level]);

	const scale = new Tween(0);
	const reveal = new Tween(0);

	const broadcastSkip = () => {
		if (!show) return;
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	context.eventEmitter.subscribeOnMount({
		freeSpinIntroShow: async (emitterEvent) => {
			level = emitterEvent.level ?? 1;
			reveal.set(0, { duration: 0 });
			scale.set(0, { duration: 0 });
			show = true;
			await scale.set(1, { duration: 420, easing: backOut });
		},
		freeSpinIntroHide: () => (show = false),
		freeSpinIntroUpdate: async (emitterEvent) => {
			freeSpinsFromEvent = emitterEvent.totalFreeSpins;
			// the count materialises in the glass like an apparition
			reveal.set(1, { duration: 720, easing: cubicOut });
			await waitForResolveOrTimeout(
				(resolve) => (oncomplete = resolve),
				12_000,
				'FreeSpinIntro.freeSpinIntroUpdate',
			);
		},
		// Same bus as TapToSkip — snap reveal / dismiss (if this panel is remounted)
		stopButtonClick: () => {
			if (!show) return;
			if (reveal.current < 1) {
				reveal.set(1, { duration: 0 });
				return;
			}
			oncomplete();
		},
	});

	// per-frame clock drives the candle/mist/apparition FX (Anticipation idiom)
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

	const panelWidth = $derived(context.stateGameDerived.boardLayout().width * 0.92);
	const panelHeight = $derived(panelWidth * PANEL_RATIO);

	const continuePulse = $derived(1 + 0.04 * Math.sin(time * 4.2));
	const numberBreath = $derived(1 + 0.03 * Math.sin(time * 2.4));
	const numberScale = $derived((0.45 + 0.55 * reveal.current) * numberBreath);

	const sectionW = $derived(Math.min(panelWidth * 0.62, SYMBOL_SIZE * 4.6));
	const sectionH = $derived(sectionW * SECTION_RATIO);
	const ctaW = $derived(Math.min(panelWidth * 0.4, SYMBOL_SIZE * 2.9));
	const ctaH = $derived(ctaW * CTA_RATIO);

	// spectral glow that swells behind the count as it resolves
	const drawApparitionGlow = (g: import('pixi.js').Graphics, t: number, r: number) => {
		if (r <= 0.01) return;
		const base = SYMBOL_SIZE * (0.55 + 0.12 * Math.sin(t * 2.4));
		for (let i = 4; i >= 1; i--) {
			const rad = base * i * 0.5;
			g.ellipse(0, 0, rad * 1.15, rad);
			g.fill({ color: i % 2 ? theme.glow : theme.glowDeep, alpha: 0.09 * r });
		}
		g.ellipse(0, 0, base * 0.7, base * 0.62);
		g.fill({ color: WHITE, alpha: 0.06 * r });
	};

	// drifting séance motes rising through the glass
	const MOTES = Array.from({ length: 16 }, (_, i) => ({
		period: 3.2 + rand(i * 7 + 1) * 2.4,
		delay: rand(i * 13 + 5) * 5,
		lane: (rand(i * 17 + 3) - 0.5) * 1.4,
		size: 1.4 + rand(i * 23 + 2) * 2.6,
		sway: 0.4 + rand(i * 29 + 9) * 0.9,
	}));
	const drawMotes = (g: import('pixi.js').Graphics, t: number) => {
		const halfW = panelWidth * 0.3;
		const halfH = panelHeight * 0.34;
		MOTES.forEach((m, i) => {
			const local = (t + m.delay) / m.period;
			const cycle = local - Math.floor(local);
			const y = halfH - cycle * (halfH * 2);
			const x = m.lane * halfW + Math.sin(t * m.sway + i) * halfW * 0.12;
			const edgeFade = Math.min(cycle / 0.16, (1 - cycle) / 0.24, 1);
			g.circle(x, y, m.size);
			g.fill({ color: i % 4 === 0 ? WHITE : theme.glow, alpha: 0.4 * Math.max(edgeFade, 0) });
		});
	};

	// slow specular sheen sweeping across the glass
	const drawSheen = (g: import('pixi.js').Graphics, t: number) => {
		const sweep = Math.sin(t * 0.55);
		const x = sweep * panelWidth * 0.16;
		g.ellipse(x, -panelHeight * 0.02, panelWidth * 0.1, panelHeight * 0.32);
		g.fill({ color: WHITE, alpha: 0.035 + 0.025 * (0.5 + 0.5 * Math.cos(t * 0.55)) });
	};
</script>

<FadeContainer {show}>
	<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.72} />

	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
			scale={scale.current}
		>
			<!-- ornate haunted-mirror centrepiece, one painting per bonus level -->
			<Sprite key={theme.panel} anchor={0.5} width={panelWidth} height={panelHeight} />

			<!-- spectral light living in the glass -->
			<Graphics y={-panelHeight * 0.02} draw={(g) => drawSheen(g, time)} />
			<Graphics draw={(g) => drawMotes(g, time)} />

			<!-- Level title on blank magenta section plate -->
			<Container y={-panelHeight * 0.42}>
				<Sprite
					key="uiSectionMagentaWide"
					anchor={0.5}
					width={sectionW}
					height={sectionH}
					eventMode="none"
				/>
				<Text
					anchor={0.5}
					text={theme.title}
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

			<!-- the awarded count, materialising as an apparition inside the glass -->
			<Container y={-panelHeight * 0.01}>
				<Graphics draw={(g) => drawApparitionGlow(g, time, reveal.current)} />
				<Container scale={numberScale} alpha={reveal.current}>
					<!-- config.fx.winAmountFont (clinical face — not ghost/silver template) -->
					<BitmapText
						anchor={0.5}
						text={freeSpinsFromEvent}
						tint={AMOUNT_TINT}
						style={{ fontFamily: AMOUNT_FAMILY, fontSize: winFontSize(1.15), fontWeight: 'bold' }}
					/>
				</Container>
			</Container>

			<Container y={panelHeight * 0.19} alpha={reveal.current}>
				<Text
					anchor={0.5}
					text="HER SIDE SPINS"
					eventMode="none"
					style={{
						fontFamily: BRAND_FAMILY,
						fontWeight: '800',
						fontSize: SYMBOL_SIZE * 0.28,
						fill: BRAND_COPY,
						align: 'center',
						letterSpacing: 3,
					}}
				/>
			</Container>

			<!-- Magenta CTA plate (buy-confirm CONFIRM family) -->
			<Container
				y={panelHeight * 0.58}
				scale={continuePulse}
				eventMode="static"
				cursor="pointer"
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
						fontSize: ctaH * 0.42,
						fill: BRAND_INK,
						align: 'center',
						letterSpacing: 3,
					}}
				/>
			</Container>
		</Container>
	</MainContainer>

	<!-- Space owned by TapToSkip; overlay tap → same stopButtonClick bus -->
	<OnPressFullScreen onpress={broadcastSkip} />
</FadeContainer>
