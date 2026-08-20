<script lang="ts">
	/**
	 * WAYS / MULTI / WIN / FREE SPINS as stacked timber boxes. A labeled
	 * wood pallet sits on top of each box; the well only shows the
	 * number. Desktop sits this to the right of the board; narrow layouts
	 * sit it under the board.
	 */
	import type { Texture } from 'pixi.js';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { hudColor } from '../game/hud.generated';
	import { multiHang, multiHangPose, syncMultiHang } from '../game/multiHang';
	import { fitFontSize, trValueStyle } from '../game/typography';

	export type HudReadoutSlot = { label: string; value: string; w?: number };

	const BOX_BASE: Record<
		string,
		'woodReadoutWays' | 'woodReadoutMulti' | 'woodReadoutWin' | 'woodReadoutSpins'
	> = {
		WAYS: 'woodReadoutWays',
		MULTI: 'woodReadoutMulti',
		WIN: 'woodReadoutWin',
		'FREE SPINS': 'woodReadoutSpins',
	};

	const PALLET_BASE: Record<
		string,
		'woodPalletWays' | 'woodPalletMulti' | 'woodPalletWin' | 'woodPalletSpins'
	> = {
		WAYS: 'woodPalletWays',
		MULTI: 'woodPalletMulti',
		WIN: 'woodPalletWin',
		'FREE SPINS': 'woodPalletSpins',
	};

	const context = getContext();
	const boxKey = (label: string) => {
		const base = BOX_BASE[label] ?? 'woodReadoutWays';
		const atmo = context.stateGame.atmosphere;
		if (atmo === 'super') return `${base}Super`;
		if (atmo === 'small') return `${base}Small`;
		return base;
	};

	const palletKey = (label: string) => {
		const base = PALLET_BASE[label] ?? 'woodPalletWays';
		const atmo = context.stateGame.atmosphere;
		if (atmo === 'super' && label !== 'FREE SPINS') return `${base}Super`;
		if (atmo === 'small' && label !== 'FREE SPINS') return `${base}Small`;
		return base;
	};

	const chainKey = () => 'hudChain';

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
		/** chains / plate behind the timber; wood + pallet + number in front */
		parts?: 'all' | 'chains' | 'plate' | 'boxes';
		/** occupy layout but stay invisible (base MULTI at 1×) */
		heldLabels?: string[];
	};

	const props: Props = $props();
	const parts = $derived(props.parts ?? 'all');
	const hasMulti = $derived(props.slots.some((slot) => slot.label === 'MULTI'));
	const multiLive = $derived(hasMulti && !(props.heldLabels ?? []).includes('MULTI'));

	$effect(() => {
		if (!hasMulti) return;
		syncMultiHang(multiLive);
	});

	/** wood_readout_*.png is 640x400 */
	const PLAQUE_ASPECT = 1.6;
	/** share the end oval with the next copy so links interlock */
	const CHAIN_TILE_STEP = 0.84;
	const OPENING = { x0: 0.2156, x1: 0.7844, y0: 0.305, y1: 0.695 };
	const PLATE = { x0: 0.2, x1: 0.8, y0: 0.28, y1: 0.72 };
	const VALUE_COLOR = hudColor('text', 0xf0e6d0);
	const VALUE_TRACKING = 0.3;
	const INK_STROKE = { color: 0x05070a, width: 2 } as const;
	const INK_SHADOW = {
		color: 0x000000,
		blur: 3,
		distance: 1,
		alpha: 0.6,
		angle: Math.PI / 2,
	} as const;

	const chainAspect = $derived.by(() => {
		const tex = context.stateApp.loadedAssets?.[chainKey()] as Texture | undefined;
		if (tex?.width) return tex.height / tex.width;
		return 16 / 9;
	});

	const palletAspectOf = (key: string) => {
		const tex = context.stateApp.loadedAssets?.[key] as Texture | undefined;
		if (tex?.width) return tex.height / tex.width;
		return 0.28;
	};

	const palletOf = (cx: number, cy: number, w: number, h: number, key: string) => {
		// Cover the box's existing top beam (WELL.top = 112/400). Do not hang
		// a second plank above it — that was the double pallet.
		const topBeam = 112 / 400;
		const pw = w * 1.02;
		const ph = Math.min(h * 0.2, pw * palletAspectOf(key));
		return { x: cx, y: cy - h * 0.5 + topBeam * h, w: pw, h: ph };
	};

	const chainCols = (cx: number, chainBot: number, w: number, h: number) => {
		const colW = Math.max(11, Math.min(w * 0.1, 18));
		const colH = colW * chainAspect;
		const step = colH * CHAIN_TILE_STEP;
		let chainTop =
			props.chainFromY != null ? props.chainFromY - props.y - colH * 0.45 : chainBot - h * 1.03;
		if (chainBot - chainTop < colH) chainTop = chainBot - colH;
		const drop = Math.max(colH, chainBot - chainTop);
		const copies = Math.max(1, Math.ceil(drop / step));
		const inset = w * 0.22;
		const segs: { id: string; x: number; y: number; w: number; h: number }[] = [];
		for (let i = 0; i < copies; i += 1) {
			const y = chainTop + i * step;
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
		const plateH = (PLATE.y1 - PLATE.y0) * blockH;
		const valueSize = Math.max(11, Math.floor(Math.min(panelH * 0.34, plateH * 0.4)));
		const axis = props.axis ?? 'y';
		const widths = props.slots.map((slot) => slot.w ?? wellW);
		const n = props.slots.length;
		if (n === 0) return { blocks: [] as const };

		const block = (slot: HudReadoutSlot, cx: number, cy: number, w: number) => {
			const pKey = palletKey(slot.label);
			const pallet = palletOf(cx, cy, w, blockH, pKey);
			return {
				label: slot.label,
				value: slot.value,
				key: boxKey(slot.label),
				palletKey: pKey,
				cx,
				cy,
				w,
				h: blockH,
				valueSize,
				pallet,
			};
		};

		if (axis === 'x') {
			const totalW = widths.reduce((sum, w) => sum + w, 0) + stackGap * (n - 1);
			let cursor = -totalW / 2;
			return {
				blocks: props.slots.map((slot, i) => {
					const w = widths[i];
					const cx = cursor + w / 2;
					cursor += w + stackGap;
					return block(slot, cx, 0, w);
				}),
			};
		}

		const totalH = n * blockH + (n - 1) * stackGap;
		return {
			blocks: props.slots.map((slot, i) =>
				block(slot, 0, -totalH / 2 + blockH / 2 + i * (blockH + stackGap), widths[i]),
			),
		};
	});

	const hangChains = (localBot: number, w: number) => {
		const colW = Math.max(11, Math.min(w * 0.1, 18));
		const colH = colW * chainAspect;
		const step = colH * CHAIN_TILE_STEP;
		const drop = Math.max(colH, localBot);
		const copies = Math.max(1, Math.ceil(drop / step));
		const inset = w * 0.22;
		const segs: { id: string; x: number; y: number; w: number; h: number }[] = [];
		for (let i = 0; i < copies; i += 1) {
			const y = i * step;
			if (y > localBot + colH * 0.2) break;
			segs.push({ id: `l${i}`, x: -inset, y, w: colW, h: colH });
			segs.push({ id: `r${i}`, x: inset, y, w: colW, h: colH });
		}
		return segs;
	};

	const hangOf = (b: (typeof metrics.blocks)[number]) => {
		if (b.label !== 'MULTI') return null;
		const t = multiHang.current;
		if (t <= 0.001 && !multiLive) return { hide: true as const };
		const hingeY =
			props.chainFromY != null ? props.chainFromY - props.y : b.cy - b.h * 1.35;
		const seated = b.cy - hingeY;
		const pose = multiHangPose(t);
		return {
			hide: false as const,
			hingeY,
			localY: seated * t,
			swing: pose.swing,
			sway: pose.sway,
		};
	};
