<script lang="ts">
	/**
	 * The boarded-up cover over the LAST-REEL LANE.
	 *
	 * The lane is locked on every base/small-bonus spin: this opaque plank +
	 * chain + padlock cover sits over the whole cell, so the reel streaking
	 * beneath is never seen. It blasts away when the lane opens (DIG UP mid-
	 * spin, or the super bonus for the whole round — stateGame.lidOpen) and
	 * slams back shut on the next locked reveal.
	 *
	 * Purely state-driven: bookEventHandlerMap flips stateGame.lidOpen, this
	 * component only animates the transition it observes.
	 */
	import { Tween } from 'svelte/motion';
	import { backOut, cubicIn } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { CELL_PITCH_X, SYMBOL_SIZE } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { stateShake } from '../game/stateShake.svelte';
	import { fxDur } from '../game/fxTiming';

	const context = getContext();

	const LAST = context.stateGame.board.length - 1;
	/** slight overhang past the cell so the reel never peeks around the boards */
	const COVER_W = CELL_PITCH_X * 1.05;
	const COVER_H = SYMBOL_SIZE * 1.05;

	/** 1 = boarded shut (rest), 0 = blasted clear. Over 1 = the pre-blast strain. */
	const shut = new Tween(1, { duration: 0 });
	let visible = $state(true);
	let wasOpen = context.stateGame.lidOpen;

	$effect(() => {
		const open = context.stateGame.lidOpen;
		if (open === wasOpen) return;
		wasOpen = open;
		if (open) {
			// BLAST OFF: a short strain, then the cover kicks up and away
			visible = true;
			(async () => {
				await shut.set(1.07, { duration: fxDur(90) });
				await shut.set(0, { duration: fxDur(340), easing: cubicIn });
				visible = false;
			})();
		} else {
			// RELOCK: the boards drop back over the lane with a slam
			visible = true;
			shut.set(0.35, { duration: 0 });
			shut.set(1, { duration: fxDur(280), easing: backOut });
		}
	});

	const boardLayout = $derived(context.stateGameDerived.boardLayout());
	const originX = $derived(boardLayout.x - boardLayout.width * 0.5);
	const originY = $derived(boardLayout.y - boardLayout.height * 0.5);
	// the lane is 1 visible row: padded row 1
	const cx = $derived(originX + getSymbolX(LAST));
	const cy = $derived(originY + getCellCenterY(LAST, 1));

	/** blast-off read of the tween: lift, tip and thin out as it goes */
	const t = $derived(Math.min(1, Math.max(0, shut.current)));
	const strain = $derived(Math.max(0, shut.current - 1));
	const lift = $derived((1 - t) * -SYMBOL_SIZE * 0.9);
	const tip = $derived((1 - t) * -0.22 + strain * 0.05);
	const fade = $derived(t < 0.35 ? t / 0.35 : 1);
</script>

{#if visible}
	<MainContainer>
		<Container x={stateShake.x} y={stateShake.y}>
			<Sprite
				key="laneLidLock"
				x={cx}
				y={cy + lift}
				anchor={0.5}
				width={COVER_W * (1 + strain * 0.6)}
				height={COVER_H * (1 + strain * 0.6)}
				rotation={tip}
				alpha={fade}
				eventMode="none"
			/>
		</Container>
	</MainContainer>
{/if}
