<script lang="ts">
	import { onMount } from 'svelte';
	import { Container, Graphics } from 'pixi-svelte';
	import { stateBetDerived } from 'state-shared';

	import { getContext } from '../game/context';
	import type { Reel } from '../game/stateGame.svelte';
	import { SYMBOL_SIZE, CELL_PITCH_X, NUM_ROWS, MAX_ROWS } from '../game/constants';
	import { getSymbolX } from '../game/utils';
	import { drawDustAnticipation } from '../game/tombstoneVfx';

	type Props = {
		reel: Reel;
		/** position on the board grid — reel.reelIndex is a STAGGER slot now
		 * (shifted +1 so the left special column drops first), never a position */
		reelIndex: number;
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// Tombstone anticipation: dusty gunsmoke shaft + falling grit (not White Room tube).
	const COL_W = CELL_PITCH_X;
	const COL_H = SYMBOL_SIZE * (NUM_ROWS[props.reelIndex] ?? MAX_ROWS);

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

<Container
	x={context.stateGameDerived.boardLayout().x -
		context.stateGameDerived.boardLayout().width * 0.5 +
		getSymbolX(props.reelIndex)}
	y={context.stateGameDerived.boardLayout().y}
>
	<Graphics
		draw={(graphics) => drawDustAnticipation(graphics, COL_W, COL_H, time, envelope)}
	/>
</Container>
