<script lang="ts">
	import { Popup } from 'components-shared';
	import { zIndex } from 'constants-shared/zIndex';
	import { stateModal, stateMetaDerived } from 'state-shared';

	import BonusCards from './BonusCards.svelte';
	import BetMenuAmountToggle from './BetMenuAmountToggle.svelte';
	import BonusContentWrap from './BonusContentWrap.svelte';

	const activateList = $derived(
		stateMetaDerived.betModeMetaList().filter((item) => item.type === 'activate'),
	);

	const buyList = $derived(
		stateMetaDerived.betModeMetaList().filter((item) => item.type === 'buy'),
	);
</script>

{#if stateModal.modal?.name === 'buyBonus'}
	<Popup zIndex={zIndex.modal} onclose={() => (stateModal.modal = null)}>
		<BonusContentWrap>
			{#snippet betAmount()}
				<BetMenuAmountToggle />
			{/snippet}

			{#snippet bonusCardsActivate()}
				<BonusCards list={activateList} />
			{/snippet}

			{#snippet bonusCardsBuy()}
				<BonusCards list={buyList} />
			{/snippet}
		</BonusContentWrap>
	</Popup>
{/if}
