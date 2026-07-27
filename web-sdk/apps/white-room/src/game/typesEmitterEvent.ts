import type { EmitterEventBoard } from '../components/Board.svelte';
import type { EmitterEventBoardFrame } from '../components/BoardFrame.svelte';
import type { EmitterEventFreeSpinIntro } from '../components/FreeSpinIntro.svelte';
import type { EmitterEventFreeSpinOutro } from '../components/FreeSpinOutro.svelte';
import type { EmitterEventWin } from '../components/Win.svelte';
import type { EmitterEventSound } from '../components/Sound.svelte';
import type { EmitterEventTransition } from '../components/Transition.svelte';
import type { EmitterEventFrameMorphHud } from '../components/FrameMorphHud.svelte';
import type { EmitterEventBonusLevelBanner } from '../components/BonusLevelBanner.svelte';
import type { EmitterEventRetriggerBanner } from '../components/RetriggerBanner.svelte';
import type { EmitterEventWinSweep } from '../components/WinSweep.svelte';
import type { EmitterEventWinDim } from '../components/WinDim.svelte';
import type { EmitterEventWinLightning } from '../components/WinLightning.svelte';
import type { EmitterEventCellSeal } from '../components/CellSealOverlay.svelte';
import type { EmitterEventWildReel } from '../components/WildReelSlide.svelte';
import type { EmitterEventPlasmaLiner } from '../components/PlasmaLiner.svelte';
import type { EmitterEventSplitPanes } from '../components/SplitPanes.svelte';
import type { EmitterEventCloneMorph } from '../components/CloneMorph.svelte';
import type { EmitterEventStretchFx } from '../components/StretchFx.svelte';
import type { EmitterEventStretchWays } from '../components/StretchWays.svelte';
import type { EmitterEventCellLightning } from '../components/CellLightning.svelte';

export type EmitterEventGame =
	| EmitterEventBoard
	| EmitterEventBoardFrame
	| EmitterEventWin
	| EmitterEventFreeSpinIntro
	| EmitterEventFreeSpinOutro
	| EmitterEventSound
	| EmitterEventTransition
	| EmitterEventFrameMorphHud
	| EmitterEventBonusLevelBanner
	| EmitterEventRetriggerBanner
	| EmitterEventWinSweep
	| EmitterEventWinDim
	| EmitterEventWinLightning
	| EmitterEventCellSeal
	| EmitterEventWildReel
	| EmitterEventPlasmaLiner
	| EmitterEventSplitPanes
	| EmitterEventCloneMorph
	| EmitterEventStretchFx
	| EmitterEventStretchWays
	| EmitterEventCellLightning;
