import type { Graphics } from 'pixi.js';

// Shared FLAME border renderer for the win liner (green) and the free-spin
// board frame (violet). Fire is drawn as stacked RAGGED BANDS: a per-sample
// turbulent height field (three sine octaves crawling at different speeds)
// plus tall individual licks on their own grow/collapse cycles. The
// silhouette itself flickers and licks - no smooth constant-width strokes,
// no circle motes. Layers go soft body -> mid -> hot, rooted just under the
// edge, capped by a thin white-hot core line hugging the base.

export type FlameSample = { x: number; y: number; nx: number; ny: number };

export type FlamePalette = {
	body: number; // deep flame color, widest silhouette
	mid: number; // main visible flame
	hot: number; // inner tongues
	core: number; // white-hot base line
};

export type FlameBorderOptions = {
	seed: number;
	time: number;
	alpha: number; // master envelope, 0..1
	heightMin: number; // ragged band floor (px)
	heightMax: number; // ragged band ceiling before licks (px)
	lickEvery?: number; // one tall lick anchor per N samples (default 9)
	lickScale?: number; // lick peak vs heightMax (default 2.1)
	upBias?: number; // 0 = even all around, 1 = strongly top-weighted (default 0.6)
	inset?: number; // how deep the band roots under the edge (default 3)
	closed?: boolean; // samples form a closed loop (default true)
};

const seededRandom = (k: number) => {
	const value = Math.sin(k * 12.9898 + 78.233) * 43758.5453;
	return value - Math.floor(value);
};

// turbulent flame height per sample: layered sines (slow swell, sideways
// crawl, fast shimmer) shaped so lulls are common and spikes are sharp
const heightField = (samples: FlameSample[], options: FlameBorderOptions) => {
	const { seed, time } = options;
	const upBias = options.upBias ?? 0.6;
	const n = samples.length;
	const heights = new Array<number>(n);
	for (let i = 0; i < n; i++) {
		const up = Math.max(0, -samples[i].ny); // 1 where the edge faces up
		const bias = 1 - upBias + upBias * (0.35 + 0.65 * up);
		const a1 = Math.sin(i * 0.53 + time * 2.3 + seed);
		const a2 = Math.sin(i * 1.31 - time * 5.1 + seed * 2.7);
		const a3 = Math.sin(i * 2.97 + time * 9.6 + seed * 1.3);
		const noise = 0.5 + 0.5 * (a1 * 0.5 + a2 * 0.35 + a3 * 0.15);
		heights[i] =
			(options.heightMin + (options.heightMax - options.heightMin) * Math.pow(noise, 1.5)) * bias;
	}

	// tall licks: seeded anchors, each on its own life cycle; the gaussian
	// bump center drifts with time so the tongue tips lean and sway
	const lickCount = Math.max(3, Math.round(n / (options.lickEvery ?? 9)));
	const lickScale = options.lickScale ?? 2.1;
	for (let k = 0; k < lickCount; k++) {
		const anchor = Math.floor(seededRandom(seed * 3.1 + k * 17) * n);
		const period = 0.55 + seededRandom(seed + k * 29) * 0.75;
		const life = (time / period + seededRandom(seed * 1.7 + k * 43)) % 1;
		const envelope = Math.pow(Math.sin(Math.PI * life), 0.85);
		if (envelope < 0.05) continue;
		const up = Math.max(0, -samples[anchor].ny);
		const peak =
			options.heightMax *
			lickScale *
			envelope *
			(0.45 + 0.55 * up) *
			(0.6 + 0.8 * seededRandom(seed + k * 7));
		const width = 1.6 + seededRandom(seed * 2.3 + k * 11) * 2.6;
		const sway = Math.sin(time * 3.1 + k * 2.2 + seed) * 1.6 * life;
		const reach = Math.ceil(width * 3);
		for (let d = -reach; d <= reach; d++) {
			let index = anchor + d;
			if (options.closed === false) {
				if (index < 0 || index >= n) continue;
			} else {
				index = ((index % n) + n) % n;
			}
			heights[index] += peak * Math.exp(-Math.pow((d - sway) / width, 2));
		}
	}
	return heights;
};

export const drawFlameBorder = (
	graphics: Graphics,
	samples: FlameSample[],
	palette: FlamePalette,
	options: FlameBorderOptions,
) => {
	const n = samples.length;
	if (n < 3 || options.alpha <= 0.01) return;
	const { time, seed, alpha } = options;
	const closed = options.closed !== false;
	const inset = options.inset ?? 3;
	const heights = heightField(samples, options);
	const flicker = 0.86 + 0.14 * Math.sin(time * 19 + seed * 5.1);

	// each layer = a chain of quads (base -> ragged silhouette); quads tile
	// exactly so the band reads as one solid tongue-y sheet
	const band = (scale: number, color: number, layerAlpha: number) => {
		const last = closed ? n : n - 1;
		for (let i = 0; i < last; i++) {
			const j = (i + 1) % n;
			const a = samples[i];
			const b = samples[j];
			const heightA = heights[i] * scale;
			const heightB = heights[j] * scale;
			graphics.poly([
				a.x - a.nx * inset,
				a.y - a.ny * inset,
				a.x + a.nx * heightA,
				a.y + a.ny * heightA,
				b.x + b.nx * heightB,
				b.y + b.ny * heightB,
				b.x - b.nx * inset,
				b.y - b.ny * inset,
			]);
		}
		graphics.fill({ color, alpha: layerAlpha * flicker * alpha });
	};

	band(1.0, palette.body, 0.34);
	band(0.62, palette.mid, 0.5);
	band(0.32, palette.hot, 0.62);

	// white-hot base line: thin, wobbling with the field (never a clean tube)
	const core: number[] = [];
	for (let i = 0; i < n; i++) {
		const sample = samples[i];
		const lift = 0.5 + Math.min(heights[i] * 0.12, 2.5);
		core.push(sample.x + sample.nx * lift, sample.y + sample.ny * lift);
	}
	graphics.poly(core, closed);
	graphics.stroke({
		color: palette.core,
		width: 1.9,
		alpha: 0.85 * flicker * alpha,
	});
};
