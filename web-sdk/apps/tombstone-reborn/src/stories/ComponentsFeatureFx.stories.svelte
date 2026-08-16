<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	// COMPONENTS/FeatureFx exercises two feature presentations in isolation, driven
	// straight through the event emitter (no book, no spin) so the beat is reliable
	// to film and easy to eyeball:
	//   knife split — 2 / 3 / 4 panes after a horizontal knife slash; 6+ is one
	//                 symbol plus a corner count.
	//   shovel dig break — the digUp spade drives in and the cell cracks open in a
	//                       burst of dirt and smoke at the point of impact.
	const { Story } = defineMeta({
		title: 'COMPONENTS/FeatureFx',
	});
</script>

<script lang="ts">
	import {
		StoryGameTemplate,
		StoryLocale,
		type TemplateArgs,
		templateArgs,
	} from 'components-storybook';
	import { stateBet } from 'state-shared';

	import Game from '../components/Game.svelte';
	import { getContext, setContext } from '../game/context';

	setContext();
	const context = getContext();

	// storybook has no wallet: fund the demo so the board and bets are live
	stateBet.balanceAmount = 10_000;
	stateBet.betAmount = 1;

	/** Populate the resting board, then run one feature presentation on it. */
	const onBoard = (run: () => void) => async () => {
		await context.stateGameDerived.enhancedBoard.preSpin({});
		run();
	};

	// 2 / 3 / 4 panes, plus a 6+ cell (one symbol + corner count).
	const knifeSplit = onBoard(() =>
		context.eventEmitter.broadcast({
			type: 'splitPanesShow',
			cells: [
				{ reel: 1, row: 1, count: 2, name: 'L1' },
				{ reel: 2, row: 1, count: 3, name: 'H1' },
				{ reel: 3, row: 1, count: 4, name: 'H4' },
				{ reel: 4, row: 1, count: 7, name: 'L5' },
			],
		}),
	);

	const digBreak = onBoard(() =>
		context.eventEmitter.broadcast({
			type: 'featureBurstShow',
			kind: 'digUp',
			cells: [
				{ reel: 2, row: 1 },
				{ reel: 3, row: 2 },
				{ reel: 1, row: 2 },
			],
		}),
	);

	// Light linked-cell fire on the RESTING board (no preSpin — the board keeps
	// its symbols so the fire has cells to burn), let it fully catch, THEN raise
	// a bounty burst on a separate reel. LinkedCellFire's burstDim knocks the
	// fire back while any feature overlay is up, so the fire (reels 1-2) should
	// visibly recede once the burst fires — without the burst cells overlapping
	// it. Used by tools/qa_fire_dim.py, which grabs a frame before and after.
	const fireUnderBurst = async () => {
		context.eventEmitter.broadcast({
			type: 'cellFireShow',
			cells: [
				{ reel: 1, row: 1 },
				{ reel: 1, row: 2 },
				{ reel: 2, row: 1 },
			],
			level: 5,
		});
		setTimeout(() => {
			context.eventEmitter.broadcast({
				type: 'featureBurstShow',
				kind: 'bounty',
				cells: [{ reel: 4, row: 1 }],
			});
		}, 1100);
	};
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

<!-- knife slash, then 2 / 3 / 4 panes; 6+ is one symbol plus a corner count -->
<Story
	name="knife split (2 3 4 7)"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: knifeSplit })}
	{template}
/>

<!-- the digUp spade strikes: the cell cracks open in dirt and smoke on impact -->
<Story
	name="shovel dig break"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: digBreak })}
	{template}
/>

<!-- linked-cell fire recedes once a feature burst raises over the board -->
<Story
	name="fire dims under burst"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: fireUnderBurst })}
	{template}
/>
