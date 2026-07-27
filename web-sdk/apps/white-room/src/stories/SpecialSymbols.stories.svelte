<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'SPECIAL SYMBOLS/showcase',
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

	import {
		wildReelSingleReel1Book,
		wildReelSingleReel2Book,
		wildReelDoubleBook,
		wildReelTripleBook,
	} from './data/wild_reel_books';
	import {
		unlockedSlotsLevel1Book,
		unlockedSlotsLevel2Book,
		unlockedSlotsLevel3Book,
	} from './data/unlocked_slot_books';
	import eyeBooks from './data/eye_books';
	import mirrorBooks from './data/mirror_books';
	import featureBooks from './data/feature_books';
	import bonusBooks from './data/bonus_books';
	import maxwinBook from './data/maxwin_book';
	import allFeaturesBook from './data/all_features_book';
	import comboFeaturesBook from './data/combo_features_book';

	setContext();

	// storybook has no wallet: fund the demo so bets/buys are clickable
	stateBet.balanceAmount = 100000;
	stateBet.betAmount = 1;

	type AnyBook = { id: number; events: any[] };

	const play = async (book: AnyBook) => {
		await playBet({ ...book, state: book.events });
	};

	// pick the first bonus book that reaches a given bonus level (1/2/3)
	const bonusByLevel = (level: number): AnyBook =>
		(bonusBooks as AnyBook[]).find((b) =>
			b.events.some((e) => e.type === 'bonusLevel' && e.level === level),
		) ?? (bonusBooks as AnyBook[])[0];
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

<!--
	ALL FEATURES IN ONE SPIN — a single level-3 bonus spin where every feature
	fires together: Unlocked Slots open the board, a Wild Reel rises, a Stretch
	overflows a reel, a Clone converts a symbol, and a Split multiplies a winning
	symbol's cells — then it resolves into a win. Sliced straight from the build.
-->
<Story
	name="allFeatures_oneSpin"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('ALL FEATURES: unlocked slots + wild reel + stretch + clone + split', allFeaturesBook.id);
			await play(allFeaturesBook as AnyBook);
		},
	})}
	{template}
/>

<!--
	COMBO SHOWCASE — one level-3 bonus spin hand-composed to show MULTIPLES of
	every feature at once: 2 clones, 2 splits, 2 wild reels, 1 NORMAL-reel stretch
	(per-symbol x-ways) and 1 WILD-reel stretch (wild column + N WAYS).
-->
<Story
	name="comboShowcase_multiOfEach"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('COMBO: 2 clone + 2 split + 2 wild reel + normal & wild stretch', comboFeaturesBook.id);
			await play(comboFeaturesBook as AnyBook);
		},
	})}
	{template}
/>

<!--
	WILD REEL — special symbols in the bottom locked slots raise a wild column,
	growing reels 1/2/3 to 4 rows. The risen wilds carry multipliers and the
	board then resolves as ways. Books below are pulled straight from the build.
-->

<!-- 1 special: reel 1 (3→4) grows one wild, resolves into a ways win -->
<Story
	name="wildReel_1_singleReel"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('WILD REEL: single middle reel grows to 4, resolves', wildReelSingleReel1Book.id);
			await play(wildReelSingleReel1Book);
		},
	})}
	{template}
/>

<!-- reel 2 (2→4) grows two wilds, one carrying a x10 multiplier -->
<Story
	name="wildReel_2_reel2_highMult"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('WILD REEL: reel 2 grows 2→4 with high multiplier', wildReelSingleReel2Book.id);
			await play(wildReelSingleReel2Book);
		},
	})}
	{template}
/>

<!-- 2 specials: two middle reels grow together -->
<Story
	name="wildReel_3_doubleReel"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('WILD REEL: two middle reels grow', wildReelDoubleBook.id);
			await play(wildReelDoubleBook);
		},
	})}
	{template}
/>

<!-- 3 specials: all three middle reels grow → the 7-wide "best case" board -->
<Story
	name="wildReel_4_tripleReel_7wide"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('WILD REEL: all three middle reels grow (7-wide)', wildReelTripleBook.id);
			await play(wildReelTripleBook);
		},
	})}
	{template}
/>

