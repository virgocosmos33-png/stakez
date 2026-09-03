<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// One slash per cell. trigger() then hold. Every fresh cell cuts together.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import 'pixi.js/advanced-blend-modes';
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicIn, linear } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Sprite } from 'pixi-svelte';
	import { playThemedOnce } from '../game/sfxTheme';
	import CellClipMask from './CellClipMask.svelte';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import { isNudgeCoveredReel, isVisibleBoardCell } from '../game/boardCells';
	import {
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
		HIGH_SYMBOLS,
		SPLIT_CELL_Z,
		SPLIT_KNIFE_Z,
	} from '../game/constants';
	import {
		SLASH,
		SLASH_ROT,
		GASH_KEY,
		GASH_H,
		DRIP_FALL,
		DRIP_FALL_MS,
		dripOrigins,
		drawSlashEnergy,
		drawSlashLip,
		type SplitDripKey,
	} from '../game/splitSlash';
	import { shakeBoard } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX } from '../game/tombstoneVfx';
	import { formatWaysMult } from '../game/waysFormat';
	import { isLowPaySymbol, usesHighPayPlate } from '../game/gunsmokeSpin';
	import HighPayBg from './HighPayBg.svelte';
	import LowPayBg from './LowPayBg.svelte';
	import RedGlowMark from './RedGlowMark.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	const COUNT_PAD = 8;

	type SplitDrip = {
		key: SplitDripKey;
		x: number;
		y0: number;
		w: number;
		h: number;
		delay: number;
		fall: Tween<number>;
	};
	type SplitCell = {
		key: string;
		reel: number;
		row: number;
		count: number;
		pinned?: SymbolName;
		cx: number;
		cy: number;
		fresh: boolean;
		split: Tween<number>;
		pulse: Tween<number>;
		slashPlay: Tween<number>;
		marked: boolean;
		drips: SplitDrip[];
	};
	type DrawnCell = SplitCell & { name: SymbolName };

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	let slashAlive = true;
	const fallOut = new Tween(0);

	onDestroy(() => {
		slashAlive = false;
	});

	const makeCell = (
		reel: number,
		row: number,
		count: number,
		pinned: SymbolName | undefined,
		fresh: boolean,
	): SplitCell => ({
		key: `${reel}-${row}`,
		reel,
		row,
		count,
		pinned,
		cx: getSymbolX(reel),
		cy: getCellCenterY(reel, row),
		fresh,
		split: new Tween(fresh ? 0 : 1),
		pulse: new Tween(1),
		slashPlay: new Tween(fresh ? 0 : 1),
		marked: !fresh,
		drips: fresh
			? []
			: dripOrigins(reel, row).map((drip) => ({
					...drip,
					fall: new Tween(1),
				})),
	});

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
			merged.set(key, makeCell(c.reel, c.row, c.count, c.name, true));
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

	const punchCell = async (cell: SplitCell) => {
		await cell.pulse.set(1.16, { duration: fxDur(SLASH.hitMs * 0.35) });
		if (!slashAlive) return;
		await cell.pulse.set(1, { duration: fxDur(SLASH.hitMs * 0.65) });
	};

	const startDrips = (cell: SplitCell) => {
		cell.drips = dripOrigins(cell.reel, cell.row).map((drip) => ({
			...drip,
			fall: new Tween(0),
		}));
		for (const drip of cell.drips) {
			void fxWait(drip.delay).then(() => {
				if (!slashAlive) return;
				void drip.fall.set(1, { duration: fxDur(DRIP_FALL_MS), easing: cubicIn });
			});
		}
	};

	const slashCell = async (cell: SplitCell) => {
		cell.slashPlay.set(0, { duration: 0 });
		cell.marked = false;
		void punchCell(cell);
		void fxWait(SLASH.markMs).then(() => {
			if (!slashAlive) return;
			cell.marked = true;
			cell.split.set(1, { duration: 0 });
			startDrips(cell);
		});
		await cell.slashPlay.set(1, { duration: fxDur(SLASH.stackMs), easing: linear });
		if (!slashAlive) return;
		cell.marked = true;
		cell.split.set(1, { duration: 0 });
		if (!cell.drips.length) startDrips(cell);
	};

	const runSplit = async () => {
		const fresh = cells.filter((cell) => cell.fresh);
		if (!fresh.length) return;
		playThemedOnce('sfx_split', { forcePlay: true });
		void fxWait(SLASH.hitMs).then(() => {
			if (!slashAlive) return;
			playThemedOnce('sfx_split_hit', { forcePlay: true });
			shakeBoard({ intensity: 12, duration: fxDur(170) });
		});
		await Promise.all(fresh.map((cell) => slashCell(cell)));
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
			fallOut.set(0, { duration: 0 });
		},
		splitPanesHide: () => {
			show = false;
			cells = [];
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

	const drawEnergy = (g: import('pixi.js').Graphics, cell: SplitCell) => {
		drawSlashEnergy(g, cell.slashPlay.current * SLASH.stackMs, cell.marked);
	};
</script>

{#snippet splitFace(cell: DrawnCell)}
	{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	{@const split = cell.split.current}
	<Container x={cell.cx} y={cell.cy} scale={cell.pulse.current}>
		<Graphics draw={drawUnderGlow} />
		{#if usesHighPayPlate(cell.name)}
			<HighPayBg reelIndex={cell.reel} />
		{:else if isLowPaySymbol(cell.name)}
			<LowPayBg reelIndex={cell.reel} />
		{/if}
		<Container>
			<CellClipMask reelIndex={cell.reel} openHat={isHigh} />
			<SymbolSprite {symbolInfo} />
		</Container>
		<Container alpha={split}>
			<Graphics draw={(g) => drawFrame(g, isHigh)} />
		</Container>
	</Container>
{/snippet}

{#snippet splitWound(cell: DrawnCell)}
	{@const split = cell.split.current}
	<Container x={cell.cx} y={cell.cy} scale={cell.pulse.current}>
		<Container>
			<CellClipMask reelIndex={cell.reel} />
			<Container rotation={SLASH_ROT}>
				{#if cell.marked}
					<Sprite
						key={GASH_KEY}
						anchor={0.5}
						width={SLASH.seamW * 0.96}
						height={GASH_H}
						alpha={0.92}
						eventMode="none"
					/>
					<Graphics draw={drawSlashLip} eventMode="none" />
				{/if}
				<Graphics
					blendMode="screen"
					draw={(g) => {
						cell.slashPlay.current;
						cell.marked;
						drawEnergy(g, cell);
					}}
					eventMode="none"
				/>
			</Container>
			{#each cell.drips as drip (`${cell.key}-${drip.key}-${drip.x}`)}
				<Sprite
					key={drip.key}
					anchor={{ x: 0.5, y: 0 }}
					x={drip.x}
					y={drip.y0 + drip.fall.current * CARD_H * DRIP_FALL}
					width={drip.w}
					height={drip.h * (0.55 + 0.45 * drip.fall.current)}
					alpha={0.25 + 0.7 * drip.fall.current}
					eventMode="none"
				/>
			{/each}
		</Container>
		{#if cell.count > 1}
			<RedGlowMark
				x={CARD_W / 2 - COUNT_PAD}
				y={CARD_H / 2 - COUNT_PAD}
				anchor={{ x: 1, y: 1 }}
				label={formatWaysMult(cell.count)}
				fontSize={22}
				alpha={split}
			/>
		{/if}
	</Container>
{/snippet}

<!-- MainContainer stays MOUNTED even while hidden: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). Face under fire; slash over fire. -->
<Container zIndex={SPLIT_CELL_Z}>
	<MainContainer>
		{#if show}
			<BoardSpace yOffset={fallOut.current}>
				{#each drawn as cell (cell.key)}
					{@render splitFace(cell)}
				{/each}
			</BoardSpace>
		{/if}
	</MainContainer>
</Container>
<Container zIndex={SPLIT_KNIFE_Z}>
	<MainContainer>
		{#if show}
			<BoardSpace yOffset={fallOut.current}>
				{#each drawn as cell (cell.key)}
					{@render splitWound(cell)}
				{/each}
			</BoardSpace>
		{/if}
	</MainContainer>
</Container>
