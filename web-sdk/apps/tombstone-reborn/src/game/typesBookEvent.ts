import type { BetType } from 'rgs-requests';

import type { SymbolName, RawSymbol, GameType, Position } from './types';

// book events shared with the other engine games
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

type BookEventSetWin = {
	index: number;
	type: 'setWin';
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

// the spin hit the 99,999x cap
type BookEventWincap = {
	index: number;
	type: 'wincap';
	amount: number;
};

// customised
type BookEventCreateBonusSnapshot = {
	index: number;
	type: 'createBonusSnapshot';
	bookEvents: BookEvent[];
};

// ---------------------------------------------------------------------------
// TOMBSTONE REBORN custom events
// ---------------------------------------------------------------------------

/** the card kinds the top special bar can reveal */
export type SpecialBarKind = 'split_gang' | 'split_outlaws' | 'gunsmoke' | 'digup' | 'coffin';

/** The special bar resolves: one entry per NON-EMPTY bar cell. */
type BookEventSpecialBar = {
	index: number;
	type: 'specialBar';
	barMode: 'off' | 'base' | 'small' | 'super';
	cells: { reel: number; kind: SpecialBarKind }[];
};

/** DIG UP unlocked the last-reel lane mid-spin. */
type BookEventDigUp = {
	index: number;
	type: 'digUp';
	reel: number;
};

/** TOMBSTONE OPEN grew short reels taller, revealing extra symbols. */
type BookEventCoffinOpen = {
	index: number;
	type: 'coffinOpen';
	reels: {
		reel: number;
		added: number;
		/** freshly revealed symbols, PADDED row indices, bottom-most last */
		newCells: { row: number; name: SymbolName }[];
	}[];
	totalWays: number;
};

/** GUNSMOKE turned one whole symbol type into WILDs. */
type BookEventGunsmoke = {
	index: number;
	type: 'gunsmoke';
	symbol: SymbolName;
	cells: Position[];
	totalWays: number;
};

/** SPLIT-GANG added ways to every premium on the board. */
type BookEventSplitGang = {
	index: number;
	type: 'splitGang';
	factor: number;
	cells: (Position & { multiplier: number })[];
	totalWays: number;
};

/** SPLIT-OUTLAWS added ways to every low on the board. */
type BookEventSplitOutlaws = {
	index: number;
	type: 'splitOutlaws';
	factor: number;
	cells: (Position & { multiplier: number })[];
	totalWays: number;
};

/** SUPERSPLIT: the last reel turned wild and EVERY paying symbol was split. */
type BookEventSuperSplit = {
	index: number;
	type: 'superSplit';
	factor: number;
	wildCells: Position[];
	cells: (Position & { multiplier: number })[];
	totalWays: number;
};

/** BOUNTY: a random premium landed on the last reel carrying a WIN multiplier. */
type BookEventBounty = {
	index: number;
	type: 'bounty';
	reel: number;
	symbol: SymbolName;
	winMult: number;
};

/** NUDGE: the nudge wild racked LEFT from the lane one notch per reel,
 * stepping onto exactly one cell per column and leaving it WILD, climbing its
 * WIN multiplier for every premium it crushed. */
type BookEventNudge = {
	index: number;
	type: 'nudge';
	symbol: SymbolName;
	baseMult: number;
	passed: number;
	winMult: number;
	/** the full walk, right-to-left (reel last-1..0, ending on the first
	 * reel's middle cell); `name` is the symbol that WAS there, `premium`
	 * whether crushing it bumped the multiplier */
	steps?: (Position & { name?: SymbolName; premium?: boolean })[];
	/** legacy books: the premium steps only */
	hits?: (Position & { name?: SymbolName })[];
};

export type BookEvent =
	| BookEventReveal
	| BookEventWinInfo
	| BookEventSetTotalWin
	| BookEventCreateBonusSnapshot
	| BookEventFinalWin
	| BookEventSetWin
	| BookEventWincap
	// customised
	| BookEventSpecialBar
	| BookEventDigUp
	| BookEventCoffinOpen
	| BookEventGunsmoke
	| BookEventSplitGang
	| BookEventSplitOutlaws
	| BookEventSuperSplit
	| BookEventBounty
	| BookEventNudge;

export type Bet = BetType<BookEvent>;
export type BookEventOfType<T> = Extract<BookEvent, { type: T }>;
export type BookEventContext = { bookEvents: BookEvent[] };
