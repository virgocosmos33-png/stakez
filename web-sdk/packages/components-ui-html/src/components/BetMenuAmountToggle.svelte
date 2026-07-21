<script lang="ts">
	import { stateBet, stateConfig } from 'state-shared';
	import { Button, OptionsToggle } from 'components-shared';
	import { getContextEventEmitter } from 'utils-event-emitter';
	import { numberToCurrencyString } from 'utils-shared/amount';

	import BaseIcon from './BaseIcon.svelte';
	import BaseButtonContent from './BaseButtonContent.svelte';
	import type { EmitterEventModal } from '../types';

	const { eventEmitter } = getContextEventEmitter<EmitterEventModal>();

	const iconSize = '2.75rem';
</script>

<OptionsToggle
	value={stateBet.betAmount}
	options={stateConfig.betAmountOptions}
	onchange={(value) => {
		stateBet.betAmount = value;
		eventEmitter.broadcast({ type: 'soundPressGeneral' });
	}}
>
	{#snippet children({ disabledDown, disabledUp, toggleDown, toggleUp })}
		<div class="toggle-wrap">
			<Button data-test="down-button" disabled={disabledDown} onclick={toggleDown}>
				<BaseIcon width={iconSize} height={iconSize} />
				<BaseButtonContent>
					<span class="glyph">&#8722;</span>
				</BaseButtonContent>
			</Button>

			<span class="amount">{numberToCurrencyString(stateBet.betAmount)}</span>

			<Button data-test="up-button" disabled={disabledUp} onclick={toggleUp}>
				<BaseIcon width={iconSize} height={iconSize} />
				<BaseButtonContent>
					<span class="glyph">+</span>
				</BaseButtonContent>
			</Button>
		</div>
	{/snippet}
</OptionsToggle>

<style lang="scss">
	.toggle-wrap {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 0.5rem;
	}

	.amount {
		min-width: 6rem;
		text-align: center;
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-weight: 700;
		font-size: 1.35rem;
		letter-spacing: 0.3px;
		color: var(--mono-fg, #ffffff);
		font-variant-numeric: tabular-nums;
	}

	.glyph {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-size: 1.6rem;
		font-weight: 400;
		line-height: 1;
		color: var(--mono-fg, #ffffff);
	}
</style>
