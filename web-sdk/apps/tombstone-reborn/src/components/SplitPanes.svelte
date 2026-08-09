<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// SPLIT: the winning symbol is sliced into N center-cropped vertical panes that
	// snap apart (Madam-Mirror style pane-split), leaving a slim-seam "XN" cell.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle, Text } from 'pixi-svelte';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { fxDur } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import {
		SYMBOL_SIZE,
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
		HIGH_SYMBOLS,
	} from '../game/constants';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import ClawHand, { clawReach } from './ClawHand.svelte';

	const context = getContext();

	// Tombstone palette: hot brass cut, dusty glass, rust bleed — not clinical white.
	const CORE = 0xf0d78c;
	const GLASS = 0xc4a574;
	const BLOOD = 0xb54a2a;
	const DARK = 0x0a0806;

	type SplitCell = {
		key: string;
		reel: number;
		row: number;
		count: number;
		/** only set when the caller names the symbol explicitly; otherwise the
			cell follows whatever the board is currently showing there */
		pinned?: SymbolName;
		cx: number;
		cy: number;
		seed: number;
		/** true only while this cell is part of the currently-playing strike;
			persisted cells from earlier events stay settled and untouched */
		fresh: boolean;
	};
	type DrawnCell = SplitCell & { name: SymbolName };

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	let time = $state(0);
	// rides the panes off the bottom edge when the next spin starts
	const fallOut = new Tween(0);

	// 0 = whole symbol, 1 = fully split into panes
	const splitProgress = new Tween(1);
	// blade head sweeps top -> bottom carving the seams
	const cutSweep = new Tween(0);
	const seamFlare = new Tween(0);
	const detonation = new Tween(0);
	const pulse = new Tween(1);

	// CLAW STRIKE
	//
	// A patient's hand presses onto the scored symbol and is dragged DOWN it,
	// fingers closing into a clench as it goes, nails cutting four gouges. The
	// card comes apart on the clench.
	//
	// Only the POSES are textures (tools/make_claw_atlas.py bakes nine, open
	// through to fist, all pinned on the wrist). Travel, scale, roll, the pose
	// crossfade and the gouges are all computed here from a wall-clock
	// progress value and re-evaluated every rendered frame, so the motion runs
	// at whatever the display does — 240Hz included — instead of being capped
	// at a baked sheet's frame rate. Nine textures, not hundreds.
	//
	const CLAW_MS = 780;
	/** open-hand height on screen */
	const CLAW_HAND_H = CARD_H * 1.08;

	// phase boundaries in normalised progress
	const CLAW_PRESS = 0.2; // hand has faded in and taken hold
	const CLAW_IMPACT = 0.62; // clench — the card comes apart here
	const CLAW_RELEASE = 0.78; // grip held until here, then dragged away

	// wrist travel, relative to the card centre (y grows downward). It starts
	// below the card because the hand reaches up into the cell from underneath.
	const CLAW_WRIST_FROM = CARD_H * 0.58;
	const CLAW_WRIST_TO = CARD_H * 1.5;
	const CLAW_WRIST_EXIT = CARD_H * 2.5;

	/** -1 when idle, else normalised progress through the strike */
	let clawT = $state(-1);

	const mix = (from: number, to: number, t: number) => from + (to - from) * t;
	const span = (t: number, from: number, to: number) =>
		Math.min(Math.max((t - from) / (to - from), 0), 1);

	/** the drag accelerates, but gently — cubicIn sits still then lurches */
	const clawFall = (u: number) => u * u;

	/** wrist y at a given progress, in card-local coordinates */
	const clawWristY = (t: number) => {
		if (t < CLAW_PRESS) return CLAW_WRIST_FROM;
		if (t <= CLAW_IMPACT) {
			return mix(CLAW_WRIST_FROM, CLAW_WRIST_TO, clawFall(span(t, CLAW_PRESS, CLAW_IMPACT)));
		}
		if (t < CLAW_RELEASE) {
			return CLAW_WRIST_TO + CARD_H * 0.04 * span(t, CLAW_IMPACT, CLAW_RELEASE);
		}
		return mix(
			CLAW_WRIST_TO + CARD_H * 0.04,
			CLAW_WRIST_EXIT,
			cubicIn(span(t, CLAW_RELEASE, 1)),
		);
	};

	/**
	 * How closed the fingers are, 0 = flat open, 1 = clenched.
	 *
	 * Deliberately LINEAR across the drag. Any ease-in here (cubicIn especially)
	 * keeps the hand open for most of its travel and then snaps it shut in the
	 * last few milliseconds, which reads as the fingers not closing at all —
	 * they have to work their way closed the whole way down.
	 */
	const clawCurl = (t: number) =>
		t <= CLAW_IMPACT ? span(t, CLAW_PRESS * 0.5, CLAW_IMPACT) : 1;

	const clawAlpha = (t: number) =>
		t < CLAW_PRESS
			? 0.96 * cubicOut(span(t, 0, CLAW_PRESS))
			: 0.96 * (1 - cubicIn(span(t, CLAW_RELEASE, 1)));

	const clawScale = (t: number) =>
		t <= CLAW_IMPACT
			? mix(0.98, 1.09, span(t, CLAW_PRESS, CLAW_IMPACT))
			: mix(1.09, 1.0, span(t, CLAW_IMPACT, 1));

	const clawRoll = (t: number) => mix(-0.1, 0.09, span(t, 0, CLAW_RELEASE));

	/**
	 * Nail tip y. The hand shortens as the fingers curl, so the tips creep back
	 * toward the wrist — which is what makes it read as digging in and dragging
	 * rather than sliding.
	 */
	const clawNailY = (t: number) =>
		clawWristY(t) - CLAW_HAND_H * clawScale(t) * clawReach(clawCurl(t));

	/** run the strike once, calling `onImpact` on the clench */
	const playClaw = (onImpact: () => void) =>
		new Promise<void>((resolve) => {
			const start = performance.now();
			let fired = false;
			clawT = 0;
			const clawMs = fxDur(CLAW_MS);
			const step = (now: number) => {
				const t = (now - start) / clawMs;
				if (!fired && t >= CLAW_IMPACT) {
					fired = true;
					onImpact();
				}
				if (t >= 1) {
					clawT = -1;
					resolve();
					return;
				}
				clawT = t;
				requestAnimationFrame(step);
			};
			requestAnimationFrame(step);
		});

	// Every split cell gets the SAME treatment no matter its size: panes plus an
	// exact "Nx" stamp. The pane count is only a visual — past this many the
	// slices get too thin to read, so the geometry caps and the stamp carries
	// the real number. (It used to be three different looks: real panes below 5,
	// an untouched symbol at 5+, and a number only above 8 — which read as three
	// unrelated features.)
	const MAX_PANES = 4;

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	/**
	 * MERGE the incoming split cells into whatever is already up.
	 *
	 * A spin can fire several feature events back to back (split, clone, split
	 * again — see combo_features_book). The panes are supposed to stay on their
	 * cells until the next reveal, but replacing `cells` wholesale here meant
	 * every later `splitPanesShow` wiped the earlier cells' panes — and a split
	 * that only hit wild-column cells (all filtered out) cleared the entire
	 * overlay. Cells already up keep their panes; a cell named again gets its
	 * new count and re-animates.
	 *
	 * Returns true when at least one cell is new or changed, i.e. there is
	 * something for the claw strike to play on.
	 */
	const layout = (incoming: { reel: number; row: number; count: number; name?: SymbolName }[]) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		// reels shown as a full wild column (Wild Reel or Stretch) swallow the split:
		// the extra ways still count, but we never paint panes over the wild column.
		const wildReels = new Set([
			...context.stateGame.wildReelReels,
			...context.stateGame.stretchedReels,
		]);
		// carry surviving cells over settled, refreshing their centres — features
		// that ran since their split (wild reel, stretch) can shift reel offsets
		const merged = new Map<string, SplitCell>(
			cells
				.filter((cell) => !wildReels.has(cell.reel))
				.map((cell) => [
					cell.key,
					{
						...cell,
						fresh: false,
						cx: originX + getSymbolX(cell.reel),
						cy: originY + getCellCenterY(cell.reel, cell.row),
					},
				]),
		);
		let anyFresh = false;
		for (const c of incoming) {
			if (c.count <= 1 || wildReels.has(c.reel)) continue;
			const reelSymbol = context.stateGame.board[c.reel]?.reelState.symbols[c.row];
			if (!c.name && !reelSymbol) continue;
			const key = `${c.reel}-${c.row}`;
			const existing = merged.get(key);
			if (existing && existing.count === c.count && existing.pinned === c.name) continue;
			anyFresh = true;
			merged.set(key, {
				key,
				reel: c.reel,
				row: c.row,
				count: c.count,
				pinned: c.name,
				cx: originX + getSymbolX(c.reel),
				cy: originY + getCellCenterY(c.reel, c.row),
				seed: c.reel * 31 + c.row * 7 + c.count * 113,
				fresh: true,
			});
		}
		cells = [...merged.values()];
		show = cells.length > 0;
		return anyFresh;
	};

	/**
	 * The symbol each split cell is CURRENTLY showing, re-read every frame.
	 *
	 * The panes stay up until the next reveal, so a later feature on the same
	 * cell can move the board out from under them. Holding the name from layout
	 * time meant a CLONE morphing a split cell left the old symbol painted over
	 * the new premium, since this overlay mounts above the board.
	 */
	const drawn = $derived(
		cells
			.map((cell) => ({
				...cell,
				// position re-solved LIVE too: a STRETCH racking this reel after the
				// split moves every row, and the panes must ride along
				cy:
					context.stateGameDerived.boardLayout().y -
					context.stateGameDerived.boardLayout().height * 0.5 +
					getCellCenterY(cell.reel, cell.row),
				name:
					cell.pinned ??
					(context.stateGame.board[cell.reel]?.reelState.symbols[cell.row]?.rawSymbol
						.name as SymbolName | undefined),
			}))
			.filter((cell): cell is DrawnCell => cell.name != null),
	);

	// The claw drives the whole beat: it fades in over every scored symbol, and
	// the panes only come apart on the frame its nails go through the card. The
	// seam blades run underneath it as the cut it is making.
	const runSplit = async () => {
		splitProgress.set(0, { duration: 0 });
		cutSweep.set(0, { duration: 0 });
		seamFlare.set(0, { duration: 0 });
		detonation.set(0, { duration: 0 });
		pulse.set(1.32, { duration: 0 });
		clawT = -1;
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });

		// the seams carve while the claw is still dragging down the card
		const swipeMs = fxDur(CLAW_MS) * CLAW_IMPACT;
		cutSweep.set(1, { duration: swipeMs * 0.85, easing: cubicIn });
		// the tear runs the length of the rake: cue it as the first gouge opens,
		// not on the clench, so the nails are audibly dragging the whole way down
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_claw_split' });

		let settle: Promise<unknown> = Promise.resolve();
		await playClaw(() => {
			// nails through: everything that makes the card come apart fires here
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_combine_a' });
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
			seamFlare.set(1, { duration: fxDur(20) });
			seamFlare.set(0, { duration: fxDur(160) });
			shakeBoard({
				intensity: Math.min(10 + cells.filter((c) => c.fresh).length * 2.5, 18),
				duration: fxDur(240),
			});
			const fx = detonation.set(1, { duration: fxDur(320), easing: cubicOut });
			const punch = pulse.set(1, { duration: fxDur(420), easing: backOut });
			const apart = splitProgress.set(1, { duration: fxDur(150), easing: backOut });
			settle = Promise.all([fx, punch, apart]);
		});
		await settle;
	};

	context.eventEmitter.subscribeOnMount({
		splitPanesShow: async ({ cells: incoming }) => {
			const anyFresh = layout(incoming);
			// nothing new to strike (e.g. the split only hit wild columns):
			// leave the surviving panes exactly as they are
			if (!anyFresh || !cells.length) return;
			await runSplit();
			// strike done: the fresh cells settle in with the persisted ones
			cells = cells.map((cell) => (cell.fresh ? { ...cell, fresh: false } : cell));
		},
		// the next spin is under way: the panes ride down and off with the symbols
		// they were cut into, rather than popping when the reveal lands.
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, show && cells.length > 0);
			show = false;
			cells = [];
			fallOut.set(0, { duration: 0 });
		},
		splitPanesHide: () => {
			show = false;
			cells = [];
			fallOut.set(0, { duration: 0 });
		},
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

	const drawUnderGlow = (g: import('pixi.js').Graphics) => {
		g.roundRect(-CARD_W / 2 - 2, -CARD_H / 2 - 2, CARD_W + 4, CARD_H + 4, 10);
		g.fill({ color: DARK, alpha: 0.9 });
	};

	// steel observation frame around the settled split cell
	const drawFrame = (g: import('pixi.js').Graphics, isHigh: boolean) => {
		g.roundRect(-CARD_W / 2 - 3, -CARD_H / 2 - 3, CARD_W + 6, CARD_H + 6, 11);
		g.stroke({ color: isHigh ? 0xc9a34a : GLASS, width: 2, alpha: 0.7 });
	};

	// settled seam between panes: white core with a cold glass glow + faint blood bleed
	const drawDivider = (
		g: import('pixi.js').Graphics,
		cell: SplitCell,
		dividerIndex: number,
		slim: number,
	) => {
		const s = CARD_H;
		const half = s / 2;
		const flicker = 0.9 + 0.1 * Math.sin(time * 14 + cell.seed * 3 + dividerIndex * 1.7);
		const glowW = 5 * slim + 1;
		g.roundRect(-glowW / 2, -half, glowW, s, 3);
		g.fill({ color: BLOOD, alpha: 0.14 * flicker * slim });
		const innerW = 2.4 * slim + 0.5;
		g.roundRect(-innerW / 2, -half, innerW, s, 1);
		g.fill({ color: GLASS, alpha: 0.5 * flicker });
		const coreW = 0.7 * slim + 0.3;
		g.roundRect(-coreW / 2, -half, coreW, s, 0.4);
		g.fill({ color: CORE, alpha: 0.92 * flicker });
	};

	// the blade of light sweeping down a seam while the symbol is still whole
	const drawCutBlade = (
		g: import('pixi.js').Graphics,
		cell: SplitCell,
		dividerIndex: number,
		sweepValue: number,
	) => {
		if (sweepValue <= 0) return;
		const s = CARD_H;
		const half = s / 2;
		const margin = 22;
		const travel = s + margin * 2;
		const headY = -half - margin + Math.min(sweepValue, 1) * travel;
		const trailTop = -half - margin;
		const segments = 8;
		const trailEnd = Math.min(headY, half + margin);
		for (let i = 0; i < segments; i++) {
			const y0 = trailTop + ((trailEnd - trailTop) / segments) * i;
			const y1 = trailTop + ((trailEnd - trailTop) / segments) * (i + 1);
			const heat = (i + 1) / segments;
			g.rect(-3, y0, 6, y1 - y0);
			g.fill({ color: BLOOD, alpha: 0.12 * heat });
			g.rect(-0.9, y0, 1.8, y1 - y0);
			g.fill({ color: CORE, alpha: 0.95 * heat });
		}
		if (sweepValue < 1) {
			g.poly([0, headY + 16, 3.4, headY + 2, 0, headY - 22, -3.4, headY + 2]);
			g.fill({ color: CORE, alpha: 0.98 });
			g.ellipse(0, headY, 16, 2);
			g.fill({ color: CORE, alpha: 0.55 });
			for (let i = 0; i < 4; i++) {
				const sparkSeed = cell.seed * 13 + dividerIndex * 29 + i * 7;
				const life = (time * (3 + rand(sparkSeed) * 2) + rand(sparkSeed + 1)) % 1;
				const angle = -Math.PI / 2 + (rand(sparkSeed + 2) - 0.5) * 2.2;
				const dist = 5 + life * (14 + rand(sparkSeed + 3) * 14);
				const x = Math.cos(angle) * dist;
				const y = headY + Math.sin(angle) * dist * 0.8;
				const tail = 3 + rand(sparkSeed + 4) * 4;
				g.moveTo(x, y);
				g.lineTo(x - Math.cos(angle) * tail, y - Math.sin(angle) * tail * 0.8);
				g.stroke({ color: i % 2 === 0 ? CORE : GLASS, width: 1.2, alpha: 0.85 * (1 - life) });
			}
		}
	};

	const drawSeamFlare = (g: import('pixi.js').Graphics, flare: number) => {
		if (flare <= 0.01) return;
		const s = CARD_H;
		const half = s / 2;
		g.roundRect(-7, -half, 14, s, 7);
		g.fill({ color: BLOOD, alpha: 0.4 * flare });
		g.roundRect(-2.4, -half, 4.8, s, 2.4);
		g.fill({ color: CORE, alpha: 0.98 * flare });
		g.ellipse(0, 0, 30 * flare + 6, 2.5);
		g.fill({ color: CORE, alpha: 0.7 * flare });
	};

	/**
	 * The four gouges the nails cut as the hand is dragged down.
	 *
	 * Each one runs from where the nails first bit to where they are right now,
	 * so the cut grows under the hand as it travels — and because the nails
	 * lead the top of the hand, the finished part of the gouge is always above
	 * the fingers where nothing covers it.
	 */
	const drawGouges = (g: import('pixi.js').Graphics, t: number) => {
		if (t < CLAW_PRESS) return;
		const fade = 1 - cubicIn(span(t, CLAW_RELEASE, 1));
		if (fade <= 0.01) return;

		const half = CARD_H / 2;
		const top = Math.max(clawNailY(CLAW_PRESS), -half);
		const bottom = Math.min(clawNailY(t), half);
		if (bottom <= top) return;

		// white-hot right at the nail, cooling off up the length of the cut
		const heat = 1 - span(t, CLAW_IMPACT, CLAW_RELEASE);

		for (let i = 0; i < 4; i++) {
			const x = -CARD_W * 0.33 + (CARD_W * 0.66 * i) / 3;
			const lean = (i - 1.5) * 2.2;
			const steps = 18;
			const left: [number, number][] = [];
			const right: [number, number][] = [];
			for (let s = 0; s <= steps; s++) {
				const u = s / steps;
				const y = mix(top, bottom, u);
				// widest in the middle of the cut, tapering at both ends
				const taper = Math.sin(Math.PI * u) ** 0.7;
				const width = (1.6 + 1.4 * (1.5 - Math.abs(i - 1.5))) * taper + 0.4;
				const cx = x + lean * u;
				left.push([cx - width, y]);
				right.push([cx + width, y]);
			}
			g.poly([...left, ...right.reverse()].flat());
			g.fill({ color: DARK, alpha: 0.9 * fade });

			// bleed + the cut edge still glowing where the nail just passed
			g.moveTo(x, top);
			g.lineTo(x + lean, bottom);
			g.stroke({ color: BLOOD, width: 4, alpha: 0.17 * fade * heat });
			g.moveTo(x + lean * 0.72, mix(top, bottom, 0.72));
			g.lineTo(x + lean, bottom);
			g.stroke({ color: CORE, width: 1.6, alpha: 0.85 * fade * heat });
		}
	};

	const drawDetonation = (
		g: import('pixi.js').Graphics,
		cell: SplitCell,
		panes: number,
		d: number,
		split: number,
	) => {
		if (d <= 0 || d >= 1) return;
		const fade = 1 - d;
		g.roundRect(-CARD_W / 2 - 5, -CARD_H / 2 - 5, CARD_W + 10, CARD_H + 10, 13);
		g.fill({ color: CORE, alpha: 0.7 * fade * fade });
		const ringRadius = CARD_H * (0.22 + 0.9 * d);
		g.circle(0, 0, ringRadius * 0.92);
		g.stroke({ color: BLOOD, width: 8 * fade + 1, alpha: 0.4 * fade });
		g.circle(0, 0, ringRadius);
		g.stroke({ color: CORE, width: 3 * fade + 0.5, alpha: 0.8 * fade });
		for (let seamIndex = 0; seamIndex < panes - 1; seamIndex++) {
			const seamX = (-CARD_W / 2 + ((seamIndex + 1) / panes) * CARD_W) * split;
			for (let k = 0; k < 5; k++) {
				const sparkSeed = cell.seed * 17 + seamIndex * 71 + k * 13;
				const side = rand(sparkSeed) > 0.5 ? 1 : -1;
				const y0 = (rand(sparkSeed + 1) - 0.5) * CARD_H * 0.8;
				const speed = 35 + rand(sparkSeed + 2) * 55;
				const vx = side * speed;
				const vy = (rand(sparkSeed + 3) - 0.5) * 24 + 70 * d;
				const x = seamX + vx * d;
				const y = y0 + vy * d * 0.5;
				const vlen = Math.sqrt(vx * vx + vy * vy) || 1;
				const tail = (6 + rand(sparkSeed + 4) * 8) * fade;
				g.moveTo(x, y);
				g.lineTo(x - (vx / vlen) * tail, y - (vy / vlen) * tail);
				g.stroke({ color: k % 3 === 0 ? CORE : GLASS, width: 1.4, alpha: 0.85 * fade });
			}
		}
	};

