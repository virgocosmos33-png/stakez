<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	export type EmitterEventNudgeSlide =
		| {
				type: 'nudgeSlideShow';
				symbol: SymbolName;
				baseMult: number;
				winMult: number;
				/** premiums crossed, ordered right-to-left (encounter order) */
				hits: { reel: number; row: number }[];
		  }
		| { type: 'nudgeSlideHide' };
</script>

<script lang="ts">
	/**
	 * Horizontal NUDGE: the bounty premium lifts out of the last-reel lane and
	 * slides LEFT across the board. Each premium it passes bumps the WIN
	 * multiplier badge, turns that cell into a WILD, and leaves a burning
	 * ember ring until the next spin rides feature FX off the board.
	 */
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicInOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Text, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';

	const context = getContext();

	type BurnMark = {
		key: string;
		reel: number;
		row: number;
		cx: number;
		cy: number;
		/** 0 = cold, 1 = fully lit */
		ignite: Tween<number>;
		seed: number;
	};

	let show = $state(false);
	let symbol = $state<SymbolName>('H1');
	let mult = $state(1);
	let burns = $state<BurnMark[]>([]);
	let time = $state(0);
	const x = new Tween(0);
	const y = new Tween(0);
	const scale = new Tween(1);
	const badgePop = new Tween(1);
	const fallOut = new Tween(0);

	const lastReel = () => context.stateGame.board.length - 1;

	const cellWorld = (reel: number, row: number) => {
		const board = context.stateGameDerived.boardLayout();
		return {
			x: board.x - board.width * 0.5 + getSymbolX(reel),
			y: board.y - board.height * 0.5 + getCellCenterY(reel, row),
		};
	};

	/** Scorch the cell: swap the board symbol to WILD under the burn ring. */
	const leaveWild = (reel: number, row: number) => {
		const reelSymbol = context.stateGame.board[reel]?.reelState.symbols[row];
		if (!reelSymbol) return;
		reelSymbol.rawSymbol = { ...reelSymbol.rawSymbol, name: 'W' };
		reelSymbol.symbolState = 'static';
	};

	const igniteBurn = (reel: number, row: number) => {
		const key = `${reel}-${row}`;
		if (burns.some((b) => b.key === key)) return;
		const { x: cx, y: cy } = cellWorld(reel, row);
		const ignite = new Tween(0);
		burns = [
			...burns,
			{
				key,
				reel,
				row,
				cx,
				cy,
				ignite,
				seed: reel * 31 + row * 17 + burns.length * 97,
			},
		];
		ignite.set(1, { duration: fxDur(420), easing: cubicOut });
	};

	const clearBurns = () => {
		burns = [];
		fallOut.set(0, { duration: 0 });
	};

	const run = async (e: {
		symbol: SymbolName;
		baseMult: number;
		winMult: number;
		hits: { reel: number; row: number }[];
	}) => {
		symbol = e.symbol;
		mult = e.baseMult;
		clearBurns();
		const start = cellWorld(lastReel(), 1);
		x.set(start.x, { duration: 0 });
		y.set(start.y, { duration: 0 });
		scale.set(1, { duration: 0 });
		show = true;

		// lift out of the lane — deliberate, not snappy
		await scale.set(1.22, { duration: fxDur(320) });
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });

		let passed = 0;
		for (const hit of e.hits) {
			const dest = cellWorld(hit.reel, hit.row);
			const prevReel = passed === 0 ? lastReel() : e.hits[passed - 1].reel;
			const dist = Math.max(1, Math.abs(hit.reel - prevReel));
			// slow crawl across each gap so the burn read lands
			const hopMs = fxDur(420 + dist * 160);
			await Promise.all([
				x.set(dest.x, { duration: hopMs, easing: cubicInOut }),
				y.set(dest.y, { duration: hopMs, easing: cubicInOut }),
			]);
			passed += 1;
			mult = Math.min(e.winMult, e.baseMult + passed);
			leaveWild(hit.reel, hit.row);
			igniteBurn(hit.reel, hit.row);
			badgePop.set(1.45, { duration: 0 });
			badgePop.set(1, { duration: fxDur(360) });
			shakeBoard({ intensity: 6, duration: fxDur(180) });
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
			// dwell on the scorch so the wild + burn read before the next hop
			await fxWait(280);
		}

		// finish the slide into the far-left column
		const end = cellWorld(0, 1);
		await Promise.all([
			x.set(end.x, { duration: fxDur(520), easing: cubicInOut }),
			y.set(end.y, { duration: fxDur(520), easing: cubicInOut }),
		]);
		mult = e.winMult;
		await scale.set(1, { duration: fxDur(280) });
		await fxWait(400);
		// rider card goes away; burns stay until the next spin
		show = false;
	};

	context.eventEmitter.subscribeOnMount({
		nudgeSlideShow: (e) => run(e),
		nudgeSlideHide: () => {
			show = false;
			clearBurns();
		},
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, burns.length > 0);
			show = false;
			clearBurns();
		},
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

	const drawBadge = (g: import('pixi.js').Graphics) => {
		g.clear();
		g.roundRect(-28, -14, 56, 28, 8);
		g.fill({ color: 0x1a1208, alpha: 0.92 });
		g.roundRect(-28, -14, 56, 28, 8);
		g.stroke({ color: 0xe0b45a, width: 2, alpha: 0.95 });
	};

	/** persistent ember ring + licking tongues on a hit premium */
	const drawBurn = (g: import('pixi.js').Graphics, burn: BurnMark) => {
		g.clear();
		const a = burn.ignite.current;
		if (a < 0.01) return;
		const w = SYMBOL_CARD_W;
		const h = SYMBOL_CARD_H;
		const flicker = 0.85 + 0.15 * Math.sin(time * 11 + burn.seed);

		// soft underglow — the card looks charred from within
		g.roundRect(-w * 0.52, -h * 0.52, w * 1.04, h * 1.04, 10);
		g.fill({ color: 0x3a1008, alpha: 0.55 * a * flicker });
		g.roundRect(-w * 0.48, -h * 0.48, w * 0.96, h * 0.96, 8);
		g.fill({ color: 0x8a2a10, alpha: 0.22 * a });

		// outer heat halo
		g.roundRect(-w * 0.58, -h * 0.58, w * 1.16, h * 1.16, 14);
		g.stroke({ color: 0xff6a20, width: 10, alpha: 0.18 * a * flicker });
		g.roundRect(-w * 0.54, -h * 0.54, w * 1.08, h * 1.08, 12);
		g.stroke({ color: 0xffa040, width: 3.5, alpha: 0.55 * a * flicker });

		// brass-hot rim
		g.roundRect(-w * 0.5, -h * 0.5, w, h, 9);
		g.stroke({ color: 0xffd080, width: 1.5, alpha: 0.75 * a * flicker });

		// licking tongues around the edge
		const tongues = 10;
		for (let i = 0; i < tongues; i++) {
			const u = i / tongues;
			const side = i % 4;
			let bx = 0;
			let by = 0;
			let nx = 0;
			let ny = 0;
			const along = (u * 4) % 1;
			if (side === 0) {
				bx = -w * 0.5 + along * w;
				by = -h * 0.5;
				nx = 0;
				ny = -1;
			} else if (side === 1) {
				bx = w * 0.5;
				by = -h * 0.5 + along * h;
				nx = 1;
				ny = 0;
			} else if (side === 2) {
				bx = w * 0.5 - along * w;
				by = h * 0.5;
				nx = 0;
				ny = 1;
			} else {
				bx = -w * 0.5;
				by = h * 0.5 - along * h;
				nx = -1;
				ny = 0;
			}
			const wave =
				0.55 +
				0.45 * Math.sin(time * (7 + (i % 3)) + burn.seed * 0.3 + i * 1.7);
			const len = (10 + 16 * wave) * a;
			const tipX = bx + nx * len;
			const tipY = by + ny * len - Math.abs(nx) * 4 * wave; // lift upward a bit
			const lean = (i % 2 === 0 ? 1 : -1) * (3 + 2 * wave);
			const px = -ny * lean;
			const py = nx * lean;
			g.poly([bx - px, by - py, tipX, tipY, bx + px, by + py]);
			g.fill({
				color: i % 3 === 0 ? 0xffe0a0 : i % 3 === 1 ? 0xff8a30 : 0xff4020,
				alpha: (0.55 + 0.35 * wave) * a,
			});
		}

		// rising sparks
		for (let i = 0; i < 6; i++) {
			const life = (time * (1.4 + (i % 3) * 0.35) + burn.seed * 0.01 + i * 0.37) % 1;
			const sx = (Math.sin(burn.seed + i * 2.1) * 0.42) * w;
			const sy = h * 0.35 - life * h * 0.95;
			const r = (1.6 + (1 - life) * 2.2) * a;
			g.circle(sx, sy, r);
			g.fill({
				color: life > 0.7 ? 0xffe8b0 : 0xff7020,
				alpha: (1 - life) * 0.85 * a,
			});
		}
	};

	const frameKey = $derived(`${String(symbol).toLowerCase()}.webp`);
