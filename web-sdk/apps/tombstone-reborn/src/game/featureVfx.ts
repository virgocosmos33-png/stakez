/**
 * Tombstone Reborn western FX language for the NON-SPLIT feature events —
 * nudge, gunsmoke, coffin open, dig up, special-bar hit and bounty.
 *
 * Atlas: tools/make_tombstone_feature_vfx_atlas.py → asset key `tombstoneFeatureVfx`.
 * Hero plates (revolver muzzle blast, sand plume, gold starburst) are separate
 * `fx*` sprite keys baked by the same script; the dig-up spade and its turned
 * earth come from tools/make_digup_shovel.py.
 *
 * Sources: Kenney CC0 particle-pack / light-masks / splat-pack / smoke-particles
 * for the atlas layers, recoloured to the graveyard palette below; already
 * generated Scenario library art (read-only) for the muzzle blast, dust plume
 * and starburst; Layer AI for the dig-up spade and dug-earth decal, and for the
 * nudge rider's card frame and multiplier plaque (tools/make_nudge_ui.py).
 *
 * Split/lock FX live in tombstoneVfx.ts and are owned elsewhere — the two atlases
 * are deliberately separate so neither agent's bake can break the other's frames.
 */

export const FEATURE_VFX_ASSET = 'tombstoneFeatureVfx';

/** Hero sprite keys (single textures, not atlas frames). */
export const FEATURE_ART = {
	dustPlume: 'fxDustPlume',
	muzzleFlash: 'fxMuzzleFlash',
	/** planted spade — blade at the bottom, D-grip at the top, drawn upright */
	shovel: 'fxShovel',
	/** turned earth left where the blade bit in */
	digScar: 'fxDigScar',
	/** cracked-strike decal stamped ON the symbol at the blade's impact — a
		gouge with cracks radiating out, so the hit is FELT on the card face */
	digImpact: 'fxDigImpact',
	/** iron-and-wood card frame with an OPEN centre — the rider reads through it */
	riderFrame: 'fxRiderFrame',
	/** oak-and-iron nameplate the nudge/bounty multiplier is struck on */
	multPlaque: 'fxMultPlaque',
	/** full-reel NUDGE WAYS totem — clipped from the top as it walks down */
	nudgeColumn: 'fxNudgeColumn',
} as const;

/**
 * Frame indices into the `tombstoneFeatureVfx` spritesheet.
 * Must stay in step with FRAMES in tools/make_tombstone_feature_vfx_atlas.py.
 */
export const FX = {
	/** revolver exhaust, drifting and thinning */
	gunsmoke: [0, 1, 2, 3, 4, 5, 6, 7],
	/** kicked grave dirt / trail dust */
	dust: [8, 9, 10, 11, 12, 13, 14, 15],
	/** directional flash cone — points UP at rest, rotate it to aim */
	muzzle: [16, 17, 18, 19],
	/** omnidirectional bloom for an impact with no barrel behind it */
	flash: [20, 21, 22, 23],
	/** the coffin lid letting go */
	burst: [24, 25, 26, 27],
	dirt: [28, 29, 30],
	/** soft ash smudge left on a scored card */
	scorch: [31, 32, 33],
	spark: [34, 35, 36],
	/** speed streak dragged behind a moving card */
	trace: [37, 38, 39],
	splat: [40, 41, 42],
	/** crescent arc a shunted or riding card cuts */
	swipe: [43, 44, 45],
	glow: 46,
	/** halos a scored cell instead of washing over it */
	ring: 47,
	shaft: [48, 49, 50],
} as const;

/** Graveyard palette. Deliberately no clinical white and no saturated yellow. */
export const FEATURE_FX = {
	brass: 0xc9a34a,
	spentBrass: 0xe6c47e,
	sand: 0xc4a87c,
	boneDust: 0xd4c4a8,
	gunsmoke: 0x988e80,
	powder: 0x563e2a,
	rust: 0xa84a28,
	ember: 0xd67e34,
	iron: 0x2a2420,
	dark: 0x0a0806,
} as const;

/**
 * Pick a frame from a sequence by normalised progress. Clamps at both ends so a
 * finished tween holds the last frame instead of wrapping back to the first.
 */
export const seqFrame = (frames: readonly number[], progress: number) => {
	const clamped = Math.min(Math.max(progress, 0), 0.999);
	return frames[Math.floor(clamped * frames.length)];
};

/** Deterministic 0..1 noise so every replay of an event looks identical. */
export const fxRandom = (seed: number) => {
	const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
	return value - Math.floor(value);
};

/**
 * Ease a puff out: rises fast, lingers, fades. Returns 0..1 opacity for a
 * particle whose life is `t` (0..1).
 */
export const puffFade = (t: number) => {
	if (t <= 0 || t >= 1) return 0;
	return Math.min(1, t / 0.12) * Math.min(1, (1 - t) / 0.45);
};
