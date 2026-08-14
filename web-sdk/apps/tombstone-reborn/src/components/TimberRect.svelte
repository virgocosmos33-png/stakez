<script lang="ts">
	/**
	 * Rectangle timber outline — the SAME parts as the board staircase
	 * (`boardWoodField` planks + `boardCornerBracket` plates). Inner pocket is
	 * {x,y,w,h}; planks sit fully outside it at `thick`, iron plates on the
	 * corners. Optional fill so the scene does not show through the panel —
	 * that fill is the original near-black rail planks (`barRail` inner field),
	 * never the outline timber. The fill sprite stays mounted from the first
	 * frame so it cannot jump in front of the plaques.
	 */
	import * as PIXI from 'pixi.js';
	import { BaseSprite, Sprite, getContextApp } from 'pixi-svelte';

	import { BAR_RAIL_POCKET } from '../game/constants';

	type Props = {
		x: number;
		y: number;
		w: number;
		h: number;
		thick: number;
		corner: number;
		fill?: boolean;
	};

	const props: Props = $props();
	const appContext = getContextApp();

	let pocketTexture = $state<PIXI.Texture>(PIXI.Texture.EMPTY);

	$effect(() => {
		if (!props.fill) {
			pocketTexture = PIXI.Texture.EMPTY;
			return;
		}
		const base = appContext.stateApp.loadedAssets?.['barRail'] as PIXI.Texture | undefined;
		if (!base || base === PIXI.Texture.EMPTY || base.width < 2) {
			pocketTexture = PIXI.Texture.EMPTY;
			return;
		}
		const f = base.frame;
		const tex = new PIXI.Texture({
			source: base.source,
			frame: new PIXI.Rectangle(
				f.x + f.width * BAR_RAIL_POCKET.x0,
				f.y + f.height * BAR_RAIL_POCKET.y0,
				f.width * (BAR_RAIL_POCKET.x1 - BAR_RAIL_POCKET.x0),
				f.height * (BAR_RAIL_POCKET.y1 - BAR_RAIL_POCKET.y0),
			),
		});
		pocketTexture = tex;
		return () => {
			if (pocketTexture === tex) pocketTexture = PIXI.Texture.EMPTY;
			tex.destroy(false);
		};
	});

	const beams = $derived.by(() => {
		const { x, y, w, h, thick } = props;
		const innerLeft = x;
		const innerRight = x + w;
		const innerTop = y;
		const innerBot = y + h;
		return {
			top: {
				cx: (innerLeft + innerRight) / 2,
				cy: innerTop - thick / 2,
				len: w + 2 * thick,
			},
			bot: {
				cx: (innerLeft + innerRight) / 2,
				cy: innerBot + thick / 2,
				len: w + 2 * thick,
			},
			left: {
				cx: innerLeft - thick / 2,
				cy: (innerTop + innerBot) / 2,
				len: h + 2 * thick,
			},
			right: {
				cx: innerRight + thick / 2,
				cy: (innerTop + innerBot) / 2,
				len: h + 2 * thick,
			},
			cTL: { cx: innerLeft - thick / 2, cy: innerTop - thick / 2 },
			cTR: { cx: innerRight + thick / 2, cy: innerTop - thick / 2 },
			cBL: { cx: innerLeft - thick / 2, cy: innerBot + thick / 2 },
			cBR: { cx: innerRight + thick / 2, cy: innerBot + thick / 2 },
		};
	});
</script>

{#if props.fill}
	<BaseSprite
		texture={pocketTexture}
		x={props.x + props.w / 2}
		y={props.y + props.h / 2}
		anchor={0.5}
		width={props.w}
		height={props.h}
		eventMode="none"
	/>
{/if}

<Sprite
	key="boardWoodField"
	anchor={0.5}
	rotation={Math.PI / 2}
	x={beams.top.cx}
	y={beams.top.cy}
	width={props.thick}
	height={beams.top.len}
	eventMode="none"
/>
<Sprite
	key="boardWoodField"
	anchor={0.5}
	rotation={Math.PI / 2}
	x={beams.bot.cx}
	y={beams.bot.cy}
	width={props.thick}
	height={beams.bot.len}
	eventMode="none"
/>
<Sprite
	key="boardWoodField"
	anchor={0.5}
	x={beams.left.cx}
	y={beams.left.cy}
	width={props.thick}
	height={beams.left.len}
	eventMode="none"
/>
<Sprite
	key="boardWoodField"
	anchor={0.5}
	x={beams.right.cx}
	y={beams.right.cy}
	width={props.thick}
	height={beams.right.len}
	eventMode="none"
/>

<Sprite
	key="boardCornerBracket"
	anchor={0.5}
	x={beams.cTL.cx}
	y={beams.cTL.cy}
	width={props.corner}
	height={props.corner}
	eventMode="none"
/>
<Sprite
	key="boardCornerBracket"
	anchor={0.5}
	x={beams.cTR.cx}
	y={beams.cTR.cy}
	width={props.corner}
	height={props.corner}
	eventMode="none"
/>
<Sprite
	key="boardCornerBracket"
	anchor={0.5}
	x={beams.cBL.cx}
	y={beams.cBL.cy}
	width={props.corner}
	height={props.corner}
	eventMode="none"
/>
<Sprite
	key="boardCornerBracket"
	anchor={0.5}
	x={beams.cBR.cx}
	y={beams.cBR.cy}
	width={props.corner}
	height={props.corner}
	eventMode="none"
/>
