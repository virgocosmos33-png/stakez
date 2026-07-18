// Handcrafted single-spin demo: TWO different symbols each connect a winning
// way, so the end-of-spin glass-glint sweep can be seen tracing two separate
// ways (H1 across 3 reels, L1 across 4 reels).
//
// Board is 5 reels x 6 entries (row 0 and row 5 are top/bottom padding;
// visible rows are 1..4). Winning positions reference the padded rows.
//
//   reel:   0    1    2    3    4
//   row0    L3   L4   L1   L2   H2   <- padding
//   row1    H1   L2   H1   L5   L2
//   row2    L1   H1   L4   L1   L3
//   row3    L4   L1   L1   H3   L5
//   row4    L5   L3   L2   L4   H4
//   row5    L2   L5   L3   L1   L4   <- padding
//
//   H1 way (kind 3): (0,1) (1,2) (2,1)
//   L1 way (kind 4): (0,2) (1,3) (2,3) (3,2)

const twoWaysBook = {
	id: 9001,
	payoutMultiplier: 3,
	events: [
		{
			index: 0,
			type: 'reveal',
			board: [
				[
					{ name: 'L3' },
					{ name: 'H1' },
					{ name: 'L1' },
					{ name: 'L4' },
					{ name: 'L5' },
					{ name: 'L2' },
				],
				[
					{ name: 'L4' },
					{ name: 'L2' },
					{ name: 'H1' },
					{ name: 'L1' },
					{ name: 'L3' },
					{ name: 'L5' },
				],
				[
					{ name: 'L1' },
					{ name: 'H1' },
					{ name: 'L4' },
					{ name: 'L1' },
					{ name: 'L2' },
					{ name: 'L3' },
				],
				[
					{ name: 'L2' },
					{ name: 'L5' },
					{ name: 'L1' },
					{ name: 'H3' },
					{ name: 'L4' },
					{ name: 'L1' },
				],
				[
					{ name: 'H2' },
					{ name: 'L2' },
					{ name: 'L3' },
					{ name: 'L5' },
					{ name: 'H4' },
					{ name: 'L4' },
				],
			],
			paddingPositions: [10, 20, 30, 40, 50],
			gameType: 'basegame',
			anticipation: [0, 0, 0, 0, 0],
		},
		{
			index: 1,
			type: 'winInfo',
			totalWin: 300,
			wins: [
				{
					symbol: 'H1',
					kind: 3,
					win: 200,
					positions: [
						{ reel: 0, row: 1 },
						{ reel: 1, row: 2 },
						{ reel: 2, row: 1 },
					],
					meta: { ways: 1, globalMult: 1, winWithoutMult: 200, symbolMult: 0 },
				},
				{
					symbol: 'L1',
					kind: 4,
					win: 100,
					positions: [
						{ reel: 0, row: 2 },
						{ reel: 1, row: 3 },
						{ reel: 2, row: 3 },
						{ reel: 3, row: 2 },
					],
					meta: { ways: 1, globalMult: 1, winWithoutMult: 100, symbolMult: 0 },
				},
			],
		},
		{ index: 2, type: 'setWin', amount: 300, winLevel: 1 },
		{ index: 3, type: 'setTotalWin', amount: 300 },
		{ index: 4, type: 'finalWin', amount: 300 },
	],
	criteria: 'basegame',
	baseGameWins: 3.0,
	freeGameWins: 0.0,
};

export default twoWaysBook;
