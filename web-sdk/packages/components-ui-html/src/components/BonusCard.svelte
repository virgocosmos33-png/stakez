<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		title: Snippet;
		description: Snippet;
		price: Snippet;
		button: Snippet;
	};

	const props: Props = $props();
</script>

<div class="bonus-card-wrap">
	<div class="info">
		{@render props.title()}
		{@render props.description()}
		{@render props.price()}
	</div>
	{@render props.button()}
</div>

<style lang="scss">
	.bonus-card-wrap {
		box-sizing: border-box;
		padding: 0.5rem;
		flex-direction: column;
		display: flex;
		justify-content: space-between;

		border-radius: 10px;
		background: rgba(0, 0, 0, 0.5);
		text-align: left;
		// desktop strip default; mobile wraps override via :global
		flex: 0 0 auto;
		width: 168px;
		min-width: 140px;
		max-width: 200px;
		gap: 0.5rem;
	}

	.info {
		display: flex;
		flex-direction: column;
		gap: 0.5em;
	}
</style>
