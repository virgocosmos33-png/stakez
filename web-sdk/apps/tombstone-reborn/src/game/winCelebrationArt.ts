/**
 * Tombstone Reborn win-celebration art contract.
 *
 * Baked by tools/make_win_celebration_art.py. The frame indices below are the
 * binding order of that script's LIGHT_FRAMES / VFX_FRAMES tables — change one
 * and you must change the other.
 *
 * This replaces the Madam Mirror celebration media entirely: the old ladder
 * played `celebT2..celebT7` (photographic White Room footage of a straitjacketed
 * woman in a padded asylum cell, tier 7 a literal white-out) inside a thin amber
 * CCTV-style bezel, and threw the Samurai Dogs 2 template coin sheet on top.
 */

export const WIN_CELEB_VFX_ASSET = 'winCelebVfx';
export const WIN_CELEB_LIGHT_ASSET = 'winCelebLight';
export const WIN_SCATTER_ASSET = 'winScatter';
export const WIN_FRAME_ASSET = 'winFrame';

/** Big soft light shapes (512px cells) — god-rays, lantern glow, bell rings. */
export const WIN_LIGHT = {
	rayFan: 0,
	rayStreaks: 1,
	rayWide: 2,
	rayCone: 3,
	glowWarm: 4,
	glowCore: 5,
	ringSoft: 6,
	ringHard: 7,
} as const;

/** Cell size of the win_celeb_vfx atlas, for scale-based sizing. */
export const WIN_VFX_CELL = 256;

/** Small particles (256px cells) — pops, dust, gunsmoke, embers. */
export const WIN_VFX = {
	/** Scenario library: gold multi-point starburst */
	starburst: 0,
	/** Scenario library: gold spark streak with a bright flare head */
	sparkStreak: 1,
	/** Scenario library: ornate spiked star emblem, tinted off its original blue */
	starEmblem: 2,
	/** Scenario library: wood-grip revolver render, used whole as a title accent */
	revolverEmblem: 3,
	/** Scenario library: tall billowing sand plume */
	dustPlume: 4,
	starBig: 5,
	starSmall: 6,
	starPoint: 7,
	muzzleFlare: 8,
	muzzleWide: 9,
	dustPuffA: 10,
	dustPuffB: 11,
	smokeA: 12,
	smokeB: 13,
	dirtA: 14,
	flashPop: 15,
	emberMote: 16,
	traceLine: 17,
	grimeSplat: 18,
} as const;

/**
 * Celebration palette. Warm gold / iron / grave dust only — the old ladder's
 * clinical near-white (0xf4f1ec on a white padded cell) is what the player kept
 * seeing, so nothing here goes above the dusty bone highlight.
 */
export const WIN_PALETTE = {
	gold: 0xc9a34a,
	goldHot: 0xe8c46e,
	goldPale: 0xd9bd82,
	ember: 0xb5622a,
	bloodRust: 0xb54a2a,
	dust: 0x8a6e4a,
	boneDust: 0xd4c4a8,
	gunsmoke: 0x6e6860,
	iron: 0x2a2420,
	ironEdge: 0x5a4e42,
	timber: 0x2e2117,
	dark: 0x0a0806,
} as const;

/**
 * Per-tier escalation. Every lever grows monotonically so a bigger win is
 * physically bigger on screen, not merely faster: more god-rays, denser dust,
 * larger starburst pops, harder entry kick. `bellTolls` is the max-win-only
 * expanding bronze ring that gives BOOT HILL its tolling gravitas.
 */
export type WinTierIntensity = {
	/** god-ray shafts behind the frame */
	rays: number;
	rayAlpha: number;
	/** rising gold embers over the whole canvas */
	embers: number;
	/** drifting dust plumes across the panel */
	dust: number;
	/** starburst pop scale on tier entry, in panel widths */
	popScale: number;
	/** radiating spark streaks on tier entry */
	streaks: number;
	/** screen kick on tier entry, in pixels */
	kick: number;
	/** slow Ken-Burns push on the hero plate over the tier's dwell */
	push: number;
	/** expanding bell rings per second (0 = no bell) */
	bellTolls: number;
};

export const WIN_TIER_INTENSITY: Record<number, WinTierIntensity> = {
	2: { rays: 3, rayAlpha: 0.20, embers: 14, dust: 2, popScale: 0.42, streaks: 5, kick: 5, push: 1.05, bellTolls: 0 },
	3: { rays: 4, rayAlpha: 0.27, embers: 22, dust: 3, popScale: 0.55, streaks: 8, kick: 8, push: 1.07, bellTolls: 0 },
	4: { rays: 5, rayAlpha: 0.34, embers: 32, dust: 4, popScale: 0.70, streaks: 12, kick: 12, push: 1.09, bellTolls: 0 },
	5: { rays: 7, rayAlpha: 0.42, embers: 44, dust: 5, popScale: 0.86, streaks: 16, kick: 16, push: 1.11, bellTolls: 0 },
	6: { rays: 9, rayAlpha: 0.50, embers: 58, dust: 6, popScale: 1.02, streaks: 20, kick: 21, push: 1.13, bellTolls: 0.55 },
	7: { rays: 12, rayAlpha: 0.60, embers: 76, dust: 8, popScale: 1.24, streaks: 26, kick: 27, push: 1.16, bellTolls: 0.85 },
};

export const winTierIntensity = (tier: number): WinTierIntensity =>
	WIN_TIER_INTENSITY[tier] ?? WIN_TIER_INTENSITY[2];

/** Hero plate asset key for a tier slug (see winCelebrationMap). */
export const winTierPlateKey = (slug: string) =>
	`winTier${slug.charAt(0).toUpperCase()}${slug.slice(1)}`;

/** Stable pseudo-random in 0..1 — layout seeds, never gameplay. */
export const winRand = (seed: number) => {
	const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
	return value - Math.floor(value);
};
