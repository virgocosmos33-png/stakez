<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// SPLIT: knives fly in like gunsmoke rounds and hit (beat 1), then vanish.
	// Beat 2 is the existing split VFX only. Count from 6+.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { playExternalOnce, preloadExternal } from 'utils-sound';
	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import { isVisibleBoardCell } from '../game/boardCells';
	import {
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
		HIGH_SYMBOLS,
	} from '../game/constants';
	import {
		BULLET_DIST_MS,
		BULLET_MAX_MS,
		BULLET_MS,
		BULLET_NEAR_SCALE,
		fpsMuzzlePoint,
		isHighPaySymbol,
		planKnifeRhythm,
		volleySeed,
	} from '../game/gunsmokeSpin';
	import { buildCountUp } from '../game/splitBullets';
	import { shakeBoard } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX } from '../game/tombstoneVfx';
	import { trValueStyle } from '../game/typography';
	import SymbolSprite from './SymbolSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	onMount(() => preloadExternal(KNIFE_HIT_SFX));

	const MAX_PANES = 4;
	/** stacked panes carry 2–5; from 6 the cell stays one symbol and shows the count */
	const COUNT_LABEL_MIN = 6;
	const COUNT_PAD = 8;
	const KNIFE_HIT_SFX = '/assets/audio/sfx_split.mp3';
	const KNIFE_ASPECT = 1024 / 290;
	const KNIFE_W = CARD_W * 0.79;
	const KNIFE_H = KNIFE_W / KNIFE_ASPECT;
	/** measured on tr_split_knife.png — clipped point, not the sprite center */
	const KNIFE_TIP = { x: 0.987, y: 0.776 };
	/** art tip points slightly down; subtract so the point leads along the path */
	const KNIFE_NATIVE = 8.09 * (Math.PI / 180);

	type SplitCell = {
		key: string;
		reel: number;
		row: number;
		count: number;
		/** live split shown so far — climbs one step per knife hit */
		shown: number;
		pinned?: SymbolName;
		cx: number;
		cy: number;
		seed: number;
		fresh: boolean;
	};
	type DrawnCell = SplitCell & { name: SymbolName };
	type FlyKnife = {
		id: number;
		x0: number;
		y0: number;
		x1: number;
		y1: number;
		travel: number;
		t: Tween<number>;
	};

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	let time = $state(0);
	let flights = $state<FlyKnife[]>([]);
	let nextFly = 0;
	/** only this cell plays the split VFX on the current hit */
	let animKey = $state<string | null>(null);
	const fallOut = new Tween(0);
	const splitProgress = new Tween(1);
	const seamFlare = new Tween(0);
	const detonation = new Tween(0);
	const pulse = new Tween(1);

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const seamYs = (count: number) => {
		const panes = count >= COUNT_LABEL_MIN ? 1 : Math.min(count, MAX_PANES);
		if (panes <= 1) return [0];
		const slice = CARD_H / panes;
		return Array.from({ length: panes - 1 }, (_, i) => -CARD_H / 2 + (i + 1) * slice);
	};

	/** one throw per split the cell is about to do, same cap as the stacked panes */
	const throwsFor = (count: number) => Math.min(Math.max(count, 1), MAX_PANES);

	const flying = $derived(
		flights.map((round) => {
			const t = round.t.current;
			return {
				...round,
				x: round.x0 + (round.x1 - round.x0) * t,
				y: round.y0 + (round.y1 - round.y0) * t,
				rotation: round.travel - KNIFE_NATIVE,
				scale: BULLET_NEAR_SCALE + (1 - BULLET_NEAR_SCALE) * t,
			};
		}),
	);

	const flyOneKnife = async (
		to: { x: number; y: number },
		side: Parameters<typeof fpsMuzzlePoint>[2],
		seed: number,
		flightScale: number,
	) => {
		const main = context.stateLayoutDerived.mainLayout();
		const board = context.stateGameDerived.boardLayout();
		const from = fpsMuzzlePoint(board, { left: 0, right: main.width }, side, seed);
		const flight = new Tween(0);
		const round: FlyKnife = {
			id: nextFly++,
			x0: from.x,
			y0: from.y,
			x1: to.x,
			y1: to.y,
			travel: Math.atan2(to.y - from.y, to.x - from.x),
			t: flight,
		};
		flights = [...flights, round];
		const dist = Math.hypot(to.x - from.x, to.y - from.y);
		await flight.set(1, {
			duration: fxDur(Math.min(BULLET_MAX_MS, BULLET_MS + dist * BULLET_DIST_MS) * flightScale),
			easing: cubicOut,
		});
		flights = flights.filter((item) => item.id !== round.id);
	};

	const stepsFor = (from: number, to: number, n: number) => {
		if (to >= COUNT_LABEL_MIN) return buildCountUp(from, to, n);
		return Array.from({ length: n }, (_, i) => Math.min(from + i + 1, to));
	};

	const playHitSplit = async (key: string, wait: boolean) => {
		const same = animKey === key;
		animKey = key;
		if (!same) {
			splitProgress.set(0, { duration: 0 });
			detonation.set(0, { duration: 0 });
		}
		seamFlare.set(1, { duration: 20 });
		seamFlare.set(0, { duration: 180 });
		pulse.set(1.06, { duration: 0 });
		pulse.set(1, { duration: 180, easing: backOut });
		const anim = Promise.all([
			detonation.set(1, { duration: 300, easing: cubicOut }),
			splitProgress.set(1, { duration: 180, easing: backOut }),
		]);
		if (wait) await anim;
	};

	const flyKnives = async (fresh: SplitCell[]) => {
		const targets: {
			key: string;
			reel: number;
			row: number;
			x: number;
			y: number;
			seed: number;
			next: number;
		}[] = [];
		for (const cell of fresh) {
			const cx = getSymbolX(cell.reel);
			const cy = getCellCenterY(cell.reel, cell.row);
			const n = throwsFor(cell.count);
			const steps = stepsFor(cell.shown, cell.count, n);
			for (let i = 0; i < n; i += 1) {
				const next = steps[i] ?? cell.count;
				const seams = seamYs(next);
				targets.push({
					key: cell.key,
					reel: cell.reel,
					row: cell.row,
					x: cx,
					y: cy + (seams[Math.min(i, seams.length - 1)] ?? 0),
					seed: cell.seed + i * 13,
					next,
				});
			}
		}
		const rhythm = planKnifeRhythm(targets.length, volleySeed(fresh));
		for (let i = 0; i < targets.length; i += 1) {
			const target = targets[i];
			const shot = rhythm[i];
			if (!target || !shot) continue;
			await flyOneKnife(target, shot.side, target.seed, shot.flightScale);
			playExternalOnce(KNIFE_HIT_SFX, { forcePlay: true });
			shakeBoard({ intensity: 4 + shot.flightScale * 2, duration: fxDur(90) });
			cells = cells.map((cell) => (cell.key === target.key ? { ...cell, shown: target.next } : cell));
			const face =
				fresh.find((cell) => cell.key === target.key)?.pinned ??
				(context.stateGameDerived.boardRaw()[target.reel]?.[target.row]?.name as
					| SymbolName
					| undefined);
			if (face && isHighPaySymbol(face)) {
				context.eventEmitter.broadcast({
					type: 'cellFrameStain',
					reel: target.reel,
					row: target.row,
				});
			}
			await playHitSplit(target.key, shot.burst !== true);
			if (shot.beatMs > 0) await fxWait(shot.beatMs);
		}
		animKey = null;
	};

	/**
	 * MERGE the incoming split cells into whatever is already up.
	 *
	 * A spin can fire several feature events back to back. Cells already up
	 * keep their panes; a cell named again gets its new count and re-animates.
	 * Returns true when at least one cell is new or changed.
	 */
	const layout = (incoming: { reel: number; row: number; count: number; name?: SymbolName }[]) => {
		const wildReels = new Set([
			...context.stateGame.wildReelReels,
			...context.stateGame.stretchedReels,
		]);
		const merged = new Map<string, SplitCell>(
			cells
				.filter((cell) => !wildReels.has(cell.reel))
				.map((cell) => [
					cell.key,
					{
						...cell,
						fresh: false,
						shown: cell.count,
						cx: getSymbolX(cell.reel),
						cy: getCellCenterY(cell.reel, cell.row),
					},
				]),
		);
		let anyFresh = false;
		for (const c of incoming) {
			if (c.count <= 1 || wildReels.has(c.reel)) continue;
			if (!isVisibleBoardCell(c.reel, c.row)) continue;
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
				shown: existing?.count ?? 1,
				pinned: c.name,
				cx: getSymbolX(c.reel),
				cy: getCellCenterY(c.reel, c.row),
				seed: c.reel * 31 + c.row * 7 + c.count * 113,
				fresh: true,
			});
		}
		cells = [...merged.values()];
		show = cells.length > 0;
		return anyFresh;
	};

	const drawn = $derived(
		cells
			.map((cell) => ({
				...cell,
				cy: getCellCenterY(cell.reel, cell.row),
				name:
					cell.pinned ??
					(context.stateGame.board[cell.reel]?.reelState.symbols[cell.row]?.rawSymbol
						.name as SymbolName | undefined),
			}))
			.filter((cell): cell is DrawnCell => cell.name != null),
	);

	const runSplit = async () => {
		splitProgress.set(0, { duration: 0 });
		seamFlare.set(0, { duration: 0 });
		detonation.set(0, { duration: 0 });
		pulse.set(1, { duration: 0 });
		flights = [];

		const fresh = cells.filter((cell) => cell.fresh);
		await flyKnives(fresh);
	};

	context.eventEmitter.subscribeOnMount({
		splitPanesShow: async ({ cells: incoming }) => {
			const anyFresh = layout(incoming);
			if (!anyFresh || !cells.length) return;
			await runSplit();
			cells = cells.map((cell) => (cell.fresh ? { ...cell, fresh: false } : cell));
		},
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, show && cells.length > 0);
			show = false;
			cells = [];
			flights = [];
			animKey = null;
			fallOut.set(0, { duration: 0 });
		},
		splitPanesHide: () => {
			show = false;
			cells = [];
			flights = [];
			animKey = null;
			fallOut.set(0, { duration: 0 });
		},
	});

	$effect(() => {
		if (!show) return;
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
		g.roundRect(-CARD_W / 2 - 2, -CARD_H / 2 - 2, CARD_W + 4, CARD_H + 4, 8);
		g.fill({ color: TOMBSTONE_FX.dark, alpha: 0.92 });
	};

	const drawFrame = (g: import('pixi.js').Graphics, isHigh: boolean) => {
		g.roundRect(-CARD_W / 2 - 3, -CARD_H / 2 - 3, CARD_W + 6, CARD_H + 6, 8);
		g.stroke({
			color: isHigh ? TOMBSTONE_FX.ironEdge : TOMBSTONE_FX.iron,
			width: 2,
			alpha: isHigh ? 0.8 : 0.62,
		});
	};

	const drawDivider = (g: import('pixi.js').Graphics, cell: SplitCell, i: number, slim: number) => {
		const flicker = 0.88 + 0.12 * Math.sin(time * 11 + cell.seed * 3 + i * 1.7);
		g.roundRect(-CARD_W / 2, -1.6 * slim, CARD_W, 3.2 * slim, 1.2);
		g.fill({ color: TOMBSTONE_FX.dust, alpha: 0.28 * flicker * slim });
		g.roundRect(-CARD_W / 2, -0.55 * slim, CARD_W, 1.1 * slim, 0.4);
		g.fill({ color: TOMBSTONE_FX.boneDust, alpha: 0.7 * flicker });
	};

	const drawSeamFlare = (g: import('pixi.js').Graphics, flare: number) => {
		if (flare <= 0.01) return;
		g.ellipse(0, 0, CARD_W * 0.55 * flare + 10, 5 * flare + 1.5);
		g.fill({ color: 0xfff4d0, alpha: 0.8 * flare });
		g.roundRect(-CARD_W / 2 - 8, -3.2, CARD_W + 16, 6.4, 3);
		g.fill({ color: TOMBSTONE_FX.spentBrass, alpha: 0.65 * flare });
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
		g.roundRect(-CARD_W / 2 - 4, -CARD_H / 2 - 4, CARD_W + 8, CARD_H + 8, 10);
		g.fill({ color: TOMBSTONE_FX.spentBrass, alpha: 0.28 * fade * fade });
		const ring = CARD_H * (0.2 + 0.85 * d);
		g.circle(0, 0, ring);
		g.stroke({ color: TOMBSTONE_FX.boneDust, width: 2.4 * fade + 0.5, alpha: 0.7 * fade });
		for (let seamIndex = 0; seamIndex < panes - 1; seamIndex++) {
			const seamY = (-CARD_H / 2 + ((seamIndex + 1) / panes) * CARD_H) * split;
			for (let k = 0; k < 4; k++) {
				const sparkSeed = cell.seed * 17 + seamIndex * 71 + k * 13;
				const side = rand(sparkSeed) > 0.5 ? 1 : -1;
				const x0 = (rand(sparkSeed + 1) - 0.5) * CARD_W * 0.75;
				const speed = 30 + rand(sparkSeed + 2) * 48;
				const x = x0 + (rand(sparkSeed + 3) - 0.5) * 20 * d;
				const y = seamY + side * speed * d;
				g.moveTo(x, y);
				g.lineTo(x, y - side * 7 * fade);
				g.stroke({
					color: k % 2 === 0 ? TOMBSTONE_FX.spentBrass : TOMBSTONE_FX.boneDust,
					width: 1.3,
					alpha: 0.8 * fade,
				});
			}
		}
	};

</script>

{#snippet splitCell(cell: DrawnCell)}
	{@const display = cell.fresh ? cell.shown : cell.count}
	{@const panes = display >= COUNT_LABEL_MIN ? 1 : Math.min(Math.max(display, 1), MAX_PANES)}
	{@const sliceHeight = CARD_H / panes}
	{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	{@const split = !cell.fresh ? 1 : cell.key === animKey ? splitProgress.current : display <= 1 ? 0 : 1}
	{@const slim = Math.min(1, 3 / panes)}
	{@const gap = CARD_H * Math.min(0.03, 0.1 / panes)}
	{@const paneHeight = Math.max((sliceHeight - gap) * split + CARD_H * (1 - split), 2)}
	<Container x={cell.cx} y={cell.cy} scale={cell.fresh && cell.key === animKey ? pulse.current : 1}>
		<Graphics draw={drawUnderGlow} />
		{#each Array.from({ length: panes }) as _, i (i)}
			{@const paneY = (-CARD_H / 2 + (i + 0.5) * sliceHeight) * split}
			<Container y={paneY}>
				<Rectangle isMask anchor={0.5} width={CARD_W} height={paneHeight} backgroundColor={0xffffff} />
				<SymbolSprite {symbolInfo} />
			</Container>
		{/each}
		{#each Array.from({ length: panes - 1 }) as _, i (i)}
			<Container y={(-CARD_H / 2 + (i + 1) * sliceHeight) * split} alpha={split}>
				<Graphics draw={(g) => drawDivider(g, cell, i, slim)} />
			</Container>
		{/each}
		<Container alpha={split}>
			<Graphics draw={(g) => drawFrame(g, isHigh)} />
		</Container>
		{#if cell.fresh && cell.key === animKey}
			<Graphics draw={(g) => drawDetonation(g, cell, panes, detonation.current, split)} />
			<Graphics draw={(g) => drawSeamFlare(g, seamFlare.current)} />
		{/if}
		{#if display >= COUNT_LABEL_MIN}
			<Text
				x={CARD_W / 2 - COUNT_PAD}
				y={CARD_H / 2 - COUNT_PAD}
				anchor={{ x: 1, y: 1 }}
				text={`${display}x`}
				alpha={1}
				style={trValueStyle({
					fontSize: 22,
					fill: 0xffffff,
					align: 'right',
					stroke: { color: 0x000000, width: 3, join: 'round' },
				})}
			/>
		{/if}
	</Container>
{/snippet}

<!-- MainContainer stays MOUNTED even while hidden: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). -->
<MainContainer>
	{#if show}
		<BoardSpace yOffset={fallOut.current}>
			{#each drawn as cell (cell.key)}
				{@render splitCell(cell)}
			{/each}
			{#each flying as round (round.id)}
				<Sprite
					key="splitKnife"
					x={round.x}
					y={round.y}
					anchor={KNIFE_TIP}
					width={KNIFE_W * round.scale}
					height={KNIFE_H * round.scale}
					rotation={round.rotation}
				/>
			{/each}
		</BoardSpace>
	{/if}
</MainContainer>
