<script lang="ts" module>
	export type EmitterEventTransition = { type: 'transition' };
</script>

<script lang="ts">
	import { waitForResolve } from 'utils-shared/wait';
	import { OnPressFullScreen } from 'components-layout';

	import TransitionAnimation from './TransitionAnimation.svelte';
	import { getContext } from '../game/context';

	const context = getContext();

	let transitioning = $state(false);
	let oncomplete = $state(() => {});
	let finished = false;

	const finish = () => {
		if (!transitioning || finished) return;
		finished = true;
		oncomplete();
		transitioning = false;
	};

	const broadcastSkip = () => {
		if (!transitioning) return;
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	context.eventEmitter.subscribeOnMount({
		transition: async () => {
			finished = false;
			// freeSpinTrigger/freeSpinEnd await this. If the shower spine failed to
			// load (missing assets/spines/transition), never mount a broken spine —
			// resolve immediately so Action / playBet cannot hang forever.
			if (!context.stateApp.loadedAssets?.transition) {
				console.error(
					'[Transition] spine "transition" missing from loadedAssets — skipping shower',
				);
				return;
			}
			transitioning = true;
			// Safety net: even a broken complete listener must not wedge the book.
			const safety = window.setTimeout(() => {
				console.warn('[Transition] shower did not complete in time — forcing resolve');
				finish();
			}, 8000);
			try {
				await waitForResolve((resolve) => (oncomplete = resolve));
			} finally {
				window.clearTimeout(safety);
			}
		},
		// Same bus as TapToSkip — tap/Space/stop skips the shower
		stopButtonClick: () => finish(),
	});
</script>

{#if transitioning}
	<TransitionAnimation oncomplete={finish} />
	<OnPressFullScreen onpress={broadcastSkip} />
{/if}
