<script lang="ts">
	/**
	 * Weathered wooden reel frame — Tombstone RIP reference: dark plank face,
	 * recessed sockets per cell, nail heads on the seams. No White Room steel.
	 *
	 * Silhouette hugs every reel top AND bottom (true staircase), so the
	 * last-reel special lane stays a single grave cell bolted to the board floor.
	 */
	import type { Graphics as PixiGraphics } from 'pixi.js';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, CELL_PITCH_X } from '../game/constants';
	import { getCellLeft, getReelWindow, getReelRows } from '../game/utils';

	const context = getContext();

	const PAD = 18;
	const GROUT = 2.25;
	const SOCKET_RADIUS = 5;
	const NAIL_R = 2.4;

	const WOOD_FACE = 0x2a2118;
	const WOOD_DEEP = 0x14100c;
	const WOOD_EDGE = 0x4a3a28;
	const WOOD_GRAIN = 0x3a2c1e;
	const SOCKET = 0x0a0806;
	const NAIL = 0x6a5a40;
	const NAIL_GLINT = 0xc9b48a;
	const DUST = 0x8a6a40;

	type Column = { left: number; right: number; top: number; bottom: number; rows: number };

	const columns = $derived.by(() =>
		context.stateGame.board.map((_, reel): Column => {
			const window = getReelWindow(reel);
			return {
				left: getCellLeft(reel),
				right: getCellLeft(reel) + CELL_PITCH_X,
				top: window.top,
				bottom: window.bottom,
				rows: getReelRows(reel),
			};
		}),
	);

	/** true staircase on TOP and BOTTOM — each reel's own height, no filled notches */
	const silhouette = $derived.by(() => {
		if (columns.length === 0) return [] as number[];
		const points: number[] = [];
		const push = (x: number, y: number) => points.push(x, y);

		const first = columns[0];
		const last = columns[columns.length - 1];

		// top edge left → right
		push(first.left - PAD, first.top - PAD);
		for (let i = 1; i < columns.length; i++) {
			push(columns[i].left, columns[i - 1].top - PAD);
			push(columns[i].left, columns[i].top - PAD);
		}
		push(last.right + PAD, last.top - PAD);

		// bottom edge right → left (mirror staircase)
		push(last.right + PAD, last.bottom + PAD);
		for (let i = columns.length - 1; i >= 1; i--) {
			push(columns[i].left, columns[i].bottom + PAD);
			push(columns[i].left, columns[i - 1].bottom + PAD);
		}
		push(first.left - PAD, first.bottom + PAD);
		return points;
	});

	const drawPlate = (g: PixiGraphics, outline: number[], cols: Column[]) => {
		if (outline.length === 0) return;

		// cast shadow
		g.poly(outline.map((value, index) => (index % 2 === 1 ? value + 8 : value)));
		g.fill({ color: 0x000000, alpha: 0.42 });

		// wood face
		g.poly(outline);
		g.fill({ color: WOOD_FACE, alpha: 0.98 });
		g.poly(outline);
		g.stroke({ color: WOOD_DEEP, width: 6, alpha: 0.7 });
		g.poly(outline);
		g.stroke({ color: WOOD_EDGE, width: 1.5, alpha: 0.55 });

		// faint plank grain lines across the face
		const minX = Math.min(...cols.map((c) => c.left)) - PAD;
		const maxX = Math.max(...cols.map((c) => c.right)) + PAD;
		const minY = Math.min(...cols.map((c) => c.top)) - PAD;
		const maxY = Math.max(...cols.map((c) => c.bottom)) + PAD;
		for (let y = minY + 10; y < maxY; y += 11) {
			g.moveTo(minX + 4, y);
			g.lineTo(maxX - 4, y);
			g.stroke({ color: WOOD_GRAIN, width: 1, alpha: 0.18 });
		}

		// dusty amber hairline (RIP-style accent, not clinical white)
		g.moveTo(minX + 10, minY + 2);
		g.lineTo(maxX - 10, minY + 2);
		g.stroke({ color: DUST, width: 1, alpha: 0.35 });

		cols.forEach((col) => {
			for (let row = 0; row < col.rows; row++) {
				const x = col.left + GROUT;
				const y = col.top + row * SYMBOL_SIZE + GROUT;
				const w = CELL_PITCH_X - GROUT * 2;
				const h = SYMBOL_SIZE - GROUT * 2;

				g.roundRect(x, y, w, h, SOCKET_RADIUS);
				g.fill({ color: SOCKET, alpha: 0.94 });
				g.roundRect(x, y, w, h, SOCKET_RADIUS);
				g.stroke({ color: 0x000000, width: 3, alpha: 0.55 });
				// warm lip catch-light
				g.moveTo(x + SOCKET_RADIUS, y + h - 0.5);
				g.lineTo(x + w - SOCKET_RADIUS, y + h - 0.5);
				g.stroke({ color: DUST, width: 1, alpha: 0.12 });
			}
		});

		// nail heads on the plank seams
		cols.forEach((col, index) => {
			const spots: { x: number; y: number }[] = [];
			spots.push({ x: col.left + (col.right - col.left) * 0.5, y: col.top - PAD * 0.45 });
			spots.push({ x: col.left + (col.right - col.left) * 0.5, y: col.bottom + PAD * 0.45 });
			if (index > 0) {
				spots.push({ x: col.left, y: col.top + 8 });
				spots.push({ x: col.left, y: col.bottom - 8 });
			}
			spots.forEach(({ x, y }) => {
				g.circle(x, y, NAIL_R);
				g.fill({ color: NAIL, alpha: 0.7 });
				g.circle(x - 0.5, y - 0.5, NAIL_R * 0.4);
				g.fill({ color: NAIL_GLINT, alpha: 0.35 });
			});
		});
	};
</script>

<Container
	x={context.stateGameDerived.boardLayout().x -
		context.stateGameDerived.boardLayout().width * 0.5}
	y={context.stateGameDerived.boardLayout().y -
		context.stateGameDerived.boardLayout().height * 0.5}
>
	<Graphics draw={(g) => drawPlate(g, silhouette, columns)} />
</Container>
