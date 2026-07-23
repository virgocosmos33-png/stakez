<script lang="ts">
	import { Button, Popup } from 'components-shared';
	import { zIndex } from 'constants-shared/zIndex';
	import { stateBet, stateBetDerived, stateModal, stateUi, INFINITY_MARK } from 'state-shared';
	import { getContextEventEmitter } from 'utils-event-emitter';

	import BaseIcon from './BaseIcon.svelte';
	import BaseTitle from './BaseTitle.svelte';
	import BaseContent from './BaseContent.svelte';
	import BaseScrollable from './BaseScrollable.svelte';
	import BaseButtonWrap from './BaseButtonWrap.svelte';
	import BaseButtonContent from './BaseButtonContent.svelte';
	import { stateBonus, stateBonusDerived } from '../stateBonus.svelte';
	import { i18nDerived } from '../i18n/i18nDerived';
	import type { EmitterEventModal } from '../types';

	const { eventEmitter } = getContextEventEmitter<EmitterEventModal>();

	const confirm = () => {
		stateBet.activeBetModeKey = stateBonus.selectedBetModeKey;

		if (stateBonusDerived.selectedBetModeData().type === 'buy') {
			eventEmitter.broadcast({ type: 'bet' });
		}

		if (stateBonusDerived.selectedBetModeData().type === 'activate') {
			// the mode multiplies the bet cost - re-clamp the bet amount so the
			// new cost still fits the balance, otherwise the spin button silently
			// disables and "pressing spin does nothing"
			stateBetDerived.setBetAmount(stateBet.betAmount);
			stateUi.autoSpinsLossLimitText = INFINITY_MARK;
			stateUi.autoSpinsSingleWinLimitText = INFINITY_MARK;
		}
	};
</script>

{#if stateModal.modal?.name === 'buyBonusConfirm'}
	<Popup zIndex={zIndex.dialog} onclose={() => (stateModal.modal = { name: 'buyBonus' })}>
		<BaseContent maxWidth="500px">
			<BaseTitle>
				{stateBonusDerived.selectedBetModeData().text.title}
			</BaseTitle>
			{#if stateBonusDerived.selectedBetModeData().assets.dialogImage}
				<img
					class="dialog-image"
					src={stateBonusDerived.selectedBetModeData().assets.dialogImage}
					alt={stateBonusDerived.selectedBetModeData().text.title}
				/>
			{/if}
			<BaseScrollable type="column">
				{stateBonusDerived.selectedBetModeData().text.dialog}
			</BaseScrollable>
			<BaseButtonWrap type="max-width">
				<Button
					data-test="confirm-button"
					onclick={() => {
						confirm();
						eventEmitter.broadcast({ type: 'soundPressGeneral' });
						stateModal.modal = null;
					}}
				>
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
	.dialog-image {
		width: 100%;
		height: auto;
		display: block;
		border-radius: 8px;
	}

	.confirm-label {
		font-family: var(--mono-font, 'Segoe UI', Arial, sans-serif);
		font-size: 1rem;
		font-weight: 700;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--mono-fg, #ffffff);
	}
</style>
