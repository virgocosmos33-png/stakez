<script lang="ts">
	/**
	 * One cell of the special bar, which reels like a board cell.
	 *
	 * The bar is a seventh column of the machine, so a plaque must not sit still
	 * while the reels move. This cell mirrors ITS OWN reel: the moment reel i
	 * starts falling out the plaque drops out through the bottom of its socket,
	 * and it drops back in when that reel falls in — same px/ms fall speed, same
	 * backOut bounce, same turbo response as a board symbol (see SlotSymbol,
	 * which does this for the locked cells).
	 *
	 * Reading the reel's live motion rather than a stagger delay is what keeps
	 * them together: the board's own fall-out stagger, anticipation and slam
	 * stops are all already expressed in that motion, so the column inherits
	 * them instead of re-deriving them and drifting.
	 *
	 * Two things separate this from a board cell. A reel window holds several
	 * symbols, so a spin STREAKS through it — the socket carries a short strip
	 * of blank plaques (parked just outside the mask at rest) so it streaks too
	 * instead of one plaque blinking away. And a plaque is about a third the
	 * height of a symbol, so the board's px/ms would flick it out three times
	 * too fast: the speed is converted to cells, and one plaque crosses its
	 * socket in the time one symbol crosses its row.
	 *
	 * The frame texture is a BORDER with nothing inside it, so each plaque also
	 * lays its own panel into the hollow. That panel is what a label is read
	 * against: without it the rail's grain runs right through the type, and
	 * every cell looks like a sticker with the wood showing through.
	 */
	import { untrack } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import * as PIXI from 'pixi.js';
	import { Container, Graphics, Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { currentSpinOptions } from '../game/fxTiming';

	type Props = {
		/** the board reel this cell belongs to; it reels with it */
		reel: number;
		cx: number;
		cy: number;
		w: number;
		h: number;
		/** the frame's hollow, as fractions of the texture — where the panel goes */
		opening: { x0: number; x1: number; y0: number; y1: number };
		/** asset key: hollow `barPlaque` or a per-kind labeled plaque */
		spriteKey: string;
		/** true when the sprite already carries embossed label + fill */
		bakedLabel: boolean;
		tint: number;
		alpha: number;
		/** how the blank plaques of the strip are painted while they stream past */
		blankTint: number;
		blankAlpha: number;
		/** landing pop for a cell that just took a card (1 = at rest) */
		pop: number;
		/** true while THIS card's effect is resolving on the board — the plaque
		 *  pulses gold so the player can read which feature is firing (they
		 *  resolve top to bottom, in book order) */
		active?: boolean;
	};

	const props: Props = $props();
	const context = getContext();

	/** the seated plaque plus one parked hard against each edge of the socket */
	const STRIP = [-1, 0, 1];
	/** cells of travel per move — how many plaques stream past on a spin */
	const TRAVEL_CELLS = 2;

	// read per transition, never derived: the options must be fixed for the
	// whole of one drop, and a turbo toggle can land in the middle of a spin
	const spinOptions = () => currentSpinOptions();
	/** board px/ms restated in this cell's units, so the rhythm carries over */
	const cellSpeed = (boardSpeed: number) => boardSpeed * (props.h / SYMBOL_SIZE);

	/** 0 = seated, +travel = cleared out through the floor, -travel = overhead */
	const dropY = new Tween(0, { duration: 0 });
	let seated = true;

	// Transitions are queued rather than raced. A reel goes fallingOut ->
	// hanging -> fallingIn in order, but on turbo (or a slam, which jumps
	// straight to stopped) the two arrive almost together — and starting the
	// drop-in on top of a running drop-out would teleport the plaque from
	// mid-fall to overhead. Queued, it always finishes leaving before it lands.
	let chain: Promise<void> = Promise.resolve();
	const queue = (step: () => Promise<void>) => {
		chain = chain.then(step);
	};

	const reelOut = async () => {
		const travel = props.h * TRAVEL_CELLS;
		await dropY.set(travel, { duration: travel / cellSpeed(spinOptions().symbolFallOutSpeed) });
	};

	const reelIn = async () => {
		const travel = props.h * TRAVEL_CELLS;
		const options = spinOptions();
		const bounce = props.h * options.symbolFallInBounceSizeMulti;
		dropY.set(-travel, { duration: 0 });
		await dropY.set(-bounce, {
			duration: (travel - bounce) / cellSpeed(options.symbolFallInSpeed),
		});
		await dropY.set(0, {
			duration: bounce / cellSpeed(options.symbolFallInBounceSpeed),
			easing: backOut,
		});
	};

	$effect(() => {
		const motion = context.stateGame.board[props.reel]?.reelState.motion;
		untrack(() => {
			if (motion === 'fallingOut' && seated) {
				seated = false;
				queue(reelOut);
			} else if ((motion === 'fallingIn' || motion === 'stopped') && !seated) {
				seated = true;
				queue(reelIn);
			}
		});
	});

	// Near-black charcoal fill — matches the reference mockups (solid dark cells,
	// NOT a warm tan wood wash that reads as translucent against the night).
	// Colour-constant, so the gradient texture is built once and remapped into
	// each rect it fills rather than rebuilt per plaque per resize.
	const PANEL_GRADIENT = new PIXI.FillGradient({
		type: 'linear',
		start: { x: 0, y: 0 },
		end: { x: 0, y: 1 },
		colorStops: [
			{ offset: 0, color: 0x141414 },
			{ offset: 0.55, color: 0x0a0a0a },
			{ offset: 1, color: 0x050505 },
		],
		textureSpace: 'local',
	});

	/** fill every hollow plaque of the strip — skipped when the seated sprite
	 *  already bakes its own charcoal panel + embossed label */
	const drawPanels = (graphics: PIXI.Graphics, { w, h, opening, bakedLabel }: Props) => {
		const x = (opening.x0 - 0.5) * w;
		const panelW = (opening.x1 - opening.x0) * w;
		const panelH = (opening.y1 - opening.y0) * h;
		const radius = Math.min(panelW, panelH) * 0.08;

		for (const offset of STRIP) {
			// seated card with a labeled Scenario plaque: its fill is in the art
			if (bakedLabel && offset === 0) continue;
			const y = (opening.y0 - 0.5) * h + offset * h;
			graphics.roundRect(x, y, panelW, panelH, radius).fill(PANEL_GRADIENT);
			graphics
				.roundRect(x, y, panelW, panelH, radius)
				.stroke({ color: 0x000000, width: 1.5, alpha: 1, alignment: 0 });
		}
	};

	// ACTIVE pulse: while this card's feature is firing on the board, a warm
	// gold ring breathes around the plaque and the card sits up a little. The
	// loop reads props.active each cycle, so it winds down on its own.
	const glow = new Tween(0, { duration: 0 });
	let pulsing = false;
	$effect(() => {
		if (!props.active || pulsing) return;
		pulsing = true;
		(async () => {
			while (props.active) {
				await glow.set(1, { duration: 380 });
				await glow.set(0.35, { duration: 380 });
			}
			await glow.set(0, { duration: 180 });
			pulsing = false;
		})();
	});

	const drawGlowRing = (graphics: PIXI.Graphics, w: number, h: number) => {
		const radius = Math.min(w, h) * 0.1;
		graphics
			.roundRect(-w / 2 - 4, -h / 2 - 4, w + 8, h + 8, radius)
			.stroke({ color: 0xf0c96a, width: 5, alpha: 1, alignment: 0.5 });
	};
</script>

<Container x={props.cx} y={props.cy}>
	<!-- clip the travel to this cell, so the plaque reels away into its own
		socket instead of sliding over the plaque below it -->
	<Rectangle
		isMask
		anchor={0.5}
		width={props.w}
		height={props.h}
		backgroundColor={0xffffff}
	/>
	<Container y={dropY.current} scale={props.bakedLabel ? props.pop : 1}>
		<!-- panels under hollow frames; labeled cards carry their own fill -->
		<Graphics eventMode="none" draw={(graphics) => drawPanels(graphics, props)} />
		{#each STRIP as offset (offset)}
			{@const seated = offset === 0}
			<Sprite
				key={seated && props.bakedLabel ? props.spriteKey : 'barPlaque'}
				anchor={0.5}
				y={offset * props.h}
				width={props.w}
				height={props.h}
				tint={seated ? props.tint : props.blankTint}
				alpha={seated ? props.alpha : props.blankAlpha}
				eventMode="none"
			/>
		{/each}
	</Container>
</Container>

<!-- the ACTIVE gold ring lives OUTSIDE the socket mask (it hugs the plaque's
	outside edge, which the travel mask would clip away) -->
{#if glow.current > 0.01}
	<Container x={props.cx} y={props.cy}>
		<Graphics
			eventMode="none"
			alpha={0.85 * glow.current}
			scale={1 + 0.05 * glow.current}
			draw={(graphics) => drawGlowRing(graphics, props.w, props.h)}
		/>
	</Container>
{/if}
