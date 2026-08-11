<script lang="ts" module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	// Stake Engine mandatory book: COMPONENTS/Game exercises the whole Game
	// component in isolation — the loading screen and the resting (pre-spin) board.
	// See https://stakeengine.github.io/math-sdk/fe_docs/explore_sb/
	const { Story } = defineMeta({
		title: 'COMPONENTS/Game',
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
	import { getContext, setContext } from '../game/context';
	import { getReelWindow, getReelYOffset } from '../game/utils';

	setContext();
	const context = getContext();

	// QA probe: run a whole spin cycle (preSpin fall-out -> reveal fall-in) and
	// measure, from live reel state, how long the board shows ZERO symbols inside
	// the reel windows. This is the "empty outlined cells" window; the number is
	// stashed on window.__reelEmptyMs for tools/qa_reel_empty_window.py to read.
	const runSpinCycle = async () => {
		const eb = context.stateGameDerived.enhancedBoard;
		const board = context.stateGame.board;
		// a valid reveal reusing the resting board's raw symbols (same shape) so
		// no RGS round-trip is needed and the only delay is the fall-out gate
		const revealEvent = {
			index: 0,
			type: 'reveal',
			board: board.map((reel: any) => reel.reelState.symbols.map((s: any) => ({ ...s.rawSymbol }))),
			anticipation: board.map(() => 0),
		} as any;

		// per-reel visible-symbol count; a reel is "empty" (blank cells) when 0
		const reelVisible = (reel: any) => {
			const win = getReelWindow(reel.reelIndex);
			const off = getReelYOffset(reel.reelIndex);
			let n = 0;
			for (const s of reel.reelState.symbols) {
				const y = s.symbolY.current + off;
				if (y >= win.top && y <= win.bottom) n += 1;
			}
			return n;
		};

		// The perceived "empty outlined cells" is the WORST reel: the leftmost
		// reel empties first, then waits out the fall-out stagger + reveal gate
		// before it refills. Track each reel's empty episode and report the max.
		const n = board.length;
		const emptyStart = new Array(n).fill(0);
		const seenEmpty = new Array(n).fill(false);
		const doneReel = new Array(n).fill(false);
		const emptyMs = new Array(n).fill(0);
		const t0 = performance.now();
		(window as any).__reelEmptyMs = null;
		const tick = () => {
			const now = performance.now();
			board.forEach((reel: any, i: number) => {
				if (doneReel[i]) return;
				const v = reelVisible(reel);
				if (!seenEmpty[i] && v === 0) {
					seenEmpty[i] = true;
					emptyStart[i] = now;
				} else if (seenEmpty[i] && v > 0) {
					doneReel[i] = true;
					emptyMs[i] = Math.round(now - emptyStart[i]);
				}
			});
			const allDone = doneReel.every(Boolean);
			if (!allDone && now - t0 < 10000) requestAnimationFrame(tick);
			else (window as any).__reelEmptyMs = Math.max(0, ...emptyMs);
		};
		requestAnimationFrame(tick);

		await Promise.all([eb.preSpin({}), eb.spin({ revealEvent })]);
	};

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

<!-- COMPONENTS/Game/component: the full game WITH the loading screen (Tombstone
	dig-out intro → tap to enter). skipLoadingScreen is false on purpose. -->
<Story
	name="component (loadingScreen)"
	args={templateArgs({ skipLoadingScreen: false, data: {}, action: async () => {} })}
	{template}
/>

<!-- COMPONENTS/Game/preSpin: the resting board the player sees before a spin.
	Runs the same preSpin the actor runs at round start (actor.ts onNewGame). -->
<Story
	name="preSpin"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await context.stateGameDerived.enhancedBoard.preSpin({});
		},
	})}
	{template}
/>

<!-- COMPONENTS/Game/spinCycle: a full spin (fall-out -> reveal fall-in). Used by
	tools/qa_reel_empty_window.py to measure the empty-board window (window.__reelEmptyMs). -->
<Story
	name="spinCycle"
	args={templateArgs({
		skipLoadingScreen: true,
		data: {},
		action: async () => {
			await runSpinCycle();
		},
	})}
	{template}
/>
