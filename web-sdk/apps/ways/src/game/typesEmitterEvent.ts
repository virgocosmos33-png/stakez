import type { EmitterEventBoard } from '../components/Board.svelte';
import type { EmitterEventBoardFrame } from '../components/BoardFrame.svelte';
import type { EmitterEventFreeSpinIntro } from '../components/FreeSpinIntro.svelte';
import type { EmitterEventFreeSpinOutro } from '../components/FreeSpinOutro.svelte';
import type { EmitterEventWin } from '../components/Win.svelte';
import type { EmitterEventSound } from '../components/Sound.svelte';
import type { EmitterEventTransition } from '../components/Transition.svelte';
import type { EmitterEventApparition } from '../components/ApparitionOverlay.svelte';
import type { EmitterEventFrameMorphHud } from '../components/FrameMorphHud.svelte';
import type { EmitterEventBonusLevelBanner } from '../components/BonusLevelBanner.svelte';
import type { EmitterEventRetriggerBanner } from '../components/RetriggerBanner.svelte';
import type { EmitterEventMirrorShatter } from '../components/MirrorShatter.svelte';
import type { EmitterEventWinSweep } from '../components/WinSweep.svelte';
import type { EmitterEventWinDim } from '../components/WinDim.svelte';
import type { EmitterEventWinLightning } from '../components/WinLightning.svelte';

export type EmitterEventGame =
	| EmitterEventBoard
	| EmitterEventBoardFrame
	| EmitterEventWin
	| EmitterEventFreeSpinIntro
	| EmitterEventFreeSpinOutro
	| EmitterEventSound
	| EmitterEventTransition
	| EmitterEventApparition
	| EmitterEventFrameMorphHud
	| EmitterEventBonusLevelBanner
	| EmitterEventRetriggerBanner
	| EmitterEventMirrorShatter
	| EmitterEventWinSweep
	| EmitterEventWinDim
	| EmitterEventWinLightning;
