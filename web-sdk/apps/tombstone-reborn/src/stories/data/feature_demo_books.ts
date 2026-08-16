// Hand-built Storybook books for the rewritten specials. Real library books
// come back after the next math rebuild; these let the new events play now.
import type { BookEvent } from '../../game/typesBookEvent';

type DemoBook = {
	label: string;
	mode: string;
	payoutX: number;
	events: BookEvent[];
};

const pad = [189, 91, 203, 176, 215, 189];
const anticipation = [0, 0, 0, 0, 0, 0];

const cell = (name: string, extra: Record<string, unknown> = {}) => ({ name, ...extra });

const reveal = (board: ReturnType<typeof cell>[][]): BookEvent =>
	({
		index: 0,
		type: 'reveal',
		board,
		paddingPositions: pad,
		gameType: 'basegame',
		anticipation,
	}) as BookEvent;

const settle = (index: number): BookEvent[] => [
	{ index, type: 'setTotalWin', amount: 0 },
	{ index: index + 1, type: 'finalWin', amount: 0 },
];

const baseBoard = (): ReturnType<typeof cell>[][] => [
	[cell('L4'), cell('H5'), cell('H3'), cell('L2'), cell('L5')],
	[cell('H4'), cell('L5'), cell('L1'), cell('H1'), cell('L1'), cell('L3')],
	[cell('L5'), cell('L4'), cell('H2'), cell('L3'), cell('L4'), cell('H3')],
	[cell('H5'), cell('H2'), cell('H3'), cell('L5')],
	[cell('L5'), cell('L3'), cell('H4'), cell('L5')],
	[cell('H3'), cell('L5'), cell('L2')],
];

export const FEATURE_DEMO_BOOKS: DemoBook[] = [
	{
		label: 'split',
		mode: 'bonus_small',
		payoutX: 12,
		events: [
			reveal((() => {
				const board = baseBoard();
				board[0][2] = cell('SP', { feature: true });
				return board;
			})()),
			{
				index: 1,
				type: 'boardSpecials',
				barMode: 'small',
				lastUnlocked: false,
				cells: [{ reel: 0, row: 2, kind: 'split' }],
			},
			{
				index: 2,
				type: 'split',
				factor: 2,
				symbols: ['L5'],
				cells: [
					{ reel: 1, row: 1, multiplier: 2 },
					{ reel: 1, row: 3, multiplier: 3 },
					{ reel: 2, row: 2, multiplier: 4 },
					{ reel: 4, row: 1, multiplier: 7 },
				],
				totalWays: 24,
			},
			{
				index: 3,
				type: 'specialsWild',
				cells: [{ reel: 0, row: 2 }],
			},
			...settle(4),
		],
	},
	{
		label: 'gunsmoke',
		mode: 'bonus_small',
		payoutX: 10,
		events: [
			reveal((() => {
				const board = baseBoard();
				board[2][2] = cell('GS', { feature: true });
				board[1][1] = cell('L5');
				board[1][3] = cell('L5');
				board[2][1] = cell('L5');
				board[4][1] = cell('L5');
				return board;
			})()),
			{
				index: 1,
				type: 'boardSpecials',
				barMode: 'small',
				lastUnlocked: false,
				cells: [{ reel: 2, row: 2, kind: 'gunsmoke' }],
			},
			{
				index: 2,
				type: 'gunsmoke',
				symbol: 'L5',
				cells: [
					{ reel: 1, row: 1 },
					{ reel: 1, row: 3 },
					{ reel: 2, row: 1 },
					{ reel: 4, row: 1 },
				],
				totalWays: 24,
			},
			{
				index: 3,
				type: 'specialsWild',
				cells: [{ reel: 2, row: 2 }],
			},
			...settle(4),
		],
	},
	{
		label: 'tombstone',
		mode: 'bonus_small',
		payoutX: 8,
		events: [
			reveal((() => {
				const board = baseBoard();
				board[1][2] = cell('SU', { scatter: true });
				board[5][1] = cell('H1');
				return board;
			})()),
			{
				index: 1,
				type: 'boardSpecials',
				barMode: 'small',
				lastUnlocked: true,
				cells: [],
			},
			{ index: 2, type: 'tombstone', reel: 5 },
			{
				index: 3,
				type: 'bounty',
				reel: 5,
				symbol: 'H1',
				winMult: 5,
				added: 5,
			},
			{ index: 4, type: 'winMult', added: 5, winMult: 5, source: 'bounty' },
			...settle(5),
		],
	},
	{
		label: 'nudge_ways',
		mode: 'bonus_small',
		payoutX: 24,
		events: [
			reveal((() => {
				const board = baseBoard();
				board[1][1] = cell('NW', { feature: true });
				return board;
			})()),
			{
				index: 1,
				type: 'boardSpecials',
				barMode: 'small',
				lastUnlocked: false,
				cells: [{ reel: 1, row: 1, kind: 'nudge' }],
			},
			{
				index: 2,
				type: 'nudgeWays',
				reel: 1,
				fullReel: false,
				startRow: 1,
				initialWays: 2,
				finalWays: 16,
				steps: [
					{ row: 2, ways: 4 },
					{ row: 3, ways: 8 },
					{ row: 4, ways: 16 },
				],
				cells: [
					{ reel: 1, row: 1, multiplier: 16 },
					{ reel: 1, row: 2, multiplier: 16 },
					{ reel: 1, row: 3, multiplier: 16 },
					{ reel: 1, row: 4, multiplier: 16 },
				],
				totalWays: 64,
			},
			...settle(3),
		],
	},
	{
		label: 'nudge_ways_full',
		mode: 'bonus_small',
		payoutX: 6,
		events: [
			reveal((() => {
				const board = baseBoard();
				board[2][1] = cell('NW', { feature: true });
				return board;
			})()),
			{
				index: 1,
				type: 'boardSpecials',
				barMode: 'small',
				lastUnlocked: false,
				cells: [{ reel: 2, row: 1, kind: 'nudge' }],
			},
			{
				index: 2,
				type: 'nudgeWays',
				reel: 2,
				fullReel: true,
				startRow: 1,
				initialWays: 3,
				finalWays: 3,
				steps: [],
				cells: [
					{ reel: 2, row: 1, multiplier: 3 },
					{ reel: 2, row: 2, multiplier: 3 },
					{ reel: 2, row: 3, multiplier: 3 },
					{ reel: 2, row: 4, multiplier: 3 },
				],
				totalWays: 12,
			},
			...settle(3),
		],
	},
	{
		label: 'nudge_ways_row3',
		mode: 'bonus_small',
		payoutX: 8,
		events: [
			reveal((() => {
				const board = baseBoard();
				board[1][3] = cell('NW', { feature: true });
				return board;
			})()),
			{
				index: 1,
				type: 'boardSpecials',
				barMode: 'small',
				lastUnlocked: false,
				cells: [{ reel: 1, row: 3, kind: 'nudge' }],
			},
			{
				index: 2,
				type: 'nudgeWays',
				reel: 1,
				fullReel: false,
				startRow: 3,
				initialWays: 2,
				finalWays: 4,
				steps: [{ row: 4, ways: 4 }],
				cells: [
					{ reel: 1, row: 3, multiplier: 4 },
					{ reel: 1, row: 4, multiplier: 4 },
				],
				totalWays: 16,
			},
			...settle(3),
		],
	},
];
