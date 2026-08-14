<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, quadOut } from 'svelte/easing';
	import { Sprite } from 'pixi-svelte';

	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_SIZE } from '../game/constants';
	import type { SymbolState } from '../game/types';

	type Props = {
		x?: number;
		y?: number;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		state?: SymbolState;
		oncomplete?: () => void;
	};

	const props: Props = $props();
	const pulse = new Tween(1);

	// Sprite-only symbols (WILD / SCATTER / special-cell cards) animate via scale.
	// The paying H/L cards run their spine rigs now, so this pulse is the WILD /
	// scatter beat. The win emphasis is a clean upward POP (overshoot above 1 then
	// settle) — reads as a celebratory jump, not the old shrink-dip. The overshoot
	// is kept modest so it stays within the cell gutter + the timber frame gap.
	const animate = async (state?: SymbolState) => {
		if (state === 'win') {
			await pulse.set(1.12, { duration: 150, easing: backOut });
			await pulse.set(1, { duration: 220, easing: quadOut });
			await pulse.set(1.06, { duration: 120, easing: backOut });
			await pulse.set(1, { duration: 200, easing: quadOut });
			props.oncomplete?.();
		} else if (state === 'land') {
			pulse.set(0.92, { duration: 0 });
			await pulse.set(1.06, { duration: 130, easing: backOut });
			await pulse.set(1, { duration: 170, easing: quadOut });
			props.oncomplete?.();
		} else {
			pulse.set(1, { duration: 0 });
			props.oncomplete?.();
		}
	};

	$effect(() => {
		props.symbolInfo;
		animate(props.state);
	});
</script>

<Sprite
	x={props.x}
	y={props.y}
	anchor={0.5}
	key={props.symbolInfo.assetKey}
	width={SYMBOL_SIZE * props.symbolInfo.sizeRatios.width * pulse.current}
	height={SYMBOL_SIZE * props.symbolInfo.sizeRatios.height * pulse.current}
/>
