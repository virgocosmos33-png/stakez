<script lang="ts">
	/**
	 * Click target over the left lantern globe. Lives in the game layer (not
	 * the zIndex -2 room) so the board never swallows the shot. Armed while
	 * the board is at rest and the lamp is not already swinging from a hit.
	 */
	import { Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { saloonLamp, strikeLamp } from '../game/saloonLamp.svelte';
	import { lampGlobeCanvas } from '../game/saloonLampSmash';

	const context = getContext();
	const idle = $derived(context.stateXstateDerived.isIdle());
	const spinning = $derived(context.stateGameDerived.reelsSpinning());
	const globe = $derived(lampGlobeCanvas(context.stateLayoutDerived.canvasSizes()));
	const armed = $derived(
		idle &&
			!spinning &&
			saloonLamp.lit &&
			saloonLamp.mode === 'idle' &&
			context.stateGame.atmosphere === 'base',
	);

	const strike = () => {
		if (!armed) return;
		strikeLamp();
		context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_lamp_smash' });
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_lamp_smash' });
	};
</script>

{#if armed}
	<Rectangle
		eventMode="static"
		cursor="pointer"
		anchor={0.5}
		x={globe.x}
		y={globe.y}
		width={globe.width}
		height={globe.height}
		backgroundColor={0x000000}
		backgroundAlpha={0.001}
		onpointerdown={strike}
		zIndex={6}
	/>
{/if}
