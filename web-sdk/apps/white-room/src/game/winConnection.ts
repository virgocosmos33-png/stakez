import { fxNum } from './fx.generated';

/** Mega-win threshold: lightning + prismatic glow (win ÷ bet). Panel-editable. */
export const MEGA_WIN_MULTIPLIER = fxNum('winLightning', 'megaWinMultiplier', 2500);

export const isMegaWin = (winAmount: number, betCost: number) => {
	if (betCost <= 0 || winAmount <= 0) return false;
	return winAmount / betCost >= MEGA_WIN_MULTIPLIER;
};
