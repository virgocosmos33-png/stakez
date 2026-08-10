import type { BetToResume } from './stateBet.svelte';

// Bet replay (`?replay=true`) runs the stored round on demand instead of on
// mount: the panel shows what the round played for and what it returned, then
// the player starts it. `round` is kept so "replay again" can re-seed the actor.
export type ReplayPhase = 'idle' | 'playing' | 'ended';

export const stateReplay = $state({
	phase: 'idle' as ReplayPhase,
	round: null as BetToResume,
});
