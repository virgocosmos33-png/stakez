import type { Graphics } from 'pixi.js';

/**
 * THE WHITE ROOM clinical FX language — NOT Madam Mirror flame/lightning/prismatic.
 * Restraint straps, fluorescent tubes, memory-glitch scanlines, ceramic dust.
 */

export type EdgeSample = { x: number; y: number; nx: number; ny: number };

export type ClinicalPalette = {
	charcoal: number;
	steel: number;
	silver: number;
	bone: number;
	blood?: number;
};

export const WHITE_ROOM_PALETTE: ClinicalPalette = {
	charcoal: 0x3a3632,
	steel: 0x8a8680,
	silver: 0xc8c4bc,
	bone: 0xf4f1ec,
	blood: 0x6b2a28,
};

const seeded = (k: number) => {
	const value = Math.sin(k * 12.9898 + 78.233) * 43758.5453;
	return value - Math.floor(value);
};

/** Dashed leather restraint straps along a closed contour — buckle ticks + stitch gaps. */
export const drawRestraintStraps = (
	g: Graphics,
	samples: EdgeSample[],
	palette: ClinicalPalette,
	opts: {
		seed: number;
		time: number;
		alpha: number;
		strapWidth?: number;
		dashLen?: number;
		gapLen?: number;
		buckleEvery?: number;
		dustCount?: number;
	},
) => {
	if (opts.alpha <= 0.01 || samples.length < 3) return;
	const strapW = opts.strapWidth ?? 5;
	const dashLen = opts.dashLen ?? 18;
	const gapLen = opts.gapLen ?? 10;
	const buckleEvery = opts.buckleEvery ?? 7;
	const dustCount = opts.dustCount ?? 10;
	const n = samples.length;
	const period = dashLen + gapLen;
	let dist = 0;

	for (let i = 0; i < n; i++) {
		const a = samples[i];
		const b = samples[(i + 1) % n];
		const seg = Math.hypot(b.x - a.x, b.y - a.y) || 1;
		const steps = Math.max(1, Math.ceil(seg / 4));
		for (let s = 0; s < steps; s++) {
			const f0 = s / steps;
			const f1 = (s + 1) / steps;
			const mid = (dist + seg * (f0 + f1) * 0.5) % period;
			const inDash = mid < dashLen;
			if (inDash) {
				const x0 = a.x + (b.x - a.x) * f0;
				const y0 = a.y + (b.y - a.y) * f0;
				const x1 = a.x + (b.x - a.x) * f1;
				const y1 = a.y + (b.y - a.y) * f1;
				const nx = a.nx;
				const ny = a.ny;
				// strap body (inset slightly)
				g.moveTo(x0 - nx * 1.5, y0 - ny * 1.5);
				g.lineTo(x1 - nx * 1.5, y1 - ny * 1.5);
				g.stroke({
					width: strapW,
					color: palette.charcoal,
					alpha: 0.72 * opts.alpha,
					cap: 'butt',
				});
				// steel edge stitch
				g.moveTo(x0 - nx * 1.5, y0 - ny * 1.5);
				g.lineTo(x1 - nx * 1.5, y1 - ny * 1.5);
				g.stroke({
					width: Math.max(1.2, strapW * 0.28),
					color: palette.silver,
					alpha: 0.55 * opts.alpha,
					cap: 'butt',
				});
			}
			dist += seg / steps;
		}

		// metal buckle tick marks
		if (i % buckleEvery === 0) {
			const pulse = 0.7 + 0.3 * Math.sin(opts.time * 9 + opts.seed + i);
			const bx = a.x - a.nx * 2;
			const by = a.y - a.ny * 2;
			const tx = -a.ny;
			const ty = a.nx;
			g.moveTo(bx - tx * 5, by - ty * 5);
			g.lineTo(bx + tx * 5, by + ty * 5);
			g.stroke({
				width: 2.4,
				color: palette.steel,
				alpha: 0.85 * opts.alpha * pulse,
			});
			// sparse dried-blood fleck on some buckles
			if (palette.blood && seeded(opts.seed + i * 3) > 0.72) {
				g.circle(bx + a.nx * 3, by + a.ny * 3, 1.6);
				g.fill({ color: palette.blood, alpha: 0.45 * opts.alpha });
			}
		}
	}

	// ceramic dust motes drifting along the strap
	for (let k = 0; k < dustCount; k++) {
		const idx = Math.floor(seeded(opts.seed * 2.1 + k * 19) * n);
		const s = samples[idx];
		const life = (opts.time * (0.4 + seeded(k + 2) * 0.6) + seeded(opts.seed + k)) % 1;
		const lift = life * 14;
		const sway = Math.sin(opts.time * 2.2 + k) * 4;
		const x = s.x + s.nx * (3 + lift) + -s.ny * sway;
		const y = s.y + s.ny * (3 + lift) + s.nx * sway;
		const r = 1 + seeded(k * 5) * 2.2;
		g.circle(x, y, r);
		g.fill({
			color: k % 3 === 0 ? palette.bone : palette.silver,
			alpha: 0.55 * opts.alpha * (1 - life),
		});
	}
};

