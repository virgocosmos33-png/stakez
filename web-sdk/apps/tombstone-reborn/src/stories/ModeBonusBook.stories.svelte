<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'MODE_BONUS/book',
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
	import { setContext } from '../game/context';
	import { playBet } from '../game/utils';
	import { bookByLabel } from './data/tombstone_books';

	setContext();

	// storybook has no wallet: fund the demo so bets and buy-bonus are clickable
	stateBet.balanceAmount = 100000;
	stateBet.betAmount = 1;

	const play = (label: string) => async () => {
		const data = bookByLabel(label);
		console.log(`Running the "${label}" showcase book (${data.payoutMultiplier}x)`);
		await playBet({ ...data, state: data.events } as never);
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

<!-- SMALL BONUS (80x): the special bar is fully awake for one enhanced spin -->
<Story
	name="smallBonusWin"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('small_bonus_win') })}
	{template}
/>

<!-- SUPER BONUS (1000x): bar awake + last lane open -->
<Story
	name="superBonusWin"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('super_bonus_win') })}
	{template}
/>

<!-- BOUNTY: a premium drops into the open lane carrying a WIN multiplier -->
<Story
	name="bounty"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('bounty') })}
	{template}
/>

<!-- NUDGE: the bounty premium slides left, climbing its WIN multiplier -->
<Story
	name="nudge"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('nudge') })}
	{template}
/>

<!-- SUPERSPLIT: the lane turns WILD and every paying symbol splits at once -->
<Story
	name="superSplit"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('super_split') })}
	{template}
/>

<!-- MAX WIN: the 99,999x spin — the Gunslinger finally smiles -->
<Story
	name="maxWin"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('max_win') })}
	{template}
/>