</script>

<!-- Burns stay mounted after the rider card hides; fall out with other feature FX. -->
<MainContainer>
	{#if burns.length > 0}
		<Container x={stateShake.x} y={stateShake.y + fallOut.current}>
			{#each burns as burn (burn.key)}
				<Container x={burn.cx} y={burn.cy}>
					<Graphics draw={(g) => drawBurn(g, burn)} />
				</Container>
			{/each}
		</Container>
	{/if}

	{#if show}
		<Container x={x.current} y={y.current} scale={scale.current}>
			<!-- heat trail under the rider -->
			<Graphics
				draw={(g) => {
					g.clear();
					g.roundRect(
						-SYMBOL_CARD_W * 0.55,
						-SYMBOL_CARD_H * 0.55,
						SYMBOL_CARD_W * 1.1,
						SYMBOL_CARD_H * 1.1,
						12,
					);
					g.fill({ color: 0xff6020, alpha: 0.22 });
				}}
			/>
			<Sprite
				key={frameKey}
				anchor={0.5}
				width={SYMBOL_CARD_W * 1.05}
				height={SYMBOL_CARD_H * 1.05}
			/>
			<Container y={SYMBOL_CARD_H * 0.42} scale={badgePop.current}>
				<Graphics draw={drawBadge} />
				<Text
					anchor={0.5}
					text={`×${mult}`}
					eventMode="none"
					style={{
						fill: 0xf0d090,
						fontSize: 18,
						fontWeight: '700',
						fontFamily: '"Segoe UI", Arial, sans-serif',
					}}
				/>
			</Container>
		</Container>
	{/if}
</MainContainer>
