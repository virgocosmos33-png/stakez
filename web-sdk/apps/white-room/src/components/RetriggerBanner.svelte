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

	const context = getContext();

	let show = $state(false);
	let amount = $state(0);
	const scale = new Tween(0);
	const alpha = new Tween(1);
	let flash = $state(0);

	// THE WHITE ROOM: stamped clinical intake toast — hard plaque + fluorescent
	// pop flash. NOT scrying-glass pill / gold séance drop-shadow.
	context.eventEmitter.subscribeOnMount({
		retriggerBannerShow: async (emitterEvent) => {
			amount = emitterEvent.amount;
			alpha.set(1, { duration: 0 });
			scale.set(0, { duration: 0 });
			flash = 1;
			show = true;
			await scale.set(1, { duration: 220, easing: backOut });
			flash = 0;
			await new Promise((resolve) => setTimeout(resolve, 900));
			await alpha.set(0, { duration: 240, easing: cubicOut });
			show = false;
		},
	});

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

	const board = $derived(context.stateGameDerived.boardLayout());
	const pillW = $derived(SYMBOL_SIZE * 3.1);
	const pillH = $derived(SYMBOL_SIZE * 0.68);
	const label = $derived(`+${amount} ${amount === 1 ? 'SPIN' : 'SPINS'}`);

	const drawStamp = (g: import('pixi.js').Graphics) => {
		const x = -pillW / 2;
		const y = -pillH / 2;
		// hard ceramic plaque
		g.roundRect(x, y, pillW, pillH, 3);
		g.fill({ color: 0xf4f1ec, alpha: 0.96 });
		g.roundRect(x, y, pillW, pillH, 3);
		g.stroke({ width: 3, color: 0x3a3632, alpha: 1 });
		// inner steel rule
		g.roundRect(x + 5, y + 5, pillW - 10, pillH - 10, 2);
		g.stroke({ width: 1.5, color: 0x8a8680, alpha: 0.8 });
		// blood stamp corner
		g.rect(x + 8, y + 8, 14, 6);
		g.fill({ color: 0x6b2a28, alpha: 0.7 });
		// fluorescent pop flash overlay
		if (flash > 0.01) {
			g.roundRect(x - 4, y - 4, pillW + 8, pillH + 8, 4);
			g.fill({ color: 0xffffff, alpha: 0.35 * flash });
		}
		// scanline stutter while held
		const scanY = y + ((time * 40) % pillH);
		g.rect(x, scanY, pillW, 2);
		g.fill({ color: 0xffffff, alpha: 0.12 });
	};
</script>

{#if show}
	<MainContainer>
		<Container
			x={board.x}
			y={board.y - board.height * 0.28}
			scale={scale.current}
			alpha={alpha.current}
		>
			<Graphics draw={drawStamp} />
			<Text
				anchor={0.5}
				text={label}
				style={{
					fontFamily: 'Arial',
					fontWeight: '900',
					fontSize: SYMBOL_SIZE * 0.28,
					fill: 0x1a1816,
					stroke: { color: 0xf4f1ec, width: 3 },
					letterSpacing: 3,
				}}
			/>
		</Container>
	</MainContainer>
{/if}
