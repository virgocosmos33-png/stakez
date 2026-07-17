<script lang="ts" module>
	export type EmitterEventWaysCounter =
		| { type: 'waysCounterUpdate'; ways: number }
		| { type: 'waysCounterHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { BitmapText, Container, Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	// brass plaque art is 1011x966; the odometer window sits just above its centre
	const PANEL_RATIO = 966 / 1011;
	const PANEL_WIDTH = SYMBOL_SIZE * 1.05;
	const PANEL_HEIGHT = PANEL_WIDTH * PANEL_RATIO;
	const WINDOW = {
		y: -PANEL_HEIGHT * 0.028,
		width: PANEL_WIDTH * 0.44,
		height: PANEL_HEIGHT * 0.155,
	};

	let show = $state(false);
	let ways = $state(1024);
	const popScale = new Tween(1);

	const pop = async () => {
		popScale.set(1.35, { duration: 0 });
		await popScale.set(1, { duration: 300, easing: backOut });
	};

	context.eventEmitter.subscribeOnMount({
		waysCounterUpdate: (emitterEvent) => {
			ways = emitterEvent.ways;
			show = true;
			pop();
		},
		waysCounterHide: () => (show = false),
	});

	// séance tally plaque, mounted on the crest of the reels frame so it never
	// clips off the top of the canvas (the board top sits near the canvas edge)
	const position = $derived({
		x: context.stateGameDerived.boardLayout().x,
		y:
			context.stateGameDerived.boardLayout().y -
			context.stateGameDerived.boardLayout().height * 0.5 -
			PANEL_HEIGHT * 0.1,
	});
</script>

<MainContainer>
	<FadeContainer {show} {...position}>
		<Container scale={popScale.current}>
			<Sprite key="mirrorWaysPanel" anchor={0.5} width={PANEL_WIDTH} height={PANEL_HEIGHT} />
			<Rectangle
				anchor={0.5}
				y={WINDOW.y}
				width={WINDOW.width}
				height={WINDOW.height}
				backgroundColor={0x120c06}
			/>
			<BitmapText
				anchor={0.5}
				y={WINDOW.y}
				text={ways.toLocaleString('en-US')}
				style={{ fontFamily: 'gold', fontSize: WINDOW.height * 0.78, align: 'center' }}
			/>
		</Container>
	</FadeContainer>
</MainContainer>
