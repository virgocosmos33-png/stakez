<script lang="ts">
	/**
	 * Two chain columns per reel, sitting on the iron slots and under the
	 * timber ring + cards. Static — symbols slide over them, so a spin
	 * reads as cards hanging on the chains.
	 */
	import type { Texture } from 'pixi.js';
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { CELL_PITCH_X } from '../game/constants';
	import { getCellLeft, getReelWindow } from '../game/utils';

	const CHAIN_TILE_STEP = 0.84;
	/** Same strip as base. Small/super cuts are shorter and leave mid-air gaps. */
	const CHAIN_KEY = 'hudChain';
	const context = getContext();

	const chainAspect = $derived.by(() => {
		const tex = context.stateApp.loadedAssets?.[CHAIN_KEY] as Texture | undefined;
		if (tex?.width) return tex.height / tex.width;
		return 288 / 56;
	});

	const segs = $derived.by(() => {
		const aspect = chainAspect;
		const out: { id: string; key: string; x: number; y: number; w: number; h: number }[] = [];
		const n = context.stateGame.board.length;
		for (let reel = 0; reel < n; reel += 1) {
			const window = getReelWindow(reel);
			const cx = getCellLeft(reel) + CELL_PITCH_X / 2;
			const colW = Math.max(12, Math.min(CELL_PITCH_X * 0.16, 20));
			const colH = colW * aspect;
			const step = colH * CHAIN_TILE_STEP;
			const inset = CELL_PITCH_X * 0.22;
			const top = window.top - colH * 0.28;
			const bot = window.bottom;
			const copies = Math.max(1, Math.ceil((bot - top) / step) + 1);
			for (let i = 0; i < copies; i += 1) {
				const y = top + i * step;
				if (y >= bot) break;
				out.push({ id: `${reel}-l${i}`, key: CHAIN_KEY, x: cx - inset, y, w: colW, h: colH });
				out.push({ id: `${reel}-r${i}`, key: CHAIN_KEY, x: cx + inset, y, w: colW, h: colH });
			}
		}
		return out;
	});
</script>

{#each segs as seg (seg.id)}
	<Sprite
		key={seg.key}
		x={seg.x}
		y={seg.y}
		anchor={{ x: 0.5, y: 0 }}
		width={seg.w}
		height={seg.h}
		eventMode="none"
	/>
{/each}
