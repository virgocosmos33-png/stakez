<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { MainContainer } from 'components-layout';
	import { Graphics } from 'pixi-svelte';

	import type { Position } from '../game/types';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { drawFlameBorder, type FlamePalette } from '../game/flameDraw';

	const context = getContext();

	// Green plasma FIRE around the connecting combination. Adjacent winning
	// cells MERGE: the flames trace the outer contour of the whole linked
	// group (per the art reference) instead of boxing every cell, pinching at
	// the junctions. Isolated cells still get their own burning ring.
	// Ignites left-to-right so the combination reads as LINKING, then burns
	// as ragged licking flame bands (flameDraw.ts) - no tubes, no dots.

	// green fire ramp sampled from the burn/liner reference art
	const FIRE: FlamePalette = {
		body: 0x2f9e3f,
		mid: 0x6fd23e,
		hot: 0xa8f04f,
		core: 0xe8ffc0,
	};

	const IGNITE_STAGGER = 0.09;
	const IGNITE_FLASH = 0.24;
	const CORNER_RADIUS = 15;
	const SAMPLE_STEP = 9;

	type Sample = { x: number; y: number; nx: number; ny: number };

	type LinerGroup = {
		key: string;
		seed: number;
		delay: number; // ignition stagger (leftmost reel of the group)
		loops: Sample[][];
		perimeter: number;
	};

	let groups = $state<LinerGroup[]>([]);
	let time = $state(0);
	let ignitionTime = $state(0);
	const fade = new Tween(0);
	let generation = 0;

	// ---- merged outline geometry -------------------------------------------

	// boundary edges with the interior on the RIGHT of the walk direction
	// (screen coords, y down): outer loops wind clockwise, outward = left.
	const traceLoops = (cellKeys: Set<string>): [number, number][][] => {
		type Point = string; // "x,y" in grid corner units
		const edges = new Map<Point, [number, number, number, number]>(); // start -> x0,y0,x1,y1
		const has = (col: number, row: number) => cellKeys.has(`${col},${row}`);

		for (const key of cellKeys) {
			const [col, row] = key.split(',').map(Number);
			if (!has(col, row - 1)) edges.set(`${col},${row}`, [col, row, col + 1, row]);
			if (!has(col + 1, row)) edges.set(`${col + 1},${row}`, [col + 1, row, col + 1, row + 1]);
			if (!has(col, row + 1))
				edges.set(`${col + 1},${row + 1}`, [col + 1, row + 1, col, row + 1]);
			if (!has(col - 1, row)) edges.set(`${col},${row + 1}`, [col, row + 1, col, row]);
		}

		const loops: [number, number][][] = [];
		while (edges.size > 0) {
			const [firstKey] = edges.keys();
			const loop: [number, number][] = [];
			let cursor = firstKey;
			while (edges.has(cursor)) {
				const [x0, y0, x1, y1] = edges.get(cursor)!;
				edges.delete(cursor);
				// merge collinear runs
				const previous = loop[loop.length - 2];
				const last = loop[loop.length - 1];
				if (
					previous &&
					last &&
					((previous[0] === last[0] && last[0] === x0 && x0 === x1 && previous[0] === x1) ||
						(previous[1] === last[1] && last[1] === y0 && y0 === y1 && previous[1] === y1))
				) {
					loop[loop.length - 1] = [x1, y1];
				} else {
					if (loop.length === 0) loop.push([x0, y0]);
					loop.push([x1, y1]);
				}
				cursor = `${x1},${y1}`;
			}
			// closing point duplicates the start; drop it (and re-check the seam
			// for a collinear merge across the wrap)
			loop.pop();
			if (loop.length >= 4) {
				const first = loop[0];
				const second = loop[1];
				const last = loop[loop.length - 1];
				if (
					(last[0] === first[0] && first[0] === second[0]) ||
					(last[1] === first[1] && first[1] === second[1])
				) {
					loop.shift();
				}
			}
			loops.push(loop);
		}
		return loops;
	};

	// dense samples along a rectilinear loop: straight runs stepped every
	// SAMPLE_STEP px, convex corners rounded with a small arc, concave
	// junction corners kept sharp (the reference pinches there)
	const sampleLoop = (vertices: [number, number][], toPx: number, ox: number, oy: number) => {
		const count = vertices.length;
		const samples: Sample[] = [];
		const pts = vertices.map(([gx, gy]) => [ox + gx * toPx, oy + gy * toPx] as [number, number]);

		const direction = (a: [number, number], b: [number, number]): [number, number] => {
			const dx = b[0] - a[0];
			const dy = b[1] - a[1];
			const length = Math.hypot(dx, dy) || 1;
			return [dx / length, dy / length];
		};

		for (let i = 0; i < count; i++) {
			const a = pts[i];
			const b = pts[(i + 1) % count];
			const prev = pts[(i - 1 + count) % count];
			const next = pts[(i + 2) % count];
			const dir = direction(a, b);
			const inDir = direction(prev, a);
			const outDir = direction(b, next);
			// outward normal = left of walk direction (interior is on the right)
			const nx = dir[1];
			const ny = -dir[0];
			const edgeLength = Math.hypot(b[0] - a[0], b[1] - a[1]);

			// convex corner at a: cross(inDir, dir) > 0 (right turn, y-down)
			const crossA = inDir[0] * dir[1] - inDir[1] * dir[0];
			const crossB = dir[0] * outDir[1] - dir[1] * outDir[0];
			const radiusA = crossA > 0 ? Math.min(CORNER_RADIUS, edgeLength / 2) : 0;
			const radiusB = crossB > 0 ? Math.min(CORNER_RADIUS, edgeLength / 2) : 0;

			// rounded corner arc replacing the cut at a (quarter turn): the arc
			// center is pulled inward from the corner by r along both normals
			if (radiusA > 0) {
				const inNx = inDir[1];
				const inNy = -inDir[0];
				const arcCx = a[0] - (inNx + nx) * radiusA;
				const arcCy = a[1] - (inNy + ny) * radiusA;
				const startAngle = Math.atan2(inNy, inNx);
				const endAngle = Math.atan2(ny, nx);
				// shortest sweep for a quarter turn
				let sweep = endAngle - startAngle;
				if (sweep > Math.PI) sweep -= Math.PI * 2;
				if (sweep < -Math.PI) sweep += Math.PI * 2;
				const ARC_POINTS = 5;
				for (let k = 0; k <= ARC_POINTS; k++) {
					const angle = startAngle + sweep * (k / ARC_POINTS);
					samples.push({
						x: arcCx + Math.cos(angle) * radiusA,
						y: arcCy + Math.sin(angle) * radiusA,
						nx: Math.cos(angle),
						ny: Math.sin(angle),
					});
				}
			}

			// straight run (skipping the rounded cuts at both ends)
			const runStart = radiusA;
			const runEnd = edgeLength - radiusB;
			for (let d = runStart; d < runEnd; d += SAMPLE_STEP) {
				samples.push({ x: a[0] + dir[0] * d, y: a[1] + dir[1] * d, nx, ny });
			}
		}
		return samples;
	};

	// ---- ignite / release ---------------------------------------------------

	const ignite = (positions: Position[]) => {
		generation += 1;
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		const minReel = Math.min(...positions.map((position) => position.reel));

		// visible-grid cell set (book event rows are padded by one)
		const keys = new Set(positions.map((position) => `${position.reel},${position.row - 1}`));

		// connected components, 4-neighborhood
		const seen = new Set<string>();
		const components: string[][] = [];
		for (const key of keys) {
			if (seen.has(key)) continue;
			const queue = [key];
			seen.add(key);
			const component: string[] = [];
			while (queue.length > 0) {
				const current = queue.pop()!;
				component.push(current);
				const [col, row] = current.split(',').map(Number);
				for (const neighbor of [
					`${col + 1},${row}`,
					`${col - 1},${row}`,
					`${col},${row + 1}`,
					`${col},${row - 1}`,
				]) {
					if (keys.has(neighbor) && !seen.has(neighbor)) {
						seen.add(neighbor);
						queue.push(neighbor);
					}
				}
			}
			components.push(component);
		}

		groups = components.map((component, index) => {
			const cellSet = new Set(component);
			const loops = traceLoops(cellSet).map((loop) =>
				sampleLoop(loop, SYMBOL_SIZE, originX, originY),
			);
			const groupMinReel = Math.min(...component.map((key) => Number(key.split(',')[0])));
			return {
				key: `${generation}-${index}`,
				seed: index * 53 + groupMinReel * 17,
				delay: (groupMinReel - minReel) * IGNITE_STAGGER,
				loops,
				perimeter: loops.reduce((total, loop) => total + loop.length * SAMPLE_STEP, 0),
			};
		});
		ignitionTime = time;
		fade.set(1, { duration: 100 });
	};

	const release = async () => {
		const token = generation;
		await fade.set(0, { duration: 260 });
		if (token === generation) groups = [];
	};

	const hide = () => {
		generation += 1;
		fade.set(0, { duration: 0 });
		groups = [];
	};

	context.eventEmitter.subscribeOnMount({
		apparitionsWinGrow: ({ positions }) => ignite(positions),
		apparitionsWinRelease: () => release(),
		winCycleStop: () => hide(),
		winDimHide: () => hide(),
		apparitionsHide: () => hide(),
		boardHide: () => hide(),
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	// ---- drawing -------------------------------------------------------------

	const drawGroup = (
		graphics: import('pixi.js').Graphics,
		group: LinerGroup,
		timeValue: number,
		fadeValue: number,
	) => {
		if (fadeValue <= 0.01) return;
		const age = timeValue - ignitionTime - group.delay;
		if (age <= 0) return;
		const alive = Math.min(age / 0.1, 1) * fadeValue;

		for (const loop of group.loops) {
			if (loop.length < 3) continue;

			// --- ignition burst: pale expanding echo of the whole contour ---
			if (age < IGNITE_FLASH) {
				const burst = age / IGNITE_FLASH;
				const burstFade = 1 - burst;
				const echo: number[] = [];
				for (const sample of loop) {
					echo.push(sample.x + sample.nx * 16 * burst, sample.y + sample.ny * 16 * burst);
				}
				graphics.poly(echo);
				graphics.stroke({
					color: FIRE.core,
					width: 8 * burstFade + 1,
					alpha: 0.85 * burstFade * fadeValue,
				});
			}

			// --- the fire itself: ragged licking flame bands, no dots ---
			drawFlameBorder(graphics, loop, FIRE, {
				seed: group.seed,
				time: timeValue,
				alpha: alive,
				heightMin: 4,
				heightMax: 18,
				lickScale: 2.8,
				lickEvery: 7,
				upBias: 0.55,
			});
		}
	};

	const drawAll = (graphics: import('pixi.js').Graphics) => {
		for (const group of groups) {
			drawGroup(graphics, group, time, fade.current);
		}
	};
</script>

<MainContainer>
	{#if groups.length > 0}
		<Graphics draw={drawAll} />
	{/if}
</MainContainer>
