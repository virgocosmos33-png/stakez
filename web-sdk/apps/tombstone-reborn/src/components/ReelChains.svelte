<script lang="ts">
	/**
	 * Irregular chain web INSIDE the reel pockets only. Masked to the
	 * staircase windows so nothing paints in the saloon or past the timber.
	 */
	import type { Graphics as PixiGraphics, Texture } from 'pixi.js';
	import { Container, Graphics, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { BOARD_FRAME_OUTER, CELL_PITCH_X, SYMBOL_SIZE } from '../game/constants';
	import { getCellLeft, getReelWindow, getReelYOffset, getSymbolX } from '../game/utils';

	const CHAIN_TILE_STEP = 0.84;

	/**
	 * Authored from the user's marked-up screenshot — each run is one drawn
	 * line, endpoints snapped to symbol CENTRES (reel, visible row).
	 * Rows per reel: [3,4,4,2,2,1].
	 *
	 *  pink   (0,0)→(2,0)  shallow climb across the top
	 *  red    (1,0)→(2,3)  steep dive through the tall reels
	 *  white  (2,0)→(1,3)  mirrored dive, crossing red
	 *  brown  (0,1)→(5,0)  dead-level run the full board width
	 *  purple (0,1)→(4,1)  slow sag fanning off the brown anchor
	 *  green  (0,2)→(4,0)  long climb from bottom-left to the short reels
	 *  orange (3,0)→(3,1)  vertical link down reel 3
	 *  gold   (4,0)→(4,1)  vertical link down reel 4
	 */
	const LINKS: {
		r0: number;
		row0: number;
		r1: number;
		row1: number;
		thick: number;
		alpha: number;
	}[] = [
		{ r0: 0, row0: 0, r1: 2, row1: 0, thick: 0.95, alpha: 0.9 }, // pink
		{ r0: 1, row0: 0, r1: 2, row1: 3, thick: 1, alpha: 1 }, // red
		{ r0: 2, row0: 0, r1: 1, row1: 3, thick: 1, alpha: 1 }, // white
		{ r0: 0, row0: 1, r1: 5, row1: 0, thick: 0.95, alpha: 0.8 }, // brown
		{ r0: 0, row0: 1, r1: 4, row1: 1, thick: 0.9, alpha: 0.75 }, // purple
		{ r0: 0, row0: 2, r1: 4, row1: 0, thick: 0.95, alpha: 0.85 }, // green
		{ r0: 3, row0: 0, r1: 3, row1: 1, thick: 1, alpha: 1 }, // orange
		{ r0: 4, row0: 0, r1: 4, row1: 1, thick: 1, alpha: 1 }, // gold
	];

	const context = getContext();

	const chainKey = () => {
		const atmo = context.stateGame.atmosphere;
		if (atmo === 'super') return 'hudChainSuper';
		if (atmo === 'small') return 'hudChainSmall';
		return 'hudChain';
	};

	const chainAspect = $derived.by(() => {
		const tex = context.stateApp.loadedAssets?.[chainKey()] as Texture | undefined;
		if (tex?.width) return tex.height / tex.width;
		return 288 / 56;
	});

	/** The baked plank ring overlaps the pockets by BOARD_FRAME_OUTER and
	 * draws ABOVE this layer (z 3), so letting the mask reach that far means
	 * a chain's cut end is always hidden UNDER timber — never a hard stop
	 * on the iron slot border. */
	const MASK_PAD = BOARD_FRAME_OUTER - 4;

	const pockets = $derived.by(() => {
		const n = context.stateGame.board.length;
		return Array.from({ length: n }, (_, reel) => {
			const window = getReelWindow(reel);
			return {
				x: getCellLeft(reel) - MASK_PAD,
				y: window.top - MASK_PAD,
				w: CELL_PITCH_X + MASK_PAD * 2,
				h: Math.max(1, window.bottom - window.top) + MASK_PAD * 2,
			};
		});
	});

	const drawPocketMask = $derived((g: PixiGraphics) => {
		// fill per rect: overlapping padded pockets must UNION, not XOR
		for (const p of pockets) {
			g.rect(p.x, p.y, p.w, p.h);
			g.fill({ color: 0xffffff });
		}
	});

	/** centre of a visible cell (reel, 0-based row) in board-local space */
	const cellCenter = (reel: number, row: number) => ({
		x: getSymbolX(reel),
		y: getReelYOffset(reel) + (row + 0.5) * SYMBOL_SIZE,
	});

	const laid = $derived.by(() => {
		const key = chainKey();
		const aspect = chainAspect;
		const baseW = Math.max(12, Math.min(CELL_PITCH_X * 0.16, 20));

		/** Overshoot past both cell centres so the run reaches the timber;
		 * the pocket mask cuts it exactly at the wood edge. */
		const END_PAD = SYMBOL_SIZE * 1.5;

		const build = (
			id: string,
			x0: number,
			y0: number,
			x1: number,
			y1: number,
			thick: number,
			alpha: number,
		) => {
			const dx = x1 - x0;
			const dy = y1 - y0;
			const len = Math.hypot(dx, dy) || 1;
			const ux = dx / len;
			const uy = dy / len;
			const startX = x0 - ux * END_PAD;
			const startY = y0 - uy * END_PAD;
			const fullLen = len + END_PAD * 2;
			const colW = baseW * thick;
			const colH = colW * aspect;
			const step = colH * CHAIN_TILE_STEP;
			const copies = Math.max(1, Math.ceil(fullLen / step));
			return {
				id,
				key,
				x: startX,
				y: startY,
				// local +y must land on (dx,dy): +y rotated by θ is (-sinθ, cosθ),
				// so θ = atan2(-dx, dy). atan2(dx, dy) mirrored every rightward
				// run to the LEFT — the horizontals flew out of the mask.
				rotation: Math.atan2(-dx, dy),
				w: colW,
				h: colH,
				alpha,
				tiles: Array.from({ length: copies }, (_, i) => ({
					id: `${id}-${i}`,
					y: i * step,
				})),
			};
		};

		return LINKS.map((link, li) => {
			const a = cellCenter(link.r0, link.row0);
			const b = cellCenter(link.r1, link.row1);
			return build(`link-${li}`, a.x, a.y, b.x, b.y, link.thick, link.alpha);
		});
	});
</script>

<Container eventMode="none">
	<Graphics isMask draw={drawPocketMask} />
	<Container>
		{#each laid as run (run.id)}
			<Container x={run.x} y={run.y} rotation={run.rotation} alpha={run.alpha} eventMode="none">
				{#each run.tiles as tile (tile.id)}
					<Sprite
						key={run.key}
						y={tile.y}
						anchor={{ x: 0.5, y: 0 }}
						width={run.w}
						height={run.h}
						eventMode="none"
					/>
				{/each}
			</Container>
		{/each}
	</Container>
</Container>
