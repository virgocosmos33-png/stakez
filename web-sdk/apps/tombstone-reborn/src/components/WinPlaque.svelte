<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { stateBet } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getRailLayout } from '../game/plaqueMount';
	import RailPlaque from './RailPlaque.svelte';

	// Static left-rail WIN nameplate (amethyst, matching WaysCounter). ALWAYS
	// mounted — shows $0.00 when idle, live win amount from stateBet when set.
	// This is SEPARATE from Win.svelte's centered red/horror-font count-up (and
	// the full-screen big-win celebration). Never a gold UiLabel HUD pill.
	const rail = $derived(getRailLayout());
	const frameW = $derived(rail.frameW);

	const amountText = $derived(bookEventAmountToCurrencyString(stateBet.winBookEventAmount));

	const popScale = new Tween(1);
	let lastAmount = stateBet.winBookEventAmount;

	$effect(() => {
		const next = stateBet.winBookEventAmount;
		if (next !== lastAmount) {
			lastAmount = next;
			if (next > 0) {
				popScale.set(1.22, { duration: 0 });
				popScale.set(1, { duration: 320, easing: backOut });
			}
		}
	});

	const position = $derived({ x: rail.win.cx, y: rail.win.cy });
</script>

<RailPlaque
	caption="WIN"
	value={amountText}
	{frameW}
	x={position.x}
	y={position.y}
	show={true}
	pop={popScale.current}
/>
