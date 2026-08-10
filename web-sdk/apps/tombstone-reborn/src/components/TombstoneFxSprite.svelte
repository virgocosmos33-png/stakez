<script lang="ts">
	/**
	 * One frame from the Kenney-derived tombstone_split_vfx atlas.
	 */
	import * as PIXI from 'pixi.js';
	import { BaseSprite, getContextApp } from 'pixi-svelte';
	import { TOMBSTONE_SPLIT_VFX_ASSET } from '../game/tombstoneVfx';

	type Props = {
		tex: number;
		x?: number;
		y?: number;
		width?: number;
		height?: number;
		rotation?: number;
		alpha?: number;
	};

	const props: Props = $props();
	const appContext = getContextApp();
	const frames = $derived(
		(appContext.stateApp.loadedAssets?.[TOMBSTONE_SPLIT_VFX_ASSET] as PIXI.Texture[] | undefined) ??
			[],
	);
	const texture = $derived(
		frames[Math.min(Math.max(props.tex, 0), Math.max(frames.length - 1, 0))],
	);
</script>

{#if texture}
	<BaseSprite
		{texture}
		anchor={0.5}
		x={props.x ?? 0}
		y={props.y ?? 0}
		width={props.width ?? 64}
		height={props.height ?? 64}
		rotation={props.rotation ?? 0}
		alpha={props.alpha ?? 1}
	/>
{/if}
