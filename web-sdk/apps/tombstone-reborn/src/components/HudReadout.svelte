<script lang="ts">
	/**
	 * WAYS / MULTI / WIN as stacked timber boxes — four boards + corner scraps
	 * baked from HUD-only wood (not the reel-frame sheet). Desktop sits this
	 * to the right of the board; narrow layouts sit it under the board.
	 */
	import { Container, Sprite, Text } from 'pixi-svelte';

	import { hudColor } from '../game/hud.generated';
	import { TR_INK_BRASS, fitFontSize, trLabelStyle, trValueStyle } from '../game/typography';

	export type HudReadoutSlot = { label: string; value: string; w?: number };

	const BOX_KEY: Record<string, 'woodReadoutWays' | 'woodReadoutMulti' | 'woodReadoutWin'> = {
		WAYS: 'woodReadoutWays',
		MULTI: 'woodReadoutMulti',
		WIN: 'woodReadoutWin',
		'FREE SPINS': 'woodReadoutMulti',
	};

	type Props = {
		slots: HudReadoutSlot[];
		x: number;
		y: number;
		wellW: number;
		/** 'y' = one column (desktop). 'x' = one row (narrow). */
		axis?: 'x' | 'y';
		/** rusty chains behind each box, hanging it from above */
		hang?: boolean;
		/** parent-space Y the chains drop from (screen top or board lip) */
		chainFromY?: number;
		/** override gap between boxes (default 8% of block height) */
		gap?: number;
		/** chains behind the timber, boxes in front */
		parts?: 'all' | 'chains' | 'boxes';
	};

	const props: Props = $props();

	/** wood_readout_*.png is 640x400 */
	const PLAQUE_ASPECT = 1.6;
	/** hud_chain.png — keep this ratio so links never stretch */
	const CHAIN_ASPECT = 1501 / 302;
	/** hud_chain.png — keep this ratio so links never stretch */
	const CHAIN_HW = 1501 / 302;
	/** dark inset well, as fractions of the baked sprite */
	const OPENING = { y0: 0.27, y1: 0.73 };
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

	const chainCols = (cx: number, cy: number, w: number, h: number) => {
		const chainBot = cy - h * 0.12;
		// Same link size as the sky hangs — a short drop must not squash the tile.
		const colW = Math.max(11, Math.min(w * 0.1, 18));
		const colH = colW * CHAIN_ASPECT;
		let chainTop = props.chainFromY != null ? props.chainFromY - props.y : cy - h * 1.15;
		if (chainBot - chainTop < colH) chainTop = chainBot - colH;
		const drop = chainBot - chainTop;
		const copies = Math.max(1, Math.ceil(drop / colH - 0.02));
		const inset = w * 0.22;
		const segs: { id: string; x: number; y: number; w: number; h: number }[] = [];
		for (let i = 0; i < copies; i += 1) {
			const y = chainTop + i * colH;
			segs.push({ id: `l${i}`, x: cx - inset, y, w: colW, h: colH });
			segs.push({ id: `r${i}`, x: cx + inset, y, w: colW, h: colH });
		}
		return segs;
	};

	const metrics = $derived.by(() => {
		const wellW = props.wellW;
		const blockH = wellW / PLAQUE_ASPECT;
		const stackGap = props.gap ?? blockH * 0.08;
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
						key: BOX_KEY[slot.label] ?? 'woodReadoutWays',
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
				key: BOX_KEY[slot.label] ?? 'woodReadoutWays',
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
		{#if props.hang !== false && props.parts !== 'boxes'}
			{#each chainCols(b.cx, b.cy, b.w, b.h) as seg (`${b.label}-${seg.id}`)}
				<Sprite
					key="hudChain"
					x={seg.x}
					y={seg.y}
					anchor={{ x: 0.5, y: 0 }}
					width={seg.w}
					height={seg.h}
					eventMode="none"
				/>
			{/each}
		{/if}
		{#if props.parts !== 'chains'}
		<Sprite
			key={b.key}
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
					maxWidth: b.w * 0.52,
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
					maxWidth: b.w * 0.52,
					letterSpacing: VALUE_TRACKING,
				}),
				letterSpacing: VALUE_TRACKING,
				stroke: INK_STROKE,
				dropShadow: INK_SHADOW,
			})}
		/>
		{/if}
	{/each}
</Container>
