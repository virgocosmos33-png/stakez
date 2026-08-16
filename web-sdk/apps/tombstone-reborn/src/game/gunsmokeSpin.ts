/**
 * Gunsmoke cell-hit stamps. No live pistol. Rounds come in from off-screen
 * left, right, bottom-left and bottom-right (muzzle out of frame) into each
 * cell, then the art cracks and a hole stamps.
 * Hits are not a metronome: each volley gets a seeded paw---paw-paw
 * rhythm, never a stacked double. Specials (H1–H5) also get blood stains
 * clipped to the iron cell-frame sprite; the stains stay.
 */
import { CELL_PITCH_X, SYMBOL_CARD_W, SYMBOL_CARD_H, SYMBOL_SIZE, HIGH_SYMBOLS } from './constants';
import { fxRandom } from './featureVfx';
import { GUNSMOKE_ART } from './gunsmokeArt.generated';
import type { SymbolName } from './types';

/** Hollow iron slot — opaque ring, open centre. Blood only paints on the frame. */
export const CELL_FRAME_MASK_KEY = 'boardSlotFrame';
export const CELL_FRAME_MASK_W = CELL_PITCH_X;
export const CELL_FRAME_MASK_H = SYMBOL_SIZE;

/** Fallback hold if a lone wound has no planned rhythm. */
export const WOUND_BEAT_MS = 280;
/** Shortest legal space after a hole — anything tighter reads as a double. */
export const WOUND_GAP_MS = 220;
export const WOUND_GAP_SPAN = 120;
/** Breath before the next shot. */
export const WOUND_HOLD_MS = 420;
export const WOUND_HOLD_SPAN = 220;
export const BLOOD_SPLASH_IN_MS = 90;
export const BLOOD_SPLASH_OUT_MS = 180;
/** Dried stain left on the iron after the splash. Do not fade to empty. */
export const BLOOD_STAIN_RESIDUAL = 0.88;
export const BULLET_MS = 36;
export const BULLET_DIST_MS = 0.03;
export const BULLET_MAX_MS = 68;
export const BULLET_W = SYMBOL_CARD_W * 0.4;
/** Near-camera size, then shrinks as the round hits the card. */
export const BULLET_NEAR_SCALE = 2.25;
export const BULLET_FAR_SCALE = 0.68;
/** Past the left/right canvas edge — never the HUD under the board. */
export const FPS_MUZZLE_PAST_VIEW = SYMBOL_SIZE * 1.8;
export const FPS_MUZZLE_FROM_BOTTOM = 0.25;
/** Just under the timber corner, still on the wing. */
export const FPS_MUZZLE_CORNER_BELOW = SYMBOL_SIZE * 0.35;
export const FPS_MUZZLE_JITTER = SYMBOL_CARD_H * 0.08;
/** Glass dent: snap in, then leave the shards sitting. */
export const DENT_PUNCH_MS = 70;
export const DENT_SETTLE_MS = 260;
export const DENT_RESIDUAL = 0.46;
export const CRUSH_IN_MS = 55;
export const CRUSH_OUT_MS = 180;

export type MuzzleSide = 'left' | 'right' | 'bottomLeft' | 'bottomRight';

const MUZZLE_SLOTS: MuzzleSide[] = ['left', 'right', 'bottomLeft', 'bottomRight'];

export const shuffleMuzzles = (seed: number): MuzzleSide[] => {
	const slots = [...MUZZLE_SLOTS];
	for (let i = slots.length - 1; i > 0; i -= 1) {
		const j = Math.floor(fxRandom(seed + i * 9) * (i + 1));
		const a = slots[i];
		const b = slots[j];
		if (a === undefined || b === undefined) continue;
		slots[i] = b;
		slots[j] = a;
	}
	return slots;
};

/** Off-screen muzzle: side (1/4 up) or bottom corner, always out of frame. */
export const fpsMuzzlePoint = (
	layout: {
		pivot: { x: number; y: number };
		x: number;
		y: number;
		visualTop: number;
		visualBottom: number;
		scale: number;
	},
	view: { left: number; right: number },
	side: MuzzleSide,
	seed: number,
) => {
	const top = layout.pivot.y + (layout.visualTop - layout.y) / layout.scale;
	const bot = layout.pivot.y + (layout.visualBottom - layout.y) / layout.scale;
	const viewLeft = layout.pivot.x + (view.left - layout.x) / layout.scale;
	const viewRight = layout.pivot.x + (view.right - layout.x) / layout.scale;
	const fromLeft = side === 'left' || side === 'bottomLeft';
	const fromFloor = side === 'bottomLeft' || side === 'bottomRight';
	const sideY = bot - (bot - top) * FPS_MUZZLE_FROM_BOTTOM;
	const cornerY = bot + FPS_MUZZLE_CORNER_BELOW;
	return {
		x: fromLeft ? viewLeft - FPS_MUZZLE_PAST_VIEW : viewRight + FPS_MUZZLE_PAST_VIEW,
		y: (fromFloor ? cornerY : sideY) + (fxRandom(seed) - 0.5) * FPS_MUZZLE_JITTER,
	};
};

