<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'BONUS_ENTRY/banner',
	});
</script>

<script lang="ts">
	/**
	 * The bonus-entry banner, driven exactly the way real play drives it.
	 *
	 * A bought round is identified by `stateBet.activeBetModeKey` (set by
	 * ModalBuyBonusConfirm on confirm), and `playBet` awaits the banner before it
	 * plays a book event — so setting the key here and playing that mode's showcase
	 * book reproduces the live path end to end, banner then spin. The MODE_BONUS
	 * stories leave the key on BASE and therefore show no banner, which is correct:
	 * they exercise the reels, not the purchase.
	 *
	 * This file exists because the five overlays deleted before this banner were
	 * never verifiable from Storybook at all, which is how they stayed broken.
	 */
	import {
		StoryGameTemplate,
		StoryLocale,
		type TemplateArgs,
		templateArgs,
	} from 'components-storybook';
	import { stateBet } from 'state-shared';
	import { STATE_BET, STATE_IDLE } from 'utils-xstate/src/constants';

	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import { stateXstate } from '../game/stateXstate';
	import { playBet } from '../game/utils';
	import type { BonusEntryTier } from '../game/bonusEntryArt';
	import { bookByLabel } from './data/tombstone_books';
	import { forceStorySpeed } from './playStory';

	setContext();

	// storybook has no wallet: fund the demo so bets and buy-bonus are clickable
	stateBet.balanceAmount = 100000;
	stateBet.betAmount = 1;
	forceStorySpeed(false);

	const buy =
		(mode: BonusEntryTier, label: string, options?: { turbo?: boolean }) => async () => {
			const data = bookByLabel(label);
			forceStorySpeed(!!options?.turbo);
			// what ModalBuyBonusConfirm does on confirm, and the only signal that
			// tells playBet this round was bought
			stateBet.activeBetModeKey = mode;
			// Live, `playBet` only ever runs from the actor's onPlayGame, with the
			// machine already out of idle. Calling it straight from a story left the
			// machine idle, and an idle machine makes the bet button's Space hotkey
			// mean SPIN rather than STOP — so pressing Space to skip the banner also
			// fired a real bet request. Standing in for the machine keeps Space doing
			// here exactly what it does in play: hand the banner off.
			stateXstate.value = STATE_BET;
			console.log(`Buying "${mode}" then running the "${label}" book (${data.payoutMultiplier}x)`);
			try {
				await playBet({ ...data, state: data.events } as never);
			} finally {
				stateXstate.value = STATE_IDLE;
				stateBet.activeBetModeKey = 'BASE';
			}
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

<!-- DEAD MAN'S HAND (80x): the six-card special bar is awake for one spin -->
<Story
	name="deadMansHand"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: buy('bonus_small', 'small_bonus_win'),
	})}
	{template}
/>

<!-- OPEN GRAVE (1,000x): the bar plus the sealed last-reel lane, cracked open -->
<Story
	name="openGrave"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: buy('bonus_super', 'super_bonus_win'),
	})}
	{template}
/>

<!-- Turbo: every banner duration is shortened by fxDur, like every feature -->
<Story
	name="openGraveTurbo"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: buy('bonus_super', 'super_bonus_win', { turbo: true }),
	})}
	{template}
/>
