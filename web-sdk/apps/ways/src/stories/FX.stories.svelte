<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'FX',
	});
</script>

<script lang="ts">
	import {
		StoryLocale,
		StoryGameTemplate,
		type TemplateArgs,
		templateArgs,
	} from 'components-storybook';

	import type { Position, RawSymbol } from '../game/types';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import { eventEmitter } from '../game/eventEmitter';
	import { playBookEvent } from '../game/utils';
	import mirrorBooks from './data/mirror_books';

	setContext();

	// One story per fx config key (game-builder config → fx.*). The parametric
	// panel embeds these by story id to preview the REAL effect components.
	const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

	// realistic mirror/split data: the first recorded mirror book (id 5) —
	// its reveal board and the mirrorBurst event the game actually plays
	const mirrorBook = (mirrorBooks as any[])[0];
	const revealEvent = mirrorBook.events.find((event: any) => event.type === 'reveal');
	const burstEvent = mirrorBook.events.find((event: any) => event.type === 'mirrorBurst');

	// mirror cells + the neighbours they split (positions use padded rows, like all book events)
	const mirrorPositions: Position[] = burstEvent.mirrors.map((entry: any) => entry.mirror);
	const hauntedPositions: Position[] = burstEvent.mirrors.flatMap((entry: any) => entry.reflected);
	const telegraphPairs = burstEvent.mirrors.map(({ mirror, reflected }: any) => ({
		mirror,
		targets: reflected,
	}));

	// the reveal board with each mirror cell dressed behind glass — exactly what
	// the real reveal handler does when it sees a mirrorBurst coming up
	const glassBoard = (): RawSymbol[][] => {
		const board = revealEvent.board.map((reel: RawSymbol[]) =>
			reel.map((rawSymbol) => ({ ...rawSymbol })),
		);
		burstEvent.mirrors.forEach(({ mirror, mirrorBecomes }: any) => {
			board[mirror.reel][mirror.row] = { name: mirrorBecomes.name, glass: true };
		});
		return board;
	};

	// the post-burst board: mirrors resolved, reflected neighbours carrying
	// their apparition counts — what mirrorBurst settles before the split runs
	const splitBoard = (): RawSymbol[][] => {
		const board = revealEvent.board.map((reel: RawSymbol[]) =>
			reel.map((rawSymbol) => ({ ...rawSymbol })),
		);
		burstEvent.mirrors.forEach(({ mirror, reflected, mirrorBecomes }: any) => {
			board[mirror.reel][mirror.row] = { name: mirrorBecomes.name };
			reflected.forEach((cell: any) => {
				board[cell.reel][cell.row] = {
					...board[cell.reel][cell.row],
					multiplier: cell.apparitions,
					ttl: cell.ttl,
				};
			});
		});
		return board;
	};

	// a connected winning combination (adjacent cells merge into one contour)
	const linkedWinPositions: Position[] = [
		{ reel: 1, row: 1 },
		{ reel: 1, row: 2 },
		{ reel: 2, row: 2 },
		{ reel: 3, row: 2 },
		{ reel: 3, row: 3 },
	];

	// a 5-reel way so the left-to-right sweep stagger is visible end to end
	const fullSpanPositions: Position[] = [
		{ reel: 0, row: 2 },
		{ reel: 1, row: 2 },
		{ reel: 2, row: 2 },
		{ reel: 2, row: 3 },
		{ reel: 3, row: 2 },
		{ reel: 4, row: 2 },
	];

	// two winning ways (realistic winInfo shapes) for lightning / dim cycling
	const winGroups: Position[][] = [
		[
			{ reel: 0, row: 1 },
			{ reel: 1, row: 3 },
			{ reel: 2, row: 3 },
		],
		[
			{ reel: 0, row: 2 },
			{ reel: 0, row: 3 },
			{ reel: 1, row: 2 },
			{ reel: 1, row: 3 },
			{ reel: 2, row: 1 },
			{ reel: 2, row: 2 },
		],
	];
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

<!-- fx.winLightning → WinLightning.svelte (+ winConnection.ts megaWinMultiplier gate):
	thunder bolts over the winning ways + prismatic burst -->
