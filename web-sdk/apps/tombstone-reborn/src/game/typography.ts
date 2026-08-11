/**
 * TOMBSTONE REBORN typography — the single source of truth for every piece of
 * text the game draws.
 *
 * No component may hardcode a font family. Import a role helper from here
 * instead; if a face ever needs repointing it happens in this file only.
 *
 * THE FOUR ROLES
 *
 *   display  Rye 400 — western wood-type slab with spurs and flourishes. Hero
 *            titles, win-tier titles, feature titles, brand marks. Ornamental,
 *            so it is only legible from roughly 20px up: never use it for HUD
 *            labels, body copy or anything that can shrink.
 *
 *   label    Oswald 600 — condensed signage caps. HUD labels (WAYS / WIN / BET /
 *            BALANCE / FREE SPINS), button captions, plaque text, the info
 *            marquee. Chosen because it still reads as stencilled wanted-poster
 *            small print at 8-12px, which no distressed face does.
 *
 *   value    Archivo Narrow 700 — every currency amount, ways count, multiplier
 *            and counter. Its figures are EQUAL WIDTH by default (456/1000 upem,
 *            verified at weight 700 by tools/qa_verify_webfonts.py) so a win
 *            count-up does not jitter as digits change. This matters because
 *            PIXI.TextStyle has no font-feature-settings, so `tnum` cannot be
 *            switched on at runtime — the face has to be tabular out of the box.
 *            Narrow also keeps long currency strings and nine-digit ways counts
 *            inside their wells.
 *
 *   accent   Special Elite 400 — distressed press/typewriter. The rough
 *            hand-painted attitude of the reference art, for hero subtitles and
 *            secondary lines at medium size only.
 *
 *   amount   The BITMAP face (`tombstone`, baked by tools/make_tombstone_font.py
 *            and read through winFont.ts). Celebration amounts keep using it:
 *            the gold-on-iron treatment is already baked per glyph, so a
 *            count-up costs no per-frame styling at all.
 *
 * GLYPH COVERAGE: only `value` (and the bitmap `amount` face) carry the full
 * currency set — ₹ ₽ ₱ ₩ live in the latin-ext subset and the display/accent
 * faces do not ship them. Never render an amount in `display` or `accent`.
 *
 * Licences and attribution: static/assets/fonts/webfont/README.md.
 */
import * as PIXI from 'pixi.js';
import { registerPreloadFontFaces } from 'pixi-svelte';

import { winFontFamily, winFontSize, winFontTint } from './winFont';
import { TYPOGRAPHY_METRICS } from './typographyMetrics.generated';

// Declares the @font-face blocks for the vendored woff2 files. Imported HERE
// rather than in +layout.svelte so a Storybook story that renders one component
// in isolation (never mounting the app layout) still gets the real faces.
import './typography.css';

export type TypographyRole = 'display' | 'label' | 'value' | 'accent';

/**
 * Family stacks handed to PIXI.TextStyle. Each keeps a narrow system fallback so
 * text can never vanish, but the vendored face is what should ever render —
 * `tools/qa_typography_shots.py` fails the build if a fallback wins.
 */
export const TR_FAMILY: Record<TypographyRole, string> = {
	display: '"Rye", "Bookman Old Style", Georgia, serif',
	label: '"Oswald", "Arial Narrow", "Segoe UI", Arial, sans-serif',
	value: '"Archivo Narrow", "Arial Narrow", "Segoe UI", Arial, sans-serif',
	accent: '"Special Elite", "Courier New", monospace',
};

/**
 * Weight each role renders at. These are LOAD-BEARING: the advance-width table
 * in typographyMetrics.generated.ts is baked from the variable fonts instanced
 * at exactly these weights, so changing one means re-running
 * `python tools/make_typography_metrics.py`.
 */
export const TR_WEIGHT: Record<TypographyRole, string> = {
	display: '400',
	label: '600',
	value: '700',
	accent: '400',
};

/** Smallest size the ornamental display face stays readable at. */
export const TR_DISPLAY_MIN_SIZE = 20;

// Faces the browser must have rasterized BEFORE the Pixi canvas draws its first
// text, or the first frames bake a system fallback into a cached texture.
// Registered at module scope: module evaluation always precedes component mount,
// so this lands before InitialiseApplication awaits preloadFont().
//
// The value face is registered TWICE: once normally, and once with a latin-ext
// sample character (₩) so the second subset is fetched up front too. Without
// that, the ext block stays unfetched until the first amount in a rupee / ruble
// / peso / won currency renders, and PIXI would cache that first text with a
// fallback glyph for the symbol and never re-rasterize it.
registerPreloadFontFaces([
	`${TR_WEIGHT.display} 16px Rye`,
	`${TR_WEIGHT.label} 16px Oswald`,
	`${TR_WEIGHT.value} 16px "Archivo Narrow"`,
	{ font: `${TR_WEIGHT.value} 16px "Archivo Narrow"`, text: '\u20a9' },
	`${TR_WEIGHT.accent} 16px "Special Elite"`,
]);