export const pickBullet = (travelAngle: number) => {
	type BulletArt = (typeof GUNSMOKE_ART.bullets)[number];
	let best: BulletArt = GUNSMOKE_ART.bullets[0] as BulletArt;
	let bestDist = Number.POSITIVE_INFINITY;
	for (const bullet of GUNSMOKE_ART.bullets) {
		let delta = travelAngle - bullet.native;
		while (delta > Math.PI) delta -= Math.PI * 2;
		while (delta < -Math.PI) delta += Math.PI * 2;
		const dist = Math.abs(delta);
		if (dist < bestDist) {
			bestDist = dist;
			best = bullet;
		}
	}
	return best;
};

export const isHighPaySymbol = (name: SymbolName) =>
	(HIGH_SYMBOLS as readonly string[]).includes(name);

/** Same shattered-glass holes as click-to-shoot — they stay on the cell. */
export const GUNSMOKE_HOLE_KEYS = [
	'bulletCrack1',
	'bulletCrack2',
	'bulletCrack3',
	'bulletCrack4',
	'bulletCrack5',
] as const;

export const GUNSMOKE_BLOOD_KEYS = [
	'gsWoundBlood1',
	'gsWoundBlood2',
	'gsWoundBlood3',
	'gsWoundBlood4',
	'gsWoundBlood5',
	'gsWoundBlood6',
	'gsWoundBlood7',
	'gsWoundBlood8',
] as const;

export type WoundLayer = {
	key: string;
	x: number;
	y: number;
	rotation: number;
	width: number;
	height: number;
	alpha: number;
	kind: 'hole' | 'blood';
};

/** Blood blobs sit on the iron ring so the frame mask keeps a stain, not a face splash. */
export const frameBloodLayers = (reel: number, row: number, hit = 0): WoundLayer[] => {
	const seed = reel * 41 + row * 13 + 7 + hit * 19;
	const count = 2 + (fxRandom(seed) > 0.45 ? 1 : 0);
	return Array.from({ length: count }, (_, i) => {
		const key = GUNSMOKE_BLOOD_KEYS[Math.floor(fxRandom(seed + i * 3) * GUNSMOKE_BLOOD_KEYS.length)];
		const ang = (i / count) * Math.PI * 2 + fxRandom(seed + i * 11) * 0.7;
		const dist = SYMBOL_SIZE * (0.36 + fxRandom(seed + i * 13) * 0.08);
		return {
			key: key ?? GUNSMOKE_BLOOD_KEYS[0],
			x: Math.cos(ang) * dist,
			y: Math.sin(ang) * dist,
			rotation: fxRandom(seed + i * 21) * Math.PI * 2,
			width: CELL_PITCH_X * (0.62 + fxRandom(seed + i * 23) * 0.18),
			height: SYMBOL_SIZE * (0.42 + fxRandom(seed + i * 27) * 0.16),
			alpha: 0.86,
			kind: 'blood' as const,
		};
	});
};

export const woundLayers = (reel: number, row: number, blood: boolean): WoundLayer[] => {
	const seed = reel * 41 + row * 13 + 7;
	const holeKey = GUNSMOKE_HOLE_KEYS[Math.floor(fxRandom(seed + 3) * GUNSMOKE_HOLE_KEYS.length)];
	const jx = (fxRandom(seed + 11) - 0.5) * SYMBOL_CARD_W * 0.18;
	const jy = (fxRandom(seed + 17) - 0.5) * SYMBOL_CARD_H * 0.18;
	const holeSize = SYMBOL_CARD_W * 0.8;
	const holes: WoundLayer[] = [
		{
			key: holeKey,
			x: jx,
			y: jy,
			rotation: fxRandom(seed + 31) * Math.PI * 2,
			width: holeSize,
			height: holeSize,
			alpha: 1,
			kind: 'hole',
		},
	];
	if (!blood) return holes;
	return [...frameBloodLayers(reel, row), ...holes];
};

export type WoundShot = {
	beatMs: number;
	flightScale: number;
	side: MuzzleSide;
	/** Tiny rest — next knife starts almost on this one's heels. */
	burst?: boolean;
};

