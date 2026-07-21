<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		maxWidth: '100%' | '500px';
		children: Snippet;
	};

	const props: Props = $props();
</script>

<div class="ui-popup-standard-content-wrap" style="--maxWidth: {props.maxWidth}; --zIndex: {100}">
	{@render props.children()}
</div>

<style lang="scss">
	.ui-popup-standard-content-wrap {
		position: relative;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		z-index: var(--zIndex);
		max-width: var(--maxWidth);
		gap: 1rem;
		padding: 1.5rem 1.6rem;
		border-radius: 16px;
		background: linear-gradient(180deg, #131a22, #0b0f14);
		border: 1px solid var(--mono-hairline, #2a3542);
		box-shadow:
			0 12px 44px rgba(0, 0, 0, 0.7),
			inset 0 1px 0 rgba(255, 255, 255, 0.04);
	}

	// thin inner hairline for the framed, "command-center" look
	.ui-popup-standard-content-wrap::before {
		content: '';
		position: absolute;
		inset: 5px;
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.05);
		pointer-events: none;
	}
</style>
