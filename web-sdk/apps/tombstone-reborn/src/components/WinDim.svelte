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
	/**
	 * Cell isolation dim. Lives INSIDE BoardContainer (see Board.svelte) so the
	 * plates share the symbols' x/y/pivot/scale. Drawing these from a sibling
	 * MainContainer via BoardSpace put the rects in the wrong space — they
	 * floated off the cells and painted over the timber.
	 */
	import { Tween } from 'svelte/motion';
	import { Container, Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W } from '../game/constants';
	import { getSymbolX, getCellCenterY, getCardHeight } from '../game/utils';
	import { fxNum } from '../game/fx.generated';

	const context = getContext();

	const DIM_ALPHA = fxNum('winDim', 'dimAlpha', 0.86);
	const DIM_COLOR = 0x0a0a0c;
	const DIM_INSET = 1;

	const dimAlpha = new Tween(0);
	let winKeys = $state<Set<string>>(new Set());
	let active = $state(false);
	let cycleWins: Position[][] = [];
	let cycleId = 0;

	const keysOf = (positions: Position[]) =>
		new Set(positions.map((position) => `${position.reel}-${position.row}`));

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

	const runGlintCycle = async () => {
		const id = ++cycleId;
		if (cycleWins.length === 0) return;
		while (id === cycleId) {
			for (const positions of cycleWins) {
				if (id !== cycleId) return;
				winKeys = keysOf(positions);
				context.stateGame.slotWinPositions = positions;
				await context.eventEmitter.broadcastAsync({ type: 'winSweep', positions });
				if (id !== cycleId) return;
				await wait(220);
				winKeys = new Set();
				context.stateGame.slotWinPositions = [];
				await wait(200);
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
			active = true;
			dimAlpha.set(DIM_ALPHA, { duration: 100 });
			runGlintCycle();
		},
		winCycleStop: () => {
			cycleWins = [];
			hide();
		},
	});

	const dimCells = $derived.by(() => {
		if (!active) return [] as { key: string; x: number; y: number; w: number; h: number }[];
		const keys = winKeys;
		const wild = new Set(context.stateGame.wildReelReels ?? []);
		const out: { key: string; x: number; y: number; w: number; h: number }[] = [];
		context.stateGame.board.forEach((reel, reelIndex) => {
			if (wild.has(reelIndex)) return;
			const cardH = getCardHeight(reelIndex);
			const last = reel.reelState.symbols.length - 1;
			for (let rowIndex = 1; rowIndex < last; rowIndex += 1) {
				if (keys.has(`${reelIndex}-${rowIndex}`)) continue;
				out.push({
					key: `${reelIndex}-${rowIndex}`,
					x: getSymbolX(reelIndex) - SYMBOL_CARD_W * 0.5 + DIM_INSET,
					y: getCellCenterY(reelIndex, rowIndex) - cardH * 0.5 + DIM_INSET,
					w: SYMBOL_CARD_W - DIM_INSET * 2,
					h: cardH - DIM_INSET * 2,
				});
			}
		});
		return out;
	});
</script>

{#if active}
	<Container alpha={dimAlpha.current}>
		{#each dimCells as cell (cell.key)}
			<Rectangle
				x={cell.x}
				y={cell.y}
				width={cell.w}
				height={cell.h}
				backgroundColor={DIM_COLOR}
				backgroundAlpha={1}
			/>
		{/each}
	</Container>
{/if}