/**
 * Continuous fluorescent tubes along a sharp rectangle perimeter with clinical flicker.
 * Must stay CONTINUOUS — segmented strokes read as the same white dashed "cut path"
 * rim bug as the baked frame PNG cutline (bonus-only via BoardFramePlasma).
 */
export const drawFluorescentFrame = (
	g: Graphics,
	hw: number,
	hh: number,
	palette: ClinicalPalette,
	opts: {
		time: number;
		alpha: number;
		tubeWidth?: number;
		flickerHz?: number;
		/** retained for fx config compat; ignored — segments looked like a cutline */
		segmentGap?: number;
		blackoutChance?: number;
	},
) => {
	if (opts.alpha <= 0.01) return;
	const tubeW = opts.tubeWidth ?? 6;
	const hz = opts.flickerHz ?? 11;
	const blackout = opts.blackoutChance ?? 0.04;

	// global fluorescent flicker + rare blackouts
	const flicker =
		seeded(Math.floor(opts.time * hz * 3)) > 1 - blackout
			? 0.08
			: 0.72 + 0.28 * Math.sin(opts.time * hz * Math.PI * 2);

	const master = opts.alpha * flicker;
	const sides: [number, number, number, number][] = [
		[-hw, -hh, hw * 2, 0], // top
		[hw, -hh, 0, hh * 2], // right
		[hw, hh, -hw * 2, 0], // bottom
		[-hw, hh, 0, -hh * 2], // left
	];

	for (let side = 0; side < 4; side++) {
		const [x0, y0, dx, dy] = sides[side];
		const x1 = x0 + dx;
		const y1 = y0 + dy;
		const len = Math.hypot(dx, dy) || 1;
		const ux = dx / len;
		const uy = dy / len;
		const nx = uy;
		const ny = -ux;
		const localFlick = 0.88 + 0.12 * Math.sin(opts.time * (hz + side) * 0.7);
		const aTube = master * localFlick;

		// soft tube halo — continuous side (no segment gaps / dashed cut look)
		g.moveTo(x0 + nx * 2, y0 + ny * 2);
		g.lineTo(x1 + nx * 2, y1 + ny * 2);
		g.stroke({ width: tubeW * 2.8, color: palette.silver, alpha: 0.12 * aTube });
		// tube body
		g.moveTo(x0, y0);
		g.lineTo(x1, y1);
		g.stroke({ width: tubeW, color: palette.bone, alpha: 0.45 * aTube });
		// soft core (NOT bright white dashes — that resurrected the cutline complaint)
		g.moveTo(x0, y0);
		g.lineTo(x1, y1);
		g.stroke({
			width: Math.max(1.0, tubeW * 0.3),
			color: palette.silver,
			alpha: 0.35 * aTube,
		});
	}
};

/** Horizontal memory-glitch / CRT tear bands across a cell. */
export const drawMemoryGlitchCell = (
	g: Graphics,
	size: number,
	alpha: number,
	time: number,
	seed: number,
) => {
	if (alpha <= 0.01) return;
	const half = size / 2;
	const bands = 5;
	for (let i = 0; i < bands; i++) {
		const y = -half + size * ((i + 0.5) / bands);
		const h = 2 + seeded(seed + i * 3) * 5;
		const shear = (seeded(seed + i + Math.floor(time * 24)) - 0.5) * size * 0.22 * alpha;
		g.rect(-half + shear, y - h / 2, size, h);
		g.fill({
			color: i % 2 === 0 ? 0xffffff : WHITE_ROOM_PALETTE.silver,
			alpha: 0.35 * alpha * (0.6 + 0.4 * seeded(seed + i * 7)),
		});
	}
	// clinical flash wash
	g.roundRect(-half + 2, -half + 2, size - 4, size - 4, 4);
	g.fill({ color: WHITE_ROOM_PALETTE.bone, alpha: 0.12 * alpha });
	// observation-glass edge
	g.roundRect(-half + 1, -half + 1, size - 2, size - 2, 4);
	g.stroke({ color: WHITE_ROOM_PALETTE.steel, width: 2, alpha: 0.7 * alpha });
};

