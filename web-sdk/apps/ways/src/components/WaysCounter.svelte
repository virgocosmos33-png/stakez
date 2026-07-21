<script lang="ts" module>
	export type EmitterEventWaysCounter =
		| { type: 'waysCounterUpdate'; ways: number }
		| { type: 'waysCounterHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';

	import { getContext } from '../game/context';
	import { getRailLayout } from '../game/plaqueMount';
	import config from '../game/config';
	import RailPlaque from './RailPlaque.svelte';

	const context = getContext();

	// WAYS nameplate: mounted on the LEFT RAIL of the reel frame (stacked ABOVE
	// the matching WIN plaque, balancing Lady Mirror on the right). On narrow
	// layouts (tablet / portrait) the stack sits ABOVE the board crest so plaques
	// never cover symbols. Styling is the shared RailPlaque so WIN matches.
	const rail = $derived(getRailLayout());
	const frameW = $derived(rail.frameW);

	// canonical full-board ways = product of the rows on each reel (this game:
	// 4^5 = 1024). Shown persistently in the base game; the live count from
	// waysCounterUpdate (bookEvent.totalWays) overrides it during splits/bonus.
	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);

	// the plaque is ALWAYS mounted/visible during gameplay (never pops in/out);
	// only the value changes, with a little pop on live updates
	let ways = $state(BASE_WAYS);
	const popScale = new Tween(1);

	const pop = async () => {
		popScale.set(1.22, { duration: 0 });
		await popScale.set(1, { duration: 320, easing: backOut });
	};

	context.eventEmitter.subscribeOnMount({
		waysCounterUpdate: (emitterEvent) => {
			ways = emitterEvent.ways;
			pop();
		},
		// don't hide — revert to the base-board ways so the plaque stays mounted
		waysCounterHide: () => (ways = BASE_WAYS),
	});

	// geometry always comes from plaqueMount (left rail OR crest stack)
	const position = $derived({ x: rail.ways.cx, y: rail.ways.cy });

	// comma renders as a floating high tick in the silver atlas, so group
	// thousands with a plain space instead ("15 360")
	const waysText = $derived(ways.toLocaleString('en-US').replaceAll(',', ' '));
</script>

<RailPlaque
	caption="WAYS"
	value={waysText}
	{frameW}
	x={position.x}
	y={position.y}
	show={true}
	pop={popScale.current}
/>
