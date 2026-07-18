<script lang="ts" module>
	import type { Position } from '../game/types';

	export type EmitterEventMirrorShatter =
		| {
				type: 'mirrorShatter';
				positions: Position[];
		  }
		| {
				type: 'mirrorBreak';
				positions: Position[];
		  }
		| {
				type: 'mirrorTelegraph';
				pairs: { mirror: Position; targets: Position[] }[];
		  };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	type Shard = {
		x0: number;
		y0: number;
		vx: number;
		vy: number;
		spin: number;
		size: number;
		color: number;
	};

	let shards = $state<Shard[]>([]);
	const progress = new Tween(0);

	// cracked pane overlay: pops in on mirrorBreak, holds, then animates away
	// (fades + drops) together with the flying shards on mirrorShatter
	let brokenCells = $state<{ cx: number; cy: number }[]>([]);
	const brokenIn = new Tween(0);
	const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

	// telegraph: pulsing outlines on the cells the mirror is about to split,
	// with smoky energy tendrils reaching out from the mirror
	type TelegraphTarget = { cx: number; cy: number };
	type TelegraphBeam = { x1: number; y1: number; x2: number; y2: number };
	let telegraphTargets = $state<TelegraphTarget[]>([]);
	let telegraphBeams = $state<TelegraphBeam[]>([]);
	const telegraphProgress = new Tween(0);

	const cellCenter = (position: Position) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		return {
			// book event rows are padded: visible row = row - 1
			cx: originX + SYMBOL_SIZE * (position.reel + 0.5),
			cy: originY + SYMBOL_SIZE * (position.row - 1 + 0.5),
		};
	};

	const telegraph = async (pairs: { mirror: Position; targets: Position[] }[]) => {
		telegraphTargets = pairs.flatMap((pair) => pair.targets.map(cellCenter));
		telegraphBeams = pairs.flatMap((pair) => {
			const from = cellCenter(pair.mirror);
			return pair.targets.map((target) => {
				const to = cellCenter(target);
				return { x1: from.cx, y1: from.cy, x2: to.cx, y2: to.cy };
			});
		});
		telegraphProgress.set(0, { duration: 0 });
		await telegraphProgress.set(1, { duration: 1250 });
		telegraphTargets = [];
		telegraphBeams = [];
	};

	// glass shards burst outward from each shattering mirror cell
	const shatter = async (positions: Position[]) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;

		shards = positions.flatMap((position) => {
			// book event rows are padded: visible row = row - 1
			const cx = originX + SYMBOL_SIZE * (position.reel + 0.5);
			const cy = originY + SYMBOL_SIZE * (position.row - 1 + 0.5);
			return Array.from({ length: 14 }, () => {
				const angle = Math.random() * Math.PI * 2;
				const speed = SYMBOL_SIZE * (0.8 + Math.random() * 1.6);
				return {
					x0: cx + (Math.random() - 0.5) * SYMBOL_SIZE * 0.4,
					y0: cy + (Math.random() - 0.5) * SYMBOL_SIZE * 0.4,
					vx: Math.cos(angle) * speed,
					vy: Math.sin(angle) * speed - SYMBOL_SIZE * 0.6,
					spin: (Math.random() - 0.5) * 9,
					size: SYMBOL_SIZE * (0.06 + Math.random() * 0.1),
					color: Math.random() < 0.6 ? 0xd8ecff : 0xb887ff,
				};
			});
		});

		progress.set(0, { duration: 0 });
		await progress.set(1, { duration: 650, easing: cubicOut });
		shards = [];
		brokenCells = [];
	};

	context.eventEmitter.subscribeOnMount({
		// the crack appears on the glass and holds a beat before the shatter
		mirrorBreak: async ({ positions }) => {
			brokenCells = positions.map(cellCenter);
			brokenIn.set(0, { duration: 0 });
			await brokenIn.set(1, { duration: 130 });
			await wait(420);
		},
		mirrorShatter: async ({ positions }) => {
			await shatter(positions);
		},
		mirrorTelegraph: async ({ pairs }) => {
			await telegraph(pairs);
		},
	});

	const t = $derived(progress.current);
	const gravity = SYMBOL_SIZE * 1.6;

	// three quick pulses over the telegraph duration
	const tt = $derived(telegraphProgress.current);
	const telegraphPulse = $derived(Math.abs(Math.sin(tt * Math.PI * 3)));
</script>

