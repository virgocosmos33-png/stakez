<script lang="ts" module>
	import type { Position } from '../game/types';

	export type EmitterEventWinSweep = {
		type: 'winSweep';
		positions: Position[];
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { linear } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	// green plasma surge that sweeps left-to-right across the connecting
	// symbols of a win, selling the LINK as the liner ignites behind it
	type SweepCell = { key: string; reel: number; cx: number; cy: number };

	const REEL_STAGGER = 0.22; // sweep offset per reel, in normalized progress units

	let sweepCells = $state<SweepCell[]>([]);
	let minReel = $state(0);
	let span = $state(0);
	const progress = new Tween(0);

	context.eventEmitter.subscribeOnMount({
		winSweep: async ({ positions }) => {
			const boardLayout = context.stateGameDerived.boardLayout();
			const originX = boardLayout.x - boardLayout.width * 0.5;
			const originY = boardLayout.y - boardLayout.height * 0.5;

			sweepCells = positions.map((position) => ({
				key: `${position.reel}-${position.row}`,
				reel: position.reel,
				// book event rows are padded: visible row = row - 1
				cx: originX + SYMBOL_SIZE * (position.reel + 0.5),
				cy: originY + SYMBOL_SIZE * (position.row - 0.5),
			}));
			const reels = sweepCells.map((cell) => cell.reel);
			minReel = Math.min(...reels);
			span = Math.max(...reels) - minReel;

			progress.set(0, { duration: 0 });
			await progress.set(1, { duration: 550 + span * 130, easing: linear });
			sweepCells = [];
		},
	});

	// per-cell flash: rises and falls as the sweep front passes its reel
	const alphaFor = (reel: number) => {
		const total = span * REEL_STAGGER + 1;
		const local = progress.current * total - (reel - minReel) * REEL_STAGGER;
		if (local <= 0 || local >= 1) return 0;
		return Math.sin(Math.PI * local);
	};

	const drawWinGlow = (graphics: import('pixi.js').Graphics, alpha: number) => {
		if (alpha <= 0) return;
		const s = SYMBOL_SIZE;
		// spectral green wash over the symbol (the surge that ignites the liner)
		graphics.roundRect(-s / 2 + 2, -s / 2 + 2, s - 4, s - 4, 9);
		graphics.fill({ color: 0xead9ff, alpha: 0.2 * alpha });
		// wide plasma halo
		graphics.roundRect(-s / 2 - 3, -s / 2 - 3, s + 6, s + 6, 12);
		graphics.stroke({ color: 0xb887ff, width: 9, alpha: 0.5 * alpha });
		// hot white-green edge
		graphics.roundRect(-s / 2 + 1, -s / 2 + 1, s - 2, s - 2, 9);
		graphics.stroke({ color: 0xf3ecff, width: 3, alpha: 0.95 * alpha });
	};
</script>

<MainContainer>
	{#each sweepCells as cell (cell.key)}
		<Container x={cell.cx} y={cell.cy}>
			<Graphics draw={(graphics) => drawWinGlow(graphics, alphaFor(cell.reel))} />
		</Container>
	{/each}
</MainContainer>