/** Knives in a cluster sit this close after the hit stack, not a full beat. */
export const KNIFE_BURST_MS = 28;
export const KNIFE_BURST_SPAN = 36;
/** 4+ throws pack into 2–3 knife bursts so a big split does not crawl. */
export const KNIFE_CLUSTER_FROM = 4;

export const volleySeed = (cells: { reel: number; row: number }[]) =>
	cells.reduce((sum, cell, i) => sum + (cell.reel + 1) * 19 + (cell.row + 1) * 7 + i * 3, 101);

type GapKind = 'burst' | 'beat' | 'hold';

const shotsFromGaps = (count: number, seed: number, kinds: GapKind[]): WoundShot[] => {
	const gaps = Math.max(0, count - 1);
	const muzzles = shuffleMuzzles(seed + 61);
	return Array.from({ length: count }, (_, i) => {
		const jitter = fxRandom(seed + 31 + i * 13);
		const flightScale = 0.78 + fxRandom(seed + 47 + i * 19) * 0.16;
		const side = muzzles[i % muzzles.length] ?? 'right';
		if (i >= gaps) {
			return { beatMs: 80 + jitter * 40, flightScale, side };
		}
		const kind = kinds[i] ?? 'beat';
		if (kind === 'burst') {
			return {
				beatMs: KNIFE_BURST_MS + jitter * KNIFE_BURST_SPAN,
				flightScale,
				side,
				burst: true,
			};
		}
		if (kind === 'hold') {
			return { beatMs: WOUND_HOLD_MS + jitter * WOUND_HOLD_SPAN, flightScale, side };
		}
		return { beatMs: WOUND_GAP_MS + jitter * WOUND_GAP_SPAN, flightScale, side };
	});
};

const beatHoldGaps = (gaps: number, seed: number): GapKind[] => {
	const kinds: GapKind[] = [];
	if (gaps === 1) {
		kinds.push(fxRandom(seed) < 0.45 ? 'hold' : 'beat');
	} else if (gaps >= 2) {
		const holdAt = Math.floor(fxRandom(seed + 5) * gaps);
		for (let i = 0; i < gaps; i += 1) {
			if (i === holdAt) kinds.push('hold');
			else kinds.push(fxRandom(seed + 11 + i * 17) < 0.32 ? 'hold' : 'beat');
		}
	}
	return kinds;
};

/**
 * Per-shot gaps for one volley. Uneven singles only — beat or hold, never a
 * stacked double. Seeded so the same book replays the same rhythm.
 */
export const planWoundRhythm = (count: number, seed: number): WoundShot[] => {
	if (count <= 0) return [];
	return shotsFromGaps(count, seed, beatHoldGaps(Math.max(0, count - 1), seed));
};

/** Pack leftover throws so the last cluster is never a single stray knife. */
const knifeClusterSizes = (count: number, seed: number): number[] => {
	const sizes: number[] = [];
	let left = count;
	let n = 0;
	while (left > 0) {
		let size = left;
		if (left > 3) {
			size = left === 4 || fxRandom(seed + 71 + n * 9) < 0.4 ? 2 : 3;
		}
		if (left - size === 1) size -= 1;
		sizes.push(size);
		left -= size;
		n += 1;
	}
	return sizes;
};

/**
 * Knife volleys: 1–3 throws keep the gunsmoke beat. 4+ pack into 2–3 knife
 * bursts (tiny gap) with a breath between clusters, so a fat split does not
 * wait out a full beat on every throw.
 */
export const planKnifeRhythm = (count: number, seed: number): WoundShot[] => {
	if (count <= 0) return [];
	if (count < KNIFE_CLUSTER_FROM) return planWoundRhythm(count, seed);
	const sizes = knifeClusterSizes(count, seed);
	const kinds: GapKind[] = [];
	let holdUsed = false;
	for (let c = 0; c < sizes.length; c += 1) {
		const size = sizes[c] ?? 1;
		for (let k = 0; k < size - 1; k += 1) kinds.push('burst');
		if (c >= sizes.length - 1) continue;
		const hold = !holdUsed || fxRandom(seed + 91 + c * 7) < 0.35;
		if (hold) holdUsed = true;
		kinds.push(hold ? 'hold' : 'beat');
	}
	return shotsFromGaps(count, seed, kinds);
};

/** Same hole centre the overlay uses, as 0..1 UV on the card. */
export const woundImpact = (reel: number, row: number, blood: boolean) => {
	const layers = woundLayers(reel, row, blood);
	const hole = layers.find((layer) => layer.kind === 'hole') ?? layers[0];
	return {
		layers,
		hitX: 0.5 + (hole?.x ?? 0) / SYMBOL_CARD_W,
		hitY: 0.5 + (hole?.y ?? 0) / SYMBOL_CARD_H,
		seed: reel * 41 + row * 13 + 7,
	};
};
