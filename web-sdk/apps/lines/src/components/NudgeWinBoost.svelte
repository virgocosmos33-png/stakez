<script lang="ts" module>
	export type EmitterEventNudgeWinBoost = {
		type: 'nudgeWinBoostShow';
		baseAmount: number;
		multiplier: number;
		totalAmount: number;
	};
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { BitmapText, Container } from 'pixi-svelte';
	import { waitForTimeout } from 'utils-shared/wait';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	let show = $state(false);
	let text = $state('');
	const scale = new Tween(0);
	const alpha = new Tween(1);

	context.eventEmitter.subscribeOnMount({
		// NLC-style: line win pops up, the nudge multiplier joins it, then the
		// multiplied total slams in before fading away.
		nudgeWinBoostShow: async ({ baseAmount, multiplier, totalAmount }) => {
			alpha.set(1, { duration: 0 });

			text = bookEventAmountToCurrencyString(baseAmount);
			show = true;
			scale.set(0, { duration: 0 });
			await scale.set(1, { duration: 250, easing: backOut });
			await waitForTimeout(350);

			text = `${bookEventAmountToCurrencyString(baseAmount)} × ${multiplier}`;
			scale.set(0.8, { duration: 0 });
			await scale.set(1, { duration: 200, easing: backOut });
			await waitForTimeout(500);

			text = bookEventAmountToCurrencyString(totalAmount);
			scale.set(2, { duration: 0 });
			await scale.set(1.2, { duration: 300, easing: backOut });
			await waitForTimeout(700);

			await alpha.set(0, { duration: 250, easing: cubicOut });
			show = false;
		},
	});
</script>

<MainContainer>
	{#if show}
		<Container
			x={context.stateGameDerived.boardLayout().x}
			y={context.stateGameDerived.boardLayout().y}
			scale={scale.current}
			alpha={alpha.current}
		>
			<BitmapText
				anchor={0.5}
				{text}
				style={{
					fontFamily: 'gold',
					fontSize: SYMBOL_SIZE * 0.8,
					align: 'center',
				}}
			/>
		</Container>
	{/if}
</MainContainer>
