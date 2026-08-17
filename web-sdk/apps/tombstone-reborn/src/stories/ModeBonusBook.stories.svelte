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
	import { forceStorySpeed, playStory } from './playStory';

	setContext();

	// storybook has no wallet: fund the demo so bets and buy-bonus are clickable
	stateBet.balanceAmount = 100000;
	stateBet.betAmount = 1;
	forceStorySpeed(false);

	const play = playStory;
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

<!-- SMALL BONUS ROUND: bought freespins — banner, then 10 spins, 142x -->
<Story
	name="smallBonus"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('small_round') })}
	{template}
/>

<!-- BIG BONUS ROUND: bought superspins — banner, lane open, 10 spins, 6372x -->
<Story
	name="bigBonus"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('big_round') })}
	{template}
/>

<!-- SMALL BONUS: gunslinger connects 4 reels — a readable 48x BOUNTY -->
<Story
	name="smallBonusWin"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('small_bonus_win') })}
	{template}
/>

<!-- SUPER BONUS: gunslinger across the open lane, last cell wearing extra WAYS -->
<Story
	name="superBonusWin"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('super_bonus_win') })}
	{template}
/>

<!-- Open lane: a premium lands with extra WAYS on the cell, not the HUD WIN multi -->
<Story
	name="lastReelPremium"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('last_reel_premium') })}
	{template}
/>

<!-- MARK: last-reel shooter fires at every premium, +1 WIN multi once -->
<Story
	name="shooter"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('shooter') })}
	{template}
/>

<!-- SUPERSPLIT: gunslinger fills the first four reels, every cell goes 6x, last reel WILD -->
<Story
	name="superSplit"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('super_split') })}
	{template}
/>

<!-- NUDGE eats the L5s under it, then GUNSMOKE shoots only the L5s still on the board -->
<Story
	name="nudgeGunsmoke"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('nudge_gunsmoke') })}
	{template}
/>

<!-- NUDGE first (2 → 16), then SPLIT doubles the stack to 32 and the gunslinger faces -->
<Story
	name="nudgeSplit"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('nudge_split') })}
	{template}
/>

<!-- Split + gunsmoke + nudge: nudge first, then the other cards; HUD WIN multi climbs -->
<Story
	name="winMultClimb"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('win_mult_climb') })}
	{template}
/>

<!-- MAX WIN: the 99,999x spin — the Gunslinger finally smiles -->
<Story
	name="maxWin"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: play('max_win') })}
	{template}
/>
