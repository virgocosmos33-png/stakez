<script lang="ts">
	import type { Snippet } from 'svelte';

	import BaseContent from './BaseContent.svelte';
	import BaseScrollable from './BaseScrollable.svelte';

	type Props = {
		betAmount: Snippet;
		bonusCardsActivate: Snippet;
		bonusCardsBuy: Snippet;
	};

	const props: Props = $props();
</script>

<BaseContent maxWidth="100%">
	{@render props.betAmount()}

	<BaseScrollable type="column">
		<!-- one horizontally scrollable strip: ante + feature spins + bonus buys.
			The inner row shrink-wraps with auto margins, so it stays centred when
			everything fits and scrolls from the left edge when it does not. -->
		<div class="bonuses-strip">
			<div class="bonuses-row">
				{@render props.bonusCardsActivate()}
				{@render props.bonusCardsBuy()}
			</div>
		</div>
	</BaseScrollable>
</BaseContent>

<style lang="scss">
	.bonuses-strip {
		max-width: min(94vw, 1500px);
		overflow-x: auto;
		overflow-y: hidden;
		padding-bottom: 0.75rem;
		scrollbar-width: thin;
		scrollbar-color: rgba(255, 255, 255, 0.35) transparent;
	}

	.bonuses-row {
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		gap: 1rem;
		width: max-content;
		margin: 0 auto;
	}
</style>