</script>

{#snippet splitCell(cell: DrawnCell)}
	{@const panes = Math.min(cell.count, MAX_PANES)}
	{@const sliceWidth = CARD_W / panes}
	{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	<!-- cells persisted from an earlier event sit fully split and ignore the
		shared strike tweens, or a later split would visibly re-cut them -->
	{@const split = cell.fresh ? splitProgress.current : 1}
	{@const slim = Math.min(1, 3 / panes)}
	{@const gap = CARD_W * Math.min(0.025, 0.09 / panes)}
	{@const paneWidth = Math.max((sliceWidth - gap) * split + CARD_W * (1 - split), 2)}
	<Container x={cell.cx} y={cell.cy} scale={cell.fresh ? pulse.current : 1}>
		<Graphics draw={drawUnderGlow} />
		{#each Array.from({ length: panes }) as _, i (i)}
			{@const paneX = (-CARD_W / 2 + (i + 0.5) * sliceWidth) * split}
			<Container x={paneX}>
				<Rectangle isMask anchor={0.5} width={paneWidth} height={CARD_H} />
				<SymbolSprite {symbolInfo} />
			</Container>
		{/each}
		{#each Array.from({ length: panes - 1 }) as _, i (i)}
			<Container x={(-CARD_W / 2 + (i + 1) * sliceWidth) * split} alpha={split}>
				<Graphics draw={(g) => drawDivider(g, cell, i, slim)} />
			</Container>
		{/each}
		{@const nDividers = panes - 1}
		{#if cell.fresh}
			{#each Array.from({ length: nDividers }) as _, i (i)}
				{@const sweep = Math.min(Math.max(cutSweep.current * (1 + 0.15 * (nDividers - 1)) - 0.15 * i, 0), 1)}
				<Container x={-CARD_W / 2 + (i + 1) * sliceWidth} alpha={1 - split * 0.9}>
					<Graphics draw={(g) => drawCutBlade(g, cell, i, sweep)} />
				</Container>
			{/each}
			{#each Array.from({ length: nDividers }) as _, i (i)}
				<Container x={-CARD_W / 2 + (i + 1) * sliceWidth}>
					<Graphics draw={(g) => drawSeamFlare(g, seamFlare.current)} />
				</Container>
			{/each}
		{/if}
		<Container alpha={split}>
			<Graphics draw={(g) => drawFrame(g, isHigh)} />
		</Container>
		{#if cell.fresh}
			<Container>
				<Graphics draw={(g) => drawDetonation(g, cell, panes, detonation.current, split)} />
			</Container>
			<!-- the claw strike plays ON TOP of the panes: it is in front of the card,
				tearing it, not embedded in it -->
			{@render clawStrike()}
		{/if}
	</Container>
{/snippet}

{#snippet clawHand(t: number, alpha: number, dy: number, tint: number)}
	<ClawHand
		curl={clawCurl(t)}
		x={0}
		y={clawWristY(t) + dy}
		handH={CLAW_HAND_H}
		scale={clawScale(t)}
		roll={clawRoll(t)}
		{alpha}
		{tint}
	/>
{/snippet}

{#snippet clawStrike()}
	{#if clawT >= 0}
		{@const t = clawT}
		{@const alpha = clawAlpha(t)}
		<!-- speed drives the motion trail, so it smears exactly as hard as the
			hand is actually moving instead of on a fixed schedule -->
		{@const speed = Math.abs(clawWristY(Math.min(t + 0.02, 1)) - clawWristY(t)) / 0.02}
		{@const smear = Math.min(speed / (CARD_H * 26), 1)}
		<Graphics draw={(g) => drawGouges(g, t)} />
		<!-- cast shadow on the card: this is what stops the cutout reading as a
			decal printed on the symbol -->
		{@render clawHand(t, alpha * 0.42, CARD_H * 0.035, 0x000000)}
		{#if smear > 0.02}
			{@render clawHand(t, alpha * 0.3 * smear, -CARD_H * 0.1 * smear, CORE)}
			{@render clawHand(t, alpha * 0.16 * smear, -CARD_H * 0.19 * smear, CORE)}
		{/if}
		{@render clawHand(t, alpha, 0, CORE)}
	{/if}
{/snippet}

{#snippet badgeMarker(cell: SplitCell)}
	<!-- EVERY split cell states exactly what it is worth. The panes are only a
		visual (capped at MAX_PANES), so the number is the ground truth — and it
		must be there whether the split is 2x or 11x, or the same feature reads
		differently from cell to cell. -->
	<Container x={cell.cx} y={cell.cy} scale={cell.fresh ? pulse.current : 1}>
		<Text
			anchor={0.5}
			text={`${cell.count}x`}
			style={{
				fontFamily: 'Arial',
				fontWeight: '900',
				fontSize: 34,
				fill: 0xffffff,
				stroke: { color: 0x000000, width: 5 },
			}}
		/>
	</Container>
{/snippet}

<!-- MainContainer stays MOUNTED even while hidden: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). -->
<MainContainer>
	{#if show}
		<Container x={stateShake.x} y={stateShake.y + fallOut.current}>
			{#each drawn as cell (cell.key)}
				{@render splitCell(cell)}
			{/each}
			{#each drawn as cell (cell.key)}
				{@render badgeMarker(cell)}
			{/each}
		</Container>
	{/if}
</MainContainer>
