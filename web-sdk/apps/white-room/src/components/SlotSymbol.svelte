<script lang="ts" module>
	import { ColorMatrixFilter } from 'pixi.js';

	// A LOCKED cell is only a tease: the symbol behind the closed bars is drained
	// of colour and dimmed so it reads as inert, in contrast with the full-colour
	// symbols in the cells the bonus has actually opened. One shared filter for
	// every locked cell (a filter per cell would cost an extra render pass each).
	const LOCKED_FILTER = new ColorMatrixFilter();
	LOCKED_FILTER.desaturate();
	LOCKED_FILTER.brightness(0.82, true);
	const LOCKED_FILTERS = [LOCKED_FILTER];
	// always pass a concrete array (never undefined): a cell that unlocks mid-spin
	// has to actively CLEAR the filter, and undefined props are skipped on sync.
	const NO_FILTERS: (typeof LOCKED_FILTER)[] = [];
</script>

<script lang="ts">
	import { untrack } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backIn, backOut } from 'svelte/easing';
	import { Container, Rectangle, Text } from 'pixi-svelte';

	import Symbol from './Symbol.svelte';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import type { SymbolName, SymbolState } from '../game/types';

	type Props = {
		cx: number;
		cy: number;
		size: number;
		/** crop the cell's visible height to this (design px). The symbol keeps
		 * its full-width proportions and the overflow is hidden — for the short
		 * bottom cells, which show a full-size symbol cut off at the waist. */
		clipH?: number;
		/** crop the visible width too (design px) — the cell's socket width */
		clipW?: number;
		/** corner radius of the crop (design px) — matches the cell's socket */
		clipRadius?: number;
		/** the content this cell should hold now; undefined = the cell empties out */
		name?: SymbolName;
		multiplier?: number;
		win?: boolean;
		dropDur?: number;
		locked?: boolean;
	};

	const props: Props = $props();
	const context = getContext();

	const scale = $derived(props.size / SYMBOL_SIZE);
	/** mask size in local (pre-scale) units */
	const maskH = $derived(props.clipH != null ? props.clipH / scale : SYMBOL_SIZE);
	const maskW = $derived(props.clipW != null ? props.clipW / scale : SYMBOL_SIZE);
	const OUT_DUR = 260; // reel-out mirrors the board reels sliding down (backIn)

	// What is CURRENTLY in the cell, held separately from the props so the
	// OUTGOING symbol can finish reeling out before the incoming one moves in
	// (the props flip to the new content the moment the spin starts).
	type Content = { name: SymbolName; multiplier?: number; locked: boolean };
	let shown = $state<Content | null>(null);
	let landed = $state(false);
	const state = $derived<SymbolState>(props.win ? 'win' : landed ? 'static' : 'land');
	const showMult = $derived((shown?.multiplier ?? 1) > 1);

	// Travel of the whole cell contents: -SYMBOL_SIZE parks it above the cell,
	// 0 is seated, +SYMBOL_SIZE has it clear out through the bottom. The isMask
	// rectangle hides it in either parked position, so it reels in and out
	// "within the symbol space" exactly like a board symbol.
	const dropY = new Tween(-SYMBOL_SIZE, { duration: 0 });

	const same = (a: Content | null, b: Content | null) =>
		a === b ||
		(!!a &&
			!!b &&
			a.name === b.name &&
			a.multiplier === b.multiplier &&
			a.locked === b.locked);

	// serialises overlapping transitions: a spin that starts mid-drop wins.
	let seq = 0;
	// what an in-flight transition is heading towards (undefined while idle), so
	// unrelated prop churn during the spin can't restart the reel-out mid-way.
	let heading: Content | null | undefined = undefined;
	const transitionTo = async (next: Content | null) => {
		const mine = ++seq;
		heading = next;
		if (shown) {
			// reel OUT downward, the way the board reels slide away on a new spin
			await dropY.set(SYMBOL_SIZE, { duration: OUT_DUR, easing: backIn });
			if (mine !== seq) return;
			shown = null;
		}
		if (next) {
			// park above the cell, then reel the new content in
			shown = next;
			landed = false;
			dropY.set(-SYMBOL_SIZE, { duration: 0 });
			await dropY.set(0, { duration: props.dropDur ?? 300, easing: backOut });
			if (mine !== seq) return;
		}
		heading = undefined;
	};

	// The whole frame of special symbols reels OUT together when the spin starts
	// (slotsReleased false) and reels back IN together once the MAIN board has
	// landed (slotsReleased true) — no per-cell stagger. Content that appears
	// later in the spin (a CLONE / SPLIT feature card) reels in on its own.
	$effect(() => {
		const released = context.stateGame.slotsReleased;
		const wanted: Content | null =
			released && props.name
				? { name: props.name, multiplier: props.multiplier, locked: !!props.locked }
				: null;
		untrack(() => {
			// already there, or already on the way there
			if (heading === undefined ? same(shown, wanted) : same(heading, wanted)) return;
			transitionTo(wanted);
		});
	});
</script>

<Container x={props.cx} y={props.cy} scale={scale}>
	<!-- clip the travel to this cell so the symbol reels in and out "within the
		symbol space", never spilling over the housing -->
	<Rectangle
		isMask
		anchor={0.5}
		width={maskW}
		height={maskH}
		borderRadius={(props.clipRadius ?? 0) / scale}
		backgroundColor={0xffffff}
	/>
	{#if shown}
		<!-- everything the cell holds rides the same travel, so the scrim and the
			multiplier badge reel out with their symbol instead of hanging behind -->
		<Container y={dropY.current}>
			<Container filters={shown.locked ? LOCKED_FILTERS : NO_FILTERS}>
				<Symbol
					{state}
					rawSymbol={{ name: shown.name, multiplier: shown.multiplier }}
					oncomplete={() => {
						if (!props.win) landed = true;
					}}
				/>
			</Container>
			{#if shown.locked}
				<!-- shadow scrim over the caged symbol; sits UNDER the bars, which
					LockedSlots draws on top of this whole cell. Kept light: the symbol
					must still read clearly THROUGH the bars, just cold and inert. -->
				<Rectangle
					anchor={0.5}
					width={SYMBOL_SIZE}
					height={SYMBOL_SIZE}
					backgroundColor={0x04060a}
					backgroundAlpha={0.26}
				/>
			{/if}
			{#if showMult}
				<!-- keep the badge inside the VISIBLE box: clipped cells (side/bottom
					openings narrower than a board card) would otherwise mask it away -->
				<Container
					x={Math.min(maskW, SYMBOL_SIZE) * 0.28}
					y={Math.min(maskH, SYMBOL_SIZE) * 0.3}
				>

					<Text
						anchor={0.5}
						text={`x${shown.multiplier}`}
						style={{
							fontFamily: 'Arial',
							fontWeight: '900',
							fontSize: SYMBOL_SIZE * 0.26,
							fill: 0xffe9a8,
							stroke: { color: 0x1a1816, width: 4 },
							letterSpacing: 1,
						}}
					/>
				</Container>
			{/if}
		</Container>
	{/if}
</Container>
