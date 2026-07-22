<script lang="ts" module>
	export type EmitterEventRetriggerBanner = {
		type: 'retriggerBannerShow';
		amount: number;
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { drawGlassPill } from '../game/glassChrome';

	const context = getContext();

	let show = $state(false);
	let amount = $state(0);
	const scale = new Tween(0);
	const alpha = new Tween(1);

	// self-dismissing award toast: pops in, holds, fades out. broadcastAsync
	// awaits this handler so the book pauses just long enough to read it.
	context.eventEmitter.subscribeOnMount({
		retriggerBannerShow: async (emitterEvent) => {
			amount = emitterEvent.amount;
			alpha.set(1, { duration: 0 });
			scale.set(0, { duration: 0 });
			show = true;
			await scale.set(1, { duration: 320, easing: backOut });
			await new Promise((resolve) => setTimeout(resolve, 900));
			await alpha.set(0, { duration: 300, easing: cubicOut });
			show = false;
		},
	});

	// gentle idle pulse while it holds on screen
	let time = $state(0);
	$effect(() => {
		if (!show) return;
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
	const pulse = $derived(1 + 0.03 * Math.sin(time * 5));

	const board = $derived(context.stateGameDerived.boardLayout());
	const pillW = $derived(SYMBOL_SIZE * 3.0);
	const pillH = $derived(SYMBOL_SIZE * 0.72);
	const label = $derived(`+${amount} ${amount === 1 ? 'SPIN' : 'SPINS'}`);
</script>

{#if show}
	<MainContainer>
		<Container
			x={board.x}
			y={board.y - board.height * 0.28}
			scale={scale.current * pulse}
			alpha={alpha.current}
		>
			<Graphics draw={(g) => drawGlassPill(g, { width: pillW, height: pillH })} />
			<Text
				anchor={0.5}
				text={label}
				style={{
					fontFamily: 'Arial',
					fontWeight: '900',
					fontSize: SYMBOL_SIZE * 0.3,
					fill: 0xf3e7c4,
					stroke: { color: 0x1a0f2c, width: 5 },
					letterSpacing: 2,
					dropShadow: {
						color: 0xb887ff,
						alpha: 0.6,
						blur: 6,
						distance: 0,
						angle: 0,
					},
				}}
			/>
		</Container>
	</MainContainer>
{/if}