/** Full-canvas padded-cell strobe: fluorescent bars + scanline wipe (replaces lightning/prism). */
export const drawPaddedCellStrobe = (
	g: Graphics,
	w: number,
	h: number,
	opts: {
		time: number;
		strobeAlpha: number;
		glitchAlpha: number;
		bandCount?: number;
		scanlineCount?: number;
	},
) => {
	const bands = opts.bandCount ?? 7;
	const scans = opts.scanlineCount ?? 18;

	if (opts.strobeAlpha > 0.01) {
		// hard clinical flash
		g.rect(0, 0, w, h);
		g.fill({ color: 0xf4f1ec, alpha: 0.18 * opts.strobeAlpha });
		// horizontal fluorescent bars sweeping
		for (let i = 0; i < bands; i++) {
			const phase = (opts.time * 1.4 + i / bands) % 1;
			const y = phase * h;
			const bh = h * (0.04 + 0.03 * seeded(i + 2));
			g.rect(0, y - bh / 2, w, bh);
			g.fill({ color: 0xffffff, alpha: 0.22 * opts.strobeAlpha * (1 - Math.abs(phase - 0.5) * 1.2) });
		}
	}

	if (opts.glitchAlpha > 0.01) {
		for (let i = 0; i < scans; i++) {
			const y = seeded(i * 13 + Math.floor(opts.time * 30)) * h;
			const sh = 1 + seeded(i * 5) * 4;
			const shear = (seeded(i * 17 + Math.floor(opts.time * 40)) - 0.5) * w * 0.08;
			g.rect(shear, y, w, sh);
			g.fill({
				color: i % 4 === 0 ? WHITE_ROOM_PALETTE.steel : 0xffffff,
				alpha: 0.28 * opts.glitchAlpha,
			});
		}
		// vertical tear columns (memory wipe)
		for (let i = 0; i < 3; i++) {
			const x = seeded(i * 29 + Math.floor(opts.time * 8)) * w;
			g.rect(x - 2, 0, 4 + seeded(i) * 10, h);
			g.fill({ color: 0xffffff, alpha: 0.08 * opts.glitchAlpha });
		}
	}
};

export type IntakeProjectileKind = 'buckle' | 'tube' | 'stamp';
export type PaddedDebrisKind = 'foam' | 'strap' | 'bucklePlate';

/**
 * HOLD: clipboard intake stamp lock + fluorescent tube frame.
 * ZERO glass pane / frost crack / observation glass.
 */
export const drawIntakeStampLock = (
	g: Graphics,
	size: number,
	opts: {
		alpha?: number;
		stampProgress?: number;
		seed?: number;
		time?: number;
		tubeWidth?: number;
	} = {},
) => {
	const a = opts.alpha ?? 0.95;
	if (a <= 0.01) return;
	const half = size / 2;
	const seed = opts.seed ?? 404;
	const stamp = Math.max(0, Math.min(1, opts.stampProgress ?? 1));
	const t = opts.time ?? 0;
	const p = WHITE_ROOM_PALETTE;
	const tubeW = opts.tubeWidth ?? 5;

	// padded wall recess (fabric, not glass)
	g.roundRect(-half + 2, -half + 2, size - 4, size - 4, 10);
	g.fill({ color: 0x1c1a18, alpha: 0.72 * a });
	// quilted padding dots
	for (let i = 0; i < 9; i++) {
		const qx = -half + 14 + (i % 3) * ((size - 28) / 2);
		const qy = -half + 14 + Math.floor(i / 3) * ((size - 28) / 2);
		g.circle(qx, qy, 3.2);
		g.fill({ color: p.charcoal, alpha: 0.35 * a * stamp });
	}

	// fluorescent tube frame (steel housing + hot filament) — not glass shards
	const flicker =
		seeded(Math.floor(t * 14) + seed) > 0.92
			? 0.12
			: 0.75 + 0.25 * Math.sin(t * 18 + seed);
	const tubeA = a * flicker * stamp;
	const inset = half - 5;
	const sides: [number, number, number, number][] = [
		[-inset, -inset, inset * 2, 0],
		[inset, -inset, 0, inset * 2],
		[inset, inset, -inset * 2, 0],
		[-inset, inset, 0, -inset * 2],
	];
	for (const [x0, y0, dx, dy] of sides) {
		g.moveTo(x0, y0);
		g.lineTo(x0 + dx, y0 + dy);
		g.stroke({ width: tubeW + 3, color: p.charcoal, alpha: 0.9 * tubeA });
		g.moveTo(x0, y0);
		g.lineTo(x0 + dx, y0 + dy);
		g.stroke({ width: tubeW, color: p.bone, alpha: 0.55 * tubeA });
		g.moveTo(x0, y0);
		g.lineTo(x0 + dx, y0 + dy);
		g.stroke({ width: Math.max(1.2, tubeW * 0.35), color: 0xffffff, alpha: 0.85 * tubeA });
	}

	// clipboard stamp plate slam
	const slam = 0.85 + 0.15 * stamp;
	const sw = size * 0.62 * slam;
	const sh = size * 0.34 * slam;
	const sy = -size * 0.02 * (1 - stamp);
	g.roundRect(-sw / 2, sy - sh / 2, sw, sh, 3);
	g.fill({ color: p.bone, alpha: 0.92 * a * stamp });
	g.roundRect(-sw / 2, sy - sh / 2, sw, sh, 3);
	g.stroke({ width: 2.4, color: p.blood ?? 0x6b2a28, alpha: 0.95 * a * stamp });
	// "INTAKE" bar glyph + 404 ticks (procedural, not text assets)
	const barW = sw * 0.72;
	g.rect(-barW / 2, sy - 5, barW, 4);
	g.fill({ color: p.blood ?? 0x6b2a28, alpha: 0.85 * a * stamp });
	g.rect(-barW / 2, sy + 3, barW * 0.45, 3);
	g.fill({ color: p.charcoal, alpha: 0.8 * a * stamp });
	// perforation teeth along stamp edge
	for (let i = 0; i < 7; i++) {
		const px = -sw / 2 + 4 + i * ((sw - 8) / 6);
		g.rect(px - 1, sy + sh / 2 - 2, 2, 4);
		g.fill({ color: p.charcoal, alpha: 0.7 * a * stamp });
	}

	// corner REC lock brackets
	const arm = size * 0.16;
	const br = half - 3;
	for (const [sx, sy2] of [
		[-1, -1],
		[1, -1],
		[1, 1],
		[-1, 1],
	] as const) {
		const x = sx * br;
		const y = sy2 * br;
		g.moveTo(x, y + sy2 * arm);
		g.lineTo(x, y);
		g.lineTo(x + sx * arm, y);
		g.stroke({ width: 2.6, color: p.bone, alpha: 0.9 * a * stamp });
	}
};

