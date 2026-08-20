<script lang="ts">
	import type { Snippet } from 'svelte';

	import UIDefault from './UIDefault.svelte';

	type Props = {
		gameName: Snippet;
		logo: Snippet;
	};

	const props: Props = $props();
</script>

<!-- Replay used to swap UIReplay (hardcoded WIN/BET stacks). That chrome
	does not match LayoutDesktop / LayoutPortrait, so Stake event replay
	looked broken. Live play and replay share this HUD. -->
<UIDefault>
	{#snippet gameName()}
		{@render props.gameName()}
	{/snippet}

	{#snippet logo()}
		{@render props.logo()}
	{/snippet}
</UIDefault>
