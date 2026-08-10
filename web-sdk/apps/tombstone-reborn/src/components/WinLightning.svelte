<script lang="ts" module>
	import type { Position } from '../game/types';

	export type EmitterEventWinLightning = {
		type: 'winLightning';
		winGroups: Position[][];
		winAmount: number;
	};
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { CanvasSizeRectangle } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';
	import { stateBetDerived } from 'state-shared';

	import { getContext } from '../game/context';
	import { BOARD_SIZES } from '../game/constants';
	import { fxNum } from '../game/fx.generated';
	import { drawPowderStrobe } from '../game/tombstoneVfx';

	const context = getContext();

	// Tombstone: powder flash + dust streaks (not White Room fluorescent strobe).
	const STROBE_Z = 120;
	const STROBE_MS = fxNum('winLightning', 'strobeMs', 900);
	const GLITCH_MS = fxNum('winLightning', 'glitchMs', 2400);
	const BAND_COUNT = fxNum('winLightning', 'bandCount', 9);
	const SCANLINE_COUNT = fxNum('winLightning', 'scanlineCount', 22);
	const FLASH_PEAK = fxNum('winLightning', 'flashPeak', 0.85);

	let active = $state(false);
	let strobeAlpha = $state(0);
	let glitchAlpha = $state(0);
	let time = $state(0);
	let strikeGeneration = 0;

	const canvasSizes = $derived(context.stateLayoutDerived.canvasSizes());

	const nextFrame = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));

	const waitForLayout = async () => {
		for (let i = 0; i < 60; i++) {
			const canvas = context.stateLayoutDerived.canvasSizes();
			const board = context.stateGameDerived.boardLayout();
			if (canvas.width > 200 && canvas.height > 200 && board.width >= BOARD_SIZES.width * 0.5) {
				return canvas;
			}
			await nextFrame();
		}
		return context.stateLayoutDerived.canvasSizes();
	};

	const resetFx = () => {
		active = false;
		strobeAlpha = 0;
		glitchAlpha = 0;
	};

	const strike = async (_winGroups: Position[][]) => {
		const generation = ++strikeGeneration;
		try {
			await waitForLayout();
			if (generation !== strikeGeneration) return;

			const speed = stateBetDerived.timeScale();
			const strobeSec = STROBE_MS / speed / 1000;
			const glitchSec = GLITCH_MS / speed / 1000;

			active = true;
			await new Promise<void>((resolve) => {
				const start = performance.now();
				const tick = (now: number) => {
					if (generation !== strikeGeneration) {
						resolve();
						return;
					}
					const elapsed = (now - start) / 1000;
					const t = elapsed * speed;
					time = t;

					if (elapsed >= glitchSec) {
						resolve();
						return;
					}

					// hard powder flash: sharp rise, stutter, cut
					if (elapsed < strobeSec) {
						const local = t / (STROBE_MS / 1000);
						const stutter =
							Math.sin(t * 48) > 0.35 ? 1 : 0.15 + 0.2 * Math.sin(t * 90);
						const envelope = Math.min(local / 0.08, 1) * (1 - Math.max(0, local - 0.55) / 0.45);
						strobeAlpha = Math.min(FLASH_PEAK, envelope * stutter);
					} else {
						strobeAlpha = 0;
					}

					// memory-glitch CRT wipe rides longer than the strobe
					const gRise = Math.min(t / 0.12, 1);
					const gFall = t > glitchSec * 0.7 ? Math.max(1 - (t - glitchSec * 0.7) / (glitchSec * 0.3), 0) : 1;
					glitchAlpha = gRise * gFall * 0.9;

					requestAnimationFrame(tick);
				};
				requestAnimationFrame(tick);
			});
		} catch (error) {
			console.error('Padded-cell whiteout failed:', error);
		} finally {
			if (generation === strikeGeneration) resetFx();
		}
	};

	context.eventEmitter.subscribeOnMount({
		winLightning: async ({ winGroups }) => {
			await strike(winGroups);
		},
		winCycleStop: () => {
			strikeGeneration += 1;
			resetFx();
		},
	});

	onMount(() => () => {
		strikeGeneration += 1;
		resetFx();
	});

	const draw = (graphics: import('pixi.js').Graphics) => {
		if (!active) return;
		drawPowderStrobe(graphics, canvasSizes.width, canvasSizes.height, {
			time,
			strobeAlpha,
			glitchAlpha,
			bandCount: BAND_COUNT,
			scanlineCount: SCANLINE_COUNT,
		});
	};
</script>

<Container zIndex={STROBE_Z}>
	{#if active}
		<CanvasSizeRectangle backgroundColor={0xd4c4a8} backgroundAlpha={strobeAlpha * 0.18} />
		<Graphics draw={draw} />
	{/if}
</Container>
