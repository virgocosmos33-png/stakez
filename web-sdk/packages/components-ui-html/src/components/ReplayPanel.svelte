<script lang="ts">
	// Bet replay (`?replay=true`). The stored round is fetched by Authenticate
	// into stateBet.betToResume; this card holds it back, shows what the round
	// played for and what it returned, and only then hands it to the game.
	// ResumeBet re-seeds the actor from stateReplay.round on every start, which
	// is what makes "Replay again" work.
	import { stateBet, stateReplay, stateUrlDerived } from 'state-shared';
	import { numberToCurrencyString } from 'utils-shared/amount';
	import { zIndex } from 'constants-shared/zIndex';

	const isReplay = stateUrlDerived.replay();

	$effect(() => {
		if (!isReplay || stateReplay.round || !stateBet.betToResume) return;
		stateReplay.round = { ...stateBet.betToResume };
	});

	const payoutMultiplier = $derived(stateReplay.round?.payoutMultiplier ?? 0);
	const betAmount = $derived(stateBet.wageredBetAmount);
	const payoutAmount = $derived(betAmount * payoutMultiplier);

	const start = () => {
		stateReplay.phase = 'playing';
	};

	const show = $derived(isReplay && Boolean(stateReplay.round) && stateReplay.phase !== 'playing');
	const isReplayAgain = $derived(stateReplay.phase === 'ended');
</script>

{#if show}
	<div class="backdrop" style="z-index: {zIndex.modal}">
		<section class="card" role="dialog" aria-label="Bet replay">
			<h1>{isReplayAgain ? 'Round finished' : 'Bet replay'}</h1>

			<dl>
				<div class="row">
					<dt>Bet</dt>
					<dd>{numberToCurrencyString(betAmount)}</dd>
				</div>
				<div class="row">
					<dt>Win</dt>
					<dd class:won={payoutMultiplier > 0}>
						{numberToCurrencyString(payoutAmount)}
						<span class="mult">{payoutMultiplier.toFixed(2)}x</span>
					</dd>
				</div>
			</dl>

			<button type="button" onclick={start}>
				{isReplayAgain ? 'Replay again' : 'Start replay'}
			</button>
		</section>
	</div>
{/if}

<style lang="scss">
	.backdrop {
		position: fixed;
		inset: 0;
		display: grid;
		place-items: center;
		padding: 1.5rem;
		background: rgba(0, 0, 0, 0.62);
		pointer-events: auto;
	}

	.card {
		width: min(26rem, 100%);
		box-sizing: border-box;
		padding: 1.75rem;
		border-radius: 14px;
		border: 1px solid #3a4552;
		background: linear-gradient(180deg, #191d25 0%, #0f1319 100%);
		box-shadow: 0 26px 64px rgba(0, 0, 0, 0.62);
		color: #ece7db;
		text-align: center;
		font-family: var(--mono-font, 'Segoe UI', Arial, Helvetica, sans-serif);
	}

	h1 {
		margin: 0 0 1.25rem;
		font-size: 1.5rem;
		font-weight: 800;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		color: #e9c46a;
	}

	dl {
		margin: 0 0 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.row {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 1.5rem;
		padding: 0.55rem 0.8rem;
		border-radius: 0.4rem;
		border: 1px solid rgba(255, 255, 255, 0.1);
		background: rgba(0, 0, 0, 0.28);
	}

	dt {
		color: rgba(244, 244, 246, 0.85);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		font-size: 0.85rem;
	}

	dd {
		margin: 0;
		font-variant-numeric: tabular-nums;
		font-weight: 700;
		color: #ffffff;

		&.won {
			color: #7ee081;
		}
	}

	.mult {
		margin-left: 0.5rem;
		font-weight: 600;
		font-size: 0.85rem;
		color: rgba(244, 244, 246, 0.6);
	}

	button {
		width: 100%;
		padding: 0.85rem 1rem;
		border: none;
		border-radius: 999px;
		background: #ffde6a;
		color: #0a0e14;
		font-size: 1rem;
		font-weight: 800;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		cursor: pointer;
		transition:
			transform 0.12s ease,
			background 0.15s ease;

		&:hover {
			transform: scale(1.02);
			background: #ffe88c;
		}

		&:focus-visible {
			outline: 3px solid #ffffff;
			outline-offset: 2px;
		}
	}
</style>
