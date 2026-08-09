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

	// card symbols animate via scale pulses since all states are static sprites
	const animate = async (state?: SymbolState) => {
		if (state === 'win') {
			await pulse.set(1.16, { duration: 180, easing: quadOut });
			await pulse.set(0.94, { duration: 150, easing: quadOut });
			await pulse.set(1.12, { duration: 150, easing: quadOut });
			await pulse.set(1, { duration: 180, easing: backOut });
			props.oncomplete?.();
		} else if (state === 'land') {
			pulse.set(1.1, { duration: 0 });
			await pulse.set(1, { duration: 180, easing: backOut });
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
