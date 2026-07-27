import { type SpinningReelSymbolState } from 'utils-slots';
import type config from './config';

export type SymbolName = keyof typeof config.symbols;
export type RawSymbol = {
	name: SymbolName;
	// Wild Reel / bonus-slot wild multiplier, rides on the math engine's multiplier attribute
	multiplier?: number;
	scatter?: boolean;
	wild?: boolean;
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
