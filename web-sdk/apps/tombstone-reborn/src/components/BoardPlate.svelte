<script lang="ts">
	/**
	 * Weathered western reel frame — LIVE STAIRCASE, built from the existing
	 * parts (`boardWoodField` planks + `boardCornerBracket` plates + per-cell
	 * `boardSlotFrame`). Each column's cap follows that reel's LIVE card
	 * pocket (getReelPocket), so when a reel grows (TOMBSTONE OPEN / stretch)
	 * that column's timber extends with it instead of the cards sitting on a
	 * frozen baked PNG.
	 *
	 * Neighbouring columns at the same height share one plank run (the authored
	 * 4-3-2-3-4 silhouette at rest). Step walls turn the staircase corners.
	 * Pockets hug the painted cards (getReelPocket) so the saloon wall never
	 * shows as a pale channel around a cell. Timber and pocket stone are
	 * graded to the saloon wall (tools/grade_board_to_saloon.py).
	 *
	 * Symbol geometry is untouched — this component only draws chrome around
	 * the live windows. Board layout x/y/pivot/size are not changed here.
	 */
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import {
		SYMBOL_CARD_W,
		BOARD_FRAME_GAP,
		BOARD_FRAME_THICK,
		BOARD_FRAME_CORNER,
		BOARD_FRAME_STEP,
	} from '../game/constants';
	import { getReelPocket, getReelRows, getSymbolX, getCellCenterY } from '../game/utils';

	const context = getContext();

	const GAP = BOARD_FRAME_GAP;
	const THICK = BOARD_FRAME_THICK;
	const CORNER = BOARD_FRAME_CORNER;
	const STEP_PLATE = BOARD_FRAME_STEP;
	const EPS = 0.5;

	type Column = { left: number; right: number; top: number; bottom: number };

	const columns = $derived.by(() =>
		context.stateGame.board.map((_, reel): Column => {
			const pocket = getReelPocket(reel);
			return {
				left: pocket.left,
				right: pocket.right,
				top: pocket.top,
				bottom: pocket.bottom,
			};
		}),
	);

	const slots = $derived.by(() =>
		context.stateGame.board.flatMap((_, reel) => {
			const rows = getReelRows(reel);
			if (rows <= 0) return [];
			const pocket = getReelPocket(reel);
			return Array.from({ length: rows }, (_, r) => ({
				key: `${reel}:${r}`,
				cx: getSymbolX(reel),
				cy: getCellCenterY(reel, r + 1),
				w: SYMBOL_CARD_W,
				h: pocket.cardH,
			}));
		}),
	);

	type Beam = { key: string; cx: number; cy: number; len: number; horizontal: boolean };
	type Plate = { key: string; cx: number; cy: number; size: number };

	const frame = $derived.by(() => {
		const n = columns.length;
		const tops = columns.map((c) => c.top - GAP);
		const bottoms = columns.map((c) => c.bottom + GAP);
		const lefts = columns.map((c) => c.left);
		const rights = columns.map((c) => c.right);
		const innerLeft = lefts[0] - GAP;
		const innerRight = rights[n - 1] + GAP;

		const beams: Beam[] = [];
		const plates: Plate[] = [];

		const runsOf = (vals: number[]) => {
			const runs: { a: number; b: number; v: number }[] = [];
			let a = 0;
			for (let i = 1; i <= n; i++) {
				if (i === n || Math.abs(vals[i] - vals[a]) > EPS) {
					runs.push({ a, b: i - 1, v: vals[a] });
					a = i;
				}
			}
			return runs;
		};

		for (const run of runsOf(tops)) {
			const xs = run.a === 0 ? innerLeft - THICK : lefts[run.a] - 1;
			const xe = run.b === n - 1 ? innerRight + THICK : rights[run.b] + 1;
			beams.push({
				key: `capT:${run.a}`,
				cx: (xs + xe) / 2,
				cy: run.v - THICK / 2,
				len: xe - xs,
				horizontal: true,
			});
		}
		for (const run of runsOf(bottoms)) {
			const xs = run.a === 0 ? innerLeft - THICK : lefts[run.a] - 1;
			const xe = run.b === n - 1 ? innerRight + THICK : rights[run.b] + 1;
			beams.push({
				key: `capB:${run.a}`,
				cx: (xs + xe) / 2,
				cy: run.v + THICK / 2,
				len: xe - xs,
				horizontal: true,
			});
		}

		for (let i = 0; i < n - 1; i++) {
			const bx = rights[i];
			if (Math.abs(tops[i] - tops[i + 1]) > EPS) {
				const shorterRight = tops[i + 1] > tops[i];
				const x0 = shorterRight ? bx : bx - THICK;
				const yTop = Math.min(tops[i], tops[i + 1]) - THICK;
				const yBot = Math.max(tops[i], tops[i + 1]);
				beams.push({
					key: `stepT:${i}`,
					cx: x0 + THICK / 2,
					cy: (yTop + yBot) / 2,
					len: yBot - yTop,
					horizontal: false,
				});
				plates.push(
					{ key: `pT:${i}:o`, cx: x0 + THICK / 2, cy: yTop + THICK / 2, size: STEP_PLATE },
					{ key: `pT:${i}:i`, cx: x0 + THICK / 2, cy: yBot - THICK / 2, size: STEP_PLATE },
				);
			}
			if (Math.abs(bottoms[i] - bottoms[i + 1]) > EPS) {
				const shorterRight = bottoms[i + 1] < bottoms[i];
				const x0 = shorterRight ? bx : bx - THICK;
				const yTop = Math.min(bottoms[i], bottoms[i + 1]);
				const yBot = Math.max(bottoms[i], bottoms[i + 1]) + THICK;
				beams.push({
					key: `stepB:${i}`,
					cx: x0 + THICK / 2,
					cy: (yTop + yBot) / 2,
					len: yBot - yTop,
					horizontal: false,
				});
				plates.push(
					{ key: `pB:${i}:i`, cx: x0 + THICK / 2, cy: yTop + THICK / 2, size: STEP_PLATE },
					{ key: `pB:${i}:o`, cx: x0 + THICK / 2, cy: yBot - THICK / 2, size: STEP_PLATE },
				);
			}
		}

		beams.push(
			{
				key: 'wallL',
				cx: innerLeft - THICK / 2,
				cy: (tops[0] + bottoms[0]) / 2,
				len: bottoms[0] - tops[0] + 2 * THICK,
				horizontal: false,
			},
			{
				key: 'wallR',
				cx: innerRight + THICK / 2,
				cy: (tops[n - 1] + bottoms[n - 1]) / 2,
				len: bottoms[n - 1] - tops[n - 1] + 2 * THICK,
				horizontal: false,
			},
		);

		plates.push(
			{ key: 'cTL', cx: innerLeft - THICK / 2, cy: tops[0] - THICK / 2, size: CORNER },
			{ key: 'cBL', cx: innerLeft - THICK / 2, cy: bottoms[0] + THICK / 2, size: CORNER },
			{ key: 'cTR', cx: innerRight + THICK / 2, cy: tops[n - 1] - THICK / 2, size: CORNER },
			{ key: 'cBR', cx: innerRight + THICK / 2, cy: bottoms[n - 1] + THICK / 2, size: CORNER },
		);

		return { beams, plates };
	});
	const layout = $derived(context.stateGameDerived.boardLayout());
</script>

<Container x={layout.x} y={layout.y} pivot={layout.pivot} scale={layout.scale}>
	{#each slots as slot (slot.key)}
		<Container x={slot.cx} y={slot.cy}>
			<Sprite key="boardStoneField" anchor={0.5} width={slot.w} height={slot.h} />
			<Sprite key="boardSlotFrame" anchor={0.5} width={slot.w} height={slot.h} />
		</Container>
	{/each}

	{#each frame.beams as beam (beam.key)}
		{#if beam.horizontal}
			<Sprite
				key="boardWoodField"
				anchor={0.5}
				rotation={Math.PI / 2}
				x={beam.cx}
				y={beam.cy}
				width={THICK}
				height={beam.len}
			/>
		{:else}
			<Sprite
				key="boardWoodField"
				anchor={0.5}
				x={beam.cx}
				y={beam.cy}
				width={THICK}
				height={beam.len}
			/>
		{/if}
	{/each}

	{#each frame.plates as plate (plate.key)}
		<Sprite
			key="boardCornerBracket"
			anchor={0.5}
			x={plate.cx}
			y={plate.cy}
			width={plate.size}
			height={plate.size}
		/>
	{/each}
</Container>
