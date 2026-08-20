<script lang="ts">
	/**
	 * One blood burst on a split seam. Plays the splitBlood flipbook once from
	 * `born`, then freezes on the last wound frame so the gash stays in the cut.
	 */
	import * as PIXI from 'pixi.js';
	import { BaseSprite, getContextApp } from 'pixi-svelte';

	import {
		SPLIT_BLOOD_ASSET,
		BLOOD_FRAME_COUNT,
		BLOOD_FPS,
	} from '../game/splitBlood';

	type Props = {
		x?: number;
		y: number;
		born: number;
		now: number;
		width: number;
		height: number;
	};

	const props: Props = $props();

	const appContext = getContextApp();
	const frames = $derived(
		(appContext.stateApp.loadedAssets?.[SPLIT_BLOOD_ASSET] as PIXI.Texture[] | undefined) ?? [],
	);

	const ageMs = $derived(Math.max(0, props.now - props.born));
	const frameIndex = $derived(
		Math.min(BLOOD_FRAME_COUNT - 1, Math.floor((ageMs / 1000) * BLOOD_FPS)),
	);
	const texture = $derived(frames[frameIndex]);
	const punch = $derived(Math.min(1, frameIndex / 3));
	const scale = $derived(0.88 + 0.14 * punch);
</script>

{#if texture}
	<BaseSprite
		{texture}
		anchor={0.5}
		x={props.x ?? 0}
		y={props.y}
		width={props.width * scale}
		height={props.height * scale}
	/>
{/if}
