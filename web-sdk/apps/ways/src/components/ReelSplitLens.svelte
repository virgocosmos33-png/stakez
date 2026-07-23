<script lang="ts">
	// Reel-layer split LENS.
	//
	// A haunted/split cell is a permanent PROPERTY OF THE POSITION, not of the
	// symbol sitting in it. So while a reel is physically spinning, every symbol
	// scrolling THROUGH a split position must appear split into that position's
	// number of ways. ApparitionOverlay only draws the split once the reel has
	// settled; this lens covers the spinning phase so the split slots are always
	// active - whatever passes through them animates as N ways.
	//
	// How it works: for each slot we render a fixed window at the cell and, per
	// pane, draw the reel's LIVE symbols (at their animating symbolY) centred and
	// masked to a slim vertical strip. Because every pane shows the same centre
	// crop, one scrolling symbol reads as N compressed copies streaming past.
	import { onMount } from 'svelte';
	import { Container, Graphics, Rectangle, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getSymbolY } from '../game/utils';
	import { SYMBOL_SIZE, HIGH_SYMBOLS, BOARD_DIMENSIONS } from '../game/constants';
	import type { RawSymbol } from '../game/types';
	import SymbolSprite from './SymbolSprite.svelte';

	const context = getContext();

	// above this many ways the per-pane copies would be an unreadable stack of
	// stripes, so we show the whole scrolling symbol once with slim seams instead
	const MANY_SPLITS = 5;

	// the lens owns the split slots for the whole spin: from the instant the
	// settled ApparitionOverlay hides (spin start) until it refreshes back on
	// (board fully settled). Gating on this window - rather than each reel's
	// motion - keeps the split HELD even while a reel waits out its stagger
	// delay, so a slot never flashes back to a whole symbol between spins.
	let spinActive = $state(false);
	context.eventEmitter.subscribeOnMount({
		apparitionsHide: () => (spinActive = true),
		apparitionsRefresh: () => (spinActive = false),
		apparitionsPulse: () => (spinActive = false),
	});

	let time = $state(0);
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

	// spine states can't be center-cropped into a sprite pane; fall back to the
	// guaranteed-sprite card state so any symbol streaming past stays croppable
	const spriteInfo = (name: RawSymbol['name'], state: string) => {
		const info = getSymbolInfo({ rawSymbol: { name }, state: state as never });
		if (info.type === 'spine') {
			return getSymbolInfo({ rawSymbol: { name }, state: 'postWinStatic' as never });
		}
		return info;
	};

	const drawUnderGlow = (graphics: import('pixi.js').Graphics) => {
		const s = SYMBOL_SIZE;
		graphics.roundRect(-s / 2 - 2, -s / 2 - 2, s + 4, s + 4, 10);
		graphics.fill({ color: 0x0a0714, alpha: 0.92 });
	};

	const drawPaneBorder = (
		graphics: import('pixi.js').Graphics,
		paneWidth: number,
		isHigh: boolean,
		count: number,
	) => {
		if (count >= MANY_SPLITS) return;
		const s = SYMBOL_SIZE;
		const w = paneWidth;
		if (isHigh) {
			graphics.roundRect(-w / 2, -s / 2, w, s, 6);
			graphics.stroke({ color: 0x120b04, width: 4, alpha: 0.85 });
			graphics.roundRect(-w / 2 + 1, -s / 2 + 1, w - 2, s - 2, 5);
			graphics.stroke({ color: 0xc9a34a, width: 2.5, alpha: 0.95 });
		} else {
			graphics.roundRect(-w / 2, -s / 2, w, s, 6);
			graphics.stroke({ color: 0x0c0a16, width: 3, alpha: 0.8 });
			graphics.roundRect(-w / 2 + 1.5, -s / 2 + 1.5, w - 3, s - 3, 5);
			graphics.stroke({ color: 0xb887ff, width: 1.5, alpha: 0.6 });
		}
	};

	const drawDivider = (
		graphics: import('pixi.js').Graphics,
		seed: number,
		dividerIndex: number,
		timeValue: number,
		slim: number,
	) => {
		const s = SYMBOL_SIZE;
		const half = s / 2;
		const flicker = 0.9 + 0.1 * Math.sin(timeValue * 14 + seed * 3 + dividerIndex * 1.7);
		const glowW = 5 * slim + 1;
		graphics.roundRect(-glowW / 2, -half, glowW, s, 3);
		graphics.fill({ color: 0xb887ff, alpha: 0.16 * flicker * slim });
		const innerW = 2.4 * slim + 0.5;
		graphics.roundRect(-innerW / 2, -half, innerW, s, 1);
		graphics.fill({ color: 0xe6d2ff, alpha: 0.5 * flicker });
		const coreW = 0.7 * slim + 0.3;
		graphics.roundRect(-coreW / 2, -half, coreW, s, 0.4);
		graphics.fill({ color: 0xffffff, alpha: 0.9 * flicker });
	};

	const drawHauntFrame = (
		graphics: import('pixi.js').Graphics,
		persistent: boolean,
		seed: number,
		timeValue: number,
	) => {
		const s = SYMBOL_SIZE;
		const pulse = 0.8 + 0.2 * Math.sin(timeValue * 2.4 + seed);
		graphics.roundRect(-s / 2 - 3, -s / 2 - 3, s + 6, s + 6, 11);
		graphics.stroke({
			color: 0x2bff66,
			width: persistent ? 3 : 1.6,
			alpha: (persistent ? 0.85 : 0.35) * pulse,
		});
		if (persistent) {
			graphics.roundRect(-s / 2 - 7, -s / 2 - 7, s + 14, s + 14, 14);
			graphics.stroke({ color: 0x2bff66, width: 7, alpha: 0.16 * pulse });
		}
	};

	const drawBadge = (graphics: import('pixi.js').Graphics, persistent: boolean) => {
		graphics.circle(0, 0, 21);
		graphics.fill({ color: 0x0a0714, alpha: 0.92 });
		graphics.circle(0, 0, 21);
		graphics.stroke({ color: persistent ? 0x2bff66 : 0x1a7a3c, width: 2, alpha: 0.95 });
	};
