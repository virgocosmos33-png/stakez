<script lang="ts" module>
	import * as PIXI from 'pixi.js';
	import { type RectangleProps } from 'pixi-svelte';

	export type UiTone = 'dark' | 'accent' | 'plate';
	export type UiShape = 'medallion' | 'panel' | 'plate';

	export type Props = RectangleProps & {
		tone?: UiTone;
		/** override the auto-detected silhouette */
		shape?: UiShape;
		hovered?: boolean;
		pressed?: boolean;
		active?: boolean;
		/** legacy sprite key (bet/buyBonus/base_ticker...) — kept for call-site compat */
		key?: string;
	};
</script>

<script lang="ts">
	import { Graphics, anchorToPivot } from 'pixi-svelte';
	import { HUD_THEME as T } from '../hudTheme';

	const {
		tone = 'dark',
		shape: shapeProp,
		hovered = false,
		pressed = false,
		active = false,
		key: _key,
		anchor,
		width,
		height,
		borderRadius,
		backgroundColor,
		backgroundAlpha: _backgroundAlpha,
		borderColor: _borderColor,
		borderWidth: _borderWidth,
		borderAlpha: _borderAlpha,
		...graphicsProps
	}: Props = $props();

	const w = $derived(Number(width) || 0);
	const h = $derived(Number(height) || 0);
	const isDisabled = $derived(backgroundColor === 0xaaaaaa);

	const shape = $derived.by<UiShape>(() => {
		if (shapeProp) return shapeProp;
		if (tone === 'plate') return 'plate';
		if (w > 0 && h > 0 && w / h > 2.2) return 'plate';
		const square = Math.abs(w - h) <= Math.max(w, h) * 0.2;
		const round = borderRadius == null || borderRadius >= Math.min(w, h) / 2 - 1;
		return square && round ? 'medallion' : 'panel';
	});

	// solid glass body colour for the current interaction state (no per-draw
	// gradient textures — robust + cheap; the metallic bevel gives the depth)
	const bodyColor = $derived.by(() => {
		if (isDisabled) return T.disabledBottom;
		if (pressed) return T.bodyBottomPressed;
		if (hovered) return T.bodyTopHover;
		return T.bodyTop;
	});
	const edge = $derived(
		isDisabled ? T.disabledEdge : active ? T.accent : hovered ? T.edgeGoldHover : T.edgeGold,
	);
	const bodyAlpha = $derived(tone === 'plate' ? 0.86 : T.bodyAlpha);

	/**
	 * Draw the shared glass body: solid fill, a dark outer line, a gold bevel
	 * and a bright inner highlight. `path` re-declares the silhouette (inset
	 * from the edge) for each layer.
	 */
	const drawFramed = (g: PIXI.Graphics, path: (inset: number) => void, ring: number) => {
		// body
		path(ring);
		g.fill({ color: bodyColor, alpha: bodyAlpha });

		// active glow sits just outside the bevel
		if (active && !isDisabled) {
			path(ring * 0.4);
			g.stroke({ color: T.accentGlow, width: ring * 1.6, alpha: 0.35 });
		}

		// dark outer line for separation from the background
		path(ring * 0.5);
		g.stroke({ color: T.edgeDark, width: ring * 1.5, alpha: isDisabled ? 0.4 : 0.85 });

		// metallic gold main edge
		path(ring);
		g.stroke({ color: edge, width: ring, alpha: isDisabled ? 0.6 : 1 });

		// inner top-lit highlight (the glass bevel)
		path(ring * 2.1);
		g.stroke({ color: T.innerHighlight, width: Math.max(1, ring * 0.4), alpha: isDisabled ? 0.1 : 0.5 });
	};

	const drawMedallion = (g: PIXI.Graphics) => {
		const cx = w / 2;
		const cy = h / 2;
		const R = Math.min(w, h) / 2;
		const ring = Math.max(1.5, R * 0.07);
		drawFramed(g, (inset) => g.circle(cx, cy, R - inset), ring);
	};

	const drawPanel = (g: PIXI.Graphics) => {
		const rad = Math.min(w, h) * 0.28;
		const ring = Math.max(1.5, Math.min(w, h) * 0.05);
		drawFramed(
			g,
			(inset) => g.roundRect(inset, inset, w - inset * 2, h - inset * 2, Math.max(1, rad - inset)),
			ring,
		);
	};

	const drawPlate = (g: PIXI.Graphics) => {
		const rad = h / 2;
		const ring = Math.max(1.2, h * 0.06);
		drawFramed(
			g,
			(inset) => g.roundRect(inset, inset, w - inset * 2, h - inset * 2, Math.max(1, rad - inset)),
			ring,
		);
	};

	const drawChrome = (g: PIXI.Graphics) => {
		if (!w || !h) return;
		if (shape === 'plate') drawPlate(g);
		else if (shape === 'panel') drawPanel(g);
		else drawMedallion(g);
	};
</script>

<Graphics
	{...graphicsProps}
	pivot={anchorToPivot({ anchor, sizes: { width: w, height: h } })}
	draw={drawChrome}
/>
