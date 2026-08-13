<script lang="ts">
	/**
	 * CLICK-TO-SHOOT. While the board is IDLE a left click on the reel area punches
	 * a shattered-glass bullet hole at the cursor. The holes persist (they stack,
	 * capped) until a spin starts, at which point they are all cleared and the
	 * board spins normally.
	 *
	 * The hit region only exists while idle, so it never fights TapToSkip's
	 * busy-only reel catcher, and it sits above the board symbols so the cracks
	 * read as glass over the whole reel window.
	 */
	import * as PIXI from 'pixi.js';
	import { MainContainer } from 'components-layout';
	import { Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W } from '../game/constants';
	import BulletHit from './BulletHit.svelte';

	const context = getContext();

	const idle = $derived(context.stateXstateDerived.isIdle());
	const board = $derived(context.stateGameDerived.boardLayout());

	/** the shooter has a six-shooter: 6 rounds, then dry until the next spin. */
	const SHOTS_PER_ROUND = 6;
	/** decal footprint in board px — a bit under a symbol so it reads as a hit,
	 * not a takeover of the whole cell. */
	const SIZE = SYMBOL_CARD_W * 0.8;
	const VARIANTS = ['bulletCrack1', 'bulletCrack2', 'bulletCrack3', 'bulletCrack4', 'bulletCrack5'];

	type Hit = {
		id: number;
		x: number;
		y: number;
		size: number;
		rotation: number;
		key: string;
	};
	let hits = $state<Hit[]>([]);
	let shotsFired = $state(0);
	let nextId = 0;

	// reload the six-shooter + wipe the glass the instant the board leaves idle
	// (spin / feature start), so each new round starts clean with 6 shots.
	$effect(() => {
		if (!idle) {
			if (hits.length) hits = [];
			shotsFired = 0;
		}
	});

	const shoot = (event: PIXI.FederatedPointerEvent) => {
		if (shotsFired >= SHOTS_PER_ROUND) return; // out of bullets this round

		// Map to the SAME container the decals live in (the MainContainer inner
		// container that both the hit rect and the hit sprites are children of),
		// so the hole lands exactly under the cursor regardless of board offset.
		const parent = (event.currentTarget as PIXI.Container).parent as PIXI.Container;
		const local = event.getLocalPosition(parent);
		const hit: Hit = {
			id: nextId++,
			x: local.x,
			y: local.y,
			size: SIZE * (0.85 + Math.random() * 0.4),
			rotation: Math.random() * Math.PI * 2,
			key: VARIANTS[Math.floor(Math.random() * VARIANTS.length)],
		};
		hits = [...hits, hit];
		shotsFired += 1;

		// .44 magnum: cut any still-ringing shot and retrigger from the top so
		// rapid clicks bang each time instead of layering into mush.
		context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_gunshot' });
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_gunshot' });
	};
</script>

<MainContainer>
	{#each hits as hit (hit.id)}
		<BulletHit x={hit.x} y={hit.y} size={hit.size} rotation={hit.rotation} spriteKey={hit.key} />
	{/each}

	{#if idle}
		<!-- invisible-but-hittable reel-area catcher (same trick as TapToSkip). -->
		<Rectangle
			eventMode="static"
			cursor="crosshair"
			anchor={0.5}
			x={board.x}
			y={board.y}
			width={board.width}
			height={board.height}
			backgroundColor={0x000000}
			backgroundAlpha={0.001}
			onpointerdown={shoot}
		/>
	{/if}
</MainContainer>
