<script lang="ts" module>
	export type EmitterEventFrameMorphHud =
		| { type: 'waysCounterUpdate'; ways: number }
		| { type: 'waysCounterHide' }
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	/**
	 * Under-board STEEL CONSOLE — now a FALLBACK / bonus readout only.
	 *
	 * WAYS and WIN normally live as free plaques on the RIGHT (SpecialBar.svelte),
	 * opposite the left special-symbol bar. This console only draws them when
	 * that rail is laid FLAT (narrow/portrait) and cannot host them — the
	 * vertical decision is shared (game/specialBarLayout.ts) so exactly one
	 * place shows them. During free spins it also carries the FREE SPINS
	 * counter. When nothing needs showing (the common desktop base game) it
	 * renders nothing at all, so no console is wedged under the board or over
	 * the bet/spin HUD.
	 *
	 * The old scrolling info marquee was removed for this game.
	 */
	import * as PIXI from 'pixi.js';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Text } from 'pixi-svelte';
	import { stateBet, stateUi } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import config from '../game/config';
	import { BOARD_PLATE_PAD } from '../game/constants';
	import { COLUMN_ROW_OFFSET } from '../game/chassisArt';
	import { isSpecialBarVertical } from '../game/specialBarLayout';
	import { stateShake } from '../game/stateShake.svelte';
	import { formatWays } from '../game/waysFormat';
	import { hudColor } from '../game/hud.generated';
	import {
		TR_INK_BRASS,
		estimateTextWidth,
		fitFontSize,
		trLabelStyle,
		trValueStyle,
	} from '../game/typography';

	const context = getContext();

	const VALUE_COLOR = hudColor('text', 0xf0e6d0);
	const LABEL_COLOR = TR_INK_BRASS;
	const LABEL_TRACKING = 2;
	const VALUE_TRACKING = 0.3;

	const GAP = 6;
	/** air between BoardPlate bottom lip and the console top */
	const PLATE_CLEAR = 14;

	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);
	let ways = $state(BASE_WAYS);
	let spinsShow = $state(false);
	let spinsCurrent = $state(0);
	let spinsTotal = $state(0);

	context.eventEmitter.subscribeOnMount({
		waysCounterUpdate: (e) => {
			ways = e.ways;
		},
		waysCounterHide: () => {
			ways = BASE_WAYS;
		},
		freeSpinCounterShow: () => {
			spinsShow = true;
		},
		freeSpinCounterHide: () => {
			spinsShow = false;
		},
		freeSpinCounterUpdate: (e) => {
			if (e.current !== undefined) spinsCurrent = e.current;
			if (e.total !== undefined) spinsTotal = e.total;
		},
	});

	const layout = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const bw = board.width;
		const bh = board.height;
		const frameY = board.y;

		// WAYS/WIN belong to the free right plaques; only fall back here when the
		// side rails are laid flat (narrow). FREE SPINS always shows here in bonus.
		const barVertical = isSpecialBarVertical(board);
		const waysShow = !barVertical;
		const winShow = !barVertical;
		const anyShow = waysShow || winShow || spinsShow;
		if (!anyShow) return { anyShow: false } as const;

		const baseW = bw + 2 * GAP;
		const railH = 56;
		const railX = board.x + COLUMN_ROW_OFFSET;
		const plateBottom = frameY + bh / 2 + BOARD_PLATE_PAD;
		const preferredRailY = plateBottom + PLATE_CLEAR + railH / 2;
		const main = context.stateLayoutDerived.mainLayout();
		const canvasH = context.stateLayoutDerived.canvasSizes().height;
		const hudTopScreen = stateUi.hudBarTopScreenY;
		const HUD_CLEAR_PX = 12;
		const railFloor =
			hudTopScreen > 0
				? main.height / 2 + (hudTopScreen - HUD_CLEAR_PX - canvasH / 2) / main.scale - railH / 2
				: Number.POSITIVE_INFINITY;
		const railY = Math.min(preferredRailY, railFloor);

		const railRadius = railH * 0.24;
		const vPad = railH * 0.15;
		const wellH = railH - 2 * vPad;
		const wellRadius = wellH * 0.26;
		const sidePad = baseW * 0.024;
		const gap = baseW * 0.022;

		const valueFontSize = Math.max(12, Math.floor(wellH * 0.44));
		const labelFontSize = Math.max(8, Math.floor(wellH * 0.24));

		const innerPadX = wellH * 0.85;
		const minWell = baseW * 0.22;
		const contentW = (label: string, value: string) => {
			const valueW = estimateTextWidth(value, {
				role: 'value',
				fontSize: valueFontSize,
				letterSpacing: VALUE_TRACKING,
			});
			const labelW = estimateTextWidth(label, {
				role: 'label',
				fontSize: labelFontSize,
				letterSpacing: LABEL_TRACKING,
			});
			return Math.max(minWell, Math.max(valueW, labelW) + innerPadX);
		};

		const waysValue = formatWays(ways);
		const winValue = bookEventAmountToCurrencyString(stateBet.winBookEventAmount);
		const spinsValue = `${spinsTotal - spinsCurrent}/${spinsTotal}`;

		// only the showing readouts get a well, laid out left→right in a rail that
		// grows to fit them
		const defs = [
			waysShow ? { label: 'WAYS', value: waysValue } : null,
			spinsShow ? { label: 'FREE SPINS', value: spinsValue } : null,
			winShow ? { label: 'WIN', value: winValue } : null,
		].filter((d): d is { label: string; value: string } => d !== null);

		const widths = defs.map((d) => contentW(d.label, d.value));
		const railW = widths.reduce((t, w) => t + w, 0) + gap * (defs.length - 1) + 2 * sidePad;

		let cursor = -railW / 2 + sidePad;
		const localWells = widths.map((w) => {
			const cx = cursor + w / 2;
			cursor += w + gap;
			return { cx, cy: 0, w, h: wellH, r: wellRadius };
		});
		const slots = defs.map((d, i) => ({
			well: { cx: railX + localWells[i].cx, cy: railY, w: localWells[i].w, h: wellH },
			label: d.label,
			value: d.value,
		}));

		return {
			anyShow: true as const,
			railX,
			railY,
			railW,
			railH,
			railRadius,
			localWells,
			slots,
			valueFontSize,
			labelFontSize,
		};
	});

	type Layout = Extract<typeof layout, { anyShow: true }>;

	const vGradient = (stops: Array<[number, number]>) =>
		new PIXI.FillGradient({
			type: 'linear',
			start: { x: 0, y: 0 },
			end: { x: 0, y: 1 },
			colorStops: stops.map(([offset, color]) => ({ offset, color })),
			textureSpace: 'local',
		});
	const STEEL_GRAD = vGradient([
		[0, 0x1d1f23],
		[0.5, 0x131417],
		[1, 0x0c0d0f],
	]);
	const GLASS_GRAD = vGradient([
		[0, 0x08090c],
		[1, 0x020304],
	]);

	/** paint the console, in rail-local coords (shake is a Container) */
	const drawConsole = (g: PIXI.Graphics, L: Layout) => {
		const rw = L.railW;
		const rh = L.railH;
		const rr = L.railRadius;

		g.roundRect(-rw / 2, -rh / 2 + 4, rw, rh, rr).fill({ color: 0x000000, alpha: 0.38 });
		g.roundRect(-rw / 2, -rh / 2, rw, rh, rr).fill(STEEL_GRAD);
		g.roundRect(-rw / 2 + 1.5, -rh / 2 + 1.5, rw - 3, rh - 3, rr - 1).stroke({
			color: 0x33363c,
			width: 1.5,
			alpha: 0.6,
		});
		g.roundRect(-rw / 2, -rh / 2, rw, rh, rr).stroke({ color: 0x050607, width: 2 });

		for (const w of L.localWells) {
			const x = w.cx - w.w / 2;
			const y = w.cy - w.h / 2;
			g.roundRect(x - 1, y - 1, w.w + 2, w.h + 2, w.r + 1).fill({ color: 0x000000, alpha: 0.6 });
			g.roundRect(x, y, w.w, w.h, w.r).fill(GLASS_GRAD);
			g.roundRect(x + 2, y + 2, w.w - 4, w.h * 0.42, w.r).fill({ color: 0xffffff, alpha: 0.05 });
			g.roundRect(x, y, w.w, w.h, w.r).stroke({ color: 0x2a2d32, width: 1.5, alpha: 0.9 });
			g.roundRect(x + 1.5, y + 1.5, w.w - 3, w.h - 3, w.r).stroke({
				color: 0x030405,
				width: 1,
				alpha: 0.85,
			});
		}
	};
