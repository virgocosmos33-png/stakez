<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn, cubicOut } from 'svelte/easing';
	import { Rectangle as HitRectangle } from 'pixi.js';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { LoadingProgress } from 'components-pixi';
	import { OnHotkey } from 'components-shared';
	import { OnPressFullScreen } from 'components-layout';

	import { getContext } from '../game/context';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { TR_INK_BONE, TR_INK_IRON, fitFontSize, trLabelStyle } from '../game/typography';
	import PreloadStreetSmoke from './PreloadStreetSmoke.svelte';

	type Props = {
		ready: boolean;
		oncontinue: () => void;
	};

	type FeatureCard = {
		title: string;
		body: string;
		art: string;
	};

	const props: Props = $props();
	const context = getContext();

	const CARDS: FeatureCard[] = [
		{
			title: 'THE WAKE',
			body: '3 BONUS TOMBSTONES\nUNLOCK 10 BONUS SPINS',
			art: 'trScatter',
		},
		{
			title: 'THE RECKONING',
			body: 'A SUPER SCATTER OPENS\nTHE LAST-REEL LANE',
			art: 'trScatterSuper',
		},
		{
			title: 'SPLIT',
			body: 'ONE SYMBOL GAINS EXTRA WAYS\nTHEN TURNS WILD',
			art: 'trSP',
		},
		{
			title: 'GUNSMOKE',
			body: 'EVERY COPY OF ONE SYMBOL\nTURNS WILD',
			art: 'trGS',
		},
		{
			title: 'NUDGE WAYS',
			body: 'NUDGES DOWN INTO WILDS\nAND GROWS THE WAYS',
			art: 'trNW',
		},
		{
			title: 'THE REVOLVER',
			body: 'WILD ON EVERY WAY\nAND THE LAST-REEL LANE',
			art: 'wrWild',
		},
	];

	const ACTIVE_RATIO = 823 / 479;
	const SIDE_RATIO = 572 / 298;
	const ARROW_RATIO = 305 / 180;
	const CONTINUE_RATIO = 165 / 784;
	const CARD_ART_TOP = 0.22;
	const CARD_ART_BOT = 0.62;
	const CARD_TITLE_Y = 0.925;
	const CARD_BODY_MAX_BOTTOM = 0.86;
	const CARD_ART_W = 0.66;
	const BODY_TRACK = 0.3;
	const BG_W = 1536;
	const BG_H = 1024;
	const LOGO_ASPECT = 717 / 1514;
	const CARD_DROP_MS = 480;
	const LOGO_DROP_MS = 520;
	const LAND_MS = 240;
	const CHROME_MS = 280;

	let index = $state(0);
	let settled = $state(false);
	const logoDrop = new Tween(0);
	const cardDrop = new Tween(0);
	const logoSquash = new Tween(1);
	const cardSquash = new Tween(1);
	const chromeIn = new Tween(0);

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const centerX = $derived(canvas.width * 0.5);
	const portrait = $derived(canvas.height / canvas.width > 1.15);
	const bgFit = $derived.by(() => {
		const scale = Math.max(canvas.width / BG_W, canvas.height / BG_H);
		return { width: BG_W * scale, height: BG_H * scale };
	});
	const stageW = $derived(Math.max(160, canvas.width * (portrait ? 0.94 : 0.86)));
	const logoW = $derived(Math.min(stageW * 0.36, canvas.height * 0.16 / LOGO_ASPECT, 340));
	const logoH = $derived(logoW * LOGO_ASPECT);
	const logoY = $derived(Math.max(logoH * 0.52 + 10, canvas.height * 0.08));

	const continueW = $derived(Math.min(stageW * 0.48, canvas.width * 0.36));
	const continueH = $derived(continueW * CONTINUE_RATIO);
	const barW = $derived(Math.min(continueW * 0.86, 480));
	const barH = $derived(barW * (87 / 492));
	const continueY = $derived(canvas.height - continueH * 0.5 - Math.max(10, canvas.height * 0.02));

	const cardTop = $derived(logoY + logoH * 0.5 + Math.max(10, canvas.height * 0.02));
	const cardBot = $derived(continueY - continueH * 0.5 - Math.max(36, canvas.height * 0.07));
	const cardBudgetH = $derived(Math.max(120, cardBot - cardTop));
	const cardY = $derived((cardTop + cardBot) * 0.5);

	const cardGap = $derived(Math.max(8, stageW * 0.016));
	const arrowPad = $derived(Math.max(10, stageW * 0.014));
	const rawCenterH = $derived(
		Math.min(cardBudgetH, portrait ? stageW * 0.92 * ACTIVE_RATIO : cardBudgetH),
	);
	const rawCenterW = $derived(rawCenterH / ACTIVE_RATIO);
	const rawSideH = $derived(rawCenterH * (portrait ? 0 : 0.84));
	const rawSideW = $derived(rawSideH / SIDE_RATIO);
	const rawArrowH = $derived(rawCenterH * 0.22);
	const rawArrowW = $derived(rawArrowH / ARROW_RATIO);
	const rawRow = $derived(
		rawCenterW +
			(portrait ? 0 : (rawSideW + cardGap) * 2) +
			(rawArrowW + arrowPad) * 2,
	);
	const cardScale = $derived(Math.min(1, (stageW * 0.96) / Math.max(1, rawRow)));
	const aW = $derived(rawCenterW * cardScale);
	const aH = $derived(rawCenterH * cardScale);
	const sW = $derived(rawSideW * cardScale);
	const sH = $derived(rawSideH * cardScale);
	const arrowH = $derived(rawArrowH * cardScale);
	const arrowW = $derived(rawArrowW * cardScale);
	const sideSpan = $derived(portrait ? 0 : sW + cardGap * cardScale);
	const arrowX = $derived(aW * 0.5 + sideSpan + arrowPad * cardScale + arrowW * 0.5);

	const cardBottom = $derived(cardY + aH * 0.5);
	const dotSize = $derived(Math.min(stageW * 0.038, 28));
	const dotsY = $derived(
		Math.min(
			continueY - continueH * 0.5 - dotSize * 0.7,
			cardBottom + Math.max(10, aH * 0.035) + dotSize * 0.5,
		),
	);

	const logoOff = $derived(-(1 - logoDrop.current) * canvas.height * 0.7);
	const cardOff = $derived(-(1 - cardDrop.current) * canvas.height * 0.92);
	const logoSx = $derived(2 - logoSquash.current);
	const cardSx = $derived(2 - cardSquash.current);
	const logoYNow = $derived(logoY + logoOff);
	const cardYNow = $derived(cardY + cardOff);
	const pointer = $derived(settled ? 'static' : 'none');

	const finishDrop = () => {
		logoDrop.set(1, { duration: 0 });
		cardDrop.set(1, { duration: 0 });
		chromeIn.set(1, { duration: 0 });
		logoSquash.set(1, { duration: 0 });
		cardSquash.set(1, { duration: 0 });
		settled = true;
	};

	const previous = () => {
		if (!settled) return;
		index = (index - 1 + CARDS.length) % CARDS.length;
	};
	const next = () => {
		if (!settled) return;
		index = (index + 1) % CARDS.length;
	};
	const advance = () => {
		if (!settled) {
			finishDrop();
			return;
		}
		if (index >= CARDS.length - 1) {
			if (props.ready) props.oncontinue();
			return;
		}
		next();
	};
	const exit = () => {
		if (!settled) {
			finishDrop();
			return;
		}
		if (props.ready) props.oncontinue();
	};

	onMount(() => {
		let cancelled = false;
		const run = async () => {
			logoDrop.set(0, { duration: 0 });
			cardDrop.set(0, { duration: 0 });
			chromeIn.set(0, { duration: 0 });
			logoSquash.set(1, { duration: 0 });
			cardSquash.set(1, { duration: 0 });
			await logoDrop.set(1, { duration: fxDur(LOGO_DROP_MS), easing: cubicIn });
			if (cancelled || settled) return;
			logoSquash.set(0.94, { duration: 0 });
			void logoSquash.set(1, { duration: fxDur(LAND_MS), easing: backOut });
			await logoDrop.set(1.03, { duration: fxDur(60) });
			if (cancelled || settled) return;
			await logoDrop.set(1, { duration: fxDur(160), easing: cubicOut });
			if (cancelled || settled) return;
			await fxWait(60);
			if (cancelled || settled) return;
			await cardDrop.set(1, { duration: fxDur(CARD_DROP_MS), easing: cubicIn });
			if (cancelled || settled) return;
			cardSquash.set(0.92, { duration: 0 });
			void cardSquash.set(1, { duration: fxDur(LAND_MS), easing: backOut });
			await cardDrop.set(1.03, { duration: fxDur(60) });
			if (cancelled || settled) return;
			await cardDrop.set(1, { duration: fxDur(160), easing: cubicOut });
			if (cancelled || settled) return;
			await chromeIn.set(1, { duration: fxDur(CHROME_MS), easing: cubicOut });
			if (!cancelled) settled = true;
		};
		void run();
		return () => {
			cancelled = true;
		};
	});

	const cardAt = (offset: number) => CARDS[(index + offset + CARDS.length) % CARDS.length];

	const localY = (frac: number, height: number) => (frac - 0.5) * height;
	const artBox = (width: number, height: number) => {
		const wellH = (CARD_ART_BOT - CARD_ART_TOP) * height;
		const wellW = width * CARD_ART_W;
		const size = Math.min(wellW, wellH * 0.88);
		return { y: localY((CARD_ART_TOP + CARD_ART_BOT) * 0.5, height), size };
	};
	const cardTitleStyle = (cardW: number) =>
		trLabelStyle({
			fontWeight: '700',
			fontSize: Math.max(12, cardW * 0.082),
			fill: TR_INK_IRON,
			align: 'center',
			letterSpacing: 0.8,
		});
	const cardBody = (cardW: number, cardH: number, text: string) => {
		const longest = text.split('\n').reduce((a, b) => (a.length >= b.length ? a : b));
		const size = fitFontSize(longest, {
			role: 'label',
			base: Math.min(cardW * 0.08, cardH * 0.04),
			maxWidth: cardW * 0.82,
			min: 11,
			letterSpacing: BODY_TRACK,
		});
		const lineH = size * 1.16;
		const blockH = lineH * 2;
		const maxBottom = cardH * CARD_BODY_MAX_BOTTOM;
		const centerFromTop = Math.min(cardH * 0.74, maxBottom - blockH * 0.5);
		return {
			y: centerFromTop - cardH * 0.5,
			style: trLabelStyle({
				fontWeight: '700',
				fontSize: size,
				fill: TR_INK_BONE,
				align: 'center',
				letterSpacing: BODY_TRACK,
				lineHeight: lineH,
				stroke: { color: TR_INK_IRON, width: Math.max(2, size * 0.14), join: 'round' },
			}),
		};
	};
	const activeArt = $derived(artBox(aW, aH));
	const sideArt = $derived(artBox(sW, sH));
	const bodyPrev = $derived(cardBody(sW, sH, cardAt(-1).body));
	const bodyActive = $derived(cardBody(aW, aH, cardAt(0).body));
	const bodyNext = $derived(cardBody(sW, sH, cardAt(1).body));
