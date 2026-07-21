<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		/** false → whole card is greyed out + non-interactive (unaffordable) */
		affordable?: boolean;
		title: Snippet;
		description: Snippet;
		price: Snippet;
		button: Snippet;
	};

	const { affordable = true, title, description, price, button }: Props = $props();
</script>

<div class="bonus-card-wrap" class:greyed={!affordable}>
	<div class="info">
		{@render title()}
		{@render description()}
		{@render price()}
	</div>
	{@render button()}
</div>

<style lang="scss">
	.bonus-card-wrap {
		box-sizing: border-box;
		padding: 0.5rem;
		flex-direction: column;
		display: flex;
		justify-content: space-between;

		border-radius: var(--mono-radius-sm, 8px);
		background: var(--mono-bg, #10161d);
		border: 1px solid var(--mono-hairline, #2a3542);
		text-align: left;
		// desktop strip default; mobile wraps override via :global
		flex: 0 0 auto;
		width: 168px;
		min-width: 140px;
		max-width: 200px;
		gap: 0.5rem;

		transition:
			opacity 0.18s ease,
			filter 0.18s ease;
	}

	// unaffordable → desaturate the whole card (art, title, price, button),
	// dim it, and take it out of the interaction flow. Reactive to bet/balance.
	.bonus-card-wrap.greyed {
		filter: grayscale(1);
		opacity: 0.45;
		pointer-events: none;
	}

	.info {
		display: flex;
		flex-direction: column;
		gap: 0.5em;
	}
</style>
