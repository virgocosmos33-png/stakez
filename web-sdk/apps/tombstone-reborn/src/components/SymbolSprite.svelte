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

	// Card symbols animate via scale reactions since all states are static
	// sprites. CRITICAL: scale NEVER exceeds 1.0 — a symbol growing past 1.0
	// bulges out of its cell frame, which looks broken/unprofessional. So the
	// win/land emphasis is a PRESS-IN (dip below 1 and recover), which reads as
	// a punchy thump while always staying inside the cell frame.
	const animate = async (state?: SymbolState) => {
		if (state === 'win') {
			await pulse.set(0.84, { duration: 150, easing: backOut });
			await pulse.set(1, { duration: 200, easing: quadOut });
			await pulse.set(0.9, { duration: 130, easing: backOut });
			await pulse.set(1, { duration: 200, easing: quadOut });
			props.oncomplete?.();
		} else if (state === 'land') {
			pulse.set(0.9, { duration: 0 });
			await pulse.set(1, { duration: 190, easing: quadOut });
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
