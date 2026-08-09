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
		art: 'scatter' | 'cards' | 'wildreel' | 'levels' | 'maxwin';
	};

	type TextSeg = { text: string; hl: boolean };

	const props: Props = $props();
	const context = getContext();

	// Same chrome language as paytable / buy-confirm / bonus level banner.
	const BRAND_FAMILY = 'Impact, "Arial Black", "Arial Narrow", Arial, sans-serif';
	const BRAND_INK = 0x0a0a0a;
	const BRAND_COPY = 0xece8df;
	const BRAND_RED = 0xe91e63;
	const LETTER_SPACING = 2;
	const CTA_RATIO = 282 / 780;
	const CLOSE_RATIO = 1;
	const CHEVRON_RATIO = 302 / 282;

	// Highlight tokens from existing mechanic copy (no invented rules text).
	const HL_TOKENS = [
		'30,000X', 'BONUS MODES', 'HUGE WAY CONNECTIONS', '3+',
		'STRETCH', 'SPLIT', 'CLONE', 'WILD',
	];
	// longest tokens first so longer phrases win over substrings on the same line
	const HL_TOKENS_SORTED = [...HL_TOKENS].sort((a, b) => b.length - a.length);

	// feature walkthrough cards — THE WHITE ROOM mechanics only, drawn with the
	// exact in-game card art (never the legacy Madam Mirror atlas pieces).
	const CARDS: Card[] = [
		{ headline: 'LAND 3+ SCATTERS\nTO ENTER BONUS MODES', art: 'scatter' },
		{ headline: 'SEALED CELLS FIRE\nSTRETCH, SPLIT, CLONE\nAND WILD CARDS', art: 'cards' },
		{ headline: 'EXPANDING WILDS TURN\nWHOLE REELS WILD\nAND STACK THE WAYS', art: 'wildreel' },
		{ headline: 'COMBINED MECHANICS FOR\nHUGE WAY CONNECTIONS', art: 'levels' },
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

	// LOGO / PLATE / CONTINUE are one vertical block, centred in the canvas.
	//
	// Everything used to be sized off `unit` (the SHORTER canvas edge), which on
	// a portrait phone is the width — so the whole stack came out phone-width
	// tall and sat marooned in the middle of a very tall screen. Widths now come
	// off the canvas width, capped against the height so a wide desktop canvas
	// does not turn the panel into a billboard, and the plate takes whatever
	// vertical room the logo and button leave behind.
	const contentW = $derived(Math.min(canvas.width * 0.94, canvas.height * 0.95));
	const blockBudget = $derived(canvas.height * 0.92);
	const gap = $derived(Math.min(canvas.height * 0.022, unit * 0.035));

	// clinical stack logo_v3 master is 2048×2082 transparent (Scenario Photoroom alpha)
	const LOGO_RATIO = 2082 / 2048;
	const logoWidth = $derived(Math.min(contentW * 0.42, (blockBudget * 0.26) / LOGO_RATIO));
	const logoHeight = $derived(logoWidth * LOGO_RATIO);

	const ctaW = $derived(Math.min(contentW * 0.5, 380));
	const ctaH = $derived(ctaW * CTA_RATIO);

	const plateW = $derived(contentW);
	// never taller than it is wide, or the content inside strands in empty plate
	const plateH = $derived(
		Math.min(plateW, Math.max(unit * 0.26, blockBudget - logoHeight - ctaH - gap * 2)),
	);
	const blockH = $derived(logoHeight + gap + plateH + gap + ctaH);
	const blockTop = $derived(Math.max(canvas.height * 0.03, (canvas.height - blockH) * 0.5));

	const logoY = $derived(blockTop);
	const plateTop = $derived(blockTop + logoHeight + gap);
	const plateY = $derived(plateTop + plateH * 0.5);
	const buttonY = $derived(plateTop + plateH + gap + ctaH * 0.5);

	// the art has to live inside the plate, so it tracks the plate, not the canvas.
	// The 0.29 also keeps the widest card (a 2.2x triptych) clear of the chevrons.
	const artSize = $derived(Math.min(plateW * 0.29, plateH * 0.42));
	// max-win card is text-only: the headline sits dead centre at ~1.8x size
	const isMaxwin = $derived(CARDS[index].art === 'maxwin');
	const fontSize = $derived(plateW * 0.048 * (isMaxwin ? 1.8 : 1));
	const lineHeight = $derived(plateW * 0.064 * (isMaxwin ? 1.8 : 1));

	// zones inside the plate (origin = plate centre, +y = down)
	const headlineY = $derived(-plateH * 0.31);
	const artY = $derived(plateH * 0.14);
	// 0.44, not 0.4: at 0.4 the dot row brushed the art frame's pink border on
	// short plates — this drops it into the clear band above the plate edge.
	const dotsY = $derived(plateH * 0.44);

	const closeSize = $derived(Math.min(canvas.width * 0.09, 64));
	const chevronSize = $derived(Math.min(plateW * 0.12, 84));
	const chevronH = $derived(chevronSize * CHEVRON_RATIO);

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
		CARDS[index].art === 'cards' || CARDS[index].art === 'wildreel' || CARDS[index].art === 'levels'
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
		if (!text) return 0;
		const ctx = measureCanvas?.getContext('2d');
		const tracking = Math.max(0, text.length - 1) * LETTER_SPACING;
		if (!ctx) return text.length * size * 0.52 + tracking;
		ctx.font = `800 ${size}px ${BRAND_FAMILY}`;
		return ctx.measureText(text).width + tracking;
	};

	const segmentLine = (line: string): TextSeg[] => {
		const upper = line.toUpperCase();
		const segs: TextSeg[] = [];
		let i = 0;
		while (i < line.length) {
			let hit: { token: string; at: number } | null = null;
			for (const token of HL_TOKENS_SORTED) {
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
				const px = x;
				x += widths[si];
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

<!-- opaque brand shell — headline, art and dots stack inside it -->
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

	<!-- headline — upper zone (dead centre on the text-only max-win card) -->
	<Container y={isMaxwin ? 0 : headlineY}>
		{#each headlineLayout as line}
			{#each line.segs as seg}
				<Text
					anchor={{ x: 0, y: 0.5 }}
					x={seg.x}
					y={line.y}
					text={seg.text}
					eventMode="none"
					style={{
						fontFamily: BRAND_FAMILY,
						fontWeight: '800',
						fontSize,
						fill: seg.hl ? BRAND_RED : BRAND_COPY,
						align: 'left',
						letterSpacing: LETTER_SPACING,
					}}
				/>
			{/each}
		{/each}
	</Container>

	<!-- card art — middle zone (the max-win card is text-only, no art) -->
	{#if !isMaxwin}
		<Container y={artY}>
			<Graphics draw={drawArtFrame} />
			{#if CARDS[index].art === 'scatter'}
				<!-- the 1st scatter face; the atlas s.png is the old wordless head -->
				<Sprite key="wrScatter1" anchor={0.5} width={artSize} height={artSize} />
			{:else if CARDS[index].art === 'cards'}
				<!-- the three feature cards the sealed cells actually deal -->
				<Sprite key="wrStretch" anchor={0.5} x={-artSize * 0.78} width={artSize * 0.72} height={artSize * 0.72} />
				<Sprite key="wrSplit" anchor={0.5} width={artSize * 0.9} height={artSize * 0.9} />
				<Sprite key="wrClone" anchor={0.5} x={artSize * 0.78} width={artSize * 0.72} height={artSize * 0.72} />
			{:else if CARDS[index].art === 'wildreel'}
				<!-- wrWild is the straitjacket card the board actually deals; the
					rising-arrow variant is the Expanding Wild that takes a reel -->
				<Sprite key="wrWild" anchor={0.5} x={-artSize * 0.58} width={artSize * 0.8} height={artSize * 0.8} />
				<Sprite key="wrWildExpand" anchor={0.5} width={artSize} height={artSize} />
				<Sprite key="wrWild" anchor={0.5} x={artSize * 0.58} width={artSize * 0.8} height={artSize * 0.8} />
			{:else if CARDS[index].art === 'levels'}
				<!-- stretch + expanding wild + split: the cards that stack on one reel -->
				<Sprite key="wrStretch" anchor={0.5} x={-artSize * 0.78} width={artSize * 0.72} height={artSize * 0.72} />
				<Sprite key="wrWildExpand" anchor={0.5} width={artSize * 0.9} height={artSize * 0.9} />
				<Sprite key="wrSplit" anchor={0.5} x={artSize * 0.78} width={artSize * 0.72} height={artSize * 0.72} />
			{/if}
		</Container>
	{/if}

	<!-- page dots — bottom of plate -->
	<Container y={dotsY}>
		<Graphics draw={drawDots} />
	</Container>
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

<!-- tap empty area advances; arrows / CONTINUE mount after so they stay clickable -->
<OnPressFullScreen onpress={advance} />

<!-- prev / next — blank magenta chevron plates + Impact glyphs -->
<Container
	x={centerX - plateW * 0.43}
	y={plateY + artY}
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
	x={centerX + plateW * 0.43}
	y={plateY + artY}
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
