import * as PIXI from 'pixi.js';

// Vector control icons drawn to match the wood/steel/gold button kit.
// Every icon is drawn centred on the local origin (0,0) inside a box of `size`,
// so callers can drop them straight onto a medallion/panel with anchor 0.5.

export type UiIconName =
	| 'decrease'
	| 'increase'
	| 'menu'
	| 'turbo'
	| 'autoSpin'
	| 'payTable'
	| 'info'
	| 'settings'
	| 'soundOn'
	| 'soundOff'
	| 'menuExit'
	| 'spin'
	| 'stop'
	| 'star'
	| 'crown'
	| 'coins'
	| 'play'
	| 'chevron';

export type IconStyle = {
	/** bounding size the icon is drawn to fit within */
	size: number;
	/** primary fill / stroke colour */
	color: number;
	/** optional secondary colour (waves, gear centre, bolt) */
	accent?: number;
};

const STROKE = { cap: 'round', join: 'round' } as const;

const star = (g: PIXI.Graphics, s: number, color: number) => {
	const outer = s * 0.4;
	const inner = s * 0.17;
	const pts: number[] = [];
	for (let i = 0; i < 10; i++) {
		const r = i % 2 === 0 ? outer : inner;
		const a = -Math.PI / 2 + (i * Math.PI) / 5;
		pts.push(Math.cos(a) * r, Math.sin(a) * r);
	}
	g.poly(pts);
	g.fill({ color });
};

const refresh = (g: PIXI.Graphics, s: number, color: number) => {
	const r = s * 0.3;
	const lw = Math.max(3, s * 0.13);
	const a0 = -Math.PI * 0.4;
	const a1 = Math.PI * 1.05;
	g.arc(0, 0, r, a0, a1);
	g.stroke({ color, width: lw, ...STROKE });
	// arrowhead at the open tip (a1), pointing along the tangent
	const ex = Math.cos(a1) * r;
	const ey = Math.sin(a1) * r;
	const nx = Math.cos(a1);
	const ny = Math.sin(a1);
	const tx = -Math.sin(a1); // clockwise tangent
	const ty = Math.cos(a1);
	const ah = s * 0.17;
	g.poly([
		ex + tx * ah,
		ey + ty * ah,
		ex + nx * ah * 0.85,
		ey + ny * ah * 0.85,
		ex - nx * ah * 0.85,
		ey - ny * ah * 0.85,
	]);
	g.fill({ color });
};

const speaker = (g: PIXI.Graphics, s: number, color: number) => {
	g.poly([
		-s * 0.36,
		-s * 0.12,
		-s * 0.14,
		-s * 0.12,
		s * 0.02,
		-s * 0.28,
		s * 0.02,
		s * 0.28,
		-s * 0.14,
		s * 0.12,
		-s * 0.36,
		s * 0.12,
	]);
	g.fill({ color });
};

