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
	import { Container, Sprite, BaseSprite, Rectangle, Graphics, Text, getContextApp } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, MAX_ROWS, pickWildReelArt, type WildReelArt } from '../game/constants';
	import { stateShake } from '../game/stateShake.svelte';

	const context = getContext();
	const appContext = getContextApp();

	const BLOOD = 0xff2d2d;

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
	};

	let reels = $state<FxReel[]>([]);
	let phase = $state<'idle' | 'drop' | 'stretch'>('idle');
	const dropT = new Tween(0);
	const stretchT = new Tween(0);
	const waysT = new Tween(0);
	const badge = new Tween(0);

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
		// overflow the TOP a lot (the pull), but stop the BOTTOM just past the
		// board edge — never into the special cells / HUD rail underneath.
		const topHalf = boardHalf + 1.6 * SYMBOL_SIZE;
		const bottomHalf = boardHalf + 0.15 * SYMBOL_SIZE;
		return incoming.map(({ reel, ways, baseRows }) => {
			const art = pickWildReelArt();
			return {
				reel,
				ways,
				baseWays: Math.max(baseRows, 1),
				cx: originX + (reel + 0.5) * SYMBOL_SIZE,
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
			};
		});
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
			badge.set(1, { duration: 260, easing: backOut });
			// 1) the wild column drops in over the vanishing symbols
			phase = 'drop';
			await dropT.set(1, { duration: 520, easing: backOut });
			// 2) then it stretches — bigger final ways ⇒ LONGER pull.
			phase = 'stretch';
			const maxWays = Math.max(...added.map((r) => r.ways));
			const dur = Math.min(3200, Math.max(750, 700 + maxWays * 4.4));
			waysT.set(1, { duration: dur, easing: cubicOut });
			await stretchT.set(1, { duration: dur, easing: backOut });
		},
		stretchFxHide: () => {
			destroyReels();
			reels = [];
			phase = 'idle';
			dropT.set(0, { duration: 0 });
			stretchT.set(0, { duration: 0 });
			waysT.set(0, { duration: 0 });
			badge.set(0, { duration: 0 });
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
			g.fill({ color: 0xffffff, alpha: 0.85 * a });
			g.rect(-w / 2 - 5, y - 4, w + 10, 8);
			g.fill({ color: BLOOD, alpha: 0.22 * a });
		}
	};
</script>

{#if reels.length}
	<MainContainer>
		<Container x={stateShake.x} y={stateShake.y}>
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
							width={SYMBOL_SIZE}
							height={cell.baseH}
							backgroundColor={0xffffff}
						/>
						<Sprite
							key={cell.art.key}
							x={0}
							y={-cell.baseH * (1 - dropT.current)}
							anchor={0.5}
							width={SYMBOL_SIZE}
							height={cell.baseH}
						/>
					</Container>
				{:else}
					<Container x={cell.cx} y={cell.cy}>
						<Rectangle
							isMask
							anchor={{ x: 0.5, y: 0 }}
							y={topY}
							width={SYMBOL_SIZE}
							height={bottomY - topY}
							backgroundColor={0xffffff}
						/>
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
									width={SYMBOL_SIZE}
									height={y1 - y0}
								/>
							{/each}
						</Container>
						<Graphics draw={(g) => drawGrip(g, SYMBOL_SIZE, topY, bottomY, flare)} />
					</Container>
				{/if}
			{/each}

			<!-- plain WAYS text centred in the reel, counting up as it stretches -->
			{#each reels as cell (cell.reel)}
				{@const bp = badge.current}
				{#if bp > 0.001}
					{@const shown = cell.settled
						? cell.ways
						: Math.round(cell.baseWays + (cell.ways - cell.baseWays) * waysT.current)}
					{@const pop = cell.settled ? 1 : 1 + 0.12 * Math.sin(Math.min(1, waysT.current) * Math.PI)}
					<Container
						x={cell.cx}
						y={cell.cy}
						scale={(0.7 + 0.3 * bp) * pop}
						alpha={Math.min(1, bp * 1.6)}
					>
						<Text
							anchor={0.5}
							text={`${shown} WAYS`}
							style={{
								fontFamily: 'Arial',
								fontWeight: '900',
								fontSize: 26,
								fill: 0xffffff,
								stroke: { color: 0x000000, width: 5 },
							}}
						/>
					</Container>
				{/if}
			{/each}
		</Container>
	</MainContainer>
{/if}
