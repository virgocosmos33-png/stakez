<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// SPLIT: the winning symbol is sliced into N center-cropped vertical panes that
	// snap apart along powder-burn / brass-wire seams (Tombstone western), with
	// a slim-seam "XN" badge.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle, Text } from 'pixi-svelte';

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
		type HoleMark,
		SHOT_GAP_MS,
		RICOCHET_CHANCE,
		holePose,
		shotsForMultiplier,
	} from '../game/splitBullets';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX, VFX, drawPowderSeam } from '../game/tombstoneVfx';
	import SymbolSprite from './SymbolSprite.svelte';
	import BulletHoleMark from './BulletHoleMark.svelte';
	import TombstoneFxSprite from './TombstoneFxSprite.svelte';

	const context = getContext();

	const BLOOD = TOMBSTONE_FX.bloodRust;
	const DARK = TOMBSTONE_FX.dark;

	type SplitCell = {
		key: string;
		reel: number;
		row: number;
		count: number;
		/** only set when the caller names the symbol explicitly; otherwise the
			cell follows whatever the board is currently showing there */
		pinned?: SymbolName;
		cx: number;
		cy: number;
		seed: number;
		/** true only while this cell is part of the currently-playing strike;
			persisted cells from earlier events stay settled and untouched */
		fresh: boolean;
	};
	type DrawnCell = SplitCell & { name: SymbolName };

	let cells = $state<SplitCell[]>([]);
	let show = $state(false);
	let time = $state(0);
	/** wall clock for muzzle flashes on stamped holes */
	let nowMs = $state(performance.now());
	/** stamped bullet holes that stay on their cells until fall-out */
	let holeMarks = $state<HoleMark[]>([]);
	// rides the panes off the bottom edge when the next spin starts
	const fallOut = new Tween(0);

	// 0 = whole symbol, 1 = fully split into panes
	const splitProgress = new Tween(1);
	// blade head sweeps top -> bottom carving the seams
	const cutSweep = new Tween(0);
	const seamFlare = new Tween(0);
	const detonation = new Tween(0);
	const pulse = new Tween(1);

	const playShotSfx = (seed: number) => {
		// forcePlay: stacked volleys must not get swallowed by the once-player
		context.eventEmitter.broadcast({
			type: 'soundOnce',
			name: 'sfx_bullet_wood',
			forcePlay: true,
		});
		// ~38% of hits get a ricochet; seed keeps it stable per shot
		const ricochetRoll = Math.sin(seed * 91.7 + 12.3) * 0.5 + 0.5;
		if (ricochetRoll < RICOCHET_CHANCE) {
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_bullet_ricochet',
				forcePlay: true,
			});
		}
	};

	/** Stamp one hole on a cell (SFX is fired once per volley, not per cell). */
	const stampHole = (cell: SplitCell, shotIndex: number) => {
		const pose = holePose(cell.seed, shotIndex, CARD_W, CARD_H);
		const born = performance.now();
		holeMarks = [
			...holeMarks,
			{
				id: `${cell.key}-${shotIndex}-${born}`,
				cellKey: cell.key,
				x: pose.x,
				y: pose.y,
				tex: pose.tex,
				scale: pose.scale,
				rot: pose.rot,
				born,
			},
		];
	};

	// Every split cell gets the SAME treatment no matter its size: panes plus an
	// exact "Nx" stamp. The pane count is only a visual — past this many the
	// slices get too thin to read, so the geometry caps and the stamp carries
	// the real number. (It used to be three different looks: real panes below 5,
	// an untouched symbol at 5+, and a number only above 8 — which read as three
	// unrelated features.)
	const MAX_PANES = 4;

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	/**
	 * MERGE the incoming split cells into whatever is already up.
	 *
	 * A spin can fire several feature events back to back (split, clone, split
	 * again — see combo_features_book). The panes are supposed to stay on their
	 * cells until the next reveal, but replacing `cells` wholesale here meant
	 * every later `splitPanesShow` wiped the earlier cells' panes — and a split
	 * that only hit wild-column cells (all filtered out) cleared the entire
	 * overlay. Cells already up keep their panes; a cell named again gets its
	 * new count and re-animates.
	 *
	 * Returns true when at least one cell is new or changed, i.e. there is
	 * something for the bullet strike to play on.
	 */
	const layout = (incoming: { reel: number; row: number; count: number; name?: SymbolName }[]) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		// reels shown as a full wild column (Wild Reel or Stretch) swallow the split:
		// the extra ways still count, but we never paint panes over the wild column.
		const wildReels = new Set([
			...context.stateGame.wildReelReels,
			...context.stateGame.stretchedReels,
		]);
		// carry surviving cells over settled, refreshing their centres — features
		// that ran since their split (wild reel, stretch) can shift reel offsets
		const merged = new Map<string, SplitCell>(
			cells
				.filter((cell) => !wildReels.has(cell.reel))
				.map((cell) => [
					cell.key,
					{
						...cell,
						fresh: false,
						cx: originX + getSymbolX(cell.reel),
						cy: originY + getCellCenterY(cell.reel, cell.row),
					},
				]),
		);
		let anyFresh = false;
		for (const c of incoming) {
			if (c.count <= 1 || wildReels.has(c.reel)) continue;
			// pad / OOB rows sit in empty diamond gaps — never tear those
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
				cx: originX + getSymbolX(c.reel),
				cy: originY + getCellCenterY(c.reel, c.row),
				seed: c.reel * 31 + c.row * 7 + c.count * 113,
				fresh: true,
			});
		}
		cells = [...merged.values()];
		show = cells.length > 0;
		return anyFresh;
	};

	/**
	 * The symbol each split cell is CURRENTLY showing, re-read every frame.
	 *
	 * The panes stay up until the next reveal, so a later feature on the same
	 * cell can move the board out from under them. Holding the name from layout
	 * time meant a CLONE morphing a split cell left the old symbol painted over
	 * the new premium, since this overlay mounts above the board.
	 */
	const drawn = $derived(
		cells
			.map((cell) => ({
				...cell,
				// position re-solved LIVE too: a STRETCH racking this reel after the
				// split moves every row, and the panes must ride along
				cy:
					context.stateGameDerived.boardLayout().y -
					context.stateGameDerived.boardLayout().height * 0.5 +
					getCellCenterY(cell.reel, cell.row),
				name:
					cell.pinned ??
					(context.stateGame.board[cell.reel]?.reelState.symbols[cell.row]?.rawSymbol
						.name as SymbolName | undefined),
			}))
			.filter((cell): cell is DrawnCell => cell.name != null),
	);

	// BULLET STRIKE: each fresh cell takes 1–4 rounds (scaled by its multiplier).
	// Volleys fire across the board so a big multi gets more holes before the
	// panes peel. Wood hit every shot; ricochet sometimes. Impact (panes apart)
	// lands after the first volley so later rounds punch into the opening card.
	const runSplit = async () => {
		splitProgress.set(0, { duration: 0 });
		cutSweep.set(0, { duration: 0 });
		seamFlare.set(0, { duration: 0 });
		detonation.set(0, { duration: 0 });
		pulse.set(1.32, { duration: 0 });
		const fresh = cells.filter((c) => c.fresh);
		// drop prior marks on cells that are re-striking this event
		const freshKeys = new Set(fresh.map((c) => c.key));
		holeMarks = holeMarks.filter((m) => !freshKeys.has(m.cellKey));

		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });

		const maxShots = Math.max(1, ...fresh.map((c) => shotsForMultiplier(c.count)));
		const swipeMs = fxDur(SHOT_GAP_MS * maxShots + 180);
		cutSweep.set(1, { duration: swipeMs * 0.85, easing: cubicIn });

		let settle: Promise<unknown> = Promise.resolve();
		let opened = false;
		const openPanes = () => {
			if (opened) return;
			opened = true;
			// wood crack / dust settle — not old-game mirror combine + wild explode
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_bullet_wood',
				forcePlay: true,
			});
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: 'sfx_bullet_ricochet',
				forcePlay: true,
			});
			seamFlare.set(1, { duration: fxDur(20) });
			seamFlare.set(0, { duration: fxDur(160) });
			shakeBoard({
				intensity: Math.min(10 + fresh.length * 2.5, 18),
				duration: fxDur(240),
			});
			const fx = detonation.set(1, { duration: fxDur(320), easing: cubicOut });
			const punch = pulse.set(1, { duration: fxDur(420), easing: backOut });
			const apart = splitProgress.set(1, { duration: fxDur(150), easing: backOut });
			settle = Promise.all([fx, punch, apart]);
		};

		for (let shot = 0; shot < maxShots; shot++) {
			let stamped = 0;
			for (const cell of fresh) {
				if (shot >= shotsForMultiplier(cell.count)) continue;
				stampHole(cell, shot);
				stamped += 1;
			}
			if (stamped > 0) playShotSfx(shot * 17 + stamped);
			if (shot === 0) openPanes();
			if (shot < maxShots - 1) await fxWait(SHOT_GAP_MS);
		}
		await settle;
	};

	context.eventEmitter.subscribeOnMount({
		splitPanesShow: async ({ cells: incoming }) => {
			const anyFresh = layout(incoming);
			// nothing new to strike (e.g. the split only hit wild columns):
			// leave the surviving panes exactly as they are
			if (!anyFresh || !cells.length) return;
			await runSplit();
			// strike done: the fresh cells settle in with the persisted ones
			cells = cells.map((cell) => (cell.fresh ? { ...cell, fresh: false } : cell));
		},
		// the next spin is under way: the panes ride down and off with the symbols
		// they were cut into, rather than popping when the reveal lands.
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, show && cells.length > 0);
			show = false;
			cells = [];
			holeMarks = [];
			fallOut.set(0, { duration: 0 });
		},
		splitPanesHide: () => {
			show = false;
			cells = [];
			holeMarks = [];
			fallOut.set(0, { duration: 0 });
		},
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			nowMs = now;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	const drawUnderGlow = (g: import('pixi.js').Graphics) => {
		g.roundRect(-CARD_W / 2 - 2, -CARD_H / 2 - 2, CARD_W + 4, CARD_H + 4, 10);
		g.fill({ color: DARK, alpha: 0.9 });
	};

	// weathered wood frame around the settled split cell
	const drawFrame = (g: import('pixi.js').Graphics, isHigh: boolean) => {
		g.roundRect(-CARD_W / 2 - 3, -CARD_H / 2 - 3, CARD_W + 6, CARD_H + 6, 8);
		g.stroke({
			color: isHigh ? TOMBSTONE_FX.brass : TOMBSTONE_FX.ironEdge,
			width: 2,
			alpha: 0.75,
		});
	};

	// settled seam: powder burn + thin brass wire (not glossy gold Madam panes)
	const drawDivider = (
		g: import('pixi.js').Graphics,
		cell: SplitCell,
		dividerIndex: number,
		slim: number,
	) => {
		drawPowderSeam(g, CARD_H, slim, {
			time,
			seed: cell.seed + dividerIndex,
		});
	};

	// bullet score / powder trail sweeping down a seam while the symbol is whole
	const drawCutBlade = (
		g: import('pixi.js').Graphics,
		_cell: SplitCell,
		_dividerIndex: number,
		sweepValue: number,
	) => {
		if (sweepValue <= 0) return;
		const s = CARD_H;
		const half = s / 2;
		const margin = 22;
		const travel = s + margin * 2;
		const headY = -half - margin + Math.min(sweepValue, 1) * travel;
		const trailTop = -half - margin;
		const segments = 7;
		const trailEnd = Math.min(headY, half + margin);
		for (let i = 0; i < segments; i++) {
			const y0 = trailTop + ((trailEnd - trailTop) / segments) * i;
			const y1 = trailTop + ((trailEnd - trailTop) / segments) * (i + 1);
			const heat = (i + 1) / segments;
			g.rect(-2.6, y0, 5.2, y1 - y0);
			g.fill({ color: TOMBSTONE_FX.powder, alpha: 0.5 * heat });
			g.rect(-0.8, y0, 1.6, y1 - y0);
			g.fill({ color: TOMBSTONE_FX.dust, alpha: 0.55 * heat });
		}
		if (sweepValue < 1) {
			g.ellipse(0, headY, 11, 3.2);
			g.fill({ color: BLOOD, alpha: 0.4 });
			g.ellipse(0, headY, 5, 1.6);
			g.fill({ color: TOMBSTONE_FX.dust, alpha: 0.55 });
		}
	};

	const drawSeamFlare = (g: import('pixi.js').Graphics, flare: number) => {
		if (flare <= 0.01) return;
		const s = CARD_H;
		const half = s / 2;
		g.roundRect(-7, -half, 14, s, 5);
		g.fill({ color: TOMBSTONE_FX.powder, alpha: 0.65 * flare });
		g.roundRect(-1.8, -half, 3.6, s, 1.6);
		g.fill({ color: TOMBSTONE_FX.bloodRust, alpha: 0.55 * flare });
	};

	const drawDetonation = (g: import('pixi.js').Graphics, d: number) => {
		if (d <= 0 || d >= 1) return;
		const fade = 1 - d;
		// dusty amber shock, not a bright clinic wash
		g.roundRect(-CARD_W / 2 - 4, -CARD_H / 2 - 4, CARD_W + 8, CARD_H + 8, 10);
		g.fill({ color: TOMBSTONE_FX.dust, alpha: 0.35 * fade * fade });
		const ringRadius = CARD_H * (0.2 + 0.75 * d);
		g.circle(0, 0, ringRadius);
		g.stroke({ color: BLOOD, width: 5 * fade + 1, alpha: 0.35 * fade });
		g.circle(0, 0, ringRadius * 0.92);
		g.stroke({ color: TOMBSTONE_FX.brass, width: 1.6 * fade + 0.4, alpha: 0.55 * fade });
	};

	/** Kenney burst poses for the open-pane moment (smoke + brass sparks + dust). */
	const burstSprites = (cell: SplitCell, panes: number, d: number, split: number) => {
		if (d <= 0.02 || d >= 0.98) return [] as {
			key: string;
			tex: number;
			x: number;
			y: number;
			size: number;
			rot: number;
			alpha: number;
		}[];
		const fade = 1 - d;
		const out: {
			key: string;
			tex: number;
			x: number;
			y: number;
			size: number;
			rot: number;
			alpha: number;
		}[] = [];
		// gunsmoke + dust only — skip pale flash discs that read as clinic sparkles
		out.push({
			key: `${cell.key}-puff`,
			tex: cell.seed % 2 === 0 ? VFX.puffA : VFX.puffB,
			x: 0,
			y: -6 * d,
			size: 110 + 40 * d,
			rot: d * 0.35,
			alpha: 0.62 * fade,
		});
		out.push({
			key: `${cell.key}-smoke`,
			tex: VFX.smokeA,
			x: 8,
			y: 10 * d,
			size: 80 + 30 * d,
			rot: -d * 0.2,
			alpha: 0.45 * fade,
		});
		for (let seamIndex = 0; seamIndex < panes - 1; seamIndex++) {
			const seamX = (-CARD_W / 2 + ((seamIndex + 1) / panes) * CARD_W) * split;
			for (let k = 0; k < 3; k++) {
				const sparkSeed = cell.seed * 17 + seamIndex * 71 + k * 13;
				const side = rand(sparkSeed) > 0.5 ? 1 : -1;
				const y0 = (rand(sparkSeed + 1) - 0.5) * CARD_H * 0.65;
				const dist = (14 + rand(sparkSeed + 2) * 28) * d;
				// brass spark / muzzle / dirt — never soft white circles
				const tex = k === 0 ? VFX.sparkB : k === 1 ? VFX.muzzleB : VFX.dirtB;
				out.push({
					key: `${cell.key}-s${seamIndex}-k${k}`,
					tex,
					x: seamX + side * dist,
					y: y0 + 10 * d,
					size: 22 + rand(sparkSeed + 3) * 20,
					rot: rand(sparkSeed + 4) * Math.PI,
					alpha: 0.7 * fade,
				});
			}
		}
		return out;
	};

	const drawBadgePlate = (g: import('pixi.js').Graphics) => {
		g.roundRect(-28, -18, 56, 36, 4);
		g.fill({ color: TOMBSTONE_FX.iron, alpha: 0.82 });
		g.roundRect(-28, -18, 56, 36, 4);
		g.stroke({ color: TOMBSTONE_FX.dust, width: 1.6, alpha: 0.85 });
		g.roundRect(-25, -15, 50, 30, 3);
		g.stroke({ color: TOMBSTONE_FX.bloodRust, width: 1, alpha: 0.45 });
	};

	const cutHeadSprites = (
		cell: SplitCell,
		dividerIndex: number,
		sweepValue: number,
		seamX: number,
	) => {
		if (sweepValue <= 0 || sweepValue >= 1) return [] as {
			key: string;
			tex: number;
			x: number;
			y: number;
			size: number;
			rot: number;
			alpha: number;
		}[];
		const half = CARD_H / 2;
		const margin = 22;
		const travel = CARD_H + margin * 2;
		const headY = -half - margin + sweepValue * travel;
		return [
			{
				key: `${cell.key}-cut-${dividerIndex}-m`,
				tex: VFX.muzzleB,
				x: seamX,
				y: headY,
				size: 42,
				rot: 0,
				alpha: 0.7,
			},
			{
				key: `${cell.key}-cut-${dividerIndex}-s`,
				tex: VFX.sparkC,
				x: seamX + 6,
				y: headY - 4,
				size: 28,
				rot: time * 4,
				alpha: 0.65,
			},
		];
	};

