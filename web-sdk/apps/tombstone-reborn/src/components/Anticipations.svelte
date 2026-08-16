<script lang="ts">
	import { OnMount } from 'components-shared';
	import { SECOND } from 'constants-shared/time';

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
	const hasAnticipation = $derived(context.stateGame.board.some((_, i) => showAnticipation(i)));

	$effect(() => {
		const last = context.stateGame.board[LAST];
		if (last?.reelState.anticipating && !context.stateGame.lidOpen) {
			last.reelState.anticipating = false;
		}
	});
</script>

{#if hasAnticipation}
	<OnMount
		onmount={() => {
			context.eventEmitter.broadcast({ type: 'soundLoop', name: 'sfx_anticipation' });
			context.eventEmitter.broadcast({
				type: 'soundFade',
				name: 'sfx_anticipation',
				from: 0,
				to: 1,
				duration: SECOND,
			});

			return () => {
				context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_anticipation' });
			};
		}}
	/>
{/if}

<BoardSpace>
{#each context.stateGame.board as reel, reelIndex}
	{#if showAnticipation(reelIndex)}
		<Anticipation {reel} {reelIndex} oncomplete={() => (reel.reelState.anticipating = false)} />
	{/if}
{/each}
</BoardSpace>