</script>

<!-- the live scrolling symbols of one reel, centred at a cell and cropped by the
	caller's mask; only symbols near the cell are drawn (the rest are culled) -->
{#snippet reelContent(reelIndex: number, cellCenterY: number)}
	{#each context.stateGame.board[reelIndex].reelState.symbols as sym (sym.symbolIndexOfBoard)}
		{#if Math.abs(sym.symbolY.current - cellCenterY) < SYMBOL_SIZE}
			<SymbolSprite
				x={0}
				y={sym.symbolY.current - cellCenterY}
				symbolInfo={spriteInfo(sym.rawSymbol.name, sym.symbolState)}
			/>
		{/if}
	{/each}
{/snippet}

{#snippet lensCell(reelIndex: number, row: number, count: number, ttl: number | undefined, name: RawSymbol['name'])}
	{@const cellX = getSymbolX(reelIndex)}
	{@const cellY = getSymbolY(row)}
	{@const seed = reelIndex * 31 + row * 7 + count * 113}
	{@const isHigh = HIGH_SYMBOLS.includes(name)}
	{@const persistent = ttl !== undefined && (ttl === -1 || ttl >= 2)}
	{@const sliceWidth = SYMBOL_SIZE / count}
	{@const slim = Math.min(1, 3 / count)}
	{@const gap = SYMBOL_SIZE * Math.min(0.025, 0.09 / count)}
	{@const paneWidth = Math.max(sliceWidth - gap, 2)}
	<Container x={cellX} y={cellY}>
		<Graphics draw={(graphics) => drawUnderGlow(graphics)} />
		{#if count >= MANY_SPLITS}
			<!-- heavily split: one readable copy of the scrolling symbol + slim seams -->
			<Container>
				<Rectangle isMask anchor={0.5} width={SYMBOL_SIZE} height={SYMBOL_SIZE} />
				{@render reelContent(reelIndex, cellY)}
			</Container>
		{:else}
			{#each Array.from({ length: count }) as _, i (i)}
				{@const paneX = -SYMBOL_SIZE / 2 + (i + 0.5) * sliceWidth}
				<Container x={paneX}>
					<Rectangle isMask anchor={0.5} width={paneWidth} height={SYMBOL_SIZE} />
					{@render reelContent(reelIndex, cellY)}
				</Container>
				<Container x={paneX}>
					<Graphics draw={(graphics) => drawPaneBorder(graphics, paneWidth, isHigh, count)} />
				</Container>
			{/each}
		{/if}
		{#each Array.from({ length: count - 1 }) as _, i (i)}
			<Container x={-SYMBOL_SIZE / 2 + (i + 1) * sliceWidth}>
				<Graphics draw={(graphics) => drawDivider(graphics, seed, i, time, slim)} />
			</Container>
		{/each}
		<Graphics draw={(graphics) => drawHauntFrame(graphics, persistent, seed, time)} />
		<Container x={SYMBOL_SIZE / 2 - 21} y={-SYMBOL_SIZE / 2 + 21}>
			<Graphics draw={(graphics) => drawBadge(graphics, persistent)} />
			<Text
				anchor={0.5}
				text={`X${count}`}
				style={{
					fontFamily: 'Arial',
					fontWeight: '900',
					fontSize: 20,
					fill: 0xffffff,
					stroke: { color: 0x000000, width: 3 },
				}}
			/>
		</Container>
	</Container>
{/snippet}

{#if spinActive}
	{#each context.stateGame.board as reel, reelIndex (reelIndex)}
		{#each reel.reelState.symbols as sym (sym.symbolIndexOfBoard)}
			{@const mult = sym.rawSymbol.multiplier}
			{#if mult !== undefined && mult > 1 && sym.symbolIndexOfBoard >= 0 && sym.symbolIndexOfBoard < BOARD_DIMENSIONS.y}
				{@render lensCell(reelIndex, sym.symbolIndexOfBoard, mult, sym.rawSymbol.ttl, sym.rawSymbol.name)}
			{/if}
		{/each}
	{/each}
{/if}
