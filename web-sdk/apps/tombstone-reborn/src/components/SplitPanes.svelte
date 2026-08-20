<script lang="ts" module>
	import type { RawSymbol, SymbolName } from '../game/types';

	// SPLIT: one stab pose per seam. After impact the blade is masked off
	// inside the card so only the handle sticks out. 1→2 is one blood, 1→3 is two.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
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
	import SplitBlood from './SplitBlood.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	const MAX_PANES = 4;
	const COUNT_LABEL_MIN = 6;
	const COUNT_PAD = 8;

	const KNIFE = {
		aspect: 1024 / 599,
		width: CARD_W * 1.72,
		anchor: { x: 0.86, y: 0.68 },
	} as const;
	const CLIP_W = CARD_W * 6;
	const CLIP_H = CARD_H * 3;
	/** Right edge of the knife mask. Open = whole flight visible; buried = card face hides the blade. */
	const CLIP_OPEN_X = CARD_W * 2.4;
	const CLIP_BURY_X = -CARD_W / 2;

	const GASH_W = CARD_W * 1.22;
	const GASH_H = GASH_W * (216 / 1024);
	const BLOOD_W = CARD_W * 1.35;
	const BLOOD_H = BLOOD_W * (360 / 640);

	const KNIFE_MS = 560;
	const KNIFE_STAB = 0.58;
	const SPLIT_SFX = '/assets/audio/sfx_split.mp3';

	const START_X = -CARD_W * 1.28;
	const HIT_X = CARD_W * 0.02;

	const paneCount = (count: number) =>
		count >= COUNT_LABEL_MIN ? 1 : Math.min(count, MAX_PANES);
	const cutCount = (count: number) => {
		const panes = paneCount(count);
		return panes <= 1 ? 1 : panes - 1;
	};
	const seamY = (count: number, seam: number) => {
		const panes = paneCount(count);
		if (panes <= 1) return 0;
		return -CARD_H / 2 + ((seam + 1) / panes) * CARD_H;
	};

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
	type DrawnCell = SplitCell & { name: SymbolName; level?: RawSymbol['level'] };

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	/** -1 when idle, else normalised progress through the current cut */
	let knifeT = $state(-1);
	let cutIndex = $state(0);
	let settledCuts = $state(0);
	let bloodBorn = $state<Record<string, number[]>>({});
	let fxNow = $state(0);
	let knifeRaf = 0;
	let clockRaf = 0;
	let knifeAlive = true;

	const fallOut = new Tween(0);
	const pulse = new Tween(1);

	const mix = (from: number, to: number, t: number) => from + (to - from) * t;
	const span = (t: number, from: number, to: number) =>
		Math.min(Math.max((t - from) / (to - from), 0), 1);

	const knifeTipX = (t: number) =>
		t < KNIFE_STAB ? mix(START_X, HIT_X, cubicOut(span(t, 0, KNIFE_STAB))) : HIT_X;

	const knifeDip = (t: number) =>
		t < KNIFE_STAB ? mix(-CARD_H * 0.08, 0, cubicOut(span(t, 0, KNIFE_STAB))) : 0;

	const knifeAlpha = (t: number) =>
		t < KNIFE_STAB * 0.35 ? cubicOut(span(t, 0, KNIFE_STAB * 0.35)) : 1;

	const knifeScale = (t: number) => {
		if (t < KNIFE_STAB) return mix(0.86, 1.1, cubicOut(span(t, 0, KNIFE_STAB)));
		return mix(1.1, 1, span(t, KNIFE_STAB, KNIFE_STAB + 0.2));
	};

	const startClock = () => {
		if (clockRaf) return;
		const step = (now: number) => {
			fxNow = now;
			clockRaf = requestAnimationFrame(step);
		};
		clockRaf = requestAnimationFrame(step);
	};

	const stopClock = () => {
		if (clockRaf) cancelAnimationFrame(clockRaf);
		clockRaf = 0;
	};

	const playKnife = (onStab: () => void) =>
		new Promise<void>((resolve) => {
			const start = performance.now();
			const dur = fxDur(KNIFE_MS);
			let stabbed = false;
			knifeT = 0;
			const step = (now: number) => {
				if (!knifeAlive) {
					resolve();
					return;
				}
				const t = (now - start) / dur;
				if (!stabbed && t >= KNIFE_STAB) {
					stabbed = true;
					onStab();
				}
				if (t >= 1) {
					knifeT = 1;
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
		stopClock();
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
			.map((cell) => {
				const raw = context.stateGame.board[cell.reel]?.reelState.symbols[cell.row]?.rawSymbol;
				return {
					...cell,
					cy: getCellCenterY(cell.reel, cell.row),
					name: cell.pinned ?? (raw?.name as SymbolName | undefined),
					level: raw?.level,
				};
			})
			.filter((cell) => cell.name != null) as DrawnCell[],
	);

	const stampBlood = (seam: number) => {
		const next: Record<string, number[]> = { ...bloodBorn };
		const now = performance.now();
		for (const cell of cells) {
			if (!cell.fresh) continue;
			if (seam >= cutCount(cell.count)) continue;
			const stamps = next[cell.key] ? [...next[cell.key]] : [];
			stamps[seam] = now;
			next[cell.key] = stamps;
		}
		bloodBorn = next;
	};

	const cellSplit = (cell: SplitCell) => {
		if (!cell.fresh) return 1;
		const cuts = cutCount(cell.count);
		const done = Math.min(settledCuts, cuts);
		const live =
			knifeT >= KNIFE_STAB && cutIndex < cuts
				? span(knifeT, KNIFE_STAB, KNIFE_STAB + 0.16)
				: 0;
		return Math.min(1, (done + live) / cuts);
	};

	const runSplit = async () => {
		pulse.set(1.2, { duration: 0 });
		knifeT = -1;
		cutIndex = 0;
		settledCuts = 0;
		bloodBorn = {};
		startClock();

		const fresh = cells.filter((cell) => cell.fresh);
		const maxCuts = Math.max(1, ...fresh.map((cell) => cutCount(cell.count)));
		let settle: Promise<unknown> = Promise.resolve();

		for (let seam = 0; seam < maxCuts; seam += 1) {
			cutIndex = seam;
			await playKnife(() => {
				playExternalOnce(SPLIT_SFX);
				stampBlood(seam);
				shakeBoard({
					intensity: Math.min(8 + fresh.length * 2, 16),
					duration: fxDur(180),
				});
				settle = pulse.set(1, { duration: 280, easing: backOut });
			});
			settledCuts = seam + 1;
			knifeT = -1;
		}
		await settle;
	};

	const resetFx = () => {
		knifeT = -1;
		cutIndex = 0;
		settledCuts = 0;
		bloodBorn = {};
		stopClock();
		fallOut.set(0, { duration: 0 });
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
			resetFx();
		},
		splitPanesHide: () => {
			show = false;
			cells = [];
			resetFx();
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

	const drawDivider = (g: import('pixi.js').Graphics, slim: number) => {
		g.roundRect(-CARD_W / 2, -1.6 * slim, CARD_W, 3.2 * slim, 1.2);
		g.fill({ color: TOMBSTONE_FX.dust, alpha: 0.26 * slim });
		g.roundRect(-CARD_W / 2, -0.55 * slim, CARD_W, 1.1 * slim, 0.4);
		g.fill({ color: TOMBSTONE_FX.boneDust, alpha: 0.66 });
	};

</script>

{#snippet knifeSprite(x: number, y: number, scale: number, alpha: number, buried: boolean)}
	<Container>
		<Rectangle
			isMask
			anchor={{ x: 1, y: 0.5 }}
			x={buried ? CLIP_BURY_X : CLIP_OPEN_X}
			width={CLIP_W}
			height={CLIP_H}
			backgroundColor={0xffffff}
		/>
		<Sprite
			key="splitKnifeStab"
			{x}
			{y}
			anchor={KNIFE.anchor}
			width={KNIFE.width * scale}
			height={(KNIFE.width / KNIFE.aspect) * scale}
			{alpha}
		/>
	</Container>
{/snippet}

{#snippet splitCell(cell: DrawnCell)}
	{@const panes = paneCount(cell.count)}
	{@const cuts = cutCount(cell.count)}
	{@const sliceHeight = CARD_H / panes}
	{@const symbolInfo = getSymbolInfo({
		rawSymbol: { name: cell.name, level: cell.level },
		state: 'postWinStatic',
	})}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	{@const split = cellSplit(cell)}
	{@const slim = Math.min(1, 3 / panes)}
	{@const gap = CARD_H * Math.min(0.03, 0.1 / panes)}
	{@const paneHeight = Math.max((sliceHeight - gap) * split + CARD_H * (1 - split), 2)}
	{@const stamps = bloodBorn[cell.key] ?? []}
	<Container x={cell.cx} y={cell.cy} scale={cell.fresh ? pulse.current : 1}>
		<Graphics draw={drawUnderGlow} />
		{#each Array.from({ length: panes }) as _, i (i)}
			{@const paneY = (-CARD_H / 2 + (i + 0.5) * sliceHeight) * split}
			<Container y={paneY}>
				<Rectangle isMask anchor={0.5} width={CARD_W} height={paneHeight} backgroundColor={0xffffff} />
				<SymbolSprite {symbolInfo} />
			</Container>
		{/each}
		{#each Array.from({ length: Math.max(0, panes - 1) }) as _, i (i)}
			{#if stamps[i] == null}
				<Container y={(-CARD_H / 2 + (i + 1) * sliceHeight) * split} alpha={split}>
					<Graphics draw={(g) => drawDivider(g, slim)} />
				</Container>
			{/if}
		{/each}
		<Container alpha={split}>
			<Graphics draw={(g) => drawFrame(g, isHigh)} />
		</Container>
		{#each Array.from({ length: cuts }) as _, seam (seam)}
			{@const y = seamY(cell.count, seam)}
			{@const born = stamps[seam]}
			{#if born != null}
				<Sprite
					key="splitBloodGash"
					{y}
					anchor={0.5}
					width={GASH_W}
					height={GASH_H}
					alpha={0.92}
				/>
				<SplitBlood {y} {born} now={fxNow} width={BLOOD_W} height={BLOOD_H} />
			{/if}
			{#if settledCuts > seam}
				{@render knifeSprite(HIT_X, y, 1, 1, true)}
			{/if}
		{/each}
		{#if cell.fresh && knifeT >= 0 && cutIndex < cuts}
			{@render knifeSprite(
				knifeTipX(knifeT),
				seamY(cell.count, cutIndex) + knifeDip(knifeT),
				knifeScale(knifeT),
				knifeAlpha(knifeT),
				knifeT >= KNIFE_STAB,
			)}
		{/if}
		{#if cell.count >= COUNT_LABEL_MIN}
			<RedGlowMark
				x={CARD_W / 2 - COUNT_PAD}
				y={CARD_H / 2 - COUNT_PAD}
				anchor={{ x: 1, y: 1 }}
				label={formatWaysMult(cell.count)}
				fontSize={22}
				alpha={cell.fresh ? split : 1}
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
		</BoardSpace>
	{/if}
</MainContainer>
