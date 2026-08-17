<script lang="ts" module>
	/** the golden sheriff card the last-reel lane swaps into the cell pocket
	 *  when its special fires: BOUNTY star / SUPER SPLIT revolvers / NUDGE spur. */
	export type EmitterEventLaneCard = {
		type: 'laneCardShow';
		kind: 'bounty' | 'supersplit' | 'nudge' | 'shooter';
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicIn, cubicOut } from 'svelte/easing';
	import { Container, Rectangle, Sprite } from 'pixi-svelte';
	import { stateBet } from 'state-shared';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W } from '../game/constants';
	import { getSymbolX, getCellCenterY, getCardHeight } from '../game/utils';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { LANE_CARD_Z } from '../game/laneDoor';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	const KIND_SPRITE = {
		bounty: 'laneGoldBounty',
		supersplit: 'laneGoldSupersplit',
		nudge: 'laneGoldNudge',
		shooter: 'laneGoldNudge',
	} as const;

	let kind = $state<null | keyof typeof KIND_SPRITE>(null);
	const swap = new Tween(0, { duration: 0 });

	$effect(() => {
		context.stateGame.laneCardSwap = swap.current;
	});

	context.eventEmitter.subscribeOnMount({
		laneCardShow: async (event) => {
			const instant = stateBet.isSuperTurbo;
			const tier = (ms: number) => (instant ? 0 : fxDur(ms));
			kind = event.kind;
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
			swap.set(0, { duration: 0 });
			await swap.set(1, { duration: tier(320), easing: cubicOut });
			await fxWait(tier(520));
			await swap.set(0, { duration: tier(280), easing: cubicIn });
			kind = null;
		},
	});

	const LAST = context.stateGame.board.length - 1;
	const cx = $derived(getSymbolX(LAST));
	const cy = $derived(getCellCenterY(LAST, 1));
	const pocketH = $derived(getCardHeight(LAST));
	const goldY = $derived(cy + (swap.current - 1) * pocketH);
</script>

{#if kind}
	<Container zIndex={LANE_CARD_Z} eventMode="none">
		<BoardSpace>
			<Container x={cx} y={cy} eventMode="none">
				<Rectangle
					isMask
					anchor={0.5}
					width={SYMBOL_CARD_W}
					height={pocketH}
					backgroundColor={0xffffff}
				/>
				<Sprite
					key={KIND_SPRITE[kind]}
					x={0}
					y={goldY - cy}
					anchor={0.5}
					width={SYMBOL_CARD_W}
					height={pocketH}
					eventMode="none"
				/>
			</Container>
		</BoardSpace>
	</Container>
{/if}
