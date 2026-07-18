<script lang="ts">
	import { Container, BitmapText, type BitmapTextProps } from 'pixi-svelte';

	// Bitmap text that is GUARANTEED to sit inside a box, truly centred on
	// (x, y). The mm_* bitmap fonts declare lineHeight == base == fontSize but
	// their glyphs are ~1.7x taller with yoffset 0, so Pixi anchors them by the
	// short line box and the glyphs hang far below the anchor (this is why the
	// old counters overflowed their panels). We counter that two ways:
	//   * vertical centre  -> anchor.y = capRatio / 2 (shifts the anchor down to
	//                         the real glyph mid-line, capRatio = glyphPx / fontSize)
	//   * fit              -> scale down uniformly so the real width AND the real
	//                         glyph height both fit maxWidth / maxHeight
	// Set fontSize to maxHeight / capRatio and the text fills the window height,
	// then shrinks only when it would be too wide (long numbers). Nothing clips.
	type Props = Omit<BitmapTextProps, 'scale' | 'anchor' | 'onresize' | 'x' | 'y'> & {
		/** centre of the text block */
		x: number;
		y: number;
		maxWidth: number;
		maxHeight: number;
		/** glyph pixel height / fontSize for this font (silver/gold ~1.69) */
		capRatio?: number;
	};

	const { x, y, maxWidth, maxHeight, capRatio = 1.69, ...textProps }: Props = $props();

	let natural = $state({ width: 0, height: 0 });
	const fontSize = $derived(Number(textProps.style?.fontSize ?? 16));
	const glyphHeight = $derived(fontSize * capRatio);
	const fitScale = $derived(
		Math.min(maxWidth / (natural.width || 1), maxHeight / (glyphHeight || 1), 1),
	);
</script>

<!-- hidden measurer (natural width at the requested fontSize) -->
<Container visible={false}>
	<BitmapText {...textProps} onresize={(sizes) => (natural = sizes)} />
</Container>

<BitmapText {...textProps} {x} {y} anchor={{ x: 0.5, y: capRatio / 2 }} scale={fitScale} />
