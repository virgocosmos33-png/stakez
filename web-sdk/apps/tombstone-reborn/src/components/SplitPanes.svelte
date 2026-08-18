<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// SPLIT: knife slashes horizontally; the card comes apart into N wide layers
	// stacked top-to-bottom (capped at 4). Count text only from 6+ (one symbol).
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle, Sprite } from 'pixi-svelte';
	import { playExternalOnce } from 'utils-sound';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { fxDur } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import { isNudgeCoveredReel, isVisibleBoardCell } from '../game/boardCells';
	import {
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
		HIGH_SYMBOLS,
	} from '../game/constants';
	import { shakeBoard } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX } from '../game/tombstoneVfx';
	import { formatWaysMult } from '../game/waysFormat';
	import RedGlowMark from './RedGlowMark.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	const MAX_PANES = 4;
	/** stacked panes carry 2–5; from 6 the cell stays one symbol and shows the count */
	const COUNT_LABEL_MIN = 6;
	const COUNT_PAD = 8;
	const KNIFE_ASPECT = 1024 / 290;
	const SLASH_ASPECT = 1280 / 172;
	const KNIFE_W = CARD_W * 1.58;
	const KNIFE_H = KNIFE_W / KNIFE_ASPECT;
	const SLASH_W = CARD_W * 1.9;
	const SLASH_H = SLASH_W / SLASH_ASPECT;

	const KNIFE_MS = 1180;
	/** knife has arrived at the left of the card, blade on the cut line */
	const KNIFE_READY = 0.36;
	/** pull-back finished — the slash starts here */
	const KNIFE_WIND = 0.5;
	/** tip is through the card — copies snap apart */
	const KNIFE_IMPACT = 0.7;
	const KNIFE_OUT = 0.86;
	const SPLIT_SFX = '/assets/audio/sfx_split.mp3';
	const READY_X = -CARD_W * 0.62;
	const READY_Y = 0;
	const START_X = -CARD_W * 1.55;
	const START_Y = -CARD_H * 0.42;
	const END_X = CARD_W * 1.28;
	const END_Y = CARD_H * 0.1;

	type SplitCell = {
		key: string;
		reel: number;
		row: number;
		count: number;
		pinned?: SymbolName;
		cx: number;
		cy: number;
		seed: number;
		fresh: boolean;
	};
	type DrawnCell = SplitCell & { name: SymbolName };

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	/** -1 when idle, else normalised progress through the slash */
	let knifeT = $state(-1);
	let knifeRaf = 0;
	let knifeAlive = true;
	const fallOut = new Tween(0);
	const splitProgress = new Tween(1);
	const seamFlare = new Tween(0);
	const detonation = new Tween(0);
	const pulse = new Tween(1);

	const mix = (from: number, to: number, t: number) => from + (to - from) * t;
	const span = (t: number, from: number, to: number) =>
		Math.min(Math.max((t - from) / (to - from), 0), 1);

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	/** blade tip, card-local. Approach → settle → pull back → slash → exit. */
	const knifeTipX = (t: number) => {
		if (t < KNIFE_READY) return mix(START_X, READY_X, cubicOut(span(t, 0, KNIFE_READY)));
		if (t < KNIFE_WIND) return mix(READY_X, READY_X - CARD_W * 0.1, span(t, KNIFE_READY, KNIFE_WIND));
		if (t <= KNIFE_IMPACT) {
			return mix(READY_X - CARD_W * 0.1, CARD_W * 0.2, cubicIn(span(t, KNIFE_WIND, KNIFE_IMPACT)));
		}
		return mix(CARD_W * 0.2, END_X, cubicIn(span(t, KNIFE_IMPACT, 1)));
	};
	const knifeY = (t: number) => {
		if (t < KNIFE_READY) return mix(START_Y, READY_Y, cubicOut(span(t, 0, KNIFE_READY)));
		if (t < KNIFE_WIND) return READY_Y;
		if (t <= KNIFE_IMPACT) return mix(READY_Y, READY_Y + CARD_H * 0.02, span(t, KNIFE_WIND, KNIFE_IMPACT));
		return mix(READY_Y + CARD_H * 0.02, END_Y, span(t, KNIFE_IMPACT, 1));
	};
	const knifeRoll = (t: number) => {
		if (t < KNIFE_READY) return mix(-0.72, -0.22, cubicOut(span(t, 0, KNIFE_READY)));
		if (t < KNIFE_WIND) return mix(-0.22, -0.4, span(t, KNIFE_READY, KNIFE_WIND));
		if (t <= KNIFE_IMPACT) return mix(-0.4, 0.08, cubicIn(span(t, KNIFE_WIND, KNIFE_IMPACT)));
		return mix(0.08, 0.18, span(t, KNIFE_IMPACT, 1));
	};
	const knifeAlpha = (t: number) =>
		t < KNIFE_READY * 0.45
			? 0.88 * cubicOut(span(t, 0, KNIFE_READY * 0.45))
			: 0.88 * (1 - cubicIn(span(t, KNIFE_OUT, 1)));
	const knifeScale = (t: number) => {
		if (t < KNIFE_READY) return mix(0.86, 1, cubicOut(span(t, 0, KNIFE_READY)));
		if (t < KNIFE_WIND) return mix(1, 0.96, span(t, KNIFE_READY, KNIFE_WIND));
		if (t <= KNIFE_IMPACT) return mix(0.96, 1.1, span(t, KNIFE_WIND, KNIFE_IMPACT));
		return mix(1.1, 0.94, span(t, KNIFE_IMPACT, 1));
	};

	const slashHeat = (t: number) => {
		if (t < KNIFE_WIND) return 0;
		if (t <= KNIFE_IMPACT) return span(t, KNIFE_WIND, KNIFE_IMPACT);
		return 1 - cubicIn(span(t, KNIFE_IMPACT, 0.96));
	};

	const playKnife = (onSlash: () => void, onImpact: () => void) =>
		new Promise<void>((resolve) => {
			const start = performance.now();
			const dur = fxDur(KNIFE_MS);
			let slashed = false;
			let fired = false;
			knifeT = 0;
			const step = (now: number) => {
				if (!knifeAlive) {
					resolve();
					return;
				}
				const t = (now - start) / dur;
				if (!slashed && t >= KNIFE_WIND) {
					slashed = true;
					onSlash();
				}
				if (!fired && t >= KNIFE_IMPACT) {
					fired = true;
					onImpact();
				}
				if (t >= 1) {
					knifeT = -1;
					resolve();
					return;
				}
				knifeT = t;
				knifeRaf = requestAnimationFrame(step);
			};
			knifeRaf = requestAnimationFrame(step);
		});

	onDestroy(() => {
		knifeAlive = false;
		if (knifeRaf) cancelAnimationFrame(knifeRaf);
	});

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
				.filter((cell) => !wildReels.has(cell.reel) && !isNudgeCoveredReel(cell.reel))
				.map((cell) => [
					cell.key,
					{
						...cell,
						fresh: false,
						cx: getSymbolX(cell.reel),
						cy: getCellCenterY(cell.reel, cell.row),
					},
				]),
		);
		let anyFresh = false;
		for (const c of incoming) {
			if (c.count <= 1 || wildReels.has(c.reel) || isNudgeCoveredReel(c.reel)) continue;
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
		pulse.set(1.28, { duration: 0 });
		knifeT = -1;

		let settle: Promise<unknown> = Promise.resolve();
		await playKnife(
			() => playExternalOnce(SPLIT_SFX),
			() => {
				seamFlare.set(1, { duration: 20 });
				seamFlare.set(0, { duration: 180 });
				shakeBoard({
					intensity: Math.min(10 + cells.filter((c) => c.fresh).length * 2.5, 18),
					duration: fxDur(240),
				});
				const fx = detonation.set(1, { duration: 300, easing: cubicOut });
				const punch = pulse.set(1, { duration: 400, easing: backOut });
				const apart = splitProgress.set(1, { duration: 180, easing: backOut });
				settle = Promise.all([fx, punch, apart]);
			},
		);
		await settle;
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
			knifeT = -1;
			fallOut.set(0, { duration: 0 });
		},
		splitPanesHide: () => {
			show = false;
			cells = [];
			knifeT = -1;
			fallOut.set(0, { duration: 0 });
		},
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

	const drawDivider = (g: import('pixi.js').Graphics, _cell: SplitCell, _i: number, slim: number) => {
		g.roundRect(-CARD_W / 2, -1.6 * slim, CARD_W, 3.2 * slim, 1.2);
		g.fill({ color: TOMBSTONE_FX.dust, alpha: 0.26 * slim });
		g.roundRect(-CARD_W / 2, -0.55 * slim, CARD_W, 1.1 * slim, 0.4);
		g.fill({ color: TOMBSTONE_FX.boneDust, alpha: 0.66 });
	};

	const drawCutLine = (g: import('pixi.js').Graphics, t: number) => {
		const heat = slashHeat(t);
		if (heat <= 0.01) return;
		const tip = knifeTipX(t);
		const left = -CARD_W / 2 - 6;
		const right = Math.min(tip, CARD_W / 2 + 10);
		if (right <= left) return;
		g.roundRect(left, -6, right - left, 12, 5);
		g.fill({ color: TOMBSTONE_FX.bloodRust, alpha: 0.2 * heat });
		g.roundRect(left, -1.4, right - left, 2.8, 1);
		g.fill({ color: 0xfff1c2, alpha: 0.95 * heat });
		if (t < KNIFE_OUT) {
			g.ellipse(tip, 0, 14, 3.2);
			g.fill({ color: 0xffe08a, alpha: 0.7 * heat });
			for (let k = 0; k < 5; k++) {
				const sparkSeed = 19 + k * 11 + Math.floor(t * 40);
				const life = (t * (4 + rand(sparkSeed) * 2) + rand(sparkSeed + 1)) % 1;
				const side = rand(sparkSeed + 2) > 0.5 ? 1 : -1;
				const x = tip - 4 - rand(sparkSeed + 3) * 18;
				const y = side * (4 + life * 16);
				g.circle(x, y, 1.1 + (1 - life) * 1.4);
				g.fill({ color: k % 2 === 0 ? 0xffe8a0 : TOMBSTONE_FX.spentBrass, alpha: 0.8 * (1 - life) * heat });
			}
		}
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
	{@const panes = cell.count >= COUNT_LABEL_MIN ? 1 : Math.min(cell.count, MAX_PANES)}
	{@const sliceHeight = CARD_H / panes}
	{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	{@const split = cell.fresh ? splitProgress.current : 1}
	{@const slim = Math.min(1, 3 / panes)}
	{@const gap = CARD_H * Math.min(0.03, 0.1 / panes)}
	{@const paneHeight = Math.max((sliceHeight - gap) * split + CARD_H * (1 - split), 2)}
	<Container x={cell.cx} y={cell.cy} scale={cell.fresh ? pulse.current : 1}>
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
		{#if cell.fresh}
			<Graphics draw={(g) => drawDetonation(g, cell, panes, detonation.current, split)} />
			<Graphics draw={(g) => drawSeamFlare(g, seamFlare.current)} />
			{@render knifeStrike()}
		{/if}
		{#if cell.count >= COUNT_LABEL_MIN}
			<RedGlowMark
				x={CARD_W / 2 - COUNT_PAD}
				y={CARD_H / 2 - COUNT_PAD}
				anchor={{ x: 1, y: 1 }}
				label={formatWaysMult(cell.count)}
				fontSize={22}
				alpha={cell.fresh ? splitProgress.current : 1}
			/>
		{/if}
	</Container>
{/snippet}

{#snippet knifeStrike()}
	{#if knifeT >= 0}
		{@const t = knifeT}
		{@const tip = knifeTipX(t)}
		{@const alpha = knifeAlpha(t)}
		{@const heat = slashHeat(t)}
		<Graphics draw={(g) => drawCutLine(g, t)} />
		<Sprite
			key="splitSlash"
			x={mix(-CARD_W * 0.15, tip * 0.15, span(t, KNIFE_WIND, KNIFE_IMPACT))}
			y={0}
			anchor={0.5}
			width={SLASH_W * mix(0.35, 1.05, span(t, KNIFE_WIND, KNIFE_IMPACT))}
			height={SLASH_H}
			alpha={heat}
			blendMode="add"
		/>
		<Sprite
			key="splitKnife"
			x={tip - 10}
			y={knifeY(t) + CARD_H * 0.03}
			anchor={{ x: 0.88, y: 0.52 }}
			width={KNIFE_W * knifeScale(t)}
			height={KNIFE_H * knifeScale(t)}
			rotation={knifeRoll(t)}
			alpha={alpha * 0.28}
			tint={0x000000}
		/>
		<Sprite
			key="splitKnife"
			x={tip}
			y={knifeY(t)}
			anchor={{ x: 0.88, y: 0.52 }}
			width={KNIFE_W * knifeScale(t)}
			height={KNIFE_H * knifeScale(t)}
			rotation={knifeRoll(t)}
			alpha={alpha}
		/>
	{/if}
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
		</BoardSpace>
	{/if}
</MainContainer>
