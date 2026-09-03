/**
 * Win-plate gunfire. Not a metronome: singles and 2–5 shot dumps
 * (GTA-style), seeded so the same win replays the same rhythm.
 */
import { fxRandom } from './featureVfx';

/** Tight dump between holes in a cluster. */
const BURST_MS = 42;
const BURST_SPAN = 38;
/** Breath after a lone shot. */
const SINGLE_REST_MS = 260;
const SINGLE_REST_SPAN = 320;
/** Breath after a 3–5 dump. */
const BURST_REST_MS = 420;
const BURST_REST_SPAN = 480;
/** First hole after the volley arms. */
const FIRST_MS = 70;
const FIRST_SPAN = 110;

export type CelebShotStep = { at: number; value: number };

const pickCluster = (left: number, seed: number, n: number) => {
	if (left <= 1) return 1;
	const roll = fxRandom(seed + n * 17);
	if (left >= 5 && roll < 0.14) return 5;
	if (left >= 4 && roll < 0.32) return 4;
	if (left >= 3 && roll < 0.58) return 3;
	if (left >= 2 && roll < 0.8) return 2;
	return 1;
};

const clusterSizes = (count: number, seed: number) => {
	const sizes: number[] = [];
	let left = count;
	let n = 0;
	while (left > 0) {
		const size = pickCluster(left, seed, n);
		sizes.push(size);
		left -= size;
		n += 1;
	}
	return sizes;
};

const shotValues = (from: number, to: number, count: number, seed: number) => {
	const span = Math.max(0, to - from);
	const n = Math.max(1, count);
	if (span <= 0) return [to];
	const weights = Array.from({ length: n }, (_, i) => 0.55 + fxRandom(seed + i * 13) * 0.55);
	const sum = weights.reduce((total, weight) => total + weight, 0);
	let acc = from;
	return weights.map((weight, i) => {
		acc = i === n - 1 ? to : acc + (span * weight) / sum;
		return acc;
	});
};

const restAfter = (clusterSize: number, seed: number, c: number) => {
	if (clusterSize >= 3) {
		return BURST_REST_MS + fxRandom(seed + 41 + c * 19) * BURST_REST_SPAN;
	}
	return SINGLE_REST_MS + fxRandom(seed + 41 + c * 19) * SINGLE_REST_SPAN;
};

const isBurstGap = (ms: number) => ms < 110;

/**
 * Timestamps for `count` holes. Burst gaps stay tight; only the rests
 * stretch or shrink to fit `remainMs`.
 */
export const planCelebGunfire = (
	from: number,
	to: number,
	count: number,
	remainMs: number,
	seed: number,
	now: number,
): CelebShotStep[] => {
	const n = Math.max(1, count);
	const values = shotValues(from, to, n, seed);
	const clusters = clusterSizes(n, seed);
	const gaps: number[] = [];

	for (let c = 0; c < clusters.length; c += 1) {
		const size = clusters[c] ?? 1;
		for (let k = 0; k < size; k += 1) {
			if (gaps.length === 0) {
				gaps.push(FIRST_MS + fxRandom(seed + 3) * FIRST_SPAN);
			} else if (k > 0) {
				gaps.push(BURST_MS + fxRandom(seed + 11 + gaps.length * 13) * BURST_SPAN);
			}
		}
		if (c < clusters.length - 1) {
			gaps.push(restAfter(size, seed, c));
		}
	}

	while (gaps.length < values.length) {
		gaps.push(SINGLE_REST_MS);
	}

	const burstTotal = gaps.reduce((sum, gap) => sum + (isBurstGap(gap) ? gap : 0), 0);
	const restTotal = gaps.reduce((sum, gap) => sum + (isBurstGap(gap) ? 0 : gap), 0);
	const raw = burstTotal + restTotal;
	const budget = Math.max(remainMs, burstTotal + n * 36);
	let restScale = 1;
	if (restTotal > 1) {
		if (raw > budget) {
			restScale = Math.max(0.45, (budget - burstTotal) / restTotal);
		} else if (raw < budget * 0.82) {
			restScale = (budget * 0.82 - burstTotal) / restTotal;
		}
	}

	let at = now;
	return values.map((value, i) => {
		const gap = gaps[i] ?? SINGLE_REST_MS;
		at += isBurstGap(gap) ? gap : gap * restScale;
		return { at, value };
	});
};

/** Same dumps as the win plate: 1–5 shot clusters, tight burst, then a breath. */
export const planCelebClusterGaps = (count: number, seed: number) => {
	const n = Math.max(0, count);
	if (n <= 0) return [];
	const clusters = clusterSizes(n, seed);
	const out: { beatMs: number; burst: boolean }[] = [];
	for (let c = 0; c < clusters.length; c += 1) {
		const size = clusters[c] ?? 1;
		for (let k = 0; k < size; k += 1) {
			const lastInCluster = k === size - 1;
			const lastOverall = lastInCluster && c === clusters.length - 1;
			if (lastOverall) {
				out.push({
					beatMs: 80 + fxRandom(seed + 3 + out.length) * 40,
					burst: false,
				});
				continue;
			}
			if (!lastInCluster) {
				out.push({
					beatMs: BURST_MS + fxRandom(seed + 11 + out.length * 13) * BURST_SPAN,
					burst: true,
				});
				continue;
			}
			out.push({
				beatMs: restAfter(size, seed, c),
				burst: false,
			});
		}
	}
	return out;
};
