<script lang="ts" module>
	import * as PIXI from 'pixi.js';

	/**
	 * One patient's hand, posed.
	 *
	 * The art is nine textures baked by tools/make_claw_atlas.py — the same hand
	 * open, through seven stages of closing, to a clench — all pinned on the
	 * wrist. This component picks the two poses either side of `curl` and
	 * cross-fades them, so the fingers move continuously off nine images.
	 *
	 * Everything else (where it is, how big, how rotated, how faded) is the
	 * caller's business and is expected to change every rendered frame. That is
	 * the whole point: motion is never baked, so it runs at the display's
	 * refresh rate rather than at some sheet's frame rate.
	 *
	 * Used by SplitPanes (drag down and tear), CloneMorph (press flat and stamp)
	 * and StretchFx (grip top and bottom and pull apart).
	 */

	// straight out of the bake script's printed output
	const TEX_W = 384;
	const TEX_H = 448;
	const HAND_H_IN_TEX = 340;
	/** where the wrist sits in the texture — also the anchor, so the hand pivots
		at the wrist and swapping poses never makes it jump */
	export const CLAW_WRIST = { x: 0.5, y: 0.92411 };

	export const CLAW_ASSET_KEY = 'splitClaw';

	/** texture pixels -> screen pixels, for a given on-screen open-hand height */
	const scaleFor = (handH: number) => handH / HAND_H_IN_TEX;

	/**
	 * How far the fingertips reach from the wrist, as a fraction of the open
	 * hand's height. A clenched hand is much shorter, which is what makes a
	 * closing hand read as digging in rather than sliding.
	 */
	export const clawReach = (curl: number) => 1 - 0.54 * Math.min(Math.max(curl, 0), 1);
</script>

<script lang="ts">
	import { BaseSprite, getContextApp } from 'pixi-svelte';

	type Props = {
		/** 0 = flat open hand, 1 = clenched fist */
		curl: number;
		/** wrist position, in the parent container's coordinates */
		x: number;
		y: number;
		/** on-screen height of the OPEN hand; posed hands come out shorter */
		handH: number;
		scale?: number;
		/** radians, about the wrist */
		roll?: number;
		alpha?: number;
		tint?: number;
		/** point the fingers DOWN instead of up (a hand reaching in from above) */
		flip?: boolean;
	};

	const props: Props = $props();

	const appContext = getContextApp();
	const poses = $derived(
		(appContext.stateApp.loadedAssets?.[CLAW_ASSET_KEY] as PIXI.Texture[] | undefined) ?? [],
	);

	const slot = $derived(Math.min(Math.max(props.curl, 0), 1) * (poses.length - 1));
	const low = $derived(Math.floor(slot));
	const high = $derived(Math.min(low + 1, poses.length - 1));
	const blend = $derived(slot - low);

	const shared = $derived({
		anchor: CLAW_WRIST,
		x: props.x,
		y: props.y,
		width: TEX_W * scaleFor(props.handH) * (props.scale ?? 1),
		height: TEX_H * scaleFor(props.handH) * (props.scale ?? 1),
		rotation: (props.roll ?? 0) + (props.flip ? Math.PI : 0),
		tint: props.tint ?? 0xffffff,
	});

	const alpha = $derived(props.alpha ?? 1);
</script>

{#if poses.length}
	<BaseSprite {...shared} texture={poses[low]} alpha={alpha * (1 - blend)} />
	{#if blend > 0.001 && high !== low}
		<BaseSprite {...shared} texture={poses[high]} alpha={alpha * blend} />
	{/if}
{/if}
