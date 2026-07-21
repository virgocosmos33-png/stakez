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
					<BaseIcon width="100%" height="3rem" border="2px solid white" />
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
		background: var(--mono-bg, #10161d);
		border: 1px solid var(--mono-hairline, #2a3542);
	}

	.section-label {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		font-size: 0.78rem;
		color: var(--mono-fg-dim, #8b96a3);
	}

	.confirm-label {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-weight: 700;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		font-size: 1.05rem;
		color: var(--mono-fg, #ffffff);
	}
</style>
