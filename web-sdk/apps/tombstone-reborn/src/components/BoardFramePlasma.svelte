<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';
	import { stateShake } from '../game/stateShake.svelte';
	import { fxNum } from '../game/fx.generated';
	import { drawLanternFrame, GRAVEYARD_PALETTE } from '../game/graveyardFx';

	const context = getContext();
	const POSITION_ADJUSTMENT = 1.01;

	// KILLED 2026-07-24: unmounted from Game.svelte. Dashed freegame lip was
	// BAKED into mirror_frame_wide.png (quilt stitches), not this overlay.
	// Component kept only so FX stories/types do not break; never draws.
	const KILLED = true;
	const ENVELOPE_MS = fxNum('framePlasma', 'envelopeMs', 280);
	const TUBE_WIDTH = fxNum('framePlasma', 'tubeWidth', 6);
	const FLICKER_HZ = fxNum('framePlasma', 'flickerHz', 11);
	const SEGMENT_GAP = fxNum('framePlasma', 'segmentGap', 14); // unused by draw (compat)
	const BLACKOUT = fxNum('framePlasma', 'blackoutChance', 0.05);
	const MARGIN_SCALE = fxNum('framePlasma', 'marginScale', 0.12);

	const frameX = $derived(
		context.stateGameDerived.boardLayout().x * POSITION_ADJUSTMENT + stateShake.x,
	);
	const frameY = $derived(
		context.stateGameDerived.boardLayout().y * POSITION_ADJUSTMENT + stateShake.y,
	);

	// The generated framePlasma.colors entry is still the old clinical grey/white
	// set. It is deliberately not consumed: this frame is graveyard lantern light.
	const PALETTE = GRAVEYARD_PALETTE;

	const envelope = new Tween(0, { duration: ENVELOPE_MS, easing: cubicOut });
	let glowActive = $state(false);
	let time = $state(0);

	context.eventEmitter.subscribeOnMount({
		boardFrameGlowShow: () => {
			if (KILLED) return;
			glowActive = true;
			envelope.set(1);
		},
		boardFrameGlowHide: async () => {
			if (KILLED) {
				glowActive = false;
				return;
			}
			await envelope.set(0);
			glowActive = false;
		},
	});

	$effect(() => {
		if (KILLED || !glowActive) return;
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<MainContainer>
	{#if glowActive}
		{@const bw = context.stateGameDerived.boardLayout().width}
		{@const bh = context.stateGameDerived.boardLayout().height}
		<Container x={frameX} y={frameY}>
			<Graphics
				draw={(graphics) =>
					drawLanternFrame(
						graphics,
						bw * 0.5 + SYMBOL_SIZE * MARGIN_SCALE,
						bh * 0.5 + SYMBOL_SIZE * MARGIN_SCALE,
						PALETTE,
						{
							time,
							alpha: envelope.current,
							tubeWidth: TUBE_WIDTH,
							flickerHz: FLICKER_HZ,
							segmentGap: SEGMENT_GAP,
							blackoutChance: BLACKOUT,
						},
					)}
			/>
		</Container>
	{/if}
</MainContainer>
