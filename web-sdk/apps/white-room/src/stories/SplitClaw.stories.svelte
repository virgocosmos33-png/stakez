<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'Showcase/Split Claw',
	});
</script>

<script lang="ts">
	/**
	 * SPLIT claw showcase.
	 *
	 * Every story here plays a REAL `splitSymbols` book event through
	 * `playBookEvent`, so what you see is the shipped sequence end to end —
	 * cell lightning, the target lock marking the chosen symbols, the multiplier
	 * stamped onto the board, then the claw atlas raking down through every
	 * scored card at once and the panes coming apart on the impact frame.
	 *
	 * Nothing is faked or hand-driven: change the handler and these move with it.
	 */
	import {
		StoryLocale,
		StoryGameTemplate,
		type TemplateArgs,
		templateArgs,
	} from 'components-storybook';

	import type { Position, RawSymbol, SymbolName } from '../game/types';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import { eventEmitter } from '../game/eventEmitter';
	import { playBookEvent } from '../game/utils';
	import { NUM_ROWS } from '../game/constants';

	setContext();

	const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

	/** filler that never collides with the symbol under test */
	const FILLER: SymbolName[] = ['L1', 'L2', 'L3', 'L4', 'L5'] as SymbolName[];

	type Placement = Position & { count: number };

	/**
	 * A padded board (rows + 1 above + 1 below, like the engine's strips) filled
	 * with lows, with `symbol` dropped onto every placement so the split has real
	 * cards to tear.
	 */
	const boardWith = (symbol: SymbolName, placements: Placement[]): RawSymbol[][] => {
		const board = NUM_ROWS.map((rows, reel) =>
			Array.from({ length: rows + 2 }, (_, row) => ({
				name: FILLER[(reel * 2 + row) % FILLER.length],
			})),
		);
		placements.forEach(({ reel, row }) => {
			if (board[reel]?.[row]) board[reel][row] = { name: symbol };
		});
		return board;
	};

	/** the shipped book-event shape for a split fired from one special cell */
	const splitEvent = (
		symbol: SymbolName,
		placements: Placement[],
		cell: { reel?: number; side?: 'left' | 'right'; slotRow?: number },
	) => ({
		index: 0,
		type: 'splitSymbols' as const,
		label: 'split',
		cell,
		symbol,
		mult: Math.max(...placements.map((p) => p.count)),
		cells: placements.map(({ reel, row, count }) => ({ reel, row, multiplier: count })),
		totalWays: placements.reduce((total, p) => total * p.count, 1),
	});

	/** settle the board, let it read, then run the real split */
	const showcase = async (
		symbol: SymbolName,
		placements: Placement[],
		cell: { reel?: number; side?: 'left' | 'right'; slotRow?: number } = { reel: 2 },
	) => {
		await wait(500);
		eventEmitter.broadcast({ type: 'boardSettle', board: boardWith(symbol, placements) });
		await wait(700);
		await playBookEvent(splitEvent(symbol, placements, cell) as any, { bookEvents: [] });
	};

	// Reels are a diamond (4/3/2/3/4 visible rows), so the row range differs per
	// column. Rows below are padded indices: visible row 1 is the top cell.

	// one symbol on every reel — the claw fades in on all five at once
	const acrossTheBoard: Placement[] = [
		{ reel: 0, row: 2, count: 3 },
		{ reel: 1, row: 1, count: 3 },
		{ reel: 2, row: 2, count: 3 },
		{ reel: 3, row: 3, count: 3 },
		{ reel: 4, row: 1, count: 3 },
	];

	// mixed counts, so the pane density difference is visible side by side
	const mixedCounts: Placement[] = [
		{ reel: 0, row: 1, count: 2 },
		{ reel: 1, row: 2, count: 3 },
		{ reel: 2, row: 1, count: 4 },
		{ reel: 3, row: 1, count: 5 },
		{ reel: 4, row: 4, count: 6 },
	];

	// a dense cluster: neighbouring cells tearing together
	const cluster: Placement[] = [
		{ reel: 1, row: 1, count: 4 },
		{ reel: 1, row: 2, count: 4 },
		{ reel: 1, row: 3, count: 4 },
		{ reel: 2, row: 1, count: 4 },
		{ reel: 2, row: 2, count: 4 },
		{ reel: 3, row: 1, count: 4 },
		{ reel: 3, row: 2, count: 4 },
		{ reel: 3, row: 3, count: 4 },
	];

	// every visible cell on the board
	const wholeBoard: Placement[] = NUM_ROWS.flatMap((rows, reel) =>
		Array.from({ length: rows }, (_, index) => ({ reel, row: index + 1, count: 3 })),
	);
</script>

{#snippet template(args: TemplateArgs<any>)}
	<StoryGameTemplate
		skipLoadingScreen={args.skipLoadingScreen}
		action={async () => {
			await args.action?.(args.data);
		}}
	>
		<StoryLocale lang="en">
			<Game />
		</StoryLocale>
	</StoryGameTemplate>
{/snippet}

<!-- ONE card, isolated: the frame-by-frame claw is easiest to judge here -->
<Story
	name="single"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => showcase('H1' as SymbolName, [{ reel: 2, row: 1, count: 3 }]),
	})}
	{template}
/>

<!-- the headline case: a claw on every reel at once, all striking together -->
<Story
	name="acrossTheBoard"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => showcase('H1' as SymbolName, acrossTheBoard),
	})}
	{template}
/>

<!-- 2x through 6x side by side: pane count rises left to right, and the 5x/6x
	cells cap their visual pane count and carry the exact "Nx" badge -->
<Story
	name="mixedCounts"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => showcase('H2' as SymbolName, mixedCounts),
	})}
	{template}
/>

<!-- adjacent cells tearing together — checks the claws do not read as one
	smeared mass when they overlap -->
<Story
	name="cluster"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => showcase('H3' as SymbolName, cluster, { side: 'right', slotRow: 1 }),
	})}
	{template}
/>

<!-- stress case: every visible cell splits at once -->
<Story
	name="wholeBoard"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => showcase('H1' as SymbolName, wholeBoard, { side: 'left', slotRow: 1 }),
	})}
	{template}
/>

<!-- three splits fired back to back from three different special cells, the way
	a bonus spin with several SPLIT cells actually plays out -->
<Story
	name="sequence"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await showcase('H1' as SymbolName, [
				{ reel: 0, row: 1, count: 2 },
				{ reel: 1, row: 1, count: 2 },
			]);
			await wait(400);
			await showcase(
				'H3' as SymbolName,
				[
					{ reel: 2, row: 1, count: 4 },
					{ reel: 2, row: 2, count: 4 },
				],
				{ side: 'right', slotRow: 1 },
			);
			await wait(400);
			await showcase(
				'H5' as SymbolName,
				[
					{ reel: 3, row: 2, count: 6 },
					{ reel: 4, row: 3, count: 6 },
				],
				{ side: 'left', slotRow: 1 },
			);
		},
	})}
	{template}
/>
