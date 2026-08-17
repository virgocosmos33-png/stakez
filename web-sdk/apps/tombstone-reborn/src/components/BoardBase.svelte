<script lang="ts">
	import { Container, Rectangle } from 'pixi-svelte';

	import ReelSymbol from './ReelSymbol.svelte';
	import { getContext } from '../game/context';
	import { getReelPocket } from '../game/utils';
	import { isNudgeCoveredReel } from '../game/boardCells';

	const context = getContext();
	const clipReel = (reel: number) =>
		isNudgeCoveredReel(reel) || (context.stateGame.nudgePush[reel]?.rows.length ?? 0) > 0;
</script>

{#each context.stateGame.board as reel, reelIndex (reelIndex)}
	{#if clipReel(reelIndex)}
		{@const pocket = getReelPocket(reelIndex)}
		<Container>
			<Rectangle
				isMask
				x={pocket.left}
				y={pocket.top}
				width={pocket.right - pocket.left}
				height={pocket.bottom - pocket.top}
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
