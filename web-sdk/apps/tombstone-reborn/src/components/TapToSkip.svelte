<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { OnHotkey } from 'components-shared';
	import { Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();

	// Shared skip bus (spin + presentation): when not idle, reel-area tap / Space
	// broadcast `stopButtonClick` — the SAME signal as the HUD stop button.
	// Listeners (do not replace this path; extend it):
	//   Board            → enhancedBoard.stop() (slam-stop dropping reels)
	//   ButtonTurbo      → temporary turbo (fast-forward remaining FX)
	//   ButtonBetProvider→ disable stop until stopButtonEnable
	//   WinCelebration   → advance/dismiss big-win stages
	//   FreeSpinOutro / BonusLevelBanner / Transition → dismiss overlays
	// Overlays that cover the board also broadcast stopButtonClick on press
	// (full-screen catchers) so one UX covers spin + celebration + FS panels.
	const busy = $derived(!context.stateXstateDerived.isIdle());

	const skip = () => {
		// Always broadcast — overlay listeners (BonusLevelBanner / Win / Outro /
		// Transition) no-op when hidden. Do NOT gate on isIdle: Storybook Action
		// calls playBet while xstate stays idle, so a gate here left CONTINUE
		// panels undismissable via Space.
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	// invisible hit region covering exactly the reel area (board design space, so
	// it scales with the board and never overlaps the HUD bar beneath it).
	// boardLayout() is centered (anchor 0.5) at board.x / board.y.
	const board = $derived(context.stateGameDerived.boardLayout());
</script>

<!-- Space always available (Storybook Action + real play). Reel tap only while
	actor is busy so idle board clicks still reach symbols/HUD. -->
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
			y={board.y}
			width={board.width}
			height={board.height}
			backgroundColor={0x000000}
			backgroundAlpha={0.001}
			onpointerdown={skip}
		/>
	{/if}
</MainContainer>
