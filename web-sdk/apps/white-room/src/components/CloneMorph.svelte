<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// CLONE: one symbol type is chosen; every copy on the board charges up, flashes,
	// and morphs together into the same premium.
	export type EmitterEventCloneMorph =
		| {
				type: 'cloneMorphShow';
				cells: { reel: number; row: number }[];
				from: SymbolName;
				to: SymbolName;
		  }
		| { type: 'cloneMorphHide' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolInfo, getReelYOffset } from '../game/utils';
	import { SYMBOL_SIZE } from '../game/constants';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import SymbolSprite from './SymbolSprite.svelte';

	const context = getContext();

	const CORE = 0xffffff;
	const GLASS = 0xdfe6ea;
	const GOLD = 0xf0d488;
	const DARK = 0x0a0a0a;

	type Cell = { key: string; reel: number; row: number; cx: number; cy: number; seed: number };

	let cells = $state<Cell[]>([]);
	let fromName = $state<SymbolName | null>(null);
	let toName = $state<SymbolName | null>(null);
	let phase = $state<'idle' | 'charge' | 'flash' | 'reveal'>('idle');
	let time = $state(0);

	const charge = new Tween(0);
	const flash = new Tween(0);
	const reveal = new Tween(0);

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const layout = (incoming: { reel: number; row: number }[]) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		cells = incoming.map((c) => ({
			key: `${c.reel}-${c.row}`,
			reel: c.reel,
			row: c.row,
			cx: originX + (c.reel + 0.5) * SYMBOL_SIZE,
			cy: originY + (c.row - 0.5) * SYMBOL_SIZE + getReelYOffset(c.reel),
			seed: c.reel * 31 + c.row * 7,
		}));
	};

	const run = async () => {
		phase = 'charge';
		charge.set(0, { duration: 0 });
		flash.set(0, { duration: 0 });
		reveal.set(0, { duration: 0 });
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		// gather energy across every copy
		await charge.set(1, { duration: 560, easing: cubicOut });

		// white-out flash hides the swap
		phase = 'flash';
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		shakeBoard({ intensity: Math.min(8 + cells.length * 1.5, 16), duration: 240 });
		await flash.set(1, { duration: 90 });

		// morph: the premium scales in as the flash falls
		phase = 'reveal';
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_combine_a' });
		flash.set(0, { duration: 240 });
		await reveal.set(1, { duration: 360, easing: backOut });
	};

	context.eventEmitter.subscribeOnMount({
		cloneMorphShow: async ({ cells: incoming, from, to }) => {
			if (!incoming.length) return;
			layout(incoming);
			fromName = from;
			toName = to;
			await run();
		},
		cloneMorphHide: () => {
			phase = 'idle';
			cells = [];
			fromName = null;
			toName = null;
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

	const drawBacking = (g: import('pixi.js').Graphics) => {
		const s = SYMBOL_SIZE;
		g.roundRect(-s / 2 - 2, -s / 2 - 2, s + 4, s + 4, 10);
		g.fill({ color: DARK, alpha: 0.9 });
	};

	// charge rings + orbiting sparks that spin faster as the clone gathers power
	const drawCharge = (g: import('pixi.js').Graphics, cell: Cell) => {
		const c = charge.current;
		if (c <= 0) return;
		const s = SYMBOL_SIZE;
		// contracting ring pulls energy inward
		const r = (s * 0.7) * (1 - c) + s * 0.2;
		g.circle(0, 0, r);
		g.stroke({ color: GLASS, width: 2, alpha: 0.5 * c });
		g.circle(0, 0, r * 0.7);
		g.stroke({ color: CORE, width: 1, alpha: 0.6 * c });
		for (let i = 0; i < 6; i++) {
			const a = time * (3 + i * 0.4) + cell.seed + (i * Math.PI) / 3;
			const dist = r * (0.8 + 0.2 * Math.sin(time * 5 + i));
			const x = Math.cos(a) * dist;
			const y = Math.sin(a) * dist;
			g.circle(x, y, 1.6 + rand(cell.seed + i) * 1.4);
			g.fill({ color: i % 2 === 0 ? CORE : GOLD, alpha: 0.8 * c });
		}
	};

	const drawFlash = (g: import('pixi.js').Graphics) => {
		const f = flash.current;
		if (f <= 0.01) return;
		const s = SYMBOL_SIZE;
		g.roundRect(-s / 2 - 6, -s / 2 - 6, s + 12, s + 12, 12);
		g.fill({ color: CORE, alpha: 0.92 * f });
		const ring = s * (0.3 + 0.8 * (1 - f));
		g.circle(0, 0, ring);
		g.stroke({ color: GOLD, width: 3 * f + 0.5, alpha: 0.8 * f });
	};

	// link line joining every clone copy, drawn while charging
	const drawLinks = (g: import('pixi.js').Graphics) => {
		if (phase !== 'charge' && phase !== 'flash') return;
		const a = (phase === 'charge' ? charge.current : 1) * 0.5;
		if (a <= 0.01 || cells.length < 2) return;
		const sorted = [...cells].sort((p, q) => p.reel - q.reel || p.row - q.row);
		for (let i = 0; i < sorted.length - 1; i++) {
			g.moveTo(sorted[i].cx, sorted[i].cy);
			g.lineTo(sorted[i + 1].cx, sorted[i + 1].cy);
			g.stroke({ color: GLASS, width: 1.5, alpha: a });
		}
	};
</script>

{#if phase !== 'idle' && cells.length}
	<MainContainer>
		<Container x={stateShake.x} y={stateShake.y}>
			<Graphics draw={drawLinks} />
			{#each cells as cell (cell.key)}
				{@const chargePulse = 1 + charge.current * 0.12 * (0.6 + 0.4 * Math.sin(time * 9 + cell.seed))}
				{@const revealScale = 0.55 + 0.45 * reveal.current}
				<Container x={cell.cx} y={cell.cy}>
					<Graphics draw={drawBacking} />
					{#if (phase === 'charge' || phase === 'flash') && fromName}
						<Container scale={chargePulse}>
							<SymbolSprite symbolInfo={getSymbolInfo({ rawSymbol: { name: fromName }, state: 'postWinStatic' })} />
						</Container>
						<Graphics draw={(g) => drawCharge(g, cell)} />
					{:else if phase === 'reveal' && toName}
						<Container scale={revealScale}>
							<SymbolSprite symbolInfo={getSymbolInfo({ rawSymbol: { name: toName }, state: 'postWinStatic' })} />
						</Container>
					{/if}
					<Graphics draw={drawFlash} />
				</Container>
			{/each}
		</Container>
	</MainContainer>
{/if}
