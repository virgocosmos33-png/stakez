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
	import { backOut } from 'svelte/easing';
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { stateBet } from 'state-shared';
	import { stateSlots } from 'utils-slots';
	import { waitForTimeout } from 'utils-shared/wait';

	import Symbol from './Symbol.svelte';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, SPIN_OPTIONS_DEFAULT, SPIN_OPTIONS_FAST } from '../game/constants';
	import { TR_INK_GOLD, trValueStyle } from '../game/typography';
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
		/** a W that grows its reel rather than substituting — wears the arrow card */
		expanding?: boolean;
		win?: boolean;
		locked?: boolean;
		/** ms to wait before reeling OUT when the board's pre-spin starts, so the
		 * cell leaves in its own column's stagger slot (LockedSlots supplies it;
		 * sampled at spin time because turbo zeroes it) */
		fallOutDelay?: () => number;
		/** awaited before reeling IN, so the cell lands with its own column:
		 * left before reel 0, bottom cells with their reels, right after the
		 * last reel (LockedSlots supplies it; resolves instantly mid-spin, so a
		 * feature card dropped later is never held up) */
		fallInGate?: () => Promise<void>;
	};

	const props: Props = $props();
	const context = getContext();

	const scale = $derived(props.size / SYMBOL_SIZE);
	/** mask size in local (pre-scale) units */
	const maskH = $derived(props.clipH != null ? props.clipH / scale : SYMBOL_SIZE);
	const maskW = $derived(props.clipW != null ? props.clipW / scale : SYMBOL_SIZE);

	// The cell reels on the board's own terms: same px/ms fall speed, same
	// backOut bounce on landing, same turbo response. Read per transition rather
	// than derived — the options must be fixed for the whole of one drop.
	const spinOptions = () => (stateBet.isTurbo ? SPIN_OPTIONS_FAST : SPIN_OPTIONS_DEFAULT);

	// What is CURRENTLY in the cell, held separately from the props so the
	// OUTGOING symbol can finish reeling out before the incoming one moves in
	// (the props flip to the new content the moment the spin starts).
	type Content = {
		name: SymbolName;
		multiplier?: number;
		expanding?: boolean;
		locked: boolean;
	};
	let shown = $state<Content | null>(null);
	let landed = $state(false);
	// travelling through the cell, so it wears the motion smear like a board symbol
	let moving = $state(false);
	// NB: not named `state` — a local binding by that name makes TypeScript
	// resolve the `$state` rune to it and every rune in the file errors out.
	const symbolState = $derived<SymbolState>(
		props.win ? 'win' : moving ? 'spin' : landed ? 'static' : 'land',
	);
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
			a.expanding === b.expanding &&
			a.locked === b.locked);

	// serialises overlapping transitions: a spin that starts mid-drop wins.
	let seq = 0;
	// what an in-flight transition is heading towards (undefined while idle), so
	// unrelated prop churn during the spin can't restart the reel-out mid-way.
	let heading: Content | null | undefined = undefined;
	// WHEN this cell's column is due to reel out, as an absolute timestamp
	// anchored to the pre-spin start. A timestamp rather than a one-shot delay:
	// a reveal that arrives before a late column's slot would otherwise cancel
	// the parked wait and yank the cell out early — anchoring it means every
	// transition that reels the old content out honours the same stagger slot.
	let parkDueAt = 0;
	const transitionTo = async (next: Content | null, gate?: () => Promise<void>) => {
		const mine = ++seq;
		heading = next;

		if (shown) {
			// hold the old content until this column's fall-out stagger slot
			// (already in the past on turbo, bonus reveals and mid-spin drops)
			const wait = parkDueAt - Date.now();
			if (wait > 0) {
				await waitForTimeout(wait);
				if (mine !== seq) return;
			}
			// reel OUT downward: linear at the board's fall-out speed, exactly as
			// a board symbol slides out of its row when a spin starts
			moving = true;
			await dropY.set(SYMBOL_SIZE, {
				duration: SYMBOL_SIZE / spinOptions().symbolFallOutSpeed,
			});
			if (mine !== seq) return;
			shown = null;
		}

		if (next) {
			// hold until this cell's own column is falling in, so the whole
			// frame of special cells lands in board order instead of as one
			// block after the board
			if (gate) {
				await gate();
				if (mine !== seq) return;
			}
			// reel IN from above: linear fall stopping a bounce short of the seat,
			// then the same backOut settle the board lands on. Options sampled
			// AFTER the gate: the wait can span a turbo toggle.
			const options = spinOptions();
			const bounce = SYMBOL_SIZE * options.symbolFallInBounceSizeMulti;
			shown = next;
			landed = false;
			moving = true;
			dropY.set(-SYMBOL_SIZE, { duration: 0 });
			await dropY.set(-bounce, {
				duration: (SYMBOL_SIZE - bounce) / options.symbolFallInSpeed,
			});
			if (mine !== seq) return;
			moving = false;
			await dropY.set(0, {
				duration: bounce / options.symbolFallInBounceSpeed,
				easing: backOut,
			});
			if (mine !== seq) return;
		}

		moving = false;
		heading = undefined;
	};

	// PARK with the board's own pre-spin: the moment the reels start their
	// staggered fall-out, this cell reels out too, delayed into its own column's
	// stagger slot (left cage first, bottoms with their reels, right cage last —
	// the main reels were shifted to slots 1..5 to make room, see stateGame).
	// parkedForSpin keeps the release effect below from reeling the OLD content
	// straight back in while the RGS round trip is still in flight.
	let parkedForSpin = $state(false);
	let wasPreSpinning = stateSlots.isPreSpinning;
	$effect(() => {
		const pre = stateSlots.isPreSpinning;
		untrack(() => {
			if (pre && !wasPreSpinning) {
				parkedForSpin = true;
				parkDueAt = Date.now() + (props.fallOutDelay?.() ?? 0);
				transitionTo(null);
			}
			wasPreSpinning = pre;
		});
	});

	// The cells reel OUT when the spin parks them (pre-spin above, or
	// slotsReleased dropping on a bonus reveal) and reel back IN once the reveal
	// releases them — each cell then gated onto its own column via fallInGate,
	// so the frame lands with the board instead of after it. Content that
	// appears later in the spin (a CLONE / SPLIT feature card) reels in on its
	// own; its gate resolves instantly on a stopped board.
	$effect(() => {
		const released = context.stateGame.slotsReleased;
		const wanted: Content | null =
			released && props.name
				? {
						name: props.name,
						multiplier: props.multiplier,
						expanding: props.expanding,
						locked: !!props.locked,
					}
				: null;
		untrack(() => {
			// the reveal parks (false) then releases (true): observing the park
			// clears the pre-spin latch so the release can reel the cell in
			if (!released) parkedForSpin = false;
			if (parkedForSpin) return;
			// already there, or already on the way there
			if (heading === undefined ? same(shown, wanted) : same(heading, wanted)) return;
			transitionTo(wanted, wanted ? props.fallInGate : undefined);
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
					state={symbolState}
					rawSymbol={{
						name: shown.name,
						multiplier: shown.multiplier,
						expanding: shown.expanding,
					}}
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
						style={trValueStyle({
							fontSize: SYMBOL_SIZE * 0.26,
							fill: TR_INK_GOLD,
							stroke: { color: 0x1a1816, width: 4 },
							letterSpacing: 1,
						})}
					/>
				</Container>
			{/if}
		</Container>
	{/if}
</Container>
