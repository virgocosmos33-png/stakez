<script lang="ts">
	import { Container, Rectangle } from 'pixi-svelte';
	import { getContextBoard } from 'components-shared';

	import ReelSymbol from './ReelSymbol.svelte';
	import { getContext } from '../game/context';
	import { getReelPocket, getReelWindow } from '../game/utils';
	import { isNudgeCoveredReel } from '../game/boardCells';

	const context = getContext();
	const boardContext = getContextBoard();
	// The static/spin layer (animate=false) clips EVERY reel to its wood pocket:
	// SymbolWrap only culls once a symbol's CENTER leaves the reel window, and
	// BoardMask spans the whole board box, so 1.6x-tall spin smears on a short
	// reel were streaking over the timber beams. The animate layer stays
	// unmasked so win/land spines can rise; nudge-covered reels keep their
	// pocket clip (the slide must vanish).
	const clipReel = (reel: number) =>
		!boardContext.animate ||
		isNudgeCoveredReel(reel) ||
		(context.stateGame.nudgePush[reel]?.rows.length ?? 0) > 0;
</script>

{#each context.stateGame.board as reel, reelIndex (reelIndex)}
	{#if clipReel(reelIndex)}
		{@const pocket = getReelPocket(reelIndex)}
		{@const window = getReelWindow(reelIndex)}
		<Container>
			<Rectangle
				isMask
				x={pocket.left}
				y={window.top}
				width={pocket.right - pocket.left}
				height={window.bottom - window.top}
				backgroundColor={0xffffff}
			/>
			{#each reel.reelState.symbols as reelSymbol, row}
				<ReelSymbol {reelIndex} {reelSymbol} {row} />
			{/each}
		</Container>
	{:else}
		{#each reel.reelState.symbols as reelSymbol, row}
			<ReelSymbol {reelIndex} {reelSymbol} {row} />
		{/each}
	{/if}
{/each}
