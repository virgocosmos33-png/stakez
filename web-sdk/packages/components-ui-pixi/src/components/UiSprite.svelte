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

	// Dark-matte + gold theme: near-black charcoal bodies with a soft top sheen,
	// a subtle light rim and a soft drop shadow. Gold is reserved for accents
	// (active state ring) and for the plate values (handled in UiLabel).
	const BODY_TOP = 0x37373d;
	const BODY_MID = 0x27272c;
	const BODY_BOT = 0x18181c;
	const OUTLINE = 0x070708;
	const RIM = 0x53535d;
	const GOLD = 0xffc12e;
</script>

<script lang="ts">
	import { Graphics, anchorToPivot } from 'pixi-svelte';

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

	const bodyGrad = (g: PIXI.Graphics, x: number, y: number, hh: number) => {
		const grad = new PIXI.FillGradient(x, y, x, y + hh);
		grad.addColorStop(0, isDisabled ? 0x2a2a2e : BODY_TOP);
		grad.addColorStop(0.5, isDisabled ? 0x212125 : BODY_MID);
		grad.addColorStop(1, isDisabled ? 0x161619 : BODY_BOT);
		g.fill(grad);
	};

	const drawMedallion = (g: PIXI.Graphics) => {
		const cx = w / 2;
		const cy = h / 2;
		const R = Math.min(w, h) / 2;

		// soft drop shadow
		g.circle(cx, cy + Math.max(2, R * 0.08), R);
		g.fill({ color: 0x000000, alpha: 0.22 });

		g.circle(cx, cy, R);
		bodyGrad(g, cx - R, cy - R, R * 2);

		g.circle(cx, cy, R);
		g.stroke({ color: OUTLINE, width: 1.5, alpha: 0.6 });
		g.circle(cx, cy, R - 1.2);
		g.stroke({ color: RIM, width: 1.4, alpha: 0.55 });

		if (active && !isDisabled) {
			g.circle(cx, cy, R - 2.5);
			g.stroke({ color: GOLD, width: 1.8, alpha: 0.55 });
		}

		g.ellipse(cx, cy - R * 0.42, R * 0.68, R * 0.4);
		g.fill({ color: 0xffffff, alpha: pressed ? 0.03 : hovered ? 0.13 : 0.06 });

		if (pressed) {
			g.circle(cx, cy, R);
			g.fill({ color: 0x000000, alpha: 0.16 });
		}
	};

	const drawPanel = (g: PIXI.Graphics) => {
		const rad = Math.min(w, h) * 0.26;
		const sh = Math.max(2, Math.min(w, h) * 0.07);

		g.roundRect(0, sh, w, h, rad);
		g.fill({ color: 0x000000, alpha: 0.22 });

		g.roundRect(0, 0, w, h, rad);
		bodyGrad(g, 0, 0, h);

		g.roundRect(0, 0, w, h, rad);
		g.stroke({ color: OUTLINE, width: 1.5, alpha: 0.6 });
		g.roundRect(1.2, 1.2, w - 2.4, h - 2.4, rad - 1);
		g.stroke({ color: RIM, width: 1.4, alpha: 0.5 });

		if (active && !isDisabled) {
			g.roundRect(2.5, 2.5, w - 5, h - 5, rad - 2);
			g.stroke({ color: GOLD, width: 1.8, alpha: 0.5 });
		}

		g.ellipse(w / 2, h * 0.24, w * 0.42, h * 0.2);
		g.fill({ color: 0xffffff, alpha: pressed ? 0.03 : hovered ? 0.13 : 0.06 });

		if (pressed) {
			g.roundRect(0, 0, w, h, rad);
			g.fill({ color: 0x000000, alpha: 0.16 });
		}
	};

	const drawPlate = (g: PIXI.Graphics) => {
		const rad = h / 2;
		const sh = Math.max(2, h * 0.09);

		g.roundRect(0, sh, w, h, rad);
		g.fill({ color: 0x000000, alpha: 0.22 });

		g.roundRect(0, 0, w, h, rad);
		bodyGrad(g, 0, 0, h);

		g.roundRect(0, 0, w, h, rad);
		g.stroke({ color: OUTLINE, width: 1.5, alpha: 0.6 });
		g.roundRect(1.2, 1.2, w - 2.4, h - 2.4, rad - 1);
		g.stroke({ color: RIM, width: 1.3, alpha: 0.45 });

		g.roundRect(rad * 0.5, h * 0.12, w - rad, h * 0.32, h * 0.16);
		g.fill({ color: 0xffffff, alpha: 0.05 });
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
