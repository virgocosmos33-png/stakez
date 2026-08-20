import { type SpinningReelSymbolState } from 'utils-slots';
import type config from './config';

export type SymbolName = keyof typeof config.symbols;
export type RawSymbol = {
	name: SymbolName;
	// Wild Reel / bonus-slot wild multiplier, rides on the math engine's multiplier attribute
	multiplier?: number;
	scatter?: boolean;
	wild?: boolean;
	// A W that grows its whole reel instead of substituting in place. Same math
	// symbol, its own card (the arrow one) — set by LockedSlots for the bottom
	// cell that a Wild Reel rises out of.
	expanding?: boolean;
	// A W left in the nudge rider's wake (or riding as the nudge card itself).
	// Same math symbol, its own face (spur wheel + left arrows + NUDGE) — set
	// by the nudge book event handler for every cell the rider racks through.
	nudged?: boolean;
	// 1..5: which scatter this is, left to right across the board. Each position
	// has its own face (MEMORY / DOUBT / REGRET / REVELATION / OBLIVION), the
	// same 1..5 the scatter stop sounds already use.
	scatterIndex?: number;
	// Which per-level premium face (h#_small / h#_super) this symbol wears —
	// STAMPED at deal time by the reveal handler, never read live from the
	// room atmosphere. A symbol keeps the face it was born with, so a settled
	// board never face-swaps mid-presentation (scatter hit, bonus banner);
	// the new deck arrives with the next reveal's drop. Unset = base faces.
	level?: 'base' | 'small' | 'super';
};
export type BetMode = keyof typeof config.betModes;
export type GameType = keyof typeof config.paddingReels;

export const SYMBOL_STATES = [
	'static',
	'spin',
	'land',
	'win',
	// looping mesh-deform ripple of the card's own art; the winner keeps
	// undulating (haunted "living photo") while the board rests after a win
	'postWin',
	// deterministic crisp card frame (used by the apparition pane slicing)
	'postWinStatic',
	'explosion',
] as const;

export type SymbolState = SpinningReelSymbolState | (typeof SYMBOL_STATES)[number];

export type Position = {
	reel: number;
	row: number;
};
