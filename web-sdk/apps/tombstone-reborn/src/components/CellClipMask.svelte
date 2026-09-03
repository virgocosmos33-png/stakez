<script lang="ts">
	/**
	 * Cell pocket clip.
	 *
	 * Tight (default): gold-frame hole, sides + rounded floor. Lows, spin, gold cards.
	 *
	 * openHat (high-pay spines): T-mask matching the painted green/red.
	 * Green = crown + brim: no clip on the roof or the top-sides (hat sits on
	 * the riveted rail). Red = shoulders down: still the cell pocket.
	 */
	import type { Graphics as PixiGraphics } from 'pixi.js';
	import { Graphics } from 'pixi-svelte';

	import { BREATHE_TOP_FRAC, CELL_PITCH_X, HAT_OPEN_FRAC } from '../game/constants';
	import { getRowPitch } from '../game/utils';
	import { slotFrameHole } from '../game/slotFrame';

	type Props = { reelIndex: number; openHat?: boolean };
	const props: Props = $props();
	const hole = $derived(slotFrameHole(getRowPitch(props.reelIndex)));

	const draw = $derived((g: PixiGraphics) => {
		const hw = hole.w * 0.5;
		const hh = hole.h * 0.5;
		const r = hole.r;
		if (!props.openHat) {
			g.roundRect(-hw, -hh, hole.w, hole.h, r);
			g.fill({ color: 0xffffff });
			return;
		}
		const extraTop = hole.h * BREATHE_TOP_FRAC;
		const extraSide = (CELL_PITCH_X - hole.w) * 0.5;
		const openH = hole.h * HAT_OPEN_FRAC;
		g.roundRect(-hw - extraSide, -hh - extraTop, hole.w + extraSide * 2, extraTop + openH, r);
		g.fill({ color: 0xffffff });
		g.roundRect(-hw, -hh + openH - r, hole.w, hole.h - openH + r, r);
		g.fill({ color: 0xffffff });
	});
</script>

<Graphics isMask draw={draw} />
