<script lang="ts">
	/**
	 * The six sealed cells that run along the TOP of the board — one over each
	 * reel. Always painted (empty sockets), so the bar reads as part of the
	 * machine. When a specialBar book event lands cards, they drop into their
	 * reel's socket with a short fall + label.
	 */
	import type { Graphics as PixiGraphics } from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, SYMBOL_CARD_W, NUM_ROWS } from '../game/constants';
	import { getSymbolX } from '../game/utils';
	import { stateShake } from '../game/stateShake.svelte';
	import { fxDur } from '../game/fxTiming';

	const context = getContext();

	const REELS = NUM_ROWS.length;
	/** bar cells are shorter than reel cards — a strip, not another reel row */
	const CELL_H = SYMBOL_SIZE * 0.58;
	const CELL_W = SYMBOL_CARD_W;
	const GAP_ABOVE_BOARD = SYMBOL_SIZE * 0.12;
	const RADIUS = 6;

	const KIND_LABEL: Record<string, string> = {
		split_gang: 'GANG',
		split_outlaws: 'OUTLAW',
		gunsmoke: 'SMOKE',
		digup: 'DIG UP',
		coffin: 'OPEN',
	};

	const KIND_TINT: Record<string, number> = {
		split_gang: 0xc9a45c,
		split_outlaws: 0x8a9bb0,
		gunsmoke: 0xb07a4a,
		digup: 0x6e8f5a,
		coffin: 0x9a6b4a,
	};

	type BarCard = { reel: number; kind: string };

	/** keyed by reel so empty sockets stay painted */
	const cardsByReel = $derived.by(() => {
		const map = new Map<number, BarCard>();
		for (const cell of context.stateGame.specialBar) {
			map.set(cell.reel, cell);
		}
		return map;
	});

	/** drop offset: 0 = seated, negative = above the socket (pre-drop) */
	const dropY = new Tween(0);

	$effect(() => {
		const cards = context.stateGame.specialBar;
		// park above, then drop in whenever a new non-empty bar lands
		if (cards.length === 0) {
			dropY.set(0, { duration: 0 });
			return;
		}
		// touch revealNonce so a fresh spin with the same card set still re-drops
		void context.stateGame.revealNonce;
		dropY.set(-CELL_H * 1.4, { duration: 0 });
		dropY.set(0, { duration: fxDur(420), easing: backOut });
	});

	const layout = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const originX = board.x - board.width * 0.5 + stateShake.x;
		const boardTop = board.y - board.height * 0.5 + stateShake.y;
		const barBottom = boardTop - GAP_ABOVE_BOARD;
		const barTop = barBottom - CELL_H;
		const barCy = (barTop + barBottom) * 0.5;
		const cells = Array.from({ length: REELS }, (_, reel) => ({
			reel,
			cx: originX + getSymbolX(reel),
			cy: barCy,
		}));
		// rail that ties the six sockets into one bar
		const left = cells[0].cx - CELL_W * 0.5 - 10;
		const right = cells[REELS - 1].cx + CELL_W * 0.5 + 10;
		return {
			cells,
			rail: {
				x: left,
				y: barTop - 8,
				w: right - left,
				h: CELL_H + 16,
			},
		};
	});

	const drawRail = (g: PixiGraphics) => {
		const { x, y, w, h } = layout.rail;
		g.clear();
		// cast shadow
		g.roundRect(x + 3, y + 5, w, h, 10);
		g.fill({ color: 0x000000, alpha: 0.35 });
		// iron face
		g.roundRect(x, y, w, h, 10);
		g.fill({ color: 0x1c1e22, alpha: 0.96 });
		g.roundRect(x, y, w, h, 10);
		g.stroke({ color: 0x3a3f48, width: 1.5, alpha: 0.8 });
		// amber hairline along the top edge
		g.moveTo(x + 12, y + 1);
		g.lineTo(x + w - 12, y + 1);
		g.stroke({ color: 0xc9a45c, width: 1, alpha: 0.35 });
	};

	const drawSocket = (g: PixiGraphics, filled: boolean, tint: number) => {
		const w = CELL_W;
		const h = CELL_H;
		const x = -w * 0.5;
		const y = -h * 0.5;
		g.clear();
		// recessed well
		g.roundRect(x, y, w, h, RADIUS);
		g.fill({ color: 0x0a0b0d, alpha: 0.95 });
		g.roundRect(x, y, w, h, RADIUS);
		g.stroke({ color: 0x000000, width: 2, alpha: 0.55 });

		if (filled) {
			// card face
			g.roundRect(x + 3, y + 3, w - 6, h - 6, RADIUS - 2);
			g.fill({ color: 0x2a241c, alpha: 0.98 });
			g.roundRect(x + 3, y + 3, w - 6, h - 6, RADIUS - 2);
			g.stroke({ color: tint, width: 2, alpha: 0.85 });
			// small accent bar under the label
			g.roundRect(x + w * 0.2, y + h * 0.68, w * 0.6, 2, 1);
			g.fill({ color: tint, alpha: 0.7 });
		} else {
			// sealed — faint bars so empty cells still read as locked graves
			const inset = 7;
			for (let i = 0; i < 3; i++) {
				const bx = x + inset + ((w - inset * 2) * (i + 0.5)) / 3;
				g.moveTo(bx, y + inset);
				g.lineTo(bx, y + h - inset);
				g.stroke({ color: 0x4a4550, width: 1.5, alpha: 0.45 });
			}
			g.roundRect(x + 2, y + 2, w - 4, h - 4, RADIUS - 1);
			g.stroke({ color: 0x3a3f48, width: 1, alpha: 0.5 });
		}
	};
</script>

<MainContainer>
	<!-- iron rail behind the six sockets -->
	<Graphics draw={drawRail} />

	{#each layout.cells as cell (cell.reel)}
		{@const card = cardsByReel.get(cell.reel)}
		{@const tint = card ? (KIND_TINT[card.kind] ?? 0xc9a45c) : 0x3a3f48}
		{@const label = card ? (KIND_LABEL[card.kind] ?? card.kind) : ''}
		<Container x={cell.cx} y={cell.cy + (card ? dropY.current : 0)}>
			<Graphics draw={(g) => drawSocket(g, !!card, tint)} />
			{#if card}
				<Text
					anchor={0.5}
					y={-2}
					text={label}
					eventMode="none"
					style={{
						fontFamily: '"Segoe UI Semibold", "Segoe UI", Arial, sans-serif',
						fontSize: Math.max(11, Math.round(CELL_H * 0.28)),
						fontWeight: '600',
						fill: tint,
						align: 'center',
						letterSpacing: 0.5,
					}}
				/>
			{/if}
		</Container>
	{/each}
</MainContainer>
