<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Graphics } from 'pixi-svelte';
	import { stateBetDerived } from 'state-shared';

	import { getContext } from '../game/context';
	import type { Reel } from '../game/stateGame.svelte';
	import { REEL_PADDING, SYMBOL_SIZE, BOARD_DIMENSIONS } from '../game/constants';

	type Props = {
		reel: Reel;
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// The old template anticipation spine carried Mining-Mayhem rock debris and
	// a five-row frame that never matched this 4-row board. This effect is
	// drawn in code instead: a spectral violet light column with drifting
	// mirror shards, sized off the real board metrics so every line lands
	// exactly on the reel bounds.
	const COL_W = SYMBOL_SIZE;
	const COL_H = SYMBOL_SIZE * BOARD_DIMENSIONS.y;

	const VIOLET = 0xb887ff;
	const LILAC = 0xd9b3ff;
	const DEEP = 0x7a4fd0;
	const WHITE = 0xffffff;

	const IN_DURATION = 0.24;
	const OUT_DURATION = 0.26;

	let time = $state(0);
	// master envelope: quick rise, held loop, quick fall (then oncomplete)
	let envelope = $state(0);
	let phase: 'in' | 'loop' | 'out' = 'in';
	let phaseStart = 0;
	let completed = false;

	$effect(() => {
		if (props.reel.reelState.motion === 'stopped' && phase !== 'out') {
			phase = 'out';
			phaseStart = time;
		}
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			const t = (now - start) / 1000;
			time = t;
			const speed = stateBetDerived.timeScale();
			if (phase === 'in') {
				const f = Math.min(((t - phaseStart) * speed) / IN_DURATION, 1);
				envelope = f;
				if (f >= 1) {
					phase = 'loop';
				}
			} else if (phase === 'out') {
				const f = Math.min(((t - phaseStart) * speed) / OUT_DURATION, 1);
				envelope = 1 - f;
				if (f >= 1 && !completed) {
					completed = true;
					props.oncomplete();
				}
			} else {
				envelope = 1;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	type ShardSpec = {
		period: number;
		delay: number;
		drift: number;
		size: number;
		spin: number;
		lane: number;
	};
	const SHARDS: ShardSpec[] = Array.from({ length: 9 }, (_, index) => ({
		period: 2.1 + rand(index * 7 + 1) * 1.6,
		delay: rand(index * 13 + 5) * 3,
		drift: (rand(index * 17 + 9) - 0.5) * COL_W * 0.5,
		size: 7 + rand(index * 23 + 3) * 13,
		spin: (rand(index * 29 + 11) - 0.5) * 5,
		lane: (rand(index * 31 + 2) - 0.5) * COL_W * 0.62,
	}));

	const drawShard = (
		graphics: import('pixi.js').Graphics,
		x: number,
		y: number,
		size: number,
		angle: number,
		alpha: number,
	) => {
		const cos = Math.cos(angle);
		const sin = Math.sin(angle);
		// irregular elongated glass sliver
		const points = [
			[0, -size],
			[size * 0.42, -size * 0.15],
			[size * 0.18, size * 0.95],
			[-size * 0.38, size * 0.2],
		].map(([px, py]) => [x + px * cos - py * sin, y + px * sin + py * cos]);
		graphics.poly(points.flat());
		graphics.fill({ color: LILAC, alpha: 0.5 * alpha });
		graphics.poly(points.flat());
		graphics.stroke({ color: WHITE, width: 1.2, alpha: 0.85 * alpha });
		// inner facet line
		graphics.moveTo(points[0][0], points[0][1]);
		graphics.lineTo(points[2][0], points[2][1]);
		graphics.stroke({ color: WHITE, width: 0.8, alpha: 0.4 * alpha });
	};

	const draw = (graphics: import('pixi.js').Graphics, timeValue: number, master: number) => {
		if (master <= 0.005) return;
		const halfW = COL_W / 2;
		const halfH = COL_H / 2;
		const breath = 0.82 + 0.18 * Math.sin(timeValue * 5.1) + 0.06 * rand(Math.floor(timeValue * 14));

		// soft outer halo hugging the column
		graphics.rect(-halfW * 1.28, -halfH, COL_W * 1.28, COL_H);
		graphics.fill({ color: DEEP, alpha: 0.1 * master * breath });
		// main light column
		graphics.rect(-halfW, -halfH, COL_W, COL_H);
		graphics.fill({ color: VIOLET, alpha: 0.16 * master * breath });
		// hot core band
		graphics.rect(-halfW * 0.42, -halfH, COL_W * 0.42, COL_H);
		graphics.fill({ color: LILAC, alpha: 0.1 * master * breath });

		// rising light streaks inside the column
		for (let i = 0; i < 4; i++) {
			const cycle = (timeValue * (0.5 + rand(i * 3) * 0.5) + rand(i * 11)) % 1;
			const y = halfH - cycle * COL_H;
			const streakH = COL_H * 0.16;
			graphics.rect(-halfW * 0.9, y - streakH / 2, COL_W * 0.9, streakH);
			graphics.fill({ color: LILAC, alpha: 0.05 * master * (1 - Math.abs(cycle - 0.5) * 2) });
		}

		// edge beams: exactly on the reel bounds
		for (const side of [-1, 1]) {
			graphics.rect(side * halfW - 4, -halfH, 8, COL_H);
			graphics.fill({ color: DEEP, alpha: 0.22 * master * breath });
			graphics.rect(side * halfW - 1.5, -halfH, 3, COL_H);
			graphics.fill({ color: LILAC, alpha: 0.55 * master * breath });
			graphics.rect(side * halfW - 0.5, -halfH, 1, COL_H);
			graphics.fill({ color: WHITE, alpha: 0.8 * master });
		}
		// top and bottom rails close the frame on the board bounds
		for (const side of [-1, 1]) {
			graphics.rect(-halfW, side * halfH - 1.5, COL_W, 3);
			graphics.fill({ color: LILAC, alpha: 0.5 * master * breath });
		}

		// drifting mirror shards
		SHARDS.forEach((shard, index) => {
			const local = (timeValue + shard.delay) / shard.period;
			const cycle = local - Math.floor(local);
			const y = halfH + 24 - cycle * (COL_H + 48);
			const x = shard.lane + Math.sin(timeValue * 1.7 + index) * shard.drift;
			const edgeFade = Math.min(cycle / 0.18, (1 - cycle) / 0.18, 1);
			drawShard(
				graphics,
				x,
				y,
				shard.size,
				timeValue * shard.spin + index,
				master * Math.max(edgeFade, 0) * 0.9,
			);
		});

		// spark motes
		for (let i = 0; i < 12; i++) {
			const local = (timeValue * (0.7 + rand(i * 5) * 0.8) + rand(i * 19)) % 1;
			const y = halfH - local * COL_H;
			const x = (rand(i * 7 + 2) - 0.5) * COL_W * 0.86 + Math.sin(timeValue * 2.4 + i * 1.8) * 5;
			const mote = 1 + rand(i * 3 + 1) * 2.2;
			graphics.circle(x, y, mote);
			graphics.fill({ color: i % 3 === 0 ? WHITE : LILAC, alpha: 0.5 * master * (1 - local * 0.6) });
		}
	};
</script>

<Container
	x={context.stateGameDerived.boardLayout().x -
		context.stateGameDerived.boardLayout().width * 0.5 +
		(props.reel.reelIndex + REEL_PADDING) * SYMBOL_SIZE}
	y={context.stateGameDerived.boardLayout().y}
>
	<Graphics draw={(graphics) => draw(graphics, time, envelope)} />
</Container>
