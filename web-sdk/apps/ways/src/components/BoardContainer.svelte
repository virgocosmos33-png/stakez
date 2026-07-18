<script lang="ts">
	import type { Snippet } from 'svelte';

	import { Container } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { stateShake } from '../game/stateShake.svelte';

	type Props = {
		children: Snippet;
	};

	const props: Props = $props();

	const context = getContext();
</script>

<Container
	x={context.stateGameDerived.boardLayout().x + stateShake.x}
	y={context.stateGameDerived.boardLayout().y + stateShake.y}
	pivot={context.stateGameDerived.boardLayout().pivot}
>
	{@render props.children()}
</Container>
