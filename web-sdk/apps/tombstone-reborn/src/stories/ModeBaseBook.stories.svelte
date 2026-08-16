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

<!-- the rare base-game spin where a feature symbol drops onto the board -->
<Story
	name="boardSpecial"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('base_special') })}
	{template}
/>

<!-- GUNSMOKE: lows get holes only; highs get masked blood inside the cell frame -->
<Story
	name="gunsmoke"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('gunsmoke') })}
	{template}
/>
<Story
	name="gunsmoke high"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('gunsmokeHigh') })}
	{template}
/>

<!-- SPLIT: one symbol type on the board gains extra ways -->
<Story
	name="split"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('split') })}
	{template}
/>

<!-- SUPER scatter: the sealed last-reel lane cracks open for this spin -->
<Story
	name="super scatter"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('tombstone') })}
	{template}
/>

<!-- NUDGE WAYS: lands on the top of reel 2, slams down, ways 2 → 4 → 8 → 16 -->
<Story
	name="nudgeWays"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('nudge_ways') })}
	{template}
/>

<!-- NUDGE WAYS full reel: the whole column is visible from the first frame -->
<Story
	name="nudgeWaysFull"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('nudge_ways_full') })}
	{template}
/>

<!-- NUDGE WAYS mid land: row 3 already shows 3/4 of the column, then one step down -->
<Story
	name="nudgeWaysRow3"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('nudge_ways_row3') })}
	{template}
/>

<!-- 3 BONUS tombstones: anticipation hang after the 2nd, then SMALL BONUS -->
<Story
	name="naturalTrigger"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('natural_trigger') })}
	{template}
/>
