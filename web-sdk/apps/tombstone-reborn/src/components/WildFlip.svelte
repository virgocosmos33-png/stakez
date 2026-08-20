<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	/** Card-flip: the old face folds away, the WILD is on the other side.
	 *  `shoot` is SFX + board shake only — the muzzle lives on the GS revolver. */
	export type EmitterEventWildFlip =
		| {
				type: 'wildFlipShow';
				cells: { reel: number; row: number; from: SymbolName }[];
				shoot?: boolean;
				/** Card is the result of a gunshot — reveal sting, not explode. */
				afterShot?: boolean;
		  }
		| { type: 'wildFlipHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicInOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Rectangle } from 'pixi-svelte';
	import { playThemedOnce } from '../game/sfxTheme';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { filterVisibleCells } from '../game/boardCells';
	import { fxDur } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolInfo, getSymbolX, getCellCenterY } from '../game/utils';
	import { SYMBOL_SIZE, CELL_PITCH_X } from '../game/constants';
	import { TOMBSTONE_FX } from '../game/tombstoneVfx';
	import { shakeBoard } from '../game/stateShake.svelte';
	import SymbolSprite from './SymbolSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const FLIP_MS = 420;

	const context = getContext();

	type Cell = { key: string; reel: number; row: number; from: SymbolName; i: number };

	let cells = $state<Cell[]>([]);
	let show = $state(false);
	let afterShot = $state(false);
	const flip = new Tween(0);
	const fallOut = new Tween(0);
	let popped = false;

	const placed = $derived.by(() =>
		cells.map((cell) => {
			const t = flip.current;
			const folded = t < 0.5;
			const sx = folded ? 1 - t * 2 : (t - 0.5) * 2;
			return {
				...cell,
				cx: getSymbolX(cell.reel),
				cy: getCellCenterY(cell.reel, cell.row),
				face: (folded ? cell.from : 'W') as SymbolName,
				sx: Math.max(0.05, sx),
				sy: 1 - 0.14 * Math.sin(t * Math.PI),
			};
		}),
	);

	const run = async (
		incoming: { reel: number; row: number; from: SymbolName }[],
		asShot: boolean,
		fromShot: boolean,
	) => {
		const visible = filterVisibleCells(incoming);
		if (!visible.length) return;
		cells = visible.map((c, i) => ({
			key: `${c.reel}-${c.row}`,
			reel: c.reel,
			row: c.row,
			from: c.from,
			i,
		}));
		popped = false;
		afterShot = fromShot;
		flip.set(0, { duration: 0 });
		fallOut.set(0, { duration: 0 });
		show = true;
		if (asShot) {
			playThemedOnce('sfx_gunshot');
			shakeBoard({ intensity: Math.min(7 + cells.length, 14), duration: fxDur(160) });
		} else if (!fromShot) {
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_ember_whoosh' });
		}
		await flip.set(1, { duration: fxDur(FLIP_MS), easing: cubicInOut });
		clear();
	};

	const clear = () => {
		show = false;
		cells = [];
		afterShot = false;
		flip.set(0, { duration: 0 });
		fallOut.set(0, { duration: 0 });
	};

	context.eventEmitter.subscribeOnMount({
		wildFlipShow: async ({ cells: incoming, shoot: asShot, afterShot: fromShot }) => {
			await run(incoming, !!asShot, !!asShot || !!fromShot);
		},
		wildFlipHide: () => clear(),
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, show && cells.length > 0);
			clear();
		},
	});

	$effect(() => {
		if (!show || popped) return;
		if (placed.some((cell) => flip.current >= 0.5)) {
			popped = true;
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: afterShot ? 'sfx_shot_reveal' : 'sfx_wild_explode',
			});
		}
	});

	const drawBack = (g: import('pixi.js').Graphics) => {
		const w = CELL_PITCH_X;
		const h = SYMBOL_SIZE;
		g.roundRect(-w / 2, -h / 2, w, h, 8);
		g.fill({ color: TOMBSTONE_FX.dark, alpha: 1 });
	};
</script>

<MainContainer>
	{#if show && cells.length}
		<BoardSpace yOffset={fallOut.current}>
			{#each placed as cell (cell.key)}
				<Container x={cell.cx} y={cell.cy}>
					<Container>
						<Rectangle
							isMask
							anchor={0.5}
							width={CELL_PITCH_X}
							height={SYMBOL_SIZE}
							backgroundColor={0xffffff}
						/>
						<Graphics draw={drawBack} />
						<Container scale={{ x: cell.sx, y: cell.sy }}>
							<SymbolSprite
								symbolInfo={getSymbolInfo({
									rawSymbol: { name: cell.face },
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
