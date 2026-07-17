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

	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import { playBet } from '../game/utils';
	import books from './data/base_books';
	import allLinesBooks from './data/all_lines_books';
	import nudgeBooks from './data/nudge_books';

	setContext();
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
	name="wildNudgeShowcase"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const data = nudgeBooks[0];
			console.log('Running the wild-nudge showcase book');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>

<Story
	name="allFiftyLinesWin"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const data = allLinesBooks[0];
			console.log('Running the all-50-lines-win book');
			await playBet({ ...data, state: data.events });
		},
	})}
	{template}
/>
