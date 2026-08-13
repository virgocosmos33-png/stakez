<script lang="ts" module>
	/** the golden sheriff card the last-reel lane flashes when its special
	 *  fires: BOUNTY star / SUPER SPLIT revolvers / NUDGE spur. */
	export type EmitterEventLaneCard = {
		type: 'laneCardShow';
		kind: 'bounty' | 'supersplit' | 'nudge';
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite } from 'pixi-svelte';
	import { stateBet } from 'state-shared';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_H } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { stateShake } from '../game/stateShake.svelte';
	import { fxDur, fxWait } from '../game/fxTiming';

	const context = getContext();

	const KIND_SPRITE = {
		bounty: 'laneGoldBounty',
		supersplit: 'laneGoldSupersplit',
		nudge: 'laneGoldNudge',
	} as const;

	/** source art is 384x576 — keep its aspect so the gold isn't squashed */
	const ART_ASPECT = 384 / 576;
	const CARD_H = SYMBOL_CARD_H * 1.04;
	const CARD_W = CARD_H * ART_ASPECT;

	let kind = $state<null | keyof typeof KIND_SPRITE>(null);
	const pop = new Tween(0, { duration: 0 });

	context.eventEmitter.subscribeOnMount({
		laneCardShow: async (event) => {
			const instant = stateBet.isSuperTurbo;
			const tier = (ms: number) => (instant ? 0 : fxDur(ms));
			kind = event.kind;
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
			pop.set(0, { duration: 0 });
			await pop.set(1, { duration: tier(260), easing: backOut });
			await fxWait(tier(650));
			await pop.set(0, { duration: tier(200), easing: cubicIn });
			kind = null;
		},
	});

	const LAST = context.stateGame.board.length - 1;
	const boardLayout = $derived(context.stateGameDerived.boardLayout());
	const cx = $derived(boardLayout.x - boardLayout.width * 0.5 + getSymbolX(LAST));
	const cy = $derived(boardLayout.y - boardLayout.height * 0.5 + getCellCenterY(LAST, 1));

	const scale = $derived(0.55 + 0.45 * pop.current);
	const alpha = $derived(Math.min(1, pop.current * 1.4));
</script>

{#if kind}
	<MainContainer>
		<Container x={stateShake.x} y={stateShake.y}>
			<Sprite
				key={KIND_SPRITE[kind]}
				x={cx}
				y={cy}
				anchor={0.5}
				width={CARD_W * scale}
				height={CARD_H * scale}
				{alpha}
				eventMode="none"
			/>
		</Container>
	</MainContainer>
{/if}
