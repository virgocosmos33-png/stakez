<script lang="ts" module>
	import type { Position } from '../game/types';

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

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { getReelYOffset } from '../game/utils';
	import { fxNum } from '../game/fx.generated';

	const context = getContext();

	// THE WHITE ROOM: cell isolation dim + fluorescent observation SCAN
	// (horizontal lamp sweep). NOT Madam Mirror diagonal glass-reflection glint.
	const DIM_ALPHA = fxNum('winDim', 'dimAlpha', 0.86);

	const dimAlpha = new Tween(0);
	let winKeys = $state<Set<string>>(new Set());
	let active = $state(false);
	let cycleWins: Position[][] = [];
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

	const runFlashCycle = async () => {
		const id = ++cycleId;
		if (cycleWins.length === 0) return;
		while (id === cycleId) {
			for (const positions of cycleWins) {
				if (id !== cycleId) return;
				flashKeys = keysOf(positions);
				sweep.set(0, { duration: 0 });
				await sweep.set(1, { duration: 420, easing: linear });
				if (id !== cycleId) return;
				flashKeys = new Set();
				await wait(120);
			}
		}
	};

	context.eventEmitter.subscribeOnMount({
		winDimShow: ({ positions }) => {
			stopCycle();
			winKeys = keysOf(positions);
			active = true;
			dimAlpha.set(DIM_ALPHA, { duration: 100 });
		},
		winDimHide: hide,
		winCycleSet: ({ wins }) => {
			cycleWins = wins;
		},
		winCycleStart: () => {
			if (cycleWins.length === 0) return;
			winKeys = keysOf(cycleWins.flat());
			active = true;
			dimAlpha.set(DIM_ALPHA, { duration: 100 });
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
				if (rowIndex === 0 || rowIndex === reel.reelState.symbols.length - 1) return;
				if (keys.has(`${reelIndex}-${rowIndex}`)) return;
				// sharp padded-cell mask (hard corners, not soft gothic rounds)
				graphics.rect(
					originX + SYMBOL_SIZE * reelIndex + 1,
					originY + SYMBOL_SIZE * (rowIndex - 1) + 1 + getReelYOffset(reelIndex),
					SYMBOL_SIZE - 2,
					SYMBOL_SIZE - 2,
				);
			});
		});
		graphics.fill({ color: 0x0a0a0c, alpha: 1 });
	};

	const cellsOf = (keys: Set<string>) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		return [...keys].map((key) => {
			const [reelIndex, rowIndex] = key.split('-').map(Number);
			return {
				x: originX + SYMBOL_SIZE * reelIndex,
				y: originY + SYMBOL_SIZE * (rowIndex - 1) + getReelYOffset(reelIndex),
			};
		});
	};

	const drawFlashMask = (graphics: import('pixi.js').Graphics, keys: Set<string>) => {
		if (keys.size === 0) return;
		cellsOf(keys).forEach((cell) => {
			graphics.rect(cell.x, cell.y, SYMBOL_SIZE, SYMBOL_SIZE);
		});
		graphics.fill({ color: 0xffffff, alpha: 1 });
	};

	/** Horizontal fluorescent observation lamp — scans top→bottom across winners. */
	const drawObservationScan = (
		graphics: import('pixi.js').Graphics,
		keys: Set<string>,
		progress: number,
	) => {
		if (keys.size === 0) return;
		const cells = cellsOf(keys);
		const minX = Math.min(...cells.map((cell) => cell.x));
		const maxX = Math.max(...cells.map((cell) => cell.x)) + SYMBOL_SIZE;
		const yTop = Math.min(...cells.map((cell) => cell.y));
		const yBot = Math.max(...cells.map((cell) => cell.y)) + SYMBOL_SIZE;
		const bandY = yTop + (yBot - yTop) * progress;
		const bandH = SYMBOL_SIZE * 0.22;

		// soft lamp body
		graphics.rect(minX - 2, bandY - bandH, maxX - minX + 4, bandH * 2);
		graphics.fill({ color: 0xf4f1ec, alpha: 0.18 });
		// hot filament core
		graphics.rect(minX, bandY - bandH * 0.35, maxX - minX, bandH * 0.7);
		graphics.fill({ color: 0xffffff, alpha: 0.55 });
		// trailing CRT afterimage lines
		for (let i = 1; i <= 3; i++) {
			const y = bandY - bandH - i * 5;
			graphics.rect(minX, y, maxX - minX, 1.5);
			graphics.fill({ color: 0xc8c4bc, alpha: 0.2 / i });
		}
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
				<Graphics draw={(graphics) => drawObservationScan(graphics, flashKeys, sweep.current)} />
			</Container>
		{/if}
	{/if}
</MainContainer>
