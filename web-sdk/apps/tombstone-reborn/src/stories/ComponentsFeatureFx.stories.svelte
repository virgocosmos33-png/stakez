<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	// COMPONENTS/FeatureFx exercises two feature presentations in isolation, driven
	// straight through the event emitter (no book, no spin) so the beat is reliable
	// to film and easy to eyeball:
	//   bullet explosion — a split cell whose multiplier cleared EXPLOSION_MIN_MULT
	//                       DETONATES (SplitExplosion flipbook + boom), on top of
	//                       the usual bullet holes + Nx badge.
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

	// A big-multiplier split: reel 2 / row 1 carries a 15x cell (detonates) and
	// reel 1 / row 1 a 3x cell (holes only), so the story shows the >10x threshold.
	const detonate = onBoard(() =>
		context.eventEmitter.broadcast({
			type: 'splitPanesShow',
			cells: [
				{ reel: 2, row: 1, count: 15, name: 'H1' },
				{ reel: 1, row: 1, count: 3, name: 'L1' },
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

<!-- a split cell over 10x DETONATES: gunpowder blast + boom over the bullet holes -->
<Story
	name="bullet explosion (15x)"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: detonate })}
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
