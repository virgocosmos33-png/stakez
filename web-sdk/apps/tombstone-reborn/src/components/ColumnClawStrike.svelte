<script lang="ts" module>
	/**
	 * The split claw, worked over a FULL wild column.
	 *
	 * When a SPLIT tears through a wild reel there is no card to slice into
	 * panes — the whole column is one wild — so instead the same patient's hand
	 * the split uses on symbols rakes the entire column, top edge to bottom
	 * edge, nails cutting four gouges the whole way down. The strike plays only
	 * after the column has settled; it is the split's animation, not the
	 * column's.
	 *
	 * Purely presentational: the parent owns WHEN it plays by driving `t` with
	 * `playColumnClaw`, which reports the clench so the parent can punch the
	 * new number in on exactly that frame.
	 */
	import { CELL_PITCH_X } from '../game/constants';
	import { eventEmitter } from '../game/eventEmitter';
	import { fxDur } from '../game/fxTiming';

	const HAND_H = CELL_PITCH_X * 1.5;

	// phase boundaries in normalised progress (same feel as SplitPanes' strike)
	const PRESS = 0.16; // hand has faded in and taken hold at the top
	const IMPACT = 0.62; // clench — the number punches in here
	const RELEASE = 0.8; // grip held until here, then dragged away

	const CLAW_MS = 860;

	const span = (t: number, from: number, to: number) =>
		Math.min(Math.max((t - from) / (to - from), 0), 1);

	/**
	 * run one strike, calling `onImpact` on the clench.
	 *
	 * The strike carries the SAME audio beats as SplitPanes' symbol strike, so
	 * a split that only hits wild columns (which SplitPanes skips entirely) is
	 * never silent. The `once` sound player ignores a name that's already
	 * playing, so when both strikes run in the same event the cues don't stack.
	 */
	export const playColumnClaw = (set: (t: number) => void, onImpact?: () => void) =>
		new Promise<void>((resolve) => {
			const start = performance.now();
			let fired = false;
			set(0);
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
			// nails dragging the whole way down the column
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_claw_split' });
			const clawMs = fxDur(CLAW_MS);
			const step = (now: number) => {
				const t = (now - start) / clawMs;
				if (!fired && t >= IMPACT) {
					fired = true;
					// the clench: the column comes apart here
					eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_combine_a' });
					eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
					onImpact?.();
				}
				if (t >= 1) {
					set(-1);
					resolve();
					return;
				}
				set(t);
				requestAnimationFrame(step);
			};
			requestAnimationFrame(step);
		});
</script>

<script lang="ts">
	import { Graphics } from 'pixi-svelte';

	import ClawHand, { clawReach } from './ClawHand.svelte';

	type Props = {
		/** column height; the strike spans all of it */
		h: number;
		/** -1 when idle, else normalised progress from playColumnClaw */
		t: number;
	};

	const props: Props = $props();

	const mix = (from: number, to: number, u: number) => from + (to - from) * u;
	/** the drag accelerates, but gently */
	const fall = (u: number) => u * u;

	const curl = $derived(props.t <= IMPACT ? span(props.t, PRESS * 0.5, IMPACT) : 1);
	const alpha = $derived(
		props.t < PRESS ? 0.96 * span(props.t, 0, PRESS) : 0.96 * (1 - span(props.t, RELEASE, 1)),
	);

	// Same posture as the symbol split: the hand reaches UP the column with the
	// fingers on top (wrist below them), and is dragged down it. Wrist positions
	// are solved so the fingertips run the top edge to the bottom edge of the
	// column, whatever the curl does to the hand's reach.
	const wristY = $derived.by(() => {
		const t = props.t;
		const h = props.h;
		const from = -h / 2 + HAND_H; // tips (reach=1, open) at the top edge
		const to = h / 2 + HAND_H * clawReach(1); // tips (clenched) at the bottom edge
		if (t < PRESS) return from;
		if (t <= IMPACT) return mix(from, to, fall(span(t, PRESS, IMPACT)));
		if (t < RELEASE) return to + props.h * 0.02 * span(t, IMPACT, RELEASE);
		return mix(to + props.h * 0.02, h / 2 + HAND_H * 2, span(t, RELEASE, 1) ** 2);
	});

	const nailY = $derived(wristY - HAND_H * clawReach(curl));

	/** four gouges growing under the nails, the length of the column */
	const drawGouges = (g: import('pixi.js').Graphics) => {
		const t = props.t;
		if (t < PRESS) return;
		const fade = 1 - span(t, RELEASE, 1) ** 2;
		if (fade <= 0.01) return;
		const half = props.h / 2;
		const top = -half;
		const bottom = Math.min(nailY, half);
		if (bottom <= top + 2) return;
		const heat = 1 - span(t, IMPACT, RELEASE);
		const w = CELL_PITCH_X;
		for (let i = 0; i < 4; i++) {
			const x = -w * 0.3 + (w * 0.6 * i) / 3;
			const lean = (i - 1.5) * 3;
			g.moveTo(x, top);
			g.lineTo(x + lean, bottom);
			g.stroke({ color: 0x0a0a0a, width: 3.4, alpha: 0.85 * fade });
			g.moveTo(x, top);
			g.lineTo(x + lean, bottom);
			g.stroke({ color: 0xff2d2d, width: 6, alpha: 0.14 * fade * heat });
			// the cut edge still glowing where the nail just passed
			g.moveTo(x + lean * 0.75, mix(top, bottom, 0.75));
			g.lineTo(x + lean, bottom);
			g.stroke({ color: 0xffffff, width: 1.4, alpha: 0.8 * fade * heat });
		}
	};
</script>

{#if props.t >= 0}
	<Graphics draw={drawGouges} />
	<!-- cast shadow, then the hand: this is what keeps it reading as IN FRONT of
		the column it is raking rather than printed on it -->
	<ClawHand {curl} x={0} y={wristY + props.h * 0.015} handH={HAND_H} alpha={alpha * 0.4} tint={0x000000} />
	<ClawHand {curl} x={0} y={wristY} handH={HAND_H} {alpha} />
{/if}