<!--
	UNLOCKED SLOTS — during free spins the reserved locked slots open by bonus
	level and fill with premiums or wilds, expanding the board toward 6/7 reels:
	  L1 → bottom slots (extends the middle reels, up to 5-of-a-kind)
	  L2 → + right column (a 6th reel, up to 6-of-a-kind)
	  L3 → + left column (a 7th reel, the full 7-wide board)
	Books below are sliced single spins pulled straight from the build.
-->

<!-- L1: bottom slots unlock; premiums drop under the middle reels -->
<Story
	name="unlockedSlots_1_level1_bottom"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('UNLOCKED SLOTS: level 1 (bottom)', unlockedSlotsLevel1Book.id);
			await play(unlockedSlotsLevel1Book);
		},
	})}
	{template}
/>

<!-- L2: bottom + RIGHT column unlock → 6th reel, up to 6-of-a-kind -->
<Story
	name="unlockedSlots_2_level2_right"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('UNLOCKED SLOTS: level 2 (+right, 6-wide)', unlockedSlotsLevel2Book.id);
			await play(unlockedSlotsLevel2Book);
		},
	})}
	{template}
/>

<!-- L3: bottom + right + LEFT unlock → the full 7-wide board -->
<Story
	name="unlockedSlots_3_level3_7wide"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			console.log('UNLOCKED SLOTS: level 3 (+left, 7-wide)', unlockedSlotsLevel3Book.id);
			await play(unlockedSlotsLevel3Book);
		},
	})}
	{template}
/>

<!--
	HAUNTED MIRROR (HM) — reflects neighbours into apparition multipliers and
	resolves the mirror into its best neighbouring face.
-->

<!-- base-game mirror burst -->
<Story
	name="hauntedMirror_1_base"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const book = mirrorBooks[0] as AnyBook;
			console.log('HAUNTED MIRROR: base burst', book.id);
			await play(book);
		},
	})}
	{template}
/>

<!-- feature spin: 1 guaranteed mirror -->
<Story
	name="hauntedMirror_2_oneMirror"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.activeBetModeKey = 'feature1';
			const book = featureBooks[1] as AnyBook;
			console.log('HAUNTED MIRROR: 1 guaranteed mirror', book.id);
			await play(book);
		},
	})}
	{template}
/>

<!-- feature spin: 2 guaranteed mirrors -->
<Story
	name="hauntedMirror_3_twoMirrors"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.activeBetModeKey = 'feature2';
			const book = featureBooks[2] as AnyBook;
			console.log('HAUNTED MIRROR: 2 guaranteed mirrors', book.id);
			await play(book);
		},
	})}
	{template}
/>

<!-- feature spin: 3 guaranteed mirrors -->
<Story
	name="hauntedMirror_4_threeMirrors"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.activeBetModeKey = 'feature3';
			const book = featureBooks[3] as AnyBook;
			console.log('HAUNTED MIRROR: 3 guaranteed mirrors', book.id);
			await play(book);
		},
	})}
	{template}
/>

<!--
	MADAM'S EYE (ME) — converts the reflected/split cells into wilds, then the
	board resolves.
-->
<Story
	name="madamsEye_1_convert"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const book = eyeBooks[0] as AnyBook;
			console.log("MADAM'S EYE: convert + resolve", book.id);
			await play(book);
		},
	})}
	{template}
/>

<Story
	name="madamsEye_2_freegame"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const book = (eyeBooks[1] ?? eyeBooks[0]) as AnyBook;
			console.log("MADAM'S EYE: freegame convert", book.id);
			await play(book);
		},
	})}
	{template}
/>

<!--
	SCATTER (S) — three+ scatters trigger free spins at the reached bonus level.
-->
<Story
	name="scatter_1_bonusLevel1"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const book = bonusByLevel(1);
			console.log('SCATTER: free spins, level 1', book.id);
			await play(book);
		},
	})}
	{template}
/>

<Story
	name="scatter_2_bonusLevel2"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const book = bonusByLevel(2);
			console.log('SCATTER: free spins, level 2', book.id);
			await play(book);
		},
	})}
	{template}
/>

<Story
	name="scatter_3_bonusLevel3"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const book = bonusByLevel(3);
			console.log('SCATTER: free spins, level 3', book.id);
			await play(book);
		},
	})}
	{template}
/>

<!-- WINCAP — a full run that clamps at the max-win ceiling -->
<Story
	name="wincap_maxWin"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const book = maxwinBook as AnyBook;
			console.log('WINCAP: max win', book.id);
			await play(book);
		},
	})}
	{template}
/>
