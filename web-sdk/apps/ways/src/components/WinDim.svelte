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
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import type { Position } from '../game/types';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	// darkens every non-winning cell so the winning combination pops
	const dimAlpha = new Tween(0);
	let winKeys = $state<Set<string>>(new Set());
	let active = $state(false);

	// idle cycle: after the win presentation the winning ways keep flashing,
	// one combination at a time, until the next spin cancels it
	let cycleWins: Position[][] = [];
	let cycleId = 0;

	const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

	const stopCycle = () => {
		cycleId += 1;
	};

	const hide = async () => {
		stopCycle();
		await dimAlpha.set(0, { duration: 180 });
		active = false;
		winKeys = new Set();
	};

	const runCycle = async () => {
		const id = ++cycleId;
		if (cycleWins.length === 0) return;
		while (id === cycleId) {
			for (const positions of cycleWins) {
				if (id !== cycleId) return;
				winKeys = new Set(positions.map((position) => `${position.reel}-${position.row}`));
				active = true;
				dimAlpha.set(0.62, { duration: 130 });
				context.eventEmitter.broadcast({ type: 'apparitionsWinGrow', positions });
				await context.eventEmitter.broadcastAsync({
					type: 'boardWithAnimateSymbols',
					symbolPositions: positions,
				});
				if (id !== cycleId) return;
				context.eventEmitter.broadcast({ type: 'apparitionsWinRelease' });
				await wait(280);
			}
		}
	};

	context.eventEmitter.subscribeOnMount({
		winDimShow: ({ positions }) => {
			stopCycle();
			winKeys = new Set(positions.map((position) => `${position.reel}-${position.row}`));
			active = true;
			dimAlpha.set(0.62, { duration: 130 });
		},
		winDimHide: hide,
		winCycleSet: ({ wins }) => {
			cycleWins = wins;
		},
		winCycleStart: () => {
			runCycle();
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
</script>

<MainContainer>
	{#if active}
		<Container alpha={dimAlpha.current}>
			<Graphics draw={(graphics) => drawDim(graphics, winKeys)} />
		</Container>
	{/if}
</MainContainer>
