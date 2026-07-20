<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { stateShake } from '../game/stateShake.svelte';

	const context = getContext();
	// keep the ornate frame inside the 800-wide portrait canvas (board is
	// SYMBOL_SIZE*5 = 700; 700*1.10 = 770 leaves a small margin each side)
	const SPRITE_SCALE = { width: 1.1, height: 1.12 };
	const POSITION_ADJUSTMENT = 1.01;

	// the frame kicks with the board on split detonations
	const frameX = $derived(
		context.stateGameDerived.boardLayout().x * POSITION_ADJUSTMENT + stateShake.x,
	);
	const frameY = $derived(
		context.stateGameDerived.boardLayout().y * POSITION_ADJUSTMENT + stateShake.y,
	);
</script>

<!-- ornate haunted-mirror ring behind the reels frame, flourishes peek out around it -->
<Sprite
	key="mirrorFrame"
	zIndex={-2}
	anchor={0.5}
	x={frameX}
	y={frameY}
	width={context.stateGameDerived.boardLayout().width * SPRITE_SCALE.width * 1.06}
	height={context.stateGameDerived.boardLayout().height * SPRITE_SCALE.height * 1.1}
/>

<Sprite
	key="frame_bg.png"
	anchor={0.5}
	x={frameX}
	y={frameY}
	width={context.stateGameDerived.boardLayout().width * SPRITE_SCALE.width}
	height={context.stateGameDerived.boardLayout().height * SPRITE_SCALE.height}
/>

<Sprite
	key="frame_edge.png"
	anchor={0.5}
	x={frameX}
	y={frameY}
	width={context.stateGameDerived.boardLayout().width * SPRITE_SCALE.width}
	height={context.stateGameDerived.boardLayout().height * SPRITE_SCALE.height}
/>
