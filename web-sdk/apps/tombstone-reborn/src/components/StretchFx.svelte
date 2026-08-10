<script lang="ts" module>
	// STRETCH FX: a random full-reel WILD portrait DROPS into the reel (over the
	// vanishing board symbols), THEN stretches vertically. The stretch is a
	// NON-LINEAR pull: the centre ~20% stays flat/natural, then the curve gets
	// steep toward the top AND bottom edges (built from stacked texture slices).
	// A wide, gentle 3D BULGE covers the whole column and fades toward the top/
	// bottom corners. A "N WAYS" plaque sits centred in the reel and COUNTS UP as
	// it stretches; the bigger the final ways, the LONGER the stretch takes.
	export type EmitterEventStretchFx =
		| { type: 'stretchFxShow'; reels: { reel: number; ways: number; baseRows: number }[] }
		| { type: 'stretchFxHide' };
</script>

<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { BulgePinchFilter } from 'pixi-filters';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, BaseSprite, Rectangle, Graphics, getContextApp } from 'pixi-svelte';

	import { stateBet } from 'state-shared';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { fxDur } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, CELL_PITCH_X, MAX_ROWS, pickWildReelArt, type WildReelArt } from '../game/constants';
	import { getSymbolX } from '../game/utils';
	import { stateShake } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX, drawPowderSeam } from '../game/tombstoneVfx';
	import WildColumnLabel from './WildColumnLabel.svelte';
	import ColumnClawStrike, { playColumnClaw } from './ColumnClawStrike.svelte';

	const context = getContext();
	const appContext = getContextApp();

	/** same visual pane cap as WildReelSlide — don't import that module (cycle risk) */
	const WILD_SPLIT_MAX_PANES = 4;

	// stretch curve: flat for the central FLAT fraction of the half-height, then a
	// steep power curve out to the edges (higher STEEP = sharper knee after 20%).
	const SLICES = 26;
	const FLAT = 0.2;
	const STEEP = 2.4;

	type Slice = { tex: PIXI.Texture; c0: number; c1: number };
	type FxReel = {
		reel: number;
		ways: number;
		baseWays: number;
		cx: number;
		cy: number;
		baseH: number;
		// ASYMMETRIC stretch bounds: the column pulls far past the board TOP for
		// drama, but the BOTTOM clamps just past the board edge so it never covers
		// the bottom special cells or the WAYS/WIN rail below them.
		topHalf: number;
		bottomHalf: number;
		targetH: number;
		art: WildReelArt;
		slices: Slice[];
		bulge: BulgePinchFilter;
		// stretch events fire ONE PER CELL (activation order): a reel from an
		// EARLIER event stays fully stretched (settled) while the new one animates.
		settled: boolean;
		/** powder-burn pane count after a SPLIT tears the column (1 = intact) */
		panes: number;
		/** 0 = whole column, 1 = fully torn into panes */
		tear: Tween<number>;
	};

	let reels = $state<FxReel[]>([]);
	let phase = $state<'idle' | 'drop' | 'stretch'>('idle');

	const dropT = new Tween(0);
	const stretchT = new Tween(0);
	const waysT = new Tween(0);
	const badge = new Tween(0);
	// rides the column off the bottom edge when the next spin starts
	const fallOut = new Tween(0);

	// non-linear vertical map: source centre coord c∈[-1,1] → display offset (px).
	// centre band (|c|<FLAT) keeps its natural size; beyond it the outer bands are
	// pushed steeply toward the edges as the stretch progresses (p).
	const push = (a: number) => (a <= FLAT ? 0 : Math.pow((a - FLAT) / (1 - FLAT), STEEP));
	const dispY = (c: number, baseHalf: number, targetHalf: number, p: number) =>
		c * baseHalf + Math.sign(c) * push(Math.abs(c)) * (targetHalf - baseHalf) * p;

	const destroyReels = () => {
		for (const cell of reels) for (const s of cell.slices) s.tex?.destroy(false);
	};

	const buildSlices = (art: WildReelArt): Slice[] => {
		const base = appContext.stateApp.loadedAssets?.[art.key] as PIXI.Texture | undefined;
		if (!base) return [];
		const f = base.frame;
		const out: Slice[] = [];
		for (let i = 0; i < SLICES; i++) {
			const v0 = i / SLICES;
			const v1 = (i + 1) / SLICES;
			const tex = new PIXI.Texture({
				source: base.source,
				frame: new PIXI.Rectangle(f.x, f.y + f.height * v0, f.width, f.height * (v1 - v0)),
			});
			out.push({ tex, c0: (v0 - 0.5) * 2, c1: (v1 - 0.5) * 2 });
		}
		return out;
	};

	const layout = (incoming: { reel: number; ways: number; baseRows: number }[]): FxReel[] => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		const cy = originY + MAX_ROWS * 0.5 * SYMBOL_SIZE;
		const boardHalf = MAX_ROWS * 0.5 * SYMBOL_SIZE;
		// The pull overflows the TOP — but only as far as the view allows: on
		// desktop the board sits near the canvas top, and a fixed 1.6-cell
		// overflow pushed the column (and the symbols on it) out of sight.
		// A bit of stretch, capped to the headroom that actually exists above
		// the board in this layout. The BOTTOM stops just past the board edge —
		// never into the special cells / HUD rail underneath.
		const headroom = Math.max(0, originY - SYMBOL_SIZE * 0.08);
		const topHalf = boardHalf + Math.min(0.9 * SYMBOL_SIZE, headroom);
		const bottomHalf = boardHalf + 0.15 * SYMBOL_SIZE;
		return incoming.map(({ reel, ways, baseRows }) => {
			const art = pickWildReelArt();
			return {
				reel,
				ways,
				baseWays: Math.max(baseRows, 1),
				cx: originX + getSymbolX(reel),
				cy,
				// rest height = the reel window; targets are fixed overflows
				// (constant — never scale with `ways`).
				baseH: Math.max(baseRows, 1) * SYMBOL_SIZE,
				topHalf,
				bottomHalf,
				targetH: topHalf + bottomHalf,
				art,
				slices: buildSlices(art),
				// wide, gentle 3D lens: big radius so it spreads over the whole column
				// and fades toward the top/bottom corners; low strength so the centre
				// isn't over-magnified. Driven steadily (no breathing) in the $effect.
				bulge: new BulgePinchFilter({ center: { x: 0.5, y: 0.5 }, radius: SYMBOL_SIZE, strength: 0 }),
				settled: false,
				panes: 1,
				tear: new Tween(0),
			};
		});
	};

	const drawWildDivider = (g: import('pixi.js').Graphics, h: number, slim: number) => {
		drawPowderSeam(g, h, slim);
	};

	context.eventEmitter.subscribeOnMount({
		stretchFxShow: async ({ reels: incoming }) => {
			if (!incoming.length) return;
			// stretch events fire one per cell: freeze any earlier stretched columns
			// at rest (settled) and animate ONLY the new batch.
			const existing = new Set(reels.map((r) => r.reel));
			const added = layout(incoming.filter((r) => !existing.has(r.reel)));
			if (!added.length) return;
			reels = [...reels.map((r) => ({ ...r, settled: true })), ...added];
			dropT.set(0, { duration: 0 });
			stretchT.set(0, { duration: 0 });
			waysT.set(0, { duration: 0 });
			// speed tiers: slow pull on normal (fxDur = /1), a bit faster on
			// turbo (/1.35), INSTANT on super turbo — the column just snaps in
			// fully stretched with its final ways.
			const instant = stateBet.isSuperTurbo;
			const tier = (ms: number) => (instant ? 0 : fxDur(ms));
			badge.set(1, { duration: tier(260), easing: backOut });
			// 1) the wild column drops in over the vanishing symbols
			phase = 'drop';
			await dropT.set(1, { duration: tier(520), easing: backOut });
			// 2) then it stretches — bigger final ways ⇒ LONGER pull.
			phase = 'stretch';
			const maxWays = Math.max(...added.map((r) => r.ways));
			const dur = tier(Math.min(3200, Math.max(750, 700 + maxWays * 4.4)));
			waysT.set(1, { duration: dur, easing: cubicOut });
			await stretchT.set(1, { duration: dur, easing: backOut });
		},
		// a split tore through a settled wild-stretch column: rake it with the
		// split claw, snap it into Madam-Mirror panes, and punch the new total
		wildReelWaysUpdate: async (e) => {
			const mine = new Set(reels.map((r) => r.reel));
			const incoming = e.reels.filter(({ reel }) => mine.has(reel));
			if (!incoming.length) return;
			tearing = incoming.map(({ reel }) => reel);
			let punch: Promise<unknown> = Promise.resolve();
			await playColumnClaw(
				(t) => (clawT = t),
				() => {
					const byReel = new Map(incoming.map((r) => [r.reel, r]));
					const touched = reels.filter((r) => byReel.has(r.reel));
					reels = reels.map((r) => {
						const next = byReel.get(r.reel);
						if (!next) return r;
						return {
							...r,
							ways: next.ways,
							settled: true,
							panes: Math.min(Math.max(next.split ?? r.panes, 2), WILD_SPLIT_MAX_PANES),
						};
					});
					punch = (async () => {
						await Promise.all([
							...touched.map((r) => r.tear.set(1, { duration: fxDur(160), easing: backOut })),
							badge.set(0.45, { duration: fxDur(110) }),
						]);
						await badge.set(1, { duration: fxDur(260), easing: backOut });
					})();
				},
			);
			tearing = [];
			await punch;
		},
		// a cage wild landed on this standing wild-stretch column: it doubles the
		// column's worth in place. Same slam as the plain wild column gets — no
		// claw, no panes, the rack stays exactly as it is.
		wildReelDouble: async (e) => {
			const byReel = new Map(e.reels.map((r) => [r.reel, r]));
			if (!reels.some((r) => byReel.has(r.reel))) return;
			await badge.set(0.35, { duration: fxDur(120) });
			reels = reels.map((r) =>
				byReel.has(r.reel) ? { ...r, ways: byReel.get(r.reel)!.ways, settled: true } : r,
			);
			await badge.set(1, { duration: fxDur(300), easing: backOut });
		},
		// the next spin is under way: the stretched wild column rides down and
		// off with the symbols rather than popping when the reveal lands.
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, reels.length > 0);
			destroyReels();
			reels = [];
			phase = 'idle';
			dropT.set(0, { duration: 0 });
			stretchT.set(0, { duration: 0 });
			waysT.set(0, { duration: 0 });
			badge.set(0, { duration: 0 });
			fallOut.set(0, { duration: 0 });
		},
		stretchFxHide: () => {
			destroyReels();
			reels = [];
			phase = 'idle';
			dropT.set(0, { duration: 0 });
			stretchT.set(0, { duration: 0 });
			waysT.set(0, { duration: 0 });
			badge.set(0, { duration: 0 });
			fallOut.set(0, { duration: 0 });
		},
	});

	// drive the per-reel bulge lens from the stretch progress (steady — no pulse);
	// settled reels hold their final lens.
	$effect(() => {
		const p = Math.min(1, stretchT.current);
		for (const cell of reels) {
			if (!cell.bulge) continue;
			const pc = cell.settled ? 1 : p;
			cell.bulge.strength = cell.settled || phase === 'stretch' ? 0.3 * pc : 0;
			cell.bulge.radius = (cell.baseH + (cell.targetH - cell.baseH) * pc) * 0.62;
		}
	});

	const drawGrip = (
		g: import('pixi.js').Graphics,
		w: number,
		topY: number,
		bottomY: number,
		a: number,
	) => {
		if (a <= 0.02) return;
		for (const y of [topY, bottomY]) {
			g.rect(-w / 2 - 3, y - 1.5, w + 6, 3);
			g.fill({ color: TOMBSTONE_FX.spentBrass, alpha: 0.8 * a });
			g.rect(-w / 2 - 5, y - 4, w + 10, 8);
			g.fill({ color: TOMBSTONE_FX.bloodRust, alpha: 0.28 * a });
		}
	};

	// When a SPLIT tears through a settled wild-stretch column, the split's claw
	// rakes the whole column and the new worth punches in on the clench.
	let clawT = $state(-1);
	let tearing = $state<number[]>([]);
