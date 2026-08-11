/**
 * Frame contract for the `splitExplosion` atlas (tools/make_split_explosion_atlas.py).
 *
 * A high-multiplier split cell (count > EXPLOSION_MIN_MULT) does not just take
 * more bullet holes — it DETONATES: a one-shot gunpowder blast that flashes,
 * billows fire, then rolls off as brown smoke. The atlas is a single band of
 * `EXPLOSION_FRAME_COUNT` frames in play order; the loader hands them back as a
 * flat Texture[] in that same order (Object.values on the JSON), so the frame
 * index IS the array index.
 *
 * Art source: Kenney `explosions/PNG/Explosion_1` (the one fiery orange/smoke
 * style; the other nine are crystal/toxic and off-theme).
 */
export const SPLIT_EXPLOSION_ASSET = 'splitExplosion';

export const EXPLOSION_FRAME_COUNT = 10;

/** ~455ms for the full blast — long enough to read fire→smoke, short enough to
 * stay a punch and not sit on the cell. */
export const EXPLOSION_FPS = 22;

/** Whole play length in ms, used to prune finished blasts. */
export const EXPLOSION_LIFE_MS = (EXPLOSION_FRAME_COUNT / EXPLOSION_FPS) * 1000;
