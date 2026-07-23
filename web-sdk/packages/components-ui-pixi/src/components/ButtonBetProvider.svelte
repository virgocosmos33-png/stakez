<script lang="ts" module>
	export type ButtonBetKey = 'spin_default' | 'spin_disabled' | 'stop_default' | 'stop_disabled';
</script>

<script lang="ts">
	import type { Snippet } from 'svelte';

	import { stateBet, stateBetDerived } from 'state-shared';

	import { getContext } from '../context';

	type Props = {
		children: Snippet<
			[
				{
					key: ButtonBetKey;
					onpress: () => void;
				},
			]
		>;
	};

	const props: Props = $props();
	const context = getContext();

	let stopDisabled = $state(false);

	// every fresh round starts with the stop control re-armed, even if the
	// previous round ended while a press had it disabled
	$effect(() => {
		if (context.stateXstateDerived.isIdle()) stopDisabled = false;
	});

	// spam guard: one action per window, so a double/triple-click can't fire
	// BET and then instantly slam-stop the very spin it just started
	const PRESS_DEBOUNCE_MS = 250;
	let lastPressAt = 0;

	const bet = () => {
		if (stateBetDerived.activeBetMode()?.type === 'buy') stateBet.activeBetModeKey = 'BASE';
		context.eventEmitter.broadcast({ type: 'bet' });
	};

	const stop = () => {
		// already stopping - rebroadcasting only spams every skip subscriber
		if (stopDisabled) return;
		stateBetDerived.updateIsTurbo(true, { persistent: false });
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	const onpress = () => {
		// cancelling continuous play must NEVER be swallowed by the spam guard
		// or the in-flight skip guard below - this button is the way out of a
		// long autobet run OR a stuck space-hold loop, so both are cleared
		// before any early return
		if (!context.stateXstateDerived.isIdle()) {
			if (stateBetDerived.hasAutoBetCounter()) stateBet.autoSpinsCounter = 0;
			if (stateBet.isSpaceHold) {
				stateBet.isSpaceHold = false;
				stateBetDerived.updateIsTurbo(false, { persistent: true });
			}
		}

		const now = performance.now();
		if (now - lastPressAt < PRESS_DEBOUNCE_MS) return;
		lastPressAt = now;

		context.eventEmitter.broadcast({ type: 'soundPressBet' });

		if (context.stateXstateDerived.isIdle()) {
			bet();
		} else {
			stop();
		}
	};

	const getKey = () => {
		if (context.stateXstateDerived.isIdle()) {
			if (!stateBetDerived.isBetCostAvailable()) return 'spin_disabled';
			return 'spin_default';
		}

		if (!context.stateXstateDerived.isIdle()) {
			if (stopDisabled) return 'stop_disabled';
			if (stateBetDerived.hasAutoBetCounter()) return 'stop_default';
			if (stateBet.isTurbo) return 'stop_disabled';
			return 'stop_default';
		}

		return 'spin_default';
	};

	const key = $derived.by(getKey);

	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => (stopDisabled = true),
		stopButtonEnable: () => (stopDisabled = false),
	});
</script>

{@render props.children({ key, onpress })}
