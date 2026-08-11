import type { Graphics } from 'pixi.js';

/**
 * Procedural chrome for the board frame and the cell-seal links, in the
 * Tombstone Reborn register: lantern light, rusted iron, grave chain, dust.
 *
 * This module replaces the old `clinicalFx` (WHITE_ROOM_PALETTE, fluorescent
 * tubes, restraint straps, CCTV scan bars, intake stamps). That art language
 * belonged to a different game and read as clinical white/steel over a
 * near-black graveyard board. Only the three helpers that were actually
 * imported survived the move; the rest was dead code.
 */

export type GraveyardPalette = {
	/** burnt wood / charred timber */
	charcoal: number;
	/** weathered iron — warm grey, never blue-steel */
	iron: number;
	/** grave dust catching lantern light */
	dust: number;
	/** sun-bleached bone; deliberately short of white */
	bone: number;
	/** oxidised iron, used sparingly as the accent */
	rust?: number;
};

export const GRAVEYARD_PALETTE: GraveyardPalette = {
	charcoal: 0x2e2620,
	iron: 0x7a6a58,
	dust: 0xb8a488,
	bone: 0xe0d2b4,
	rust: 0x7a3320,
};

const seeded = (k: number) => {
	const value = Math.sin(k * 12.9898 + 78.233) * 43758.5453;
	return value - Math.floor(value);
};

/**
 * Lantern-lit rectangle perimeter with a slow warm guttering flame.
 *
 * Must stay CONTINUOUS: segmented strokes read as a dashed "cut path" rim
 * around the board, which is the bug this frame was rebuilt to kill.
 */
export const drawLanternFrame = (
	g: Graphics,
	hw: number,
	hh: number,
	palette: GraveyardPalette,
	opts: {
		time: number;
		alpha: number;
		tubeWidth?: number;
		/** gutter rate, in Hz — a flame breathes, it does not strobe */
		flickerHz?: number;
		/** retained for fx config compat; ignored — segments looked like a cutline */
		segmentGap?: number;
		/** retained for fx config compat; a lantern does not blackout */
		blackoutChance?: number;
	},
) => {
	if (opts.alpha <= 0.01) return;
	const bandW = opts.tubeWidth ?? 6;
	const hz = Math.min(opts.flickerHz ?? 11, 4.5);

	// two detuned waves so the gutter never settles into an obvious pulse
	const gutter =
		0.82 +
		0.12 * Math.sin(opts.time * hz * Math.PI * 2) +
		0.06 * Math.sin(opts.time * hz * 1.7 + 1.3);

	const master = opts.alpha * gutter;
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
		const nx = dy / len;
		const ny = -dx / len;
		const local = 0.9 + 0.1 * Math.sin(opts.time * (hz + side * 0.4) * 0.7);
		const lit = master * local;

		// dusty halo, offset outward so the board art keeps its own edge
		g.moveTo(x0 + nx * 2, y0 + ny * 2);
		g.lineTo(x1 + nx * 2, y1 + ny * 2);
		g.stroke({ width: bandW * 2.8, color: palette.dust, alpha: 0.1 * lit });
		// warm body
		g.moveTo(x0, y0);
		g.lineTo(x1, y1);
		g.stroke({ width: bandW, color: palette.bone, alpha: 0.38 * lit });
		// soft core — never a hot white filament
		g.moveTo(x0, y0);
		g.lineTo(x1, y1);
		g.stroke({
			width: Math.max(1.0, bandW * 0.3),
			color: palette.dust,
			alpha: 0.32 * lit,
		});
	}
};

/**
 * Grave chain — the link drawn between two sealed reels.
 *
 * A charred rail carrying iron chain links, a lantern filament running its
 * length, brand plates at each end and a spark that travels the span. Every
 * value is warm: the old version ran a hard white CCTV scan bar down a steel
 * conduit, which read as a lab instrument bolted across the graveyard.
 */
