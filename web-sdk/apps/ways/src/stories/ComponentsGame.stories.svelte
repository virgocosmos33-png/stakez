<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	const { Story } = defineMeta({
		title: 'COMPONENTS/<Game>',
	});
</script>

<script lang="ts">
	import {
		StoryLocale,
		StoryGameTemplate,
		type TemplateArgs,
		templateArgs,
	} from 'components-storybook';
	import { stateBet, stateModal } from 'state-shared';

	import { stateGame, stateGameDerived } from '../game/stateGame.svelte';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';
	import { eventEmitter } from '../game/eventEmitter';
	import config from '../game/config';

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

<Story name="component (loadingScreen)">
	<StoryLocale lang="en">
		<Game />
	</StoryLocale>
</Story>

<Story
	name="preSpin"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await stateGameDerived.enhancedBoard.preSpin({
				paddingBoard: config.paddingReels[stateGame.gameType],
			});
		},
	})}
	{template}
/>

<Story
	name="emitterEvent: boardHide"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			eventEmitter.broadcast({ type: 'boardHide' });
		},
	})}
	{template}
/>

<!-- QA: buy menu with EXTRA BET + feature spins + bonus buys (horizontal strip) -->
<Story
	name="buyMenu"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.balanceAmount = 100000;
			stateBet.betAmount = 1;
			stateModal.modal = { name: 'buyBonus' };
		},
	})}
	{template}
/>

<!-- QA: buy menu at $0 balance — every card is unaffordable → all greyed out -->
<Story
	name="buyMenuGreyed"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.balanceAmount = 0;
			stateBet.betAmount = 1;
			stateModal.modal = { name: 'buyBonus' };
		},
	})}
	{template}
/>

<!-- QA: mixed affordability — balance 50 @ bet 1 funds ante/feature1-3 (<=40x)
	but not the bonus buys (100x/400x/1000x), so some cards colour + some grey -->
<Story
	name="buyMenuMixed"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.balanceAmount = 50;
			stateBet.betAmount = 1;
			stateModal.modal = { name: 'buyBonus' };
		},
	})}
	{template}
/>

<!-- QA: pay table / game info + settings tab (mono regression check) -->
<Story
	name="payTable"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateBet.balanceAmount = 100000;
			stateBet.betAmount = 1;
			stateModal.modal = { name: 'payTable' };
		},
	})}
	{template}
/>

<!-- QA: WAYS + FREE SPINS counters at typical values (panel-fit check) -->
<Story
	name="waysCounter"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: 600 });
			eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
			eventEmitter.broadcast({ type: 'freeSpinCounterUpdate', current: 1, total: 10 });
		},
	})}
	{template}
/>

<!-- QA: worst-case widths (6-digit ways, two-digit both sides) -->
<Story
	name="countersMax"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: 262144 });
			eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
			eventEmitter.broadcast({ type: 'freeSpinCounterUpdate', current: 15, total: 15 });
		},
	})}
	{template}
/>

<!-- QA: WIN + WAYS plaques (left rail) ON TOP of every ambient FX at once —
	green plasma liner, purple frame ring, apparition grow, and the WIN amount -->
<Story
	name="winWaysLayer"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			const positions = [
				{ reel: 1, row: 1 },
				{ reel: 2, row: 1 },
				{ reel: 2, row: 2 },
				{ reel: 3, row: 2 },
			];
			// ambient / decorative FX (must sit BELOW the readouts)
			eventEmitter.broadcast({ type: 'boardFrameGlowShow' }); // purple ring
			eventEmitter.broadcast({ type: 'winDimShow', positions });
			eventEmitter.broadcast({ type: 'apparitionsWinGrow', positions }); // green liner
			// side plaques (always-on amethyst) + centered red horror-font count-up
			eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: 15360 });
			stateBet.winBookEventAmount = 1234; // side WIN plaque value
			eventEmitter.broadcast({ type: 'winShow' });
			// amount/100 = 12.3x -> 'nice' small win = centered gold/horror font
			eventEmitter.broadcast({ type: 'winUpdate', amount: 1234 });
		},
	})}
	{template}
/>

<!-- QA: base-idle side character + always-on WAYS/WIN plaques, base game -->
<Story
	name="sceneBase"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateGame.gameType = 'basegame';
			stateBet.winBookEventAmount = 0;
		},
	})}
	{template}
/>

<!-- QA: bonus/free-spins ACTIVATED character (glowing hand-mirror). Sets the
	canonical freegame signal SceneCharacter swaps on -->
<Story
	name="sceneBonus"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			stateGame.gameType = 'freegame';
			eventEmitter.broadcast({ type: 'boardFrameGlowShow' });
			eventEmitter.broadcast({ type: 'waysCounterUpdate', ways: 15360 });
			eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
			eventEmitter.broadcast({ type: 'freeSpinCounterUpdate', current: 11, total: 15 });
			// free-spins also arms the collapse-HUD drawer button (portrait)
			eventEmitter.broadcast({ type: 'drawerButtonShow' });
		},
	})}
	{template}
/>

<!-- QA: BIG-WIN celebration (amount/100 = 5000x -> full-screen takeover) — must
	stay the centred horror-font takeover, NOT the rail plaque -->
<Story
	name="bigWin"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			eventEmitter.broadcast({ type: 'winShow' });
			eventEmitter.broadcast({ type: 'winUpdate', amount: 500000 });
		},
	})}
	{template}
/>
