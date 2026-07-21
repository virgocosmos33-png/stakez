<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { Container, Sprite, Graphics } from 'pixi-svelte';

	import { drawWindowShade } from '../game/glassChrome';
	import { PLAQUE_RATIO } from '../game/plaqueMount';
	import FittedText from './FittedText.svelte';

	// Shared ornate amethyst haunted-mirror NAMEPLATE (mirrorWaysFrame art +
	// dark-glass display window). Used by BOTH WaysCounter and the rail WIN
	// readout so they render as a matched, stacked pair on the frame's left rail:
	// a "CAPTION | value" pill (e.g. "WAYS | 15 360", "WIN | $9.15"). Caption +
	// value are FittedText INSIDE the glass window so they always fit.
	type Props = {
		caption: string;
		value: string;
		frameW: number;
		x: number;
		y: number;
		show: boolean;
		pop?: number; // external pop scale (1 = none)
	};
	const { caption, value, frameW, x, y, show, pop = 1 }: Props = $props();

	const frameH = $derived(frameW * PLAQUE_RATIO);

	// glass window, measured from the art (fractions of the frame), then a safe
	// inner inset so text keeps clear of the ornate lip
	const WIN = { cx: 0.517, cy: 0.495, w: 0.789, h: 0.352 };
	const winX = $derived((WIN.cx - 0.5) * frameW);
	const winY = $derived((WIN.cy - 0.5) * frameH);
	const winW = $derived(WIN.w * frameW);
	const winH = $derived(WIN.h * frameH);
	const textH = $derived(winH * 0.66);
</script>

<MainContainer>
	<FadeContainer {show} {x} {y}>
		<Container scale={pop}>
			<!-- soft recess so the silver text lifts off the glass -->
			<Container x={winX} y={winY}>
				<Graphics
					draw={(g) =>
						drawWindowShade(g, { width: winW * 0.98, height: winH * 0.9, radius: winH * 0.32 })}
				/>
				<Sprite
					key="mirrorCounterGlass"
					anchor={0.5}
					width={winW * 0.98}
					height={winH * 0.92}
					alpha={0.22}
				/>
			</Container>

			<Sprite key="mirrorWaysFrame" anchor={0.5} width={frameW} height={frameH} />

			<!-- caption (left third) -->
			<FittedText
				x={winX - winW * 0.31}
				y={winY}
				maxWidth={winW * 0.32}
				maxHeight={textH * 0.62}
				tint={0xcdb8f5}
				text={caption}
				style={{ fontFamily: 'silver', fontSize: (textH * 0.62) / 1.69, letterSpacing: 2 }}
			/>
			<!-- value (hero, right two-thirds) -->
			<FittedText
				x={winX + winW * 0.17}
				y={winY}
				maxWidth={winW * 0.6}
				maxHeight={textH}
				tint={0xf6f0ff}
				text={value}
				style={{ fontFamily: 'silver', fontSize: textH / 1.69, letterSpacing: 1 }}
			/>
		</Container>
	</FadeContainer>
</MainContainer>
