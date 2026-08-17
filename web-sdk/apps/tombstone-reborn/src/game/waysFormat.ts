/**
 * WAYS counts are combinatorial — a split-heavy board can pay tens of millions
 * of ways. Every surface (HUD plaque, win celebration) prints the full
 * calculated integer, no thousands separators and no K/M abbreviation.
 */

/** "192" | "10532" | "9000000" */
export const formatWays = (ways: number): string => {
	if (!Number.isFinite(ways) || ways <= 0) return '0';
	return String(Math.floor(ways));
};

/** "1 WAY" | "9000000 WAYS" — the caption used under a win amount. */
export const waysLabel = (ways: number): string =>
	ways === 1 ? '1 WAY' : `${formatWays(ways)} WAYS`;
