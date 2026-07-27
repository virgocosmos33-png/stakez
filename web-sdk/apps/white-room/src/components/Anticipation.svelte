<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Graphics } from 'pixi-svelte';
	import { stateBetDerived } from 'state-shared';

	import { getContext } from '../game/context';
	import type { Reel } from '../game/stateGame.svelte';
	import { REEL_PADDING, SYMBOL_SIZE, NUM_ROWS, MAX_ROWS } from '../game/constants';

	type Props = {
		reel: Reel;
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// THE WHITE ROOM anticipation: fluorescent tube column + falling ceramic dust
	// + restraint buckle flashes. NOT spectral violet light / mirror shards.
	const COL_W = SYMBOL_SIZE;
	// diamond: the fluorescent column matches THIS reel's height (it's already
	// drawn centered on the board mid-line, where every reel is centered).
	const COL_H = SYMBOL_SIZE * (NUM_ROWS[props.reel.reelIndex] ?? MAX_ROWS);

	const BONE = 0xf4f1ec;
	const SILVER = 0xc8c4bc;
	const STEEL = 0x8a8680;
	const CHARCOAL = 0x3a3632;
	const WHITE = 0xffffff;

	const IN_DURATION = 0.18;
	const OUT_DURATION = 0.22;

	let time = $state(0);
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
				if (f >= 1) phase = 'loop';
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

	type DustSpec = {
		period: number;
		delay: number;
		lane: number;
		size: number;
		spin: number;
	};
	const DUST: DustSpec[] = Array.from({ length: 14 }, (_, index) => ({
		period: 1.4 + rand(index * 7 + 1) * 1.2,
		delay: rand(index * 13 + 5) * 2.5,
		lane: (rand(index * 31 + 2) - 0.5) * COL_W * 0.7,
		size: 2 + rand(index * 23 + 3) * 5,
		spin: (rand(index * 29 + 11) - 0.5) * 8,
	}));

	const draw = (graphics: import('pixi.js').Graphics, timeValue: number, master: number) => {
		if (master <= 0.005) return;
		const halfW = COL_W / 2;
		const halfH = COL_H / 2;
		// fluorescent flicker + rare blackout
		const blackout = rand(Math.floor(timeValue * 33)) > 0.94 ? 0.1 : 1;
		const flicker = (0.65 + 0.35 * Math.sin(timeValue * 22)) * blackout;
		const a = master * flicker;

		// charcoal tube housing
		graphics.rect(-halfW * 0.55, -halfH, COL_W * 0.55, COL_H);
		graphics.fill({ color: CHARCOAL, alpha: 0.35 * master });

		// fluorescent core column
		graphics.rect(-halfW * 0.22, -halfH, COL_W * 0.22, COL_H);
		graphics.fill({ color: BONE, alpha: 0.28 * a });
		graphics.rect(-halfW * 0.08, -halfH, COL_W * 0.08, COL_H);
		graphics.fill({ color: WHITE, alpha: 0.55 * a });

		// tube edge rails (observation glass)
		for (const side of [-1, 1] as const) {
			graphics.rect(side * halfW - 2, -halfH, 4, COL_H);
			graphics.fill({ color: STEEL, alpha: 0.55 * a });
			graphics.rect(side * halfW - 0.7, -halfH, 1.4, COL_H);
			graphics.fill({ color: WHITE, alpha: 0.75 * a });
		}

		// restraint buckle flashes along the column
		for (let i = 0; i < 5; i++) {
			const y = -halfH + ((i + 0.5) / 5) * COL_H;
			const pulse = 0.5 + 0.5 * Math.sin(timeValue * 10 + i * 1.7);
			graphics.rect(-halfW * 0.42, y - 2, COL_W * 0.42, 4);
			graphics.fill({ color: SILVER, alpha: 0.45 * a * pulse });
			graphics.rect(-6, y - 5, 12, 10);
			graphics.stroke({ color: STEEL, width: 1.5, alpha: 0.7 * a * pulse });
		}

		// falling ceramic dust / tile chips
		DUST.forEach((dust, index) => {
			const local = (timeValue + dust.delay) / dust.period;
			const cycle = local - Math.floor(local);
			const y = -halfH - 10 + cycle * (COL_H + 20);
			const x = dust.lane + Math.sin(timeValue * 1.4 + index) * 6;
			const edge = Math.min(cycle / 0.12, (1 - cycle) / 0.15, 1);
			const ang = timeValue * dust.spin + index;
			const c = Math.cos(ang);
			const s = Math.sin(ang);
			const sz = dust.size;
			graphics.poly([
				x + c * sz,
				y - s * sz * 0.4,
				x - s * sz * 0.5,
				y + c * sz * 0.5,
				x - c * sz * 0.7,
				y + s * sz * 0.3,
			]);
			graphics.fill({
				color: index % 3 === 0 ? BONE : SILVER,
				alpha: 0.65 * master * Math.max(edge, 0),
			});
		});

		// horizontal scanline stutter inside the tube
		for (let i = 0; i < 6; i++) {
			const y = -halfH + ((timeValue * 80 + i * 28) % COL_H);
			graphics.rect(-halfW * 0.5, y, COL_W * 0.5, 1.5);
			graphics.fill({ color: WHITE, alpha: 0.12 * a });
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
