import * as PIXI from 'pixi.js';

type PillOptions = {
	/** rectangle drawn centered on (0,0) */
	width: number;
	height: number;
	/** corner radius; defaults to a full pill */
	radius?: number;
	/** draw the soft violet aura ring around the pill */
	glow?: boolean;
};

/**
 * Draws the Madam Mirror "scrying-glass" chrome used by every overlay CONTINUE
 * button so they match the in-game HUD (see components-ui-pixi/UiSprite.svelte):
 * a tarnished antique-silver frame around a dark violet glass plate with a top
 * specular sheen and an optional violet aura. Drawn centered on the origin.
 */
export const drawGlassPill = (g: PIXI.Graphics, opts: PillOptions) => {
	const { width, height, glow = true } = opts;
	if (!width || !height) return;
	const r = opts.radius ?? height / 2;
	const x = -width / 2;
	const y = -height / 2;
	const frame = Math.max(3, height * 0.09);
	const iw = width - frame * 2;
	const ih = height - frame * 2;
	const ir = Math.max(0, r - frame);

	if (glow) {
		for (let i = 5; i >= 1; i--) {
			const grow = i * 2.6;
			g.roundRect(x - grow, y - grow, width + grow * 2, height + grow * 2, r + grow);
			g.stroke({ width: 3, color: 0xb887ff, alpha: 0.06 * i });
		}
	}

	const frameGrad = new PIXI.FillGradient(0, y, 0, y + height);
	frameGrad.addColorStop(0, 0xcdbdf0);
	frameGrad.addColorStop(0.5, 0x1a1130);
	frameGrad.addColorStop(1, 0xcdbdf0);
	g.roundRect(x, y, width, height, r);
	g.fill(frameGrad);
	g.roundRect(x, y, width, height, r);
	g.stroke({ width: 2, color: 0x05030a, alpha: 0.85 });

	const glass = new PIXI.FillGradient(0, y + frame, 0, y + height - frame);
	glass.addColorStop(0, 0x2a1a44);
	glass.addColorStop(1, 0x0c0715);
	g.roundRect(x + frame, y + frame, iw, ih, ir);
	g.fill(glass);

	g.ellipse(0, y + frame + ih * 0.26, iw * 0.42, ih * 0.22);
	g.fill({ color: 0xffffff, alpha: 0.12 });

	g.roundRect(x + frame, y + frame, iw, ih, ir);
	g.stroke({ width: 1.5, color: 0xd7c7f5, alpha: 0.5 });
};

/**
 * A soft dark "scrying-glass" recess drawn centered on the origin, used inside
 * the generated counter frames so the silver bitmap numerals lift off the
 * amethyst glass window with clean contrast (no hard box — just a deepened
 * violet pad with a faint inner rim).
 */
export const drawWindowShade = (
	g: PIXI.Graphics,
	opts: { width: number; height: number; radius: number },
) => {
	const { width, height, radius } = opts;
	if (!width || !height) return;
	g.roundRect(-width / 2, -height / 2, width, height, radius);
	g.fill({ color: 0x0a0512, alpha: 0.5 });
	g.roundRect(-width / 2, -height / 2, width, height, radius);
	g.stroke({ width: 1.5, color: 0x3a2860, alpha: 0.55 });
};
