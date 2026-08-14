<script lang="ts">
	/**
	 * WAYS / WIN / FREE SPINS as stacked ornate nameplates — the baked
	 * bar_readout_plaque frames, no timber slab around them. Desktop sits this
	 * to the right of the board; narrow layouts sit it under the board.
	 */
	import { Container, Sprite, Text } from 'pixi-svelte';

	import { hudColor } from '../game/hud.generated';
	import { TR_INK_BRASS, fitFontSize, trLabelStyle, trValueStyle } from '../game/typography';

	export type HudReadoutSlot = { label: string; value: string; w?: number };

	type Props = {
		slots: HudReadoutSlot[];
		x: number;
		y: number;
		wellW: number;
		/** 'y' = one column (desktop). 'x' = one row (narrow). */
		axis?: 'x' | 'y';
	};

	const props: Props = $props();

	/** bar_readout_plaque.png is 1200x800 */
	const PLAQUE_ASPECT = 1.5;
	/** dark inset panel, as fractions of the texture (inside the beaded border) */
	const OPENING = { y0: 0.19, y1: 0.81 };
	const VALUE_COLOR = hudColor('text', 0xf0e6d0);
	const LABEL_COLOR = TR_INK_BRASS;
	const LABEL_TRACKING = 2;
	const VALUE_TRACKING = 0.3;
	const INK_STROKE = { color: 0x05070a, width: 2 } as const;
	const INK_SHADOW = {
		color: 0x000000,
		blur: 3,
		distance: 1,
		alpha: 0.6,
		angle: Math.PI / 2,
	} as const;

	const metrics = $derived.by(() => {
		const wellW = props.wellW;
		const blockH = wellW / PLAQUE_ASPECT;
		const stackGap = blockH * 0.08;
		const panelH = (OPENING.y1 - OPENING.y0) * blockH;
		const labelSize = Math.max(8, Math.floor(panelH * 0.26));
		const valueSize = Math.max(12, Math.floor(panelH * 0.46));
		const axis = props.axis ?? 'y';
		const widths = props.slots.map((slot) => slot.w ?? wellW);
		const n = props.slots.length;
		if (n === 0) return { blocks: [] as const, panelH };

		if (axis === 'x') {
			const totalW = widths.reduce((sum, w) => sum + w, 0) + stackGap * (n - 1);
			let cursor = -totalW / 2;
			return {
				panelH,
				blocks: props.slots.map((slot, i) => {
					const w = widths[i];
					const cx = cursor + w / 2;
					cursor += w + stackGap;
					return {
						label: slot.label,
						value: slot.value,
						cx,
						cy: 0,
						w,
						h: blockH,
						labelSize,
						valueSize,
					};
				}),
			};
		}

		const totalH = n * blockH + (n - 1) * stackGap;
		return {
			panelH,
			blocks: props.slots.map((slot, i) => ({
				label: slot.label,
				value: slot.value,
				cx: 0,
				cy: -totalH / 2 + blockH / 2 + i * (blockH + stackGap),
				w: widths[i],
				h: blockH,
				labelSize,
				valueSize,
			})),
		};
	});
</script>

<Container x={props.x} y={props.y}>
	{#each metrics.blocks as b (b.label)}
		<Sprite
			key="barReadoutPlaque"
			x={b.cx}
			y={b.cy}
			anchor={0.5}
			width={b.w}
			height={b.h}
			eventMode="none"
		/>
		<Text
			x={b.cx}
			y={b.cy - metrics.panelH * 0.24}
			anchor={0.5}
			text={b.label}
			eventMode="none"
			style={trLabelStyle({
				fill: LABEL_COLOR,
				fontSize: fitFontSize(b.label, {
					role: 'label',
					base: b.labelSize,
					maxWidth: b.w * 0.68,
					letterSpacing: LABEL_TRACKING,
				}),
				letterSpacing: LABEL_TRACKING,
			})}
		/>
		<Text
			x={b.cx}
			y={b.cy + metrics.panelH * 0.18}
			anchor={0.5}
			text={b.value}
			eventMode="none"
			style={trValueStyle({
				fill: VALUE_COLOR,
				fontSize: fitFontSize(b.value, {
					role: 'value',
					base: b.valueSize,
					maxWidth: b.w * 0.68,
					letterSpacing: VALUE_TRACKING,
				}),
				letterSpacing: VALUE_TRACKING,
				stroke: INK_STROKE,
				dropShadow: INK_SHADOW,
			})}
		/>
	{/each}
</Container>
