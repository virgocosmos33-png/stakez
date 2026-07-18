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
	import { OnHotkey } from 'components-shared';
	import { FadeContainer } from 'components-pixi';
	import { BitmapText, Container, Graphics, Sprite } from 'pixi-svelte';
	import { waitForResolve } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { drawGlassPill } from '../game/glassChrome';

	const context = getContext();

	const WHITE = 0xffffff;

	// one haunted-mirror painting + spectral palette per bonus level
	const LEVEL_THEME = {
		1: { panel: 'mirrorFsIntro', glow: 0x8ff2a6, glowDeep: 0x2f6b45 }, // THE SÉANCE
		2: { panel: 'mirrorFsIntroOtherside', glow: 0xa4ffb8, glowDeep: 0x2f6b45 }, // THE OTHER SIDE
		3: { panel: 'mirrorFsIntroBloodmoon', glow: 0xff6b5a, glowDeep: 0x6e1014 }, // BLOOD MOON
	} as const;

	// mirror centrepiece art is 1024x1024; the dark glass oval sits at centre
	const PANEL_RATIO = 1;

	let show = $state(false);
	let level = $state<1 | 2 | 3>(1);
	let freeSpinsFromEvent = $state(0);
	let oncomplete = $state(() => {});

	const theme = $derived(LEVEL_THEME[level]);

	const scale = new Tween(0);
	const reveal = new Tween(0);

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
			await waitForResolve((resolve) => (oncomplete = resolve));
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

	// soft dark halo grounding a text line on any painting (esp. the bright
	// green Other Side glass, where blood-red lettering goes muddy without it)
	const drawTextBacking = (g: import('pixi.js').Graphics, width: number, height: number) => {
		for (let i = 3; i >= 1; i--) {
			g.ellipse(0, 0, (width / 2) * (0.6 + i * 0.2), (height / 2) * (0.6 + i * 0.2));
			g.fill({ color: 0x000000, alpha: 0.16 });
		}
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

			<!-- title carved above the frame's crest -->
			<Container y={-panelHeight * 0.42}>
				<Graphics draw={(g) => drawTextBacking(g, SYMBOL_SIZE * 3.6, SYMBOL_SIZE * 0.62)} />
				<BitmapText
					anchor={0.5}
					text="THE VEIL PARTS"
					style={{ fontFamily: 'gold', fontSize: SYMBOL_SIZE * 0.3, letterSpacing: 2, align: 'center' }}
				/>
			</Container>

			<!-- the awarded count, materialising as an apparition inside the glass -->
			<Container y={-panelHeight * 0.01}>
				<Graphics draw={(g) => drawApparitionGlow(g, time, reveal.current)} />
				<Container scale={numberScale} alpha={reveal.current}>
					<!-- absinthe-green apparition numeral (ghost font) -->
					<BitmapText
						anchor={0.5}
						text={freeSpinsFromEvent}
						style={{ fontFamily: 'ghost', fontSize: SYMBOL_SIZE * 1.15, fontWeight: 'bold' }}
					/>
				</Container>
			</Container>

			<Container y={panelHeight * 0.19} alpha={reveal.current}>
				<Graphics draw={(g) => drawTextBacking(g, SYMBOL_SIZE * 3.2, SYMBOL_SIZE * 0.68)} />
				<BitmapText
					anchor={0.5}
					text="FREE SPINS"
					style={{ fontFamily: 'gold', fontSize: SYMBOL_SIZE * 0.34, letterSpacing: 3, align: 'center' }}
				/>
			</Container>

			<!-- themed CONTINUE matching the HUD scrying-glass chrome -->
			<Container y={panelHeight * 0.58} scale={continuePulse}>
				<Graphics
					eventMode="static"
					cursor="pointer"
					onpointerup={() => oncomplete()}
					draw={(g) => drawGlassPill(g, { width: SYMBOL_SIZE * 2.6, height: SYMBOL_SIZE * 0.56 })}
				/>
				<BitmapText
					anchor={0.5}
					text="CONTINUE"
					eventMode="none"
					style={{ fontFamily: 'gold', fontSize: SYMBOL_SIZE * 0.28, letterSpacing: 2 }}
				/>
			</Container>
		</Container>
	</MainContainer>

	<!-- keep the press-anywhere / space-to-continue affordance -->
	<OnHotkey hotkey="Space" onpress={() => oncomplete()} />
	<OnPressFullScreen onpress={() => oncomplete()} />
</FadeContainer>
