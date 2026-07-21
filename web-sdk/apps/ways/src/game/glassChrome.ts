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
	const frame = Math.max(4, height * 0.12); // ornate mirror frame is a touch thicker
	const iw = width - frame * 2;
	const ih = height - frame * 2;
	const ir = Math.max(0, r - frame);

	// layered violet séance aura: a wide soft haze fading out, then a tighter
	// hotter ring hugging the frame so the button glows like haunted glass
	if (glow) {
		for (let i = 7; i >= 1; i--) {
			const grow = i * 3.0;
			g.roundRect(x - grow, y - grow, width + grow * 2, height + grow * 2, r + grow);
			g.stroke({ width: 3, color: 0x9a6cff, alpha: 0.05 * i });
		}
		g.roundRect(x - 1.5, y - 1.5, width + 3, height + 3, r + 1.5);
		g.stroke({ width: 2, color: 0xc9a9ff, alpha: 0.6 });
	}

	// tarnished antique-silver mirror frame: bright lavender highlight on the
	// top lip, a dark plum core, and a silver return along the bottom bevel
	const frameGrad = new PIXI.FillGradient(0, y, 0, y + height);
	frameGrad.addColorStop(0, 0xe4d8ff);
	frameGrad.addColorStop(0.22, 0x9c86c8);
	frameGrad.addColorStop(0.5, 0x2a1c42);
	frameGrad.addColorStop(0.8, 0x6a5691);
	frameGrad.addColorStop(1, 0xd8c9f5);
	g.roundRect(x, y, width, height, r);
	g.fill(frameGrad);
	// crisp bright outer lip + dark outline seat the frame against the scene
	g.roundRect(x, y, width, height, r);
	g.stroke({ width: 1.5, color: 0xf0e6ff, alpha: 0.35 });
	g.roundRect(x + 0.75, y + 0.75, width - 1.5, height - 1.5, r - 0.75);
	g.stroke({ width: 2, color: 0x05030a, alpha: 0.9 });

	// dark groove separating the frame from the glass (carved-bezel depth)
	g.roundRect(x + frame - 2, y + frame - 2, iw + 4, ih + 4, ir + 2);
	g.stroke({ width: 2, color: 0x0a0614, alpha: 0.9 });

	// deep amethyst scrying glass with a darkened lower vignette
	const glass = new PIXI.FillGradient(0, y + frame, 0, y + height - frame);
	glass.addColorStop(0, 0x39244f);
	glass.addColorStop(0.55, 0x1a0f2c);
	glass.addColorStop(1, 0x080410);
	g.roundRect(x + frame, y + frame, iw, ih, ir);
	g.fill(glass);

	// broad top specular sheen across the glass
	g.ellipse(0, y + frame + ih * 0.24, iw * 0.44, ih * 0.24);
	g.fill({ color: 0xffffff, alpha: 0.14 });

	// a diagonal glass glint (contained inside the interior), the signature
	// polished-mirror streak of light sliding across the pane
	const gx = x + frame;
	const gTop = y + frame;
	const gBot = y + height - frame;
	const slant = ih * 0.5;
	const cx = gx + iw * 0.3;
	const half = Math.max(3, iw * 0.045);
	g.poly([
		cx - half - slant / 2, gTop,
		cx + half - slant / 2, gTop,
		cx + half + slant / 2, gBot,
		cx - half + slant / 2, gBot,
	]);
	g.fill({ color: 0xe9deff, alpha: 0.1 });

	// bright inner rim so the glass edge catches the light
	g.roundRect(x + frame, y + frame, iw, ih, ir);
	g.stroke({ width: 1.5, color: 0xd7c7f5, alpha: 0.55 });
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
