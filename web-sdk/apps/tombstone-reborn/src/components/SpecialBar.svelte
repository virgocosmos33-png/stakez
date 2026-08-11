<script lang="ts">
	/**
	 * Side rails around the board:
	 *   LEFT  — six special-bar cells (one per reel) as an iron-framed charred
	 *           plank of ornate nameplates. Special symbols only.
	 *   RIGHT — WAYS (top) + WIN (bottom) as SEPARATE ornate plaques (no shared
	 *           container plank), only when the left rail stands upright
	 *           (desktop/wide).
	 *
	 * On narrow layouts the left rail lies flat above the board and cannot carry
	 * the readouts, so FrameMorphHud shows WAYS/WIN under the board instead; the
	 * vertical decision is shared (game/specialBarLayout.ts) so the two never
	 * both draw them.
	 *
	 * Baked sprites (Scenario transparent PNGs → tools/make_special_bar_art.py):
	 *   bar_rail         — iron frame + skull + solid opaque near-black wood
	 *   bar_plaque       — hollow pewter nameplate, tinted for EMPTY slots
	 *   bar_plaque_*     — per-kind plaques with baked embossed labels
	 *
	 * The LEFT rail is a nine-slice so the iron corners and rivets stay crisp while
	 * the wood run stretches. Empty sockets use the hollow frame + charcoal fill.
	 * Revealed cards use the colored labeled plaque sprites (no runtime Text).
	 */
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import * as PIXI from 'pixi.js';
	import { Container, Sprite, Text, getContextParent } from 'pixi-svelte';
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import SpecialBarPlaque from './SpecialBarPlaque.svelte';
	import FeatureFxSprite from './FeatureFxSprite.svelte';

	import { FX, seqFrame, fxRandom } from '../game/featureVfx';
	import { getContext } from '../game/context';
	import config from '../game/config';
	import { NUM_ROWS } from '../game/constants';
	import {
		PLAQUE_WIDTH_FRACTION,
		MAX_RAIL_W,
		MIN_SIDE_WIDTH,
		BOARD_GAP,
		PLATE_OVERHANG,
		EDGE_MARGIN,
	} from '../game/specialBarLayout';
	import { getSymbolX } from '../game/utils';
	import { stateShake } from '../game/stateShake.svelte';
	import { fxDur } from '../game/fxTiming';
	import { formatWays } from '../game/waysFormat';
	import { hudColor } from '../game/hud.generated';
	import { TR_INK_BRASS, fitFontSize, trLabelStyle, trValueStyle } from '../game/typography';

	const context = getContext();
	const parentContext = getContextParent();

	const REELS = NUM_ROWS.length;

	// --- baked art (tools/make_special_bar_art.py prints these) ----------------
	/** bar_plaque.png is 384x192 */
	const PLAQUE_ASPECT = 384 / 192;
	/** bar_readout_plaque.png is 1200x800 (tools/make_readout_plaque.py) — the
	 *  ornate WAYS/WIN nameplate. Its dark inset panel, as fractions, is where the
	 *  gold text seats (inside the beaded border). */
	const READOUT_ASPECT = 1.5;
	const READOUT_OPENING = { y0: 0.19, y1: 0.81 };
	/** the frame's hollow, as fractions of the texture (from punch_hollow) */
	const PLAQUE_OPENING = { x0: 0.0729, x1: 0.9271, y0: 0.2604, y1: 0.7344 };
	const OPENING_CY = (PLAQUE_OPENING.y0 + PLAQUE_OPENING.y1) * 0.5;
	/** bar_rail.webp is 320x960; rivet band reaches ~45px in */
	const RAIL_TEXTURE_W = 320;
	const RAIL_INSET = 45;

	// --- proportions ------------------------------------------------------------
	/** vertical step between plaques — leave a strip of plank + skull between */
	const PITCH_FACTOR = 1.38;
	/** wood left above the first well and below the last, in rail widths */
	const RAIL_PAD_FRACTION = 0.16;

	// --- WAYS / WIN readouts (separate plaques, vertical layout only) -----------
	/** scale the free-floating WAYS/WIN plaques past the special-bar cell size */
	const READOUT_SCALE = 1.28;
	const VALUE_COLOR = hudColor('text', 0xf0e6d0);
	const LABEL_COLOR = TR_INK_BRASS;
	const LABEL_TRACKING = 2;
	const VALUE_TRACKING = 0.3;
	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);

	let ways = $state(BASE_WAYS);
	context.eventEmitter.subscribeOnMount({
		waysCounterUpdate: (e) => {
			ways = e.ways;
		},
		waysCounterHide: () => {
			ways = BASE_WAYS;
		},
	});
	const winValue = $derived(bookEventAmountToCurrencyString(stateBet.winBookEventAmount));

	/** per-kind Scenario plaques with baked embossed labels */
	const KIND_SPRITE: Record<string, string> = {
		split_gang: 'barPlaqueGang',
		split_outlaws: 'barPlaqueOutlaw',
		gunsmoke: 'barPlaqueSmoke',
		digup: 'barPlaqueDigup',
		coffin: 'barPlaqueOpen',
	};

	/** empty plaques stay mounted as six solid slots — full opacity, cold bone
	 *  metal. Never fade them: translucent frames against the plank is exactly
	 *  the washed "wood with opacity" look the refs do not have. */
	const EMPTY_TINT = 0x9a9084;
	const EMPTY_ALPHA = 1;

	type BarCard = { reel: number; kind: string };

	/** keyed by reel so empty plaques stay painted */
	const cardsByReel = $derived.by(() => {
		const map = new Map<number, BarCard>();
		for (const cell of context.stateGame.specialBar) {
			map.set(cell.reel, cell);
		}
		return map;
	});

	/** 0 = seated, 1 = just struck; drives the pop a landing card makes */
	const enter = new Tween(0);

	$effect(() => {
		const cards = context.stateGame.specialBar;
		if (cards.length === 0) {
			enter.set(0, { duration: 0 });
			return;
		}
		// touch revealNonce so a fresh spin with the same card set still pops
		void context.stateGame.revealNonce;
		enter.set(1, { duration: 0 });
		enter.set(0, { duration: fxDur(420), easing: backOut });
	});

	const layout = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const originX = board.x - board.width * 0.5 + stateShake.x;
		const originRight = board.x + board.width * 0.5 + stateShake.x;
		const boardTop = board.y - board.height * 0.5 + stateShake.y;
		const boardCy = board.y + stateShake.y;

		// clear room the layout leaves left of the wooden plate
		const railRight = originX - PLATE_OVERHANG - BOARD_GAP;
		const sideWidth = railRight - EDGE_MARGIN;

		if (sideWidth >= MIN_SIDE_WIDTH) {
			const railW = Math.min(MAX_RAIL_W, sideWidth);
			const cellW = railW * PLAQUE_WIDTH_FRACTION;
			const cellH = cellW / PLAQUE_ASPECT;
			const pitch = cellH * PITCH_FACTOR;
			const stackH = pitch * (REELS - 1) + cellH;

			// LEFT rail: special-symbol plaques only (no WAYS/WIN ends).
			const pad = railW * RAIL_PAD_FRACTION;
			const railH = stackH + pad * 2;
			const cx = railRight - railW * 0.5;
			const railTop = boardCy - railH * 0.5;
			// centre the FRAMES on the stack, not their textures: the skull hangs
			// below each frame, so a box-centred stack reads as sitting high
			const skullBias = (0.5 - OPENING_CY) * cellH;
			const firstCy = railTop + pad + cellH * 0.5 + skullBias;

			// RIGHT: two free-floating ornate plaques (WAYS top, WIN bottom) —
			// no shared container plank. Slightly larger than a special-bar cell,
			// centered in the side strip and pinned near the top/bottom of the
			// left rail so they still bookend the board.
			const railLeftR = originRight + PLATE_OVERHANG + BOARD_GAP;
			const wellW = cellW * READOUT_SCALE;
			const wellH = wellW / READOUT_ASPECT;
			const cxR = railLeftR + railW * 0.5;
			const waysCy = railTop + pad + wellH * 0.5;
			const winCy = railTop + railH - pad - wellH * 0.5;

			return {
				vertical: true,
				cellW,
				cellH,
				cells: Array.from({ length: REELS }, (_, reel) => ({
					reel,
					cx,
					cy: firstCy + pitch * reel,
				})),
				rail: { x: railRight - railW, y: railTop, w: railW, h: railH },
				waysWell: { cx: cxR, cy: waysCy, w: wellW, h: wellH },
				winWell: { cx: cxR, cy: winCy, w: wellW, h: wellH },
			};
		}

		// narrow: the rail lies down above the board, one plaque over each reel.
		// WAYS/WIN move to FrameMorphHud here (no room for a right readout column).
		// MAX_RAIL_W * PLAQUE_WIDTH_FRACTION === one card wide (SYMBOL_CARD_W).
		const cellW = MAX_RAIL_W * PLAQUE_WIDTH_FRACTION;
		const cellH = cellW / PLAQUE_ASPECT;
		const thickness = cellH + (cellW / PLAQUE_WIDTH_FRACTION) * RAIL_PAD_FRACTION * 2;
		const railBottom = boardTop - BOARD_GAP;
		const cy = railBottom - thickness * 0.5;
		const cells = Array.from({ length: REELS }, (_, reel) => ({
			reel,
			cx: originX + getSymbolX(reel),
			cy,
		}));
		const left = cells[0].cx - cellW * 0.5 - thickness * RAIL_PAD_FRACTION;
		const right = cells[REELS - 1].cx + cellW * 0.5 + thickness * RAIL_PAD_FRACTION;

		return {
			vertical: false,
			cellW,
			cellH,
			cells,
			rail: { x: left, y: railBottom - thickness, w: right - left, h: thickness },
			waysWell: null,
			winWell: null,
		};
	});

	const pop = $derived(1 + 0.22 * enter.current);
	/** 0 → 1 across the strike, so the hit FX can run forwards while `enter`
	 * eases the plaque back down. */
	const strike = $derived(1 - enter.current);

	// pixi-svelte has no NineSlice component — same escape hatch as BoardFrame.
	// LEFT specials rail only; WAYS/WIN are free plaques (no right container).
	const railSprite = (() => {
		const s = new PIXI.NineSliceSprite({
			texture: PIXI.Texture.EMPTY,
			leftWidth: RAIL_INSET,
			topHeight: RAIL_INSET,
			rightWidth: RAIL_INSET,
			bottomHeight: RAIL_INSET,
		});
		s.eventMode = 'none';
		s.zIndex = -1;
		parentContext.addToParent(s);
		return s;
	})();

	onDestroy(() => {
		railSprite.removeFromParent();
		railSprite.destroy();
	});

	const placeRail = (
		sprite: PIXI.NineSliceSprite,
		rail: { x: number; y: number; w: number; h: number },
		vertical: boolean,
	) => {
		// panel is drawn upright: upright = rail size, laid down = thickness×span
		// then a quarter turn. Uniform scale keeps iron rivets round.
		const thickness = vertical ? rail.w : rail.h;
		const span = vertical ? rail.h : rail.w;
		const scale = thickness / RAIL_TEXTURE_W;
		sprite.scale.set(scale);
		sprite.width = RAIL_TEXTURE_W;
		sprite.height = span / scale;
		sprite.rotation = vertical ? 0 : -Math.PI / 2;
		sprite.x = rail.x;
		sprite.y = vertical ? rail.y : rail.y + thickness;
	};

	$effect(() => {
		const texture = context.stateApp.loadedAssets?.['barRail'] as PIXI.Texture | undefined;
		if (texture && railSprite.texture !== texture) railSprite.texture = texture;
		placeRail(railSprite, layout.rail, layout.vertical);
	});

