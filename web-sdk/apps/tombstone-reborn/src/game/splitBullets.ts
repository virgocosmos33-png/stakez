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

/**
 * BASE gap between shots. A sheriff's revolver / magnum is a DELIBERATE weapon:
 * each round is a fat, spaced boom, not a machine-gun rattle. This is only the
 * anchor — the real gap per shot is jittered by `nextShotGap` so no two rests
 * are identical and the volley never reads as an evenly-timed "pam-pam-pam".
 */
export const SHOT_GAP_MS = 240;

/**
 * Uneven, human trigger-pull spacing. Every shot waits a DIFFERENT amount so the
 * volley sounds like a hand cocking and firing, not a worn machine on a metronome.
 * ~0.6x..1.7x the base (≈145..410ms at SHOT_GAP_MS 240).
 */
export const nextShotGap = () => Math.round(SHOT_GAP_MS * (0.6 + Math.random() * 1.1));

/**
 * Build the per-shot multiplier count-up: a strictly increasing run of integers
 * from just above `start` to EXACTLY `target`, one value per shot, in RANDOM
 * small increments (never a single big leap). The last entry is always `target`
 * so the number lands on the final shot (the ricochet). e.g. 10 -> 20 over 4
 * shots might roll 10 -> 13 -> 16 -> 18 -> 20.
 */
export const buildCountUp = (start: number, target: number, steps: number): number[] => {
	const s = Math.max(0, Math.min(Math.round(start), target - 1));
	const span = target - s;
	if (steps <= 1 || span <= 1) return [target];
	const weights = Array.from({ length: steps }, () => 0.5 + Math.random());
	const wsum = weights.reduce((a, b) => a + b, 0);
	const out: number[] = [];
	let acc = s;
	let used = 0;
	for (let i = 0; i < steps; i++) {
		used += weights[i];
		let v = i === steps - 1 ? target : Math.round(s + (span * used) / wsum);
		if (v <= acc) v = acc + 1; // stay strictly increasing
		if (i < steps - 1 && v >= target) v = target - 1; // don't hit target early
		acc = v;
		out.push(v);
	}
	// guard monotonicity, then pin the final value exactly on target
	for (let i = 1; i < out.length; i++) {
		if (out[i] <= out[i - 1]) out[i] = Math.min(target, out[i - 1] + 1);
	}
	out[steps - 1] = target;
	return out;
};

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
