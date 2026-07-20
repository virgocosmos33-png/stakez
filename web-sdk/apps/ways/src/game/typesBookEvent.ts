import type { BetType } from 'rgs-requests';

import type { SymbolName, RawSymbol, GameType, Position } from './types';

// book events shared with scatter game
type BookEventReveal = {
	index: number;
	type: 'reveal';
	board: RawSymbol[][];
	paddingPositions: number[];
	anticipation: number[];
	gameType: GameType;
};

type BookEventSetTotalWin = {
	index: number;
	type: 'setTotalWin';
	amount: number;
};

type BookEventFinalWin = {
	index: number;
	type: 'finalWin';
	amount: number;
};

type BookEventFreeSpinTrigger = {
	index: number;
	type: 'freeSpinTrigger';
	totalFs: number;
	positions: Position[];
};

type BookEventUpdateFreeSpin = {
	index: number;
	type: 'updateFreeSpin';
	amount: number;
	total: number;
};

type BookEventFreeSpinRetrigger = {
	index: number;
	type: 'freeSpinRetrigger';
	totalFs: number;
	positions: Position[];
};

type BookEventSetWin = {
	index: number;
	type: 'setWin';
	amount: number;
	winLevel: number;
};

type BookEventFreeSpinEnd = {
	index: number;
	type: 'freeSpinEnd';
	amount: number;
	winLevel: number;
};

type BookEventWinInfo = {
	index: number;
	type: 'winInfo';
	totalWin: number;
	wins: {
		symbol: SymbolName;
		kind: number;
		win: number;
		positions: Position[];
		meta: {
			ways: number;
			globalMult: number;
			winWithoutMult: number;
			symbolMult: number;
		};
	}[];
};

// customised
type BookEventCreateBonusSnapshot = {
	index: number;
	type: 'createBonusSnapshot';
	bookEvents: BookEvent[];
};

// customised: xMirror feature (Madam Mirror)
type BookEventMirrorBurst = {
	index: number;
	type: 'mirrorBurst';
	mirrors: {
		mirror: Position;
		// ttl (free spins only): reveals the split cell survives
		// (1 = this spin only, 2+ = carries over, -1 = sticky all bonus)
		reflected: (Position & { apparitions: number; ttl?: number })[];
		mirrorBecomes: { name: SymbolName };
	}[];
	totalWays: number;
};

// customised: the Madam's Eye - every split symbol turns wild for the spin
type BookEventMadamsEye = {
	index: number;
	type: 'madamsEye';
	eye: Position;
	converted: (Position & { apparitions: number })[];
};

type BookEventHauntDeepen = {
	index: number;
	type: 'hauntDeepen';
	cells: (Position & { apparitions: number })[];
};

type BookEventBonusLevel = {
	index: number;
	type: 'bonusLevel';
	level: 1 | 2 | 3;
	name: string;
	startHaunted: (Position & { apparitions: number })[];
};

export type BookEvent =
	| BookEventReveal
	| BookEventWinInfo
	| BookEventSetTotalWin
	| BookEventFreeSpinTrigger
	| BookEventUpdateFreeSpin
	| BookEventFreeSpinRetrigger
	| BookEventCreateBonusSnapshot
	| BookEventFinalWin
	| BookEventSetWin
	| BookEventFreeSpinEnd
	// customised
	| BookEventMirrorBurst
	| BookEventMadamsEye
	| BookEventHauntDeepen
	| BookEventBonusLevel;

export type Bet = BetType<BookEvent>;
export type BookEventOfType<T> = Extract<BookEvent, { type: T }>;
export type BookEventContext = { bookEvents: BookEvent[] };
