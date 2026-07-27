<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// SPLIT: the winning symbol is sliced into N center-cropped vertical panes that
	// snap apart (Madam-Mirror style pane-split), leaving a slim-seam "XN" cell.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolInfo, getReelYOffset } from '../game/utils';
	import {
		SYMBOL_SIZE,
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
		HIGH_SYMBOLS,
	} from '../game/constants';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import SymbolSprite from './SymbolSprite.svelte';

	const context = getContext();

	// clinical White Room palette: white-hot cut, cold steel glass, blood-red bleed.
	const CORE = 0xffffff;
	const GLASS = 0xdfe6ea;
	const BLOOD = 0xff2d2d;
	const DARK = 0x0a0a0a;

	type SplitCell = {
		key: string;
		reel: number;
		row: number;
		count: number;
		name: SymbolName;
		cx: number;
		cy: number;
		seed: number;
	};

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	let time = $state(0);

	// 0 = whole symbol, 1 = fully split into panes
	const splitProgress = new Tween(1);
	// blade head sweeps top -> bottom carving the seams
	const cutSweep = new Tween(0);
	const seamFlare = new Tween(0);
	const detonation = new Tween(0);
	const pulse = new Tween(1);

	const MANY_SPLITS = 5;

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const layout = (incoming: { reel: number; row: number; count: number; name?: SymbolName }[]) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		// reels shown as a full wild column (Wild Reel or Stretch) swallow the split:
		// the extra ways still count, but we never paint panes over the wild column.
		const wildReels = new Set([
			...context.stateGame.wildReelReels,
			...context.stateGame.stretchedReels,
		]);
		const found: SplitCell[] = [];
		for (const c of incoming) {
			if (c.count <= 1 || wildReels.has(c.reel)) continue;
			const reelSymbol = context.stateGame.board[c.reel]?.reelState.symbols[c.row];
			const name = (c.name ?? reelSymbol?.rawSymbol.name) as SymbolName | undefined;
			if (!name) continue;
			found.push({
				key: `${c.reel}-${c.row}`,
				reel: c.reel,
				row: c.row,
				count: c.count,
				name,
				cx: originX + (c.reel + 0.5) * SYMBOL_SIZE,
				cy: originY + (c.row - 0.5) * SYMBOL_SIZE + getReelYOffset(c.reel),
				seed: c.reel * 31 + c.row * 7 + c.count * 113,
			});
		}
		cells = found;
		show = found.length > 0;
	};

	// one decisive blade cut down every seam, hit-stop flare, then the panes snap
	// apart with a detonation flash + board kick.
	const runSplit = async () => {
		splitProgress.set(0, { duration: 0 });
		cutSweep.set(0, { duration: 0 });
		seamFlare.set(0, { duration: 0 });
		detonation.set(0, { duration: 0 });
		pulse.set(1.32, { duration: 0 });
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		await cutSweep.set(1, { duration: 150, easing: cubicIn });

		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_combine_a' });
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		seamFlare.set(1, { duration: 20 });
		seamFlare.set(0, { duration: 160 });
		shakeBoard({ intensity: Math.min(10 + cells.length * 2.5, 18), duration: 240 });
		const fx = detonation.set(1, { duration: 320, easing: cubicOut });
		const punch = pulse.set(1, { duration: 420, easing: backOut });
		await splitProgress.set(1, { duration: 150, easing: backOut });
		await fx;
		await punch;
	};

	context.eventEmitter.subscribeOnMount({
		splitPanesShow: async ({ cells: incoming }) => {
			layout(incoming);
			if (!cells.length) return;
			await runSplit();
		},
		splitPanesHide: () => {
			show = false;
			cells = [];
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

	const drawUnderGlow = (g: import('pixi.js').Graphics) => {
		g.roundRect(-CARD_W / 2 - 2, -CARD_H / 2 - 2, CARD_W + 4, CARD_H + 4, 10);
		g.fill({ color: DARK, alpha: 0.9 });
	};

	// steel observation frame around the settled split cell
	const drawFrame = (g: import('pixi.js').Graphics, isHigh: boolean) => {
		g.roundRect(-CARD_W / 2 - 3, -CARD_H / 2 - 3, CARD_W + 6, CARD_H + 6, 11);
		g.stroke({ color: isHigh ? 0xc9a34a : GLASS, width: 2, alpha: 0.7 });
	};

	// settled seam between panes: white core with a cold glass glow + faint blood bleed
	const drawDivider = (
		g: import('pixi.js').Graphics,
		cell: SplitCell,
		dividerIndex: number,
		slim: number,
	) => {
		const s = CARD_H;
		const half = s / 2;
		const flicker = 0.9 + 0.1 * Math.sin(time * 14 + cell.seed * 3 + dividerIndex * 1.7);
		const glowW = 5 * slim + 1;
		g.roundRect(-glowW / 2, -half, glowW, s, 3);
		g.fill({ color: BLOOD, alpha: 0.14 * flicker * slim });
		const innerW = 2.4 * slim + 0.5;
		g.roundRect(-innerW / 2, -half, innerW, s, 1);
		g.fill({ color: GLASS, alpha: 0.5 * flicker });
		const coreW = 0.7 * slim + 0.3;
		g.roundRect(-coreW / 2, -half, coreW, s, 0.4);
		g.fill({ color: CORE, alpha: 0.92 * flicker });
	};

	// the blade of light sweeping down a seam while the symbol is still whole
	const drawCutBlade = (
		g: import('pixi.js').Graphics,
		cell: SplitCell,
		dividerIndex: number,
		sweepValue: number,
	) => {
		if (sweepValue <= 0) return;
		const s = CARD_H;
		const half = s / 2;
		const margin = 22;
		const travel = s + margin * 2;
		const headY = -half - margin + Math.min(sweepValue, 1) * travel;
		const trailTop = -half - margin;
		const segments = 8;
		const trailEnd = Math.min(headY, half + margin);
		for (let i = 0; i < segments; i++) {
			const y0 = trailTop + ((trailEnd - trailTop) / segments) * i;
			const y1 = trailTop + ((trailEnd - trailTop) / segments) * (i + 1);
			const heat = (i + 1) / segments;
			g.rect(-3, y0, 6, y1 - y0);
			g.fill({ color: BLOOD, alpha: 0.12 * heat });
			g.rect(-0.9, y0, 1.8, y1 - y0);
			g.fill({ color: CORE, alpha: 0.95 * heat });
		}
		if (sweepValue < 1) {
			g.poly([0, headY + 16, 3.4, headY + 2, 0, headY - 22, -3.4, headY + 2]);
			g.fill({ color: CORE, alpha: 0.98 });
			g.ellipse(0, headY, 16, 2);
			g.fill({ color: CORE, alpha: 0.55 });
			for (let i = 0; i < 4; i++) {
				const sparkSeed = cell.seed * 13 + dividerIndex * 29 + i * 7;
				const life = (time * (3 + rand(sparkSeed) * 2) + rand(sparkSeed + 1)) % 1;
				const angle = -Math.PI / 2 + (rand(sparkSeed + 2) - 0.5) * 2.2;
				const dist = 5 + life * (14 + rand(sparkSeed + 3) * 14);
				const x = Math.cos(angle) * dist;
				const y = headY + Math.sin(angle) * dist * 0.8;
				const tail = 3 + rand(sparkSeed + 4) * 4;
				g.moveTo(x, y);
				g.lineTo(x - Math.cos(angle) * tail, y - Math.sin(angle) * tail * 0.8);
				g.stroke({ color: i % 2 === 0 ? CORE : GLASS, width: 1.2, alpha: 0.85 * (1 - life) });
			}
		}
	};

	const drawSeamFlare = (g: import('pixi.js').Graphics, flare: number) => {
		if (flare <= 0.01) return;
		const s = CARD_H;
		const half = s / 2;
		g.roundRect(-7, -half, 14, s, 7);
		g.fill({ color: BLOOD, alpha: 0.4 * flare });
		g.roundRect(-2.4, -half, 4.8, s, 2.4);
		g.fill({ color: CORE, alpha: 0.98 * flare });
		g.ellipse(0, 0, 30 * flare + 6, 2.5);
		g.fill({ color: CORE, alpha: 0.7 * flare });
	};

	const drawDetonation = (
		g: import('pixi.js').Graphics,
		cell: SplitCell,
		d: number,
		split: number,
	) => {
		if (d <= 0 || d >= 1) return;
		const fade = 1 - d;
		g.roundRect(-CARD_W / 2 - 5, -CARD_H / 2 - 5, CARD_W + 10, CARD_H + 10, 13);
		g.fill({ color: CORE, alpha: 0.7 * fade * fade });
		const ringRadius = CARD_H * (0.22 + 0.9 * d);
		g.circle(0, 0, ringRadius * 0.92);
		g.stroke({ color: BLOOD, width: 8 * fade + 1, alpha: 0.4 * fade });
		g.circle(0, 0, ringRadius);
		g.stroke({ color: CORE, width: 3 * fade + 0.5, alpha: 0.8 * fade });
		for (let seamIndex = 0; seamIndex < cell.count - 1; seamIndex++) {
			const seamX = (-CARD_W / 2 + ((seamIndex + 1) / cell.count) * CARD_W) * split;
			for (let k = 0; k < 5; k++) {
				const sparkSeed = cell.seed * 17 + seamIndex * 71 + k * 13;
				const side = rand(sparkSeed) > 0.5 ? 1 : -1;
				const y0 = (rand(sparkSeed + 1) - 0.5) * CARD_H * 0.8;
				const speed = 35 + rand(sparkSeed + 2) * 55;
				const vx = side * speed;
				const vy = (rand(sparkSeed + 3) - 0.5) * 24 + 70 * d;
				const x = seamX + vx * d;
				const y = y0 + vy * d * 0.5;
				const vlen = Math.sqrt(vx * vx + vy * vy) || 1;
				const tail = (6 + rand(sparkSeed + 4) * 8) * fade;
				g.moveTo(x, y);
				g.lineTo(x - (vx / vlen) * tail, y - (vy / vlen) * tail);
				g.stroke({ color: k % 3 === 0 ? CORE : GLASS, width: 1.4, alpha: 0.85 * fade });
			}
		}
	};

</script>

{#snippet splitCell(cell: SplitCell)}
	{@const sliceWidth = CARD_W / cell.count}
	{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	{@const split = splitProgress.current}
	{@const slim = Math.min(1, 3 / cell.count)}
	{@const gap = CARD_W * Math.min(0.025, 0.09 / cell.count)}
	{@const paneWidth = Math.max((sliceWidth - gap) * split + CARD_W * (1 - split), 2)}
	<Container x={cell.cx} y={cell.cy} scale={pulse.current}>
		<Graphics draw={drawUnderGlow} />
		{#if cell.count >= MANY_SPLITS}
			<Container>
				<Rectangle isMask anchor={0.5} width={CARD_W} height={CARD_H} />
				<SymbolSprite {symbolInfo} />
			</Container>
		{:else}
			{#each Array.from({ length: cell.count }) as _, i (i)}
				{@const paneX = (-CARD_W / 2 + (i + 0.5) * sliceWidth) * split}
				<Container x={paneX}>
					<Rectangle isMask anchor={0.5} width={paneWidth} height={CARD_H} />
					<SymbolSprite {symbolInfo} />
				</Container>
			{/each}
		{/if}
		{#each Array.from({ length: cell.count - 1 }) as _, i (i)}
			<Container x={(-CARD_W / 2 + (i + 1) * sliceWidth) * split} alpha={split}>
				<Graphics draw={(g) => drawDivider(g, cell, i, slim)} />
			</Container>
		{/each}
		{@const nDividers = cell.count - 1}
		{#each Array.from({ length: nDividers }) as _, i (i)}
			{@const sweep = Math.min(Math.max(cutSweep.current * (1 + 0.15 * (nDividers - 1)) - 0.15 * i, 0), 1)}
			<Container x={-CARD_W / 2 + (i + 1) * sliceWidth} alpha={1 - split * 0.9}>
				<Graphics draw={(g) => drawCutBlade(g, cell, i, sweep)} />
			</Container>
		{/each}
		{#each Array.from({ length: nDividers }) as _, i (i)}
			<Container x={-CARD_W / 2 + (i + 1) * sliceWidth}>
				<Graphics draw={(g) => drawSeamFlare(g, seamFlare.current)} />
			</Container>
		{/each}
		<Container alpha={split}>
			<Graphics draw={(g) => drawFrame(g, isHigh)} />
		</Container>
		<Container>
			<Graphics draw={(g) => drawDetonation(g, cell, detonation.current, split)} />
		</Container>
	</Container>
{/snippet}

{#snippet badgeMarker(cell: SplitCell)}
	<!-- the split panes speak for themselves; only a BIG split (> 8 ways on a single
		symbol) is hard to read, so it gets a plain "Nx" number. -->
	{#if cell.count > 8}
		<Container x={cell.cx} y={cell.cy} scale={pulse.current}>
			<Text
				anchor={0.5}
				text={`${cell.count}x`}
				style={{
					fontFamily: 'Arial',
					fontWeight: '900',
					fontSize: 34,
					fill: 0xffffff,
					stroke: { color: 0x000000, width: 5 },
				}}
			/>
		</Container>
	{/if}
{/snippet}

{#if show}
	<MainContainer>
		<Container x={stateShake.x} y={stateShake.y}>
			{#each cells as cell (cell.key)}
				{@render splitCell(cell)}
			{/each}
			{#each cells as cell (cell.key)}
				{@render badgeMarker(cell)}
			{/each}
		</Container>
	</MainContainer>
{/if}
