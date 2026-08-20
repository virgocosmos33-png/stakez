<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		maxWidth: '100%' | '500px';
		/** Cap to the overlay and scroll internally (confirm / long copy). */
		fit?: boolean;
		children: Snippet;
	};

	const props: Props = $props();
</script>

<div
	class="ui-popup-standard-content-wrap"
	class:fit={props.fit}
	style="--maxWidth: {props.maxWidth}; --zIndex: {100}"
>
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

	.fit {
		box-sizing: border-box;
		font-size: 16px;
		width: min(var(--maxWidth), 100%);
		max-height: 100%;
		min-height: 0;
		overflow: hidden;
		justify-content: flex-start;
		padding: 1.15rem 1.2rem 1.1rem;
	}

	@media (max-width: 480px) {
		.fit {
			padding: 0.9rem 0.85rem 0.85rem;
			gap: 0.75rem;
			border-radius: 14px;
		}
	}

	@media (max-height: 560px) {
		.fit {
			padding: 0.7rem 0.8rem 0.7rem;
			gap: 0.55rem;
		}
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
