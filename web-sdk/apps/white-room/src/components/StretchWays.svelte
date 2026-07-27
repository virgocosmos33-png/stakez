<script lang="ts" module>
	// STRETCH (normal reel): every symbol on the stretched reel gets extra x-ways.
	// Each symbol stretches a little WITHIN its own cell (overflow clipped) and, when
	// its multiplier is > 5, shows a plain "Nx". No wild column, no centred total.
	export type EmitterEventStretchWays =
		| { type: 'stretchWaysShow'; cells: { reel: number; row: number; multiplier: number }[] }
		| { type: 'stretchWaysHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, Rectangle, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolInfo, getReelYOffset } from '../game/utils';
	import { SYMBOL_SIZE } from '../game/constants';
	import { shakeBoard, stateShake } from '../game/stateShake.svelte';
	import type { SymbolName } from '../game/types';

	const context = getContext();

	type WaysCell = {
		key: string;
		reel: number;
		row: number;
		multiplier: number;
		name: SymbolName;
		cx: number;
		cy: number;
		// stretch events fire ONE PER CELL (activation order): symbols from an
		// EARLIER stretch stay elongated (settled) while the new reel animates.
		settled: boolean;
	};

	let cells = $state<WaysCell[]>([]);
	let show = $state(false);
	// 0 = at rest, 1 = stretched (each symbol elongated a little in its cell)
	const stretchT = new Tween(0);
	const badge = new Tween(0);

	const layout = (incoming: { reel: number; row: number; multiplier: number }[]): WaysCell[] => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		const found: WaysCell[] = [];
		for (const c of incoming) {
			const reelSymbol = context.stateGame.board[c.reel]?.reelState.symbols[c.row];
			const name = reelSymbol?.rawSymbol.name as SymbolName | undefined;
			if (!name) continue;
			found.push({
				key: `${c.reel}-${c.row}`,
				reel: c.reel,
				row: c.row,
				multiplier: c.multiplier,
				name,
				cx: originX + (c.reel + 0.5) * SYMBOL_SIZE,
				cy: originY + (c.row - 0.5) * SYMBOL_SIZE + getReelYOffset(c.reel),
				settled: false,
			});
		}
		return found;
	};

	context.eventEmitter.subscribeOnMount({
		stretchWaysShow: async ({ cells: incoming }) => {
			// stretch events fire one per cell: freeze earlier stretched symbols at
			// full elongation (settled) and animate ONLY the new reel's cells.
			const existing = new Set(cells.map((c) => c.key));
			const added = layout(incoming.filter((c) => !existing.has(`${c.reel}-${c.row}`)));
			if (!added.length) return;
			cells = [...cells.map((c) => ({ ...c, settled: true })), ...added];
			show = true;
			stretchT.set(0, { duration: 0 });
			badge.set(0, { duration: 0 });
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_wild_explode' });
			shakeBoard({ intensity: 7, duration: 220 });
			badge.set(1, { duration: 220, easing: backOut });
			await stretchT.set(1, { duration: 460, easing: backOut });
		},
		stretchWaysHide: () => {
			show = false;
			cells = [];
			stretchT.set(0, { duration: 0 });
			badge.set(0, { duration: 0 });
		},
	});
</script>

{#if show}
	<MainContainer>
		<Container x={stateShake.x} y={stateShake.y}>
			{#each cells as cell (cell.key)}
				{@const symbolInfo = getSymbolInfo({ rawSymbol: { name: cell.name }, state: 'postWinStatic' })}
				{@const p = cell.settled ? 1 : stretchT.current}
				<!-- stretch a bit: taller with the bigger multipliers, clipped to the cell
					so it never overflows into its neighbours (overflow hidden). -->
				{@const grow = (0.28 + Math.min(0.4, cell.multiplier * 0.035)) * Math.min(1, p)}
				<Container x={cell.cx} y={cell.cy}>
					<Rectangle isMask anchor={0.5} width={SYMBOL_SIZE} height={SYMBOL_SIZE} backgroundColor={0xffffff} />
					<Sprite
						key={symbolInfo.assetKey}
						anchor={0.5}
						width={SYMBOL_SIZE * symbolInfo.sizeRatios.width}
						height={SYMBOL_SIZE * symbolInfo.sizeRatios.height * (1 + grow)}
					/>
				</Container>
			{/each}
			<!-- only BIG per-symbol multipliers (> 5) get a number, to avoid clutter -->
			{#each cells as cell (cell.key)}
				{#if cell.multiplier > 5}
					{@const bp = cell.settled ? 1 : badge.current}
					<Container x={cell.cx} y={cell.cy} scale={0.7 + 0.3 * bp} alpha={Math.min(1, bp * 1.6)}>
						<Text
							anchor={0.5}
							text={`${cell.multiplier}x`}
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
	</MainContainer>
{/if}
