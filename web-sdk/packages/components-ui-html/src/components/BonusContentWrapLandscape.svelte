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

<!-- Phone / tablet landscape: bet on the left, horizontal snap-scroll of cards. -->
<div class="sheet">
	<div class="bet-col">
		{@render props.betAmount()}
	</div>

	<div class="cards-scroll">
		<div class="cards-row">
			{@render props.bonusCardsActivate()}
			{@render props.bonusCardsBuy()}
		</div>
	</div>
</div>

<style lang="scss">
	.sheet {
		box-sizing: border-box;
		width: min(96vw, 1100px);
		max-height: min(88dvh, 520px);
		display: flex;
		flex-direction: row;
		align-items: stretch;
		gap: 0.75rem;
		padding: 0.85rem 0.9rem;
		margin: 0.4rem;
		border-radius: 16px;
		background: linear-gradient(180deg, rgba(26, 23, 32, 0.96), rgba(9, 8, 12, 0.98));
		border: 1px solid rgba(201, 154, 63, 0.55);
		box-shadow:
			0 12px 44px rgba(0, 0, 0, 0.7),
			inset 0 1px 0 rgba(246, 228, 166, 0.15);
	}

	.bet-col {
		flex: 0 0 auto;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0.4rem 0.55rem;
		border-radius: 12px;
		background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(0, 0, 0, 0.35));
		border: 1px solid rgba(201, 154, 63, 0.35);
	}

	.cards-scroll {
		flex: 1 1 auto;
		min-width: 0;
		overflow-x: auto;
		overflow-y: hidden;
		-webkit-overflow-scrolling: touch;
		overscroll-behavior-x: contain;
		scroll-snap-type: x proximity;
		padding-bottom: 0.25rem;
		scrollbar-width: thin;
		scrollbar-color: #c99a3f rgba(255, 255, 255, 0.06);

		&::-webkit-scrollbar {
			height: 6px;
		}
		&::-webkit-scrollbar-thumb {
			background: linear-gradient(90deg, #e9c877, #c99a3f);
			border-radius: 999px;
		}
	}

	.cards-row {
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		align-items: stretch;
		gap: 0.65rem;
		width: max-content;
		height: 100%;
		padding: 0.1rem 0.15rem;

		:global(.bonus-card-wrap) {
			flex: 0 0 auto;
			width: min(42vw, 200px);
			max-width: 200px;
			min-width: 150px;
			height: 100%;
			max-height: calc(88dvh - 2.5rem);
			scroll-snap-align: start;
		}

		:global(.description) {
			min-height: 0;
			font-size: 0.7rem;
			line-height: 1.25;
		}

		:global(.card-art) {
			max-height: 6.5rem;
			object-fit: contain;
		}
	}
</style>
