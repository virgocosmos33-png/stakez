<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// Beat 1: slide in, hold stabbed. Beat 2: drag through the wound (the cut).
	// Tip stays in the hole during the drag. Do not wipe the sprite from either end.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import 'pixi.js/advanced-blend-modes';
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut, expoIn, linear } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle, Sprite } from 'pixi-svelte';
	import { playThemedOnce } from '../game/sfxTheme';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { fxRandom } from '../game/featureVfx';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import { isNudgeCoveredReel, isVisibleBoardCell } from '../game/boardCells';
	import {
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
		HIGH_SYMBOLS,
		SPLIT_KNIFE_Z,
	} from '../game/constants';
	import { SPLIT_AXE, SPLIT_AXE_H, SPLIT_AXE_W } from '../game/splitAxe';
	import { shakeBoard } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX } from '../game/tombstoneVfx';
	import { formatWaysMult } from '../game/waysFormat';
	import { CRUSH_IN_MS, CRUSH_OUT_MS, planKnifeRhythm, volleySeed } from '../game/gunsmokeSpin';
	import RedGlowMark from './RedGlowMark.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	const MAX_PANES = 4;
	const COUNT_LABEL_MIN = 6;
	const COUNT_PAD = 8;
	/** User axe split.png (1536×1024). Tip is the left bit. */
	const KNIFE_H = SPLIT_AXE_H;
	const KNIFE_W = SPLIT_AXE_W;
	const KNIFE_TIP = SPLIT_AXE.tip;
	/** PNG blade, pommel → tip. */
	const NATIVE_BLADE = SPLIT_AXE.nativeBlade;
	/** Approach ~122°. */
	const KNIFE_APPROACH = 2.13 - NATIVE_BLADE;
	/** Thunk lands almost 90° (tip down). */
	const KNIFE_STAB = Math.PI / 2 + 0.06 - NATIVE_BLADE;
	/** Cut-drag tilts off vertical as it rips. */
	const KNIFE_OUT = 1.92 - NATIVE_BLADE;
	/** Tip → pommel in the displayed sprite (unrotated). */
	const HANDLE_LOCAL = {
		x: (SPLIT_AXE.knob.x - KNIFE_TIP.x) * KNIFE_W,
		y: (SPLIT_AXE.knob.y - KNIFE_TIP.y) * KNIFE_H,
	};
	const rotateLocal = (rot: number) => {
		const c = Math.cos(rot);
		const s = Math.sin(rot);
		return {
			x: HANDLE_LOCAL.x * c - HANDLE_LOCAL.y * s,
			y: HANDLE_LOCAL.x * s + HANDLE_LOCAL.y * c,
		};
	};
	const BEAT_MS = 220;
	const THUNK_HOLD_MS = 500;
	const KNIFE_FADE_MS = 40;
	const BLOOD = 0xc40812;
	const TIP_WOUND_W = CARD_W * 0.16;
	const TIP_WOUND_H = TIP_WOUND_W * (216 / 1024) * 1.2;
	const OPEN_WOUND_W = CARD_W * 0.92;
	const OPEN_WOUND_H = CARD_H * 0.11;

	type Pose = { x: number; y: number; rot: number };

	/** Tip in cell UV (0–1), measured on the red-bordered stills. */
	const cellUv = (u: number, v: number, rot: number): Pose => ({
		x: (u - 0.5) * CARD_W,
		y: (v - 0.5) * CARD_H,
		rot,
	});

	/** Tip well past the hole so the guard sits in the face, not on the hat brim. */
	const THUNK = cellUv(0.46, 1.24, KNIFE_STAB);
	/** Horizontal gash on the face. Tip is the lowest point, so this hides the tip first. */
	const WOUND_Y = (0.66 - 0.5) * CARD_H;
	/** Blade keeps going past the lip so it sits in the blood, not above it. */
	const KNIFE_IN_HOLE = CARD_H * 0.055;
	/** Knife visible above the gash. Stable fns so Pixi does not clear the mask every frame. */
	const drawKnifeHoleMask = (g: import('pixi.js').Graphics) => {
		const top = -CARD_H * 3;
		const cut = WOUND_Y + KNIFE_IN_HOLE;
		g.rect(-CARD_W * 2.5, top, CARD_W * 5, cut - top);
		g.fill({ color: 0xffffff });
	};
	const drawKnifeOpenMask = (g: import('pixi.js').Graphics) => {
		g.rect(-CARD_W * 3, -CARD_H * 3, CARD_W * 6, CARD_H * 6);
		g.fill({ color: 0xffffff });
	};
	const handleAtApproach = rotateLocal(KNIFE_APPROACH);
	const handleLen = Math.hypot(handleAtApproach.x, handleAtApproach.y) || 1;
	/** Tip starts above the card and slams down into the thunk. */
	const SLIDE_IN = CARD_H * 0.95;
	const STAB_POSES = {
		start: {
			x: THUNK.x + (handleAtApproach.x / handleLen) * SLIDE_IN,
			y: THUNK.y + (handleAtApproach.y / handleLen) * SLIDE_IN,
			rot: KNIFE_APPROACH,
		},
		thunk: THUNK,
		out: cellUv(1.08, 1.22, KNIFE_OUT),
	};

	const punchBoard = (cell: SplitCell) => {
		shakeBoard({
			intensity: 14,
			duration: fxDur(160),
		});
		void cell.crush.set(1, { duration: fxDur(CRUSH_IN_MS), easing: backOut }).then(() => {
			void cell.crush.set(0, { duration: fxDur(CRUSH_OUT_MS), easing: cubicOut });
		});
		cell.pulse.set(1.16, { duration: 0 });
		void cell.pulse.set(1, { duration: fxDur(260), easing: backOut });
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

	type WoundDrip = {
		key: string;
		x: number;
		y0: number;
		r0: number;
		travel: number;
		stretch: number;
		wobble: number;
		phase: number;
		life: Tween<number>;
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
		split: Tween<number>;
		pulse: Tween<number>;
		crush: Tween<number>;
		slash: Tween<number>;
		woundBorn: number;
		hole: boolean;
		bleed: boolean;
		dripSeq: number;
		drips: WoundDrip[];
	};
	type DrawnCell = SplitCell & { name: SymbolName };
	type Stab = {
		key: string;
		x: Tween<number>;
		y: Tween<number>;
		rot: Tween<number>;
		alpha: Tween<number>;
		cut: boolean;
	};

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	let stab = $state<Stab | null>(null);
	let knifeAlive = true;
	const fallOut = new Tween(0);

	onDestroy(() => {
		knifeAlive = false;
	});

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
			woundBorn: fresh ? 0 : 1,
			hole: false,
			bleed: false,
			dripSeq: 0,
			drips: [],
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

	const bladeCells = $derived(
		drawn.filter((cell) => cell.hole || stab?.key === cell.key),
	);

	const woundLine = (cell: SplitCell) => {
		const open = cell.slash.current;
		const trail = knifeTrail(cell);
		if (trail && open > 0.001) {
			return {
				x: trail.x,
				y: WOUND_Y,
				w: Math.max(TIP_WOUND_W, trail.w),
				h: TIP_WOUND_H + (OPEN_WOUND_H - TIP_WOUND_H) * open,
			};
		}
		return { x: 0, y: WOUND_Y, w: TIP_WOUND_W, h: TIP_WOUND_H };
	};

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

	/** One teardrop path: neck blends into the bulb. No stem-plus-circle. */
	const drawBloodDrip = (g: import('pixi.js').Graphics, drip: WoundDrip) => {
		const t = drip.life.current;
		if (t <= 0) return;
		const hang = Math.min(1, t / 0.22);
		const fallT = Math.max(0, (t - 0.22) / 0.78);
		const fall = fallT * fallT;
		const fade = t > 0.82 ? 1 - (t - 0.82) / 0.18 : 1;
		const neck = 1.1 + drip.r0 * (0.18 + hang * 0.1);
		const bulb = drip.r0 * (0.55 + hang * 0.35);
		const len = drip.r0 * 2.2 * (0.55 + hang * 0.45) + fall * drip.travel;
		const tipY = drip.y0 + len;
		const midY = drip.y0 + len * 0.52;
		const wave = Math.sin(len * 0.11 + drip.phase) * drip.wobble * (0.25 + fall * 0.75);
		const left = drip.x - neck + wave * 0.35;
		const right = drip.x + neck + wave * 0.15;
		const tipX = drip.x + wave;
		g.moveTo(left, drip.y0);
		g.bezierCurveTo(left + wave * 0.2, midY - len * 0.08, tipX - bulb, midY + len * 0.12, tipX - bulb * 0.2, tipY);
		g.quadraticCurveTo(tipX, tipY + bulb * 0.55, tipX + bulb * 0.2, tipY);
		g.bezierCurveTo(tipX + bulb, midY + len * 0.12, right + wave * 0.1, midY - len * 0.08, right, drip.y0);
		g.closePath();
		g.fill({ color: BLOOD, alpha: fade * 0.92 });
		g.moveTo(drip.x - neck * 0.45, drip.y0 + 1);
		g.bezierCurveTo(
			drip.x - neck * 0.2,
			midY,
			tipX - bulb * 0.35,
			midY + len * 0.08,
			tipX,
			tipY - bulb * 0.15,
		);
		g.bezierCurveTo(
			tipX + bulb * 0.35,
			midY + len * 0.08,
			drip.x + neck * 0.2,
			midY,
			drip.x + neck * 0.45,
			drip.y0 + 1,
		);
		g.closePath();
		g.fill({ color: 0x8a0a10, alpha: fade * 0.35 });
	};

	/** Small wet blotch on the lip so the drip tops are not a ruler line. */
	const drawWoundLipSplash = (
		g: import('pixi.js').Graphics,
		line: { x: number; y: number; w: number },
		seed: number,
	) => {
		const w = Math.max(TIP_WOUND_W, line.w * 0.38);
		const cx = line.x;
		const cy = line.y + 1;
		g.ellipse(cx, cy + 2.2, w * 0.4, 5.2);
		g.fill({ color: BLOOD, alpha: 0.86 });
		g.ellipse(cx, cy + 2.6, w * 0.22, 2.4);
		g.fill({ color: 0x8a0a10, alpha: 0.28 });
		for (let i = 0; i < 5; i += 1) {
			const u = (i + 0.5) / 5 - 0.5;
			const rx = 2.8 + fxRandom(seed + i * 3) * 2.2;
			const ry = 2.1 + fxRandom(seed + i * 5) * 2.0;
			g.ellipse(cx + u * w * 0.88, cy + 1.2 + fxRandom(seed + i * 7) * 2.4, rx, ry);
			g.fill({ color: BLOOD, alpha: 0.8 });
		}
		for (let i = 0; i < 3; i += 1) {
			const u = (fxRandom(seed + 40 + i) - 0.5) * 0.5;
			const r = 1.05 + fxRandom(seed + 50 + i) * 1.25;
			g.circle(cx + u * w, cy - 1.2 - fxRandom(seed + 60 + i) * 2.0, r);
			g.fill({ color: BLOOD, alpha: 0.72 });
		}
	};

	const spawnDrip = (cell: SplitCell, along: number) => {
		if (cell.drips.length >= 18) return;
		const line = woundLine(cell);
		const seq = cell.dripSeq;
		cell.dripSeq += 1;
		const short = seq % 3 === 0;
		const drip: WoundDrip = {
			key: `${cell.key}-drip-${seq}`,
			x: line.x + (along - 0.5) * Math.max(line.w, TIP_WOUND_W),
			y0: line.y,
			r0: 2 + fxRandom(cell.seed + seq * 3) * 2.6,
			travel: CARD_H * (short ? 0.18 + fxRandom(cell.seed + seq) * 0.12 : 0.4 + fxRandom(cell.seed + seq * 5) * 0.22),
			stretch: 1.3 + fxRandom(cell.seed + seq * 7) * 1.7,
			wobble: 1.1 + fxRandom(cell.seed + seq * 11) * 2.4,
			phase: fxRandom(cell.seed + seq * 13) * Math.PI * 2,
			life: new Tween(0),
		};
		cell.drips = [...cell.drips, drip];
		void drip.life.set(1, { duration: fxDur(640 + (seq % 5) * 90), easing: linear }).then(() => {
			if (!knifeAlive) return;
			cell.drips = cell.drips.filter((item) => item.key !== drip.key);
		});
	};

	const startBleed = (cell: SplitCell) => {
		if (cell.bleed) return;
		cell.bleed = true;
		cell.woundBorn = performance.now();
		const first = [0.08, 0.26, 0.44, 0.62, 0.8, 0.94];
		for (let i = 0; i < first.length; i += 1) {
			const along = Math.min(1, Math.max(0, first[i] + (fxRandom(cell.seed + i * 19) - 0.5) * 0.08));
			void fxWait(12 + i * 36).then(() => {
				if (!knifeAlive || !cell.bleed) return;
				spawnDrip(cell, along);
			});
		}
		void (async () => {
			while (knifeAlive && cell.bleed && show) {
				await fxWait(160 + fxRandom(cell.seed + cell.dripSeq * 23) * 220);
				if (!knifeAlive || !cell.bleed || !show) return;
				const n = 2 + Math.floor(fxRandom(cell.seed + cell.dripSeq * 29) * 3);
				for (let i = 0; i < n; i += 1) {
					spawnDrip(cell, fxRandom(cell.seed + cell.dripSeq * 31 + i * 7));
				}
			}
		})();
	};

	const moveStab = (shot: Stab, pose: Pose, duration: number, easing: (t: number) => number) =>
		Promise.all([
			shot.x.set(pose.x, { duration, easing }),
			shot.y.set(pose.y, { duration, easing }),
			shot.rot.set(pose.rot, { duration, easing }),
		]);

	const stabCell = async (cell: SplitCell, flightScale: number) => {
		const poses = STAB_POSES;
		const beatMs = fxDur(BEAT_MS);
		const shot: Stab = {
			key: cell.key,
			x: new Tween(poses.start.x),
			y: new Tween(poses.start.y),
			rot: new Tween(poses.start.rot),
			alpha: new Tween(1),
			cut: true,
		};
		stab = shot;
		cell.hole = true;
		await moveStab(shot, poses.thunk, beatMs, expoIn);
		playThemedOnce('sfx_split_thunk', { forcePlay: true });
		punchBoard(cell);
		startBleed(cell);
		await fxWait(THUNK_HOLD_MS);
		await Promise.all([
			moveStab(shot, poses.out, beatMs, expoIn),
			cell.slash.set(1, { duration: beatMs, easing: expoIn }),
			cell.split.set(1, { duration: beatMs, easing: expoIn }),
		]);
		playThemedOnce('sfx_split_drag', { forcePlay: true });
		punchBoard(cell);
		await shot.alpha.set(0, { duration: fxDur(KNIFE_FADE_MS), easing: cubicOut });
		cell.hole = false;
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
			for (const cell of cells) cell.bleed = false;
			await fallOutFeatureFx(fallOut, show && cells.length > 0);
			show = false;
			cells = [];
			stab = null;
			fallOut.set(0, { duration: 0 });
		},
		splitPanesHide: () => {
			for (const cell of cells) cell.bleed = false;
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
			{#each bladeCells as cell (cell.key + '-blade')}
				<Container x={cell.cx} y={cell.cy}>
					<Graphics isMask draw={cell.hole ? drawKnifeHoleMask : drawKnifeOpenMask} />
					{#if liveStab && liveStab.key === cell.key}
						<Sprite
							key="splitHandAxe"
							x={liveStab.x}
							y={liveStab.y}
							anchor={KNIFE_TIP}
							width={KNIFE_W}
							height={KNIFE_H}
							rotation={liveStab.rot}
							alpha={liveStab.alpha}
							tint={SPLIT_AXE.tint}
							eventMode="none"
						/>
					{/if}
				</Container>
			{/each}
			{#each drawn as cell (cell.key + '-wound')}
				{#if cell.woundBorn > 0}
					<Container x={cell.cx} y={cell.cy}>
						<Rectangle isMask anchor={0.5} width={CARD_W} height={CARD_H} backgroundColor={0xffffff} />
						{@const line = woundLine(cell)}
						<Sprite
							key="splitBloodGash"
							x={line.x}
							y={line.y}
							anchor={{ x: 0.5, y: 0.22 }}
							width={line.w}
							height={line.h}
							alpha={0.96}
							eventMode="none"
						/>
						{#each cell.drips as drip (drip.key)}
							<Graphics
								draw={(g) => {
									drip.life.current;
									drawBloodDrip(g, drip);
								}}
								eventMode="none"
							/>
						{/each}
						<Graphics
							draw={(g) => drawWoundLipSplash(g, line, cell.seed)}
							eventMode="none"
						/>
					</Container>
				{/if}
			{/each}
		</BoardSpace>
	{/if}
</MainContainer>
</Container>
