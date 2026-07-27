<script lang="ts" module>
	export type EmitterEventFreeSpinCounter =
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	import { getContext } from '../game/context';
	import { getRailLayout } from '../game/plaqueMount';
	import RailPlaque from './RailPlaque.svelte';

	const context = getContext();

	// Same RailPlaque as WAYS + WIN — top slot of the connected column attached
	// to the frame (geometry from plaqueMount; never self-offset above the stack).
	const rail = $derived(getRailLayout());

	let show = $state(false);
	let current = $state(0);
	let total = $state(0);

	context.eventEmitter.subscribeOnMount({
		freeSpinCounterShow: () => (show = true),
		freeSpinCounterHide: () => (show = false),
		freeSpinCounterUpdate: (emitterEvent) => {
			if (emitterEvent.current !== undefined) current = emitterEvent.current;
			if (emitterEvent.total !== undefined) total = emitterEvent.total;
		},
	});

	const tally = $derived(`${total - current} / ${total}`);
</script>

<RailPlaque
	caption="SPINS"
	value={tally}
	frameW={rail.frameW}
	x={rail.spins.cx}
	y={rail.spins.cy}
	{show}
/>
