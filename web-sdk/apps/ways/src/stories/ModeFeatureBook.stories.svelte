<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'MODE_FEATURE/book',
	});
</script>

<script lang="ts">
	import {
		StoryGameTemplate,
		StoryLocale,
		type TemplateArgs,
		templateArgs,
	} from 'components-storybook';
	import { stateBet, stateModal } from 'state-shared';

	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import { playBet } from '../game/utils';
	import featureBooks from './data/feature_books';

	setContext();

	// storybook has no wallet: fund the demo so bets and buys are clickable
	stateBet.balanceAmount = 100000;
	stateBet.betAmount = 1;
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

<!-- The buy menu with all 7 options: EXTRA BET + 3 feature spins + 3 bonus buys -->
<Story
	name="buyMenu"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateModal.modal = { name: 'buyBonus' };
		},
	})}
	{template}
/>

<!-- EXTRA BET active: reel-1 scatter guaranteed, this book triggers the bonus -->
<Story
	name="extraBet_anteTrigger"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.activeBetModeKey = 'ante';
			const data = featureBooks[0];
			console.log('Running EXTRA BET (ante) book: reel-1 scatter, bonus trigger');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>

<!-- MIRROR SPIN (10x): one guaranteed haunted mirror -->
<Story
	name="featureSpin1_MirrorSpin"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.activeBetModeKey = 'feature1';
			const data = featureBooks[1];
			console.log('Running MIRROR SPIN (feature1) book: 1 guaranteed mirror');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>

<!-- TWIN MIRRORS (20x): two guaranteed haunted mirrors -->
<Story
	name="featureSpin2_TwinMirrors"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.activeBetModeKey = 'feature2';
			const data = featureBooks[2];
			console.log('Running TWIN MIRRORS (feature2) book: 2 guaranteed mirrors');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>

<!-- TRIPLE MIRRORS (40x): three guaranteed haunted mirrors -->
<Story
	name="featureSpin3_TripleMirrors"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.activeBetModeKey = 'feature3';
			const data = featureBooks[3];
			console.log('Running TRIPLE MIRRORS (feature3) book: 3 guaranteed mirrors');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>
