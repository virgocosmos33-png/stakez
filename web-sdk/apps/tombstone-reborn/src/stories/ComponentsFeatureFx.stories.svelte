<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	// COMPONENTS/FeatureFx exercises feature presentations in isolation, driven
	// straight through the event emitter (no book, no spin) so the beat is reliable
	// to film and easy to eyeball:
	//   knife split — fast stab to ~90°, 0.5s hold, cut-drag (wound opens).
	//                 2 panes = 1 cut, 3 panes = 2 cuts. 6+ is one symbol plus a count.
	//   shovel dig break — the digUp spade drives in and the cell cracks open in a
	//                       burst of dirt and smoke at the point of impact.
	//   gunsmoke wounds — bullet + smoke + glass dent + hole; same GTA dumps
	//                     as win-plate gunfire (clusters + breath); specials
	//                     stain the iron cell frame, and the stain stays.
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
	import { fxWait } from '../game/fxTiming';
	import { planWoundRhythm, volleySeed } from '../game/gunsmokeSpin';
	import { forceStorySpeed } from './playStory';

	setContext();
	const context = getContext();

	// storybook has no wallet: fund the demo so the board and bets are live
	stateBet.balanceAmount = 10_000;
	stateBet.betAmount = 1;
	forceStorySpeed(false);

	/** Populate the resting board, then run one feature presentation on it. */
	const onBoard = (run: () => void) => async () => {
		forceStorySpeed(false);
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
	const gunsmokeWounds = async () => {
		await context.stateGameDerived.enhancedBoard.preSpin({});
		const hits = [
			{ reel: 1, row: 1, blood: true, name: 'H1' as const },
			{ reel: 1, row: 2, blood: false, name: 'L5' as const },
			{ reel: 3, row: 1, blood: true, name: 'H3' as const },
			{ reel: 4, row: 1, blood: false, name: 'L2' as const },
		];
		const rhythm = planWoundRhythm(hits.length, volleySeed(hits));
		for (let i = 0; i < hits.length; i += 1) {
			const hit = hits[i];
			if (!hit) continue;
			const shot = rhythm[i];
			const fire = context.eventEmitter.broadcastAsync({
				type: 'gunsmokeWound',
				reel: hit.reel,
				row: hit.row,
				blood: hit.blood,
				name: hit.name,
				beatMs: 0,
				flightScale: shot?.flightScale,
				side: shot?.side,
			});
			if (shot?.burst) {
				void fire;
				if ((shot.beatMs ?? 0) > 0) await fxWait(shot.beatMs);
				continue;
			}
			await fire;
			if ((shot?.beatMs ?? 0) > 0) await fxWait(shot.beatMs);
		}
	};

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

<!-- 3D stab+slice: 2 panes = 1 blood, 3 = 2 bloods; 6+ is one symbol plus a count -->
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

<!-- GUNSMOKE: holes on every hit; specials stain the iron cell-frame mask -->
<Story
	name="gunsmoke wounds"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: gunsmokeWounds })}
	{template}
/>

<!-- linked-cell fire recedes once a feature burst raises over the board -->
<Story
	name="fire dims under burst"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: fireUnderBurst })}
	{template}
/>
