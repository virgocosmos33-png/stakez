<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, quadOut } from 'svelte/easing';

	import { Container, Sprite } from 'pixi-svelte';

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

	// Sprite-only symbols stay flat on a win — no scale pop, no mesh warp.
	// Land still does a short settle so a dropping WILD / scatter reads as a hit.
	const animate = async (state?: SymbolState) => {
		if (state === 'win') {
			pulse.set(1, { duration: 0 });
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

<Container x={props.x} y={props.y} scale={pulse.current}>
	<Sprite
		anchor={0.5}
		key={props.symbolInfo.assetKey}
		width={SYMBOL_SIZE * props.symbolInfo.sizeRatios.width}
		height={SYMBOL_SIZE * props.symbolInfo.sizeRatios.height}
		blendMode="normal"
	/>
</Container>
