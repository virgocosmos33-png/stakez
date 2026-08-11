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

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { filterVisibleCells } from '../game/boardCells';
	import { fxDur } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import { SYMBOL_SIZE, CELL_PITCH_X } from '../game/constants';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX } from '../game/tombstoneVfx';
	import SymbolSprite from './SymbolSprite.svelte';

	const context = getContext();

	const BRASS = TOMBSTONE_FX.brass;
	const DUST = TOMBSTONE_FX.dust;
	const DARK = TOMBSTONE_FX.dark;

	type Cell = { key: string; reel: number; row: number; seed: number };

	let cells = $state<Cell[]>([]);
	let fromName = $state<SymbolName | null>(null);
	let toName = $state<SymbolName | null>(null);
	let phase = $state<'idle' | 'charge' | 'flash' | 'reveal'>('idle');
	let time = $state(0);

	const charge = new Tween(0);
	const flash = new Tween(0);
	const reveal = new Tween(0);
	// rides the morphed cards off the bottom edge when the next spin starts
	const fallOut = new Tween(0);

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const layout = (incoming: { reel: number; row: number }[]) => {
		// Drawn in a fixed reel/row order rather than book order. The overlay paints
		// opaque plates over live board cells, so if two clone cells are neighbours
		// an arbitrary order lets a later cell's plate clip the one next to it.
		// Skip pad / OOB rows — those sockets are empty on the diamond board.
		cells = filterVisibleCells([...incoming])
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
		// the dashed powder fuse burning along the link
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fuse_crackle' });
		// gather energy across every copy
		await charge.set(1, { duration: fxDur(560), easing: cubicOut });

		// brass muzzle flash hides the swap
		phase = 'flash';
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		shakeBoard({ intensity: Math.min(8 + cells.length * 1.5, 16), duration: fxDur(240) });
		await flash.set(1, { duration: fxDur(90) });

		// morph: the premium scales in as the ember front sweeps through
		phase = 'reveal';
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_ember_whoosh' });
		flash.set(0, { duration: fxDur(240) });
		await reveal.set(1, { duration: fxDur(360), easing: backOut });
	};

	context.eventEmitter.subscribeOnMount({
		cloneMorphShow: async ({ cells: incoming, from, to }) => {
			if (!incoming.length) return;
			layout(incoming);
			fromName = from;
			toName = to;
			// the copies are linked: set them burning for the whole morph. The
			// fire is what says "these belong together" — no line is drawn
			// between them any more.
			context.eventEmitter.broadcast({
				type: 'cellFireShow',
				cells: cells.map((c) => ({ reel: c.reel, row: c.row })),
				level: cells.length,
			});
			await run();
		},
		// the next spin is under way: the morphed cards ride down and off with
		// the symbols instead of popping when the reveal lands.
		featureFxFallOut: async () => {
			context.eventEmitter.broadcast({ type: 'cellFireHide' });
			await fallOutFeatureFx(fallOut, phase !== 'idle' && cells.length > 0);
			phase = 'idle';
			cells = [];
			fromName = null;
			toName = null;
			fallOut.set(0, { duration: 0 });
		},
		cloneMorphHide: () => {
			context.eventEmitter.broadcast({ type: 'cellFireHide' });
			phase = 'idle';
			cells = [];
			fromName = null;
			toName = null;
			fallOut.set(0, { duration: 0 });
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

	/**
	 * Dust drawn in from the card EDGES as the clone gathers.
	 *
	 * Two earlier passes both drew a circle here: first concentric rings with
	 * orbiting beads, then "four gapped arcs" — but four arcs struck on one
	 * radius is still a ring, and on a dark card it reads as the energy-orb
	 * reticle from the game this was cloned from. There is no radius left: the
	 * gather is four straight dust bands sliding in against the card sides,
	 * with embers riding them inward.
	 */
	const drawCharge = (g: import('pixi.js').Graphics, cell: Cell) => {
		const c = charge.current;
		if (c <= 0) return;
		const w = CELL_PITCH_X;
		const s = SYMBOL_SIZE;
		const inset = (1 - c) * s * 0.42;
		const band = 4 * c + 1;
		for (const sy of [-1, 1]) {
			g.rect(-w * 0.3, sy * (s / 2 - inset) - band / 2, w * 0.6, band);
			g.fill({ color: DUST, alpha: 0.2 * c });
		}
		for (const sx of [-1, 1]) {
			g.rect(sx * (w / 2 - inset) - band / 2, -s * 0.3, band, s * 0.6);
			g.fill({ color: DUST, alpha: 0.2 * c });
		}
		// embers riding the dust inward, as short streaks not orbiting dots
		for (let i = 0; i < 5; i++) {
			const side = i % 2 === 0 ? -1 : 1;
			const along = (rand(cell.seed + i) - 0.5) * s * 0.7;
			const drift = (s / 2 - inset) * (0.9 + 0.1 * Math.sin(time * 4 + i));
			const x = i < 3 ? along : side * drift;
			const y = i < 3 ? side * drift : along;
			const len = 3 + rand(cell.seed + i * 3) * 5;
			g.moveTo(x, y);
			g.lineTo(x + (i < 3 ? 0 : -side * len), y + (i < 3 ? -side * len : 0));
			g.stroke({ color: i % 2 === 0 ? BRASS : DUST, width: 1.4, alpha: 0.5 * c });
		}
	};

	/**
	 * The cover that hides the swap. It has to reach near-opaque at peak or the
	 * incoming symbol ghosts through, and that is exactly why it kept reading as
	 * a pale panel dropped over the cell: it was mid-grey gunsmoke at 0.74. It
	 * masks just as well in powder and shadow, and a dark cell is the point.
	 */
	const drawFlashFill = (g: import('pixi.js').Graphics) => {
		const f = flash.current;
		if (f <= 0.01) return;
		const w = CELL_PITCH_X;
		const s = SYMBOL_SIZE;
		g.roundRect(-w / 2 - 6, -s / 2 - 6, w + 12, s + 12, 12);
		g.fill({ color: TOMBSTONE_FX.powder, alpha: 0.88 * f });
		g.roundRect(-w / 2 - 6, -s / 2 - 6, w + 12, s + 12, 12);
		g.fill({ color: TOMBSTONE_FX.dark, alpha: 0.4 * f });
	};

	// Powder trail joining every clone copy, drawn while charging. A solid brass
	// line strung a bright gold wire diagonally across the board; a broken fuse
	// in dust keeps the link readable without drawing a ruled line over cells.
</script>

<!-- MainContainer stays MOUNTED even while idle: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). -->
<MainContainer>
	{#if phase !== 'idle' && cells.length}
		<Container x={stateShake.x} y={stateShake.y + fallOut.current}>
			<!-- No connector is drawn between clone cells. A dashed powder fuse
				used to run cell to cell, which crosses a card corner to corner
				whenever two clones are diagonal neighbours and lands as a pale
				band over an otherwise dark cell. The cells burn instead, and the
				fire is what says they are connected. -->

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
				</Container>
			{/each}
		</Container>
	{/if}
</MainContainer>
