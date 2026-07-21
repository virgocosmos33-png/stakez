/** Mega-win threshold: lightning + prismatic glow (win ÷ bet). */
export const MEGA_WIN_MULTIPLIER = 2500;

export const isMegaWin = (winAmount: number, betCost: number) => {
	if (betCost <= 0 || winAmount <= 0) return false;
	return winAmount / betCost >= MEGA_WIN_MULTIPLIER;
};
