/**
 * Frame contract for the `splitBlood` atlas (tools/make_split_cut_fx.py).
 *
 * One play per CUT, not per cell: 1→2 is one seam / one flipbook, 1→3 is two.
 * The loader hands textures back as a flat Texture[] in JSON insertion order,
 * so index 0 is the puncture and index 7 is the hold wound.
 */
export const SPLIT_BLOOD_ASSET = 'splitBlood';

export const BLOOD_FRAME_COUNT = 8;

/** Fast enough to read as a burst, short enough that a 3-cut cell does not crawl. */
export const BLOOD_FPS = 18;

export const BLOOD_LIFE_MS = (BLOOD_FRAME_COUNT / BLOOD_FPS) * 1000;