</script>

{#snippet splitCell(cell: DrawnCell)}
	{@const panes = Math.min(cell.count, MAX_PANES)}
	{@const sliceWidth = CARD_W / panes}
	{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	<!-- cells persisted from an earlier event sit fully split and ignore the
		shared strike tweens, or a later split would visibly re-cut them -->
	{@const split = cell.fresh ? splitProgress.current : 1}
	{@const slim = Math.min(1, 3 / panes)}
	{@const gap = CARD_W * Math.min(0.025, 0.09 / panes)}
	{@const paneWidth = Math.max((sliceWidth - gap) * split + CARD_W * (1 - split), 2)}
	<Container x={cell.cx} y={cell.cy} scale={cell.fresh ? pulse.current : 1}>
		<Graphics draw={drawUnderGlow} />
		{#each Array.from({ length: panes }) as _, i (i)}
			{@const paneX = (-CARD_W / 2 + (i + 0.5) * sliceWidth) * split}
			<Container x={paneX}>
				<Rectangle isMask anchor={0.5} width={paneWidth} height={CARD_H} />
				<SymbolSprite {symbolInfo} />
			</Container>
		{/each}
		{#each Array.from({ length: panes - 1 }) as _, i (i)}
			<Container x={(-CARD_W / 2 + (i + 1) * sliceWidth) * split} alpha={split}>
				<!-- Kenney scorch strip under the hairline — powder burn, not gold pane -->
				<TombstoneFxSprite
					tex={i % 2 === 0 ? VFX.scorchA : VFX.scorchB}
					width={22}
					height={CARD_H * 0.98}
					alpha={0.72}
					rotation={0}
				/>
				<TombstoneFxSprite
					tex={VFX.scratch}
					width={18}
					height={CARD_H * 0.9}
					alpha={0.4}
					rotation={Math.PI / 2}
				/>
				<Graphics draw={(g) => drawDivider(g, cell, i, slim)} />
			</Container>
		{/each}
		{@const nDividers = panes - 1}
		{#if cell.fresh}
			{#each Array.from({ length: nDividers }) as _, i (i)}
				{@const seamX = -CARD_W / 2 + (i + 1) * sliceWidth}
				{@const sweep = Math.min(Math.max(cutSweep.current * (1 + 0.15 * (nDividers - 1)) - 0.15 * i, 0), 1)}
				<Container x={seamX} alpha={1 - split * 0.9}>
					<Graphics draw={(g) => drawCutBlade(g, cell, i, sweep)} />
				</Container>
				{#each cutHeadSprites(cell, i, sweep, 0) as fx (fx.key)}
					<Container x={seamX} alpha={1 - split * 0.9}>
						<TombstoneFxSprite
							tex={fx.tex}
							x={fx.x}
							y={fx.y}
							width={fx.size}
							height={fx.size}
							rotation={fx.rot}
							alpha={fx.alpha}
						/>
					</Container>
				{/each}
			{/each}
			{#each Array.from({ length: nDividers }) as _, i (i)}
				{@const seamX = -CARD_W / 2 + (i + 1) * sliceWidth}
				<Container x={seamX}>
					<Graphics draw={(g) => drawSeamFlare(g, seamFlare.current)} />
					{#if seamFlare.current > 0.05}
						<TombstoneFxSprite
							tex={VFX.scorchA}
							width={36}
							height={CARD_H * 0.95}
							alpha={0.55 * seamFlare.current}
						/>
					{/if}
				</Container>
			{/each}
		{/if}
		<Container alpha={split}>
			<Graphics draw={(g) => drawFrame(g, isHigh)} />
		</Container>
		{#if cell.fresh}
			<Container>
				<Graphics draw={(g) => drawDetonation(g, detonation.current)} />
				{#each burstSprites(cell, panes, detonation.current, split) as fx (fx.key)}
					<TombstoneFxSprite
						tex={fx.tex}
						x={fx.x}
						y={fx.y}
						width={fx.size}
						height={fx.size}
						rotation={fx.rot}
						alpha={fx.alpha}
					/>
				{/each}
			</Container>
		{/if}
		<!-- bullet holes sit ON the card — stamped into the wood, not a hand in front -->
		{#each holeMarks.filter((m) => m.cellKey === cell.key) as mark (mark.id)}
			<BulletHoleMark
				tex={mark.tex}
				x={mark.x}
				y={mark.y}
				scale={mark.scale}
				rot={mark.rot}
				born={mark.born}
				now={nowMs}
			/>
		{/each}
	</Container>
{/snippet}

{#snippet badgeMarker(cell: SplitCell)}
	<!-- EVERY split cell states exactly what it is worth. Wanted-poster plaque
		— dusty amber on iron, not clinical white "3x" HUD text. -->
	<Container x={cell.cx} y={cell.cy} scale={cell.fresh ? pulse.current : 1}>
		<Graphics draw={drawBadgePlate} />
		<Text
			anchor={0.5}
			text={`${cell.count}x`}
			style={{
				fontFamily: 'Georgia, Times New Roman, serif',
				fontWeight: '900',
				fontSize: 28,
				fill: 0xc9a34a,
				stroke: { color: 0x0a0806, width: 5 },
			}}
		/>
	</Container>
{/snippet}

<!-- MainContainer stays MOUNTED even while hidden: a remounted node appends to
	the END of the shared pixi parent and would jump above WinDim
	(see .cursor/skills/pixi-svelte-layering). -->
<MainContainer>
	{#if show}
		<Container x={stateShake.x} y={stateShake.y + fallOut.current}>
			{#each drawn as cell (cell.key)}
				{@render splitCell(cell)}
			{/each}
			{#each drawn as cell (cell.key)}
				{@render badgeMarker(cell)}
			{/each}
		</Container>
	{/if}
</MainContainer>
