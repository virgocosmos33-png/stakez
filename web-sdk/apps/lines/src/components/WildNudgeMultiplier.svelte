<script lang="ts" module>
	export type EmitterEventWildNudgeMultiplier =
		| { type: 'nudgeMultiplierShow'; reel: number; multiplier: number }
		| { type: 'nudgeMultiplierUpdate'; multiplier: number }
		| { type: 'nudgeMultiplierHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { BitmapText, Container } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, REEL_PADDING } from '../game/constants';

	const context = getContext();

	let show = $state(false);
	let reel = $state(0);
	let multiplier = $state(1);
	const popScale = new Tween(1);

	const pop = async () => {
		popScale.set(1.7, { duration: 0 });
		await popScale.set(1, { duration: 320, easing: backOut });
	};

	context.eventEmitter.subscribeOnMount({
		nudgeMultiplierShow: (emitterEvent) => {
			reel = emitterEvent.reel;
			multiplier = emitterEvent.multiplier;
			show = true;
			pop();
		},
		nudgeMultiplierUpdate: (emitterEvent) => {
			multiplier = emitterEvent.multiplier;
			pop();
		},
		nudgeMultiplierHide: () => (show = false),
	});

	// centered on the nudged reel, sitting on the bottom edge of the board
	const position = $derived({
		x:
			context.stateGameDerived.boardLayout().x -
			context.stateGameDerived.boardLayout().width * 0.5 +
			SYMBOL_SIZE * (reel + REEL_PADDING),
		y:
			context.stateGameDerived.boardLayout().y +
			context.stateGameDerived.boardLayout().height * 0.5 -
			SYMBOL_SIZE * 0.28,
	});
</script>

<MainContainer>
	<FadeContainer {show} {...position}>
		<Container scale={popScale.current}>
			<BitmapText
				anchor={0.5}
				text={`x${multiplier}`}
				style={{
					fontFamily: 'gold',
					fontSize: SYMBOL_SIZE * 0.55,
					align: 'center',
				}}
			/>
		</Container>
	</FadeContainer>
</MainContainer>
