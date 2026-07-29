<script lang="ts">
	/**
	 * Feeds a stored round into the game actor.
	 *
	 * Normal play: an interrupted round is resumed the moment the game is ready.
	 *
	 * Replay (`?replay=true`): the round is NOT started on mount. The replay
	 * panel shows what the round cost and what it paid first, and only starts
	 * the sequence when the player asks for it — and again on "Replay Again",
	 * which is why the round is re-seeded from `stateReplay.round` each time
	 * (the actor consumes `betToResume`).
	 */
	import { onMount } from 'svelte';

	import { stateBet, stateReplay, stateUrlDerived } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();
	const isReplay = stateUrlDerived.replay();

	/** the actor has actually left idle, so returning to idle means "finished" */
	let running = $state(false);

	const start = () => {
		if (stateBet.betToResume?.active && stateBet.betToResume.mode) {
			stateBet.activeBetModeKey = stateBet.betToResume.mode;
		}
		context.eventEmitter.broadcast({ type: 'resumeBet' });
	};

	onMount(() => {
		if (!isReplay) start();
	});

	$effect(() => {
		if (!isReplay || stateReplay.phase !== 'playing' || running) return;
		if (!stateReplay.round) return;

		stateBet.betToResume = { ...stateReplay.round };
		start();
	});

	$effect(() => {
		if (!isReplay || stateReplay.phase !== 'playing') return;

		if (!context.stateXstateDerived.isIdle()) {
			running = true;
		} else if (running) {
			running = false;
			stateReplay.phase = 'ended';
		}
	});
</script>
