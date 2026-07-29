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

type BookEventBonusLevel = {
	index: number;
	type: 'bonusLevel';
	level: 1 | 2 | 3;
	name: string;
	// legacy field kept optional for older generated books; unused now.
	startHaunted?: (Position & { apparitions: number })[];
};

// customised: Wild Reel — a special symbol in a bottom locked slot grows its
// middle reel (1/2/3) into a rising wild. The reel extends to baseRows + added
// rows; the risen cells are WILDs carrying a random multiplier (White Room).
type BookEventWildReel = {
	index: number;
	type: 'wildReel';
	label: string;
	reels: {
		reel: number;
		baseRows: number;
		added: number;
		cells: (Position & { multiplier: number })[];
		// what the whole column is worth on its own. Filling the reel to four
		// rows is already worth 4, so this never reads below 4.
		ways: number;
	}[];
	totalWays: number;
};

// customised: Unlocked Slots — bonus board expansion. During free spins the
// reserved locked slots open progressively by bonus level (L1 bottom, L2 +right,
// L3 +left) and fill with premiums/wilds. Filled RIGHT/LEFT columns become extra
// board reels (=> 6/7-of-a-kind), bottom premiums extend their middle reel.
// customised: Stretch — a STRETCH cell stretches its reel and gives the symbols on
// it extra x-ways. mode 'wild' = whole reel is wild (wild column + centred total);
// mode 'normal' = real symbols stretch in place, each showing its own x-ways.
type BookEventStretchReel = {
	index: number;
	type: 'stretchReel';
	label: string;
	reels: {
		reel: number;
		mode: 'wild' | 'normal';
		baseRows: number;
		reelWays: number;
		cells: { row: number; multiplier: number }[];
	}[];
	totalWays: number;
};

// customised: Clone — a CLONE cell turns every copy of one chosen symbol into a
// premium.
// the feature card lands in a special cell: a BOTTOM reel ({ reel }) or a SIDE
// column slot ({ side, slotRow }). 1 special symbol per cell.
type FeatureCardCell = { reel?: number; side?: 'left' | 'right'; slotRow?: number };

type BookEventCloneSymbol = {
	index: number;
	type: 'cloneSymbol';
	label: string;
	cell: FeatureCardCell;
	from: SymbolName;
	to: SymbolName;
	cells: Position[];
	totalWays: number;
};

// customised: Split — a SPLIT cell ADDS +1..+10 ways (`mult`) to each winning
// cell of one winning symbol type, and to every cell of any risen wild column.
// Always additive, never a multiplier.
type BookEventSplitSymbols = {
	index: number;
	type: 'splitSymbols';
	label: string;
	cell: FeatureCardCell;
	symbol: SymbolName;
	mult: number;
	// cells on a wild column are flagged `wild`: the wild-reel overlay owns their
	// Madam-Mirror pane tear (via wildReelWaysUpdate), not SplitPanes.
	cells: (Position & { multiplier: number; wild?: boolean })[];
	wildReels: { reel: number; ways: number }[];
	totalWays: number;
};

type SlotGroup = 'bottom' | 'right' | 'left';
type BookEventUnlockedSlots = {
	index: number;
	type: 'unlockedSlots';
	label: string;
	level: 1 | 2 | 3;
	unlocked: SlotGroup[];
	bottom: { reel: number; row: number; name: SymbolName }[];
	sides: {
		side: 'left' | 'right';
		reel: number;
		cells: { row: number; slotRow: number; name: SymbolName; multiplier?: number }[];
	}[];
	totalWays: number;
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
	| BookEventBonusLevel
	| BookEventWildReel
	| BookEventUnlockedSlots
	| BookEventStretchReel
	| BookEventCloneSymbol
	| BookEventSplitSymbols;

export type Bet = BetType<BookEvent>;
export type BookEventOfType<T> = Extract<BookEvent, { type: T }>;
export type BookEventContext = { bookEvents: BookEvent[] };
