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
	import { Container, Sprite, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { drawWindowShade } from '../game/glassChrome';
	import FittedText from './FittedText.svelte';

	const context = getContext();

	// Ornate amethyst haunted-mirror nameplate (generated art, mirrorWaysFrame)
	// with a dedicated dark-glass display window. "WAYS" + the live count are
	// rendered as FittedText INSIDE that window so they always fit and never
	// collide with each other or the ornate frame.
	const FRAME_RATIO = 827 / 1505; // processed ways_frame.png h/w
	const FRAME_W = SYMBOL_SIZE * 2.4;
	const FRAME_H = FRAME_W * FRAME_RATIO;

	// glass window, measured from the art (fractions of the frame), then a safe
	// inner inset so text keeps clear of the ornate lip
	const WIN = { cx: 0.517, cy: 0.495, w: 0.789, h: 0.352 };
	const winX = (WIN.cx - 0.5) * FRAME_W;
	const winY = (WIN.cy - 0.5) * FRAME_H;
	const winW = WIN.w * FRAME_W;
	const winH = WIN.h * FRAME_H;
	const textH = winH * 0.66;

	let show = $state(false);
	let ways = $state(1024);
	const popScale = new Tween(1);

	const pop = async () => {
		popScale.set(1.22, { duration: 0 });
		await popScale.set(1, { duration: 320, easing: backOut });
	};

	context.eventEmitter.subscribeOnMount({
		waysCounterUpdate: (emitterEvent) => {
			ways = emitterEvent.ways;
			show = true;
			pop();
		},
		waysCounterHide: () => (show = false),
	});

	// on the crest of the reels, mostly above the board top
	const position = $derived({
		x: context.stateGameDerived.boardLayout().x,
		y:
			context.stateGameDerived.boardLayout().y -
			context.stateGameDerived.boardLayout().height * 0.5 -
			FRAME_H * 0.34,
	});

	// comma renders as a floating high tick in the silver atlas, so group
	// thousands with a plain space instead ("15 360")
	const waysText = $derived(ways.toLocaleString('en-US').replaceAll(',', ' '));
</script>

<MainContainer>
	<FadeContainer {show} {...position}>
		<Container scale={popScale.current}>
			<!-- soft recess so the silver number lifts off the glass -->
			<Container x={winX} y={winY}>
				<Graphics
					draw={(g) => drawWindowShade(g, { width: winW * 0.98, height: winH * 0.9, radius: winH * 0.32 })}
				/>
				<Sprite
					key="mirrorCounterGlass"
					anchor={0.5}
					width={winW * 0.98}
					height={winH * 0.92}
					alpha={0.22}
				/>
			</Container>

			<Sprite key="mirrorWaysFrame" anchor={0.5} width={FRAME_W} height={FRAME_H} />

			<!-- WAYS caption (left third) -->
			<FittedText
				x={winX - winW * 0.31}
				y={winY}
				maxWidth={winW * 0.32}
				maxHeight={textH * 0.62}
				tint={0xcdb8f5}
				text="WAYS"
				style={{ fontFamily: 'silver', fontSize: (textH * 0.62) / 1.69, letterSpacing: 2 }}
			/>
			<!-- live count (hero, right two-thirds) -->
			<FittedText
				x={winX + winW * 0.17}
				y={winY}
				maxWidth={winW * 0.6}
				maxHeight={textH}
				tint={0xf6f0ff}
				text={waysText}
				style={{ fontFamily: 'silver', fontSize: textH / 1.69, letterSpacing: 1 }}
			/>
		</Container>
	</FadeContainer>
</MainContainer>