</script>

<!-- MainContainer stays MOUNTED even while empty: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). -->
<MainContainer>
	{#if reels.length}
		<Container x={stateShake.x} y={stateShake.y + fallOut.current}>
			{#each reels as cell (cell.reel)}
				{@const p = cell.settled ? 1 : stretchT.current}
				{@const baseHalf = cell.baseH / 2}
				{@const topY = dispY(-1, baseHalf, cell.topHalf, p)}
				{@const bottomY = dispY(1, baseHalf, cell.bottomHalf, p)}
				{@const flare = cell.settled ? 0 : Math.sin(Math.min(1, p) * Math.PI)}
				{#if !cell.settled && phase === 'drop'}
					<Container x={cell.cx} y={cell.cy}>
						<Rectangle
							isMask
							anchor={0.5}
							width={CELL_PITCH_X}
							height={cell.baseH}
							backgroundColor={0xffffff}
						/>
						<Sprite
							key={cell.art.key}
							x={0}
							y={-cell.baseH * (1 - dropT.current)}
							anchor={0.5}
							width={CELL_PITCH_X}
							height={cell.baseH}
						/>
					</Container>
				{:else}
					{@const panes = Math.max(cell.panes, 1)}
					{@const tear = cell.tear.current}
					{@const colH = bottomY - topY}
					{@const sliceW = CELL_PITCH_X / panes}
					{@const gap = CELL_PITCH_X * Math.min(0.025, 0.09 / panes)}
					{@const slim = Math.min(1, 3 / panes)}
					{@const paneW = Math.max((sliceW - gap) * tear + CELL_PITCH_X * (1 - tear), 2)}
					<Container x={cell.cx} y={cell.cy}>
						<Rectangle
							isMask
							anchor={{ x: 0.5, y: 0 }}
							y={topY}
							width={CELL_PITCH_X + 6}
							height={colH}
							backgroundColor={0xffffff}
						/>
						{#if panes <= 1 || tear < 0.001}
							<!-- bulge lens wraps the sliced column so the grip bars stay crisp -->
							<Container filters={[cell.bulge]}>
								{#each cell.slices as s (s.c0)}
									{@const y0 = dispY(s.c0, baseHalf, s.c0 < 0 ? cell.topHalf : cell.bottomHalf, p)}
									{@const y1 = dispY(s.c1, baseHalf, s.c1 < 0 ? cell.topHalf : cell.bottomHalf, p)}
									<BaseSprite
										texture={s.tex}
										x={0}
										y={(y0 + y1) / 2}
										anchor={0.5}
										width={CELL_PITCH_X}
										height={y1 - y0}
									/>
								{/each}
							</Container>
						{:else}
							<!-- SPLIT tore the wild stretch into powder-burn panes -->
							{#each Array.from({ length: panes }) as _, i (i)}
								{@const paneX = (-CELL_PITCH_X / 2 + (i + 0.5) * sliceW) * tear}
								<Container x={paneX}>
									<Rectangle
										isMask
										anchor={{ x: 0.5, y: 0 }}
										y={topY}
										width={paneW}
										height={colH}
									/>
									<Container x={-paneX} filters={[cell.bulge]}>
										{#each cell.slices as s (s.c0)}
											{@const y0 = dispY(s.c0, baseHalf, s.c0 < 0 ? cell.topHalf : cell.bottomHalf, p)}
											{@const y1 = dispY(s.c1, baseHalf, s.c1 < 0 ? cell.topHalf : cell.bottomHalf, p)}
											<BaseSprite
												texture={s.tex}
												x={0}
												y={(y0 + y1) / 2}
												anchor={0.5}
												width={CELL_PITCH_X}
												height={y1 - y0}
											/>
										{/each}
									</Container>
								</Container>
							{/each}
							{#each Array.from({ length: panes - 1 }) as _, i (i)}
								<Container
									x={(-CELL_PITCH_X / 2 + (i + 1) * sliceW) * tear}
									y={(topY + bottomY) / 2}
									alpha={tear}
								>
									<Graphics draw={(g) => drawWildDivider(g, colH, slim)} />
								</Container>
							{/each}
						{/if}
						<Graphics draw={(g) => drawGrip(g, CELL_PITCH_X, topY, bottomY, flare)} />
					</Container>
				{/if}
			{/each}
		</Container>

		<!-- Same WILD plate the Wild Reel uses, counting up as the column
			stretches. This IS a wild column, so it has to say so in the same
			words and the same place as the other feature that makes one.

			In its OWN layer, mounted after the columns' container: the column
			above switches subtrees when the drop phase becomes the stretch
			phase, and a remounted pixi-svelte child is appended to the END of
			its parent — as a sibling it would land on top of this label and
			hide the ways (which is exactly what used to happen). -->
		<Container x={stateShake.x} y={stateShake.y + fallOut.current}>
			{#each reels as cell (cell.reel)}
				{@const shown = cell.settled
					? cell.ways
					: Math.round(cell.baseWays + (cell.ways - cell.baseWays) * waysT.current)}
				{@const pop = cell.settled ? 1 : 1 + 0.12 * Math.sin(Math.min(1, waysT.current) * Math.PI)}
				<WildColumnLabel
					x={cell.cx}
					y={cell.cy}
					ways={shown}
					progress={badge.current}
					{pop}
				/>
			{/each}
		</Container>

		<!-- the split's claw raking a torn column, over everything it cuts. The
			settled column spans -topHalf..+bottomHalf around cy, so the strike
			box is recentred on that. -->
		{#if clawT >= 0}
			<Container x={stateShake.x} y={stateShake.y + fallOut.current}>
				{#each reels.filter((r) => tearing.includes(r.reel)) as cell (cell.reel)}
					<Container x={cell.cx} y={cell.cy + (cell.bottomHalf - cell.topHalf) / 2}>
						<ColumnClawStrike h={cell.topHalf + cell.bottomHalf} t={clawT} />
					</Container>
				{/each}
			</Container>
		{/if}
	{/if}
</MainContainer>
