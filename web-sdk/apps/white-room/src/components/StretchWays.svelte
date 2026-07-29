<script lang="ts" module>
	// STRETCH (normal reel) — the RACK. A chain drops from above, its clamp
	// bites the reel's top edge, and PULLS UP: the reel's dark backplate
	// physically stretches taller past the board top (the bottom edge stays
	// bolted to the board) and the vertical distance between the symbols grows
	// with it. The symbols themselves are NEVER scaled — only the space between
	// them. The stretched state then HOLDS, chain taut, until the next reveal.
	export type EmitterEventStretchWays =
		| { type: 'stretchWaysShow'; cells: { reel: number; row: number; multiplier: number }[] }
		| { type: 'stretchWaysHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicInOut, cubicOut, backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Graphics, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getReelWindow } from '../game/utils';
	import { SYMBOL_SIZE, CELL_PITCH_X } from '../game/constants';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import type { SymbolName } from '../game/types';

	const context = getContext();

	type StretchedReel = {
		reel: number;
		rows: { row: number; multiplier: number }[];
		/** 0 = clamps off-screen, 1 = jaws on the reel edges */
		clampIn: Tween<number>;
		/** quick jaw-bite pulse when the clamps take hold */
		bite: Tween<number>;
		/** 0 = board pitch, 1 = fully racked — drives cover fade + tension look */
		pull: Tween<number>;
	};

	let stretched = $state<StretchedReel[]>([]);
	let show = $state(false);

	/** how many extra display-rows the pull adds (the visual stretch amount) */
	const growOf = (rows: number) => Math.min(1.4, rows * 0.32);
	/** how far past the window edge the jaws reach when they bite */
	const JAW_OVERLAP = SYMBOL_SIZE * 0.16;
	const CLAMP_ASPECT = 943 / 1397; // clamp.png h/w
	const CHAIN_ASPECT = 1536 / 194; // chain_tile.png h/w
	/** chains travel this far when flying in from off-screen */
	const FLY_IN = SYMBOL_SIZE * 5;

	context.eventEmitter.subscribeOnMount({
		stretchWaysShow: async ({ cells: incoming }) => {
			// one stretch event per reel; earlier reels stay racked (their tweens
			// are already parked at 1) while the new one animates.
			const byReel = new Map<number, { row: number; multiplier: number }[]>();
			for (const c of incoming) {
				if (stretched.some((s) => s.reel === c.reel)) continue;
				if (!byReel.has(c.reel)) byReel.set(c.reel, []);
				byReel.get(c.reel)!.push({ row: c.row, multiplier: c.multiplier });
			}
			if (byReel.size === 0) return;

			const jobs: Promise<void>[] = [];
			for (const [reel, rows] of byReel) {
				const entry: StretchedReel = {
					reel,
					rows: rows.sort((a, b) => a.row - b.row),
					clampIn: new Tween(0),
					bite: new Tween(0),
					pull: new Tween(0),
				};
				stretched = [...stretched, entry];
				show = true;
				jobs.push(runRack(entry));
			}
			await Promise.all(jobs);
		},
		stretchWaysHide: () => {
			show = false;
			stretched = [];
		},
	});

	const runRack = async (entry: StretchedReel) => {
		const rows = entry.rows.length;

		// 1) the chain flies in and the clamp bites the reel's top edge
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		await entry.clampIn.set(1, { duration: 420, easing: cubicOut });
		shakeBoard({ intensity: 4, duration: 140 });
		await entry.bite.set(1, { duration: 130, easing: backOut });

		// 2) THE PULL: the display-height override grows, so the backplate, the
		//    reel window and everything solved from getReelRows stretches with it.
		//    The clamps ride the moving edges; the symbols only spread apart.
		const drive = new Tween(rows);
		context.stateGame.reelStretch[entry.reel] = drive;
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
		await Promise.all([
			drive.set(rows + growOf(rows), { duration: 900, easing: cubicInOut }),
			entry.pull.set(1, { duration: 900, easing: cubicInOut }),
		]);
		shakeBoard({ intensity: 7, duration: 220 });
		// racked state HOLDS — chains stay taut until the next reveal clears
		// reelStretch and stretchWaysHide drops the rig.
	};

	// --- layout ---------------------------------------------------------------
	const boardLayout = $derived(context.stateGameDerived.boardLayout());
	const originX = $derived(boardLayout.x - boardLayout.width * 0.5);
	const originY = $derived(boardLayout.y - boardLayout.height * 0.5);

	type DrawnReel = {
		reel: number;
		cx: number;
		top: number;
		bottom: number;
		pitch: number;
		clampIn: number;
		bite: number;
		pull: number;
		cells: {
			key: string;
			cy: number;
			multiplier: number;
			shown: number;
			tick: number;
			name: SymbolName;
		}[];
	};

	/** where every counter starts its climb (each symbol is worth ~1-2 ways
	 * before the stretch multiplies it) */
	const COUNT_FROM = 2;

	const drawn = $derived(
		stretched.map((entry): DrawnReel => {
			// window is reactive through reelStretch.current: it grows during the
			// pull, and this whole layout grows with it.
			const window = getReelWindow(entry.reel);
			const top = originY + window.top;
			const bottom = originY + window.bottom;
			const pitch = (bottom - top) / entry.rows.length;
			const pull = entry.pull.current;
			return {
				reel: entry.reel,
				cx: originX + getSymbolX(entry.reel),
				top,
				bottom,
				pitch,
				clampIn: entry.clampIn.current,
				bite: entry.bite.current,
				pull,
				cells: entry.rows
					.map((r, i) => {
						// the counter rides the SAME pull tween as the physical stretch,
						// squared so it lags early and sprints home — at pull=1 the raw
						// value IS the final multiplier, so the resting number is exact.
						const start = Math.min(COUNT_FROM, r.multiplier);
						const raw = start + (r.multiplier - start) * pull * pull;
						return {
							key: `${entry.reel}-${r.row}`,
							cy: top + (i + 0.5) * pitch,
							multiplier: r.multiplier,
							shown: Math.round(raw),
							// odometer tick: a small scale pop each time the integer rolls
							// over, windowed by sin(pi*pull) so the badge rests at scale 1
							// both before and after the pull.
							tick: 1 + 0.12 * (1 - (raw - Math.floor(raw))) * Math.sin(Math.PI * pull),
							// live board read: a later clone re-skins the spread copy too
							name: context.stateGame.board[entry.reel]?.reelState.symbols[r.row]?.rawSymbol
								.name as SymbolName,
						};
					})
					.filter((c) => c.name != null),
			};
		}),
	);

	// the stretched backplate: same face/socket palette as BoardPlate, but the
	// sockets sit at the SPREAD pitch, so the black background visibly stretches
	const drawCover = (g: import('pixi.js').Graphics, r: DrawnReel) => {
		const x = r.cx - CELL_PITCH_X / 2;
		const h = r.bottom - r.top;
		g.rect(x, r.top, CELL_PITCH_X, h);
		g.fill({ color: 0x24262a, alpha: 1 });
		for (let i = 0; i < r.cells.length; i++) {
			const y = r.top + i * r.pitch + 1.75;
			g.roundRect(x + 1.75, y, CELL_PITCH_X - 3.5, r.pitch - 3.5, 7);
			g.fill({ color: 0x0c0d0f, alpha: 0.95 });
			g.roundRect(x + 1.75, y, CELL_PITCH_X - 3.5, r.pitch - 3.5, 7);
			g.stroke({ color: 0x000000, width: 3, alpha: 0.5 });
		}
		// strained edge where the clamp pulls — a faint hot line under the jaws
		if (r.pull > 0) {
			g.rect(x, r.top - 1.5, CELL_PITCH_X, 3);
			g.fill({ color: 0xd8dce0, alpha: 0.18 * r.pull });
		}
	};

	const clampW = CELL_PITCH_X * 1.14;
	const clampH = clampW * CLAMP_ASPECT;
	const chainW = CELL_PITCH_X * 0.17;
	const chainSegH = chainW * CHAIN_ASPECT;

	/** top clamp centre y, including fly-in travel (bottom edge is bolted to the
	 * board, so there is no bottom clamp) */
	const clampY = (r: DrawnReel, _edge: 'top') => {
		const attachedY = r.top - clampH * 0.5 + JAW_OVERLAP;
		return attachedY - (1 - r.clampIn) * FLY_IN;
	};

	/** stacked chain segments from the clamp's stub off the edge of the screen */
	const chainSegments = (fromY: number, dir: -1 | 1) => {
		const segs: number[] = [];
		for (let i = 0; i < 6; i++) segs.push(fromY + dir * i * chainSegH);
		return segs;
	};
</script>

<MainContainer>
	<Container x={stateShake.x} y={stateShake.y}>
		{#if show}
			{#each drawn as r (r.reel)}
				{@const coverAlpha = Math.min(1, r.clampIn * 2)}
				<!-- stretched backplate + spread symbol copies (fade in while the
					clamps arrive; they sit exactly over the real symbols until the
					pull starts, so there is no pop) -->
				<Container alpha={coverAlpha}>
					<Graphics draw={(g) => drawCover(g, r)} />
					{#each r.cells as cell (cell.key)}
						{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
						<Container x={r.cx} y={cell.cy}>
							<Sprite
								key={symbolInfo.assetKey}
								anchor={0.5}
								width={SYMBOL_SIZE * symbolInfo.sizeRatios.width}
								height={SYMBOL_SIZE * symbolInfo.sizeRatios.height}
							/>
						</Container>
					{/each}
					{#each r.cells as cell (cell.key)}
						{#if cell.multiplier > 1}
							<Container x={r.cx} y={cell.cy} scale={cell.tick}>
								<Text
									anchor={0.5}
									text={`${cell.shown}x`}
									style={{
										fontFamily: 'Arial',
										fontWeight: '900',
										fontSize: 30,
										fill: 0xffffff,
										stroke: { color: 0x000000, width: 5 },
									}}
								/>
							</Container>
						{/if}
					{/each}
				</Container>

				<!-- the rig: ONE chain from above — the reel's bottom edge is bolted
					to the board now, so only the top clamp pulls -->
				{@const cy = clampY(r, 'top')}
				{@const stubY = cy - clampH / 2}
				<Container x={r.cx}>
					{#each chainSegments(stubY, -1) as segY, i (i)}
						<Sprite
							key="stretchChain"
							anchor={{ x: 0.5, y: 1 }}
							x={0}
							y={segY}
							width={chainW}
							height={chainSegH}
						/>
					{/each}
					<Container
						y={cy}
						scale={{
							x: 1 + 0.06 * r.bite * (1 - r.pull),
							y: 1 - 0.08 * r.bite * (1 - r.pull),
						}}
					>
						<Sprite key="stretchClamp" anchor={0.5} width={clampW} height={clampH} />
					</Container>
				</Container>
			{/each}
		{/if}
	</Container>
</MainContainer>
