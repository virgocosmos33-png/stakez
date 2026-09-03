<script lang="ts" module>
	import type { RawSymbol, Position } from '../game/types';

	export type EmitterEventBoard =
		| { type: 'boardSettle'; board: RawSymbol[][] }
		| { type: 'boardShow' }
		| { type: 'boardHide' }
		| {
				type: 'boardWithAnimateSymbols';
				symbolPositions: Position[];
		  };
</script>

<script lang="ts">
	import { waitForResolve } from 'utils-shared/wait';
	import { BoardContext } from 'components-shared';

	import { getContext } from '../game/context';
	import { isHighPaySymbol } from '../game/gunsmokeSpin';
	import BoardContainer from './BoardContainer.svelte';
	import BoardMask from './BoardMask.svelte';
	import BoardBase from './BoardBase.svelte';
	import WinDim from './WinDim.svelte';
	import WinLinkMark from './WinLinkMark.svelte';

	const context = getContext();

	let show = $state(true);

	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => context.stateGameDerived.enhancedBoard.stop(),
		boardSettle: ({ board }) => context.stateGameDerived.enhancedBoard.settle(board),
		boardShow: () => (show = true),
		boardHide: () => (show = false),
		boardWithAnimateSymbols: async ({ symbolPositions }) => {
			const getPromises = () =>
				symbolPositions.map(async (position) => {
					const reelSymbol =
						context.stateGame.board[position.reel]?.reelState.symbols[position.row];
					if (!reelSymbol) {
						console.error(
							'[Board] boardWithAnimateSymbols missing symbol',
							position,
						);
						return;
					}
					reelSymbol.symbolState = 'win';
					// Spine/sprite win must resolve; if the anim never fires complete
					// (missing track, off-screen wrap), don't hang the whole book.
					await Promise.race([
						waitForResolve((resolve) => (reelSymbol.oncomplete = resolve)),
						new Promise<void>((resolve) => {
							window.setTimeout(resolve, 2500);
						}),
					]);
					reelSymbol.symbolState = isHighPaySymbol(reelSymbol.rawSymbol.name)
						? 'postWin'
						: 'static';
				});

			await Promise.all(getPromises());
		},
	});

	context.stateGameDerived.enhancedBoard.readyToSpinEffect();
</script>

{#if show}
	<BoardContext animate={false}>
		<BoardContainer>
			<BoardMask />
			<BoardBase />
			<WinDim />
		</BoardContainer>
	</BoardContext>

	<BoardContext animate={true}>
		<BoardContainer>
			<BoardBase />
		</BoardContainer>
	</BoardContext>

	<!-- Over idle plates and faces. Highs live on the animate layer so the
		hat clears the pocket clip; an earlier slot under that layer buried
		the skim. Band hides before winFacesRise. -->
	<WinLinkMark layer="wipe" />
{/if}
