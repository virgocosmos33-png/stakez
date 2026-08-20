<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	// Stake Engine mandatory book: COMPONENTS/WinCelebration exercises every win
	// presentation in isolation — the small "YOU WON" count-up plate, each big
	// hero-plate tier, and the staged rollup that climbs through all tiers.
	// These are OUR hunt tiers (LAST AMEN → BACK FROM HELL & BACK TO HELL & BACK), not another game's.
	const { Story } = defineMeta({
		title: 'COMPONENTS/WinCelebration',
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
	import { presentWinCelebration } from '../game/bookEventHandlerMap';
	import { winFramePick, type WinFrameId } from '../game/winCelebrationArt';
	import { forceStorySpeed } from './playStory';

	setContext();

	// storybook has no wallet: fund the demo so bets and buy-bonus are clickable
	stateBet.balanceAmount = 10_000_000;
	stateBet.betAmount = 1;
	forceStorySpeed(false);

	// amount is a book amount; tier = amount / 100 as a multiple of bet. This runs
	// the SAME live presentation setWin runs (tier art + coins + sound bed +
	// staged rollup), so what a story shows is exactly what a real win shows.
	const celebrate = (amount: number, ways: number, frame?: WinFrameId) => async () => {
		forceStorySpeed(false);
		if (frame) winFramePick.id = frame;
		console.log(`Presenting a ${amount / 100}x win (${ways} ways)`);
		await presentWinCelebration(amount, ways);
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

<!-- YOU WON plate: the small-win count-up over the board (tier "nice", < 25x). -->
<Story
	name="YOU WON plate (small)"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(1200, 24) })}
	{template}
/>

<!-- Scene 1 — LAST AMEN (25x+) -->
<Story
	name="Scene 1 LAST AMEN"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(3000, 48) })}
	{template}
/>

<Story
	name="Frame A carpentry"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(3000, 48, 'carpentry') })}
	{template}
/>
<Story
	name="Frame B saloon"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(3000, 48, 'saloon') })}
	{template}
/>
<Story
	name="Frame C casket"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(3000, 48, 'casket') })}
	{template}
/>
<Story
	name="Frame D meat hook"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(3000, 48, 'hook') })}
	{template}
/>

<!-- Scene 2 — DUST TRAIL (50x+) -->
<Story
	name="Scene 2 DUST TRAIL"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(7500, 96) })}
	{template}
/>

<!-- Scene 3 — HANG THE PIG (100x+) -->
<Story
	name="Scene 3 HANG THE PIG"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(25000, 268) })}
	{template}
/>

<!-- Scene 4 — THE LAST WORDS (500x+) -->
<Story
	name="Scene 4 THE LAST WORDS"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(100000, 512) })}
	{template}
/>

<!-- Scene 5 — HAUL THE DEAD (2,500x+) -->
<Story
	name="Scene 5 HAUL THE DEAD"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(500000, 4096) })}
	{template}
/>

<!-- Scene 6 — BACK FROM HELL & BACK TO HELL & BACK / MAX WIN (30,000x+) -->
<Story
	name="Scene 6 BACK FROM HELL & BACK TO HELL & BACK (MAX)"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(3_000_000, 46656) })}
	{template}
/>

<!-- win tiers staged rollup: the MAX amount climbs through every tier in one
	presentation (getTiersPassed). Each plate stays until its clip finishes,
	then the next starts, unless skipped. -->
<Story
	name="win tiers staged rollup"
	args={templateArgs({ skipLoadingScreen: true, data: {}, action: celebrate(3_000_000, 46656) })}
	{template}
/>
