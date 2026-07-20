<script lang="ts" module>
	export type EmitterEventBonusLevelBanner = {
		type: 'bonusLevelShow';
		level: 1 | 2 | 3;
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { CanvasSizeRectangle, MainContainer } from 'components-layout';
	import { Container, Graphics, Sprite, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { drawGlassPill } from '../game/glassChrome';

	const context = getContext();

	// panel art is 1536x1024; the level title is baked into each painting
	const LEVEL_PANELS = {
		1: 'mirrorIntroSeance',
		2: 'mirrorIntroOtherside',
		3: 'mirrorIntroBloodmoon',
	} as const;
	// how each level plays, compared to the base game
	const LEVEL_RULES = {
		1: 'INCREASED CHANCE TO LAND MIRROR SYMBOL',
		2: 'HAUNTINGS SURVIVE ONE EXTRA SPIN\nAND STACK WHEN HIT AGAIN.',
		3: 'HAUNTINGS ARE STICKY AND STACK ENDLESSLY,\nUNTIL THE END OF THE FREE SPINS.',
	} as const;
	const PANEL_RATIO = 1024 / 1536;

	let show = $state(false);
	let level = $state<1 | 2 | 3>(1);
	const scale = new Tween(0);
	const alpha = new Tween(1);

	// the game waits on the CONTINUE click before free spins begin
	context.eventEmitter.subscribeOnMount({
		bonusLevelShow: async (emitterEvent) => {
			level = emitterEvent.level;
			alpha.set(1, { duration: 0 });
			scale.set(0, { duration: 0 });
			show = true;
			await scale.set(1, { duration: 350, easing: backOut });
			await new Promise<void>((resolve) => (oncontinue = resolve));
			await alpha.set(0, { duration: 350, easing: cubicOut });
			show = false;
		},
	});

	let oncontinue = $state(() => {});
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
	const continuePulse = $derived(1 + 0.04 * Math.sin(time * 4.2));

	const panelWidth = $derived(context.stateGameDerived.boardLayout().width * 0.98);
	const panelHeight = $derived(panelWidth * PANEL_RATIO);
</script>

<!-- pixi appends children on mount, so the dim and the panel must mount
	together (dim first) or the dim lands on top of the panel -->
{#if show}
	<Container alpha={alpha.current}>
		<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.78} />
	</Container>
	<MainContainer>
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
			scale={scale.current}
			alpha={alpha.current}
		>
			<Sprite key={LEVEL_PANELS[level]} anchor={0.5} width={panelWidth} height={panelHeight} />
			<!-- mechanics vs base game, centred in the empty glass of the painting -->
			<Text
				anchor={0.5}
				y={panelHeight * 0.02}
				text={LEVEL_RULES[level]}
				style={{
					fontFamily: 'Arial',
					fontWeight: '700',
					fontSize: SYMBOL_SIZE * 0.15,
					fill: 0xffffff,
					stroke: { color: 0x000000, width: 4 },
					align: 'center',
					lineHeight: SYMBOL_SIZE * 0.22,
				}}
			/>
			<Container y={panelHeight * 0.32} scale={continuePulse}>
				<Graphics
					eventMode="static"
					cursor="pointer"
					onpointerup={() => oncontinue()}
					draw={(g) => drawGlassPill(g, { width: SYMBOL_SIZE * 2.4, height: SYMBOL_SIZE * 0.56 })}
				/>
				<Text
					anchor={0.5}
					text="CONTINUE"
					eventMode="none"
					style={{
						fontFamily: 'Arial',
						fontWeight: '900',
						fontSize: SYMBOL_SIZE * 0.24,
						fill: 0xffffff,
						stroke: { color: 0x000000, width: 4 },
						letterSpacing: 2,
					}}
				/>
			</Container>
		</Container>
	</MainContainer>
{/if}
