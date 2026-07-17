import type { EmitterEventBoard } from '../components/Board.svelte';
import type { EmitterEventBoardFrame } from '../components/BoardFrame.svelte';
import type { EmitterEventFreeSpinIntro } from '../components/FreeSpinIntro.svelte';
import type { EmitterEventFreeSpinCounter } from '../components/FreeSpinCounter.svelte';
import type { EmitterEventFreeSpinOutro } from '../components/FreeSpinOutro.svelte';
import type { EmitterEventWin } from '../components/Win.svelte';
import type { EmitterEventSound } from '../components/Sound.svelte';
import type { EmitterEventTransition } from '../components/Transition.svelte';
import type { EmitterEventApparition } from '../components/ApparitionOverlay.svelte';
import type { EmitterEventWaysCounter } from '../components/WaysCounter.svelte';
import type { EmitterEventBonusLevelBanner } from '../components/BonusLevelBanner.svelte';
import type { EmitterEventMirrorShatter } from '../components/MirrorShatter.svelte';
import type { EmitterEventWinSweep } from '../components/WinSweep.svelte';
import type { EmitterEventWinDim } from '../components/WinDim.svelte';

export type EmitterEventGame =
	| EmitterEventBoard
	| EmitterEventBoardFrame
	| EmitterEventWin
	| EmitterEventFreeSpinIntro
	| EmitterEventFreeSpinCounter
	| EmitterEventFreeSpinOutro
	| EmitterEventSound
	| EmitterEventTransition
	| EmitterEventApparition
	| EmitterEventWaysCounter
	| EmitterEventBonusLevelBanner
	| EmitterEventMirrorShatter
	| EmitterEventWinSweep
	| EmitterEventWinDim;