</script>

{#each layout.cells as cell (cell.reel)}
	{@const card = cardsByReel.get(cell.reel)}
	{@const kindSprite = card ? (KIND_SPRITE[card.kind] ?? '') : ''}
	<SpecialBarPlaque
		reel={cell.reel}
		cx={cell.cx}
		cy={cell.cy}
		w={layout.cellW}
		h={layout.cellH}
		opening={PLAQUE_OPENING}
		spriteKey={kindSprite || 'barPlaque'}
		bakedLabel={Boolean(kindSprite)}
		tint={kindSprite ? 0xffffff : EMPTY_TINT}
		alpha={card ? 1 : EMPTY_ALPHA}
		blankTint={EMPTY_TINT}
		blankAlpha={EMPTY_ALPHA}
		{pop}
		active={Boolean(card) && context.stateGame.specialBarActiveKind === card?.kind}
	/>

	<!-- SPECIAL BAR HIT: a card struck into its socket throws powder smoke and
	spent brass. Only lit sockets get it, and it clears as the plaque seats. -->
	{#if card && strike < 0.995}
		{@const seed = cell.reel * 29 + 7}
		<FeatureFxSprite
			tex={seqFrame(FX.flash, strike / 0.45)}
			x={cell.cx}
			y={cell.cy}
			width={layout.cellW * (0.9 + strike * 1.4)}
			height={layout.cellW * (0.9 + strike * 1.4)}
			alpha={strike < 0.45 ? 0.85 * (1 - strike / 0.45) : 0}
		/>
		<FeatureFxSprite
			tex={seqFrame(FX.gunsmoke, strike)}
			x={cell.cx - layout.cellW * 0.16 * strike}
			y={cell.cy - layout.cellH * (0.2 + 0.9 * strike)}
			width={layout.cellW * (0.7 + strike * 0.7)}
			height={layout.cellW * (0.7 + strike * 0.7)}
			alpha={0.4 * Math.min(1, strike / 0.2) * (1 - strike)}
		/>
		{#each FX.spark as sparkFrame, i}
			{@const spread = fxRandom(seed + i * 11)}
			<FeatureFxSprite
				tex={sparkFrame}
				x={cell.cx + (spread - 0.5) * layout.cellW * 1.9 * strike}
				y={cell.cy + layout.cellH * (-0.5 * strike + 1.4 * strike * strike)}
				width={layout.cellW * 0.34}
				height={layout.cellW * 0.34}
				rotation={strike * (spread - 0.5) * 8}
				alpha={0.9 * (1 - strike)}
			/>
		{/each}
	{/if}
{/each}

{#snippet valueWell(well: { cx: number; cy: number; w: number; h: number }, label: string, value: string)}
	<!-- text seats inside the plaque's dark inset panel (the beaded border), so
		sizes/positions are struck off the OPENING, not the whole sprite -->
	{@const panelH = (READOUT_OPENING.y1 - READOUT_OPENING.y0) * well.h}
	{@const panelW = well.w * 0.68}
	{@const labelSize = Math.max(8, Math.floor(panelH * 0.26))}
	{@const valueSize = Math.max(12, Math.floor(panelH * 0.46))}
	<Container x={well.cx} y={well.cy}>
		<Sprite key="barReadoutPlaque" anchor={0.5} width={well.w} height={well.h} eventMode="none" />
		<Text
			x={0}
			y={-panelH * 0.24}
			anchor={0.5}
			text={label}
			eventMode="none"
			style={trLabelStyle({
				fill: LABEL_COLOR,
				fontSize: fitFontSize(label, {
					role: 'label',
					base: labelSize,
					maxWidth: panelW,
					letterSpacing: LABEL_TRACKING,
				}),
				letterSpacing: LABEL_TRACKING,
			})}
		/>
		<Text
			x={0}
			y={panelH * 0.18}
			anchor={0.5}
			text={value}
			eventMode="none"
			style={trValueStyle({
				fill: VALUE_COLOR,
				fontSize: fitFontSize(value, {
					role: 'value',
					base: valueSize,
					maxWidth: panelW,
					letterSpacing: VALUE_TRACKING,
				}),
				letterSpacing: VALUE_TRACKING,
				stroke: { color: 0x05070a, width: 2 },
				dropShadow: { color: 0x000000, blur: 3, distance: 1, alpha: 0.6, angle: Math.PI / 2 },
			})}
		/>
	</Container>
{/snippet}

{#if layout.vertical && layout.waysWell && layout.winWell}
	{@render valueWell(layout.waysWell, 'WAYS', formatWays(ways))}
	{@render valueWell(layout.winWell, 'WIN', winValue)}
{/if}
