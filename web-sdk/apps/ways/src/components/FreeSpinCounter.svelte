<script lang="ts" module>
	export type EmitterEventFreeSpinCounter =
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { Container, Sprite, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { drawWindowShade } from '../game/glassChrome';
	import FittedText from './FittedText.svelte';

	const context = getContext();

	// Ornate amethyst haunted-mirror plaque (generated art, mirrorFsFrame) with
	// a dark-glass window. "FREE SPINS" and the live "current / total" tally are
	// stacked as FittedText INSIDE the window, so each line auto-fits and can
	// never overlap the other line or the ornate frame.
	const FRAME_RATIO = 985 / 1310; // processed fs_frame.png h/w
	const FRAME_W = SYMBOL_SIZE * 1.9;
	const FRAME_H = FRAME_W * FRAME_RATIO;

	const WIN = { cx: 0.498, cy: 0.518, w: 0.768, h: 0.445 };
	const winX = (WIN.cx - 0.5) * FRAME_W;
	const winY = (WIN.cy - 0.5) * FRAME_H;
	const winW = WIN.w * FRAME_W;
	const winH = WIN.h * FRAME_H;

	let show = $state(false);
	let current = $state(0);
	let total = $state(0);

	// seated in the left margin, beside the top of the board
	const position = $derived({
		x:
			context.stateGameDerived.boardLayout().x -
			context.stateGameDerived.boardLayout().width * 0.5 -
			FRAME_W * 0.5 -
			SYMBOL_SIZE * 0.3,
		y:
			context.stateGameDerived.boardLayout().y -
			context.stateGameDerived.boardLayout().height * 0.5 +
			FRAME_H * 0.5,
	});

	context.eventEmitter.subscribeOnMount({
		freeSpinCounterShow: () => (show = true),
		freeSpinCounterHide: () => (show = false),
		freeSpinCounterUpdate: (emitterEvent) => {
			if (emitterEvent.current !== undefined) current = emitterEvent.current;
			if (emitterEvent.total !== undefined) total = emitterEvent.total;
		},
	});

	const tally = $derived(`${current} / ${total}`);
</script>

<MainContainer>
	<FadeContainer {show} {...position}>
		<!-- glass recess + subtle etched texture behind both lines -->
		<Container x={winX} y={winY}>
			<Graphics
				draw={(g) => drawWindowShade(g, { width: winW * 0.98, height: winH * 0.94, radius: winH * 0.16 })}
			/>
			<Sprite
				key="mirrorCounterGlass"
				anchor={0.5}
				width={winW * 0.98}
				height={winH * 0.94}
				alpha={0.22}
			/>
		</Container>

		<Sprite key="mirrorFsFrame" anchor={0.5} width={FRAME_W} height={FRAME_H} />

		<!-- FREE SPINS caption (top line) -->
		<FittedText
			x={winX}
			y={winY - winH * 0.27}
			maxWidth={winW * 0.9}
			maxHeight={winH * 0.34}
			tint={0xcdb8f5}
			text="FREE SPINS"
			style={{ fontFamily: 'silver', fontSize: (winH * 0.34) / 1.69, letterSpacing: 2 }}
		/>
		<!-- current / total tally (hero, bottom line) -->
		<FittedText
			x={winX}
			y={winY + winH * 0.21}
			maxWidth={winW * 0.9}
			maxHeight={winH * 0.5}
			tint={0xf6f0ff}
			text={tally}
			style={{ fontFamily: 'silver', fontSize: (winH * 0.5) / 1.69, letterSpacing: 1 }}
		/>
	</FadeContainer>
</MainContainer>
