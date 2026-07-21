<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { OnHotkey } from 'components-shared';
	import { Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();

	// NLC-style "slam stop": tapping anywhere over the reels while a spin /
	// animation is in progress fires the SAME signal as the stop button
	// (`stopButtonClick`) — Board interrupts the dropping reels and Turbo
	// fast-forwards the rest of the presentation. It self-resets at the end of
	// the spin (playBet broadcasts `stopButtonEnable`). While idle the catcher is
	// not mounted, so it never blocks anything and idle taps do nothing.
	const busy = $derived(!context.stateXstateDerived.isIdle());

	const skip = () => {
		if (context.stateXstateDerived.isIdle()) return;
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	// invisible hit region covering exactly the reel area (board design space, so
	// it scales with the board and never overlaps the HUD bar beneath it).
	// boardLayout() is centered (anchor 0.5) at board.x / board.y.
	const board = $derived(context.stateGameDerived.boardLayout());
</script>

<!-- space bar slam-stops too (works even when turbo isn't latched on) -->
{#if busy}
	<OnHotkey hotkey="Space" onpress={skip} />
{/if}

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
