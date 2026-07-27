<script lang="ts">
	import { Rectangle as HitRectangle } from 'pixi.js';
	import { Container, Graphics, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { OnHotkey } from 'components-shared';
	import { OnPressFullScreen } from 'components-layout';
	import { stateUrlDerived } from 'state-shared';

	import { getContext } from '../game/context';

	type Props = {
		oncontinue: () => void;
	};

	type Card = {
		headline: string;
		art: 'scatter' | 'mirror' | 'eye' | 'hauntings' | 'maxwin';
	};

	type TextSeg = { text: string; hl: boolean };

	const props: Props = $props();
	const context = getContext();

	// Same chrome language as paytable / buy-confirm / bonus level banner.
	const BRAND_FAMILY = 'Impact, "Arial Black", "Arial Narrow", Arial, sans-serif';
	const BRAND_INK = 0x0a0a0a;
	const BRAND_COPY = 0xece8df;
	const BRAND_RED = 0xe91e63;
	const CTA_RATIO = 282 / 780;
	const CLOSE_RATIO = 1;
	const CHEVRON_RATIO = 302 / 282;

	// Highlight tokens from existing mechanic copy (no invented rules text).
	const HL_TOKENS = ['30,000X', 'HER SIDE', 'THE INTAKE', 'WHITEOUT', 'IT KNOWS', '3+', '3 LEVELS'];

	// feature walkthrough cards — content unchanged; chrome is NEW UI plates.
	const CARDS: Card[] = [
		{ headline: 'LAND 3+ MEMORY RESETS\nTO ENTER HER SIDE', art: 'scatter' },
		{ headline: 'OBSERVATION PANES\nFRACTURE CELLS INTO\nTHOUSANDS OF WAYS', art: 'mirror' },
		{ headline: 'IT KNOWS TURNS EVERY\nFRACTURED SYMBOL WILD\nFOR THE SPIN', art: 'eye' },
		{ headline: 'SURVIVE 3 LEVELS\nTHE INTAKE / HER SIDE\nWHITEOUT', art: 'hauntings' },
		{
			// stake.us social mode prohibits "bet" wording
			headline: stateUrlDerived.social() ? 'WIN UP TO\n30,000X YOUR PLAY' : 'WIN UP TO\n30,000X YOUR BET',
			art: 'maxwin',
		},
	];

	let index = $state(0);

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const centerX = $derived(canvas.width * 0.5);
	const unit = $derived(Math.min(canvas.width, canvas.height));

	const logoWidth = $derived(unit * 0.32);
	// clinical stack logo_v3 master is 2048×2082 transparent (Scenario Photoroom alpha)
	const logoHeight = $derived(logoWidth * (2082 / 2048));
	const logoY = $derived(canvas.height * 0.05);
	const logoBottom = $derived(logoY + logoHeight);

	const artSize = $derived(unit * 0.24);
	const headlineY = $derived(logoBottom + unit * 0.1);
	const artY = $derived(canvas.height * 0.56);
	const dotsY = $derived(canvas.height * 0.72);
	const buttonY = $derived(canvas.height * 0.84);

	const plateW = $derived(Math.min(unit * 0.72, canvas.width * 0.78));
	const plateH = $derived(Math.min(unit * 0.58, canvas.height * 0.62));
	const plateY = $derived((logoBottom + buttonY) * 0.5);

	const ctaW = $derived(Math.min(unit * 0.42, 340));
	const ctaH = $derived(ctaW * CTA_RATIO);
	const closeSize = $derived(Math.min(unit * 0.07, 56));
	const chevronSize = $derived(Math.min(unit * 0.085, 68));
	const chevronH = $derived(chevronSize * CHEVRON_RATIO);
	const fontSize = $derived(unit * 0.034);
	const lineHeight = $derived(unit * 0.046);

	const previous = () => (index = (index - 1 + CARDS.length) % CARDS.length);
	const next = () => (index = (index + 1) % CARDS.length);
	// tap / Space advances; last card exits. CONTINUE / close always exit.
	const advance = () => {
		if (index >= CARDS.length - 1) props.oncontinue();
		else next();
	};
	const exit = () => props.oncontinue();

	const drawPlate = (graphics: import('pixi.js').Graphics) => {
		const w = plateW;
		const h = plateH;
		const r = Math.min(unit * 0.01, 8);
		// buy-confirm / bet-menu shell — distressed dark, not plain glass grey
		graphics.roundRect(-w * 0.5, -h * 0.5, w, h, r);
		graphics.fill({ color: 0x0a0c10, alpha: 0.94 });
		graphics.roundRect(-w * 0.5, -h * 0.5, w, h, r);
		graphics.stroke({ width: Math.max(2, unit * 0.0035), color: 0x2a3038, alpha: 1 });
		const inset = Math.max(4, unit * 0.008);
		graphics.roundRect(-w * 0.5 + inset, -h * 0.5 + inset, w - inset * 2, h - inset * 2, Math.max(2, r - 2));
		graphics.stroke({ width: 1, color: 0xece8df, alpha: 0.14 });
		graphics.roundRect(-w * 0.5 + 1, -h * 0.5 + 1, w - 2, h - 2, r);
		graphics.stroke({ width: 1, color: 0xffffff, alpha: 0.06 });
	};

	const artFrameW = $derived(
		CARDS[index].art === 'mirror' || CARDS[index].art === 'eye' || CARDS[index].art === 'hauntings'
			? artSize * 2.2
			: artSize,
	);
	const drawArtFrame = (graphics: import('pixi.js').Graphics) => {
		const pad = artSize * 0.08;
		const w = artFrameW + pad * 2;
		const h = artSize + pad * 2;
		graphics.roundRect(-w * 0.5, -h * 0.5, w, h, 3);
		graphics.stroke({ width: Math.max(2, unit * 0.004), color: BRAND_RED, alpha: 0.85 });
	};

	const drawDots = (graphics: import('pixi.js').Graphics) => {
		const gap = unit * 0.035;
		const radius = unit * 0.0075;
		CARDS.forEach((_, dotIndex) => {
			const x = (dotIndex - (CARDS.length - 1) / 2) * gap;
			graphics.circle(x, 0, radius);
			graphics.fill({ color: dotIndex === index ? BRAND_RED : 0x5c5854, alpha: 1 });
		});
	};

	const measureCanvas = typeof document !== 'undefined' ? document.createElement('canvas') : null;
	const measure = (text: string, size: number) => {
		const ctx = measureCanvas?.getContext('2d');
		if (!ctx) return text.length * size * 0.5;
		ctx.font = `800 ${size}px ${BRAND_FAMILY}`;
		return ctx.measureText(text).width;
	};

	const segmentLine = (line: string): TextSeg[] => {
		const upper = line.toUpperCase();
		const segs: TextSeg[] = [];
		let i = 0;
		while (i < line.length) {
			let hit: { token: string; at: number } | null = null;
			for (const token of HL_TOKENS) {
				const at = upper.indexOf(token, i);
				if (at === -1) continue;
				if (!hit || at < hit.at || (at === hit.at && token.length > hit.token.length)) {
					hit = { token, at };
				}
			}
			if (!hit) {
				segs.push({ text: line.slice(i), hl: false });
				break;
			}
			if (hit.at > i) segs.push({ text: line.slice(i, hit.at), hl: false });
			segs.push({ text: line.slice(hit.at, hit.at + hit.token.length), hl: true });
			i = hit.at + hit.token.length;
		}
		return segs.filter((s) => s.text.length > 0);
	};

	const headlineLayout = $derived.by(() => {
		const lines = CARDS[index].headline.split('\n');
		const size = fontSize;
		const lh = lineHeight;
		const totalH = (lines.length - 1) * lh;
		return lines.map((line, li) => {
			const segs = segmentLine(line);
			const widths = segs.map((s) => measure(s.text, size));
			const totalW = widths.reduce((a, b) => a + b, 0);
			let x = -totalW * 0.5;
			const placed = segs.map((s, si) => {
				const w = widths[si];
				const px = x + w * 0.5;
				x += w;
				return { ...s, x: px };
			});
			return { y: li * lh - totalH * 0.5, segs: placed };
		});
	});
</script>

<!-- dark scrim over the loading painting (full-bleed padded cell) -->
<Rectangle
	{...canvas}
	backgroundColor={0x050308}
	backgroundAlpha={0.55}
/>

<!-- game logo up top -->
<Sprite
	key="mirrorLogo"
	anchor={{ x: 0.5, y: 0 }}
	x={centerX}
	y={logoY}
	width={logoWidth}
	height={logoHeight}
/>

<!-- opaque brand shell behind tip copy + art -->
<Container x={centerX} y={plateY}>
	<Graphics draw={drawPlate} />
	<!-- magenta edge bleeds (same accent as buy-confirm / bet menu) -->
	<Sprite
		key="uiAccentStain"
		anchor={{ x: 0.5, y: 0.5 }}
		x={-plateW * 0.48}
		y={0}
		width={unit * 0.06}
		height={plateH * 0.72}
		alpha={0.85}
		eventMode="none"
	/>
	<Sprite
		key="uiAccentStain"
		anchor={{ x: 0.5, y: 0.5 }}
		x={plateW * 0.48}
		y={0}
		width={unit * 0.06}
		height={plateH * 0.72}
		alpha={0.85}
		angle={180}
		eventMode="none"
	/>
</Container>

<!-- close X — skip remaining cards into game -->
<Container
	x={centerX + plateW * 0.5 - closeSize * 0.65}
	y={plateY - plateH * 0.5 + closeSize * 0.65}
	eventMode="static"
	cursor="pointer"
	hitArea={new HitRectangle(-closeSize / 2, -closeSize / 2, closeSize, closeSize)}
	onpointerup={exit}
>
	<Sprite
		key="uiBtnCloseMagenta"
		anchor={0.5}
		width={closeSize}
		height={closeSize * CLOSE_RATIO}
		eventMode="none"
	/>
	<Text
		anchor={0.5}
		text="×"
		eventMode="none"
		style={{
			fontFamily: BRAND_FAMILY,
			fontWeight: '800',
			fontSize: closeSize * 0.72,
			fill: BRAND_INK,
			align: 'center',
		}}
	/>
</Container>

<!-- headline — Impact brand type with red mechanic highlights -->
<Container x={centerX} y={headlineY}>
	{#each headlineLayout as line}
		{#each line.segs as seg}
			<Text
				anchor={0.5}
				x={seg.x}
				y={line.y}
				text={seg.text}
				eventMode="none"
				style={{
					fontFamily: BRAND_FAMILY,
					fontWeight: '800',
					fontSize,
					fill: seg.hl ? BRAND_RED : BRAND_COPY,
					align: 'center',
					letterSpacing: 2,
				}}
			/>
		{/each}
	{/each}
</Container>

<!-- card art -->
<Container x={centerX} y={artY}>
	<Graphics draw={drawArtFrame} />
	{#if CARDS[index].art === 'scatter'}
		<Sprite key="s.png" anchor={0.5} width={artSize} height={artSize} />
	{:else if CARDS[index].art === 'mirror'}
		<!-- intact mirror flanked by the cracked one: before/after of the burst -->
		<Sprite key="hm_intact.png" anchor={0.5} x={-artSize * 0.55} width={artSize * 0.92} height={artSize * 0.92} />
		<Sprite key="hm_cracked.png" anchor={0.5} x={artSize * 0.55} width={artSize * 0.92} height={artSize * 0.92} />
	{:else if CARDS[index].art === 'eye'}
		<!-- the eye between two wilds: what the conversion produces -->
		<Sprite key="w.png" anchor={0.5} x={-artSize * 0.58} width={artSize * 0.8} height={artSize * 0.8} />
		<Sprite key="me.png" anchor={0.5} width={artSize} height={artSize} />
		<Sprite key="w.png" anchor={0.5} x={artSize * 0.58} width={artSize * 0.8} height={artSize * 0.8} />
	{:else if CARDS[index].art === 'hauntings'}
		<!-- the three bonus-level plates as a triptych -->
		<Sprite key="mirrorIntroSeance" anchor={0.5} x={-artSize * 0.78} width={artSize * 0.72} height={artSize * 0.72} />
		<Sprite key="mirrorIntroOtherside" anchor={0.5} width={artSize * 0.9} height={artSize * 0.9} />
		<Sprite key="mirrorIntroBloodmoon" anchor={0.5} x={artSize * 0.78} width={artSize * 0.72} height={artSize * 0.72} />
	{:else}
		<Sprite key="w.png" anchor={0.5} width={artSize} height={artSize} />
	{/if}
</Container>

<!-- tap empty area advances; arrows / CONTINUE mount after so they stay clickable -->
<OnPressFullScreen onpress={advance} />

<!-- prev / next — blank magenta chevron plates + Impact glyphs -->
<Container
	x={centerX - unit * 0.28}
	y={artY}
	eventMode="static"
	cursor="pointer"
	hitArea={new HitRectangle(-chevronSize / 2, -chevronH / 2, chevronSize, chevronH)}
	onpointerup={previous}
>
	<Sprite key="uiChevronPlate" anchor={0.5} width={chevronSize} height={chevronH} eventMode="none" />
	<Text
		anchor={0.5}
		text="<"
		eventMode="none"
		style={{
			fontFamily: BRAND_FAMILY,
			fontWeight: '800',
			fontSize: chevronSize * 0.55,
			fill: BRAND_INK,
			align: 'center',
		}}
	/>
</Container>
<Container
	x={centerX + unit * 0.28}
	y={artY}
	eventMode="static"
	cursor="pointer"
	hitArea={new HitRectangle(-chevronSize / 2, -chevronH / 2, chevronSize, chevronH)}
	onpointerup={next}
>
	<Sprite key="uiChevronPlate" anchor={0.5} width={chevronSize} height={chevronH} eventMode="none" />
	<Text
		anchor={0.5}
		text=">"
		eventMode="none"
		style={{
			fontFamily: BRAND_FAMILY,
			fontWeight: '800',
			fontSize: chevronSize * 0.55,
			fill: BRAND_INK,
			align: 'center',
		}}
	/>
</Container>

<!-- page dots — red active / grey inactive -->
<Container x={centerX} y={dotsY}>
	<Graphics draw={drawDots} />
</Container>

<!-- CONTINUE — magenta CTA plate (same as buy-confirm / bonus level banner) -->
<Container
	x={centerX}
	y={buttonY}
	eventMode="static"
	cursor="pointer"
	hitArea={new HitRectangle(-ctaW / 2, -ctaH / 2, ctaW, ctaH)}
	onpointerup={exit}
>
	<Sprite key="uiCtaActivate" anchor={0.5} width={ctaW} height={ctaH} eventMode="none" />
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

<OnHotkey hotkey="Space" onpress={advance} />
<OnHotkey hotkey="ArrowLeft" onpress={previous} />
<OnHotkey hotkey="ArrowRight" onpress={next} />
<OnHotkey hotkey="Escape" onpress={exit} />