</script>

<Rectangle {...canvas} backgroundColor={0x050308} backgroundAlpha={1} />
<Sprite
	key="preloadBg"
	anchor={0.5}
	x={centerX}
	y={canvas.height * 0.5}
	width={bgFit.width}
	height={bgFit.height}
	eventMode="none"
/>
<Container
	x={centerX - bgFit.width * 0.5}
	y={canvas.height * 0.5 - bgFit.height * 0.5}
	eventMode="none"
>
	<PreloadStreetSmoke width={bgFit.width} height={bgFit.height} />
</Container>
<Container
	x={centerX}
	y={logoYNow}
	scale={{ x: logoSx, y: logoSquash.current }}
	eventMode="none"
>
	<Sprite key="mirrorLogo" anchor={0.5} width={logoW} height={logoH} eventMode="none" />
</Container>
<OnPressFullScreen onpress={advance} />

{#if !portrait}
	<Container
		x={centerX - (aW * 0.5 + cardGap * cardScale + sW * 0.5)}
		y={cardYNow}
		scale={{ x: cardSx, y: cardSquash.current }}
		alpha={0.78}
	>
		<Sprite key="preloadCardSideL" anchor={0.5} width={sW} height={sH} eventMode="none" />
		<Sprite
			key={cardAt(-1).art}
			anchor={0.5}
			y={sideArt.y}
			width={sideArt.size}
			height={sideArt.size}
			eventMode="none"
		/>
		<Text
			anchor={0.5}
			y={bodyPrev.y}
			text={cardAt(-1).body}
			eventMode="none"
			style={bodyPrev.style}
		/>
		<Text
			anchor={0.5}
			y={localY(CARD_TITLE_Y, sH)}
			text={cardAt(-1).title}
			eventMode="none"
			style={cardTitleStyle(sW)}
		/>
	</Container>
{/if}

<Container x={centerX} y={cardYNow} scale={{ x: cardSx, y: cardSquash.current }}>
	<Sprite key="preloadCardActive" anchor={0.5} width={aW} height={aH} eventMode="none" />
	<Sprite
		key={cardAt(0).art}
		anchor={0.5}
		y={activeArt.y}
		width={activeArt.size}
		height={activeArt.size}
		eventMode="none"
	/>
	<Text
		anchor={0.5}
		y={bodyActive.y}
		text={cardAt(0).body}
		eventMode="none"
		style={bodyActive.style}
	/>
	<Text
		anchor={0.5}
		y={localY(CARD_TITLE_Y, aH)}
		text={cardAt(0).title}
		eventMode="none"
		style={cardTitleStyle(aW)}
	/>
</Container>

{#if !portrait}
	<Container
		x={centerX + (aW * 0.5 + cardGap * cardScale + sW * 0.5)}
		y={cardYNow}
		scale={{ x: cardSx, y: cardSquash.current }}
		alpha={0.78}
	>
		<Sprite key="preloadCardSideR" anchor={0.5} width={sW} height={sH} eventMode="none" />
		<Sprite
			key={cardAt(1).art}
			anchor={0.5}
			y={sideArt.y}
			width={sideArt.size}
			height={sideArt.size}
			eventMode="none"
		/>
		<Text
			anchor={0.5}
			y={bodyNext.y}
			text={cardAt(1).body}
			eventMode="none"
			style={bodyNext.style}
		/>
		<Text
			anchor={0.5}
			y={localY(CARD_TITLE_Y, sH)}
			text={cardAt(1).title}
			eventMode="none"
			style={cardTitleStyle(sW)}
		/>
	</Container>
{/if}

<Container
	x={centerX - arrowX}
	y={cardYNow}
	scale={{ x: cardSx, y: cardSquash.current }}
	eventMode={pointer}
	cursor="pointer"
	hitArea={new HitRectangle(-arrowW / 2, -arrowH / 2, arrowW, arrowH)}
	onpointerup={previous}
>
	<Sprite key="preloadArrowLeft" anchor={0.5} width={arrowW} height={arrowH} eventMode="none" />
</Container>
<Container
	x={centerX + arrowX}
	y={cardYNow}
	scale={{ x: cardSx, y: cardSquash.current }}
	eventMode={pointer}
	cursor="pointer"
	hitArea={new HitRectangle(-arrowW / 2, -arrowH / 2, arrowW, arrowH)}
	onpointerup={next}
>
	<Sprite key="preloadArrowRight" anchor={0.5} width={arrowW} height={arrowH} eventMode="none" />
</Container>

<Container x={centerX} y={dotsY} alpha={chromeIn.current}>
	{#each CARDS as _card, dotIndex}
		<Sprite
			key={dotIndex === index ? 'preloadDotOn' : 'preloadDotOff'}
			anchor={0.5}
			x={(dotIndex - (CARDS.length - 1) / 2) * dotSize * 1.45}
			width={dotIndex === index ? dotSize * 1.15 : dotSize * 0.72}
			height={dotIndex === index ? dotSize * 1.15 : dotSize * 0.72}
			eventMode="none"
		/>
	{/each}
</Container>

{#if props.ready}
	<Container
		x={centerX}
		y={continueY}
		alpha={chromeIn.current}
		eventMode={pointer}
		cursor="pointer"
		hitArea={new HitRectangle(-continueW / 2, -continueH / 2, continueW, continueH)}
		onpointerup={exit}
	>
		<Sprite key="preloadContinue" anchor={0.5} width={continueW} height={continueH} eventMode="none" />
	</Container>
{:else}
	<Container x={centerX} y={continueY} alpha={chromeIn.current}>
		<LoadingProgress width={barW} height={barH}>
			{#snippet background(sizes)}
				<Sprite key="progressBarBackground.png" {...sizes} />
			{/snippet}
			{#snippet progress(sizes)}
				<Sprite key="progressBar.png" {...sizes} />
			{/snippet}
			{#snippet frame(sizes)}
				<Sprite key="progressBarFrame.png" {...sizes} />
			{/snippet}
		</LoadingProgress>
	</Container>
{/if}

<OnHotkey hotkey="Space" onpress={advance} />
<OnHotkey hotkey="ArrowLeft" onpress={previous} />
<OnHotkey hotkey="ArrowRight" onpress={next} />
<OnHotkey hotkey="Escape" onpress={exit} />
