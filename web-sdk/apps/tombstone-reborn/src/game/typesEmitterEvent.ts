import type { EmitterEventBoard } from '../components/Board.svelte';
import type { EmitterEventBoardFrame } from '../components/BoardFrame.svelte';
import type { EmitterEventFreeSpinIntro } from '../components/FreeSpinIntro.svelte';
import type { EmitterEventFreeSpinOutro } from '../components/FreeSpinOutro.svelte';
import type { EmitterEventWin } from '../components/Win.svelte';
import type { EmitterEventSound } from '../components/Sound.svelte';
import type { EmitterEventTransition } from '../components/Transition.svelte';
import type { EmitterEventFrameMorphHud } from '../components/FrameMorphHud.svelte';
import type { EmitterEventBonusLevelBanner } from '../components/BonusLevelBanner.svelte';
import type { EmitterEventBonusUpgradeBanner } from '../components/BonusUpgradeBanner.svelte';
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
import type { EmitterEventTargetLock } from '../components/TargetLock.svelte';
import type { EmitterEventNudgeSlide } from '../components/NudgeSlide.svelte';

/** Every feature overlay rides the reels off the board on the next spin. Shared
 * rather than owned by one component, because they all have to leave together
 * — see game/featureFallOut.svelte.ts. */
export type EmitterEventFeatureFx = { type: 'featureFxFallOut' };

export type EmitterEventGame =
	| EmitterEventFeatureFx
	| EmitterEventBoard
	| EmitterEventBoardFrame
	| EmitterEventWin
	| EmitterEventFreeSpinIntro
	| EmitterEventFreeSpinOutro
	| EmitterEventSound
	| EmitterEventTransition
	| EmitterEventFrameMorphHud
	| EmitterEventBonusLevelBanner
	| EmitterEventBonusUpgradeBanner
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
	| EmitterEventTargetLock
	| EmitterEventNudgeSlide;
