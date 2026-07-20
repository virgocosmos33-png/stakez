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
		background: linear-gradient(180deg, rgba(26, 23, 32, 0.96), rgba(9, 8, 12, 0.98));
		border: 1px solid rgba(201, 154, 63, 0.55);
		box-shadow:
			0 12px 44px rgba(0, 0, 0, 0.7),
			inset 0 1px 0 rgba(246, 228, 166, 0.15);
	}

	// thin inner gold hairline for the framed, "designed" look
	.ui-popup-standard-content-wrap::before {
		content: '';
		position: absolute;
		inset: 5px;
		border-radius: 12px;
		border: 1px solid rgba(201, 154, 63, 0.18);
		pointer-events: none;
	}
</style>
