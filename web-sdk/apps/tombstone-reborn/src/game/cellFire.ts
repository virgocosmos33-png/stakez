/**
 * Frame contract for the `cellFire` atlas (tools/make_cell_fire_atlas.py).
 *
 * The atlas is packed in bands, in this order, and the loader hands them back
 * as one flat Texture[] — so the offsets below are the only thing standing
 * between the component and the right picture. If the bake script's counts
 * change, these change with it.
 *
 * Art sources:
 *   frame — REAL fire footage (Layer-AI flame wall on black, 16 frames), keyed
 *           black->alpha by luminance with its real colour kept, ringed per edge
 *           into a burning frame whose transparent gaps let the card read
 *           through. Drawn NORMAL blend (compositing is baked, so it renders in
 *           headless and matches the qa_fire_mock preview).
 *   smoke — Kenney smoke-particles / "Black smoke" sequence (CC0)
 *   glow  — Kenney light-masks-1.0 / Transparent (CC0)
 *   ember — Kenney particle-pack / spark (CC0), warm-tinted
 */
export const CELL_FIRE_ASSET = 'cellFire';

const wrap = (index: number, count: number) => ((index % count) + count) % count;

/** Burning-frame flipbook — the primary fire, one continuous scroll. */
export const FRAME_FRAME_COUNT = 16;
export const frameFrame = (index: number) => wrap(index, FRAME_FRAME_COUNT);

export const SMOKE_FRAME_COUNT = 16;
export const smokeFrame = (index: number) =>
	FRAME_FRAME_COUNT + wrap(index, SMOKE_FRAME_COUNT);

export const GLOW_FRAME = FRAME_FRAME_COUNT + SMOKE_FRAME_COUNT;

const EMBER_START = GLOW_FRAME + 1;
export const EMBER_FRAME_COUNT = 8;
export const emberFrame = (index: number) => EMBER_START + wrap(index, EMBER_FRAME_COUNT);

/**
 * Every frame the atlas must contain. Guard on this rather than on any single
 * band: a stale bake missing a band would otherwise index past the end of the
 * texture list and draw nothing, silently.
 */
export const CELL_FIRE_FRAME_COUNT = EMBER_START + EMBER_FRAME_COUNT;

/**
 * Geometry contract with make_cell_fire_atlas.py: the baked frame texture is
 * FRAME_W x FRAME_H around a CARD_W x CARD_H card. The component draws the sprite
 * at these ratios of the real card so the fire hugs the border and licks outward
 * WITHOUT stretching (aspect matches). Keep in sync with the bake constants.
 */
export const FIRE_FRAME_W_RATIO = 270 / 186;
export const FIRE_FRAME_H_RATIO = 324 / 240;

/** Scroll rate of the burning frame, and the smoke flipbook rate. */
export const FRAME_FPS = 18;
export const SMOKE_FPS = 12;
