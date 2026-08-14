<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	// SPLIT (no-tear): the scored symbol is NEVER cut apart. The cell stays a
	// single whole card and the multiplier is told by a bullet volley stamping
	// holes into it plus an "Nx" wanted-poster badge. The user rejected every
	// version that visibly split / parted / sliced the cell — bullet holes and
	// the badge are the entire read.
	export type EmitterEventSplitPanes =
		| { type: 'splitPanesShow'; cells: { reel: number; row: number; count: number; name?: SymbolName }[] }
		| { type: 'splitPanesHide' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Text } from 'pixi-svelte';

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
		EXPLOSION_MIN_MULT,
		EXPLOSION_READ_MS,
		holePose,
		shotsForMultiplier,
		nextShotGap,
		buildCountUp,
	} from '../game/splitBullets';
	import { EXPLOSION_LIFE_MS } from '../game/splitExplosion';
	import { shakeBoard } from '../game/stateShake.svelte';
	import { TOMBSTONE_FX } from '../game/tombstoneVfx';
	import { trValueStyle, TR_INK_GOLD, TR_INK_IRON } from '../game/typography';
	import SymbolSprite from './SymbolSprite.svelte';
	import BulletHoleMark from './BulletHoleMark.svelte';
	import SplitExplosion from './SplitExplosion.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

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
	/**
	 * The multiplier value each cell's badge is CURRENTLY showing. During a
	 * strike this rolls up in random small steps (one per shot) from the cell's
	 * previous value to its target, landing on the final shot — instead of the
	 * badge snapping straight to the target. Settled cells read their final count
	 * via the `?? cell.count` fallback in the badge.
	 */
	let displayCounts = $state<Record<string, number>>({});
	/** wall clock for muzzle flashes on stamped holes */
	let nowMs = $state(performance.now());
	/** stamped bullet holes that stay on their cells until fall-out */
	let holeMarks = $state<HoleMark[]>([]);
	/** one-shot detonations on cells whose multiplier cleared EXPLOSION_MIN_MULT */
	let explosionMarks = $state<{ id: string; cellKey: string; born: number }[]>([]);
	// rides the scored cells off the bottom edge when the next spin starts
	const fallOut = new Tween(0);

	// Rotated so several cells detonating on one board are not the same boom
	// three times. forcePlay so a stacked chain still rings each blast.
	const EXPLOSION_SFX = [
		'sfx_multiplier_explosion_a',
		'sfx_multiplier_explosion_b',
		'sfx_multiplier_explosion_c',
	] as const;

	const playShotSfx = (isFinal: boolean) => {
		// forcePlay: stacked volleys must not get swallowed by the once-player.
		// Earlier rounds are the dry pistol-into-wood punch. The LAST round always
		// RICOCHETS — and it plays ALONE, not stacked on the wood punch, because
		// the ricochet cue already carries the magnum crack PLUS the whine ringing
		// off iron. Stacking wood under it (the old behaviour) buried the zing. So
		// a volley now reads BANG .. BANG .. CRACK-ZING and the ear knows the
		// count-up has landed on its target on that final shot.
		context.eventEmitter.broadcast({
			type: 'soundOnce',
			name: isFinal ? 'sfx_bullet_ricochet' : 'sfx_bullet_wood',
			forcePlay: true,
		});
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
						cx: getSymbolX(cell.reel),
						cy: getCellCenterY(cell.reel, cell.row),
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
			// SEED the count-up start: a re-struck cell climbs from what it already
			// showed (e.g. 10x -> 20x); a brand-new cell climbs from a low base
			// (~a quarter of its target) so the roll-up is felt, not a snap.
			const prev = displayCounts[key];
			const startBase = prev != null ? prev : Math.max(1, Math.round(c.count * 0.25));
			displayCounts = { ...displayCounts, [key]: startBase };
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
				cy: getCellCenterY(cell.reel, cell.row),
				name:
					cell.pinned ??
					(context.stateGame.board[cell.reel]?.reelState.symbols[cell.row]?.rawSymbol
						.name as SymbolName | undefined),
			}))
			.filter((cell): cell is DrawnCell => cell.name != null),
	);

	/**
	 * Detonate the given big cells: a one-shot gunpowder blast on each card plus a
	 * rotated boom, and a heavier board shake so a big hit is FELT, not just seen.
	 *
	 * This is the FINAL step of the strike — it runs after the whole bullet volley
	 * has stamped the multiplier AND a read-beat has passed, so the explosion
	 * never covers the Nx before the player can read it. Only cells over
	 * EXPLOSION_MIN_MULT ever reach here, and each detonates exactly once.
	 */
	const detonateBigCells = (big: SplitCell[]) => {
		if (!big.length) return;
		const born = performance.now();
		explosionMarks = [
			...explosionMarks,
			...big.map((cell) => ({ id: `${cell.key}-boom-${born}`, cellKey: cell.key, born })),
		];
		big.forEach((cell, i) => {
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: EXPLOSION_SFX[i % EXPLOSION_SFX.length],
				forcePlay: true,
			});
		});
		shakeBoard({ intensity: 20, duration: fxDur(340) });
		context.eventEmitter.broadcast({ type: 'saloonCheers' });
	};

	// BULLET STRIKE: each fresh cell takes 1–4 rounds (scaled by its multiplier).
	// Volleys fire across the board so a big multi gets more holes. Wood + ricochet
	// on every shot. The cell is NEVER cut — the holes and the badge carry the
	// read; cells over EXPLOSION_MIN_MULT also DETONATE. One shake on the first
	// volley for impact (upgraded to a heavier one when something blows up).
	const runSplit = async () => {
		const fresh = cells.filter((c) => c.fresh);
		// drop prior marks on cells that are re-striking this event
		const freshKeys = new Set(fresh.map((c) => c.key));
		holeMarks = holeMarks.filter((m) => !freshKeys.has(m.cellKey));
		explosionMarks = explosionMarks.filter((m) => !freshKeys.has(m.cellKey));

		const maxShots = Math.max(1, ...fresh.map((c) => shotsForMultiplier(c.count)));

		// Per cell, the random step values its badge visits, one per shot, from
		// its seeded start (set in layout) up to its target on its LAST shot.
		const countUp = new Map<string, number[]>(
			fresh.map((cell) => [
				cell.key,
				buildCountUp(
					displayCounts[cell.key] ?? cell.count,
					cell.count,
					shotsForMultiplier(cell.count),
				),
			]),
		);

		for (let shot = 0; shot < maxShots; shot++) {
			let stamped = 0;
			const stepped: Record<string, number> = {};
			for (const cell of fresh) {
				const cellShots = shotsForMultiplier(cell.count);
				if (shot >= cellShots) continue;
				stampHole(cell, shot);
				// roll this cell's multiplier to its value for this shot
				stepped[cell.key] = countUp.get(cell.key)?.[shot] ?? cell.count;
				stamped += 1;
			}
			if (stamped > 0) {
				// commit this shot's rolled multiplier values in one reactive write
				displayCounts = { ...displayCounts, ...stepped };
				const isFinal = shot === maxShots - 1;
				playShotSfx(isFinal);
				// one light impact shake on the first volley — the HEAVY blast shake
				// belongs to the detonation, which now comes last (below)
				if (shot === 0) {
					shakeBoard({
						intensity: Math.min(10 + fresh.length * 2.5, 18),
						duration: fxDur(240),
					});
				}
			}
			// uneven rest between shots so the volley never sounds metronomic
			if (shot < maxShots - 1) await fxWait(nextShotGap());
		}

		// pin every struck cell exactly on its target once the volley is done
		displayCounts = {
			...displayCounts,
			...Object.fromEntries(fresh.map((c) => [c.key, c.count])),
		};

		// SEQUENCE (the whole point of this feature's read):
		//   flame → bullets stamp the multiplier (Nx badge up) → HOLD so the
		//   player can READ the Nx → THEN only cells over EXPLOSION_MIN_MULT
		//   detonate, exactly once, as the final beat. Never during the volley.
		const big = fresh.filter((c) => c.count > EXPLOSION_MIN_MULT);
		if (big.length) {
			await fxWait(EXPLOSION_READ_MS);
			detonateBigCells(big);
		}
	};

	context.eventEmitter.subscribeOnMount({
		splitPanesShow: async ({ cells: incoming }) => {
			const anyFresh = layout(incoming);
			// nothing new to strike (e.g. the split only hit wild columns):
			// leave the surviving panes exactly as they are
			if (!anyFresh || !cells.length) return;
			// scored cells burn while the strike plays: with no divider drawn
			// down a split, the fire is what ties the struck cells together,
			// and it climbs with the biggest multiplier on the board.
			context.eventEmitter.broadcast({
				type: 'cellFireShow',
				cells: cells.map((c) => ({ reel: c.reel, row: c.row })),
				level: Math.max(...cells.map((c) => c.count)),
			});
			await runSplit();
			// strike done: the fresh cells settle in with the persisted ones
			cells = cells.map((cell) => (cell.fresh ? { ...cell, fresh: false } : cell));
		},
		// the next spin is under way: the panes ride down and off with the symbols
		// they were cut into, rather than popping when the reveal lands.
		featureFxFallOut: async () => {
			context.eventEmitter.broadcast({ type: 'cellFireHide' });
			await fallOutFeatureFx(fallOut, show && cells.length > 0);
			show = false;
			cells = [];
			holeMarks = [];
			explosionMarks = [];
			displayCounts = {};
			fallOut.set(0, { duration: 0 });
		},
		splitPanesHide: () => {
			context.eventEmitter.broadcast({ type: 'cellFireHide' });
			show = false;
			cells = [];
			holeMarks = [];
			explosionMarks = [];
			displayCounts = {};
			fallOut.set(0, { duration: 0 });
		},
	});

	onMount(() => {
		let raf = 0;
		const tick = (now: number) => {
			nowMs = now;
			// drop detonations that have finished playing so the list never grows
			// unbounded across a long session of big hits
			if (explosionMarks.length) {
				const live = explosionMarks.filter((m) => now - m.born < EXPLOSION_LIFE_MS);
				if (live.length !== explosionMarks.length) explosionMarks = live;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	// Weathered iron frame around the settled scored cell. High symbols used to
	// get a bright brass stroke, which drew a glossy gold rounded rectangle
	// around the card — the exact gilded-pane look the reskin is removing. Both
	// tiers are dark iron now; the tier reads from the warmth, not the shine.
	const drawFrame = (g: import('pixi.js').Graphics, isHigh: boolean) => {
		g.roundRect(-CARD_W / 2 - 3, -CARD_H / 2 - 3, CARD_W + 6, CARD_H + 6, 8);
		g.stroke({
			color: isHigh ? TOMBSTONE_FX.ironEdge : TOMBSTONE_FX.iron,
			width: 2,
			alpha: isHigh ? 0.8 : 0.62,
		});
	};

	const drawBadgePlate = (g: import('pixi.js').Graphics) => {
		g.roundRect(-28, -18, 56, 36, 4);
		g.fill({ color: TOMBSTONE_FX.iron, alpha: 0.82 });
		g.roundRect(-28, -18, 56, 36, 4);
		g.stroke({ color: TOMBSTONE_FX.dust, width: 1.6, alpha: 0.85 });
		g.roundRect(-25, -15, 50, 30, 3);
		g.stroke({ color: TOMBSTONE_FX.bloodRust, width: 1, alpha: 0.45 });
	};

</script>

{#snippet splitCell(cell: DrawnCell)}
	{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
	{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
	<!-- The cell is a SINGLE whole card. It is never cut, sliced, parted or
		masked into panes — that was rejected repeatedly. The scored symbol is
		redrawn here (so a clone/stretch that moved the board stays correct),
		wearing a thin iron frame, and the ONLY feature marks are the bullet
		holes stamped into it and the multiplier badge above it. -->
	<Container x={cell.cx} y={cell.cy}>
		<SymbolSprite {symbolInfo} />
		<Graphics draw={(g) => drawFrame(g, isHigh)} />
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
		<!-- big-multiplier detonation, drawn ABOVE the holes so the blast reads
			over the freshly punched wood -->
		{#each explosionMarks.filter((m) => m.cellKey === cell.key) as boom (boom.id)}
			<SplitExplosion x={0} y={0} born={boom.born} now={nowMs} size={CARD_W * 1.85} />
		{/each}
	</Container>
{/snippet}

{#snippet badgeMarker(cell: SplitCell)}
	<!-- EVERY scored cell states exactly what it is worth. Wanted-poster plaque
		— dusty amber on iron, not clinical white "3x" HUD text. -->
	<Container x={cell.cx} y={cell.cy}>
		<Graphics draw={drawBadgePlate} />
		<Text
			anchor={0.5}
			text={`${Math.round(displayCounts[cell.key] ?? cell.count)}x`}
			style={trValueStyle({
				fontSize: 28,
				fill: TR_INK_GOLD,
				stroke: { color: TR_INK_IRON, width: 5, join: 'round' },
			})}
		/>
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
			{#each drawn as cell (cell.key)}
				{@render badgeMarker(cell)}
			{/each}
		</BoardSpace>
	{/if}
</MainContainer>
