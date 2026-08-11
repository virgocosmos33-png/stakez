<script lang="ts">
	/**
	 * One gunpowder detonation on a high-multiplier split cell.
	 * Atlas: tools/make_split_explosion_atlas.py → asset key `splitExplosion`.
	 * Frame order / rate is the contract in src/game/splitExplosion.ts.
	 *
	 * A one-shot flipbook: it plays once from `born`, driven by the parent's live
	 * `now` clock (no internal ticker — the parent already runs one), grows a touch
	 * for punch, and fades out on its last frames so it clears the cell instead of
	 * freezing on the final smoke.
	 */
	import * as PIXI from 'pixi.js';
	import { BaseSprite, getContextApp } from 'pixi-svelte';

	import {
		SPLIT_EXPLOSION_ASSET,
		EXPLOSION_FRAME_COUNT,
		EXPLOSION_FPS,
	} from '../game/splitExplosion';

	type Props = {
		x: number;
		y: number;
		/** performance.now() when the cell detonated */
		born: number;
		/** live clock (ms) from the parent */
		now: number;
		/** drawn width/height of the blast */
		size: number;
	};

	const props: Props = $props();

	const appContext = getContextApp();
	const frames = $derived(
		(appContext.stateApp.loadedAssets?.[SPLIT_EXPLOSION_ASSET] as PIXI.Texture[] | undefined) ?? [],
	);

	const ageMs = $derived(Math.max(0, props.now - props.born));
	const frameIndex = $derived(Math.floor((ageMs / 1000) * EXPLOSION_FPS));
	const done = $derived(frameIndex >= EXPLOSION_FRAME_COUNT || frames.length === 0);
	const texture = $derived(
		done ? undefined : frames[Math.min(frameIndex, frames.length - 1)],
	);

	/** 0..1 across the whole blast, for the grow + fade. */
	const life = $derived(Math.min(1, frameIndex / EXPLOSION_FRAME_COUNT));
	// a hard punch out of nothing, then ease; fades over the last third as the
	// smoke thins so the cell is readable again for the badge/settle
	const scale = $derived(props.size * (0.85 + 0.4 * life));
	const alpha = $derived(life > 0.66 ? Math.max(0, 1 - (life - 0.66) / 0.34) : 1);
</script>

{#if texture}
	<BaseSprite
		{texture}
		anchor={0.5}
		x={props.x}
		y={props.y}
		width={scale}
		height={scale}
		{alpha}
	/>
{/if}
