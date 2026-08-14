<script lang="ts" module>
	export type EmitterEventWildReel =
		| {
				type: 'wildReelSlideShow';
				// `ways` is what the WHOLE column is worth, not a per-cell multiplier.
				// Growing the reel to its full four rows is already worth 4, so this
				// never reads below 4 — it is the number the column shows the player.
				reels: { reel: number; ways: number }[];
		  }
		// a SPLIT tore through a standing wild column: raise what it is worth AND
		// visually slice the column into panes (same powder-burn treatment the
		// paying symbols get). `split` is the resulting per-cell ways count that
		// drives the pane geometry (capped visually at MAX_PANES).
		| {
				type: 'wildReelWaysUpdate';
				reels: { reel: number; ways: number; split?: number }[];
		  }
		// a cage WILD landed on a column that was already standing: it cannot
		// rise the reel twice, so the column's worth doubles in place. No claw
		// and no panes — this is not a split — just a slam and a new number.
		| {
				type: 'wildReelDouble';
				reels: { reel: number; ways: number }[];
		  }
		| { type: 'wildReelSlideHide' };

	/** visual pane cap — past this the slices get too thin; the ways badge carries the real number */
	export const WILD_SPLIT_MAX_PANES = 4;
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import type { Texture, VideoSource } from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { Container, Sprite, Rectangle, Graphics } from 'pixi-svelte';

	import { fxDur } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, CELL_PITCH_X, MAX_ROWS, pickWildReelArt, type WildReelArt } from '../game/constants';
	import { getSymbolX, getReelWindow } from '../game/utils';
	import WildColumnLabel from './WildColumnLabel.svelte';
	import ColumnClawStrike, { playColumnClaw } from './ColumnClawStrike.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	// One wild-reel column (H3) is an mp4 WITH audio. Pixi loads it as a video
	// texture; we grab the underlying <video> element to drive playback and sound
	// ourselves. The still columns have no video, so videoOf() returns undefined.
	const videoOf = (key?: string): HTMLVideoElement | undefined => {
		if (!key) return undefined;
		const tex = context.stateApp.loadedAssets?.[key] as Texture | undefined;
		return (tex?.source as VideoSource | undefined)?.resource as HTMLVideoElement | undefined;
	};
	/** the asset key to actually draw: the video if it loaded, else the still poster */
	const drawKeyFor = (art: WildReelArt) => (art.video && videoOf(art.video) ? art.video : art.key);
	/** audio must play only ONCE per feature, even if the column re-stands */
	let videoAudioUsed = $state(false);
	const resetVideo = () => {
		videoAudioUsed = false;
		for (const r of reels) {
			const v = videoOf(r.art.video);
			if (!v) continue;
			try {
				v.pause();
				v.currentTime = 0;
			} catch {
				/* seek can throw before metadata */
			}
			v.muted = true;
		}
	};

	// each triggered reel remembers WHICH random premium wild portrait it drew, so
	// the art stays fixed for the whole slide (no per-frame flicker). Wild reels
	// now fire ONE PER CELL (activation order), so each entry keeps its OWN slide
	// tween — a later wild reel slides in while the earlier columns stay at rest.
	// `panes` / `tear` drive the Madam-Mirror split that a later SPLIT paints on.
	// rides the columns off the bottom edge when the next spin starts
	const fallOut = new Tween(0);

	let reels = $state<
		{
			reel: number;
			art: WildReelArt;
			slide: Tween<number>;
			ways: number;
			badge: Tween<number>;
			panes: number;
			tear: Tween<number>;
		}[]
	>([]);

	// One column overlay per triggered reel. A risen reel is ALWAYS grown (or
	// converted) to the full target height — the math appends wild cells until
	// the column stands MAX_ROWS tall — so the art spans AT LEAST the full
	// board window on every reel, not the reel's shorter base window. Sizing it
	// to the base rows made the middle reel (2 base rows) show a half-height
	// "wild reel" wearing a full-column ways badge.
	//
	// The height is the UNION of the board window and the reel's LIVE window
	// (getReelWindow): a reel a STRETCH racked past the board top keeps its
	// override for the takeover slide (StretchWays tweens it back to MAX_ROWS),
	// and the column must cover that extra height the whole way down — sizing
	// to MAX_ROWS alone left the racked top sticking out above the wild art.
	const columns = $derived.by(() => {
		if (!reels.length)
			return [] as {
				reel: number;
				art: WildReelArt;
				slide: Tween<number>;
				badge: Tween<number>;
				ways: number;
				panes: number;
				tear: Tween<number>;
				cx: number;
				cy: number;
				w: number;
				h: number;
				artW: number;
				artH: number;
			}[];
		const w = CELL_PITCH_X;
		return reels.map(({ reel, art, slide, badge, ways, panes, tear }) => {
			const window = getReelWindow(reel);
			const top = Math.min(window.top, 0);
			const bottom = Math.max(window.bottom, MAX_ROWS * SYMBOL_SIZE);
			const h = bottom - top;
			const cy = (top + bottom) * 0.5;
			// cover-fit the portrait art into the reel column (crop overflow, never letterbox)
			const scale = Math.max(w / art.width, h / art.height);
			return {
				reel,
				art,
				slide,
				badge,
				ways,
				panes,
				tear,
				cx: getSymbolX(reel),
				cy,
				w,
				h,
				artW: art.width * scale,
				artH: art.height * scale,
			};
		});
	});

	// ----------------------------------------------------------------- the tear
	// When a SPLIT tears through a standing wild column, the split's claw rakes
	// the column top to bottom, the column snaps into vertical panes, and the
	// new worth punches in on the clench. Only the columns the split actually
	// touched get the strike.
	let clawT = $state(-1);
	let tearing = $state<number[]>([]);

	// ---------------------------------------------------------------- border FX
	// A live containment border around the whole wild column: a dark halo, a
	// white-hot core, and a charge running the perimeter. Same black & white
	// electric language as the special-cell lightning, but held steady around a
	// full reel instead of crackling around one cell, so the column reads as
	// locked-in for the rest of the spin rather than as a momentary event.
	const CORE = 0xf0d78c;
	const GLOW = 0xc9a34a;
	const DEEP = 0x0a0806;
	const GLASS = 0x8a6e4a;
	const BLOOD = 0xb54a2a;

	const BORDER_INSET = 2;
	const PULSE_SPAN = 0.16; // how much of the perimeter the running charge covers

	let time = $state(0);
	onMount(() => {
		let raf = 0;
		const tick = (now: number) => {
			time = now;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	/** rect perimeter sampled at even arc length, so the running charge keeps a
	 * constant speed instead of sprinting along the short edges */
	const perimeter = (hx: number, hy: number) => {
		const corners = [
			[-hx, -hy],
			[hx, -hy],
			[hx, hy],
			[-hx, hy],
		];
		const pts: { x: number; y: number }[] = [];
		for (let i = 0; i < 4; i++) {
			const [ax, ay] = corners[i];
			const [bx, by] = corners[(i + 1) % 4];
			const steps = Math.max(2, Math.round(Math.hypot(bx - ax, by - ay) / 10));
			for (let k = 0; k < steps; k++) {
				const f = k / steps;
				pts.push({ x: ax + (bx - ax) * f, y: ay + (by - ay) * f });
			}
		}
		return pts;
	};

	const strokeLoop = (
		g: import('pixi.js').Graphics,
		pts: { x: number; y: number }[],
		color: number,
		width: number,
		alpha: number,
	) => {
		if (alpha <= 0.01) return;
		g.moveTo(pts[0].x, pts[0].y);
		for (let i = 1; i < pts.length; i++) g.lineTo(pts[i].x, pts[i].y);
		g.lineTo(pts[0].x, pts[0].y);
		g.stroke({ color, width, alpha, cap: 'round', join: 'round' });
	};

	const drawBorder = (
		g: import('pixi.js').Graphics,
		w: number,
		h: number,
		progress: number,
		now: number,
	) => {
		if (progress <= 0.01) return;
		const hx = w / 2 - BORDER_INSET;
		const hy = h / 2 - BORDER_INSET;
		const pts = perimeter(hx, hy);
		const t = now / 1000;
		// slow breath so a standing column keeps living without flickering
		const b = progress * (0.82 + 0.18 * Math.sin(t * 2.2));

		strokeLoop(g, pts, DEEP, 13, 0.34 * b);
		strokeLoop(g, pts, GLOW, 5.5, 0.42 * b);
		strokeLoop(g, pts, CORE, 2.2, 0.9 * b);

		// the charge running the perimeter, brightest at its head
		const span = Math.max(2, Math.round(pts.length * PULSE_SPAN));
		const head = Math.floor(((t * 0.34) % 1) * pts.length);
		for (let i = span; i > 0; i--) {
			const a = ((span - i) / span) ** 2;
			const p0 = pts[(head - i + pts.length) % pts.length];
			const p1 = pts[(head - i + 1 + pts.length) % pts.length];
			g.moveTo(p0.x, p0.y);
			g.lineTo(p1.x, p1.y);
			g.stroke({ color: CORE, width: 2.2 + 4.4 * a, alpha: 0.9 * a * b, cap: 'round' });
		}
		const hp = pts[head % pts.length];
		g.circle(hp.x, hp.y, 8);
		g.fill({ color: GLOW, alpha: 0.45 * b });
		g.circle(hp.x, hp.y, 3.4);
		g.fill({ color: CORE, alpha: 0.95 * b });

		// corner brackets: the column is clamped, not merely outlined
		const arm = Math.min(hx, hy) * 0.42;
		for (const [sx, sy] of [
			[-1, -1],
			[1, -1],
			[1, 1],
			[-1, 1],
		]) {
			g.moveTo(sx * hx, sy * hy - sy * arm);
			g.lineTo(sx * hx, sy * hy);
			g.lineTo(sx * hx - sx * arm, sy * hy);
			g.stroke({ color: CORE, width: 4.5, alpha: 0.95 * b, cap: 'round', join: 'round' });
		}
	};

	const applySplit = (incoming: { reel: number; ways: number; split?: number }[]) => {
		const byReel = new Map(incoming.map((r) => [r.reel, r]));
		reels = reels.map((r) => {
			const next = byReel.get(r.reel);
			if (!next) return r;
			const panes = Math.min(
				Math.max(next.split ?? r.panes, 2),
				WILD_SPLIT_MAX_PANES,
			);
			return { ...r, ways: next.ways, panes };
		});
		return reels.filter((r) => byReel.has(r.reel));
	};

	context.eventEmitter.subscribeOnMount({
		// a bottom-slot WILD turned this middle reel into a Wild Reel: the wild
		// column drops in from the top of the reel window with a weighty nudge.
		// ACCUMULATES: earlier wild columns stay at rest while the new one slides.
		wildReelSlideShow: async (e) => {
			const existing = new Set(reels.map((r) => r.reel));
			const added = e.reels
				.filter(({ reel }) => !existing.has(reel))
				.map(({ reel, ways }) => ({
					reel,
					art: pickWildReelArt(),
					slide: new Tween(0),
					badge: new Tween(0),
					ways,
					panes: 1,
					tear: new Tween(0),
				}));
			if (!added.length) return;
			reels = [...reels, ...added];
			await Promise.all(added.map((r) => r.slide.set(1, { duration: fxDur(560), easing: backOut })));
			// the WILD plate lands AFTER the column does, so it reads as being
			// punched onto the wild rather than riding down with it
			await Promise.all(added.map((r) => r.badge.set(1, { duration: fxDur(260), easing: backOut })));
		},
		// a split tore through the standing column: the split claw rakes it top
		// to bottom, the column snaps into Madam-Mirror panes on the clench, and
		// the new worth punches in. The panes PERSIST until the next reveal.
		wildReelWaysUpdate: async (e) => {
			const mine = new Set(reels.map((r) => r.reel));
			const incoming = e.reels.filter(({ reel }) => mine.has(reel));
			if (!incoming.length) return;
			tearing = incoming.map(({ reel }) => reel);
			let punch: Promise<unknown> = Promise.resolve();
			await playColumnClaw(
				(t) => (clawT = t),
				() => {
					const touched = applySplit(incoming);
					punch = (async () => {
						await Promise.all([
							...touched.map((r) => r.tear.set(1, { duration: fxDur(160), easing: backOut })),
							...touched.map((r) => r.badge.set(0.45, { duration: fxDur(110) })),
						]);
						await Promise.all(
							touched.map((r) => r.badge.set(1, { duration: fxDur(260), easing: backOut })),
						);
					})();
				},
			);
			tearing = [];
			await punch;
		},
		// the column is already down; a cage wild just doubled what it is worth.
		// The badge dips and slams back with the new number so the change is
		// unmissable, but the column itself stays exactly where it is.
		wildReelDouble: async (e) => {
			const byReel = new Map(e.reels.map((r) => [r.reel, r]));
			const touched = reels.filter((r) => byReel.has(r.reel));
			if (!touched.length) return;
			await Promise.all(touched.map((r) => r.badge.set(0.35, { duration: fxDur(120) })));
			reels = reels.map((r) =>
				byReel.has(r.reel) ? { ...r, ways: byReel.get(r.reel)!.ways } : r,
			);
			await Promise.all(
				touched.map((r) => r.badge.set(1, { duration: fxDur(300), easing: backOut })),
			);
		},
		// the next spin is under way: ride the columns down and off with the
		// symbols, rather than hanging over a spinning board until the reveal.
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, reels.length > 0);
			resetVideo();
			reels = [];
			fallOut.set(0, { duration: 0 });
		},
		wildReelSlideHide: () => {
			resetVideo();
			reels = [];
			fallOut.set(0, { duration: 0 });
		},
	});

	// Drive the video column: on the FIRST appearance in a feature it plays with
	// sound, then freezes on its last frame (loop off). If a video column stands
	// again later in the same feature it replays SILENTLY — the audio is one-shot.
	$effect(() => {
		const videoReel = reels.find((r) => r.art.video && videoOf(r.art.video));
		if (!videoReel) return;
		const video = videoOf(videoReel.art.video);
		if (!video) return;
		video.loop = false;
		video.playsInline = true;
		if (!videoAudioUsed) {
			video.muted = false;
			videoAudioUsed = true;
			try {
				video.currentTime = 0;
			} catch {
				/* ignore pre-metadata seek */
			}
		} else {
			video.muted = true;
		}
		const onEnded = () => {
			try {
				video.pause();
			} catch {
				/* ignore */
			}
		};
		video.addEventListener('ended', onEnded);
		if (video.paused) video.play().catch(() => {});
		return () => video.removeEventListener('ended', onEnded);
	});
</script>

<!-- MainContainer stays MOUNTED even while empty: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). -->
<MainContainer>
	{#if reels.length}
		<BoardSpace yOffset={fallOut.current}>
		{#each columns as c (c.reel)}
			{@const panes = Math.max(c.panes, 1)}
			{@const tear = c.tear.current}
			{@const sliceW = c.w / panes}
			{@const gap = c.w * Math.min(0.025, 0.09 / panes)}
			{@const paneW = Math.max((sliceW - gap) * tear + c.w * (1 - tear), 2)}
			{@const slideY = -c.h * (1 - c.slide.current)}
			{@const drawKey = drawKeyFor(c.art)}
			<!-- masked to the reel window: the wild column slides DOWN into the reel
				(clipped like a reel drop), landing on top of the board symbols.
				After a SPLIT, the same art is sliced into vertical panes that snap
				apart — identical treatment to a paying symbol, just column-tall. -->
			<Container x={c.cx} y={c.cy}>
				<Rectangle isMask anchor={0.5} width={c.w + 6} height={c.h} backgroundColor={0xffffff} />
				{#if panes <= 1 || tear < 0.001}
					<Sprite
						key={drawKey}
						x={0}
						y={slideY}
						anchor={0.5}
						width={c.artW}
						height={c.artH}
					/>
				{:else}
					{#each Array.from({ length: panes }) as _, i (i)}
						{@const paneX = (-c.w / 2 + (i + 0.5) * sliceW) * tear}
						{@const artX = -paneX}
						<Container x={paneX} y={slideY}>
							<Rectangle isMask anchor={0.5} width={paneW} height={c.h} />
							<Sprite
								key={drawKey}
								x={artX}
								anchor={0.5}
								width={c.artW}
								height={c.artH}
							/>
						</Container>
					{/each}
					<!-- no strip down the tear: the panes part over the dark reel,
						matching the paying-symbol split -->
				{/if}
			</Container>
		{/each}

		<!-- border + label, drawn OUTSIDE the column mask so neither is clipped,
			and after every column so they always sit on top -->
		{#each columns as c (c.reel)}
			{@const now = time}
			<Container x={c.cx} y={c.cy}>
				<Graphics draw={(g) => drawBorder(g, c.w, c.h, c.slide.current, now)} />
			</Container>
		{/each}

		{#each columns as c (c.reel)}
			<!-- WILD always reads, with what the column is worth stamped under it.
				Shared with the wild-mode Stretch so the two never diverge. -->
			<WildColumnLabel x={c.cx} y={c.cy} ways={c.ways} progress={c.badge.current} />
		{/each}

		<!-- the split's claw raking a torn column, over everything it cuts -->
		{#if clawT >= 0}
			{#each columns.filter((c) => tearing.includes(c.reel)) as c (c.reel)}
				<Container x={c.cx} y={c.cy}>
					<ColumnClawStrike h={c.h} t={clawT} />
				</Container>
			{/each}
		{/if}
		</BoardSpace>
	{/if}
</MainContainer>
