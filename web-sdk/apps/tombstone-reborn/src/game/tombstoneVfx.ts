/**
 * Tombstone Reborn western FX language for the SPLIT strike + target lock.
 * Atlas: tools/make_tombstone_split_vfx_atlas.py → asset key `tombstoneSplitVfx`.
 *
 * Hero plates (revolver muzzle flash, dust plume, gold starburst, sparkler)
 * come from the Scenario team library; the supporting sparks, scorch, dirt and
 * gunsmoke are Kenney particle-pack / smoke-particles (CC0), recoloured to the
 * dusty amber + powder-burn palette below.
 *
 * A split cell is N center-cropped panes (capped at 4) plus an Nx badge.
 * Thin iron seams sit between panes; the old powder-bar divider is gone.
 */

export const TOMBSTONE_SPLIT_VFX_ASSET = 'tombstoneSplitVfx';

/** Dusty western palette shared by TargetLock, SplitPanes and the wild columns. */
export const TOMBSTONE_FX = {
	brass: 0xc9a34a,
	spentBrass: 0xf0d78c,
	dust: 0x8a6e4a,
	gunsmoke: 0x6e6860,
	iron: 0x2a2420,
	ironEdge: 0x5a4e42,
	powder: 0x3a2418,
	bloodRust: 0xb54a2a,
	boneDust: 0xd4c4a8,
	dark: 0x0a0806,
} as const;

/**
 * Frame indices into the `tombstoneSplitVfx` spritesheet (row order).
 * Must stay in step with FRAMES in tools/make_tombstone_split_vfx_atlas.py.
 *
 * There is deliberately no ring/`scope` frame and no bright `flash` disc: those
 * were the yellow-circle reticle and the cream sticker that buried the symbols.
 */
export const VFX = {
	sparkA: 0,
	sparkB: 1,
	sparkC: 2,
	/** Scenario: wood-grip revolver blast, gun cut away */
	muzzleA: 3,
	/** Scenario: chrome revolver blast, gun cut away */
	muzzleB: 4,
	dirtA: 5,
	dirtB: 6,
	scorchA: 7,
	scorchB: 8,
	smokeA: 9,
	smokeB: 10,
	/** Scenario: tall sand plume kicked off the ground */
	dustPlume: 11,
	scratch: 12,
	slash: 13,
	puffA: 14,
	puffB: 15,
	/** Scenario: gold multi-point starburst — multiplier pop */
	starburst: 16,
	/** Scenario: gold sparkler streak with a flare head */
	sparkStreak: 17,
	/** Scenario: dark jagged impact silhouette */
	burstDark: 18,
} as const;

/**
 * CSS cell-card mark gold (`--c` / `--c2` on `.fx-corner`).
 * Same pair as the gold rim under paying cards and the split slash.
 * The ways skim wipe is the high-pay grunge plate through Febucci fire,
 * additive only. Not this flat gold.
 */
export const CELL_MARK = {
	gold: 0xffb628,
	goldDeep: 0x8a5300,
} as const;

/**
 * Accent per feature — dark iron only. No brass, no spentBrass, no dust: warm
 * accents still read as yellow on screen. `split` was blood rust, which is what
 * put red ticks on the corner brackets; the three features are separated by
 * iron value now, not by hue. Gunsmoke pre-hit uses CELL_MARK gold corners,
 * not this iron snap.
 */
export const TARGET_ACCENT: Record<'split' | 'clone' | 'stretch', number> = {
	split: TOMBSTONE_FX.ironEdge,
	clone: TOMBSTONE_FX.gunsmoke,
	stretch: TOMBSTONE_FX.iron,
};

// SplitPanes draws thin iron seams between its panes. StretchFx / WildReelSlide
// still part over a dark backing with no powder-bar divider.

const seeded = (n: number) => {
	const value = Math.sin(n * 12.9898 + 78.233) * 43758.5453;
	return value - Math.floor(value);
};

/**
 * Anticipation column: falling grit + faint gutter ticks.
 * Never paint a dark / powder / gunsmoke plate over the spinning cards — that
 * read as leftover White Room tube housing and buried the 3rd-scatter hang.
 */
