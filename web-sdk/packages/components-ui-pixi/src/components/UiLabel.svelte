<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Text, Graphics } from 'pixi-svelte';

	import UiSprite from './UiSprite.svelte';
	import { UI_BASE_FONT_SIZE } from '../constants';

	type Props = {
		label: string;
		value: string;
		tiled?: boolean;
		stacked?: boolean;
	};

	const props: Props = $props();

	// horizontal pill: [ LABEL | VALUE ] — label light, value gold, thin divider.
	const fs = UI_BASE_FONT_SIZE;
	const labelFs = fs * 0.84;
	const valueFs = fs * 0.92;
	const padX = fs * 0.9;
	const gap = fs * 0.55;
	const pillH = fs * 2.0;

	const labelW = $derived(props.label.length * labelFs * 0.64);
	const valueW = $derived(props.value.length * valueFs * 0.6);
	const dividerX = $derived(padX + labelW + gap);
	const totalW = $derived(dividerX + gap + valueW + padX);

	const labelStyle = {
		fontFamily: 'proxima-nova',
		fontWeight: '600',
		fontSize: labelFs,
		fill: 0xf1f1f4,
		letterSpacing: 1,
	} as const;

	const valueStyle = {
		fontFamily: 'proxima-nova',
		fontWeight: '700',
		fontSize: valueFs,
		fill: 0xffc12e,
		dropShadow: {
			color: 0x1a1200,
			alpha: 0.6,
			blur: 2,
			distance: 1,
			angle: Math.PI / 2,
		},
	} as const;

	const drawDivider = (g: PIXI.Graphics) => {
		g.roundRect(-1, -pillH * 0.28, 2, pillH * 0.56, 1);
		g.fill({ color: 0x63636d, alpha: 0.75 });
	};
</script>

<UiSprite
	y={0}
	anchor={{ x: 0.5, y: 0 }}
	tone="plate"
	shape="plate"
	key="base_ticker"
	width={totalW}
	height={pillH}
/>
<Text
	anchor={{ x: 0, y: 0.5 }}
	x={-totalW / 2 + padX}
	y={pillH / 2}
	text={props.label}
	style={labelStyle}
/>
<Graphics x={-totalW / 2 + dividerX} y={pillH / 2} draw={drawDivider} />
<Text
	anchor={{ x: 1, y: 0.5 }}
	x={totalW / 2 - padX}
	y={pillH / 2}
	text={props.value}
	style={valueStyle}
/>
