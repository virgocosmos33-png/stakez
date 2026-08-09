<script lang="ts" module>
	import type { Position } from '../game/types';

	export type EmitterEventWinSweep = {
		type: 'winSweep';
		positions: Position[];
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { linear } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, CELL_PITCH_X, MAX_ROWS } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { cellFrames } from '../game/chassisArt';
	import { BOTTOM_START } from '../game/cellUnlock';
	import { fxNum } from '../game/fx.generated';
	import { drawMirrorSweep } from '../game/clinicalFx';

	const context = getContext();

	// THE WHITE ROOM: winning cells get a fast MIRROR glint — one diagonal
	// light band sliding over each card, staggered column by column, strictly
	// left to right. Positions may live on the core board OR inside a reserved
	// socket (bottom cells / side columns): socket cards glint inside their own
	// frame, so a winning symbol type shines through EVERY card it owns.
	type SweepCell = {
		key: string;
		order: number;
		cx: number;
		cy: number;
		w: number;
		h: number;
		/** full wild-column glint: one big band over the whole reel, not per cell */
		wild?: boolean;
	};

	const REEL_STAGGER = fxNum('winSweep', 'reelStagger', 0.14);
	const SWEEP_BASE_MS = fxNum('winSweep', 'baseMs', 320);
	const SWEEP_PER_REEL_MS = fxNum('winSweep', 'perReelMs', 70);
	/** glancing-light tilt of the band, radians */
	const SWEEP_TILT = -0.45;
	// The card art does NOT fill its texture: every paying symbol's opaque
	// footprint inside the 300px frame is x 37..262, y 4..295 with ~16px
	// rounded corners (measured on symbolsStatic.png; identical for h1-h5,
	// l1-l5 and W). The glint must be masked to THAT footprint — masking the
	// full cell painted the band over the transparent gutters beside the
	// card. Fractions carry a ~2px inset so the band never touches the
	// anti-aliased card edge.
	const CARD_W_FRAC = 222 / 300;
	const CARD_H_FRAC = 288 / 300;
	const CARD_RADIUS_FRAC = 16 / 300;

	let sweepCells = $state<SweepCell[]>([]);
	let span = $state(0);
	const progress = new Tween(0);

	/** socket key for a board position that lives inside a reserved cell */
	const slotKeyOf = (p: Position): string | null => {
		const u = context.stateGame.unlockedSlots;
		if (!u) return null;
		for (const c of u.bottom) {
			if (c.reel === p.reel && c.row === p.row) return `bottom:${c.reel - BOTTOM_START}`;
		}
		for (const s of u.sides) {
			if (s.reel !== p.reel) continue;
			for (const c of s.cells) if (c.row === p.row) return `${s.side}:${c.slotRow}`;
		}
		return null;
	};

	context.eventEmitter.subscribeOnMount({
		winSweep: async ({ positions }) => {
			const boardLayout = context.stateGameDerived.boardLayout();
			const originX = boardLayout.x - boardLayout.width * 0.5;
			const originY = boardLayout.y - boardLayout.height * 0.5;
			const frames = cellFrames(boardLayout);

			// A wild column is presented as ONE thing (the full-reel overlay), so
			// its winning cells collapse into ONE full-height glint over the whole
			// column — per-cell sparkles under the overlay read as broken tiles.
			// Geometry mirrors WildReelSlide: reel-centred, MAX_ROWS tall (every
			// risen column is grown to the full board window).
			const wildReels = new Set(context.stateGame.wildReelReels ?? []);
			const wildSwept = new Set<number>();
			const cells: SweepCell[] = [];
			for (const position of positions) {
				const slotKey = slotKeyOf(position);
				const frame = slotKey ? frames[slotKey] : undefined;
				if (frame) {
					cells.push({
						key: `${position.reel}-${position.row}`,
						order: 0,
						cx: frame.cx,
						cy: frame.cy,
						w: frame.w,
						h: frame.h,
					});
					continue;
				}
				if (wildReels.has(position.reel)) {
					if (wildSwept.has(position.reel)) continue;
					wildSwept.add(position.reel);
					cells.push({
						key: `wild-${position.reel}`,
						order: 0,
						cx: originX + getSymbolX(position.reel),
						cy: originY + MAX_ROWS * 0.5 * SYMBOL_SIZE,
						w: CELL_PITCH_X,
						h: MAX_ROWS * SYMBOL_SIZE,
						wild: true,
					});
					continue;
				}
				cells.push({
					key: `${position.reel}-${position.row}`,
					order: 0,
					cx: originX + getSymbolX(position.reel),
					cy: originY + getCellCenterY(position.reel, position.row),
					w: SYMBOL_SIZE,
					h: SYMBOL_SIZE,
				});
			}

			// stagger by VISUAL column (screen x), so the glint always travels
			// left socket -> board -> right socket, never by board reel index
			const columns = [...new Set(cells.map((cell) => Math.round(cell.cx)))].sort(
				(a, b) => a - b,
			);
			for (const cell of cells) cell.order = columns.indexOf(Math.round(cell.cx));
			span = columns.length - 1;
			sweepCells = cells;

			const duration = SWEEP_BASE_MS + span * SWEEP_PER_REEL_MS;
			progress.set(0, { duration: 0 });
			await progress.set(1, { duration, easing: linear });
			sweepCells = [];
		},
	});

	/** per-column glint progress 0..1 (columns fire left to right, staggered) */
	const localFor = (order: number) => {
		const total = span * REEL_STAGGER + 1;
		return progress.current * total - order * REEL_STAGGER;
	};

	const drawCardMask = (g: import('pixi.js').Graphics, cell: SweepCell) => {
		if (cell.wild) {
			// the wild overlay art is cover-fit full-bleed on the column, so the
			// glint clips to the column box itself (tiny inset off the border FX)
			g.roundRect(-cell.w / 2 + 3, -cell.h / 2 + 3, cell.w - 6, cell.h - 6, 10);
			g.fill(0xffffff);
			return;
		}
		const w = cell.w * CARD_W_FRAC;
		const h = cell.h * CARD_H_FRAC;
		const r = cell.w * CARD_RADIUS_FRAC;
		g.roundRect(-w / 2, -h / 2, w, h, r);
		g.fill(0xffffff);
	};
</script>

<MainContainer>
	{#each sweepCells as cell (cell.key)}
		<Container x={cell.cx} y={cell.cy}>
			<Graphics isMask draw={(g) => drawCardMask(g, cell)} />
			<Container rotation={SWEEP_TILT}>
				<Graphics
					draw={(g) => drawMirrorSweep(g, Math.max(cell.w, cell.h), localFor(cell.order))}
				/>
			</Container>
		</Container>
	{/each}
</MainContainer>
