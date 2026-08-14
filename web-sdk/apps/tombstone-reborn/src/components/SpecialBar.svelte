<script lang="ts">
	/**
	 * Side chrome around the board:
	 *   LEFT  — six special-bar cells (one per reel) inside a timber frame
	 *           built from the SAME planks + iron plates as the reel board.
	 *   RIGHT — stacked WAYS + WIN nameplates (FREE SPINS inserted in bonus),
	 *           no timber slab, only when the left rail stands upright.
	 *
	 * On narrow layouts the left rail lies flat above the board and cannot carry
	 * the readouts, so FrameMorphHud shows the same stack under the board; the
	 * vertical decision is shared (game/specialBarLayout.ts) so the two never
	 * both draw them.
	 *
	 * Special-bar plaques stay the baked Scenario nameplates. WAYS/WIN keep
	 * their ornate plates; they just do not sit inside a woody frame.
	 */
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { Container } from 'pixi-svelte';
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import SpecialBarPlaque from './SpecialBarPlaque.svelte';
	import FeatureFxSprite from './FeatureFxSprite.svelte';
	import TimberRect from './TimberRect.svelte';
	import HudReadout from './HudReadout.svelte';

	import { FX, seqFrame, fxRandom } from '../game/featureVfx';
	import { getContext } from '../game/context';
	import config from '../game/config';
	import { NUM_ROWS, BOARD_FRAME_THICK, BOARD_FRAME_CORNER } from '../game/constants';
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

	const context = getContext();

	const REELS = NUM_ROWS.length;

	// --- baked art (tools/make_special_bar_art.py prints these) ----------------
	/** bar_plaque.png is 384x192 */
	const PLAQUE_ASPECT = 384 / 192;
	/** the frame's hollow, as fractions of the texture (from punch_hollow) */
	const PLAQUE_OPENING = { x0: 0.0729, x1: 0.9271, y0: 0.2604, y1: 0.7344 };

	// --- proportions ------------------------------------------------------------
	/** vertical step between plaques — leave a strip of wood between */
	const PITCH_FACTOR = 1.38;
	/** wood left above the first well and below the last, as a fraction of inner width */
	const RAIL_PAD_FRACTION = 0.12;

	// --- WAYS / WIN / FREE SPINS (stacked nameplates, vertical layout only) ---
	/** scale the readout plaques past the special-bar cell size */
	const READOUT_WIDTH_SCALE = 1.28;
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
		const s = board.scale;
		const originX = board.visualLeft + stateShake.x;
		const originRight = board.visualRight + stateShake.x;
		const boardTop = board.visualTop + stateShake.y;
		const boardCy = board.y + stateShake.y;

		// clear room the layout leaves left of the wooden plate
		const railRight = originX - PLATE_OVERHANG * s - BOARD_GAP * s;
		const sideWidth = railRight - EDGE_MARGIN;

		if (sideWidth >= MIN_SIDE_WIDTH) {
			const thick = BOARD_FRAME_THICK * s;
			const corner = BOARD_FRAME_CORNER * s;
			const outerW = Math.min(MAX_RAIL_W, sideWidth);
			const innerW = Math.max(8, outerW - 2 * thick);
			const cellW = innerW * PLAQUE_WIDTH_FRACTION;
			const cellH = cellW / PLAQUE_ASPECT;
			const pitch = cellH * PITCH_FACTOR;
			const stackH = pitch * (REELS - 1) + cellH;

			const pad = innerW * RAIL_PAD_FRACTION;
			const innerH = stackH + pad * 2;
			const innerX = railRight - thick - innerW;
			const cx = innerX + innerW * 0.5;
			const innerTop = boardCy - innerH * 0.5;
			const firstCy = innerTop + pad + cellH * 0.5;

			const railLeftR = originRight + PLATE_OVERHANG * s + BOARD_GAP * s;
			const wellW = cellW * READOUT_WIDTH_SCALE;
			const slots: { label: string; value: string }[] = [
				{ label: 'WAYS', value: formatWays(ways) },
			];
			if (spinsShow) {
				slots.push({
					label: 'FREE SPINS',
					value: `${spinsTotal - spinsCurrent}/${spinsTotal}`,
				});
			}
			slots.push({ label: 'WIN', value: winValue });

			return {
				vertical: true,
				thick,
				corner,
				cellW,
				cellH,
				cells: Array.from({ length: REELS }, (_, reel) => ({
					reel,
					cx,
					cy: firstCy + pitch * reel,
				})),
				rail: { x: innerX, y: innerTop, w: innerW, h: innerH },
				readout: {
					x: railLeftR + wellW * 0.5,
					y: boardCy,
					wellW,
					slots,
				},
			};
		}

		// narrow: the rail lies down above the board, one plaque over each reel.
		// WAYS/WIN move to FrameMorphHud here (no room for a right readout column).
		// MAX_RAIL_W * PLAQUE_WIDTH_FRACTION === one card wide (SYMBOL_CARD_W).
		const cellW = MAX_RAIL_W * PLAQUE_WIDTH_FRACTION;
		const cellH = cellW / PLAQUE_ASPECT;
		const thick = BOARD_FRAME_THICK * s;
		const corner = BOARD_FRAME_CORNER * s;
		const innerPad = thick * 0.5;
		const innerH = cellH + innerPad * 2;
		const railBottom = boardTop - BOARD_GAP * s;
		const innerTop = railBottom - thick - innerH;
		const cy = innerTop + innerH * 0.5;
		const cells = Array.from({ length: REELS }, (_, reel) => ({
			reel,
			cx: originX + getSymbolX(reel) * s,
			cy,
		}));
		const left = cells[0].cx - cellW * 0.5 - innerPad;
		const right = cells[REELS - 1].cx + cellW * 0.5 + innerPad;

		return {
			vertical: false,
			thick,
			corner,
			cellW,
			cellH,
			cells,
			rail: { x: left, y: innerTop, w: right - left, h: innerH },
			readout: null,
		};
	});

	const pop = $derived(1 + 0.22 * enter.current);
	/** 0 → 1 across the strike, so the hit FX can run forwards while `enter`
	 * eases the plaque back down. */
	const strike = $derived(1 - enter.current);
</script>

<Container>
	<TimberRect
		x={layout.rail.x}
		y={layout.rail.y}
		w={layout.rail.w}
		h={layout.rail.h}
		thick={layout.thick}
		corner={layout.corner}
		fill
	/>
</Container>

<Container>
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
</Container>

{#if layout.readout}
	<HudReadout
		x={layout.readout.x}
		y={layout.readout.y}
		wellW={layout.readout.wellW}
		slots={layout.readout.slots}
		axis="y"
	/>
{/if}