<Story
	name="winLightning"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			await eventEmitter.broadcastAsync({
				type: 'winLightning',
				winGroups,
				winAmount: 250000,
			});
		},
	})}
	{template}
/>

<!-- fx.winSweep → WinSweep.svelte: plasma surge sweeping left-to-right across
	the connecting symbols (dim shown first, like the real winInfo flow) -->
<Story
	name="winSweep"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			eventEmitter.broadcast({ type: 'winDimShow', positions: fullSpanPositions });
			await eventEmitter.broadcastAsync({ type: 'winSweep', positions: fullSpanPositions });
		},
	})}
	{template}
/>

<!-- fx.winDim → WinDim.svelte: non-winning cells darken; the cycle then loops
	the glass-glint flash across each winning way (real setWin behaviour) -->
<Story
	name="winDim"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			eventEmitter.broadcast({ type: 'winDimShow', positions: winGroups.flat() });
			eventEmitter.broadcast({ type: 'winCycleSet', wins: winGroups });
			eventEmitter.broadcast({ type: 'winCycleStart' });
		},
	})}
	{template}
/>

<!-- fx.splitTelegraph → MirrorShatter.svelte: volley of tiny glass shards
	stabbing from the mirror into the cells it is about to split -->
<Story
	name="splitTelegraph"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			await eventEmitter.broadcastAsync({ type: 'mirrorTelegraph', pairs: telegraphPairs });
		},
	})}
	{template}
/>

<!-- fx.splitShatter → MirrorShatter.svelte: cracked pane pops in, holds, then
	bursts into flying glass shards (break + shatter, the real burst order) -->
<Story
	name="splitShatter"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			await eventEmitter.broadcastAsync({ type: 'mirrorBreak', positions: mirrorPositions });
			await eventEmitter.broadcastAsync({ type: 'mirrorShatter', positions: mirrorPositions });
		},
	})}
	{template}
/>

<!-- fx.mirrorBreak → MirrorShatter.svelte: cracked-glass pane pop-in + hold -->
<Story
	name="mirrorBreak"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			await eventEmitter.broadcastAsync({ type: 'mirrorBreak', positions: mirrorPositions });
		},
	})}
	{template}
/>

<!-- fx.apparition → ApparitionOverlay.svelte: haunted (split) cells on the
	board grow by winGrow while they are part of the winning combination -->
<Story
	name="apparition"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			eventEmitter.broadcast({ type: 'boardSettle', board: splitBoard() });
			eventEmitter.broadcast({ type: 'apparitionsRefresh' });
			await wait(900);
			eventEmitter.broadcast({ type: 'winDimShow', positions: hauntedPositions });
			eventEmitter.broadcast({ type: 'apparitionsWinGrow', positions: hauntedPositions });
			await wait(1600);
			eventEmitter.broadcast({ type: 'apparitionsWinRelease' });
		},
	})}
	{template}
/>

<!-- fx.splitAnimation → ApparitionOverlay.svelte runSplit/pulse: plays the REAL
	mirrorBurst book event (crack → shatter → telegraph → blade cut sweep,
	seam flare, detonation, panes snapping apart) on its recorded board -->
<Story
	name="splitAnimation"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			eventEmitter.broadcast({ type: 'boardSettle', board: glassBoard() });
			await wait(500);
			await playBookEvent(burstEvent, { bookEvents: [] });
		},
	})}
	{template}
/>

<!-- fx.plasmaLiner → PlasmaLiner.svelte: green plasma fire tracing the merged
	outer contour of the winning combination (burns until the win releases) -->
<Story
	name="plasmaLiner"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			eventEmitter.broadcast({ type: 'winDimShow', positions: linkedWinPositions });
			eventEmitter.broadcast({ type: 'apparitionsWinGrow', positions: linkedWinPositions });
		},
	})}
	{template}
/>

<!-- fx.framePlasma → BoardFramePlasma.svelte: purple flame ring licking off
	the board-frame perimeter (free-spins ambience, burns until hidden) -->
<Story
	name="framePlasma"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await wait(600);
			eventEmitter.broadcast({ type: 'boardFrameGlowShow' });
		},
	})}
	{template}
/>
