import { fxNum } from './fx.generated';
import { bookAmountToMultiplier } from './winCelebrationMap';

/** Mega-win threshold: lightning + prismatic glow (win ÷ bet). Panel-editable. */
export const MEGA_WIN_MULTIPLIER = fxNum('winLightning', 'megaWinMultiplier', 1000);

/**
 * Book win amounts are in hundredths of a bet multiple (a 90x win arrives as
 * 9000), the same unit setWin/getWinCelebration use — so the mega-win gate
 * converts with bookAmountToMultiplier instead of dividing by the bet cost
 * (which is in currency and made the gate fire at the wrong wins).
 */
export const isMegaWin = (bookWinAmount: number) => {
	if (bookWinAmount <= 0) return false;
	return bookAmountToMultiplier(bookWinAmount) >= MEGA_WIN_MULTIPLIER;
};
