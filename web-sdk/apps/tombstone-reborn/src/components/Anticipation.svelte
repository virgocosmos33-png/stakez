<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Graphics } from 'pixi-svelte';
	import { stateBetDerived } from 'state-shared';

	import type { Reel } from '../game/stateGame.svelte';
	import { SYMBOL_SIZE, CELL_PITCH_X } from '../game/constants';
	import { getReelRows, getReelYOffset, getSymbolX } from '../game/utils';
	import { drawDustAnticipation } from '../game/tombstoneVfx';

	type Props = {
		reel: Reel;
		/** position on the board grid — reel.reelIndex is a STAGGER slot now
		 * (shifted +1 so the left special column drops first), never a position */
		reelIndex: number;
		oncomplete: () => void;
	};

	const props: Props = $props();

	// Sit on THIS reel's window. Board-centre + authored height put a dark
	// shaft over the boarded lane and the short diamond steps.
	const COL_W = CELL_PITCH_X;
	const colH = $derived(SYMBOL_SIZE * getReelRows(props.reelIndex));
	const colY = $derived(getReelYOffset(props.reelIndex) + colH / 2);

	const IN_DURATION = 0.18;
	const OUT_DURATION = 0.22;

	let time = $state(0);
	let envelope = $state(0);
	let phase: 'in' | 'loop' | 'out' = 'in';
	let phaseStart = 0;
	let completed = false;

	$effect(() => {
		if (props.reel.reelState.motion === 'stopped' && phase !== 'out') {
			phase = 'out';
			phaseStart = time;
		}
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			const t = (now - start) / 1000;
			time = t;
			const speed = stateBetDerived.timeScale();
			if (phase === 'in') {
				const f = Math.min(((t - phaseStart) * speed) / IN_DURATION, 1);
				envelope = f;
				if (f >= 1) phase = 'loop';
			} else if (phase === 'out') {
				const f = Math.min(((t - phaseStart) * speed) / OUT_DURATION, 1);
				envelope = 1 - f;
				if (f >= 1 && !completed) {
					completed = true;
					props.oncomplete();
				}
			} else {
				envelope = 1;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<Container x={getSymbolX(props.reelIndex)} y={colY}>
	<Graphics
		draw={(graphics) => drawDustAnticipation(graphics, COL_W, colH, time, envelope)}
	/>
</Container>
