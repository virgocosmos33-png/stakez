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
		/* --ui-title-font lets a game brand modal headings with a display face
		   while modal body copy stays on --mono-font. Undefined by default, so
		   this resolves to --mono-font exactly as before. */
		font-family: var(--ui-title-font, var(--mono-font, 'Segoe UI', Arial, sans-serif));
		font-weight: 700;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		font-size: 1.4rem;
		color: var(--mono-fg, #ffffff);
	}
</style>