</script>

{#snippet blockFace(b: (typeof metrics.blocks)[number], ox: number, oy: number)}
	{#if parts === 'all' || parts === 'plate'}
		<Rectangle
			x={ox}
			y={oy}
			anchor={0.5}
			width={b.w * (PLATE.x1 - PLATE.x0)}
			height={b.h * (PLATE.y1 - PLATE.y0)}
			borderRadius={Math.max(4, b.h * 0.04)}
			backgroundColor={0x000000}
			eventMode="none"
		/>
	{/if}
	{#if parts === 'all' || parts === 'boxes'}
		<Sprite
			key={b.key}
			x={ox}
			y={oy}
			anchor={0.5}
			width={b.w}
			height={b.h}
			eventMode="none"
		/>
		<Sprite
			key={b.palletKey}
			x={ox + (b.pallet.x - b.cx)}
			y={oy + (b.pallet.y - b.cy)}
			anchor={0.5}
			width={b.pallet.w}
			height={b.pallet.h}
			eventMode="none"
		/>
		<Text
			x={ox}
			y={oy}
			anchor={0.5}
			text={b.value}
			eventMode="none"
			style={trValueStyle({
				fill: VALUE_COLOR,
				fontSize: fitFontSize(b.value, {
					role: 'value',
					base: b.valueSize,
					maxWidth: b.w * (PLATE.x1 - PLATE.x0) * 0.88,
					min: 9,
					letterSpacing: VALUE_TRACKING,
				}),
				letterSpacing: VALUE_TRACKING,
				stroke: INK_STROKE,
				dropShadow: INK_SHADOW,
			})}
		/>
	{/if}
{/snippet}

<Container x={props.x} y={props.y}>
	{#each metrics.blocks as b (b.label)}
		{@const hang = hangOf(b)}
		{#if !hang?.hide}
			{#if hang}
				<Container x={b.cx + hang.sway} y={hang.hingeY} rotation={hang.swing} eventMode="none">
					{#if props.hang !== false && (parts === 'all' || parts === 'chains')}
						{#each hangChains(hang.localY + (b.pallet.y - b.cy) - b.pallet.h * 0.38, b.w) as seg (`${b.label}-${seg.id}`)}
							<Sprite
								key={chainKey()}
								x={seg.x}
								y={seg.y}
								anchor={{ x: 0.5, y: 0 }}
								width={seg.w}
								height={seg.h}
								eventMode="none"
							/>
						{/each}
					{/if}
					{@render blockFace(b, 0, hang.localY)}
				</Container>
			{:else}
				{#if props.hang !== false && (parts === 'all' || parts === 'chains')}
					{#each chainCols(b.cx, b.pallet.y - b.pallet.h * 0.38, b.w, b.h) as seg (`${b.label}-${seg.id}`)}
						<Sprite
							key={chainKey()}
							x={seg.x}
							y={seg.y}
							anchor={{ x: 0.5, y: 0 }}
							width={seg.w}
							height={seg.h}
							eventMode="none"
						/>
					{/each}
				{/if}
				{@render blockFace(b, b.cx, b.cy)}
			{/if}
		{/if}
	{/each}
</Container>
