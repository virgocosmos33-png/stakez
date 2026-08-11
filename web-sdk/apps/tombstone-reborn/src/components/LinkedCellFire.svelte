<script lang="ts" module>
	/**
	 * LINKED CELL FIRE — every linked/wild cell burns with the user's CodePen
	 * "burning letters" fire traced around its card BORDER.
	 *
	 * The fire itself lives in BorderFireLayer.svelte: an imperative pooled
	 * particle system stepping the reference simulation verbatim (density is
	 * what makes it read as real fire, and only an imperative pool reaches the
	 * reference's live-particle count). This component keeps owning the
	 * lifecycle: which cells burn, ignite/douse ramps, the fire audio bed, and
	 * dimming under feature overlays — plus the reference's dim ember base
	 * (rgba(60,10,0,0.8)) stroked around each burning card.
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
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import type { Graphics as PixiGraphics } from 'pixi.js';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import BorderFireLayer from './BorderFireLayer.svelte';
	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { filterVisibleCells } from '../game/boardCells';

	const context = getContext();

	const IGNITE_MS = 320;
	const DOUSE_MS = 300;

	let cells = $state<{ reel: number; row: number }[]>([]);
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

	const burn = $derived(ignite.current * burstDim.current);

	const HW = SYMBOL_CARD_W / 2;
	const HH = SYMBOL_CARD_H / 2;

	const placed = $derived.by(() => {
		const layout = context.stateGameDerived.boardLayout();
		const originX = layout.x - layout.width * 0.5;
		const originY = layout.y - layout.height * 0.5;
		return cells.slice(0, MAX_CELLS).map((cell) => ({
			key: `${cell.reel}-${cell.row}`,
			cx: originX + getSymbolX(cell.reel),
			cy: originY + getCellCenterY(cell.reel, cell.row),
		}));
	});

	/** the reference's "hot ember base" (rgba(60,10,0,0.8)) under the flames */
	const drawEmberBase = (g: PixiGraphics) => {
		g.roundRect(-HW, -HH, SYMBOL_CARD_W, SYMBOL_CARD_H, 10);
		g.stroke({ color: 0x3c0a00, width: 7, alpha: 1 });
	};

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
</script>

<!-- zIndex 8: over the board and feature overlays (0), under CellFlameBorder (9)
	/ CellLightning (10) and the screen panels at 20. -->
<Container zIndex={8}>
	<MainContainer>
		<!-- ember base per burning cell (under the particles) -->
		{#if burn > 0.01}
			{#each placed as cell (cell.key)}
				<Container x={cell.cx} y={cell.cy}>
					<Graphics draw={drawEmberBase} alpha={0.8 * burn} />
				</Container>
			{/each}
		{/if}

		<!-- the fire: permanently mounted pooled particle layer. Spawning follows
			`burn`; on douse the live particles finish their own burn-out. -->
		<BorderFireLayer cells={placed} {burn} />
	</MainContainer>
</Container>
