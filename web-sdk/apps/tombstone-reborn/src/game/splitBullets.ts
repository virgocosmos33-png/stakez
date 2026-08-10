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

/** Chance a wood hit is followed by a ricochet whine. */
export const RICOCHET_CHANCE = 0.38;

export type HoleMark = {
	id: string;
	cellKey: string;
	/** card-local x (0 = centre) */
	x: number;
	/** card-local y */
	y: number;
	/** atlas frame index 0..2 */
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
		tex: Math.floor(rand(s + 2) * 3) % 3,
		scale: 0.42 + rand(s + 3) * 0.22,
		rot: (rand(s + 4) - 0.5) * 0.7,
	};
};
