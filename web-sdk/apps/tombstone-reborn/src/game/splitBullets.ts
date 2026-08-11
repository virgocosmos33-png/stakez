/**
 * SPLIT bullet-hole strike helpers.
 *
 * Shot count scales with the cell's multiplier (book `count` / badge "Nx"):
 * bigger splits get more rounds into the wood before the panes peel apart.
 */

export const shotsForMultiplier = (count: number) => {
	if (count <= 2) return 1;
	if (count <= 4) return 2;
	if (count <= 7) return 3;
	return 4;
};

/** Gap between volleys so stacked hits still read as separate rounds. */
export const SHOT_GAP_MS = 105;

/**
 * Beat held AFTER the last bullet volley (multiplier badge fully up) and BEFORE
 * a big cell detonates, so the player can READ the Nx before it blows up. The
 * explosion is the final step of the strike, never simultaneous with the shots.
 */
export const EXPLOSION_READ_MS = 520;

/**
 * A split cell whose multiplier is STRICTLY above this detonates: instead of only
 * taking more bullet holes, the cell blows up (SplitExplosion flipbook + boom).
 * 10x is the "big hit" line the player already reads off the Nx badge.
 */
export const EXPLOSION_MIN_MULT = 10;

/** Splintered-hole variants packed by tools/make_bullet_hole_atlas.py. */
export const HOLE_VARIANTS = 6;

export type HoleMark = {
	id: string;
	cellKey: string;
	/** card-local x (0 = centre) */
	x: number;
	/** card-local y */
	y: number;
	/** atlas frame index, 0..HOLE_VARIANTS-1 */
	tex: number;
	scale: number;
	/** radians */
	rot: number;
	/** performance.now() when stamped — drives the muzzle flash */
	born: number;
};

const rand = (seed: number) => {
	const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
	return value - Math.floor(value);
};

/** Deterministic scatter position inside the card for shot `index` on a cell. */
export const holePose = (seed: number, index: number, cardW: number, cardH: number) => {
	const s = seed * 17 + index * 97;
	return {
		x: (rand(s) - 0.5) * cardW * 0.62,
		y: (rand(s + 1) - 0.5) * cardH * 0.58,
		tex: Math.floor(rand(s + 2) * HOLE_VARIANTS) % HOLE_VARIANTS,
		// kept small: at the old 0.42-0.64 a single hole spanned most of the card
		// and its splinter ring read as a sparkle decal over the symbol
		scale: 0.26 + rand(s + 3) * 0.14,
		rot: (rand(s + 4) - 0.5) * 0.7,
	};
};
