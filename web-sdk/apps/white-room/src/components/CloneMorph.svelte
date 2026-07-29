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
	import { Container, Graphics, Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import { SYMBOL_SIZE, CELL_PITCH_X } from '../game/constants';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import SymbolSprite from './SymbolSprite.svelte';

	const context = getContext();

	const CORE = 0xffffff;
	const GLASS = 0xdfe6ea;
	const GOLD = 0xf0d488;
	const DARK = 0x0a0a0a;

	type Cell = { key: string; reel: number; row: number; seed: number };

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
		// Drawn in a fixed reel/row order rather than book order. The overlay paints
		// opaque plates over live board cells, so if two clone cells are neighbours
		// an arbitrary order lets a later cell's plate clip the one next to it.
		cells = [...incoming]
			.sort((a, b) => a.reel - b.reel || a.row - b.row)
			.map((c) => ({
				key: `${c.reel}-${c.row}`,
				reel: c.reel,
				row: c.row,
				seed: c.reel * 31 + c.row * 7,
			}));
	};

	/**
	 * Cell centres, recomputed every frame instead of snapshotted at `show`.
	 *
	 * `getReelYOffset` depends on a reel's CURRENT row count, which other features
	 * (wild reel, stretch) change mid-spin. Baking the position once meant a clone
	 * that followed one of those drew its plates a whole row off the symbols they
	 * were meant to cover — you saw the settled new premium peeking out from behind
	 * an offset copy of the old one.
	 */
	const placed = $derived.by(() => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		return cells.map((cell) => ({
			...cell,
			cx: originX + getSymbolX(cell.reel),
			cy: originY + getCellCenterY(cell.reel, cell.row),
		}));
	});

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

	// Fully opaque. The handler settles the board to the NEW premium before the
	// morph starts, so anything less than opaque lets that new symbol ghost
	// through underneath the old one the overlay is still showing.
	const drawBacking = (g: import('pixi.js').Graphics) => {
		const w = CELL_PITCH_X;
		const h = SYMBOL_SIZE;
		g.roundRect(-w / 2 - 2, -h / 2 - 2, w + 4, h + 4, 10);
		g.fill({ color: DARK, alpha: 1 });
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

	// The white-out is split in two: the FILL belongs to the cell and is clipped
	// to it (it used to bleed 6px over the neighbours and white out their
	// symbols), while the expanding ring is chrome that is meant to escape.
	const drawFlashFill = (g: import('pixi.js').Graphics) => {
		const f = flash.current;
		if (f <= 0.01) return;
		const w = CELL_PITCH_X;
		const s = SYMBOL_SIZE;
		g.roundRect(-w / 2 - 6, -s / 2 - 6, w + 12, s + 12, 12);
		g.fill({ color: CORE, alpha: 0.92 * f });
	};

	const drawFlashRing = (g: import('pixi.js').Graphics) => {
		const f = flash.current;
		if (f <= 0.01) return;
		const ring = SYMBOL_SIZE * (0.3 + 0.8 * (1 - f));
		g.circle(0, 0, ring);
		g.stroke({ color: GOLD, width: 3 * f + 0.5, alpha: 0.8 * f });
	};

	// link line joining every clone copy, drawn while charging
	const drawLinks = (g: import('pixi.js').Graphics) => {
		if (phase !== 'charge' && phase !== 'flash') return;
		const a = (phase === 'charge' ? charge.current : 1) * 0.5;
		if (a <= 0.01 || placed.length < 2) return;
		for (let i = 0; i < placed.length - 1; i++) {
			g.moveTo(placed[i].cx, placed[i].cy);
			g.lineTo(placed[i + 1].cx, placed[i + 1].cy);
			g.stroke({ color: GLASS, width: 1.5, alpha: a });
		}
	};
</script>

<!-- MainContainer stays MOUNTED even while idle: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). -->
<MainContainer>
	{#if phase !== 'idle' && cells.length}
		<Container x={stateShake.x} y={stateShake.y}>
			<Graphics draw={drawLinks} />

			<!-- PASS 1 — the cells themselves. Each is clipped to its own cell, so
				the charge pulse and the reveal's backOut overshoot can grow past the
				card without ever spilling a symbol onto the cell next door. Every
				plate is drawn before any chrome, so no cell can paint over another's
				symbol either. -->
			{#each placed as cell (cell.key)}
				{@const chargePulse = 1 + charge.current * 0.12 * (0.6 + 0.4 * Math.sin(time * 9 + cell.seed))}
				{@const revealScale = 0.55 + 0.45 * reveal.current}
				<Container x={cell.cx} y={cell.cy}>
					<Rectangle
						isMask
						anchor={0.5}
						width={CELL_PITCH_X}
						height={SYMBOL_SIZE}
						backgroundColor={0xffffff}
					/>
					<Graphics draw={drawBacking} />
					{#if (phase === 'charge' || phase === 'flash') && fromName}
						<Container scale={chargePulse}>
							<SymbolSprite symbolInfo={getSymbolInfo({ rawSymbol: { name: fromName }, state: 'postWinStatic' })} />
						</Container>
					{:else if phase === 'reveal' && toName}
						<Container scale={revealScale}>
							<SymbolSprite symbolInfo={getSymbolInfo({ rawSymbol: { name: toName }, state: 'postWinStatic' })} />
						</Container>
					{/if}
					<Graphics draw={drawFlashFill} />
				</Container>
			{/each}

			<!-- PASS 2 — chrome that is supposed to reach outside its cell -->
			{#each placed as cell (cell.key)}
				<Container x={cell.cx} y={cell.cy}>
					{#if phase === 'charge' || phase === 'flash'}
						<Graphics draw={(g) => drawCharge(g, cell)} />
					{/if}
					<Graphics draw={drawFlashRing} />
				</Container>
			{/each}
		</Container>
	{/if}
</MainContainer>
