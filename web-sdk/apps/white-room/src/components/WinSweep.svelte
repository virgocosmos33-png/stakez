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
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { fxNum } from '../game/fx.generated';
	import { drawMemoryGlitchCell } from '../game/clinicalFx';

	const context = getContext();

	// THE WHITE ROOM: memory-glitch wipe — CRT tears across winning cells.
	// NOT Madam Mirror green/violet plasma wash.
	type SweepCell = { key: string; reel: number; cx: number; cy: number; seed: number };

	const REEL_STAGGER = fxNum('winSweep', 'reelStagger', 0.14);
	const SWEEP_BASE_MS = fxNum('winSweep', 'baseMs', 380);
	const SWEEP_PER_REEL_MS = fxNum('winSweep', 'perReelMs', 90);

	let sweepCells = $state<SweepCell[]>([]);
	let minReel = $state(0);
	let span = $state(0);
	let time = $state(0);
	const progress = new Tween(0);

	context.eventEmitter.subscribeOnMount({
		winSweep: async ({ positions }) => {
			const boardLayout = context.stateGameDerived.boardLayout();
			const originX = boardLayout.x - boardLayout.width * 0.5;
			const originY = boardLayout.y - boardLayout.height * 0.5;

			sweepCells = positions.map((position, index) => ({
				key: `${position.reel}-${position.row}`,
				reel: position.reel,
				cx: originX + getSymbolX(position.reel),
				cy: originY + getCellCenterY(position.reel, position.row),
				seed: index * 17 + position.reel * 3,
			}));
			const reels = sweepCells.map((cell) => cell.reel);
			minReel = Math.min(...reels);
			span = Math.max(...reels) - minReel;

			const start = performance.now();
			const duration = SWEEP_BASE_MS + span * SWEEP_PER_REEL_MS;
			progress.set(0, { duration: 0 });
			const anim = progress.set(1, { duration, easing: linear });
			let raf = 0;
			const tick = (now: number) => {
				time = (now - start) / 1000;
				raf = requestAnimationFrame(tick);
			};
			raf = requestAnimationFrame(tick);
			await anim;
			cancelAnimationFrame(raf);
			sweepCells = [];
		},
	});

	const alphaFor = (reel: number) => {
		const total = span * REEL_STAGGER + 1;
		const local = progress.current * total - (reel - minReel) * REEL_STAGGER;
		if (local <= 0 || local >= 1) return 0;
		// hard clinical pulse (not soft sine plasma)
		const spike = local < 0.35 ? local / 0.35 : 1 - (local - 0.35) / 0.65;
		return Math.pow(Math.max(spike, 0), 0.7);
	};
</script>

<MainContainer>
	{#each sweepCells as cell (cell.key)}
		<Container x={cell.cx} y={cell.cy}>
			<Graphics
				draw={(graphics) =>
					drawMemoryGlitchCell(graphics, SYMBOL_SIZE, alphaFor(cell.reel), time, cell.seed)}
			/>
		</Container>
	{/each}
</MainContainer>
