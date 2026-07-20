<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		children: Snippet;
	};

	const props: Props = $props();
</script>

<div class="ui-modal-title-wrap">
	{@render props.children()}
</div>

<style lang="scss">
	.ui-modal-title-wrap {
		text-align: center;
		font-family: 'Cinzel', Georgia, serif;
		font-weight: 900;
		letter-spacing: 0.05em;
		font-size: 1.55rem;
		color: #f4ecd8;
		text-shadow:
			0 0 12px rgba(255, 193, 46, 0.35),
			0 2px 4px rgba(0, 0, 0, 0.75);
	}
</style>
