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
	import { fxNum, fxColors } from '../game/fx.generated';

	const context = getContext();

	// parametric FX (panel-editable via game-builder config)
	const TELEGRAPH_SHARDS = fxNum('splitTelegraph', 'shardsPerTarget', 8);
	const TELEGRAPH_MS = fxNum('splitTelegraph', 'durationMs', 340);
	const TELEGRAPH_COLORS = fxColors('splitTelegraph', 'colors', [0xd8ecff, 0xc9a8ff]);
	const SHATTER_SHARDS = fxNum('splitShatter', 'shardsPerCell', 14);
	const SHATTER_MS = fxNum('splitShatter', 'durationMs', 650);
	const SHATTER_COLORS = fxColors('splitShatter', 'colors', [0xd8ecff, 0xb887ff]);
	const BREAK_POP_MS = fxNum('mirrorBreak', 'popMs', 130);
	const BREAK_HOLD_MS = fxNum('mirrorBreak', 'holdMs', 420);

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

	let brokenCells = $state<{ cx: number; cy: number }[]>([]);
	const brokenIn = new Tween(0);
	const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

	// telegraph: many tiny glass shards stab mirror → split targets (fast volley)
	type TelegraphTarget = { cx: number; cy: number };
	type TelegraphBeam = { x1: number; y1: number; x2: number; y2: number; seed: number };
	let telegraphTargets = $state<TelegraphTarget[]>([]);
	let telegraphBeams = $state<TelegraphBeam[]>([]);
	const telegraphProgress = new Tween(0);

	const cellCenter = (position: Position) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		return {
			cx: originX + SYMBOL_SIZE * (position.reel + 0.5),
			cy: originY + SYMBOL_SIZE * (position.row - 1 + 0.5),
		};
	};

	const seeded = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const telegraph = async (pairs: { mirror: Position; targets: Position[] }[]) => {
		telegraphTargets = pairs.flatMap((pair) => pair.targets.map(cellCenter));
		const SHARDS_PER_TARGET = TELEGRAPH_SHARDS;
		telegraphBeams = pairs.flatMap((pair, pairIndex) => {
			const from = cellCenter(pair.mirror);
			return pair.targets.flatMap((target, targetIndex) => {
				const to = cellCenter(target);
				return Array.from({ length: SHARDS_PER_TARGET }, (_, shardIndex) => {
					const seed = pairIndex * 997 + targetIndex * 131 + shardIndex * 17;
					return {
						x1: from.cx + (seeded(seed + 1) - 0.5) * SYMBOL_SIZE * 0.28,
						y1: from.cy + (seeded(seed + 2) - 0.5) * SYMBOL_SIZE * 0.28,
						x2: to.cx + (seeded(seed + 3) - 0.5) * SYMBOL_SIZE * 0.4,
						y2: to.cy + (seeded(seed + 4) - 0.5) * SYMBOL_SIZE * 0.4,
						seed,
					};
				});
			});
		});
		telegraphProgress.set(0, { duration: 0 });
		await telegraphProgress.set(1, { duration: TELEGRAPH_MS });
		telegraphTargets = [];
		telegraphBeams = [];
	};

	const shatter = async (positions: Position[]) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;

		shards = positions.flatMap((position) => {
			const cx = originX + SYMBOL_SIZE * (position.reel + 0.5);
			const cy = originY + SYMBOL_SIZE * (position.row - 1 + 0.5);
			return Array.from({ length: SHATTER_SHARDS }, () => {
				const angle = Math.random() * Math.PI * 2;
				const speed = SYMBOL_SIZE * (0.8 + Math.random() * 1.6);
				return {
					x0: cx + (Math.random() - 0.5) * SYMBOL_SIZE * 0.4,
					y0: cy + (Math.random() - 0.5) * SYMBOL_SIZE * 0.4,
					vx: Math.cos(angle) * speed,
					vy: Math.sin(angle) * speed - SYMBOL_SIZE * 0.6,
					spin: (Math.random() - 0.5) * 9,
					size: SYMBOL_SIZE * (0.06 + Math.random() * 0.1),
					color: Math.random() < 0.6 ? SHATTER_COLORS[0] : (SHATTER_COLORS[1] ?? SHATTER_COLORS[0]),
				};
			});
		});

		progress.set(0, { duration: 0 });
		await progress.set(1, { duration: SHATTER_MS, easing: cubicOut });
		shards = [];
		brokenCells = [];
	};

	context.eventEmitter.subscribeOnMount({
		mirrorBreak: async ({ positions }) => {
			brokenCells = positions.map(cellCenter);
			brokenIn.set(0, { duration: 0 });
			await brokenIn.set(1, { duration: BREAK_POP_MS });
			await wait(BREAK_HOLD_MS);
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
	const tt = $derived(telegraphProgress.current);
	const telegraphPulse = $derived(Math.abs(Math.sin(tt * Math.PI * 5)));

	// tiny glass shards — stabbing volley (not the big knife)
	type StabShard = {
		key: number;
		x: number;
		y: number;
		rotation: number;
		alpha: number;
		size: number;
		color: number;
		arrived: boolean;
		tx: number;
		ty: number;
		since: number;
	};

	const stabShards = $derived.by((): StabShard[] => {
		return telegraphBeams.map((beam, beamIndex) => {
			const dx = beam.x2 - beam.x1;
			const dy = beam.y2 - beam.y1;
			const length = Math.sqrt(dx * dx + dy * dy) || 1;
			const px = -dy / length;
			const py = dx / length;
			// almost straight — slight jitter, not a big lazy arc
			const curve = (seeded(beam.seed + 3) - 0.5) * SYMBOL_SIZE * 0.22;
			// staggered rapid fire within the short volley window
			const delay = seeded(beam.seed + 7) * 0.45;
			const travel = 0.18 + seeded(beam.seed + 11) * 0.12; // snappy flight
			const raw = (tt - delay) / travel;
			// ease-in for stab punch (accelerate into the hit)
			const headF = Math.max(Math.min(raw * raw, 1), 0);

			const pointAt = (f: number) => {
				const arc = Math.sin(Math.PI * f) * curve;
				return {
					x: beam.x1 + dx * f + px * arc,
					y: beam.y1 + dy * f + py * arc,
				};
			};

			const head = pointAt(Math.min(Math.max(headF, 0.001), 0.999));
			const ahead = pointAt(Math.min(headF + 0.04, 1));
			const rotation = Math.atan2(ahead.y - head.y, ahead.x - head.x);
			const since = headF >= 1 ? Math.min((tt - delay - travel) / 0.12, 1) : 0;
			const size = SYMBOL_SIZE * (0.045 + seeded(beam.seed + 13) * 0.055);
			const color = seeded(beam.seed + 19) < 0.55 ? TELEGRAPH_COLORS[0] : (TELEGRAPH_COLORS[1] ?? TELEGRAPH_COLORS[0]);

			return {
				key: beamIndex,
				x: head.x,
				y: head.y,
				rotation,
				alpha:
					headF > 0 && headF < 1
						? 0.95
						: headF >= 1 && since < 1
							? 0.85 * (1 - since)
							: 0,
				size,
				color,
				arrived: headF >= 1,
				tx: beam.x2,
				ty: beam.y2,
				since,
			};
		});
	});
</script>

<MainContainer>
	{#if telegraphTargets.length > 0}
		<!-- flying glass shards + stab impacts + target outlines -->
		<Graphics
			draw={(graphics) => {
				graphics.clear();
				for (const shard of stabShards) {
					if (shard.alpha > 0.01 && !shard.arrived) {
						const s = shard.size;
						const c = Math.cos(shard.rotation);
						const sn = Math.sin(shard.rotation);
						// elongated glass spike pointed along flight (stab silhouette)
						const tipX = shard.x + c * s * 1.4;
						const tipY = shard.y + sn * s * 1.4;
						const b1x = shard.x - c * s * 0.7 + -sn * s * 0.45;
						const b1y = shard.y - sn * s * 0.7 + c * s * 0.45;
						const b2x = shard.x - c * s * 0.7 - -sn * s * 0.45;
						const b2y = shard.y - sn * s * 0.7 - c * s * 0.45;
						graphics.moveTo(tipX, tipY);
						graphics.lineTo(b1x, b1y);
						graphics.lineTo(b2x, b2y);
						graphics.closePath();
						graphics.fill({ color: shard.color, alpha: shard.alpha });
						graphics.stroke({ color: 0xffffff, width: 0.8, alpha: shard.alpha * 0.75 });
					}
					if (shard.arrived && shard.since < 1) {
						// sharp hit flash — small + fast (stab impact)
						const r = SYMBOL_SIZE * (0.06 + 0.22 * shard.since);
						graphics.circle(shard.tx, shard.ty, r);
						graphics.stroke({
							color: 0xf3ecff,
							width: 2.2 * (1 - shard.since) + 0.5,
							alpha: 0.85 * (1 - shard.since),
						});
						graphics.circle(shard.tx, shard.ty, r * 0.45);
						graphics.fill({
							color: 0xb887ff,
							alpha: 0.35 * (1 - shard.since),
						});
					}
				}
				for (const target of telegraphTargets) {
					const s = SYMBOL_SIZE;
					graphics.roundRect(target.cx - s / 2 + 3, target.cy - s / 2 + 3, s - 6, s - 6, 10);
					graphics.stroke({ color: 0xb887ff, width: 5, alpha: 0.2 + 0.45 * telegraphPulse });
					graphics.roundRect(target.cx - s / 2 + 7, target.cy - s / 2 + 7, s - 14, s - 14, 8);
					graphics.stroke({ color: 0xf3ecff, width: 1.6, alpha: 0.25 + 0.5 * telegraphPulse });
				}
			}}
		/>
	{/if}

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
