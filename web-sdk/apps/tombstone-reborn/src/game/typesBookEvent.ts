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

/** the card kinds planted on the board */
export type SpecialBarKind =
	| 'split'
	| 'gunsmoke'
	| 'tombstone'
	| 'nudge'
	| 'split_gang'
	| 'split_outlaws'
	| 'digup'
	| 'coffin';

/** Feature symbols that landed on the board this spin. */
type BookEventBoardSpecials = {
	index: number;
	type: 'boardSpecials';
	barMode: 'off' | 'base' | 'small' | 'super' | 'wake';
	lastUnlocked: boolean;
	cells: { reel: number; row: number; kind: SpecialBarKind }[];
};

/** The special bar resolves: one entry per NON-EMPTY bar cell. (legacy books) */
type BookEventSpecialBar = {
	index: number;
	type: 'specialBar';
	barMode: 'off' | 'base' | 'small' | 'super';
	cells: { reel: number; kind: SpecialBarKind }[];
};

/** TOMBSTONE unlocked the last-reel lane mid-spin. */
type BookEventTombstone = {
	index: number;
	type: 'tombstone';
	reel: number;
};

/** DIG UP — legacy name for tombstone. */
type BookEventDigUp = {
	index: number;
	type: 'digUp';
	reel: number;
};

/** TOMBSTONE OPEN — removed. Kept so older books still type-check. */
type BookEventCoffinOpen = {
	index: number;
	type: 'coffinOpen';
	reels: {
		reel: number;
		added: number;
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
	/** WIN multi gained this volley (1 per shot). */
	added?: number;
	/** stacked WIN multiplier AFTER this volley */
	winMult?: number;
};

/** SPLIT added ways to every copy of one chosen symbol type. */
type BookEventSplit = {
	index: number;
	type: 'split';
	factor: number;
	symbols: SymbolName[];
	cells: (Position & { multiplier: number })[];
	totalWays: number;
	added?: number;
	winMult?: number;
};

/** SPLIT-GANG — legacy. */
type BookEventSplitGang = {
	index: number;
	type: 'splitGang';
	factor: number;
	cells: (Position & { multiplier: number })[];
	totalWays: number;
};

/** SPLIT-OUTLAWS — legacy. */
type BookEventSplitOutlaws = {
	index: number;
	type: 'splitOutlaws';
	factor: number;
	cells: (Position & { multiplier: number })[];
	totalWays: number;
};

/** NUDGE WAYS: a ways-wild on reel 1 or 2, optionally nudging down. */
type BookEventNudgeWays = {
	index: number;
	type: 'nudgeWays';
	reel: number;
	fullReel: boolean;
	startRow: number;
	initialWays: number;
	finalWays: number;
	steps: { row: number; ways: number }[];
	cells: (Position & { multiplier: number })[];
	totalWays: number;
	added?: number;
	winMult?: number;
};

/** SUPERSPLIT: the last reel turned wild and EVERY symbol was split. */
type BookEventSuperSplit = {
	index: number;
	type: 'superSplit';
	factor: number;
	wildCells: Position[];
	cells: (Position & { multiplier: number })[];
	totalWays: number;
	added?: number;
	winMult?: number;
};

/** Last-reel premium landed with extra WAYS. Does not touch the WIN multi. */
type BookEventLanePremium = {
	index: number;
	type: 'lanePremium';
	reel: number;
	symbol: SymbolName;
	ways: number;
	cells: (Position & { multiplier: number })[];
	totalWays: number;
};

/** BOUNTY: a premium on the last reel stacked onto the WIN multiplier. */
type BookEventBounty = {
	index: number;
	type: 'bounty';
	reel: number;
	symbol: SymbolName;
	winMult: number;
	added?: number;
};

/** MARK: last-reel shooter fired at every premium, +1 WIN multi per trigger. */
type BookEventShooter = {
	index: number;
	type: 'shooter';
	reel: number;
	hits: Position[];
	added: number;
	winMult: number;
};

/** Feature symbols remaining on the board became the revolver WILD. */
type BookEventSpecialsWild = {
	index: number;
	type: 'specialsWild';
	cells: Position[];
};

/** HUD tick for the stacked WIN multiplier. */
type BookEventWinMult = {
	index: number;
	type: 'winMult';
	added: number;
	winMult: number;
	source: string;
};

/** NUDGE: legacy books only — the mechanic was removed. */
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

// ---------------------------------------------------------------------------
// BONUS ROUNDS (small bonus: bar awake / big bonus: grave lane open)
// ---------------------------------------------------------------------------

/** 3 scatters triggered the SMALL BONUS round, 4+ the BIG BONUS. */
type BookEventFreeSpinTrigger = {
	index: number;
	type: 'freeSpinTrigger';
	totalFs: number;
	/** where the scatters sit (padded rows); length is the trigger count */
	positions: Position[];
};

/** a new bonus-round spin is about to reveal: `amount` of `total` */
type BookEventUpdateFreeSpin = {
	index: number;
	type: 'updateFreeSpin';
	amount: number;
	total: number;
};

/** the round settled: `amount` is the round's total win */
type BookEventFreeSpinEnd = {
	index: number;
	type: 'freeSpinEnd';
	amount: number;
	winLevel: number;
};

/** the 1-in-100 UPGRADE: a 4th scatter dropped mid small-bonus round — the
 * grave lane is open from this spin on and the spin count is topped back up */
type BookEventBonusUpgrade = {
	index: number;
	type: 'bonusUpgrade';
	position: Position;
	spin: number;
	totalFs: number;
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
	| BookEventBoardSpecials
	| BookEventTombstone
	| BookEventDigUp
	| BookEventCoffinOpen
	| BookEventGunsmoke
	| BookEventSplit
	| BookEventSplitGang
	| BookEventSplitOutlaws
	| BookEventNudgeWays
	| BookEventSuperSplit
	| BookEventLanePremium
	| BookEventBounty
	| BookEventShooter
	| BookEventSpecialsWild
	| BookEventWinMult
	| BookEventNudge
	// bonus rounds
	| BookEventFreeSpinTrigger
	| BookEventUpdateFreeSpin
	| BookEventFreeSpinEnd
	| BookEventBonusUpgrade;

export type Bet = BetType<BookEvent>;
export type BookEventOfType<T> = Extract<BookEvent, { type: T }>;
export type BookEventContext = { bookEvents: BookEvent[] };