// --- brand ink -------------------------------------------------------------
// Every ink here is checked against the near-black HUD glass (~#0a0d10) it sits
// on. Nothing cool or grey: the game this was cloned from used a thin grey
// condensed sans on white steel, and that is precisely the read to avoid.
/** Bone/parchment — the readable ink for values and body copy on dark glass. */
export const TR_INK_BONE = 0xf0e6d0;
/** Tarnished brass — de-emphasised captions. 7.6:1 on the well interior. */
export const TR_INK_BRASS = 0xb8a074;
/** Branded gold, matching the baked bitmap amount face. */
export const TR_INK_GOLD = 0xe8d6a8;
/**
 * Dried blood, for the one emphasised word in a hero line. Bright enough to
 * clear 3:1 on a dark plate, so LARGE TEXT ONLY — it is not a body-copy ink.
 */
export const TR_INK_BLOOD = 0xc0392b;
/** Near-black iron, for the outline under hero titles. */
export const TR_INK_IRON = 0x120d0a;

// --- hero metal fills ------------------------------------------------------
// Built ONCE at module scope. Two reasons this must never happen per frame:
// generating the gradient is the expensive part, and PIXI keys its rasterized
// text cache off `fill.styleKey`, so reusing one instance keeps every hero title
// on a cache hit instead of re-rendering. textureSpace 'local' remaps the ramp
// across whatever text box uses it, at any size.
const metalFill = (stops: Array<[number, number]>) =>
	new PIXI.FillGradient({
		type: 'linear',
		start: { x: 0, y: 0 },
		end: { x: 0, y: 1 },
		colorStops: stops.map(([offset, color]) => ({ offset, color })),
		textureSpace: 'local',
	});

/**
 * Tarnished nickel: bone-white highlight down through warm silver into
 * gunmetal. The metallic display treatment of the reference art — deliberately
 * warm and grimy rather than the clinical white/steel of the game this was
 * cloned from.
 */
const METAL_NICKEL = metalFill([
	[0, 0xfdf6e6],
	[0.34, 0xd8d2c4],
	[0.52, 0x8f8a80],
	[0.72, 0x55524c],
	[1, 0x2b2926],
]);

/** Branded gold, for titles that sit beside the gold bitmap amounts. */
const METAL_GOLD = metalFill([
	[0, 0xfbeec2],
	[0.36, 0xeece84],
	[0.58, 0xc79a45],
	[0.8, 0x8a642a],
	[1, 0x4a3517],
]);

export const TR_METAL = { nickel: METAL_NICKEL, gold: METAL_GOLD } as const;
export type TrMetal = keyof typeof TR_METAL;

// --- role styles -----------------------------------------------------------

type RoleStyleOptions = {
	fontSize: number;
	fill?: PIXI.TextStyleOptions['fill'];
	letterSpacing?: number;
	align?: PIXI.TextStyleOptions['align'];
	lineHeight?: number;
	fontWeight?: PIXI.TextStyleOptions['fontWeight'];
	stroke?: PIXI.TextStyleOptions['stroke'];
	dropShadow?: PIXI.TextStyleOptions['dropShadow'];
	wordWrap?: boolean;
	wordWrapWidth?: number;
};

/** Build a PIXI text style for a role. Family and weight come from the role. */
export function trTextStyle(role: TypographyRole, opts: RoleStyleOptions): PIXI.TextStyleOptions {
	const style: PIXI.TextStyleOptions = {
		fontFamily: TR_FAMILY[role],
		fontWeight: opts.fontWeight ?? (TR_WEIGHT[role] as PIXI.TextStyleOptions['fontWeight']),
		fontSize: opts.fontSize,
		fill: opts.fill ?? TR_INK_BONE,
		align: opts.align ?? 'center',
	};
	if (opts.letterSpacing !== undefined) style.letterSpacing = opts.letterSpacing;
	if (opts.lineHeight !== undefined) style.lineHeight = opts.lineHeight;
	if (opts.stroke !== undefined) style.stroke = opts.stroke;
	if (opts.dropShadow !== undefined) style.dropShadow = opts.dropShadow;
	if (opts.wordWrap !== undefined) style.wordWrap = opts.wordWrap;
	if (opts.wordWrapWidth !== undefined) style.wordWrapWidth = opts.wordWrapWidth;
	return style;
}

/**
 * Western display face with a FLAT fill, for titles printed as dark ink on a
 * bright plate where the metallic gradient of `trHeroTitleStyle` would vanish.
 * Still subject to the display face's legibility floor (TR_DISPLAY_MIN_SIZE).
 */
export const trDisplayStyle = (opts: RoleStyleOptions) => trTextStyle('display', opts);

/** Stencilled condensed caps for HUD labels and captions. */
export const trLabelStyle = (opts: RoleStyleOptions) => trTextStyle('label', opts);

/** Tabular condensed figures for amounts, ways counts and multipliers. */
export const trValueStyle = (opts: RoleStyleOptions) => trTextStyle('value', opts);

/** Distressed press face for hero subtitles and secondary lines. */
export const trAccentStyle = (opts: RoleStyleOptions) => trTextStyle('accent', opts);

