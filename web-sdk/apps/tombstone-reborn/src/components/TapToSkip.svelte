<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { OnHotkey } from 'components-shared';
	import { Rectangle } from 'pixi-svelte';

	import { stateBet } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();

	// Shared skip bus (spin + presentation): when not idle OR the reels are
	// in flight, reel-area tap / Space broadcast `stopButtonClick` — the SAME
	// signal as the HUD stop button.
	// Listeners (do not replace this path; extend it):
	//   Board            → enhancedBoard.stop() (slam-stop dropping reels)
	//   ButtonTurbo      → temporary turbo (fast-forward remaining FX)
	//   ButtonBetProvider→ disable stop until stopButtonEnable
	//   WinCelebration   → advance/dismiss big-win stages
	//   Transition       → dismiss overlay
	// Overlays that cover the board also broadcast stopButtonClick on press
	// (full-screen catchers) so one UX covers spin + celebration.
	//
	// Reel motion is required because Storybook Action calls playBet while
	// xstate stays idle — without it the shooter stayed armed and this
	// catcher never mounted.
	const spinning = $derived(context.stateGameDerived.reelsSpinning());
	const busy = $derived(!context.stateXstateDerived.isIdle() || spinning);

	const skip = () => {
		// A click on moving reels is super turbo for this spin (faster fall
		// + timeScale), then the shared slam-stop bus. Transient: the HUD
		// bolts clear on stopButtonEnable unless the player already locked
		// a turbo tier with the button.
		if (spinning) {
			stateBet.isTurbo = true;
			stateBet.isSuperTurbo = true;
		}
		// Always broadcast — overlay listeners (Win / Transition) no-op when
		// hidden. Do NOT gate on isIdle: Storybook Action keeps xstate idle.
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	// invisible hit region covering exactly the reel area (board design space, so
	// it scales with the board and never overlaps the HUD bar beneath it).
	// boardLayout() is centered (anchor 0.5) at board.x / board.y.
	const board = $derived(context.stateGameDerived.boardLayout());
</script>

<!-- Space always available (Storybook Action + real play). Reel tap only while
	the actor is busy or the reels are moving, so a settled idle board still
	reaches the shooter / HUD. -->
<OnHotkey hotkey="Space" onpress={skip} />

<MainContainer>
	{#if busy}
		<!-- eventMode/cursor live on the Rectangle itself (i.e. the drawn
			Graphics) so Pixi actually hit-tests the geometry. A near-zero alpha
			keeps it invisible while remaining hittable. -->
		<Rectangle
			eventMode="static"
			cursor="pointer"
			anchor={0.5}
			x={board.x}
			y={(board.visualTop + board.visualBottom) * 0.5}
			width={board.visualRight - board.visualLeft}
			height={board.visualBottom - board.visualTop}
			backgroundColor={0x000000}
			backgroundAlpha={0.001}
			onpointerdown={skip}
		/>
	{/if}
</MainContainer>