export const drawIcon = (g: PIXI.Graphics, name: UiIconName, style: IconStyle) => {
	const s = style.size;
	const color = style.color;
	const accent = style.accent ?? color;
	const lw = Math.max(2.5, s * 0.12);

	switch (name) {
		case 'menu': {
			const bw = s * 0.62;
			const bh = Math.max(3, s * 0.13);
			const gap = s * 0.2;
			for (const dy of [-gap, 0, gap]) g.roundRect(-bw / 2, dy - bh / 2, bw, bh, bh / 2);
			g.fill({ color });
			break;
		}
		case 'soundOn': {
			speaker(g, s, color);
			for (const k of [1, 2]) {
				const x = s * 0.1 + k * s * 0.11;
				g.moveTo(x, -s * 0.13);
				g.lineTo(x + s * 0.06, 0);
				g.lineTo(x, s * 0.13);
				g.stroke({ color: accent, width: lw * 0.8, ...STROKE });
			}
			break;
		}
		case 'soundOff': {
			speaker(g, s, color);
			g.moveTo(s * 0.14, -s * 0.14);
			g.lineTo(s * 0.36, s * 0.14);
			g.moveTo(s * 0.36, -s * 0.14);
			g.lineTo(s * 0.14, s * 0.14);
			g.stroke({ color: accent, width: lw * 0.8, ...STROKE });
			break;
		}
		case 'turbo': {
			g.poly([
				s * 0.08,
				-s * 0.4,
				-s * 0.26,
				s * 0.06,
				-s * 0.02,
				s * 0.06,
				-s * 0.12,
				s * 0.4,
				s * 0.28,
				-s * 0.1,
				s * 0.02,
				-s * 0.1,
			]);
			g.fill({ color: accent });
			break;
		}
		case 'autoSpin':
		case 'spin': {
			refresh(g, name === 'spin' ? s * 1.05 : s, color);
			break;
		}
		case 'stop': {
			const r = s * 0.24;
			g.roundRect(-r, -r, r * 2, r * 2, s * 0.08);
			g.fill({ color });
			break;
		}
		case 'payTable': {
			const w = s * 0.6;
			const rh = Math.max(2, s * 0.1);
			const gap = s * 0.19;
			for (const dy of [-gap, 0, gap]) {
				g.circle(-w / 2 + rh * 0.7, dy, rh * 0.7);
				g.fill({ color });
				g.roundRect(-w / 2 + rh * 2.2, dy - rh / 2, w - rh * 2.6, rh, rh / 2);
				g.fill({ color });
			}
			break;
		}
		case 'info': {
			g.circle(0, -s * 0.24, lw * 0.62);
			g.fill({ color });
			g.roundRect(-lw * 0.5, -s * 0.05, lw, s * 0.34, lw * 0.5);
			g.fill({ color });
			break;
		}
		case 'settings': {
			const ro = s * 0.24;
			const tl = s * 0.11;
			const tw = s * 0.14;
			for (let i = 0; i < 8; i++) {
				const a = (i / 8) * Math.PI * 2;
				const rr = ro + tl * 0.35;
				const cx = Math.cos(a) * rr;
				const cy = Math.sin(a) * rr;
				const ux = Math.cos(a);
				const uy = Math.sin(a);
				const vx = -Math.sin(a);
				const vy = Math.cos(a);
				g.poly([
					cx + ux * (tl / 2) + vx * (tw / 2),
					cy + uy * (tl / 2) + vy * (tw / 2),
					cx + ux * (tl / 2) - vx * (tw / 2),
					cy + uy * (tl / 2) - vy * (tw / 2),
					cx - ux * (tl / 2) - vx * (tw / 2),
					cy - uy * (tl / 2) - vy * (tw / 2),
					cx - ux * (tl / 2) + vx * (tw / 2),
					cy - uy * (tl / 2) + vy * (tw / 2),
				]);
			}
			g.fill({ color });
			g.circle(0, 0, ro);
			g.stroke({ color, width: s * 0.13 });
			g.circle(0, 0, s * 0.06);
			g.fill({ color: accent });
			break;
		}
		case 'menuExit': {
			const d = s * 0.24;
			g.moveTo(-d, -d);
			g.lineTo(d, d);
			g.moveTo(d, -d);
			g.lineTo(-d, d);
			g.stroke({ color, width: lw, ...STROKE });
			break;
		}
		case 'chevron': {
			g.moveTo(-s * 0.2, -s * 0.08);
			g.lineTo(0, s * 0.12);
			g.lineTo(s * 0.2, -s * 0.08);
			g.stroke({ color, width: lw, ...STROKE });
			break;
		}
		case 'increase':
		case 'decrease': {
			const len = s * 0.44;
			const th = Math.max(4, s * 0.14);
			g.roundRect(-len / 2, -th / 2, len, th, th / 2);
			if (name === 'increase') g.roundRect(-th / 2, -len / 2, th, len, th / 2);
			g.fill({ color });
			break;
		}
		case 'star': {
			star(g, s, color);
			break;
		}
		case 'crown': {
			g.poly([
				-s * 0.42,
				s * 0.2,
				-s * 0.42,
				-s * 0.12,
				-s * 0.21,
				s * 0.04,
				0,
				-s * 0.3,
				s * 0.21,
				s * 0.04,
				s * 0.42,
				-s * 0.12,
				s * 0.42,
				s * 0.2,
			]);
			g.fill({ color });
			g.roundRect(-s * 0.42, s * 0.12, s * 0.84, s * 0.14, s * 0.04);
			g.fill({ color });
			for (const [px, py] of [
				[-s * 0.42, -s * 0.12],
				[0, -s * 0.3],
				[s * 0.42, -s * 0.12],
			]) {
				g.circle(px, py, s * 0.05);
				g.fill({ color });
			}
			break;
		}
		case 'coins': {
			const rx = s * 0.3;
			const ry = s * 0.12;
			for (const cy of [s * 0.17, -s * 0.02, -s * 0.21]) {
				g.ellipse(0, cy, rx, ry);
				g.fill({ color });
				g.ellipse(0, cy, rx, ry);
				g.stroke({ color: 0x000000, width: 2, alpha: 0.4 });
			}
			break;
		}
		case 'play': {
			g.poly([-s * 0.2, -s * 0.28, s * 0.28, 0, -s * 0.2, s * 0.28]);
			g.fill({ color });
			break;
		}
	}
};
