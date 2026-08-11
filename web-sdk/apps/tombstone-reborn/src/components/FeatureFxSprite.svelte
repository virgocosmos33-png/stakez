<script lang="ts">
	/**
	 * One frame from the tombstone_feature_vfx atlas (see game/featureVfx.ts).
	 */
	import * as PIXI from 'pixi.js';
	import { BaseSprite, getContextApp } from 'pixi-svelte';

	import { FEATURE_VFX_ASSET } from '../game/featureVfx';

	type Props = {
		tex: number;
		x?: number;
		y?: number;
		width?: number;
		height?: number;
		rotation?: number;
		alpha?: number;
		tint?: number;
		blendMode?: PIXI.BLEND_MODES;
	};

	const props: Props = $props();
	const appContext = getContextApp();
	const frames = $derived(
		(appContext.stateApp.loadedAssets?.[FEATURE_VFX_ASSET] as PIXI.Texture[] | undefined) ?? [],
	);
	const texture = $derived(
		frames[Math.min(Math.max(props.tex, 0), Math.max(frames.length - 1, 0))],
	);
</script>

{#if texture && (props.alpha ?? 1) > 0.004}
	<BaseSprite
		{texture}
		anchor={0.5}
		x={props.x ?? 0}
		y={props.y ?? 0}
		width={props.width ?? 64}
		height={props.height ?? 64}
		rotation={props.rotation ?? 0}
		alpha={props.alpha ?? 1}
		tint={props.tint ?? 0xffffff}
		blendMode={props.blendMode ?? 'normal'}
	/>
{/if}