<MainContainer>
	{#if telegraphTargets.length > 0}
		<Graphics
			draw={(graphics) => {
				graphics.clear();
				// spectral comets: each target gets its own comet of green energy
				// that swoops from the mirror along a randomly curved path with
				// turbulent drift, a fading tail, sparks, and a burst on arrival
				const seeded = (seed: number) => {
					const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
					return value - Math.floor(value);
				};
				const easeInOut = (f: number) => f * f * (3 - 2 * f);

				telegraphBeams.forEach((beam, beamIndex) => {
					const dx = beam.x2 - beam.x1;
					const dy = beam.y2 - beam.y1;
					const length = Math.sqrt(dx * dx + dy * dy) || 1;
					const px = -dy / length;
					const py = dx / length;

					// every comet flies differently: its own curve, speed and delay
					const curve = (seeded(beamIndex * 17 + 3) - 0.5) * SYMBOL_SIZE * 1.5;
					const delay = 0.06 + seeded(beamIndex * 29 + 7) * 0.18;
					const travel = 0.42 + seeded(beamIndex * 41 + 11) * 0.14;
					const turbFreqA = 5 + seeded(beamIndex * 53 + 13) * 4;
					const turbFreqB = 9 + seeded(beamIndex * 67 + 17) * 6;
					const headF = easeInOut(Math.max(Math.min((tt - delay) / travel, 1), 0));

					// curved flight path with living turbulence layered on top
					const pointAt = (f: number) => {
						const arc = Math.sin(Math.PI * f) * curve;
						const turb =
							Math.sin(f * turbFreqA + tt * 11 + beamIndex * 2.7) * 5 +
							Math.sin(f * turbFreqB - tt * 17 + beamIndex * 1.3) * 3;
						const swell = Math.sin(Math.PI * f);
						return {
							x: beam.x1 + dx * f + px * (arc + turb * swell),
							y: beam.y1 + dy * f + py * (arc + turb * swell),
						};
					};

					if (headF > 0 && headF < 1) {
						// tail: past positions shrink and cool from white to green
						const tailSteps = 14;
						for (let k = tailSteps; k >= 1; k--) {
							const f = headF - (k / tailSteps) * 0.3;
							if (f <= 0) continue;
							const point = pointAt(f);
							const fade = 1 - k / tailSteps;
							graphics.circle(point.x, point.y, 8 * fade + 1.5);
							graphics.fill({ color: 0xb887ff, alpha: 0.1 + 0.2 * fade });
							graphics.circle(point.x, point.y, 3.4 * fade + 0.6);
							graphics.fill({ color: 0xd0a6ff, alpha: 0.5 * fade });
						}
						// comet head: hot white core in a green corona
						const head = pointAt(headF);
						graphics.circle(head.x, head.y, 11);
						graphics.fill({ color: 0xb887ff, alpha: 0.22 });
						graphics.circle(head.x, head.y, 6);
						graphics.fill({ color: 0xd0a6ff, alpha: 0.65 });
						graphics.circle(head.x, head.y, 3);
						graphics.fill({ color: 0xf3ecff, alpha: 0.95 });
						// stray sparks flickering off the head
						const sparkSeed = Math.floor(tt * 30);
						for (let sparkIndex = 0; sparkIndex < 3; sparkIndex++) {
							const angle = seeded(sparkSeed * 7 + sparkIndex * 31 + beamIndex) * Math.PI * 2;
							const dist = 6 + seeded(sparkSeed * 13 + sparkIndex * 43 + beamIndex) * 10;
							graphics.circle(head.x + Math.cos(angle) * dist, head.y + Math.sin(angle) * dist, 1.4);
							graphics.fill({ color: 0xe6d2ff, alpha: 0.7 });
						}
					}

					// arrival burst: an expanding green ring that settles into the outline
					if (headF >= 1) {
						const since = Math.min((tt - delay - travel) / 0.2, 1);
						if (since < 1) {
							graphics.circle(beam.x2, beam.y2, SYMBOL_SIZE * 0.15 + SYMBOL_SIZE * 0.35 * since);
							graphics.stroke({ color: 0xb887ff, width: 4 * (1 - since) + 1, alpha: 0.7 * (1 - since) });
						}
					}
				});

				// pulsing outline on each target cell, in the same green as the split
				for (const target of telegraphTargets) {
					const s = SYMBOL_SIZE;
					graphics.roundRect(target.cx - s / 2 + 3, target.cy - s / 2 + 3, s - 6, s - 6, 10);
					graphics.stroke({ color: 0xb887ff, width: 6, alpha: 0.22 + 0.5 * telegraphPulse });
					graphics.roundRect(target.cx - s / 2 + 7, target.cy - s / 2 + 7, s - 14, s - 14, 8);
					graphics.stroke({ color: 0xf3ecff, width: 2, alpha: 0.28 + 0.55 * telegraphPulse });
				}
			}}
		/>
	{/if}
	<!-- cracked pane: sits over the symbol, then fades/drops away with the shards -->
	{#each brokenCells as cell, i (i)}
		<Container
			x={cell.cx}
			y={cell.cy + (shards.length > 0 ? t * SYMBOL_SIZE * 0.2 : 0)}
			alpha={brokenIn.current * (shards.length > 0 ? 1 - t : 1)}
		>
			<Sprite
				key="glassBroken"
				anchor={0.5}
				width={SYMBOL_SIZE * (1 + (shards.length > 0 ? t * 0.08 : 0))}
				height={SYMBOL_SIZE * (1 + (shards.length > 0 ? t * 0.08 : 0))}
			/>
		</Container>
	{/each}
	{#each shards as shard, i (i)}
		<Container
			x={shard.x0 + shard.vx * t}
			y={shard.y0 + shard.vy * t + gravity * t * t}
			rotation={shard.spin * t}
			alpha={1 - t}
		>
			<Graphics
				draw={(graphics) => {
					graphics.clear();
					graphics.moveTo(0, -shard.size);
					graphics.lineTo(shard.size * 0.8, shard.size * 0.7);
					graphics.lineTo(-shard.size * 0.7, shard.size * 0.5);
					graphics.closePath();
					graphics.fill({ color: shard.color, alpha: 0.85 });
					graphics.stroke({ color: 0xffffff, width: 1, alpha: 0.7 });
				}}
			/>
		</Container>
	{/each}
</MainContainer>
