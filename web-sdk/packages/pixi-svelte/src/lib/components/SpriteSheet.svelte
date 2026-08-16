<script lang="ts" module>
	import { type Props as BaseProps } from './AnimatedSprite.svelte';

	export type Props = Omit<BaseProps, 'textures'> & { key: string };
</script>

<script lang="ts">
	import AnimatedSprite from './AnimatedSprite.svelte';
	import { getContextApp } from '../context.svelte';
	import type { LoadedSpriteSheet } from '../types';

	const context = getContextApp();

	const { key, ...animateSpriteProps }: Props = $props();
	const textures = $derived(context.stateApp.loadedAssets?.[key] as LoadedSpriteSheet);
	const isValid = $derived(textures && 'length' in textures);
</script>

{#if isValid}
	<AnimatedSprite {...animateSpriteProps} textures={textures} />
{/if}
