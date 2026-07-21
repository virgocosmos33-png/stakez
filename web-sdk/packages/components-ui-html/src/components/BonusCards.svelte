<script lang="ts">
	import { stateBet, stateModal, type BetModeData } from 'state-shared';
	import { Button } from 'components-shared';
	import { getContextEventEmitter } from 'utils-event-emitter';
	import { numberToCurrencyString } from 'utils-shared/amount';

	import BaseIcon from './BaseIcon.svelte';
	import BonusCard from './BonusCard.svelte';
	import BaseButtonContent from './BaseButtonContent.svelte';
	import { stateBonus } from '../stateBonus.svelte';
	import type { EmitterEventModal } from '../types';

	type Props = {
		list: BetModeData[];
	};

	const props: Props = $props();
	const { eventEmitter } = getContextEventEmitter<EmitterEventModal>();
</script>

{#each props.list as betModeData}
	{#if betModeData.type !== 'default'}
		{@const affordable =
			stateBet.betAmount > 0 &&
			stateBet.balanceAmount >= stateBet.betAmount * betModeData.costMultiplier}
		<BonusCard {affordable}>
			{#snippet title()}
				{#if betModeData.assets.icon}
					<!-- the bonus name is baked into the card art, so no text title here -->
					<img class="card-art" src={betModeData.assets.icon} alt={betModeData.text.title} />
				{:else}
					<div class="title">
						{betModeData.text.title}
					</div>
				{/if}
			{/snippet}

			{#snippet description()}
				{#if betModeData?.text?.description}
					<div class="description">
						{betModeData.text.description}
					</div>
				{/if}
			{/snippet}

			{#snippet price()}
				<div class="price">
					{`${numberToCurrencyString(stateBet.betAmount * betModeData.costMultiplier)}`}
				</div>
			{/snippet}

			{#snippet button()}
				<Button
					onclick={() => {
						stateBonus.selectedBetModeKey = betModeData.mode;
						eventEmitter.broadcast({ type: 'buyBonusConfirm' });
						eventEmitter.broadcast({ type: 'soundPressGeneral' });
					}}
					disabled={!affordable}
				>
					<BaseIcon width="100%" height="2rem" border="2px solid white;" />
					<BaseButtonContent>
						<span class="btn-label">{betModeData.text.button}</span>
					</BaseButtonContent>
				</Button>
			{/snippet}
		</BonusCard>
	{/if}
{/each}

<style lang="scss">
	.card-art {
		width: 100%;
		height: auto;
		display: block;
		border-radius: 6px;
	}

	.title {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-weight: 600;
		font-size: 1rem;
		line-height: 1rem;
		text-align: center;
		color: var(--mono-fg, #ffffff);
	}

	.description {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-size: 0.75rem;
		text-align: center;
		min-height: 0;
		white-space: pre-line;
		display: inline-flex;
		align-items: center;
		color: var(--mono-fg-dim, #8b96a3);
	}

	.description:empty {
		display: none;
	}

	.price {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-weight: 700;
		font-size: 1rem;
		line-height: 1rem;
		text-align: center;
		white-space: nowrap;
		color: var(--mono-fg, #ffffff);
		font-variant-numeric: tabular-nums;
	}

	.btn-label {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-size: 0.9rem;
		font-weight: 700;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--mono-fg, #ffffff);
	}
</style>
