<script lang="ts" module>
	/**
	 * LINKED CELL FIRE — every linked/wild cell gets a CONTINUOUS ORANGE BURNING
	 * FRAME that traces its border and licks outward, with the card face fully
	 * readable inside (matches assets-raw/ref_fire/ref_card.png).
	 *
	 * The fire is a pre-composited flipbook border (tools/make_cell_fire_atlas.py)
	 * drawn with NORMAL alpha blend — not runtime additive tongues. Two additive
	 * passes before this broke into disconnected yellow-green blobs at real cell
	 * size and, being additive, never rendered in the headless harness so they
	 * could not be verified. A baked border is continuous by construction, orange
	 * by grade, and renders identically headless and in-engine.
	 *
	 * Each cell draws its OWN full frame (no shared-edge suppression): the
	 * reference board shows adjacent burning cells each ringed in fire, seams and
	 * all, so a full frame per cell is the correct picture, not a special case.
	 */
	export type EmitterEventCellFire =
		| {
				type: 'cellFireShow';
				/** book positions; pad / off-diamond cells are dropped */
				cells: { reel: number; row: number }[];
				/** link size or multiplier — drives how hard the fire burns */
				level?: number;
		  }
		| { type: 'cellFireHide' };

	/** cap so a huge link can never spawn an unbounded number of sprites */
	const MAX_CELLS = 12;
</script>

