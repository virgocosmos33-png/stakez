<script lang="ts">
	/**
	 * The six special-bar cells — one per reel — as an iron-framed charred
	 * plank of ornate nameplates standing down the LEFT of the board.
	 *
	 * Baked sprites (Scenario transparent PNGs → tools/make_special_bar_art.py):
	 *   bar_rail         — iron frame + skull + solid opaque near-black wood
	 *   bar_plaque       — hollow pewter nameplate, tinted for EMPTY slots
	 *   bar_plaque_*     — per-kind plaques with baked embossed labels
	 *
	 * The rail is a nine-slice so the iron corners and rivets stay crisp while
	 * the wood run stretches to the six plaques. Never strip the frame and
	 * fake an edge in code — that is what read as washed translucent wood.
	 *
	 * Empty sockets use the hollow frame + charcoal fill. Revealed cards use
	 * the colored labeled plaque sprites (no runtime Text). The column reels
	 * with the board. On narrow layouts the rail lies down above the board.
	 */
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import * as PIXI from 'pixi.js';
	import { getContextParent } from 'pixi-svelte';

	import SpecialBarPlaque from './SpecialBarPlaque.svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, SYMBOL_CARD_W, NUM_ROWS, BOARD_PLATE_PAD } from '../game/constants';
	import { getSymbolX } from '../game/utils';
	import { stateShake } from '../game/stateShake.svelte';
	import { fxDur } from '../game/fxTiming';

	const context = getContext();
	const parentContext = getContextParent();

	const REELS = NUM_ROWS.length;

	// --- baked art (tools/make_special_bar_art.py prints these) ----------------
	/** bar_plaque.png is 384x192 */
	const PLAQUE_ASPECT = 384 / 192;
	/** the frame's hollow, as fractions of the texture (from punch_hollow) */
	const PLAQUE_OPENING = { x0: 0.0729, x1: 0.9271, y0: 0.2604, y1: 0.7344 };
	const OPENING_CY = (PLAQUE_OPENING.y0 + PLAQUE_OPENING.y1) * 0.5;
	/** bar_rail.webp is 320x960; rivet band reaches ~45px in */
	const RAIL_TEXTURE_W = 320;
	const RAIL_INSET = 45;

	// --- proportions ------------------------------------------------------------
	/** plaques sit inside the wood field, clear of the iron rivet band */
	const PLAQUE_WIDTH_FRACTION = 0.70;
	/** vertical step between plaques — leave a strip of plank + skull between */
	const PITCH_FACTOR = 1.38;
	/** wood left above the first plaque and below the last, in rail widths */
	const RAIL_PAD_FRACTION = 0.16;
	/** one card wide, like the reels it belongs to */
	const MAX_RAIL_W = SYMBOL_CARD_W / PLAQUE_WIDTH_FRACTION;
	/** below this the side margin cannot hold a readable cell — lie the rail down */
	const MIN_SIDE_WIDTH = MAX_RAIL_W * 0.8;

	const BOARD_GAP = SYMBOL_SIZE * 0.12;
	/** BoardPlate's wooden face overhangs the board box by its own PAD */
	const PLATE_OVERHANG = BOARD_PLATE_PAD;
	const EDGE_MARGIN = 6;

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
			const railH = stackH + railW * RAIL_PAD_FRACTION * 2;
			const cx = railRight - railW * 0.5;
			// centre the FRAMES on the rail, not their textures: the skull hangs
			// below each frame, so a box-centred stack reads as sitting high
			const skullBias = (0.5 - OPENING_CY) * cellH;
			const firstCy = boardCy - stackH * 0.5 + cellH * 0.5 + skullBias;

			return {
				vertical: true,
				cellW,
				cellH,
				cells: Array.from({ length: REELS }, (_, reel) => ({
					reel,
					cx,
					cy: firstCy + pitch * reel,
				})),
				rail: { x: railRight - railW, y: boardCy - railH * 0.5, w: railW, h: railH },
			};
		}

		// narrow: the rail lies down above the board, one plaque over each reel
		const cellW = SYMBOL_CARD_W;
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
		};
	});

	const pop = $derived(1 + 0.22 * enter.current);

	// pixi-svelte has no NineSlice component — same escape hatch as BoardFrame
	const railSprite = new PIXI.NineSliceSprite({
		texture: PIXI.Texture.EMPTY,
		leftWidth: RAIL_INSET,
		topHeight: RAIL_INSET,
		rightWidth: RAIL_INSET,
		bottomHeight: RAIL_INSET,
	});
	railSprite.eventMode = 'none';
	railSprite.zIndex = -1;
	parentContext.addToParent(railSprite);

	onDestroy(() => {
		railSprite.removeFromParent();
		railSprite.destroy();
	});

	$effect(() => {
		const texture = context.stateApp.loadedAssets?.['barRail'] as PIXI.Texture | undefined;
		if (texture && railSprite.texture !== texture) railSprite.texture = texture;

		const { rail, vertical } = layout;
		// panel is drawn upright: upright = rail size, laid down = thickness×span
		// then a quarter turn. Uniform scale keeps iron rivets round.
		const thickness = vertical ? rail.w : rail.h;
		const span = vertical ? rail.h : rail.w;
		const scale = thickness / RAIL_TEXTURE_W;
		railSprite.scale.set(scale);
		railSprite.width = RAIL_TEXTURE_W;
		railSprite.height = span / scale;
		railSprite.rotation = vertical ? 0 : -Math.PI / 2;
		railSprite.x = rail.x;
		railSprite.y = vertical ? rail.y : rail.y + thickness;
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
	/>
{/each}
