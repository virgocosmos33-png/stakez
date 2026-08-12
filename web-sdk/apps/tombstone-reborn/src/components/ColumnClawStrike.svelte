<script lang="ts" module>
	/**
	 * The split strike over a FULL wild column.
	 *
	 * When a SPLIT tears through a wild reel there is no card to slice into
	 * panes — the whole column is one wild — so instead the same bullet-hole
	 * volley used on symbols sprays down the column. The strike plays only
	 * after the column has settled; it is the split's animation, not the
	 * column's.
	 *
	 * Purely presentational: the parent owns WHEN it plays by driving `t` with
	 * `playColumnClaw`, which reports impact so the parent can punch the
	 * new number in on exactly that frame. (Export name kept for callers.)
	 */
	import { eventEmitter } from '../game/eventEmitter';
	import { fxDur } from '../game/fxTiming';
	import { shotsForMultiplier, nextShotGap } from '../game/splitBullets';

	/** Default column multi when the caller does not pass one — mid pack. */
	const DEFAULT_COLUMN_COUNT = 5;
	export const COLUMN_VOLLEYS = shotsForMultiplier(DEFAULT_COLUMN_COUNT);

	/** beat held after the last round before the strike resolves */
	const TAIL_MS = 220;
	const IMPACT_AT = 0.22;

	/**
	 * run one strike, calling `onImpact` after the first volley.
	 *
	 * Uneven per-volley spacing (each rest jittered by nextShotGap, same as
	 * SplitPanes) so the column reads as deliberate magnum fire, not a metronome.
	 * The progress `t` is WARPED to those uneven beats, so the bullet-hole stamps
	 * (driven off the same `t`) stay locked to their bangs. The ricochet is the
	 * STOP beat: it sings off only on the final round. forcePlay so stacked hits
	 * are not swallowed by the once-player.
	 */
	export const playColumnClaw = (set: (t: number) => void, onImpact?: () => void) =>
		new Promise<void>((resolve) => {
			const start = performance.now();
			let fired = false;
			let lastVolley = -1;
			set(0);
			// the column's planks tearing open, same cue as a split seam
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_split_seam_tear' });

			// cumulative fire time of each volley (volley 0 at t=0), then a tail
			const fireTimes = [0];
			for (let v = 1; v < COLUMN_VOLLEYS; v++) {
				fireTimes[v] = fireTimes[v - 1] + fxDur(nextShotGap());
			}
			const total = fireTimes[COLUMN_VOLLEYS - 1] + fxDur(TAIL_MS);
			// map elapsed ms -> 0..1 so volley v boundary (v/COLUMN_VOLLEYS) is
			// crossed exactly at fireTimes[v]; piecewise-linear between beats.
			const warp = (e: number) => {
				if (e >= total) return 1;
				let v = 0;
				while (v < COLUMN_VOLLEYS - 1 && fireTimes[v + 1] <= e) v++;
				const segStart = fireTimes[v];
				const segEnd = v < COLUMN_VOLLEYS - 1 ? fireTimes[v + 1] : total;
				const frac = segEnd > segStart ? (e - segStart) / (segEnd - segStart) : 1;
				return (v + frac) / COLUMN_VOLLEYS;
			};

			const step = (now: number) => {
				const e = now - start;
				const t = warp(e);
				const volley = Math.min(COLUMN_VOLLEYS - 1, Math.floor(t * COLUMN_VOLLEYS));
				if (volley > lastVolley) {
					lastVolley = volley;
					// earlier volleys punch pistol-into-wood; the FINAL volley always
					// RICOCHETS and plays ALONE (its cue carries the crack + the whine
					// off iron), so stacking wood under it never buries the zing. The
					// ricochet is the "it stops here" beat.
					const isFinalVolley = volley === COLUMN_VOLLEYS - 1;
					eventEmitter.broadcast({
						type: 'soundOnce',
						name: isFinalVolley ? 'sfx_bullet_ricochet' : 'sfx_bullet_wood',
						forcePlay: true,
					});
				}
				if (!fired && t >= IMPACT_AT) {
					fired = true;
					// no bullet cue here: the impact frame falls inside a volley that
					// already fired one, and doubling up breaks one hit per volley
					onImpact?.();
				}
				if (e >= total) {
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
	import { onMount } from 'svelte';
	import { Container } from 'pixi-svelte';

	import { CELL_PITCH_X } from '../game/constants';
	import { holePose, type HoleMark } from '../game/splitBullets';
	import BulletHoleMark from './BulletHoleMark.svelte';

	type Props = {
		/** column height; the strike spans all of it */
		h: number;
		/** -1 when idle, else normalised progress from playColumnClaw */
		t: number;
	};

	const props: Props = $props();

	const VOLLEYS = COLUMN_VOLLEYS;

	let marks = $state<HoleMark[]>([]);
	let nowMs = $state(performance.now());
	let lastVolley = $state(-1);

	$effect(() => {
		const t = props.t;
		if (t < 0) {
			marks = [];
			lastVolley = -1;
			return;
		}
		const volley = Math.min(VOLLEYS - 1, Math.floor(t * VOLLEYS));
		if (volley <= lastVolley) return;
		// stamp one new hole per newly reached volley, scattered down the column
		const next: HoleMark[] = [];
		for (let v = lastVolley + 1; v <= volley; v++) {
			const pose = holePose(41 + v * 7, v, CELL_PITCH_X * 0.85, props.h * 0.9);
			next.push({
				id: `col-${v}-${performance.now()}`,
				cellKey: 'column',
				x: pose.x,
				y: pose.y,
				tex: pose.tex,
				scale: pose.scale * 1.15,
				rot: pose.rot,
				born: performance.now(),
			});
		}
		lastVolley = volley;
		marks = [...marks, ...next];
	});

	onMount(() => {
		let raf = 0;
		const tick = (now: number) => {
			nowMs = now;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

{#if props.t >= 0}
	<Container>
		{#each marks as mark (mark.id)}
			<BulletHoleMark
				tex={mark.tex}
				x={mark.x}
				y={mark.y}
				scale={mark.scale}
				rot={mark.rot}
				born={mark.born}
				now={nowMs}
				size={110}
			/>
		{/each}
	</Container>
{/if}
