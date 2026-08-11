/**
 * WAYS counts are combinatorial, so a split-heavy 6-of-a-kind board can pay
 * tens of millions of ways (the math engine really does emit 268,489,320 for a
 * capped split board). Printed raw that is an unreadable digit wall in the HUD
 * rail and under the celebration amount, so anything past five figures is
 * abbreviated and everything below it gets thousands separators.
 */

const COMPACT_FROM = 100_000;
const UNITS: readonly [number, string][] = [
	[1e12, 'T'],
	[1e9, 'B'],
	[1e6, 'M'],
	[1e3, 'K'],
];

/** "192" | "14,490" | "268M" | "67.1M" */
export const formatWays = (ways: number): string => {
	if (!Number.isFinite(ways) || ways <= 0) return '0';
	const value = Math.floor(ways);
	if (value < COMPACT_FROM) return value.toLocaleString('en-US');

	for (const [base, suffix] of UNITS) {
		if (value < base) continue;
		const scaled = value / base;
		// keep it to three significant-ish characters so the plaque never grows
		return `${scaled >= 100 ? Math.round(scaled) : scaled.toFixed(1)}${suffix}`;
	}
	return value.toLocaleString('en-US');
};

/** "1 WAY" | "268M WAYS" — the caption used under a win amount. */
export const waysLabel = (ways: number): string =>
	ways === 1 ? '1 WAY' : `${formatWays(ways)} WAYS`;
