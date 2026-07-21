<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		maxListLength: number;
		betAmount: Snippet;
		bonusCardsActivate: Snippet;
		bonusCardsBuy: Snippet;
	};

	const props: Props = $props();
</script>

<!-- Mobile portrait: full-viewport sheet, bet stepper on top, 2-col card grid
     that scrolls vertically. No transform-scale hacks. -->
<div class="sheet">
	<div class="bet-row">
		{@render props.betAmount()}
	</div>

	<div class="cards-scroll">
		<div class="cards-grid">
			{@render props.bonusCardsActivate()}
			{@render props.bonusCardsBuy()}
		</div>
	</div>
</div>

<style lang="scss">
	.sheet {
		box-sizing: border-box;
		width: min(100vw - 1rem, 440px);
		max-height: min(92dvh, 920px);
		display: flex;
		flex-direction: column;
		gap: 0.7rem;
		padding: 1.1rem 0.8rem 1rem;
		margin: 0.5rem;
		border-radius: 16px;
		background: linear-gradient(180deg, #131a22, #0b0f14);
		border: 1px solid var(--mono-hairline, #2a3542);
		box-shadow:
			0 12px 44px rgba(0, 0, 0, 0.7),
			inset 0 1px 0 rgba(255, 255, 255, 0.04);
	}

	.bet-row {
		flex: 0 0 auto;
		display: flex;
		justify-content: center;
		padding: 0.35rem 0.5rem;
		border-radius: 12px;
		background: var(--mono-bg, #10161d);
		border: 1px solid var(--mono-hairline, #2a3542);
	}

	.cards-scroll {
		flex: 1 1 auto;
		min-height: 0;
		overflow-x: hidden;
		overflow-y: auto;
		-webkit-overflow-scrolling: touch;
		overscroll-behavior: contain;
		padding: 0.15rem 0.1rem 0.35rem;
		scrollbar-width: thin;
		scrollbar-color: var(--mono-edge, #33414f) rgba(255, 255, 255, 0.06);

		&::-webkit-scrollbar {
			width: 6px;
		}
		&::-webkit-scrollbar-thumb {
			background: var(--mono-edge, #33414f);
			border-radius: 999px;
		}
	}

	.cards-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 0.55rem;
		align-content: start;

		// fluid cards — kill the desktop fixed widths
		:global(.bonus-card-wrap) {
			min-width: 0;
			max-width: none;
			width: 100%;
			height: 100%;
			padding: 0.4rem;
			gap: 0.4rem;
		}

		:global(.card-art) {
			max-height: 7.5rem;
			object-fit: contain;
		}

		:global(.description) {
			min-height: 0;
			font-size: 0.68rem;
			line-height: 1.25;
		}

		:global(.price) {
			font-size: 0.9rem;
		}

		:global(.title) {
			font-size: 0.85rem;
			line-height: 1.1;
		}
	}

	// very narrow phones: stack to one column
	@media (max-width: 340px) {
		.cards-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
