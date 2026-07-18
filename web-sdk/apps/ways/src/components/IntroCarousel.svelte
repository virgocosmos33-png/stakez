<script lang="ts">
	import { Container, Graphics, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { OnHotkey } from 'components-shared';

	import { getContext } from '../game/context';
	import { drawGlassPill } from '../game/glassChrome';

	type Props = {
		oncontinue: () => void;
	};

	type Card = {
		headline: string;
		art: 'scatter' | 'mirror' | 'hauntings' | 'maxwin';
	};

	const props: Props = $props();
	const context = getContext();

	// feature walkthrough cards (Made Men-style intro carousel)
	// Copy uses only glyphs present in the 'silver' bitmap font (no accents /
	// middots): SEANCE stays unaccented and levels are slash-separated.
	const CARDS: Card[] = [
		{ headline: 'LAND 3+ SCATTERS TO\nBEGIN THE SEANCE', art: 'scatter' },
		{ headline: 'HAUNTED MIRRORS SHATTER\nINTO APPARITIONS FOR\nTHOUSANDS OF WAYS', art: 'mirror' },
		{ headline: 'SURVIVE 3 HAUNTINGS\nSEANCE / THE OTHER SIDE\nBLOOD MOON', art: 'hauntings' },
		{ headline: 'WIN UP TO\n30,000X YOUR BET', art: 'maxwin' },
	];

	let index = $state(0);

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const centerX = $derived(canvas.width * 0.5);
	// content scales off the smaller canvas edge so portrait keeps fitting
	const unit = $derived(Math.min(canvas.width, canvas.height));

	// logo geometry (art is 1024x641); everything below hangs off its real bottom
	// edge so the headline can never ride up into the wordmark
	const logoWidth = $derived(unit * 0.32);
	const logoHeight = $derived(logoWidth * (641 / 1024));
	const logoY = $derived(canvas.height * 0.05);
	const logoBottom = $derived(logoY + logoHeight);

	const artSize = $derived(unit * 0.24);
	// headline sits a fixed gap under the logo (anchor 0.5)
	const headlineY = $derived(logoBottom + unit * 0.1);
	const artY = $derived(canvas.height * 0.56);
	const dotsY = $derived(canvas.height * 0.72);
	const buttonY = $derived(canvas.height * 0.84);

	const buttonWidth = $derived(Math.min(unit * 0.42, 340));
	const buttonHeight = $derived(Math.min(unit * 0.085, 64));

	const previous = () => (index = (index - 1 + CARDS.length) % CARDS.length);
	const next = () => (index = (index + 1) % CARDS.length);

	const drawChevron = (graphics: import('pixi.js').Graphics, direction: 1 | -1) => {
		const size = unit * 0.028;
		graphics.moveTo(-direction * size * 0.5, -size);
		graphics.lineTo(direction * size * 0.5, 0);
		graphics.lineTo(-direction * size * 0.5, size);
		graphics.stroke({ width: size * 0.45, color: 0xcfc4e8, cap: 'round', join: 'round' });
	};

	const drawDots = (graphics: import('pixi.js').Graphics) => {
		const gap = unit * 0.035;
		const radius = unit * 0.0075;
		CARDS.forEach((_, dotIndex) => {
			const x = (dotIndex - (CARDS.length - 1) / 2) * gap;
			graphics.circle(x, 0, radius);
			graphics.fill({ color: dotIndex === index ? 0xb887ff : 0x5a5468, alpha: 1 });
		});
	};

	const drawButton = (graphics: import('pixi.js').Graphics) => {
		drawGlassPill(graphics, { width: buttonWidth, height: buttonHeight });
	};
</script>

<!-- dark scrim over the loading painting -->
<Rectangle
	{...canvas}
	backgroundColor={0x050308}
	backgroundAlpha={0.72}
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

<!-- headline (uses the loaded 'silver' bitmap font to match the rest of the UI) -->
<Text
	anchor={0.5}
	x={centerX}
	y={headlineY}
	text={CARDS[index].headline}
	style={{
		fontFamily: 'silver',
		fontSize: unit * 0.034,
		fill: 0xffffff,
		align: 'center',
		lineHeight: unit * 0.046,
		letterSpacing: 2,
	}}
/>

<!-- card art -->
<Container x={centerX} y={artY}>
	{#if CARDS[index].art === 'scatter'}
		<Sprite key="s.png" anchor={0.5} width={artSize} height={artSize} />
	{:else if CARDS[index].art === 'mirror'}
		<!-- intact mirror flanked by the cracked one: before/after of the burst -->
		<Sprite key="hm_intact.png" anchor={0.5} x={-artSize * 0.55} width={artSize * 0.92} height={artSize * 0.92} />
		<Sprite key="hm_cracked.png" anchor={0.5} x={artSize * 0.55} width={artSize * 0.92} height={artSize * 0.92} />
	{:else if CARDS[index].art === 'hauntings'}
		<!-- the three bonus-level plates as a triptych -->
		<Sprite key="mirrorIntroSeance" anchor={0.5} x={-artSize * 0.78} width={artSize * 0.72} height={artSize * 0.72} />
		<Sprite key="mirrorIntroOtherside" anchor={0.5} width={artSize * 0.9} height={artSize * 0.9} />
		<Sprite key="mirrorIntroBloodmoon" anchor={0.5} x={artSize * 0.78} width={artSize * 0.72} height={artSize * 0.72} />
	{:else}
		<Sprite key="w.png" anchor={0.5} width={artSize} height={artSize} />
	{/if}
</Container>

<!-- prev / next arrows -->
<Container
	x={centerX - unit * 0.28}
	y={artY}
	eventMode="static"
	cursor="pointer"
	onpointerup={previous}
>
	<Rectangle width={unit * 0.08} height={unit * 0.12} anchor={0.5} backgroundColor={0xffffff} backgroundAlpha={0.001} />
	<Graphics draw={(graphics) => drawChevron(graphics, -1)} />
</Container>
<Container
	x={centerX + unit * 0.28}
	y={artY}
	eventMode="static"
	cursor="pointer"
	onpointerup={next}
>
	<Rectangle width={unit * 0.08} height={unit * 0.12} anchor={0.5} backgroundColor={0xffffff} backgroundAlpha={0.001} />
	<Graphics draw={(graphics) => drawChevron(graphics, 1)} />
</Container>

<!-- page dots -->
<Container x={centerX} y={dotsY}>
	<Graphics draw={drawDots} />
</Container>

<!-- continue button -->
<Container x={centerX} y={buttonY} eventMode="static" cursor="pointer" onpointerup={() => props.oncontinue()}>
	<Graphics draw={drawButton} />
	<Text
		anchor={0.5}
		text="CONTINUE"
		style={{
			fontFamily: 'silver',
			fontSize: buttonHeight * 0.42,
			fill: 0xffffff,
			letterSpacing: 3,
		}}
	/>
</Container>

<OnHotkey hotkey="Space" onpress={() => props.oncontinue()} />
<OnHotkey hotkey="ArrowLeft" onpress={previous} />
<OnHotkey hotkey="ArrowRight" onpress={next} />
