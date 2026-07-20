<script lang="ts">
	import { Button, Popup } from 'components-shared';
	import { zIndex } from 'constants-shared/zIndex';
	import { stateModal } from 'state-shared';

	import BaseIcon from './BaseIcon.svelte';
	import BaseTitle from './BaseTitle.svelte';
	import BaseContent from './BaseContent.svelte';
	import BaseButtonWrap from './BaseButtonWrap.svelte';
	import BaseButtonContent from './BaseButtonContent.svelte';
	import BetMenuAmountToggle from './BetMenuAmountToggle.svelte';
	import BetMenuAmountGrid from './BetMenuAmountGrid.svelte';
	import { i18nDerived } from '../i18n/i18nDerived';

	const confirm = () => {
		stateModal.modal = null;
	};
</script>

{#if stateModal.modal?.name === 'betAmountMenu'}
	<Popup zIndex={zIndex.modal} onclose={() => (stateModal.modal = null)}>
		<BaseContent maxWidth="100%">
			<BaseTitle>
				{i18nDerived.betMenu()}
			</BaseTitle>

			<div class="bet-menu">
				<!-- current bet stepper -->
				<div class="stepper-plate">
					<BetMenuAmountToggle />
				</div>

				<!-- quick pick, scrollable -->
				<span class="section-label">{i18nDerived.selectYourBet()}</span>
				<BetMenuAmountGrid />
			</div>

			<BaseButtonWrap type="full-width">
				<Button data-test="confirm-button" onclick={confirm}>
					<BaseIcon width="100%" height="3rem" />
					<BaseButtonContent>
						<span class="confirm-label">{i18nDerived.confirm()}</span>
					</BaseButtonContent>
				</Button>
			</BaseButtonWrap>
		</BaseContent>
	</Popup>
{/if}

<style lang="scss">
	.bet-menu {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.9rem;
		width: 100%;
	}

	.stepper-plate {
		display: flex;
		justify-content: center;
		width: 100%;
		padding: 0.5rem 1rem;
		border-radius: 12px;
		background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(0, 0, 0, 0.35));
		border: 1px solid rgba(201, 154, 63, 0.4);
		box-shadow: inset 0 1px 0 rgba(246, 228, 166, 0.15);
	}

	.section-label {
		font-family: 'Cinzel', Georgia, serif;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		font-size: 0.78rem;
		color: #b9b1a4;
	}

	.confirm-label {
		font-family: 'Cinzel', Georgia, serif;
		font-weight: 800;
		letter-spacing: 0.08em;
		font-size: 1.05rem;
		color: #ffedb8;
		text-shadow: 0 0 8px rgba(255, 193, 46, 0.4);
	}
</style>
