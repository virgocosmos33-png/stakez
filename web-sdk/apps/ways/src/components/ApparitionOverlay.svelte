<script lang="ts" module>
	export type EmitterEventApparition =
		| { type: 'apparitionsRefresh' }
		// keepPersistent (free spins): surviving split cells stay on the field as
		// ghost markers while the reels spin, so the haunting never visually drops
		| { type: 'apparitionsHide'; keepPersistent?: boolean }
		| { type: 'apparitionsPulse'; positions: Position[] }
		| { type: 'apparitionsWinGrow'; positions: Position[] }
		| { type: 'apparitionsWinRelease' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle, Text } from 'pixi-svelte';

	import type { Position } from '../game/types';
	import type { RawSymbol } from '../game/types';
	import { getContext } from '../game/context';
	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_SIZE, HIGH_SYMBOLS } from '../game/constants';
	import { stateShake, shakeBoard } from '../game/stateShake.svelte';
	import SymbolSprite from './SymbolSprite.svelte';

	const context = getContext();

	// Haunted cells render in this overlay ABOVE the whole board: randomly
	// tilted/scaled/z-ordered (so neighbouring haunts overlap each other
	// organically), split into center-cropped panes divided by slim lightning.
	type HauntCell = {
		key: string;
		reel: number;
		row: number; // padded row index
		count: number;
		name: RawSymbol['name'];
		// reveals the cell survives: 1/undefined = this spin only, 2+ = carries
		// over into the next spin(s), -1 = sticky for the whole bonus
		ttl?: number;
		cx: number;
		cy: number;
		scale: number;
		rotation: number;
		z: number;
		seed: number;
	};

	// haunted cells sit at normal size and only grow when they win
	const WIN_GROW = 1.1;

	let cells = $state<HauntCell[]>([]);
	// ghost markers: split cells that survive into the next spin keep their
	// haunt frame + count on the field WHILE the reels spin beneath them
	let ghosts = $state<HauntCell[]>([]);
	let show = $state(false);
	let time = $state(0);
	const pulseScale = new Tween(1);
	let pulsedKeys = $state<Set<string>>(new Set());
	const winScale = new Tween(1);
	let winningKeys = $state<Set<string>>(new Set());
	// split animation: 0 = whole symbol, 1 = fully split into panes
	const splitProgress = new Tween(1);
	let splittingKeys = $state<Set<string>>(new Set());
	// cut sweep: a blade head travels top -> bottom carving the cut line
	// (0 = above the symbol, 1 = blade has fully passed through)
	const cutSweep = new Tween(0);
	// detonation payoff: seams flare white during the hit-stop, then the cell
	// blows apart with a flash, shockwave rings, seam sparks and smoke
	const seamFlare = new Tween(0);
	const detonation = new Tween(0);
	let detonatingKeys = $state<Set<string>>(new Set());

	const rand = (seed: number) => {
		const value = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
		return value - Math.floor(value);
	};

	const refresh = () => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;

		const found: HauntCell[] = [];
		context.stateGame.board.forEach((reel, reelIndex) => {
			reel.reelState.symbols.forEach((reelSymbol, rowIndex) => {
				const multiplier = reelSymbol.rawSymbol.multiplier;
				if (
					multiplier !== undefined &&
					multiplier > 1 &&
					rowIndex > 0 &&
					rowIndex < reel.reelState.symbols.length - 1
				) {
					const seed = reelIndex * 31 + rowIndex * 7 + multiplier * 113;
					found.push({
						key: `${reelIndex}-${rowIndex}`,
						reel: reelIndex,
						row: rowIndex,
						count: multiplier,
						name: reelSymbol.rawSymbol.name,
						ttl: reelSymbol.rawSymbol.ttl,
						cx: originX + SYMBOL_SIZE * (reelIndex + 0.5) + (rand(seed + 1) - 0.5) * 5,
						cy: originY + SYMBOL_SIZE * (rowIndex - 0.5) + (rand(seed + 2) - 0.5) * 5,
						scale: 1 + (rand(seed + 3) - 0.5) * 0.05,
						rotation: (rand(seed + 4) - 0.5) * 0.06,
						z: rand(seed + 5),
						seed,
					});
				}
			});
		});
		// random depth: neighbouring haunts overlap each other in random order
		found.sort((a, b) => a.z - b.z);
		cells = found;
		show = found.length > 0;
	};

	// the cut sequence: a blade of light sweeps down through the symbol
	// carving glowing cut lines (with sparks flying off the blade head).
	// When the blade exits, time holds for a beat while the carved seams
	// flare white-hot (hit-stop), then the cell DETONATES: flash, expanding
	// shockwave rings, sparks spraying off the seams, smoke, a board kick,
	// and the panes slamming apart with a slight overshoot.
	const runSplit = async (keys: Set<string>) => {
		splittingKeys = keys;
		splitProgress.set(0, { duration: 0 });
		cutSweep.set(0, { duration: 0 });
		seamFlare.set(0, { duration: 0 });
		detonation.set(0, { duration: 0 });
		// one fast decisive slash: the blade rips straight down the seam
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_celeb_whoosh_hi' });
		await cutSweep.set(1, { duration: 140, easing: cubicIn });

		// impact lands the instant the blade clears: crack + white seam flash,
		// a hard board kick, and the panes snap apart with overshoot - all at once
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_xways_split' });
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_explosion_b' });
		detonatingKeys = keys;
		seamFlare.set(1, { duration: 20 });
		seamFlare.set(0, { duration: 150 });
		shakeBoard({ intensity: Math.min(10 + keys.size * 2.5, 18), duration: 240 });
		const fx = detonation.set(1, { duration: 300, easing: cubicOut });
		await splitProgress.set(1, { duration: 130, easing: backOut });
		await fx;
		detonatingKeys = new Set();
		splittingKeys = new Set();
	};

	const pulse = async (positions: Position[]) => {
		const keys = new Set(positions.map((position) => `${position.reel}-${position.row}`));
		pulsedKeys = keys;
		pulseScale.set(1.45, { duration: 0 });
		const punch = pulseScale.set(1, { duration: 420, easing: backOut });
		await runSplit(keys);
		await punch;
		pulsedKeys = new Set();
	};

	context.eventEmitter.subscribeOnMount({
		// persistent haunted cells arrive with the reveal ALREADY split: the
		// symbol lands pre-carved into its panes (no re-crack animation - the
		// crack only ever plays once, on the mirror burst that created the cell)
		apparitionsRefresh: () => {
			refresh();
			ghosts = [];
		},
		apparitionsHide: (emitterEvent) => {
			// free spins: surviving cells leave a ghost frame on the field during
			// the spin, telegraphing that whatever lands there is already split
			ghosts = emitterEvent.keepPersistent
				? cells.filter((cell) => cell.ttl === -1 || (cell.ttl !== undefined && cell.ttl >= 2))
				: [];
			show = false;
			cells = [];
		},
		apparitionsPulse: async ({ positions }) => {
			refresh();
			await pulse(positions);
		},
		// haunted cells grow only while they are part of the winning combination
		apparitionsWinGrow: ({ positions }) => {
			winningKeys = new Set(positions.map((position) => `${position.reel}-${position.row}`));
			winScale.set(WIN_GROW, { duration: 220, easing: backOut });
		},
		apparitionsWinRelease: async () => {
			await winScale.set(1, { duration: 180 });
			winningKeys = new Set();
		},
	});

	onMount(() => {
		let raf = 0;
		let start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	// dark backing behind the split panes
	const drawUnderGlow = (graphics: import('pixi.js').Graphics) => {
		const s = SYMBOL_SIZE;
		graphics.roundRect(-s / 2 - 2, -s / 2 - 2, s + 4, s + 4, 10);
		graphics.fill({ color: 0x0a0714, alpha: 0.92 });
	};

	// haunt frame: split cells always carry an absinthe-green outline so the
	// split state is unmistakable. Cells that SURVIVE into the next spin
	// (bonus levels 2/3: ttl >= 2 or sticky -1) burn steady and bright with a
	// wide halo; one-spin splits only get a faint dying flicker.
	const drawHauntFrame = (
		graphics: import('pixi.js').Graphics,
		cell: HauntCell,
		timeValue: number,
	) => {
		const s = SYMBOL_SIZE;
		const persistent = cell.ttl !== undefined && (cell.ttl === -1 || cell.ttl >= 2);
		const pulse = persistent
			? 0.8 + 0.2 * Math.sin(timeValue * 2.4 + cell.seed)
			: 0.5 + 0.5 * rand(Math.floor(timeValue * 16) * 11 + cell.seed);
		graphics.roundRect(-s / 2 - 3, -s / 2 - 3, s + 6, s + 6, 11);
		graphics.stroke({
			color: 0x2bff66,
			width: persistent ? 3 : 1.6,
			alpha: (persistent ? 0.85 : 0.35) * pulse,
		});
		if (persistent) {
			// wide soft halo marks the cell as held for coming spins
			graphics.roundRect(-s / 2 - 7, -s / 2 - 7, s + 14, s + 14, 14);
			graphics.stroke({ color: 0x2bff66, width: 7, alpha: 0.16 * pulse });
		}
	};

	// apparition count badge backing (the xN text renders on top of it)
	const drawBadge = (graphics: import('pixi.js').Graphics, persistent: boolean) => {
		graphics.circle(0, 0, 21);
		graphics.fill({ color: 0x0a0714, alpha: 0.92 });
		graphics.circle(0, 0, 21);
		graphics.stroke({ color: persistent ? 0x2bff66 : 0x1a7a3c, width: 2, alpha: 0.95 });
	};

	// per-pane card border so every split copy still reads as a framed symbol
	const drawPaneBorder = (
		graphics: import('pixi.js').Graphics,
		paneWidth: number,
		isHigh: boolean,
	) => {
		const s = SYMBOL_SIZE;
		const w = paneWidth;
		if (isHigh) {
			graphics.roundRect(-w / 2, -s / 2, w, s, 6);
			graphics.stroke({ color: 0x120b04, width: 4, alpha: 0.85 });
			graphics.roundRect(-w / 2 + 1, -s / 2 + 1, w - 2, s - 2, 5);
			graphics.stroke({ color: 0xc9a34a, width: 2.5, alpha: 0.95 });
			graphics.roundRect(-w / 2 + 4, -s / 2 + 4, w - 8, s - 8, 4);
			graphics.stroke({ color: 0xf0e3c0, width: 1, alpha: 0.55 });
		} else {
			graphics.roundRect(-w / 2, -s / 2, w, s, 6);
			graphics.stroke({ color: 0x0c0a16, width: 3, alpha: 0.8 });
			graphics.roundRect(-w / 2 + 1.5, -s / 2 + 1.5, w - 3, s - 3, 5);
			graphics.stroke({ color: 0xb887ff, width: 1.5, alpha: 0.6 });
		}
	};

	// the settled cut seam: a clean, sharp line of light between panes -
	// a white-hot core with a cold violet edge glow (no crawling lightning)
	const drawDivider = (
		graphics: import('pixi.js').Graphics,
		cell: HauntCell,
		dividerIndex: number,
		timeValue: number,
	) => {
		const s = SYMBOL_SIZE;
		const half = s / 2;
		const intensity = Math.min((cell.count - 1) / 3, 1);
		const flicker = 0.9 + 0.1 * Math.sin(timeValue * 14 + cell.seed * 3 + dividerIndex * 1.7);

		// soft violet edge glow
		graphics.roundRect(-4 - 1.5 * intensity, -half, 8 + 3 * intensity, s, 4);
		graphics.fill({ color: 0xb887ff, alpha: 0.16 * flicker });
		// inner violet
		graphics.roundRect(-1.8, -half, 3.6, s, 1.8);
		graphics.fill({ color: 0xe6d2ff, alpha: 0.5 * flicker });
		// white-hot core
		graphics.roundRect(-0.7, -half, 1.4, s, 0.7);
		graphics.fill({ color: 0xffffff, alpha: 0.92 * flicker });
	};

	// the cut blade: a hot head that sweeps top -> bottom carving a glowing
	// trail behind it, spraying sparks off the contact point. sweepValue < 0
	// means the blade hasn't reached this divider yet (staggered multi-cuts).
	const drawCutBlade = (
		graphics: import('pixi.js').Graphics,
		cell: HauntCell,
		dividerIndex: number,
		sweepValue: number,
		timeValue: number,
	) => {
		if (sweepValue <= 0) return;
		const s = SYMBOL_SIZE;
		const half = s / 2;
		const margin = 22;
		const travel = s + margin * 2;
		const headY = -half - margin + Math.min(sweepValue, 1) * travel;
		const trailTop = -half - margin;

		// carved trail: a crisp white core inside a violet glow, hottest
		// right behind the head and cooling further back
		const segments = 8;
		const trailEnd = Math.min(headY, half + margin);
		for (let i = 0; i < segments; i++) {
			const y0 = trailTop + ((trailEnd - trailTop) / segments) * i;
			const y1 = trailTop + ((trailEnd - trailTop) / segments) * (i + 1);
			const heat = (i + 1) / segments;
			graphics.rect(-3, y0, 6, y1 - y0);
			graphics.fill({ color: 0xb887ff, alpha: 0.14 * heat });
			graphics.rect(-0.9, y0, 1.8, y1 - y0);
			graphics.fill({ color: 0xffffff, alpha: 0.95 * heat });
		}

		if (sweepValue < 1) {
			// blade head: a sharp downward sliver of light with a violet flare
			graphics.poly([0, headY + 16, 3.4, headY + 2, 0, headY - 22, -3.4, headY + 2]);
			graphics.fill({ color: 0xffffff, alpha: 0.98 });
			graphics.circle(0, headY, 8);
			graphics.fill({ color: 0xb887ff, alpha: 0.5 });
			// horizontal flare where the blade bites the glass
			graphics.ellipse(0, headY, 16, 2);
			graphics.fill({ color: 0xffffff, alpha: 0.55 });

			// a few sharp sparks flicking off the contact point
			for (let i = 0; i < 4; i++) {
				const sparkSeed = cell.seed * 13 + dividerIndex * 29 + i * 7;
				const life = (timeValue * (3 + rand(sparkSeed) * 2) + rand(sparkSeed + 1)) % 1;
				const angle = -Math.PI / 2 + (rand(sparkSeed + 2) - 0.5) * 2.2;
				const dist = 5 + life * (14 + rand(sparkSeed + 3) * 14);
				const x = Math.cos(angle) * dist;
				const y = headY + Math.sin(angle) * dist * 0.8;
				const tail = 3 + rand(sparkSeed + 4) * 4;
				graphics.moveTo(x, y);
				graphics.lineTo(x - Math.cos(angle) * tail, y - Math.sin(angle) * tail * 0.8);
				graphics.stroke({
					color: i % 2 === 0 ? 0xffffff : 0xe6d2ff,
					width: 1.2,
					alpha: 0.85 * (1 - life),
				});
			}
		}
	};

	// hit-stop seam flare: the instant the blade exits, the carved line burns
	// white-hot for a frozen beat - a vertical bar of light with a lens flare
	// at its waist - before the panes blow apart
	const drawSeamFlare = (graphics: import('pixi.js').Graphics, flare: number) => {
		if (flare <= 0.01) return;
		const s = SYMBOL_SIZE;
		const half = s / 2;
		graphics.roundRect(-7, -half, 14, s, 7);
		graphics.fill({ color: 0xb887ff, alpha: 0.4 * flare });
		graphics.roundRect(-2.4, -half, 4.8, s, 2.4);
		graphics.fill({ color: 0xffffff, alpha: 0.98 * flare });
		// horizontal lens flare across the waist of the seam
		graphics.ellipse(0, 0, 30 * flare + 6, 2.5);
		graphics.fill({ color: 0xffffff, alpha: 0.7 * flare });
	};

	// the detonation payoff (kept tight): a fast white flash, one crisp
	// shockwave ring with a violet halo, and a short burst of sparks flung
	// off the parting seams - no rolling smoke, all gone in a beat
	const drawDetonation = (
		graphics: import('pixi.js').Graphics,
		cell: HauntCell,
		d: number,
		split: number,
	) => {
		if (d <= 0 || d >= 1) return;
		const s = SYMBOL_SIZE;
		const half = s / 2;
		const fade = 1 - d;

		// flash wash over the whole cell, hottest at the first instant
		graphics.roundRect(-half - 5, -half - 5, s + 10, s + 10, 13);
		graphics.fill({ color: 0xf3e9ff, alpha: 0.8 * fade * fade });
		graphics.roundRect(-half, -half, s, s, 10);
		graphics.fill({ color: 0xb887ff, alpha: 0.25 * fade });

		// single crisp shockwave: white core ring inside a soft violet halo
		const ringRadius = s * (0.22 + 0.9 * d);
		graphics.circle(0, 0, ringRadius * 0.92);
		graphics.stroke({ color: 0xb887ff, width: 8 * fade + 1, alpha: 0.4 * fade });
		graphics.circle(0, 0, ringRadius);
		graphics.stroke({ color: 0xffffff, width: 3 * fade + 0.5, alpha: 0.8 * fade });

		// sparks flung sideways off each parting seam
		for (let seamIndex = 0; seamIndex < cell.count - 1; seamIndex++) {
			const seamX = (-half + ((seamIndex + 1) / cell.count) * s) * split;
			for (let k = 0; k < 6; k++) {
				const sparkSeed = cell.seed * 17 + seamIndex * 71 + k * 13;
				const side = rand(sparkSeed) > 0.5 ? 1 : -1;
				const y0 = (rand(sparkSeed + 1) - 0.5) * s * 0.8;
				const speed = 35 + rand(sparkSeed + 2) * 55;
				const vx = side * speed;
				const vy = (rand(sparkSeed + 3) - 0.5) * 24 + 70 * d;
				const x = seamX + vx * d;
				const y = y0 + vy * d * 0.5;
				const vlen = Math.sqrt(vx * vx + vy * vy) || 1;
				const tail = (6 + rand(sparkSeed + 4) * 8) * fade;
				graphics.moveTo(x, y);
				graphics.lineTo(x - (vx / vlen) * tail, y - (vy / vlen) * tail);
				graphics.stroke({
					color: k % 3 === 0 ? 0xffffff : 0xe6d2ff,
					width: 1.4,
					alpha: 0.85 * fade,
				});
			}
		}
	};

</script>

<MainContainer>
	<!-- ghost markers during the spin: surviving haunted cells keep their frame
		and count on the field while the reels spin beneath them, so the next
		symbol visibly drops INTO an already-split position -->
	{#if !show && ghosts.length > 0}
		{#each ghosts as ghost (ghost.key)}
			<Container x={ghost.cx} y={ghost.cy} alpha={0.75}>
				<Graphics draw={(graphics) => drawHauntFrame(graphics, ghost, time)} />
				<Container x={SYMBOL_SIZE / 2 - 21} y={-SYMBOL_SIZE / 2 + 21}>
					<Graphics draw={(graphics) => drawBadge(graphics, true)} />
					<Text
						anchor={0.5}
						text={`X${ghost.count}`}
						style={{
							fontFamily: 'Arial',
							fontWeight: '900',
							fontSize: 20,
							fill: 0xffffff,
							stroke: { color: 0x000000, width: 3 },
						}}
					/>
				</Container>
			</Container>
		{/each}
	{/if}
	{#if show}
		<Container x={stateShake.x} y={stateShake.y}>
		{#each cells as cell (cell.key)}
			{@const sliceWidth = SYMBOL_SIZE / cell.count}
			{@const symbolInfo = getSymbolInfo({
				// postWinStatic is the guaranteed-sprite card state (static now
				// routes to the looping Spine idle, which panes can't slice)
				rawSymbol: { name: cell.name },
				state: 'postWinStatic',
			})}
			{@const isHigh = HIGH_SYMBOLS.includes(cell.name)}
			<!-- split = 0: all panes stack centered with a full-width mask, reading
				as one whole symbol; split = 1: panes at their final offsets with
				slice-width masks. Animating it makes the symbol visibly crack apart. -->
			{@const split = splittingKeys.has(cell.key) ? splitProgress.current : 1}
			{@const paneWidth = Math.max(
				(sliceWidth - SYMBOL_SIZE * 0.025) * split + SYMBOL_SIZE * (1 - split),
				2,
			)}
			<Container
				x={cell.cx}
				y={cell.cy}
				rotation={cell.rotation}
				scale={cell.scale *
					(pulsedKeys.has(cell.key) ? pulseScale.current : 1) *
					(winningKeys.has(cell.key) ? winScale.current : 1)}
			>
				<Graphics draw={(graphics) => drawUnderGlow(graphics)} />
				{#each Array.from({ length: cell.count }) as _, i (i)}
					{@const paneX = (-SYMBOL_SIZE / 2 + (i + 0.5) * sliceWidth) * split}
					<Container x={paneX}>
						<Rectangle isMask anchor={0.5} width={paneWidth} height={SYMBOL_SIZE} />
						<SymbolSprite {symbolInfo} />
					</Container>
					<Container x={paneX}>
						<Graphics draw={(graphics) => drawPaneBorder(graphics, paneWidth, isHigh)} />
					</Container>
				{/each}
				{#each Array.from({ length: cell.count - 1 }) as _, i (i)}
					<Container x={(-SYMBOL_SIZE / 2 + (i + 1) * sliceWidth) * split} alpha={split}>
						<Graphics draw={(graphics) => drawDivider(graphics, cell, i, time)} />
					</Container>
				{/each}
				<!-- cut blades sweep down the future seam lines while the symbol is
					still whole, then the carved trails dissolve as the panes part -->
				{#if splittingKeys.has(cell.key)}
					{@const nDividers = cell.count - 1}
					{#each Array.from({ length: nDividers }) as _, i (i)}
						{@const sweep = Math.min(
							Math.max(cutSweep.current * (1 + 0.15 * (nDividers - 1)) - 0.15 * i, 0),
							1,
						)}
						<Container x={-SYMBOL_SIZE / 2 + (i + 1) * sliceWidth} alpha={1 - split * 0.9}>
							<Graphics
								draw={(graphics) => drawCutBlade(graphics, cell, i, sweep, time)}
							/>
						</Container>
					{/each}
					<!-- hit-stop: the carved seams burn white-hot for a frozen beat -->
					{#each Array.from({ length: nDividers }) as _, i (i)}
						<Container x={-SYMBOL_SIZE / 2 + (i + 1) * sliceWidth}>
							<Graphics draw={(graphics) => drawSeamFlare(graphics, seamFlare.current)} />
						</Container>
					{/each}
				{/if}
				<!-- persistent-haunt frame + apparition count badge: the split state
					stays readable at rest, and cells that survive into the next
					spin (bonus 2/3) visibly burn instead of flickering out -->
				{@const persistent = cell.ttl !== undefined && (cell.ttl === -1 || cell.ttl >= 2)}
				<Container alpha={split}>
					<Graphics draw={(graphics) => drawHauntFrame(graphics, cell, time)} />
					<Container x={SYMBOL_SIZE / 2 - 21} y={-SYMBOL_SIZE / 2 + 21}>
						<Graphics draw={(graphics) => drawBadge(graphics, persistent)} />
						<Text
							anchor={0.5}
							text={`X${cell.count}`}
							style={{
								fontFamily: 'Arial',
								fontWeight: '900',
								fontSize: 20,
								fill: 0xffffff,
								stroke: { color: 0x000000, width: 3 },
							}}
						/>
					</Container>
				</Container>
				<!-- detonation: flash + shockwaves + seam sparks + plasma smoke -->
				{#if detonatingKeys.has(cell.key)}
					<Container>
						<Graphics
							draw={(graphics) => drawDetonation(graphics, cell, detonation.current, split)}
						/>
					</Container>
				{/if}
			</Container>
		{/each}
		</Container>
	{/if}
</MainContainer>