</script>

{#if layout.anyShow}
	{@const L = layout}
	<MainContainer>
		<!-- shake is a cheap Container translate so it never re-runs the console
			draw (geometry is computed shake-free) -->
		<Container x={stateShake.x} y={stateShake.y}>
			<Graphics x={L.railX} y={L.railY} draw={(g) => drawConsole(g, L)} />

			{#each L.slots as s (s.label)}
				<Container x={s.well.cx} y={s.well.cy}>
					<Text
						x={0}
						y={-s.well.h * 0.26}
						anchor={0.5}
						text={s.label}
						eventMode="none"
						style={trLabelStyle({
							fill: LABEL_COLOR,
							fontSize: fitFontSize(s.label, {
								role: 'label',
								base: L.labelFontSize,
								maxWidth: s.well.w * 0.9,
								letterSpacing: LABEL_TRACKING,
							}),
							letterSpacing: LABEL_TRACKING,
						})}
					/>
					<Text
						x={0}
						y={s.well.h * 0.16}
						anchor={0.5}
						text={s.value}
						eventMode="none"
						style={trValueStyle({
							fill: VALUE_COLOR,
							fontSize: fitFontSize(s.value, {
								role: 'value',
								base: L.valueFontSize,
								maxWidth: s.well.w * 0.88,
								letterSpacing: VALUE_TRACKING,
							}),
							letterSpacing: VALUE_TRACKING,
							stroke: { color: 0x05070a, width: 2 },
							dropShadow: { color: 0x000000, blur: 3, distance: 1, alpha: 0.6, angle: Math.PI / 2 },
						})}
					/>
				</Container>
			{/each}
		</Container>
	</MainContainer>
{/if}
