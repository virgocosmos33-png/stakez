import { type SpinningReelSymbolState } from 'utils-slots';
import type config from './config';

export type SymbolName = keyof typeof config.symbols;
export type RawSymbol = {
	name: SymbolName;
	// apparition count of a haunted cell (2-4), rides on the math engine's multiplier attribute
	multiplier?: number;
	scatter?: boolean;
	wild?: boolean;
	mirror?: boolean;
	// haunted mirror: the symbol is trapped behind a glass overlay until the burst shatters it
	glass?: boolean;
};
export type BetMode = keyof typeof config.betModes;
export type GameType = keyof typeof config.paddingReels;

export const SYMBOL_STATES = [
	'static',
	'spin',
	'land',
	'win',
	'postWinStatic',
	'explosion',
] as const;

export type SymbolState = SpinningReelSymbolState | (typeof SYMBOL_STATES)[number];

export type Position = {
	reel: number;
	row: number;
};