export const drawDustAnticipation = (
	g: import('pixi.js').Graphics,
	colW: number,
	colH: number,
	timeValue: number,
	master: number,
) => {
	if (master <= 0.005) return;
	const halfW = colW / 2;
	const halfH = colH / 2;
	const wind = 0.72 + 0.28 * Math.sin(timeValue * 7.5);
	const a = master * wind;

	for (const side of [-1, 1] as const) {
		const pulse = 0.55 + 0.45 * Math.sin(timeValue * 9 + side);
		g.rect(side * halfW - 1.1, -halfH, 2.2, colH);
		g.fill({ color: TOMBSTONE_FX.ironEdge, alpha: 0.22 * a * pulse });
		g.rect(side * halfW - 0.45, -halfH, 0.9, colH);
		g.fill({ color: TOMBSTONE_FX.brass, alpha: 0.18 * a * pulse });
	}

	for (let i = 0; i < 14; i++) {
		const period = 1.4 + seeded(i * 7 + 1) * 1.2;
		const delay = seeded(i * 13 + 5) * 2.5;
		const lane = (seeded(i * 31 + 2) - 0.5) * colW * 0.7;
		const size = 2 + seeded(i * 23 + 3) * 5;
		const spin = (seeded(i * 29 + 11) - 0.5) * 8;
		const local = (timeValue + delay) / period;
		const cycle = local - Math.floor(local);
		const y = -halfH - 10 + cycle * (colH + 20);
		const x = lane + Math.sin(timeValue * 1.4 + i) * 6;
		const edge = Math.min(cycle / 0.12, (1 - cycle) / 0.15, 1);
		const ang = timeValue * spin + i;
		const c = Math.cos(ang);
		const s = Math.sin(ang);
		g.poly([
			x + c * size,
			y - s * size * 0.4,
			x - s * size * 0.5,
			y + c * size * 0.5,
			x - c * size * 0.7,
			y + s * size * 0.3,
		]);
		g.fill({
			color: i % 3 === 0 ? TOMBSTONE_FX.boneDust : TOMBSTONE_FX.dust,
			alpha: 0.48 * master * Math.max(edge, 0),
		});
	}
};

/** Full-canvas powder flash + dust streaks (replaces padded-cell fluorescent strobe). */
export const drawPowderStrobe = (
	g: import('pixi.js').Graphics,
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
		g.rect(0, 0, w, h);
		g.fill({ color: TOMBSTONE_FX.boneDust, alpha: 0.12 * opts.strobeAlpha });
		for (let i = 0; i < bands; i++) {
			const phase = (opts.time * 1.4 + i / bands) % 1;
			const y = phase * h;
			const bh = h * (0.04 + 0.03 * seeded(i + 2));
			g.rect(0, y - bh / 2, w, bh);
			g.fill({
				color: i % 2 === 0 ? TOMBSTONE_FX.spentBrass : TOMBSTONE_FX.gunsmoke,
				alpha: 0.2 * opts.strobeAlpha * (1 - Math.abs(phase - 0.5) * 1.2),
			});
		}
	}

	if (opts.glitchAlpha > 0.01) {
		for (let i = 0; i < scans; i++) {
			const y = seeded(i * 13 + Math.floor(opts.time * 30)) * h;
			const sh = 1 + seeded(i * 5) * 4;
			const shear = (seeded(i * 17 + Math.floor(opts.time * 40)) - 0.5) * w * 0.08;
			g.rect(shear, y, w, sh);
			g.fill({
				color: i % 4 === 0 ? TOMBSTONE_FX.dust : TOMBSTONE_FX.brass,
				alpha: 0.22 * opts.glitchAlpha,
			});
		}
		for (let i = 0; i < 3; i++) {
			const x = seeded(i * 29 + Math.floor(opts.time * 8)) * w;
			g.rect(x - 2, 0, 4 + seeded(i) * 10, h);
			g.fill({ color: TOMBSTONE_FX.powder, alpha: 0.1 * opts.glitchAlpha });
		}
	}
};

/** ParticleEmitter palette: falling brass / dust (replaces WHITE_ROOM_FALL). */
export const TOMBSTONE_COIN_FALL = {
	alpha: { start: 0.95, end: 0.15 },
	scale: { start: 0.22, end: 0.38, minimumScaleMultiplier: 0.7 },
	color: { start: '#c9a34a', end: '#5a4e42' },
	speed: { start: 180, end: 420, minimumSpeedMultiplier: 0.6 },
	acceleration: { x: 0, y: 980 },
	maxSpeed: 0,
	startRotation: { min: 70, max: 110 },
	noRotation: false,
	rotationSpeed: { min: -220, max: 220 },
	lifetime: { min: 2.2, max: 3.4 },
	blendMode: 'normal',
	frequency: 0.08,
	emitterLifetime: -1,
	maxParticles: 140,
	pos: { x: 0, y: 0 },
	addAtBack: false,
	spawnType: 'rect',
	spawnRect: { x: -280, y: -220, w: 560, h: 40 },
} as const;
