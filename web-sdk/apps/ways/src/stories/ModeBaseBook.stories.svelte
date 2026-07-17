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
	import { randomInteger } from 'utils-shared/random';
	import { stateBet } from 'state-shared';

	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import { playBet } from '../game/utils';
	import books from './data/base_books';
	import mirrorBooks from './data/mirror_books';
	import maxwinBook from './data/maxwin_book';

	setContext();

	// storybook has no wallet: fund the demo so bets and buy-bonus are clickable
	stateBet.balanceAmount = 10000;
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

<Story
	name="random"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const index = randomInteger({ min: 0, max: books.length - 1 });
			const data = books[index];
			console.log('Running a book at index', index);
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>

<Story
	name="maxwinShowcase"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('Running the MAX WIN showcase: full board of H1 at max apparitions');
			await playBet({ ...maxwinBook, state: maxwinBook.events });
		},
	})}
	{template}
/>

<Story
	name="mirrorBurstShowcase"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const data = mirrorBooks[0];
			console.log('Running the xMirror showcase book');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>

<Story
	name="bonusLevel1_TheSeance"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const data = mirrorBooks[1];
			console.log('Running THE SEANCE (level 1 bonus) showcase book');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>

<Story
	name="bonusLevel2_TheOtherSide"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const data = mirrorBooks[2];
			console.log('Running THE OTHER SIDE (level 2 bonus) showcase book');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>

<Story
	name="bonusLevel3_BloodMoon"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const data = mirrorBooks[3];
			console.log('Running BLOOD MOON (level 3 bonus) showcase book');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>
