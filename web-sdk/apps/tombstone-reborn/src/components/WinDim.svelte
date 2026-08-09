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
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, CELL_PITCH_X } from '../game/constants';
	import { getReelYOffset, getCellLeft, getReelRows } from '../game/utils';
	import { fxNum } from '../game/fx.generated';

	const context = getContext();

	// Cell isolation dim. After the count-up the wins replay ONE SYMBOL TYPE
	// AT A TIME: that type's cells step out of the dim, the glint sweeps them
	// (WinSweep), they drop back under the overlay, the next type shines —
	// looping until the next spin stops the cycle.
	// Tombstone has no LockedSlots / side sockets — dim the reel board only.
	const DIM_ALPHA = fxNum('winDim', 'dimAlpha', 0.86);

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
				// the mirror glint runs across every one of its cards
				await context.eventEmitter.broadcastAsync({ type: 'winSweep', positions });
				if (id !== cycleId) return;
				await wait(220);
				// back under the overlay before the next type shines
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

	const drawDim = (graphics: import('pixi.js').Graphics, keys: Set<string>) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;

		context.stateGame.board.forEach((reel, reelIndex) => {
			// a risen wild column is ONE piece of art covering the whole reel;
			// dimming its "non-winning" cells blacks out half the artwork. The
			// column is always part of every win anyway, so never dim it.
			if (context.stateGame.wildReelReels.includes(reelIndex)) return;
			// a racked (STRETCH) reel spreads its rows over a taller window, so the
			// dim cells must use the spread pitch or they drift off the symbols
			const rowCount = reel.reelState.symbols.length - 2;
			const pitch =
				context.stateGame.reelStretch[reelIndex] != null && rowCount > 0
					? (getReelRows(reelIndex) * SYMBOL_SIZE) / rowCount
					: SYMBOL_SIZE;
			reel.reelState.symbols.forEach((_, rowIndex) => {
				if (rowIndex === 0 || rowIndex === reel.reelState.symbols.length - 1) return;
				if (keys.has(`${reelIndex}-${rowIndex}`)) return;
				// sharp padded-cell mask (hard corners, not soft gothic rounds)
				graphics.rect(
					originX + getCellLeft(reelIndex) + 1,
					originY + pitch * (rowIndex - 1) + 1 + getReelYOffset(reelIndex),
					CELL_PITCH_X - 2,
					pitch - 2,
				);
			});
		});

		graphics.fill({ color: 0x0a0a0c, alpha: 1 });
	};

</script>

<MainContainer>
	{#if active}
		<Container alpha={dimAlpha.current}>
			<Graphics draw={(graphics) => drawDim(graphics, winKeys)} />
		</Container>
	{/if}
</MainContainer>
