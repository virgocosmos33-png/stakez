import * as PIXI from 'pixi.js';

type PillOptions = {
	/** rectangle drawn centered on (0,0) */
	width: number;
	height: number;
	/** corner radius; defaults to a full pill */
	radius?: number;
	/** soft clinical halo around the pill */
	glow?: boolean;
};

/**
 * THE WHITE ROOM observation-glass chrome for secondary UI still on glass
 * (WinCelebration MAX WIN gate). IntroCarousel uses magenta `uiCtaActivate`
 * plates instead — same family as HTML paytable / buy-confirm. (The bonus-entry
 * overlays that also used those plates are deleted; this game has no bonus
 * levels.)
 * Frosted clinical plate in a steel/silver bezel — NOT Madam Mirror violet
 * scrying glass. HUD control-bar tokens are untouched (hud.colors).
 */
export const drawGlassPill = (g: PIXI.Graphics, opts: PillOptions) => {
	const { width, height, glow = true } = opts;
	if (!width || !height) return;
	const r = opts.radius ?? height / 2;
	const x = -width / 2;
	const y = -height / 2;
	const frame = Math.max(4, height * 0.12);
	const iw = width - frame * 2;
	const ih = height - frame * 2;
	const ir = Math.max(0, r - frame);

	if (glow) {
		for (let i = 5; i >= 1; i--) {
			const grow = i * 2.4;
			g.roundRect(x - grow, y - grow, width + grow * 2, height + grow * 2, r + grow);
			g.stroke({ width: 2, color: 0xc8c4bc, alpha: 0.04 * i });
		}
		g.roundRect(x - 1.5, y - 1.5, width + 3, height + 3, r + 1.5);
		g.stroke({ width: 1.5, color: 0xf4f1ec, alpha: 0.35 });
	}

	const frameGrad = new PIXI.FillGradient(0, y, 0, y + height);
	frameGrad.addColorStop(0, 0xf4f1ec);
	frameGrad.addColorStop(0.22, 0xc8c4bc);
	frameGrad.addColorStop(0.5, 0x3a3632);
	frameGrad.addColorStop(0.8, 0x8a8680);
	frameGrad.addColorStop(1, 0xe8e4dc);
	g.roundRect(x, y, width, height, r);
	g.fill(frameGrad);
	g.roundRect(x, y, width, height, r);
	g.stroke({ width: 1.5, color: 0xf4f1ec, alpha: 0.4 });
	g.roundRect(x + 0.75, y + 0.75, width - 1.5, height - 1.5, r - 0.75);
	g.stroke({ width: 2, color: 0x1a1816, alpha: 0.9 });

	g.roundRect(x + frame - 2, y + frame - 2, iw + 4, ih + 4, ir + 2);
	g.stroke({ width: 2, color: 0x12100e, alpha: 0.9 });

	// frosted observation glass (clinical grey, not amethyst)
	const glass = new PIXI.FillGradient(0, y + frame, 0, y + height - frame);
	glass.addColorStop(0, 0x5c5854);
	glass.addColorStop(0.55, 0x2a2826);
	glass.addColorStop(1, 0x12100e);
	g.roundRect(x + frame, y + frame, iw, ih, ir);
	g.fill(glass);

	g.ellipse(0, y + frame + ih * 0.24, iw * 0.44, ih * 0.24);
	g.fill({ color: 0xffffff, alpha: 0.12 });

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
	g.fill({ color: 0xf4f1ec, alpha: 0.08 });

	g.roundRect(x + frame, y + frame, iw, ih, ir);
	g.stroke({ width: 1.5, color: 0xc8c4bc, alpha: 0.5 });
};

/** Soft clinical recess for counter windows (no violet pad). */
export const drawWindowShade = (
	g: PIXI.Graphics,
	opts: { width: number; height: number; radius: number },
) => {
	const { width, height, radius } = opts;
	if (!width || !height) return;
	g.roundRect(-width / 2, -height / 2, width, height, radius);
	g.fill({ color: 0x12100e, alpha: 0.55 });
	g.roundRect(-width / 2, -height / 2, width, height, radius);
	g.stroke({ width: 1.5, color: 0x8a8680, alpha: 0.45 });
};