/**
 * SHOOT: restraint buckle / fluorescent tube stub / clipboard stamp.
 * ZERO knife spikes, glass chips, or triangular slivers.
 */
export const drawIntakeProjectile = (
	g: Graphics,
	opts: {
		x: number;
		y: number;
		rotation: number;
		size: number;
		alpha: number;
		kind: IntakeProjectileKind;
		seed?: number;
	},
) => {
	if (opts.alpha <= 0.01) return;
	const { x, y, rotation: rot, size: s, alpha, kind } = opts;
	const seed = opts.seed ?? 1;
	const c = Math.cos(rot);
	const sn = Math.sin(rot);
	const local = (lx: number, ly: number) => ({
		px: x + lx * c - ly * sn,
		py: y + lx * sn + ly * c,
	});
	const p = WHITE_ROOM_PALETTE;

	if (kind === 'buckle') {
		// rectangular steel buckle plate + strap tongue
		const a0 = local(-s * 1.1, -s * 0.55);
		const a1 = local(s * 0.7, -s * 0.55);
		const a2 = local(s * 0.7, s * 0.55);
		const a3 = local(-s * 1.1, s * 0.55);
		g.poly([a0.px, a0.py, a1.px, a1.py, a2.px, a2.py, a3.px, a3.py]);
		g.fill({ color: p.steel, alpha });
		const i0 = local(-s * 0.55, -s * 0.28);
		const i1 = local(s * 0.35, -s * 0.28);
		const i2 = local(s * 0.35, s * 0.28);
		const i3 = local(-s * 0.55, s * 0.28);
		g.poly([i0.px, i0.py, i1.px, i1.py, i2.px, i2.py, i3.px, i3.py]);
		g.fill({ color: p.charcoal, alpha: alpha * 0.95 });
		// leather strap trailing behind
		const t0 = local(-s * 1.1, -s * 0.22);
		const t1 = local(-s * 2.2, -s * 0.22);
		const t2 = local(-s * 2.2, s * 0.22);
		const t3 = local(-s * 1.1, s * 0.22);
		g.poly([t0.px, t0.py, t1.px, t1.py, t2.px, t2.py, t3.px, t3.py]);
		g.fill({ color: p.charcoal, alpha: alpha * 0.75 });
		return;
	}

	if (kind === 'tube') {
		// fluorescent housing cylinder (metal + filament), not glass shard
		const len = s * 2.4;
		const r = s * 0.38;
		const b0 = local(-len * 0.5, -r);
		const b1 = local(len * 0.5, -r);
		const b2 = local(len * 0.5, r);
		const b3 = local(-len * 0.5, r);
		g.poly([b0.px, b0.py, b1.px, b1.py, b2.px, b2.py, b3.px, b3.py]);
		g.fill({ color: p.silver, alpha: alpha * 0.9 });
		const c0 = local(-len * 0.42, -r * 0.35);
		const c1 = local(len * 0.42, -r * 0.35);
		const c2 = local(len * 0.42, r * 0.35);
		const c3 = local(-len * 0.42, r * 0.35);
		g.poly([c0.px, c0.py, c1.px, c1.py, c2.px, c2.py, c3.px, c3.py]);
		g.fill({ color: 0xffffff, alpha: alpha * 0.85 });
		// end caps
		for (const sign of [-1, 1] as const) {
			const e0 = local(sign * len * 0.5, -r * 1.1);
			const e1 = local(sign * len * 0.5 + sign * s * 0.25, -r * 1.1);
			const e2 = local(sign * len * 0.5 + sign * s * 0.25, r * 1.1);
			const e3 = local(sign * len * 0.5, r * 1.1);
			g.poly([e0.px, e0.py, e1.px, e1.py, e2.px, e2.py, e3.px, e3.py]);
			g.fill({ color: p.charcoal, alpha });
		}
		return;
	}

	// clipboard / file stamp rectangle with blood border
	const w = s * 1.8;
	const h = s * 1.15;
	const s0 = local(-w * 0.5, -h * 0.5);
	const s1 = local(w * 0.5, -h * 0.5);
	const s2 = local(w * 0.5, h * 0.5);
	const s3 = local(-w * 0.5, h * 0.5);
	g.poly([s0.px, s0.py, s1.px, s1.py, s2.px, s2.py, s3.px, s3.py]);
	g.fill({ color: p.bone, alpha });
	g.poly([s0.px, s0.py, s1.px, s1.py, s2.px, s2.py, s3.px, s3.py]);
	g.stroke({ color: p.blood ?? 0x6b2a28, width: 1.8, alpha });
	const ink = seeded(seed + 3) > 0.5 ? p.blood ?? 0x6b2a28 : p.charcoal;
	const m0 = local(-w * 0.32, -h * 0.12);
	const m1 = local(w * 0.32, -h * 0.12);
	const m2 = local(w * 0.32, h * 0.08);
	const m3 = local(-w * 0.32, h * 0.08);
	g.poly([m0.px, m0.py, m1.px, m1.py, m2.px, m2.py, m3.px, m3.py]);
	g.fill({ color: ink, alpha: alpha * 0.9 });
};

