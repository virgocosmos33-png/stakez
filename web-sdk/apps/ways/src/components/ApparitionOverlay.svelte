<script lang="ts" module>
	export type EmitterEventApparition =
		| { type: 'apparitionsRefresh' }
		| { type: 'apparitionsHide' }
		| { type: 'apparitionsPulse'; positions: Position[] }
		| { type: 'apparitionsWinGrow'; positions: Position[] }
		| { type: 'apparitionsWinRelease' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle } from 'pixi-svelte';

	import type { Position } from '../game/types';
	import type { RawSymbol } from '../game/types';
	import { getContext } from '../game/context';
	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_SIZE, HIGH_SYMBOLS } from '../game/constants';
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
	let show = $state(false);
	let time = $state(0);
	const pulseScale = new Tween(1);
	let pulsedKeys = $state<Set<string>>(new Set());
	const winScale = new Tween(1);
	let winningKeys = $state<Set<string>>(new Set());
	// split animation: 0 = whole symbol, 1 = fully split into panes
	const splitProgress = new Tween(1);
	let splittingKeys = $state<Set<string>>(new Set());

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

	// the cell shows as one whole symbol, holds a beat, then cracks apart into
	// its panes - the split sfx transient fires exactly when the crack starts
	const runSplit = async (keys: Set<string>) => {
		splittingKeys = keys;
		splitProgress.set(0, { duration: 0 });
		// fire the sfx slightly before the crack: the clip ramps ~50ms to its
		// peak and audio output adds latency, so the impact lands on the split
		await new Promise((resolve) => setTimeout(resolve, 100));
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_xways_split' });
		await new Promise((resolve) => setTimeout(resolve, 50));
		// cubicOut: no overshoot, so the panes slide straight to their final
		// spots without wiggling back inward
		await splitProgress.set(1, { duration: 400, easing: cubicOut });
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
		// persistent haunted cells arriving with the reveal (free games) also
		// crack apart on landing so the split is always seen and heard
		apparitionsRefresh: () => {
			refresh();
			if (cells.length > 0) {
				runSplit(new Set(cells.map((cell) => cell.key)));
			}
		},
		apparitionsHide: () => {
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
		graphics.fill({ color: 0x050d07, alpha: 0.92 });
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
			graphics.stroke({ color: 0x0c1a10, width: 3, alpha: 0.8 });
			graphics.roundRect(-w / 2 + 1.5, -s / 2 + 1.5, w - 3, s - 3, 5);
			graphics.stroke({ color: 0x67d98a, width: 1.5, alpha: 0.55 });
		}
	};

	// energy divider between panes: a slim green lightning spindle - thickest
	// in the middle, tapering and fading toward the ends, with a jagged core
	const drawDivider = (
		graphics: import('pixi.js').Graphics,
		cell: HauntCell,
		dividerIndex: number,
		timeValue: number,
	) => {
		const s = SYMBOL_SIZE;
		const half = s / 2;
		const intensity = Math.min((cell.count - 1) / 3, 1);
		const flicker =
			0.8 + 0.2 * Math.sin(timeValue * 27 + cell.seed * 3 + dividerIndex * 1.7);
		const steps = 16;

		// nested spindles: faint aura -> narrow hot core (kept tight)
		const layers = [
			{ maxWidth: 6 + 2 * intensity, color: 0x2bff66, alpha: 0.18 * flicker },
			{ maxWidth: 3.5 + intensity, color: 0x2bff66, alpha: 0.42 * flicker },
			{ maxWidth: 1.8, color: 0xdfffe8, alpha: 0.9 * flicker },
		];
		for (const layer of layers) {
			const left: [number, number][] = [];
			const right: [number, number][] = [];
			for (let i = 0; i <= steps; i++) {
				const y = -half + (i / steps) * s;
				const taper = Math.pow(Math.max(1 - Math.pow(y / half, 2), 0), 0.75);
				const halfWidth = (layer.maxWidth / 2) * taper;
				left.push([-halfWidth, y]);
				right.push([halfWidth, y]);
			}
			graphics.poly([...left, ...right.reverse()].flat());
			graphics.fill({ color: layer.color, alpha: layer.alpha });
		}

		// jagged lightning core crawling inside the spindle
		const jagSeed = Math.floor(timeValue * 24);
		const jagX = (y: number) => {
			const i = Math.round(((y + half) / s) * steps);
			const taper = Math.max(1 - Math.pow(y / half, 2), 0);
			const noise = rand(jagSeed * 89 + i * 37 + dividerIndex * 53 + cell.seed);
			return (noise - 0.5) * 4.5 * taper;
		};
		let started = false;
		for (let i = 0; i <= steps; i++) {
			const y = -half + (i / steps) * s;
			if (!started) {
				graphics.moveTo(jagX(y), y);
				started = true;
			} else {
				graphics.lineTo(jagX(y), y);
			}
		}
		graphics.stroke({ color: 0xffffff, width: 1.1, alpha: 0.85 * flicker });

		// travelling energy pulse riding the bolt: direction (up/down) and
		// speed are random per divider, with a fading tail behind the head
		const direction = rand(cell.seed * 7 + dividerIndex * 13) > 0.5 ? 1 : -1;
		const travelSpeed = 0.55 + 0.35 * rand(cell.seed * 3 + dividerIndex * 17);
		const phase = rand(cell.seed * 11 + dividerIndex * 23);
		const headP = ((timeValue * travelSpeed + phase) % 1 + 1) % 1;
		const headY = direction === 1 ? -half + headP * s : half - headP * s;
		for (let j = 0; j < 7; j++) {
			const y = headY - direction * j * 5;
			if (y < -half || y > half) continue;
			const taper = Math.max(1 - Math.pow(y / half, 2), 0.15);
			const fade = 1 - j / 7;
			const x = jagX(y);
			// glow halo
			graphics.circle(x, y, (5.5 - j * 0.5) * taper + 1.5);
			graphics.fill({ color: 0x2bff66, alpha: 0.22 * fade });
			// hot core
			graphics.circle(x, y, (2.4 - j * 0.28) * taper + 0.4);
			graphics.fill({ color: j === 0 ? 0xffffff : 0xdfffe8, alpha: 0.9 * fade });
		}
	};
</script>

<MainContainer>
	{#if show}
		{#each cells as cell (cell.key)}
			{@const sliceWidth = SYMBOL_SIZE / cell.count}
			{@const symbolInfo = getSymbolInfo({
				rawSymbol: { name: cell.name },
				state: 'static',
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
			</Container>
		{/each}
	{/if}
</MainContainer>