/**
 * CSS font shorthand for a role, for surfaces that measure text with a 2D canvas
 * context instead of estimating it (the intro carousel lays highlight segments
 * end-to-end, where accumulated estimate error would visibly mis-centre a line).
 * Keeps the measuring font locked to the rendering font.
 */
export function trCssFont(role: TypographyRole, fontSize: number, fontWeight?: string): string {
	return `${fontWeight ?? TR_WEIGHT[role]} ${fontSize}px ${TR_FAMILY[role]}`;
}

/**
 * HERO TITLE — the western display face wearing the reference-art metal
 * treatment: vertical metallic gradient fill, thick iron outline, and a soft
 * light rim so the letters lift off a dark plate.
 *
 * The gradient, the only costly ingredient, is a module-scope singleton, so
 * calling this every render is still a text-texture cache hit.
 */
export function trHeroTitleStyle(opts: {
	fontSize: number;
	metal?: TrMetal;
	letterSpacing?: number;
	align?: PIXI.TextStyleOptions['align'];
	lineHeight?: number;
	/** thickness of the iron outline as a fraction of the font size */
	outlineRatio?: number;
	/** set false for titles over busy art where the rim muddies the edge */
	rim?: boolean;
}): PIXI.TextStyleOptions {
	const outline = opts.fontSize * (opts.outlineRatio ?? 0.085);
	return trTextStyle('display', {
		fontSize: opts.fontSize,
		fill: TR_METAL[opts.metal ?? 'nickel'],
		align: opts.align,
		letterSpacing: opts.letterSpacing ?? 1,
		lineHeight: opts.lineHeight,
		stroke: { color: TR_INK_IRON, width: outline, join: 'round' },
		dropShadow:
			opts.rim === false
				? undefined
				: {
						color: 0xf6e6c8,
						alpha: 0.42,
						blur: Math.max(3, opts.fontSize * 0.12),
						distance: 0,
						angle: 0,
					},
	});
}

// --- width estimation ------------------------------------------------------

/**
 * Width a string will occupy, WITHOUT laying out a PIXI.Text.
 *
 * The HUD sizes its wells before it can measure the real text node, and the old
 * estimate was a flat `text.length * fontSize * 0.6` tuned for Segoe UI. Against
 * the condensed faces that guess is ~30% too wide for digits, which over-grows
 * every well, while being too narrow for wide caps runs, which clips them. This
 * sums the real per-glyph advances baked out of the shipped woff2 files.
 *
 * PIXI adds letterSpacing after every character including the last, so the same
 * is charged here — an estimate that runs a hair wide is safe, one that runs
 * short clips text.
 */
export function estimateTextWidth(
	text: string,
	opts: { role: TypographyRole; fontSize: number; letterSpacing?: number },
): number {
	const metrics = TYPOGRAPHY_METRICS[opts.role];
	let ratio = 0;
	for (const char of text) ratio += metrics.advance[char] ?? metrics.fallback;
	return ratio * opts.fontSize + (opts.letterSpacing ?? 0) * text.length;
}

/**
 * Mean glyph advance per role, as a fraction of the font size.
 *
 * Only for handing to shared components that estimate width with a single
 * `length * fontSize * coefficient` coefficient and cannot import this app's
 * per-glyph table (see hudTheme's fontLabelAdvance / fontValueAdvance). Anything
 * in this app should call estimateTextWidth instead — it is strictly better.
 *
 * Sampled over the characters each role actually renders in those components:
 * caps for labels, figures and currency punctuation for values. Rounded UP so a
 * consumer errs wide, since a short estimate clips.
 */
export const TR_MEAN_ADVANCE: Record<TypographyRole, number> = (() => {
	const SAMPLE: Record<TypographyRole, string> = {
		display: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
		label: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
		value: '0123456789.,$',
		accent: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
	};
	const out = {} as Record<TypographyRole, number>;
	for (const role of Object.keys(SAMPLE) as TypographyRole[]) {
		const chars = [...SAMPLE[role]];
		const metrics = TYPOGRAPHY_METRICS[role];
		const mean =
			chars.reduce((sum, c) => sum + (metrics.advance[c] ?? metrics.fallback), 0) / chars.length;
		out[role] = Math.ceil(mean * 100) / 100;
	}
	return out;
})();

/**
 * Largest font size at or below `base` that keeps `text` inside `maxWidth`.
 * Used by the HUD wells and plaques so a huge value shrinks instead of clipping.
 */
export function fitFontSize(
	text: string,
	opts: { role: TypographyRole; base: number; maxWidth: number; min?: number; letterSpacing?: number },
): number {
	const width = estimateTextWidth(text, {
		role: opts.role,
		fontSize: opts.base,
		letterSpacing: opts.letterSpacing,
	});
	if (width <= opts.maxWidth) return opts.base;
	const scaled = opts.base * (opts.maxWidth / width);
	return Math.max(opts.min ?? 9, Math.floor(scaled));
}

// --- baked bitmap amount face ---------------------------------------------
// Re-exported so a component needs ONE typography import, whether it draws
// browser-font text or the bitmap celebration amounts.
export { winFontFamily as trAmountFamily, winFontTint as trAmountTint, winFontSize as trAmountSize };
