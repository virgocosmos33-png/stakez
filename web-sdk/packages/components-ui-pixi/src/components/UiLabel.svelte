<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Container, Text, Graphics } from 'pixi-svelte';

	import UiSprite from './UiSprite.svelte';
	import { UI_BASE_FONT_SIZE } from '../constants';
	import { HUD_THEME as T } from '../hudTheme';

	type Props = {
		label: string;
		value: string;
		tiled?: boolean;
		stacked?: boolean;
		/** how the pill sits relative to its x anchor (default centred) */
		align?: 'left' | 'center' | 'right';
		/** draw the plate background + ring + divider (default true) */
		bordered?: boolean;
	};

	const props: Props = $props();
	const bordered = $derived(props.bordered !== false);

	// horizontal pill: [ LABEL | VALUE ] — label light, value white, thin divider.
	const fs = UI_BASE_FONT_SIZE;
	const labelFs = fs * 0.84;
	const valueFs = fs * 0.92;
	// borderless labels drop the pill's inner padding so the text edge lands
	// exactly on the anchor (matching the flush-aligned buttons)
	const padX = $derived(fs * (bordered ? 0.9 : 0));
	const gap = fs * 0.55;
	const pillH = fs * 2.0;

	const labelW = $derived(props.label.length * labelFs * 0.64);
	const valueW = $derived(props.value.length * valueFs * 0.6);
	const dividerX = $derived(padX + labelW + gap);
	const totalW = $derived(dividerX + gap + valueW + padX);
	// shift the whole centred pill so its left/right edge lands on the x anchor
	const alignOffset = $derived(
		props.align === 'left' ? totalW / 2 : props.align === 'right' ? -totalW / 2 : 0,
	);

	const labelStyle = {
		fontFamily: T.fontDisplay,
		fontWeight: '700',
		fontSize: labelFs,
		fill: T.textSecondary,
		letterSpacing: 1.5,
	} as const;

	const valueStyle = {
		fontFamily: T.fontDisplay,
		fontWeight: '700',
		fontSize: valueFs,
		fill: T.textValue,
	} as const;

	const drawDivider = (g: PIXI.Graphics) => {
		g.roundRect(-1, -pillH * 0.28, 2, pillH * 0.56, 1);
		g.fill({ color: T.edgeGold, alpha: 0.6 });
	};
</script>

<Container x={alignOffset}>
	{#if bordered}
		<UiSprite
			y={0}
			anchor={{ x: 0.5, y: 0 }}
			tone="plate"
			shape="plate"
			key="base_ticker"
			width={totalW}
			height={pillH}
		/>
		<Graphics x={-totalW / 2 + dividerX} y={pillH / 2} draw={drawDivider} />
	{/if}
	<Text
		anchor={{ x: 0, y: 0.5 }}
		x={-totalW / 2 + padX}
		y={pillH / 2}
		text={props.label}
		style={labelStyle}
	/>
	<Text
		anchor={{ x: 1, y: 0.5 }}
		x={totalW / 2 - padX}
		y={pillH / 2}
		text={props.value}
		style={valueStyle}
	/>
</Container>
