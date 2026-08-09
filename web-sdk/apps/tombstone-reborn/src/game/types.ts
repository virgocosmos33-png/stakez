import type config from './config';

export type SymbolName = keyof typeof config.symbols;
export type BetMode = keyof typeof config.betModes;
export type GameType = keyof typeof config.paddingReels;

export type RawSymbol = {
	name: SymbolName;
	wild?: boolean;
};

export const SYMBOL_STATES = [
	'static',
	'spin',
	'land',
	'win',
	'postWin',
	'postWinStatic',
	'explosion',
] as const;

export type SymbolState = (typeof SYMBOL_STATES)[number];

export type Position = {
	reel: number;
	row: number;
};
