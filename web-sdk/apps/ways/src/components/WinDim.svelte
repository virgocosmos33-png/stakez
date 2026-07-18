<script lang="ts" module>
	export type EmitterEventWinDim =
		| { type: 'winDimShow'; positions: Position[] }
		| { type: 'winDimHide' }
		| { type: 'winCycleSet'; wins: Position[][] }
		| { type: 'winCycleStart' }
		| { type: 'winCycleStop' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { linear } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import type { Position } from '../game/types';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	// how dark the overlay over every non-winning cell is (winners stay bright)
	const DIM_ALPHA = 0.78;

	// darkens every non-winning cell so the winning symbols pop
	const dimAlpha = new Tween(0);
	let winKeys = $state<Set<string>>(new Set());
	let active = $state(false);

	// the winning combinations of the current spin (union stays lit while resting)
	let cycleWins: Position[][] = [];

	// ending flash: a diagonal glass-reflection glint sweeps left->right across
	// each winning way (masked to the winning cells), cycling way by way, until
	// the next spin clears it
	const sweep = new Tween(0);
	let flashKeys = $state<Set<string>>(new Set());
	let cycleId = 0;

	const keysOf = (positions: Position[]) =>
		new Set(positions.map((position) => `${position.reel}-${position.row}`));

	const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

	const stopCycle = () => {
		cycleId += 1;
		flashKeys = new Set();
		sweep.set(0, { duration: 0 });
	};

	const hide = async () => {
		stopCycle();
		await dimAlpha.set(0, { duration: 180 });
		active = false;
		winKeys = new Set();
	};

	// sweep a glass glint from the left edge to the right edge of one whole
	// winning way, then the next; loop
	const runFlashCycle = async () => {
		const id = ++cycleId;
		if (cycleWins.length === 0) return;
		while (id === cycleId) {
			for (const positions of cycleWins) {
				if (id !== cycleId) return;
				flashKeys = keysOf(positions);
				sweep.set(0, { duration: 0 });
				await sweep.set(1, { duration: 600, easing: linear });
				if (id !== cycleId) return;
				flashKeys = new Set();
				await wait(150);
			}
		}
	};

	context.eventEmitter.subscribeOnMount({
		winDimShow: ({ positions }) => {
			stopCycle();
			winKeys = keysOf(positions);
			active = true;
			dimAlpha.set(DIM_ALPHA, { duration: 130 });
		},
		winDimHide: hide,
		winCycleSet: ({ wins }) => {
			cycleWins = wins;
		},
		// after the win presentation: keep EVERY winning cell lit and hold the
		// dark overlay over all the others (no morph), then flash each winning
		// way as a whole, one way at a time, until the next spin clears it
		winCycleStart: () => {
			if (cycleWins.length === 0) return;
			winKeys = keysOf(cycleWins.flat());
			active = true;
			dimAlpha.set(DIM_ALPHA, { duration: 130 });
			runFlashCycle();
		},
		winCycleStop: () => {
			cycleWins = [];
			hide();
		},
	});

	const drawDim = (graphics: import('pixi.js').Graphics, keys: Set<string>) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;

		context.stateGame.board.forEach((reel, reelIndex) => {
			reel.reelState.symbols.forEach((_, rowIndex) => {
				// skip the padding rows above/below the visible board
				if (rowIndex === 0 || rowIndex === reel.reelState.symbols.length - 1) return;
				if (keys.has(`${reelIndex}-${rowIndex}`)) return;
				graphics.roundRect(
					originX + SYMBOL_SIZE * reelIndex + 1,
					originY + SYMBOL_SIZE * (rowIndex - 1) + 1,
					SYMBOL_SIZE - 2,
					SYMBOL_SIZE - 2,
					8,
				);
			});
		});
		graphics.fill({ color: 0x000000, alpha: 1 });
	};

	const cellsOf = (keys: Set<string>) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		return [...keys].map((key) => {
			const [reelIndex, rowIndex] = key.split('-').map(Number);
			return {
				x: originX + SYMBOL_SIZE * reelIndex,
				y: originY + SYMBOL_SIZE * (rowIndex - 1),
			};
		});
	};

	// mask: the winning cells - the glass glint is clipped to exactly these
	const drawFlashMask = (graphics: import('pixi.js').Graphics, keys: Set<string>) => {
		if (keys.size === 0) return;
		cellsOf(keys).forEach((cell) => {
			graphics.roundRect(cell.x, cell.y, SYMBOL_SIZE, SYMBOL_SIZE, 8);
		});
		graphics.fill({ color: 0xffffff, alpha: 1 });
	};

	// a diagonal glass-reflection glint: a soft violet halo, a broad frosted
	// band, a hot specular core and a thin trailing highlight - the classic
	// double streak of light sliding across polished glass
	const drawGlassStreak = (
		graphics: import('pixi.js').Graphics,
		keys: Set<string>,
		progress: number,
	) => {
		if (keys.size === 0) return;
		const cells = cellsOf(keys);
		const minX = Math.min(...cells.map((cell) => cell.x));
		const maxX = Math.max(...cells.map((cell) => cell.x)) + SYMBOL_SIZE;
		const yTop = Math.min(...cells.map((cell) => cell.y)) - 2;
		const yBot = Math.max(...cells.map((cell) => cell.y)) + SYMBOL_SIZE + 2;

		const slant = (yBot - yTop) * 0.34;
		const margin = SYMBOL_SIZE * 0.9;
		const center = minX - margin + (maxX + margin - (minX - margin)) * progress;

		// a slanted parallelogram band centered at (center + offset)
		const band = (half: number, color: number, alpha: number, offset = 0) => {
			const c = center + offset;
			graphics.poly([
				c - half - slant / 2,
				yTop,
				c + half - slant / 2,
				yTop,
				c + half + slant / 2,
				yBot,
				c - half + slant / 2,
				yBot,
			]);
			graphics.fill({ color, alpha });
		};

		band(SYMBOL_SIZE * 0.36, 0xb887ff, 0.16); // violet halo
		band(SYMBOL_SIZE * 0.2, 0xe6d2ff, 0.3); // frosted spread
		band(SYMBOL_SIZE * 0.07, 0xffffff, 0.95); // hot specular core
		band(SYMBOL_SIZE * 0.035, 0xffffff, 0.7, SYMBOL_SIZE * 0.24); // trailing streak
	};
</script>

<MainContainer>
	{#if active}
		<Container alpha={dimAlpha.current}>
			<Graphics draw={(graphics) => drawDim(graphics, winKeys)} />
		</Container>
		{#if flashKeys.size > 0}
			<Container>
				<Graphics isMask draw={(graphics) => drawFlashMask(graphics, flashKeys)} />
				<Graphics draw={(graphics) => drawGlassStreak(graphics, flashKeys, sweep.current)} />
			</Container>
		{/if}
	{/if}
</MainContainer>
