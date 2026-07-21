<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Container, Graphics, getContextParent } from 'pixi-svelte';
	import { stateUi } from 'state-shared';

	import { getContext } from '../game/context';
	import { stateShake } from '../game/stateShake.svelte';

	const context = getContext();
	// the pixi-svelte parent container (this component's <MainContainer>); we
	// attach a raw PIXI.NineSliceSprite to it because pixi-svelte has no
	// NineSlice component (same escape hatch <Graphics>/<Sprite> use internally).
	const parentContext = getContextParent();

	// The ornate gold frame is rendered as a nine-slice (the WebGL equivalent of
	// CSS `border-image`): ONE texture (mirror_frame_wide.png, 1213x892) cut into
	// 4 fixed corners + 4 stretchable edges + a stretchable centre. The corners
	// keep their crisp ornament at any size; the top/bottom + left/right moldings
	// stretch along the board's live width AND height, so the frame hugs all four
	// sides at every aspect ratio (the fixed-aspect single-sprite was the bug).
	//
	// Insets (texture px) measured from the art (tools/measure_frame_nineslice.py
	// + profile_frame_depth.py): the ornate CORNER turn reaches ~130x135 in from
	// each corner, so a 140px inset fully contains every corner while leaving only
	// the flat black interior in the stretchable centre.
	const INSET = 140;
	// where the gold molding meets the black interior (texture px): the side rails
	// are ~58 deep, the top/bottom rails ~101. Used to sit the gold's INNER edge
	// just outside the reels on every side.
	const GOLD_INNER_X = 58;
	const GOLD_INNER_Y = 101;
	// The ornate art is intrinsically bulky, so we render the nine-slice UNIFORMLY
	// downscaled: corners + edge moldings shrink together (no distortion) to a
	// slim, elegant gold trim rather than a heavy slab. Tuned visually: at 0.34
	// the side rail reads ~20px and the corner ornament ~48px in board-space.
	const FRAME_SCALE = 0.34;
	// gap (board-space px) between the reels and the gold's INNER edge, so the
	// trim hugs the grid tightly with a small consistent breathing margin
	const GAP = 6;
	// dark recess matte: a board-shaped fill behind the reels so nothing leaks
	// through the frame opening (kept from the previous implementation)
	const BACKING = 1.0;

	const texture = $derived(
		(context.stateApp.loadedAssets?.['mirrorFrame'] as PIXI.Texture | undefined) ??
			PIXI.Texture.EMPTY,
	);

	const bw = $derived(context.stateGameDerived.boardLayout().width);
	const bh = $derived(context.stateGameDerived.boardLayout().height);
	const frameX = $derived(context.stateGameDerived.boardLayout().x + stateShake.x);
	const frameY = $derived(context.stateGameDerived.boardLayout().y + stateShake.y);
	const backW = $derived(bw * BACKING);
	const backH = $derived(bh * BACKING);

	// Responsive sizing. The frame is downscaled by FRAME_SCALE, so the gold
	// molding's rendered depth is GOLD_INNER_*·FRAME_SCALE. We size the RENDERED
	// outer box so the gold inner edge lands GAP px outside the reels on every
	// side, then divide by the scale to get the geometry (local) size the
	// nine-slice needs. Because we drive both live board width AND height, the
	// trim hugs all four sides at any aspect ratio; the small, fixed outward
	// extent (≈ GAP + gold·scale ≈ 26–40px) keeps the whole frame on-screen.
	const s = FRAME_SCALE;
	const outerW = $derived(bw + 2 * GAP + 2 * GOLD_INNER_X * s); // rendered px
	const outerH = $derived(bh + 2 * GAP + 2 * GOLD_INNER_Y * s); // rendered px
	const geoW = $derived(outerW / s); // nine-slice geometry (local) width
	const geoH = $derived(outerH / s); // nine-slice geometry (local) height

	// assets are fully loaded before this component mounts (the loading screen
	// gates the board), so the texture is already available at init
	const nineSlice = new PIXI.NineSliceSprite({
		texture:
			(context.stateApp.loadedAssets?.['mirrorFrame'] as PIXI.Texture | undefined) ??
			PIXI.Texture.EMPTY,
		leftWidth: INSET,
		topHeight: INSET,
		rightWidth: INSET,
		bottomHeight: INSET,
	});
	nineSlice.eventMode = 'none';
	nineSlice.zIndex = -3; // behind the reels (and behind the matte), like the old frame
	parentContext.addToParent(nineSlice);

	$effect(() => {
		if (nineSlice.texture !== texture) nineSlice.texture = texture;
		// uniform downscale keeps corners + edges undistorted at a slim size
		nineSlice.scale.set(s);
		nineSlice.width = geoW;
		nineSlice.height = geoH;
		// NineSliceSprite origin is top-left; scale expands from it, so the
		// rendered box is [x, x + geo·s] -> offset by the RENDERED half-size
		nineSlice.x = frameX - outerW / 2;
		nineSlice.y = frameY - outerH / 2;
	});

	// Publish the frame's OUTER width (in main-layout design px) so the shared
	// bottom HUD can fit its control row to exactly this width. This is the same
	// value the nine-slice renders, so the HUD tracks the frame automatically at
	// every screen size (single source of truth, no duplicated constants).
	$effect(() => {
		stateUi.boardFrameWidth = outerW;
	});
</script>

<!-- dark recess behind the reels — a board-shaped matte so no light/gold leaks
	through the frame opening; sized to the board so it never covers the gold -->
<Container x={frameX} y={frameY} zIndex={-2}>
	<Graphics
		draw={(g: import('pixi.js').Graphics) => {
			g.clear();
			g.roundRect(-backW / 2, -backH / 2, backW, backH, Math.min(backW, backH) * 0.05);
			g.fill({ color: 0x0a090c, alpha: 1 });
		}}
	/>
</Container>
