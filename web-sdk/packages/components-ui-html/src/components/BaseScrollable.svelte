<script lang="ts">
	import type { Snippet } from 'svelte';

	type Element = null | HTMLDivElement;

	type Props = {
		type: 'column' | 'row';
		noScroll?: boolean;
		/** Take leftover space in a fit popup so copy scrolls, chrome stays. */
		grow?: boolean;
		children: Snippet<[{ element: Element }]>;
	};

	let element = $state(null as Element);

	const props: Props = $props();
</script>

<div
	bind:this={element}
	class="content {props.type}"
	class:scrollX={!props.noScroll && props.type === 'row'}
	class:scrollY={!props.noScroll && props.type === 'column'}
	class:grow={props.grow}
>
	{@render props.children({ element })}
</div>

<style lang="scss">
	.content {
		position: relative;
		text-align: center;
		display: flex;
		gap: 1rem;

		&.column {
			flex-direction: column;
			align-items: center;
			max-height: 100%;
		}

		&.row {
			flex-direction: row;
			justify-content: center;
			max-width: 100%;
		}

		&.grow {
			flex: 1 1 auto;
			min-height: 0;
			width: 100%;
		}
	}
</style>
