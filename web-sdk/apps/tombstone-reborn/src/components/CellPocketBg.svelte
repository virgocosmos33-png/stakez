<script lang="ts">
	/**
	 * Static cell-pocket plate. Never on the Spine / win-grow transform.
	 * Never inside the T-clip — only the face uses that mask.
	 *
	 * Both user plates are 1024x1536 with a dark letterbox. Stretching the
	 * whole file puts that black on the hat / letter row. Use the mid band.
	 */
	import * as PIXI from 'pixi.js';
	import { BaseSprite, getContextApp } from 'pixi-svelte';

	import { SYMBOL_CARD_H, SYMBOL_CARD_W } from '../game/constants';
	import { getRowPitch } from '../game/utils';
	import { slotFrameHole } from '../game/slotFrame';

	const PLATE_UV = { x0: 0.08, y0: 0.26, x1: 0.92, y1: 0.74 };

	const props: { assetKey: string; reelIndex?: number; x?: number; y?: number } = $props();
	const hole = $derived(slotFrameHole(getRowPitch(props.reelIndex ?? 0)));
	const app = getContextApp();
	let plateTex = $state<PIXI.Texture>(PIXI.Texture.EMPTY);

	$effect(() => {
		const base = app.stateApp.loadedAssets?.[props.assetKey] as PIXI.Texture | undefined;
		if (!base || base === PIXI.Texture.EMPTY || base.width < 2) {
			plateTex = PIXI.Texture.EMPTY;
			return;
		}
		const f = base.frame;
		const tex = new PIXI.Texture({
			source: base.source,
			frame: new PIXI.Rectangle(
				f.x + f.width * PLATE_UV.x0,
				f.y + f.height * PLATE_UV.y0,
				f.width * (PLATE_UV.x1 - PLATE_UV.x0),
				f.height * (PLATE_UV.y1 - PLATE_UV.y0),
			),
		});
		plateTex = tex;
		return () => {
			if (plateTex === tex) plateTex = PIXI.Texture.EMPTY;
			tex.destroy(false);
		};
	});
</script>

<BaseSprite
	texture={plateTex}
	anchor={0.5}
	x={props.x ?? 0}
	y={props.y ?? 0}
	width={props.reelIndex === undefined ? SYMBOL_CARD_W : hole.w}
	height={props.reelIndex === undefined ? SYMBOL_CARD_H : hole.h}
	blendMode="normal"
	eventMode="none"
/>
