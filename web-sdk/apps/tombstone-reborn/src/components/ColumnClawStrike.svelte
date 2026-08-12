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
	import { SHOT_GAP_MS, shotsForMultiplier, shotRicochets } from '../game/splitBullets';

	/** Default column multi when the caller does not pass one — mid pack. */
	const DEFAULT_COLUMN_COUNT = 5;
	export const COLUMN_VOLLEYS = shotsForMultiplier(DEFAULT_COLUMN_COUNT);

	const STRIKE_MS = SHOT_GAP_MS * COLUMN_VOLLEYS + 220;
	const IMPACT_AT = 0.22;

	/**
	 * run one strike, calling `onImpact` after the first volley.
	 *
	 * Audio matches SplitPanes: wood punch AND ricochet whine on every round.
	 * forcePlay so stacked hits are not swallowed by the once-player.
	 */
	export const playColumnClaw = (set: (t: number) => void, onImpact?: () => void) =>
		new Promise<void>((resolve) => {
			const start = performance.now();
			let fired = false;
			let lastVolley = -1;
			set(0);
			// the column's planks tearing open, same cue as a split seam
			eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_split_seam_tear' });
			const strikeMs = fxDur(STRIKE_MS);
			const step = (now: number) => {
				const t = (now - start) / strikeMs;
				const volley = Math.min(COLUMN_VOLLEYS - 1, Math.floor(t * COLUMN_VOLLEYS));
				if (volley > lastVolley) {
					lastVolley = volley;
					// wood punch on every round; ricochet whine only sings off on
					// SOME rounds so the column reads as deliberate magnum fire.
					eventEmitter.broadcast({
						type: 'soundOnce',
						name: 'sfx_bullet_wood',
						forcePlay: true,
					});
					if (shotRicochets()) {
						eventEmitter.broadcast({
							type: 'soundOnce',
							name: 'sfx_bullet_ricochet',
							forcePlay: true,
						});
					}
				}
				if (!fired && t >= IMPACT_AT) {
					fired = true;
					// no bullet cue here: the impact frame falls inside a volley that
					// already fired one, and doubling up breaks one hit per volley
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
