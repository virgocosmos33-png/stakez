<script lang="ts">
	/**
	 * Weathered western reel frame — baked timber-and-iron chassis, cohesive with
	 * the shipped win-celebration timber plates. The art is baked
	 * (tools/make_board_frame_art.py); this component only lays it onto the live
	 * board geometry:
	 *   - boardPlate         a dark-graded Layer AI plank field, clipped to the
	 *                        diamond staircase silhouette (the timber behind it all)
	 *   - boardCellSocket    one crafted recessed window per VISIBLE cell (dark
	 *                        recess + brass inner lip + corner rivets), drawn at
	 *                        the exact cell size with a transparent grout margin so
	 *                        the timber reads as the raised wood between windows
	 *   - boardCornerBracket a bolted iron corner boss at the four outer corners of
	 *                        the staircase, inside the plate's PAD overhang
	 *
	 * GEOMETRY IS FROZEN: the `columns` + `silhouette` maths below are unchanged
	 * from the procedural frame this replaced (cell rects, CELL_PITCH_X,
	 * SYMBOL_SIZE, per-reel rows, getCellLeft/getReelWindow/getReelRows and PAD =
	 * BOARD_PLATE_PAD). A parallel feature traces fire around this exact cell
	 * geometry, so only the ART changed — never the skeleton.
	 */
	import type { Graphics as PixiGraphics } from 'pixi.js';
	import { Container, Graphics, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, CELL_PITCH_X, BOARD_PLATE_PAD } from '../game/constants';
	import { getCellLeft, getReelWindow, getReelRows } from '../game/utils';

	const context = getContext();

	const PAD = BOARD_PLATE_PAD;
	/** iron corner boss size — a touch over the PAD overhang so it hugs the corner */
	const BRACKET = PAD * 2.3;

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

	/** axis-aligned bounds of the silhouette — the timber sprite covers this box
	 * and the silhouette mask clips it back to the staircase */
	const bounds = $derived.by(() => {
		if (columns.length === 0) return { x: 0, y: 0, w: 0, h: 0 };
		const first = columns[0];
		const last = columns[columns.length - 1];
		const x = first.left - PAD;
		const right = last.right + PAD;
		const y = Math.min(...columns.map((c) => c.top)) - PAD;
		const bottom = Math.max(...columns.map((c) => c.bottom)) + PAD;
		return { x, y, w: right - x, h: bottom - y };
	});

	/** every VISIBLE cell centre — sockets only ever sit on live rows (getReelRows),
	 * never on the off-window pad rows the book events index */
	const cells = $derived.by(() =>
		columns.flatMap((col) =>
			Array.from({ length: col.rows }, (_, row) => ({
				cx: col.left + CELL_PITCH_X / 2,
				cy: col.top + row * SYMBOL_SIZE + SYMBOL_SIZE / 2,
			})),
		),
	);

	/** the four outer corners of the staircase — leftmost + rightmost columns */
	const brackets = $derived.by(() => {
		if (columns.length === 0) return [];
		const first = columns[0];
		const last = columns[columns.length - 1];
		return [
			{ x: first.left - PAD, y: first.top - PAD, ax: 0, ay: 0 },
			{ x: last.right + PAD, y: last.top - PAD, ax: 1, ay: 0 },
			{ x: first.left - PAD, y: first.bottom + PAD, ax: 0, ay: 1 },
			{ x: last.right + PAD, y: last.bottom + PAD, ax: 1, ay: 1 },
		];
	});

	/** broad, soft edge only — never a thin bright stroke (minifies to a hairline).
	 * The plate reads against the background via its cast shadow + this dark burn. */
	const drawShadow = (g: PixiGraphics, outline: number[]) => {
		if (outline.length === 0) return;
		g.poly(outline.map((value, index) => (index % 2 === 1 ? value + 8 : value)));
		g.fill({ color: 0x000000, alpha: 0.42 });
	};

	const drawEdge = (g: PixiGraphics, outline: number[]) => {
		if (outline.length === 0) return;
		g.poly(outline);
		g.stroke({ color: 0x090705, width: 6, alpha: 0.85 });
	};

	const drawMask = (g: PixiGraphics, outline: number[]) => {
		if (outline.length === 0) return;
		g.poly(outline);
		g.fill({ color: 0xffffff, alpha: 1 });
	};
</script>

<Container
	x={context.stateGameDerived.boardLayout().x -
		context.stateGameDerived.boardLayout().width * 0.5}
	y={context.stateGameDerived.boardLayout().y -
		context.stateGameDerived.boardLayout().height * 0.5}
>
	<!-- cast shadow so the plate sits on the graveyard behind it -->
	<Graphics draw={(g) => drawShadow(g, silhouette)} />

	<!-- weathered timber field, clipped to the diamond staircase -->
	<Container>
		<Sprite key="boardPlate" x={bounds.x} y={bounds.y} width={bounds.w} height={bounds.h} />
		<Graphics isMask draw={(g) => drawMask(g, silhouette)} />
	</Container>

	<!-- broad burnt edge -->
	<Graphics draw={(g) => drawEdge(g, silhouette)} />

	<!-- crafted recessed window per visible cell -->
	{#each cells as cell (`${cell.cx}:${cell.cy}`)}
		<Sprite
			key="boardCellSocket"
			x={cell.cx}
			y={cell.cy}
			anchor={0.5}
			width={CELL_PITCH_X}
			height={SYMBOL_SIZE}
		/>
	{/each}

	<!-- bolted iron corner bosses on the outer corners -->
	{#each brackets as b (`${b.ax}:${b.ay}`)}
		<Sprite
			key="boardCornerBracket"
			x={b.x}
			y={b.y}
			anchor={{ x: b.ax, y: b.ay }}
			width={BRACKET}
			height={BRACKET}
		/>
	{/each}
</Container>
