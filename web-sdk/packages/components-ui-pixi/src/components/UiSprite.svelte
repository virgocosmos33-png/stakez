<script lang="ts" module>
	import { Rectangle, type RectangleProps } from 'pixi-svelte';

	export type Props = RectangleProps;
</script>

<script lang="ts">
	const props: Props = $props();
	// NLC-style chrome: fully circular buttons (pills when not square) with a
	// subtle light rim over a translucent dark fill
	const radius = $derived(Math.min(Number(props.width) || 100, Number(props.height) || 100) / 2);
</script>

<Rectangle
	borderRadius={radius}
	backgroundAlpha={0.72}
	borderColor={0xffffff}
	borderAlpha={0.28}
	borderWidth={3}
	{...props}
/>

<!-- ADD YOUR DESIGN -->

<!-- <script lang="ts" module>
	import { Sprite, type SpriteProps } from 'pixi-svelte';
	import type { sharedAssetsPixi } from 'constants-shared/assets';

	export type Props = SpriteProps & {
		key: keyof typeof sharedAssetsPixi;
	};
</script>

<script lang="ts">
	const props: Props = $props();
</script>

<Sprite {...props} /> -->
