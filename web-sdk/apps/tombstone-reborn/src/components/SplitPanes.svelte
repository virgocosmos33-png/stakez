<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// Come in → thunk + hold → drag out the right frame. Thin cut follows the
	// live tip. Kenney blood stains clip to the iron cell frame. Clip the
	// knife on the right frame only.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import 'pixi.js/advanced-blend-modes';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut, quartIn, quartOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle, Sprite } from 'pixi-svelte';
	import { playThemedOnce } from '../game/sfxTheme';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import { isNudgeCoveredReel, isVisibleBoardCell } from '../game/boardCells';
	import {
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
		HIGH_SYMBOLS,
		SPLIT_KNIFE_Z,
	} from '../game/constants';
	import { shakeBoard } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX } from '../game/tombstoneVfx';
	import { formatWaysMult } from '../game/waysFormat';
	import {
		BLOOD_SPLASH_IN_MS,
		BLOOD_SPLASH_OUT_MS,
		BLOOD_STAIN_RESIDUAL,
		CELL_FRAME_MASK_H,
		CELL_FRAME_MASK_KEY,
		CELL_FRAME_MASK_W,
		CRUSH_IN_MS,
		CRUSH_OUT_MS,
		frameBloodLayers,
		planKnifeRhythm,
		volleySeed,
		type WoundLayer,
	} from '../game/gunsmokeSpin';
	import RedGlowMark from './RedGlowMark.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	const MAX_PANES = 4;
	const COUNT_LABEL_MIN = 6;
	const COUNT_PAD = 8;
	/** Cropped fist+blade (660×1101). Tip is the bottom-left point of the PNG. */
	const KNIFE_ASPECT = 660 / 1101;
	const KNIFE_H = CARD_H * 0.95;
	const KNIFE_W = KNIFE_H * KNIFE_ASPECT;
	const KNIFE_TIP = { x: 22 / 660, y: 1100 / 1101 };
	/** PNG blade, handle → tip. Stills never go to straight-down 90°. */
	const NATIVE_BLADE = 1.8893158349070782;
	/** Still 1: ~149°, in from the top-right. */
	const KNIFE_IN = 2.601 - NATIVE_BLADE;
	/** Stills 2–3: ~122°, fist on the right, tip low-left. */
	const KNIFE_STAB = 2.13 - NATIVE_BLADE;
	/** Still 4: ~114°, sliding out the right frame. */
	const KNIFE_OUT = 1.99 - NATIVE_BLADE;
	/** Impact curve: slam in, dead stop, yank out. */
	const IN_MS = 70;
	const THUNK_HOLD_MS = 70;
	const DRAG_OUT_MS = 130;
	const KNIFE_FADE_MS = 40;
	const PANE_MS = 130;
	const SLASH_MS = 130;

	type Pose = { x: number; y: number; rot: number };

	/** Tip in cell UV (0–1), measured on the red-bordered stills. */
	const cellUv = (u: number, v: number, rot: number): Pose => ({
		x: (u - 0.5) * CARD_W,
		y: (v - 0.5) * CARD_H,
		rot,
	});

	const STAB_POSES = {
		peek: cellUv(0.55, 0.08, KNIFE_IN),
		thunk: cellUv(0.382, 0.85, KNIFE_STAB),
		out: cellUv(0.897, 0.959, KNIFE_OUT),
	};

	/** Wound rides thunk → out, the same path the tip drags. */
	const PATH_ORIGIN = STAB_POSES.thunk;
	const PATH_EXIT = STAB_POSES.out;
	const PATH_SPAN_X = PATH_EXIT.x - PATH_ORIGIN.x;
	const PATH_SPAN_Y = PATH_EXIT.y - PATH_ORIGIN.y;
	const CUT_LINE_H = 5;
	const CUT_SMEAR_H = 7;

	const alongKnifePath = (u: number) => ({
		x: PATH_ORIGIN.x + PATH_SPAN_X * u,
		y: PATH_ORIGIN.y + PATH_SPAN_Y * u,
	});

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
		split: Tween<number>;
		pulse: Tween<number>;
		crush: Tween<number>;
		slash: Tween<number>;
		splash: Tween<number>;
		frames: WoundLayer[];
	};
	type DrawnCell = SplitCell & { name: SymbolName };
	type Stab = {
		key: string;
		x: Tween<number>;
		y: Tween<number>;
		rot: Tween<number>;
		alpha: Tween<number>;
	};

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	let stab = $state<Stab | null>(null);
	const fallOut = new Tween(0);

	const makeCell = (
		reel: number,
		row: number,
		count: number,
		pinned: SymbolName | undefined,
		fresh: boolean,
	): SplitCell => {
		const seed = reel * 31 + row * 7 + count * 113;
		return {
			key: `${reel}-${row}`,
			reel,
			row,
			count,
			pinned,
			cx: getSymbolX(reel),
			cy: getCellCenterY(reel, row),
			seed,
			fresh,
			split: new Tween(fresh ? 0 : 1),
			pulse: new Tween(1),
			crush: new Tween(0),
			slash: new Tween(fresh ? 0 : 1),
			splash: new Tween(fresh ? 0 : BLOOD_STAIN_RESIDUAL),
			frames: fresh ? [] : frameBloodLayers(reel, row, count),
		};
	};

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

	const liveStab = $derived.by(() => {
		const shot = stab;
		if (!shot) return null;
		const cell = cells.find((item) => item.key === shot.key);
		if (!cell) return null;
		return {
			key: shot.key,
			cx: getSymbolX(cell.reel),
			cy: getCellCenterY(cell.reel, cell.row),
			x: shot.x.current,
			y: shot.y.current,
			rot: shot.rot.current,
			alpha: shot.alpha.current,
		};
	});

	const knifeTipOnCell = (cell: SplitCell) => {
		if (liveStab && liveStab.key === cell.key && cell.slash.current > 0.001) {
			return { x: liveStab.x, y: liveStab.y };
		}
		return alongKnifePath(Math.max(0, Math.min(1, cell.slash.current)));
	};

	const knifeTrail = (cell: SplitCell) => {
		const tip = knifeTipOnCell(cell);
		const w = Math.hypot(tip.x - PATH_ORIGIN.x, tip.y - PATH_ORIGIN.y);
		if (w < 2) return null;
		return {
			x: (PATH_ORIGIN.x + tip.x) / 2,
			y: (PATH_ORIGIN.y + tip.y) / 2,
			w,
			rot: Math.atan2(tip.y - PATH_ORIGIN.y, tip.x - PATH_ORIGIN.x),
		};
	};

	const stainFrame = (cell: SplitCell) => {
		cell.frames = frameBloodLayers(cell.reel, cell.row, cell.count);
		void cell.splash.set(1, { duration: fxDur(BLOOD_SPLASH_IN_MS), easing: backOut }).then(() => {
			void cell.splash.set(BLOOD_STAIN_RESIDUAL, {
				duration: fxDur(BLOOD_SPLASH_OUT_MS),
				easing: cubicOut,
			});
		});
	};

	const moveStab = (shot: Stab, pose: Pose, duration: number, easing: (t: number) => number) =>
		Promise.all([
			shot.x.set(pose.x, { duration, easing }),
			shot.y.set(pose.y, { duration, easing }),
			shot.rot.set(pose.rot, { duration, easing }),
		]);

	const stabCell = async (cell: SplitCell, flightScale: number) => {
		const poses = STAB_POSES;
		const shot: Stab = {
			key: cell.key,
			x: new Tween(poses.peek.x),
			y: new Tween(poses.peek.y),
			rot: new Tween(poses.peek.rot),
			alpha: new Tween(1),
		};
		stab = shot;
		await moveStab(shot, poses.thunk, fxDur(IN_MS * flightScale), quartOut);
		playThemedOnce('sfx_split_thunk', { forcePlay: true });
		shakeBoard({
			intensity: 10,
			duration: fxDur(140),
		});
		void cell.crush.set(1, { duration: fxDur(CRUSH_IN_MS), easing: backOut }).then(() => {
			void cell.crush.set(0, { duration: fxDur(CRUSH_OUT_MS), easing: cubicOut });
		});
		cell.pulse.set(1.16, { duration: 0 });
		void cell.pulse.set(1, { duration: fxDur(260), easing: backOut });
		stainFrame(cell);
		await fxWait(THUNK_HOLD_MS);
		playThemedOnce('sfx_split_seam_tear', { forcePlay: true });
		void cell.split.set(1, { duration: fxDur(PANE_MS), easing: backOut });
		await Promise.all([
			moveStab(shot, poses.out, fxDur(DRAG_OUT_MS), quartIn),
			cell.slash.set(1, { duration: fxDur(SLASH_MS), easing: quartIn }),
		]);
		await shot.alpha.set(0, { duration: fxDur(KNIFE_FADE_MS), easing: cubicOut });
		if (stab?.key === cell.key) stab = null;
	};

	const runSplit = async () => {
		const fresh = cells.filter((cell) => cell.fresh);
		if (!fresh.length) return;
		const rhythm = planKnifeRhythm(fresh.length, volleySeed(fresh));
		for (let i = 0; i < fresh.length; i += 1) {
			const cell = fresh[i];
			if (!cell) continue;
			const shot = rhythm[i];
			if (i === 0) playThemedOnce('sfx_split');
			await stabCell(cell, shot?.flightScale ?? 1);
			if ((shot?.beatMs ?? 0) > 0) await fxWait(shot.beatMs);
		}
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
			stab = null;
			fallOut.set(0, { duration: 0 });
		},
		splitPanesHide: () => {
			show = false;
			cells = [];
			stab = null;
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

	const drawKnifeMask = (g: import('pixi.js').Graphics) => {
		const right = CARD_W / 2;
		g.rect(-CARD_W * 5, -CARD_H * 5, CARD_W * 5 + right, CARD_H * 10);
		g.fill({ color: 0xffffff });
	};

</script>

{#snippet splitCell(cell: DrawnCell)}
	{@const panes = cell.count >= COUNT_LABEL_MIN ? 1 : Math.min(cell.count, MAX_PANES)}
	{@const sliceHeight = CARD_H / panes}
	{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	{@const split = cell.split.current}
	{@const slim = Math.min(1, 3 / panes)}
	{@const gap = CARD_H * Math.min(0.03, 0.1 / panes)}
	{@const paneHeight = Math.max((sliceHeight - gap) * split + CARD_H * (1 - split), 2)}
	{@const crushX = 1 + 0.08 * cell.crush.current}
	{@const crushY = 1 - 0.14 * cell.crush.current}
	<Container x={cell.cx} y={cell.cy} scale={{ x: cell.pulse.current * crushX, y: cell.pulse.current * crushY }}>
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
		{#if cell.frames.length}
			<Container>
				<Sprite
					isMask
					key={CELL_FRAME_MASK_KEY}
					anchor={0.5}
					width={CELL_FRAME_MASK_W}
					height={CELL_FRAME_MASK_H}
					renderable={false}
					eventMode="none"
				/>
				{#each cell.frames as layer, i (`${cell.key}-frame-${i}`)}
					<Sprite
						key={layer.key}
						x={layer.x}
						y={layer.y}
						anchor={0.5}
						width={layer.width}
						height={layer.height}
						rotation={layer.rotation}
						alpha={layer.alpha * cell.splash.current}
						eventMode="none"
					/>
				{/each}
			</Container>
		{/if}
		{@const trail = knifeTrail(cell)}
		{#if trail}
				<Sprite
					key="splitCutScratch"
					x={trail.x}
					y={trail.y}
					anchor={0.5}
					width={trail.w}
					height={CUT_LINE_H}
					rotation={trail.rot}
					alpha={0.9}
					blendMode="linear-burn"
					eventMode="none"
				/>
				<Sprite
					key="splitCutSmear"
					x={trail.x}
					y={trail.y}
					anchor={0.5}
					width={trail.w}
					height={CUT_SMEAR_H}
					rotation={trail.rot}
					alpha={0.72}
					blendMode="linear-burn"
					eventMode="none"
				/>
		{/if}
		{#if cell.count >= COUNT_LABEL_MIN}
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
	(see .cursor/skills/pixi-svelte-layering). -->
<Container zIndex={SPLIT_KNIFE_Z}>
<MainContainer>
	{#if show}
		<BoardSpace yOffset={fallOut.current}>
			{#each drawn as cell (cell.key)}
				{@render splitCell(cell)}
			{/each}
			{#if liveStab}
				<Container x={liveStab.cx} y={liveStab.cy}>
					<Graphics isMask draw={drawKnifeMask} />
					<Sprite
						key="splitHandKnife"
						x={liveStab.x}
						y={liveStab.y}
						anchor={KNIFE_TIP}
						width={KNIFE_W}
						height={KNIFE_H}
						rotation={liveStab.rot}
						alpha={liveStab.alpha}
						eventMode="none"
					/>
				</Container>
			{/if}
		</BoardSpace>
	{/if}
</MainContainer>
</Container>
