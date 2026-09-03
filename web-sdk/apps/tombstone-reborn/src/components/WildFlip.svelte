<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	/** One card yaws. Face + plate swap on the back so the change is hidden. */
	export type EmitterEventWildFlip =
		| {
				type: 'wildFlipShow';
				cells: { reel: number; row: number; from: SymbolName }[];
				shoot?: boolean;
		  }
		| { type: 'wildFlipHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container } from 'pixi-svelte';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { filterVisibleCells } from '../game/boardCells';
	import { fxDur } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import {
		isHighPaySymbol,
		isLowPaySymbol,
		isSpinnerBack,
		spinnerFaceScale,
		spinnerSpinTo,
		usesHighPayPlate,
	} from '../game/gunsmokeSpin';
	import { shakeBoard } from '../game/stateShake.svelte';
	import CellClipMask from './CellClipMask.svelte';
	import HighPayBg from './HighPayBg.svelte';
	import LowPayBg from './LowPayBg.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	type Cell = { key: string; reel: number; row: number; from: SymbolName };

	let cells = $state<Cell[]>([]);
	let show = $state(false);
	let swapped = $state(false);
	const spin = new Tween(0);
	const fallOut = new Tween(0);

	const placed = $derived.by(() => {
		const yaw = spin.current;
		const face = spinnerFaceScale(yaw);
		const wild = swapped || isSpinnerBack(yaw);
		return cells.map((cell) => {
			const name = (wild ? 'W' : cell.from) as SymbolName;
			return {
				...cell,
				cx: getSymbolX(cell.reel),
				cy: getCellCenterY(cell.reel, cell.row),
				sx: face.x,
				sy: face.y,
				name,
				low: isLowPaySymbol(name),
				highPlate: usesHighPayPlate(name),
				hat: isHighPaySymbol(name),
			};
		});
	});

	$effect(() => {
		if (!show || swapped) return;
		if (isSpinnerBack(spin.current)) swapped = true;
	});

	const runSpin = async (asShot: boolean) => {
		spin.set(0, { duration: 0 });
		swapped = false;
		show = true;
		if (asShot) {
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_gunshot' });
			shakeBoard({ intensity: Math.min(7 + cells.length, 14), duration: fxDur(160) });
		} else {
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_ember_whoosh' });
		}
		await spin.set(spinnerSpinTo, { duration: fxDur(640), easing: cubicOut });
		clear();
	};

	const run = async (
		incoming: { reel: number; row: number; from: SymbolName }[],
		asShot: boolean,
	) => {
		const visible = filterVisibleCells(incoming);
		if (!visible.length) return;
		cells = visible.map((c) => ({
			key: `${c.reel}-${c.row}`,
			reel: c.reel,
			row: c.row,
			from: c.from,
		}));
		fallOut.set(0, { duration: 0 });
		await runSpin(asShot);
	};

	const clear = () => {
		show = false;
		cells = [];
		swapped = false;
		spin.set(0, { duration: 0 });
		fallOut.set(0, { duration: 0 });
		context.stateGame.wildFlipCover = [];
	};

	context.eventEmitter.subscribeOnMount({
		wildFlipShow: async ({ cells: incoming, shoot: asShot }) => {
			await run(incoming, !!asShot);
		},
		wildFlipHide: () => clear(),
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, show && cells.length > 0);
			clear();
		},
	});
</script>

<MainContainer>
	{#if show && cells.length}
		<BoardSpace yOffset={fallOut.current}>
			{#each placed as cell (cell.key)}
				<Container x={cell.cx} y={cell.cy} eventMode="none">
					<Container scale={{ x: cell.sx, y: cell.sy }} eventMode="none">
						{#if cell.highPlate}
							<HighPayBg reelIndex={cell.reel} />
						{:else if cell.low}
							<LowPayBg reelIndex={cell.reel} />
						{/if}
						<Container eventMode="none">
							<CellClipMask reelIndex={cell.reel} openHat={cell.hat} />
							<SymbolSprite
								symbolInfo={getSymbolInfo({
									rawSymbol: { name: cell.name },
									state: 'postWinStatic',
								})}
							/>
						</Container>
					</Container>
				</Container>
			{/each}
		</BoardSpace>
	{/if}
</MainContainer>
