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
		// visually slice the column into panes (same Madam-Mirror treatment the
		// paying symbols get). `split` is the resulting per-cell ways count that
		// drives the pane geometry (capped visually at MAX_PANES).
		| {
				type: 'wildReelWaysUpdate';
				reels: { reel: number; ways: number; split?: number }[];
		  }
		| { type: 'wildReelSlideHide' };

	/** visual pane cap — past this the slices get too thin; the ways badge carries the real number */
	export const WILD_SPLIT_MAX_PANES = 4;
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Rectangle, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, CELL_PITCH_X, MAX_ROWS, NUM_ROWS, pickWildReelArt, type WildReelArt } from '../game/constants';
	import { getSymbolX } from '../game/utils';
	import WildColumnLabel from './WildColumnLabel.svelte';
	import ColumnClawStrike, { playColumnClaw } from './ColumnClawStrike.svelte';

	const context = getContext();

	// each triggered reel remembers WHICH random premium wild portrait it drew, so
	// the art stays fixed for the whole slide (no per-frame flicker). Wild reels
	// now fire ONE PER CELL (activation order), so each entry keeps its OWN slide
	// tween — a later wild reel slides in while the earlier columns stay at rest.
	// `panes` / `tear` drive the Madam-Mirror split that a later SPLIT paints on.
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

	// One column overlay per triggered middle reel. The art spans EXACTLY that
	// reel's visible rows (diamond board: reels are centred on the board mid-line),
	// so it covers the reel that went wild — not a phantom extra row.
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
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		const w = CELL_PITCH_X;
		// every reel is vertically centred on the board mid-line
		const cy = originY + MAX_ROWS * 0.5 * SYMBOL_SIZE;
		return reels.map(({ reel, art, slide, badge, ways, panes, tear }) => {
			const rows = NUM_ROWS[reel] ?? MAX_ROWS;
			const h = rows * SYMBOL_SIZE;
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
				cx: originX + getSymbolX(reel),
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
	const CORE = 0xffffff;
	const GLOW = 0xf2f2f2;
	const DEEP = 0x0a0a0a;
	const GLASS = 0xdfe6ea;
	const BLOOD = 0xff2d2d;

	/** steel seam between two wild panes — same language as SplitPanes */
	const drawWildDivider = (g: import('pixi.js').Graphics, h: number, slim: number) => {
		const half = (h * 0.5 - 4) * slim;
		g.moveTo(0, -half);
		g.lineTo(0, half);
		g.stroke({ color: BLOOD, width: 5, alpha: 0.55 });
		g.moveTo(0, -half);
		g.lineTo(0, half);
		g.stroke({ color: CORE, width: 1.6, alpha: 0.95 });
		g.moveTo(-1.2, -half);
		g.lineTo(-1.2, half);
		g.stroke({ color: GLASS, width: 0.7, alpha: 0.55 });
	};
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
			await Promise.all(added.map((r) => r.slide.set(1, { duration: 560, easing: backOut })));
			// the WILD plate lands AFTER the column does, so it reads as being
			// punched onto the wild rather than riding down with it
			await Promise.all(added.map((r) => r.badge.set(1, { duration: 260, easing: backOut })));
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
							...touched.map((r) => r.tear.set(1, { duration: 160, easing: backOut })),
							...touched.map((r) => r.badge.set(0.45, { duration: 110 })),
						]);
						await Promise.all(
							touched.map((r) => r.badge.set(1, { duration: 260, easing: backOut })),
						);
					})();
				},
			);
			tearing = [];
			await punch;
		},
		wildReelSlideHide: () => {
			reels = [];
		},
	});
</script>

<!-- MainContainer stays MOUNTED even while empty: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). -->
<MainContainer>
	{#if reels.length}
		{#each columns as c (c.reel)}
			{@const panes = Math.max(c.panes, 1)}
			{@const tear = c.tear.current}
			{@const sliceW = c.w / panes}
			{@const gap = c.w * Math.min(0.025, 0.09 / panes)}
			{@const slim = Math.min(1, 3 / panes)}
			{@const paneW = Math.max((sliceW - gap) * tear + c.w * (1 - tear), 2)}
			{@const slideY = -c.h * (1 - c.slide.current)}
			<!-- masked to the reel window: the wild column slides DOWN into the reel
				(clipped like a reel drop), landing on top of the board symbols.
				After a SPLIT, the same art is sliced into vertical panes that snap
				apart — identical treatment to a paying symbol, just column-tall. -->
			<Container x={c.cx} y={c.cy}>
				<Rectangle isMask anchor={0.5} width={c.w + 6} height={c.h} backgroundColor={0xffffff} />
				{#if panes <= 1 || tear < 0.001}
					<Sprite
						key={c.art.key}
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
								key={c.art.key}
								x={artX}
								anchor={0.5}
								width={c.artW}
								height={c.artH}
							/>
						</Container>
					{/each}
					{#each Array.from({ length: panes - 1 }) as _, i (i)}
						<Container
							x={(-c.w / 2 + (i + 1) * sliceW) * tear}
							y={slideY}
							alpha={tear}
						>
							<Graphics draw={(g) => drawWildDivider(g, c.h, slim)} />
						</Container>
					{/each}
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
	{/if}
</MainContainer>
