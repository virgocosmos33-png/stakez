<script lang="ts">
	import { Container, Sprite, Text } from 'pixi-svelte';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import { waysLabel } from '../game/waysFormat';
	import {
		fitFontSize,
		trLabelStyle,
		trValueStyle,
		TR_INK_GOLD,
		TR_INK_IRON,
	} from '../game/typography';

	type Props = {
		amount: number;
		ways: number;
	};

	const props: Props = $props();
	const context = getContext();

	/** Authored plate 1536×1024. Width follows the board hole. Never stretch. */
	const ART_W = 1536;
	const ART_H = 1024;
	const plateW = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		return Math.max(1, (board.visualRight - board.visualLeft) * 0.78);
	});
	const plateH = $derived(plateW * (ART_H / ART_W));
	const textW = $derived(plateW * 0.5);
	const waysText = $derived(props.ways > 0 ? waysLabel(props.ways) : '');
	const amountText = $derived(bookEventAmountToCurrencyString(props.amount));
	const waysSize = $derived(
		fitFontSize(waysText, {
			role: 'label',
			base: Math.max(22, Math.floor(plateH * 0.09)),
			maxWidth: textW,
			min: 16,
			letterSpacing: 2,
		}),
	);
	const amountSize = $derived(
		fitFontSize(amountText, {
			role: 'value',
			base: Math.max(34, Math.floor(plateH * 0.16)),
			maxWidth: textW,
			min: 22,
			letterSpacing: 0.4,
		}),
	);
	const waysStroke = $derived(Math.max(2, Math.round(waysSize * 0.08)));
	const amountStroke = $derived(Math.max(3, Math.round(amountSize * 0.07)));
</script>

<Container>
	<Sprite key="winChipPlate" anchor={0.5} width={plateW} height={plateH} eventMode="none" />
	{#if waysText}
		<Text
			x={0}
			y={plateH * -0.04}
			anchor={0.5}
			text={waysText}
			eventMode="none"
			style={trLabelStyle({
				fill: TR_INK_GOLD,
				fontSize: waysSize,
				letterSpacing: 2,
				lineHeight: waysSize,
				stroke: { color: TR_INK_IRON, width: waysStroke, join: 'round' },
				dropShadow: {
					color: 0x000000,
					blur: 3,
					distance: 1,
					alpha: 0.55,
					angle: Math.PI / 2,
				},
			})}
		/>
	{/if}
	<Text
		x={0}
		y={plateH * 0.1}
		anchor={0.5}
		text={amountText}
		eventMode="none"
		style={trValueStyle({
			fill: TR_INK_GOLD,
			fontSize: amountSize,
			letterSpacing: 0.4,
			lineHeight: amountSize,
			stroke: { color: TR_INK_IRON, width: amountStroke, join: 'round' },
			dropShadow: {
				color: 0x000000,
				blur: 4,
				distance: 2,
				alpha: 0.6,
				angle: Math.PI / 2,
			},
		})}
	/>
</Container>
