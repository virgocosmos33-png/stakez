import { SYMBOL_CARD_W } from './constants';
import { fxRandom } from './featureVfx';

/**
 * CellSlash port: one cut, trigger() then hold.
 * Flash + traveling blade + sparks, then the seam stays.
 */
export const SLASH = {
	color: 0xffb628,
	colorDeep: 0x8a5300,
	cutDeg: -34,
	cutW: 7,
	cutOp: 0.9,
	flashPeak: 0.86,
	seamW: SYMBOL_CARD_W * 1.48,
	seamH: 22,
	hitMs: 82,
	flashMs: 160,
	travelMs: 200,
	sparkMs: 200,
	markMs: 90,
	stackMs: 420,
	sparks: [
		{ sx: 0.12, a: 88.6, d: 56 },
		{ sx: 0.247, a: -77.4, d: 68 },
		{ sx: 0.373, a: 88.0, d: 62 },
		{ sx: 0.5, a: -69.3, d: 37 },
		{ sx: 0.627, a: 86.1, d: 42 },
		{ sx: 0.753, a: -101.8, d: 54 },
		{ sx: 0.88, a: 79.9, d: 30 },
	],
	ticks: [
		{ tx: 0.325, th: 13 },
		{ tx: 0.497, th: 11 },
	],
} as const;

const BLADE_POLY: ReadonlyArray<readonly [number, number]> = [
	[0, 0.46],
	[0.1, 0.16],
	[0.24, 0.38],
	[0.38, 0.04],
	[0.54, 0.34],
	[0.7, 0],
	[0.88, 0.3],
	[1, 0.42],
	[0.94, 0.6],
	[0.76, 0.5],
	[0.6, 0.92],
	[0.44, 0.54],
	[0.28, 0.88],
	[0.14, 0.56],
	[0, 0.64],
];

const CUT_POLY: ReadonlyArray<readonly [number, number]> = [
	[0.03, 0.4],
	[0.14, 0.14],
	[0.28, 0.46],
	[0.41, 0.06],
	[0.55, 0.4],
	[0.69, 0.04],
	[0.84, 0.36],
	[0.97, 0.18],
	[0.97, 0.82],
	[0.82, 0.58],
	[0.7, 0.96],
	[0.54, 0.54],
	[0.4, 0.94],
	[0.26, 0.52],
	[0.12, 0.86],
	[0.03, 0.6],
];

const poly = (
	pts: ReadonlyArray<readonly [number, number]>,
	x: number,
	y: number,
	w: number,
	h: number,
) => pts.flatMap(([u, v]) => [x + u * w, y + v * h]);

/** cubic-bezier(0.12, 0.82, 0.22, 1) */
const bladeEase = (t: number) => {
	const target = Math.min(1, Math.max(0, t));
	let x = target;
	for (let i = 0; i < 5; i += 1) {
		const xx = 3 * (1 - x) * (1 - x) * x * 0.12 + 3 * (1 - x) * x * x * 0.22 + x * x * x;
		const dx = 3 * (1 - x) * (1 - x) * 0.12 + 6 * (1 - x) * x * 0.1 + 3 * x * x * 0.78;
		if (Math.abs(dx) < 1e-6) break;
		x -= (xx - target) / dx;
	}
	return 3 * (1 - x) * (1 - x) * x * 0.82 + 3 * (1 - x) * x * x + x * x * x;
};

const flashAlpha = (ms: number) => {
	const u = ms / SLASH.flashMs;
	if (u <= 0 || u >= 1) return 0;
	if (u < 0.25) return SLASH.flashPeak * (u / 0.25);
	return SLASH.flashPeak * (1 - (u - 0.25) / 0.75);
};

export const drawSlashLip = (g: import('pixi.js').Graphics) => {
	const cutW = SLASH.seamW * 0.92;
	const cutH = SLASH.cutW;
	const lipH = cutH * 2.6;
	g.rect(-cutW / 2, -lipH / 2, cutW, lipH * 0.4);
	g.fill({ color: 0x000000, alpha: 0.55 });
	g.rect(-cutW / 2, lipH * 0.1, cutW, lipH * 0.4);
	g.fill({ color: 0x000000, alpha: 0.6 });
};

