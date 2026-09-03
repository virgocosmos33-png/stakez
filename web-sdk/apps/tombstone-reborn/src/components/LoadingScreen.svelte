<script lang="ts">
	import { getContext } from '../game/context';
	import IntroCarousel from './IntroCarousel.svelte';

	type Props = {
		onloaded: () => void;
	};

	const props: Props = $props();
	const context = getContext();
	const ready = $derived(Boolean(context.stateApp.loaded));
</script>

<IntroCarousel {ready} oncontinue={props.onloaded} />
