<script lang="ts">
	/**
	 * Shared board transform for every overlay that positions in board-local
	 * space (cell centres from getSymbolX / getCellCenterY).
	 *
	 * BoardContainer / BoardPlate already scale around the same pivot. Overlays
	 * that used `origin = board.x - width/2` desync the moment the expanded
	 * board shrinks to fit under the HUD — this wrapper is the single fix.
	 */
	import type { Snippet } from 'svelte';
	import { Container } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { stateShake } from '../game/stateShake.svelte';

	type Props = {
		children: Snippet;
		/** extra main-space Y (feature fall-out, etc.) */
		yOffset?: number;
	};

	const props: Props = $props();
	const context = getContext();
	const layout = $derived(context.stateGameDerived.boardLayout());
</script>

<Container
	x={layout.x + stateShake.x}
	y={layout.y + stateShake.y + (props.yOffset ?? 0)}
	pivot={layout.pivot}
	scale={layout.scale}
>
	{@render props.children()}
</Container>