export const drawGraveChainLink = (
	g: Graphics,
	opts: {
		x0: number;
		y0: number;
		x1: number;
		y1: number;
		time: number;
		/** 0..1 — the chain draws on as the seals expand */
		drawProgress: number;
		alpha?: number;
		seed?: number;
		housingHeight?: number;
		/** chain links across the span */
		buckleCount?: number;
		/** how fast the travelling spark runs the chain */
		scanSpeed?: number;
	},
) => {
	const a = opts.alpha ?? 1;
	const draw = Math.max(0, Math.min(1, opts.drawProgress));
	if (a <= 0.01 || draw <= 0.02) return;

	const p = GRAVEYARD_PALETTE;
	const seed = opts.seed ?? 7;
	const { x0, y0, x1, y1 } = opts;
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

	// lantern gutter — slow and warm, no strobe and no blackout
	const gutter = 0.84 + 0.16 * Math.sin(t * 3.1 + seed);

	const at = (u: number, offN = 0) => ({
		x: x0 + ux * u + nx * offN,
		y: y0 + uy * u + ny * offN,
	});

	// charred timber rail the chain is slung along
	const bodySteps = Math.max(8, Math.ceil(visibleLen / 10));
	for (let i = 0; i < bodySteps; i++) {
		const u0 = (i / bodySteps) * visibleLen;
		const u1 = ((i + 1) / bodySteps) * visibleLen;
		const c0 = at(u0, -hh * 0.55);
		const c1 = at(u1, -hh * 0.55);
		const c2 = at(u1, hh * 0.55);
		const c3 = at(u0, hh * 0.55);
		g.poly([c0.x, c0.y, c1.x, c1.y, c2.x, c2.y, c3.x, c3.y]);
		g.fill({ color: 0x15100c, alpha: 0.82 * a * draw });
	}

	// iron banding along both edges of the rail
	for (const side of [-1, 1] as const) {
		const r0 = at(0, side * hh * 0.42);
		const r1 = at(visibleLen, side * hh * 0.42);
		g.moveTo(r0.x, r0.y);
		g.lineTo(r1.x, r1.y);
		g.stroke({ width: 2.4, color: p.iron, alpha: 0.9 * a * draw, cap: 'butt' });
		g.moveTo(r0.x, r0.y);
		g.lineTo(r1.x, r1.y);
		g.stroke({ width: 1, color: p.dust, alpha: 0.4 * a * draw * gutter, cap: 'butt' });
	}

	// lantern filament running the span
	const f0 = at(2, 0);
	const f1 = at(Math.max(2, visibleLen - 2), 0);
	const filament: [number, number, number][] = [
		[hh * 0.55, 0.14, p.rust ?? 0x7a3320],
		[hh * 0.28, 0.6, 0xc07a2e],
		[Math.max(1.2, hh * 0.1), 0.85, p.bone],
	];
	for (const [width, alpha, color] of filament) {
		g.moveTo(f0.x, f0.y);
		g.lineTo(f1.x, f1.y);
		g.stroke({ width, color, alpha: alpha * a * draw * gutter, cap: 'round' });
	}

	// brand plates: an iron bracket hammered over each end of the rail
	const drawBrandPlate = (u: number, engage: number) => {
		const mid = at(u, 0);
		const pw = 13;
		const ph = hh + 8;
		const box = (insetX: number, insetY: number) => [
			at(u - insetX, -insetY),
			at(u + insetX, -insetY),
			at(u + insetX, insetY),
			at(u - insetX, insetY),
		];
		const outer = box(pw * 0.5, ph * 0.5);
		g.poly(outer.flatMap(({ x, y }) => [x, y]));
		g.fill({ color: p.iron, alpha: 0.95 * a * engage });
		const inner = box(pw * 0.28, ph * 0.28);
		g.poly(inner.flatMap(({ x, y }) => [x, y]));
		g.fill({ color: 0x241c16, alpha: 0.92 * a * engage });
		// rust weep off the top rivet
		const weep = at(u - 3, -ph * 0.32);
		g.rect(weep.x - 3, weep.y - 1, 7, 2.2);
		g.fill({ color: p.rust ?? 0x7a3320, alpha: 0.72 * a * engage });
		// corner nail heads
		const arm = 4.5;
		for (const [sx, sy] of [
			[-1, -1],
			[1, -1],
			[1, 1],
			[-1, 1],
		] as const) {
			const bx = mid.x + sx * (pw * 0.38);
			const by = mid.y + sy * (ph * 0.38);
			g.moveTo(bx, by + sy * arm);
			g.lineTo(bx, by);
			g.lineTo(bx + sx * arm, by);
			g.stroke({ width: 1.6, color: p.dust, alpha: 0.8 * a * engage * gutter });
		}
	};

	if (draw > 0.08) drawBrandPlate(0, Math.min(1, draw * 1.4));
	if (draw > 0.92) drawBrandPlate(visibleLen, Math.min(1, (draw - 0.85) / 0.15));

	// chain links slung between the plates
	const linkCount = opts.buckleCount ?? Math.max(3, Math.floor(len / 36));
	for (let i = 0; i < linkCount; i++) {
		const u = ((i + 0.5) / linkCount) * visibleLen;
		if (u > visibleLen - 4 || u < 4) continue;
		const engage =
			draw >= (i + 0.5) / linkCount ? 0.7 + 0.3 * Math.sin(t * 5 + i * 1.7 + seed) : 0;
		if (engage < 0.05) continue;
		const c = at(u, 0);
		g.ellipse(c.x, c.y, 7.5, 3.2);
		g.fill({ color: p.charcoal, alpha: 0.8 * a * engage });
		g.ellipse(c.x, c.y, 7.5, 3.2);
		g.stroke({ width: 1.2, color: p.iron, alpha: 0.85 * a * engage });
		// the pin through the link
		const pin = at(u, 0);
		g.circle(pin.x, pin.y, 1.4);
		g.fill({ color: 0x120e0a, alpha: 0.9 * a * engage });
	}

	// a spark running the chain, trailing ember rather than a hard scan edge
	const sparkSpeed = opts.scanSpeed ?? 0.72;
	if (draw > 0.35) {
		const travel = (t * sparkSpeed + seed * 0.13) % 1;
		const su = travel * visibleLen;
		const tailLen = Math.min(28, visibleLen * 0.18);
		const head = at(su, 0);
		const tail = at(Math.max(0, su - tailLen), 0);
		g.moveTo(tail.x + nx * hh * 0.35, tail.y + ny * hh * 0.35);
		g.lineTo(head.x + nx * hh * 0.35, head.y + ny * hh * 0.35);
		g.lineTo(head.x - nx * hh * 0.35, head.y - ny * hh * 0.35);
		g.lineTo(tail.x - nx * hh * 0.35, tail.y - ny * hh * 0.35);
		g.fill({ color: 0xc07a2e, alpha: 0.16 * a * gutter * draw });
		g.circle(head.x, head.y, 2.4);
		g.fill({ color: p.bone, alpha: 0.85 * a * gutter * draw });
		g.circle(head.x, head.y, 4.6);
		g.fill({ color: 0xc07a2e, alpha: 0.3 * a * gutter * draw });
	}

	// a branded marker seated mid-span once the chain is drawn
	if (draw > 0.55) {
		const midU = visibleLen * 0.5;
		const pulse = 0.5 + 0.5 * Math.sin(t * 4 + seed);
		const seat = 0.78 + 0.22 * pulse;
		const markA = a * draw * (0.4 + 0.4 * pulse) * gutter;
		const mw = 18 * seat;
		const mh = 9 * seat;
		const plate = [
			at(midU - mw * 0.5, -mh * 0.5),
			at(midU + mw * 0.5, -mh * 0.5),
			at(midU + mw * 0.5, mh * 0.5),
			at(midU - mw * 0.5, mh * 0.5),
		];
		g.poly(plate.flatMap(({ x, y }) => [x, y]));
		g.fill({ color: p.dust, alpha: 0.7 * markA });
		g.poly(plate.flatMap(({ x, y }) => [x, y]));
		g.stroke({ width: 1.8, color: p.rust ?? 0x7a3320, alpha: 0.9 * markA });
		const brand0 = at(midU - mw * 0.32, -1.2);
		const brand1 = at(midU + mw * 0.32, -1.2);
		g.moveTo(brand0.x, brand0.y);
		g.lineTo(brand1.x, brand1.y);
		g.stroke({ width: 2.4, color: p.rust ?? 0x7a3320, alpha: 0.85 * markA });
	}

	// grave dust drifting off the chain
	for (let k = 0; k < 5; k++) {
		const life = (t * (0.35 + seeded(seed + k) * 0.5) + seeded(seed * 3 + k)) % 1;
		const u = seeded(seed + k * 11) * visibleLen;
		const lift = life * 10;
		const mote = at(u, (seeded(k + 4) - 0.5) * hh + lift * (seeded(k) > 0.5 ? 1 : -1));
		g.circle(mote.x, mote.y, 1 + seeded(k * 2) * 1.6);
		g.fill({
			color: k % 2 === 0 ? p.dust : p.iron,
			alpha: 0.4 * a * draw * (1 - life),
		});
	}
};
