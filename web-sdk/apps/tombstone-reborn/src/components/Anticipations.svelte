<script lang="ts">
	import { getContext } from '../game/context';
	import Anticipation from './Anticipation.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();
	const LAST = context.stateGame.board.length - 1;
	const showAnticipation = (reelIndex: number) => {
		const reel = context.stateGame.board[reelIndex];
		if (!reel?.reelState.anticipating) return false;
		// The boarded lane is already a dark cover. A second shaft on top of it
		// was the stacked wash on the 3rd-scatter hang.
		if (reelIndex === LAST && !context.stateGame.lidOpen) return false;
		return true;
	};

	$effect(() => {
		const last = context.stateGame.board[LAST];
		if (last?.reelState.anticipating && !context.stateGame.lidOpen) {
			last.reelState.anticipating = false;
		}
	});
</script>

<BoardSpace>
{#each context.stateGame.board as reel, reelIndex}
	{#if showAnticipation(reelIndex)}
		<Anticipation {reel} {reelIndex} oncomplete={() => (reel.reelState.anticipating = false)} />
	{/if}
{/each}
</BoardSpace>
