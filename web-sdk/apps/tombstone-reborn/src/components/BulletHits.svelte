<script lang="ts">
	/**
	 * CLICK-TO-SHOOT. While the board is at rest a left click on the reel area
	 * punches a shattered-glass bullet hole at the cursor, flashes muzzle fire,
	 * hangs Kenney gunsmoke. The holes persist until a spin starts, then they
	 * clear. No revolver sprite — fire and smoke only. The hit region only
	 * exists while idle AND the reels are stopped, so a click during a spin
	 * goes to TapToSkip (super turbo + slam-stop) instead.
	 */
	import * as PIXI from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { quadIn } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W } from '../game/constants';
	import { GUNSMOKE_HOLE_KEYS } from '../game/gunsmokeSpin';
	import BulletHit from './BulletHit.svelte';
	import MuzzleSmoke from './MuzzleSmoke.svelte';

	const context = getContext();

	const idle = $derived(context.stateXstateDerived.isIdle());
	const spinning = $derived(context.stateGameDerived.reelsSpinning());
	const roundLive = $derived(context.stateGame.roundLive);
	const canShoot = $derived(idle && !spinning && !roundLive);
	const board = $derived(context.stateGameDerived.boardLayout());

	/** the shooter has a six-shooter: 6 rounds, then dry until the next spin. */
	const SHOTS_PER_ROUND = 6;
	/** decal footprint in board px — a bit under a symbol so it reads as a hit,
	 * not a takeover of the whole cell. */
	const SIZE = SYMBOL_CARD_W * 0.8;
	const VARIANTS = GUNSMOKE_HOLE_KEYS;

	// fireburst.png: cone originates lower-right, sprays upper-left
	const BURST_SRC_W = 1084;
	const BURST_SRC_H = 888;
	const BURST_ORIGIN_X = 980 / BURST_SRC_W;
	const BURST_ORIGIN_Y = 680 / BURST_SRC_H;
	const BURST_W = 60;
	const BURST_H = BURST_W * (BURST_SRC_H / BURST_SRC_W);
	const BURST_FADE_MS = 150;

	type Hit = {
		id: number;
		x: number;
		y: number;
		size: number;
		rotation: number;
		key: string;
	};
	type Puff = { id: number; x: number; y: number; size: number };
	let hits = $state<Hit[]>([]);
	let puffs = $state<Puff[]>([]);
	let shotsFired = $state(0);
	let nextId = 0;
	let flashAt = $state<{ x: number; y: number } | null>(null);

	const burst = new Tween(0);

	// reload the six-shooter + wipe the glass the instant a spin starts
	// (xstate leave-idle, or Storybook playBet that stays idle). Each new
	// round starts clean with 6 shots.
	$effect(() => {
		if (!canShoot) {
			if (hits.length) hits = [];
			if (puffs.length) puffs = [];
			shotsFired = 0;
			flashAt = null;
			burst.set(0, { duration: 0 });
		}
	});

	const localOf = (event: PIXI.FederatedPointerEvent) => {
		const parent = (event.currentTarget as PIXI.Container).parent as PIXI.Container;
		return event.getLocalPosition(parent);
	};

	const kick = () => {
		burst.set(1, { duration: 0 });
		void burst.set(0, { duration: BURST_FADE_MS, easing: quadIn });
	};

	const shoot = (event: PIXI.FederatedPointerEvent) => {
		if (!canShoot || shotsFired >= SHOTS_PER_ROUND) return;
		const local = localOf(event);
		flashAt = { x: local.x, y: local.y };

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
		kick();
		// Kenney gunsmoke hangs in WORLD space at the shot. Two overlapping
		// wisps so a single click still reads as a puff.
		puffs = [
			...puffs,
			{
				id: nextId++,
				x: local.x + (Math.random() - 0.5) * 6,
				y: local.y - 4,
				size: 40 + Math.random() * 10,
			},
			{
				id: nextId++,
				x: local.x + (Math.random() - 0.5) * 10,
				y: local.y - 8,
				size: 32 + Math.random() * 8,
			},
		];

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

	{#each puffs as puff (puff.id)}
		<MuzzleSmoke
			x={puff.x}
			y={puff.y}
			size={puff.size}
			oncomplete={() => {
				puffs = puffs.filter((p) => p.id !== puff.id);
			}}
		/>
	{/each}

	{#if canShoot}
		<!-- invisible-but-hittable reel-area catcher (same trick as TapToSkip). -->
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
			onpointerdown={shoot}
		/>
	{/if}

	{#if flashAt && burst.current > 0.04}
		<Sprite
			key="muzzleBurst"
			x={flashAt.x}
			y={flashAt.y}
			anchor={{ x: BURST_ORIGIN_X, y: BURST_ORIGIN_Y }}
			width={BURST_W * (0.85 + 0.35 * burst.current)}
			height={BURST_H * (0.85 + 0.35 * burst.current)}
			alpha={burst.current}
			blendMode="add"
			eventMode="none"
			zIndex={8}
		/>
	{/if}
</MainContainer>