export const drawSlashEnergy = (g: import('pixi.js').Graphics, ms: number, marked: boolean) => {
	const seamW = SLASH.seamW;
	const seamH = SLASH.seamH;
	const flash = flashAlpha(ms);
	if (flash > 0.01) {
		g.rect(-seamW * 0.56, -seamH * 1.4, seamW * 1.12, seamH * 2.8);
		g.fill({ color: 0xffffff, alpha: flash * 0.55 });
		g.rect(-seamW * 0.5, -seamH * 0.7, seamW, seamH * 1.4);
		g.fill({ color: SLASH.color, alpha: flash * 0.7 });
	}

	const travel = ms / SLASH.travelMs;
	if (travel > 0 && travel < 1) {
		const u = bladeEase(travel);
		const left = seamW * (-0.42 + 1.5 * u - 0.5);
		const bw = seamW * 0.4;
		const bh = seamH * 4.2;
		const by = -seamH / 2 - seamH * 1.6;
		const fade = travel < 0.58 ? 1 : 1 - (travel - 0.58) / 0.42;
		g.poly(poly(BLADE_POLY, left, by, bw, bh));
		g.fill({ color: SLASH.color, alpha: fade });
		g.poly(poly(BLADE_POLY, left + bw * 0.12, by + bh * 0.18, bw * 0.76, bh * 0.64));
		g.fill({ color: 0xffffff, alpha: fade * 0.85 });
	}

	for (const spark of SLASH.sparks) {
		const local = (ms - spark.d) / SLASH.sparkMs;
		if (local < 0 || local > 1) continue;
		const fade = 1 - local;
		const x = -seamW / 2 + spark.sx * seamW;
		const ang = (spark.a * Math.PI) / 180;
		const lift = -20 * local;
		const h = 12 * (1 - 0.72 * local);
		const dx = Math.sin(ang) * lift;
		const dy = -Math.cos(ang) * lift;
		g.rect(x - 1 + dx, -h / 2 + dy, 2, h);
		g.fill({ color: 0xffffff, alpha: fade });
		g.rect(x - 1 + dx, -h / 2 + dy + h * 0.45, 2, h * 0.55);
		g.fill({ color: SLASH.color, alpha: fade });
	}

	if (!marked) return;
	const cutW = seamW * 0.92;
	const cutH = SLASH.cutW;
	g.poly(poly(CUT_POLY, -cutW / 2, -cutH / 2, cutW, cutH));
	g.fill({ color: SLASH.color, alpha: SLASH.cutOp });
	g.poly(poly(CUT_POLY, -cutW / 2 + 2, -cutH / 2 + 1.2, cutW - 4, cutH - 2.4));
	g.fill({ color: 0xffffff, alpha: 0.72 });
	for (const tick of SLASH.ticks) {
		g.rect(-cutW / 2 + tick.tx * cutW - 1, cutH * 0.2, 2, tick.th);
		g.fill({ color: SLASH.color, alpha: 0.78 });
	}
};

export const SLASH_ROT = (SLASH.cutDeg * Math.PI) / 180;

export const GASH_KEY = 'splitBloodGash';
export const GASH_H = SLASH.seamW * (216 / 1024);

export const DRIP_KEYS = [
	'splitDrip1',
	'splitDrip2',
	'splitDrip3',
	'splitDrip4',
	'splitDrip5',
	'splitDrip6',
	'splitDrip7',
	'splitDrip8',
] as const;

export type SplitDripKey = (typeof DRIP_KEYS)[number];

export const DRIP_FALL_MS = 480;
export const DRIP_FALL = 0.26;

/** Seeded drip origins along the cut. Gravity is screen-down, not along the slash. */
export const dripOrigins = (reel: number, row: number) => {
	const seed = reel * 41 + row * 13 + 7;
	return [0, 1, 2].map((i) => {
		const u = -0.3 + i * 0.28 + (fxRandom(seed + i) - 0.5) * 0.1;
		const along = u * SLASH.seamW * 0.82;
		const pick = Math.floor(fxRandom(seed + 11 + i) * DRIP_KEYS.length);
		return {
			key: DRIP_KEYS[pick] ?? DRIP_KEYS[0],
			x: Math.cos(SLASH_ROT) * along,
			y0: Math.sin(SLASH_ROT) * along + 8,
			w: SLASH.seamW * (0.12 + fxRandom(seed + 21 + i) * 0.05),
			h: SLASH.seamW * (0.16 + fxRandom(seed + 31 + i) * 0.05),
			delay: i * 40,
		};
	});
};