/**
 * SHATTER: padded-wall foam chunks + strap strips + buckle plates.
 * ZERO falling glass / triangular shards / ceramic knife chips.
 */
export const drawPaddedTearDebris = (
	g: Graphics,
	opts: {
		size: number;
		color: number;
		alpha: number;
		seed: number;
		kind: PaddedDebrisKind;
	},
) => {
	if (opts.alpha <= 0.01) return;
	const s = opts.size;
	const p = WHITE_ROOM_PALETTE;
	const r = seeded(opts.seed);

	if (opts.kind === 'strap') {
		const w = s * (1.8 + r * 1.2);
		const h = s * (0.28 + seeded(opts.seed + 1) * 0.18);
		g.roundRect(-w / 2, -h / 2, w, h, 1);
		g.fill({ color: p.charcoal, alpha: opts.alpha });
		g.roundRect(-w / 2 + 1, -h / 2 + 0.5, w - 2, h * 0.35, 0);
		g.fill({ color: p.steel, alpha: opts.alpha * 0.45 });
		return;
	}

	if (opts.kind === 'bucklePlate') {
		const w = s * 1.4;
		const h = s * 0.9;
		g.roundRect(-w / 2, -h / 2, w, h, 2);
		g.fill({ color: p.steel, alpha: opts.alpha });
		g.roundRect(-w * 0.28, -h * 0.28, w * 0.56, h * 0.56, 1);
		g.fill({ color: p.charcoal, alpha: opts.alpha * 0.9 });
		return;
	}

	// foam / padded-wall rectangle with torn notches (soft fabric, not glass)
	const w = s * (1.1 + r * 0.9);
	const h = s * (0.7 + seeded(opts.seed + 2) * 0.7);
	g.roundRect(-w / 2, -h / 2, w, h, 3);
	g.fill({ color: opts.color, alpha: opts.alpha });
	// torn edge notches
	for (let i = 0; i < 3; i++) {
		const nx = -w / 2 + seeded(opts.seed + 10 + i) * w;
		g.rect(nx - 1.5, h / 2 - 1, 3, 3 + seeded(opts.seed + 20 + i) * 4);
		g.fill({ color: p.charcoal, alpha: opts.alpha * 0.5 });
	}
};

/** Brief fluorescent blackout blink overlay for tear payoff. */
export const drawFluorescentBlackout = (
	g: Graphics,
	size: number,
	alpha: number,
) => {
	if (alpha <= 0.01) return;
	const half = size / 2;
	g.rect(-half - 6, -half - 6, size + 12, size + 12);
	g.fill({ color: 0x050505, alpha: 0.85 * alpha });
	// single tube flash bar
	g.rect(-half, -3, size, 6);
	g.fill({ color: 0xffffff, alpha: 0.55 * alpha });
};

