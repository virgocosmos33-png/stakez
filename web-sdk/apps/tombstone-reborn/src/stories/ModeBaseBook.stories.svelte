<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'MODE_BASE/book',
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
	stateBet.balanceAmount = 10000;
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

<!-- a 92%-of-the-time spin: the board lands, nothing connects, the grave stays shut -->
<Story
	name="deadSpin"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('base_dead') })}
	{template}
/>

<!-- the rare base-game spin where the special bar wakes up and drops a card -->
<Story
	name="specialBarHit"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('base_special') })}
	{template}
/>

<!-- TOMBSTONE OPEN: short reels grow taller, revealing buried symbols -->
<Story
	name="tombstoneOpen"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('coffin_open') })}
	{template}
/>

<!-- GUNSMOKE: every copy of one symbol morphs into the revolver WILD -->
<Story
	name="gunsmoke"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('gunsmoke') })}
	{template}
/>

<!-- GANG SPLIT: every premium on the board splits into extra ways -->
<Story
	name="splitGang"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('split_gang') })}
	{template}
/>

<!-- OUTLAW SPLIT: every low on the board splits into extra ways -->
<Story
	name="splitOutlaws"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('split_outlaws') })}
	{template}
/>

<!-- DIG UP: the sealed last-reel lane cracks open mid-spin -->
<Story
	name="digUp"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('dig_up') })}
	{template}
/>
