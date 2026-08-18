/**
 * WAYS counts are combinatorial — a split-heavy board can pay tens of millions
 * of ways. The hanging WAYS box prints the bare count. On-board stamps and the
 * WIN multi use opposite faces so a glance tells them apart:
 *   win multiplier → "x4" / "x15"
 *   ways stamp     → "2x" / "15x"
 * ASCII "x" only — some bitmap faces drop U+00D7 × and leave a bare number.
 */

/** "192" | "10532" | "9000000" */
export const formatWays = (ways: number): string => {
	if (!Number.isFinite(ways) || ways <= 0) return '0';
	return String(Math.floor(ways));
};

/** HUD / cell WIN multiplier: "x4" | "x15" */
export const formatWinMult = (n: number): string => {
	if (!Number.isFinite(n) || n <= 0) return 'x1';
	return `x${Math.floor(n)}`;
};

/** On-board extra-ways stamp: "2x" | "15x" */
export const formatWaysMult = (n: number): string => `${formatWays(n)}x`;

/** "1 WAY" | "9000000 WAYS" — the caption used under a win amount. */
export const waysLabel = (ways: number): string =>
	ways === 1 ? '1 WAY' : `${formatWays(ways)} WAYS`;
