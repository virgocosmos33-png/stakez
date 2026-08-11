import type { EmitterEventBoard } from '../components/Board.svelte';
import type { EmitterEventBoardFrame } from '../components/BoardFrame.svelte';
import type { EmitterEventWin } from '../components/Win.svelte';
import type { EmitterEventSound } from '../components/Sound.svelte';
import type { EmitterEventTransition } from '../components/Transition.svelte';
import type { EmitterEventFrameMorphHud } from '../components/FrameMorphHud.svelte';
import type { EmitterEventWinSweep } from '../components/WinSweep.svelte';
import type { EmitterEventWinDim } from '../components/WinDim.svelte';
import type { EmitterEventWinLightning } from '../components/WinLightning.svelte';
import type { EmitterEventCellSeal } from '../components/CellSealOverlay.svelte';
import type { EmitterEventWildReel } from '../components/WildReelSlide.svelte';
import type { EmitterEventSplitPanes } from '../components/SplitPanes.svelte';
import type { EmitterEventCloneMorph } from '../components/CloneMorph.svelte';
import type { EmitterEventStretchFx } from '../components/StretchFx.svelte';
import type { EmitterEventStretchWays } from '../components/StretchWays.svelte';
import type { EmitterEventCellLightning } from '../components/CellLightning.svelte';
import type { EmitterEventCellFire } from '../components/LinkedCellFire.svelte';
import type { EmitterEventTargetLock } from '../components/TargetLock.svelte';
import type { EmitterEventNudgeSlide } from '../components/NudgeSlide.svelte';
import type { EmitterEventFeatureBurst } from '../components/FeatureBurst.svelte';
import type { EmitterEventBonusEntry } from '../components/BonusEntry.svelte';
import type { EmitterEventLaneCard } from '../components/LaneGoldCard.svelte';

/** No free-spin / bonus-level events exist on this bus by design. Tombstone
 * Reborn's bonuses are SINGLE enhanced spins (math game_config.py declares no
 * freespin triggers, and gameInfo.ts states it to the player), so there is no
 * spin counter to award, no level to announce and no level to upgrade. The
 * FreeSpinIntro / FreeSpinOutro / FreeSpinCounter / BonusLevelBanner /
 * BonusUpgradeBanner overlays that used to declare `freeSpinIntroShow`,
 * `freeSpinOutro*`, `bonusLevelShow` and `levelUpBannerShow` were Madam Mirror
 * leftovers ("THE INTAKE" / "HER SIDE" / "WHITEOUT" over White Room art); they
 * were never mounted and nothing ever broadcast them. Deleted — do not re-add
 * without a math feature to drive them.
 *
 * What DOES exist is `bonusEntryShow` / `bonusEntryHandoff`
 * (EmitterEventBonusEntry): two tiers, one per real buy mode, each announcing a
 * single enhanced spin. Broadcast from game/bonusEntry.ts at round start. */

/** Every feature overlay rides the reels off the board on the next spin. Shared
 * rather than owned by one component, because they all have to leave together
 * — see game/featureFallOut.svelte.ts. */
export type EmitterEventFeatureFx = { type: 'featureFxFallOut' };

export type EmitterEventGame =
	| EmitterEventFeatureFx
	| EmitterEventBoard
	| EmitterEventBoardFrame
	| EmitterEventWin
	| EmitterEventSound
	| EmitterEventTransition
	| EmitterEventFrameMorphHud
	| EmitterEventWinSweep
	| EmitterEventWinDim
	| EmitterEventWinLightning
	| EmitterEventCellSeal
	| EmitterEventWildReel
	| EmitterEventSplitPanes
	| EmitterEventCloneMorph
	| EmitterEventStretchFx
	| EmitterEventStretchWays
	| EmitterEventCellLightning
	| EmitterEventCellFire
	| EmitterEventTargetLock
	| EmitterEventNudgeSlide
	| EmitterEventFeatureBurst
	| EmitterEventBonusEntry
	| EmitterEventLaneCard;
