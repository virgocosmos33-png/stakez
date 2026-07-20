<script lang="ts" module>
	export type EmitterEventFreeSpinCounter =
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	let show = $state(false);
	let current = $state(0);
	let total = $state(0);

	// plain two-line label seated in the left margin, beside the top of the board
	const position = $derived({
		x:
			context.stateGameDerived.boardLayout().x -
			context.stateGameDerived.boardLayout().width * 0.5 -
			SYMBOL_SIZE * 0.8,
		y:
			context.stateGameDerived.boardLayout().y -
			context.stateGameDerived.boardLayout().height * 0.5 +
			SYMBOL_SIZE * 0.55,
	});

	context.eventEmitter.subscribeOnMount({
		freeSpinCounterShow: () => (show = true),
		freeSpinCounterHide: () => (show = false),
		freeSpinCounterUpdate: (emitterEvent) => {
			if (emitterEvent.current !== undefined) current = emitterEvent.current;
			if (emitterEvent.total !== undefined) total = emitterEvent.total;
		},
	});

	const tally = $derived(`${total - current} / ${total}`);

	const baseStyle = {
		fontFamily: 'Arial',
		fontWeight: '700',
		fill: 0xffffff,
		stroke: { color: 0x000000, width: 4 },
		align: 'center',
	} as const;
</script>

<MainContainer>
	<FadeContainer {show} {...position}>
		<Text
			anchor={0.5}
			y={-SYMBOL_SIZE * 0.15}
			text="FREE SPINS"
			style={{ ...baseStyle, fontSize: SYMBOL_SIZE * 0.17, letterSpacing: 1 }}
		/>
		<Text
			anchor={0.5}
			y={SYMBOL_SIZE * 0.15}
			text={tally}
			style={{ ...baseStyle, fontSize: SYMBOL_SIZE * 0.26, letterSpacing: 1 }}
		/>
	</FadeContainer>
</MainContainer>