<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import * as PIXI from 'pixi.js';
	import { MainContainer } from 'components-layout';
	import { Container, BaseSprite, getContextApp } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { filterVisibleCells } from '../game/boardCells';
	import {
		CELL_FIRE_ASSET,
		FRAME_FPS,
		SMOKE_FPS,
		GLOW_FRAME,
		CELL_FIRE_FRAME_COUNT,
		FIRE_FRAME_W_RATIO,
		FIRE_FRAME_H_RATIO,
		frameFrame,
		smokeFrame,
		emberFrame,
	} from '../game/cellFire';

	const context = getContext();
	const appContext = getContextApp();

	const frames = $derived(
		(appContext.stateApp.loadedAssets?.[CELL_FIRE_ASSET] as PIXI.Texture[] | undefined) ?? [],
	);

	const IGNITE_MS = 320;
	const DOUSE_MS = 300;

	let cells = $state<{ reel: number; row: number }[]>([]);
	let time = $state(0);
	const ignite = new Tween(0);

	/**
	 * FIRE YIELDS TO FEATURE OVERLAYS. A feature burst / nudge slide can be up over
	 * the same board; a full-strength fire pulled contrast off them. While any is
	 * up the fire drops to BURST_DIM, then swells back. Ref-counted so an
	 * overlapping second overlay hiding does not un-dim, and featureFxFallOut (the
	 * reveal wipe) hard-resets it.
	 */
	const BURST_DIM = 0.45;
	const BURST_DIM_MS = 240;
	const burstDim = new Tween(1);
	let activeOverlays = 0;
	const pushOverlay = () => {
		activeOverlays += 1;
		if (activeOverlays === 1) burstDim.set(BURST_DIM, { duration: BURST_DIM_MS, easing: cubicOut });
	};
	const popOverlay = () => {
		activeOverlays = Math.max(0, activeOverlays - 1);
		if (activeOverlays === 0) burstDim.set(1, { duration: BURST_DIM_MS, easing: cubicOut });
	};
	const resetOverlays = () => {
		activeOverlays = 0;
		burstDim.set(1, { duration: BURST_DIM_MS, easing: cubicOut });
	};

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	// Sprite footprint: the baked frame is FRAME/CARD bigger than the card, so the
	// flames sit just outside the card border and lick outward without stretching.
	const FIRE_W = SYMBOL_CARD_W * FIRE_FRAME_W_RATIO;
	const FIRE_H = SYMBOL_CARD_H * FIRE_FRAME_H_RATIO;

	const placed = $derived.by(() => {
		const layout = context.stateGameDerived.boardLayout();
		const originX = layout.x - layout.width * 0.5;
		const originY = layout.y - layout.height * 0.5;
		return cells.slice(0, MAX_CELLS).map((cell) => ({
			key: `${cell.reel}-${cell.row}`,
			cx: originX + getSymbolX(cell.reel),
			cy: originY + getCellCenterY(cell.reel, cell.row),
			seed: cell.reel * 7.31 + cell.row * 3.77,
		}));
	});

	/**
	 * FIRE AUDIO LIFECYCLE. ONE burn bed for the whole feature, never one per
	 * cell. The loop player ignores a second play while running; `burning` makes a
	 * re-show with more cells flare instead of re-triggering the bed. The bed stops
	 * on douse AND destroy so a feature that ends early can never leave fire under
	 * the next spin.
	 */
	let burning = false;
	let burningCells = 0;

	const startFire = (cellCount: number) => {
		if (burning) {
			if (cellCount > burningCells) {
				context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fire_flare', forcePlay: true });
			}
			burningCells = Math.max(burningCells, cellCount);
			return;
		}
		burning = true;
		burningCells = cellCount;
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fire_ignite' });
		context.eventEmitter.broadcast({ type: 'soundLoop', name: 'sfx_fire_loop' });
	};

	const stopFire = (withTail: boolean) => {
		if (!burning) return;
		burning = false;
		burningCells = 0;
		context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_fire_loop' });
		if (withTail) context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fire_out' });
	};

	onDestroy(() => stopFire(false));

	context.eventEmitter.subscribeOnMount({
		cellFireShow: ({ cells: incoming }) => {
			const visible = filterVisibleCells([...incoming]);
			if (!visible.length) return;
			cells = visible;
			startFire(visible.length);
			ignite.set(1, { duration: IGNITE_MS, easing: cubicOut });
		},
		cellFireHide: async () => {
			if (!cells.length) return;
			stopFire(true);
			await ignite.set(0, { duration: DOUSE_MS });
			cells = [];
		},
		// dim the fire while a feature overlay owns the foreground, restore after
		featureBurstShow: () => pushOverlay(),
		featureBurstHide: () => popOverlay(),
		nudgeSlideShow: () => pushOverlay(),
		nudgeSlideHide: () => popOverlay(),
		featureFxFallOut: () => resetOverlays(),
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<!-- zIndex 8: over the board and feature overlays (0), under CellFlameBorder (9)
	/ CellLightning (10) and the screen panels at 20. -->
<Container zIndex={8}>
	<MainContainer>
		{#if ignite.current > 0.01 && frames.length >= CELL_FIRE_FRAME_COUNT}
			<!-- burn folds in burstDim so the whole fire recedes together while a
				feature overlay is up -->
			{@const burn = ignite.current * burstDim.current}
			{#each placed as cell (cell.key)}
				<Container x={cell.cx} y={cell.cy}>
					<!-- Warm light the fire throws on the card face. Additive; adds
						richness in-engine (invisible in the headless GL harness, which the
						normal-blend frame below covers for). -->
					<BaseSprite
						texture={frames[GLOW_FRAME]}
						anchor={0.5}
						width={FIRE_W * 1.05}
						height={FIRE_H * 1.02}
						alpha={0.16 * burn}
						tint={0xff5a12}
						blendMode="add"
					/>

					<!-- THE BURNING FRAME. Pre-composited, continuous, orange, drawn
						NORMAL blend so it reads exactly like the reference and renders in
						headless. Motion comes ONLY from the flipbook (the flame tongues
						licking phase to phase) — the sprite size and alpha are HELD steady
						so the fire never breathes/pulses in and out and never bulges past
						the cell. -->
					<BaseSprite
						texture={frames[frameFrame(Math.floor(time * FRAME_FPS + cell.seed * 5))]}
						anchor={0.5}
						width={FIRE_W}
						height={FIRE_H}
						alpha={burn}
					/>

					<!-- Black smoke rolling off the top edge. -->
					{#each [0, 1, 2] as puff (puff)}
						{@const s = cell.seed + puff * 5.1}
						{@const life = (time * 0.4 + rand(s)) % 1}
						<BaseSprite
							texture={frames[smokeFrame(Math.floor(time * SMOKE_FPS + rand(s) * 16))]}
							anchor={0.5}
							x={(rand(s + 1) - 0.5) * SYMBOL_CARD_W * 0.7 + (rand(s + 2) - 0.5) * 30 * life}
							y={-SYMBOL_CARD_H * 0.4 - life * (SYMBOL_CARD_H * 0.9)}
							width={(38 + rand(s + 3) * 30) * (0.5 + life * 1.3)}
							height={(38 + rand(s + 3) * 30) * (0.5 + life * 1.3)}
							rotation={(rand(s + 4) - 0.5) * 2 + life * 0.6}
							alpha={0.32 * burn * Math.sin(Math.min(life, 1) * Math.PI)}
						/>
					{/each}

					<!-- Rising embers off the border — additive, in-engine sparkle. -->
					{#each [0, 1, 2, 3] as e (e)}
						{@const s = cell.seed + e * 9.7}
						{@const life = (time * (0.5 + rand(s) * 0.3) + rand(s + 5)) % 1}
						<BaseSprite
							texture={frames[emberFrame(Math.floor(rand(s) * 8))]}
							anchor={0.5}
							x={(rand(s + 1) - 0.5) * SYMBOL_CARD_W * 0.9 + Math.sin(life * 6 + rand(s) * 6) * 6}
							y={SYMBOL_CARD_H * 0.5 - life * SYMBOL_CARD_H * 1.15}
							width={5 + rand(s + 2) * 7}
							height={5 + rand(s + 2) * 7}
							alpha={burn * (1 - life) * 0.9}
							blendMode="add"
						/>
					{/each}
				</Container>
			{/each}
		{/if}
	</MainContainer>
</Container>
