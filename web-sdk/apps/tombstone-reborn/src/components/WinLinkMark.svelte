<script lang="ts">
	/**
	 * Paying-way mark. Rim / wash stay UNDER the reels. The scan wipe
	 * sits OVER idle plates and faces. Win spines rise after the band hides.
	 */
	import BoardSpace from './BoardSpace.svelte';
	import WinLinkFx from './WinLinkFx.svelte';

	type Props = { layer: 'rim' | 'wipe' };
	const props: Props = $props();
</script>

<BoardSpace>
	<WinLinkFx layer={props.layer} />
</BoardSpace>
