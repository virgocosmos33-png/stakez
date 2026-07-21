import * as PIXI from 'pixi.js';

import { HUD_THEME as T, radiusFor, pillRadius, strokeFor } from './hudTheme';

/**
 * Shared MONO / ROUNDED HUD primitives. Everything is a dark near-black card
 * with a thin light-grey hairline, matching UiSprite. Rounded rects use PIXI's
 * native roundRect so corners stay perfectly circular at any size.
 */

type ChromeOpts = {
	/** corner radius; defaults to the squircle radius for the short side */
	radius?: number;
	/** body fill colour / alpha */
	fill?: number;
	fillAlpha?: number;
	/** hairline colour / alpha / width */
	stroke?: number;
	strokeAlpha?: number;
	sw?: number;
	/** optional faint wash colour drawn over the fill (functional state) */
	wash?: number;
	washAlpha?: number;
};

/** rounded-rect card (fill + inset hairline) spanning (0,0)-(w,h) */
export const drawRoundedRect = (g: PIXI.Graphics, w: number, h: number, opts: ChromeOpts = {}) => {
	if (!w || !h) return;
	const short = Math.min(w, h);
	const r = opts.radius ?? radiusFor(short);
	const sw = opts.sw ?? strokeFor(short);

	// body fill
	g.roundRect(0, 0, w, h, r);
	g.fill({ color: opts.fill ?? T.bodyFill, alpha: opts.fillAlpha ?? T.bodyAlpha });

	// optional functional wash (kept faint so content stays legible)
	if (opts.wash !== undefined) {
		g.roundRect(0, 0, w, h, r);
		g.fill({ color: opts.wash, alpha: opts.washAlpha ?? T.accentActiveFillAlpha });
	}

	// inset hairline
	const inset = sw / 2;
	g.roundRect(inset, inset, w - sw, h - sw, Math.max(1, r - inset));
	g.stroke({
		color: opts.stroke ?? T.borderColor,
		width: sw,
		alpha: opts.strokeAlpha ?? T.borderAlpha,
		alignment: 0.5,
	});
};

/** fully-rounded pill (fill + inset hairline) spanning (0,0)-(w,h) */
export const drawPill = (g: PIXI.Graphics, w: number, h: number, opts: ChromeOpts = {}) =>
	drawRoundedRect(g, w, h, { ...opts, radius: opts.radius ?? pillRadius(h) });

/**
 * A small rounded chip ("nub") that holds an icon inside a pill. Drawn centred
 * on the local origin so an icon (anchor 0.5) drops straight on top.
 */
export const drawNub = (
	g: PIXI.Graphics,
	size: number,
	opts: { radius?: number; fill?: number; alpha?: number; stroke?: number; strokeAlpha?: number } = {},
) => {
	const r = opts.radius ?? radiusFor(size);
	const sw = strokeFor(size);
	g.roundRect(-size / 2, -size / 2, size, size, r);
	g.fill({ color: opts.fill ?? T.nubFill, alpha: opts.alpha ?? T.nubAlpha });
	g.roundRect(-size / 2 + sw / 2, -size / 2 + sw / 2, size - sw, size - sw, Math.max(1, r - sw / 2));
	g.stroke({ color: opts.stroke ?? T.borderColor, width: sw, alpha: opts.strokeAlpha ?? T.borderAlpha });
};

/** thin vertical divider centred at (x, 0), height a fraction of the pill */
export const drawDivider = (
	g: PIXI.Graphics,
	x: number,
	pillH: number,
	sw: number,
	opts: { color?: number; alpha?: number; heightRatio?: number } = {},
) => {
	const half = pillH * (opts.heightRatio ?? 0.3);
	g.moveTo(x, -half);
	g.lineTo(x, half);
	g.stroke({
		color: opts.color ?? T.borderColor,
		width: Math.max(1, sw * 0.7),
		alpha: opts.alpha ?? 0.5,
		cap: 'round',
	});
};