/**
 * Observation Conduit Handshake — cinematic link between 2+ Cell Seal reels.
 * Fluorescent tube housing + steel coupler buckles + CCTV scan packet + intake stamp.
 * BANNED: arcade flower/gear hubs, trailing yellow/white dots, neon laser blobs.
 */
export const drawObservationConduitHandshake = (
	g: Graphics,
	opts: {
		x0: number;
		y0: number;
		x1: number;
		y1: number;
		time: number;
		/** 0..1 expand progress — conduit draws on as seals expand */
		drawProgress: number;
		alpha?: number;
		seed?: number;
		housingHeight?: number;
		buckleCount?: number;
		scanSpeed?: number;
	},
) => {
	const a = opts.alpha ?? 1;
	const draw = Math.max(0, Math.min(1, opts.drawProgress));
	if (a <= 0.01 || draw <= 0.02) return;

	const p = WHITE_ROOM_PALETTE;
	const seed = opts.seed ?? 7;
	const x0 = opts.x0;
	const y0 = opts.y0;
	const x1 = opts.x1;
	const y1 = opts.y1;
	const dx = x1 - x0;
	const dy = y1 - y0;
	const len = Math.hypot(dx, dy) || 1;
	const ux = dx / len;
	const uy = dy / len;
	const nx = -uy;
	const ny = ux;
	const hh = opts.housingHeight ?? 11;
	const visibleLen = len * draw;
	const t = opts.time;

	// fluorescent flicker + rare blackout (clinical tube, not neon)
	const flicker =
		seeded(Math.floor(t * 13) + seed) > 0.94
			? 0.14
			: 0.78 + 0.22 * Math.sin(t * 12.5 + seed);

	const at = (u: number, offN = 0) => ({
		x: x0 + ux * u + nx * offN,
		y: y0 + uy * u + ny * offN,
	});

	// ── 1. charcoal conduit housing (capsule body) ──
	const bodySteps = Math.max(8, Math.ceil(visibleLen / 10));
	for (let i = 0; i < bodySteps; i++) {
		const u0 = (i / bodySteps) * visibleLen;
		const u1 = ((i + 1) / bodySteps) * visibleLen;
		const a0 = at(u0, -hh * 0.55);
		const a1 = at(u1, -hh * 0.55);
		const a2 = at(u1, hh * 0.55);
		const a3 = at(u0, hh * 0.55);
		g.poly([a0.x, a0.y, a1.x, a1.y, a2.x, a2.y, a3.x, a3.y]);
		g.fill({ color: 0x1a1816, alpha: 0.82 * a * draw });
	}

	// ── 2. dual steel rails (Beams metaphor → instrumentation rails) ──
	for (const side of [-1, 1] as const) {
		const r0 = at(0, side * hh * 0.42);
		const r1 = at(visibleLen, side * hh * 0.42);
		g.moveTo(r0.x, r0.y);
		g.lineTo(r1.x, r1.y);
		g.stroke({ width: 2.4, color: p.steel, alpha: 0.9 * a * draw, cap: 'butt' });
		// frost stitch hairline
		g.moveTo(r0.x, r0.y);
		g.lineTo(r1.x, r1.y);
		g.stroke({
			width: 1,
			color: p.silver,
			alpha: 0.45 * a * draw * flicker,
			cap: 'butt',
		});
	}

	// ── 3. fluorescent filament core (Laser Flow → hot clinical core) ──
	const c0 = at(2, 0);
	const c1 = at(Math.max(2, visibleLen - 2), 0);
	g.moveTo(c0.x, c0.y);
	g.lineTo(c1.x, c1.y);
	g.stroke({
		width: hh * 0.55,
		color: p.silver,
		alpha: 0.16 * a * draw * flicker,
		cap: 'round',
	});
	g.moveTo(c0.x, c0.y);
	g.lineTo(c1.x, c1.y);
	g.stroke({
		width: hh * 0.28,
		color: p.bone,
		alpha: 0.72 * a * draw * flicker,
		cap: 'round',
	});
	g.moveTo(c0.x, c0.y);
	g.lineTo(c1.x, c1.y);
	g.stroke({
		width: Math.max(1.2, hh * 0.1),
		color: 0xffffff,
		alpha: 0.88 * a * draw * flicker,
		cap: 'round',
	});

	// ── 4. edge coupler plates (process nodes — rectangular steel, NOT flowers) ──
	const drawCoupler = (u: number, engage: number) => {
		const mid = at(u, 0);
		const pw = 13;
		const ph = hh + 8;
		const corners = [
			at(u - pw * 0.5, -ph * 0.5),
			at(u + pw * 0.5, -ph * 0.5),
			at(u + pw * 0.5, ph * 0.5),
			at(u - pw * 0.5, ph * 0.5),
		];
		g.poly([
			corners[0].x,
			corners[0].y,
			corners[1].x,
			corners[1].y,
			corners[2].x,
			corners[2].y,
			corners[3].x,
			corners[3].y,
		]);
		g.fill({ color: p.steel, alpha: 0.95 * a * engage });
		// plaque recess
		const inset = [
			at(u - pw * 0.28, -ph * 0.28),
			at(u + pw * 0.28, -ph * 0.28),
			at(u + pw * 0.28, ph * 0.28),
			at(u - pw * 0.28, ph * 0.28),
		];
		g.poly([
			inset[0].x,
			inset[0].y,
			inset[1].x,
			inset[1].y,
			inset[2].x,
			inset[2].y,
			inset[3].x,
			inset[3].y,
		]);
		g.fill({ color: 0x2a2826, alpha: 0.92 * a * engage });
		// blood intake fleck
		const fleck = at(u - 3, -ph * 0.32);
		g.rect(fleck.x - 3, fleck.y - 1, 7, 2.2);
		g.fill({ color: p.blood ?? 0x6b2a28, alpha: 0.7 * a * engage });
		// REC lock corner ticks (axis-aligned for horizontal conduits)
		const arm = 4.5;
		const ox = mid.x;
		const oy = mid.y;
		for (const [sx, sy] of [
			[-1, -1],
			[1, -1],
			[1, 1],
			[-1, 1],
		] as const) {
			const bx = ox + sx * (pw * 0.38);
			const by = oy + sy * (ph * 0.38);
			g.moveTo(bx, by + sy * arm);
			g.lineTo(bx, by);
			g.lineTo(bx + sx * arm, by);
			g.stroke({
				width: 1.6,
				color: p.bone,
				alpha: 0.85 * a * engage * flicker,
			});
		}
	};

	if (draw > 0.08) drawCoupler(0, Math.min(1, draw * 1.4));
	if (draw > 0.92) drawCoupler(visibleLen, Math.min(1, (draw - 0.85) / 0.15));

	// ── 5. restraint strap links + steel buckles (oval links, NOT dots) ──
	const buckleN = opts.buckleCount ?? Math.max(3, Math.floor(len / 36));
	for (let i = 0; i < buckleN; i++) {
		const u = ((i + 0.5) / buckleN) * visibleLen;
		if (u > visibleLen - 4 || u < 4) continue;
		const engage =
			draw >= (i + 0.5) / buckleN
				? 0.65 + 0.35 * Math.sin(t * 8 + i * 1.7 + seed)
				: 0;
		if (engage < 0.05) continue;
		const c = at(u, 0);
		// leather strap segment (charcoal oval)
		g.ellipse(c.x, c.y, 7.5, 3.2);
		g.fill({ color: p.charcoal, alpha: 0.78 * a * engage });
		g.ellipse(c.x, c.y, 7.5, 3.2);
		g.stroke({ width: 1.2, color: p.steel, alpha: 0.85 * a * engage });
		// steel buckle tongue (rectangle)
		const b0 = at(u - 3.2, -2.4);
		const b1 = at(u + 3.2, -2.4);
		const b2 = at(u + 3.2, 2.4);
		const b3 = at(u - 3.2, 2.4);
		g.poly([b0.x, b0.y, b1.x, b1.y, b2.x, b2.y, b3.x, b3.y]);
		g.fill({ color: p.steel, alpha: 0.9 * a * engage });
		const hole = at(u, 0);
		g.circle(hole.x, hole.y, 1.3);
		g.fill({ color: 0x1a1816, alpha: 0.9 * a * engage });
	}

	// ── 6. CCTV scan handshake packet (traveling CRT bar — not trailing dots) ──
	const scanSpeed = opts.scanSpeed ?? 0.72;
	if (draw > 0.35) {
		const travel = (t * scanSpeed + seed * 0.13) % 1;
		const su = travel * visibleLen;
		const packetW = Math.min(28, visibleLen * 0.18);
		const head = at(su, 0);
		const tail = at(Math.max(0, su - packetW), 0);
		// soft scan wash
		g.moveTo(tail.x + nx * hh * 0.35, tail.y + ny * hh * 0.35);
		g.lineTo(head.x + nx * hh * 0.35, head.y + ny * hh * 0.35);
		g.lineTo(head.x - nx * hh * 0.35, head.y - ny * hh * 0.35);
		g.lineTo(tail.x - nx * hh * 0.35, tail.y - ny * hh * 0.35);
		g.fill({ color: p.bone, alpha: 0.14 * a * flicker * draw });
		// hard CRT leading edge
		g.moveTo(head.x + nx * (hh * 0.5), head.y + ny * (hh * 0.5));
		g.lineTo(head.x - nx * (hh * 0.5), head.y - ny * (hh * 0.5));
		g.stroke({
			width: 2.2,
			color: 0xffffff,
			alpha: 0.85 * a * flicker * draw,
		});
		// secondary shear ghost (memory glitch)
		const ghost = at(Math.max(0, su - 8), 1.5);
		g.moveTo(ghost.x + nx * hh * 0.3, ghost.y + ny * hh * 0.3);
		g.lineTo(ghost.x - nx * hh * 0.3, ghost.y - ny * hh * 0.3);
		g.stroke({
			width: 1.2,
			color: p.silver,
			alpha: 0.35 * a * draw,
		});
	}

	// ── 7. mid-span intake stamp pulse (handshake lock) ──
	if (draw > 0.55) {
		const midU = visibleLen * 0.5;
		const pulse = 0.5 + 0.5 * Math.sin(t * 5.5 + seed);
		const slam = 0.7 + 0.3 * pulse;
		const stampA = a * draw * (0.35 + 0.45 * pulse) * flicker;
		const sw = 18 * slam;
		const sh = 9 * slam;
		const s0 = at(midU - sw * 0.5, -sh * 0.5);
		const s1 = at(midU + sw * 0.5, -sh * 0.5);
		const s2 = at(midU + sw * 0.5, sh * 0.5);
		const s3 = at(midU - sw * 0.5, sh * 0.5);
		g.poly([s0.x, s0.y, s1.x, s1.y, s2.x, s2.y, s3.x, s3.y]);
		g.fill({ color: p.bone, alpha: 0.75 * stampA });
		g.poly([s0.x, s0.y, s1.x, s1.y, s2.x, s2.y, s3.x, s3.y]);
		g.stroke({
			width: 1.8,
			color: p.blood ?? 0x6b2a28,
			alpha: 0.9 * stampA,
		});
		// INTAKE bar glyph
		const bar0 = at(midU - sw * 0.32, -1.2);
		const bar1 = at(midU + sw * 0.32, -1.2);
		g.moveTo(bar0.x, bar0.y);
		g.lineTo(bar1.x, bar1.y);
		g.stroke({
			width: 2.4,
			color: p.blood ?? 0x6b2a28,
			alpha: 0.85 * stampA,
		});
	}

	// ── 8. sparse ceramic dust along conduit ──
	for (let k = 0; k < 5; k++) {
		const life = (t * (0.35 + seeded(seed + k) * 0.5) + seeded(seed * 3 + k)) % 1;
		const u = seeded(seed + k * 11) * visibleLen;
		const lift = life * 10;
		const c = at(u, (seeded(k + 4) - 0.5) * hh + lift * (seeded(k) > 0.5 ? 1 : -1));
		g.circle(c.x, c.y, 1 + seeded(k * 2) * 1.6);
		g.fill({
			color: k % 2 === 0 ? p.bone : p.silver,
			alpha: 0.4 * a * draw * (1 - life),
		});
	}
};

