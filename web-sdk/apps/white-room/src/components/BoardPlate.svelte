<script lang="ts">
	/**
	 * The board the symbols are bolted to.
	 *
	 * Without this the diamond is just cards floating on the room wall — no
	 * surface, no edge, nothing tying the five columns into one object. This
	 * draws a single steel plate cut to the diamond's silhouette, with one
	 * recessed socket per cell, so every symbol reads as sitting IN the board
	 * rather than in front of it.
	 *
	 * Mounted before <Board /> in its own MainContainer so it can never be
	 * pushed in front of the symbols by a remount.
	 */
	import type { Graphics as PixiGraphics } from 'pixi.js';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, CELL_PITCH_X, MAX_ROWS } from '../game/constants';
	import { getCellLeft, getReelWindow, getReelRows } from '../game/utils';
	import { WHITE_ROOM_PALETTE } from '../game/clinicalFx';

	const context = getContext();

	/** steel lip left around the grid — the part that reads as "a board" */
	const PAD = 15;
	/** grout between neighbouring sockets (half on each side of the seam) */
	const GROUT = 1.75;
	const SOCKET_RADIUS = 7;
	const RIVET_R = 2.6;

	const PLATE_FACE = 0x24262a;
	const PLATE_DEEP = 0x131417;
	const SOCKET = 0x0c0d0f;

	type Column = { left: number; right: number; top: number; bottom: number; rows: number };

	const columns = $derived(
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

	// The plate keeps the diamond STAIRCASE along its top edge, but its bottom
	// is one FLAT line at the board's true bottom (the tallest reels' bottom,
	// fixed to the authored extents): the notches under the short middle reels
	// are filled with plate face because the bottom special cells live there
	// and must read as part of the same board. A racked/grown reel overflows
	// past the plate by design, it never inflates it.
	const silhouette = $derived.by(() => {
		if (columns.length === 0) return [] as number[];
		const points: number[] = [];
		const push = (x: number, y: number) => points.push(x, y);

		// staircase across the top, exactly as the diamond is authored
		push(columns[0].left - PAD, columns[0].top - PAD);
		for (let i = 1; i < columns.length; i++) {
			push(columns[i].left, columns[i - 1].top - PAD);
			push(columns[i].left, columns[i].top - PAD);
		}
		const last = columns[columns.length - 1];
		const bottom = SYMBOL_SIZE * MAX_ROWS + PAD;
		push(last.right + PAD, last.top - PAD);
		// straight down the right edge, flat across the bottom, back up the left
		push(last.right + PAD, bottom);
		push(columns[0].left - PAD, bottom);
		return points;
	});

	const drawPlate = (g: PixiGraphics, outline: number[], cols: Column[]) => {
		if (outline.length === 0) return;

		// cast shadow: the plate stands off the wall
		g.poly(outline.map((value, index) => (index % 2 === 1 ? value + 7 : value)));
		g.fill({ color: 0x000000, alpha: 0.38 });

		g.poly(outline);
		g.fill({ color: PLATE_FACE, alpha: 0.96 });
		g.poly(outline);
		g.stroke({ color: PLATE_DEEP, width: 5, alpha: 0.55 });
		g.poly(outline);
		g.stroke({ color: WHITE_ROOM_PALETTE.steel, width: 1.5, alpha: 0.45 });

		cols.forEach((col) => {
			for (let row = 0; row < col.rows; row++) {
				const x = col.left + GROUT;
				const y = col.top + row * SYMBOL_SIZE + GROUT;
				const w = CELL_PITCH_X - GROUT * 2;
				const h = SYMBOL_SIZE - GROUT * 2;

				g.roundRect(x, y, w, h, SOCKET_RADIUS);
				g.fill({ color: SOCKET, alpha: 0.9 });
				// inner shadow on the way in, catch light on the far lip
				g.roundRect(x, y, w, h, SOCKET_RADIUS);
				g.stroke({ color: 0x000000, width: 3, alpha: 0.5 });
				g.moveTo(x + SOCKET_RADIUS, y + h - 0.5);
				g.lineTo(x + w - SOCKET_RADIUS, y + h - 0.5);
				g.stroke({ color: WHITE_ROOM_PALETTE.bone, width: 1, alpha: 0.09 });
			}
		});

		// rivets down the seams, where the plate would actually be bolted
		cols.forEach((col, index) => {
			const xs = index === 0 ? [col.left - PAD * 0.5] : [];
			if (index === cols.length - 1) xs.push(col.right + PAD * 0.5);
			if (index > 0) xs.push(col.left);
			xs.forEach((x) => {
				// top rivets ride the staircase; bottom rivets sit on the flat line
				[col.top - PAD * 0.5, SYMBOL_SIZE * MAX_ROWS + PAD * 0.5].forEach((y) => {
					g.circle(x, y, RIVET_R);
					g.fill({ color: WHITE_ROOM_PALETTE.steel, alpha: 0.55 });
					g.circle(x - 0.6, y - 0.6, RIVET_R * 0.45);
					g.fill({ color: WHITE_ROOM_PALETTE.bone, alpha: 0.3 });
				});
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