/** @deprecated glass pane — do not use for White Room split FX */
export const drawObservationPane = (
	g: Graphics,
	size: number,
	opts: {
		alpha?: number;
		cracked?: boolean;
		crackProgress?: number;
		seed?: number;
		bezelWidth?: number;
		crackBranches?: number;
	} = {},
) => {
	// Redirect: intake stamp lock only (no frost glass web).
	drawIntakeStampLock(g, size, {
		alpha: opts.alpha,
		stampProgress: opts.crackProgress ?? (opts.cracked ? 1 : 0.85),
		seed: opts.seed,
	});
};

/** @deprecated knife/chip spit — redirects to intake projectiles */
export const drawCeramicSpit = (
	g: Graphics,
	opts: {
		x: number;
		y: number;
		rotation: number;
		size: number;
		color: number;
		alpha: number;
		kind: 'chip' | 'sliver' | 'buckle' | IntakeProjectileKind;
	},
) => {
	const kind: IntakeProjectileKind =
		opts.kind === 'buckle' ? 'buckle' : opts.kind === 'tube' || opts.kind === 'stamp' ? opts.kind : 'stamp';
	drawIntakeProjectile(g, {
		x: opts.x,
		y: opts.y,
		rotation: opts.rotation,
		size: opts.size,
		alpha: opts.alpha,
		kind,
	});
};

/** @deprecated glass/ceramic shards — redirects to padded foam debris */
export const drawCeramicBurstShard = (
	g: Graphics,
	opts: { size: number; color: number; alpha: number; seed: number },
) => {
	const kinds: PaddedDebrisKind[] = ['foam', 'strap', 'bucklePlate'];
	const kind = kinds[Math.floor(seeded(opts.seed) * kinds.length)] ?? 'foam';
	drawPaddedTearDebris(g, { ...opts, kind });
};
