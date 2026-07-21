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
	import * as PIXI from 'pixi.js';
	import { CanvasSizeRectangle } from 'components-layout';
	import { BaseSprite, Container } from 'pixi-svelte';
	import { stateBetDerived } from 'state-shared';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE, BOARD_SIZES } from '../game/constants';
	import { createReactBitsLightning } from '../game/reactBitsLightning';
	import { createPrismaticBurst } from '../game/prismaticBurst';

	const context = getContext();

	const PRISMATIC_Z_INDEX = 120;
	const HUE = 260;
	const SIZE = 1;
	const LIGHTNING_DURATION_MS = 1400;
	const PRISMATIC_DURATION_MS = 2000;
	const MAX_EXTRA_BOLTS = 4;

	type PlannedBolt = { xOffset: number; startT: number; timeSeed: number };

	type GpuLayers = {
		lightningCanvas: HTMLCanvasElement;
		lightningRenderer: ReturnType<typeof createReactBitsLightning>;
		lightningTexture: PIXI.Texture;
		prismatic?: {
			canvas: HTMLCanvasElement;
			renderer: ReturnType<typeof createPrismaticBurst>;
			texture: PIXI.Texture;
		};
	};

	const createGpu = (): GpuLayers | null => {
		try {
			const lightningCanvas = document.createElement('canvas');
			const lightningRenderer = createReactBitsLightning(lightningCanvas);
			const lightningTexture = PIXI.Texture.from({ resource: lightningCanvas, dynamic: true });

			let prismatic: GpuLayers['prismatic'];
			try {
				const canvas = document.createElement('canvas');
				prismatic = {
					canvas,
					renderer: createPrismaticBurst(canvas, {
						intensity: 2.5,
						speed: 0.5,
						animationType: 'rotate3d',
						colors: ['#A855F7', '#7C3AED', '#6366F1'],
						distort: 0,
						rayCount: 0,
					}),
					texture: PIXI.Texture.from({ resource: canvas, dynamic: true }),
				};
			} catch (error) {
				console.warn('PrismaticBurst init failed (WebGL2?):', error);
			}

			return { lightningCanvas, lightningRenderer, lightningTexture, prismatic };
		} catch (error) {
			console.error('WinLightning GPU init failed:', error);
			return null;
		}
	};

	// eager sync init — never wait for onMount (Storybook Action race)
	const gpu = createGpu();

	let active = $state(false);
	let lightningAlpha = $state(0);
	let prismaticAlpha = $state(0);
	let strikeGeneration = 0;

	const canvasSizes = $derived(context.stateLayoutDerived.canvasSizes());

	const nextFrame = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));

	const waitForLayout = async () => {
		for (let i = 0; i < 60; i++) {
			const canvas = context.stateLayoutDerived.canvasSizes();
			const board = context.stateGameDerived.boardLayout();
			if (
				canvas.width > 200 &&
				canvas.height > 200 &&
				board.width >= BOARD_SIZES.width * 0.5
			) {
				return { canvas, board };
			}
			await nextFrame();
		}
		return {
			canvas: context.stateLayoutDerived.canvasSizes(),
			board: context.stateGameDerived.boardLayout(),
		};
	};

	const cellCenter = (position: Position) => {
		const board = context.stateGameDerived.boardLayout();
		const originX = board.x - board.width * 0.5;
		const originY = board.y - board.height * 0.5;
		return {
			x: originX + SYMBOL_SIZE * (position.reel + 0.5),
			y: originY + SYMBOL_SIZE * (position.row - 1 + 0.5),
		};
	};

	const xOffsetForPosition = (position: Position) => {
		const board = context.stateGameDerived.boardLayout();
		const center = cellCenter(position);
		return ((center.x - board.x) / (board.width * 0.5)) * 0.5;
	};

	const boltOffsets = (positions: Position[]) => {
		const board = context.stateGameDerived.boardLayout();
		const targets = positions.map(cellCenter);
		const centroidX = targets.reduce((sum, p) => sum + p.x, 0) / targets.length;
		const base = ((centroidX - board.x) / (board.width * 0.5)) * 0.5;
		return { first: base - 0.48, second: base + 0.52 };
	};

	const planBolts = (winGroups: Position[][]): PlannedBolt[] => {
		const primary = winGroups[0] ?? [];
		if (primary.length === 0) return [];

		const { first, second } = boltOffsets(primary);
		const bolts: PlannedBolt[] = [
			{ xOffset: first, startT: 0, timeSeed: 0 },
			{ xOffset: second, startT: 0.34, timeSeed: 3.1 },
		];

		const usedOffsets = new Set(bolts.map((bolt) => Math.round(bolt.xOffset * 100)));
		const addOffset = (xOffset: number, startT: number, timeSeed: number) => {
			const key = Math.round(xOffset * 100);
			if (usedOffsets.has(key)) return;
			usedOffsets.add(key);
			bolts.push({ xOffset, startT, timeSeed });
		};

		// other win lines → staggered strikes after bolt 2
		winGroups.slice(1).forEach((group, index) => {
			if (bolts.length >= 2 + MAX_EXTRA_BOLTS) return;
			addOffset(boltOffsets(group).first, 0.52 + index * 0.16, 5.7 + index * 1.9);
		});

		// within the primary line, hit left / mid / right cells after bolt 2
		if (primary.length >= 2) {
			const byReel = [...primary].sort((a, b) => a.reel - b.reel);
			const anchors = [byReel[0]];
			if (byReel.length > 2) anchors.push(byReel[Math.floor(byReel.length / 2)]);
			if (byReel.length > 1) anchors.push(byReel[byReel.length - 1]);

			let extraIndex = 0;
			for (const anchor of anchors) {
				if (bolts.length >= 2 + MAX_EXTRA_BOLTS) break;
				addOffset(
					xOffsetForPosition(anchor),
					0.52 + extraIndex * 0.16,
					6.4 + extraIndex * 2.1,
				);
				extraIndex += 1;
			}
		}

		return bolts;
	};

	const boltEnvelope = (t: number, startT: number, peakDuration = 0.22) => {
		if (t < startT) return 0;
		const local = t - startT;
		const rise = Math.min(local / 0.05, 1);
		const fall =
			local > peakDuration ? Math.max(1 - (local - peakDuration) / 0.14, 0) : 1;
		const flicker = startT === 0 ? 0.82 + 0.18 * Math.sin(t * 38) : 0.8 + 0.2 * Math.sin(local * 52 + 2.1);
		return rise * fall * flicker;
	};

	const prismaticEnvelope = (t: number) => {
		const rise = Math.min(t / 0.2, 1);
		const fall = t > 1.5 ? Math.max(1 - (t - 1.5) / 0.5, 0) : 1;
		return rise * fall;
	};

	const refreshTexture = (texture: PIXI.Texture, canvas: HTMLCanvasElement) => {
		const source = texture.source as PIXI.TextureSource & {
			width?: number;
			height?: number;
			update?: () => void;
		};
		source.width = canvas.width;
		source.height = canvas.height;
		source.update?.();
	};

	const resizeLayers = (canvas: { width: number; height: number }) => {
		if (!gpu) return;
		const dpr = Math.min(window.devicePixelRatio || 1, 2);
		const w = Math.max(canvas.width, BOARD_SIZES.width);
		const h = Math.max(canvas.height, BOARD_SIZES.height);
		gpu.lightningRenderer.resize(w * dpr, h * dpr);
		gpu.prismatic?.renderer.resize(w * dpr, h * dpr);
	};

	const resetFx = () => {
		active = false;
		lightningAlpha = 0;
		prismaticAlpha = 0;
	};

	const strike = async (winGroups: Position[][]) => {
		if (!gpu || winGroups.length === 0) return;

		const generation = ++strikeGeneration;
		const plannedBolts = planBolts(winGroups);

		try {
			const { canvas } = await waitForLayout();
			if (generation !== strikeGeneration) return;

			await nextFrame();
			await nextFrame();
			if (generation !== strikeGeneration) return;

			resizeLayers(canvas);

			const speed = stateBetDerived.timeScale();
			const lightningDurationSec = LIGHTNING_DURATION_MS / speed / 1000;
			const prismaticDurationSec = PRISMATIC_DURATION_MS / speed / 1000;

			gpu.lightningRenderer.renderStrikes([
				{
					uniforms: {
						hue: HUE,
						xOffset: plannedBolts[0]?.xOffset ?? 0,
						speed,
						intensity: 0.01,
						size: SIZE,
					},
					timeSec: 0,
				},
			]);
			refreshTexture(gpu.lightningTexture, gpu.lightningCanvas);
			if (gpu.prismatic) {
				gpu.prismatic.renderer.render(0, 0.15);
				refreshTexture(gpu.prismatic.texture, gpu.prismatic.canvas);
			}

			active = true;
			prismaticAlpha = gpu.prismatic ? 0.15 : 0;

			await new Promise<void>((resolve) => {
				const start = performance.now();
				const tick = (now: number) => {
					if (generation !== strikeGeneration) {
						resolve();
						return;
					}

					const elapsed = (now - start) / 1000;
					const t = elapsed * speed;

					if (elapsed >= prismaticDurationSec) {
						resolve();
						return;
					}

					const prism = prismaticEnvelope(t);
					if (gpu!.prismatic) {
						gpu!.prismatic.renderer.render(t, prism * 0.85);
						refreshTexture(gpu!.prismatic.texture, gpu!.prismatic.canvas);
					}
					prismaticAlpha = Math.min(prism * 0.5, 0.55);

					if (elapsed < lightningDurationSec) {
						let peakAlpha = 0;
						const strikes = plannedBolts.map((bolt, index) => {
							const env = boltEnvelope(t, bolt.startT, index === 0 ? 0.48 : 0.2);
							peakAlpha = Math.max(peakAlpha, env);
							if (env <= 0.01) return null;
							return {
								uniforms: {
									hue: HUE,
									xOffset: bolt.xOffset,
									speed,
									intensity: env * (index === 0 ? 1.35 : 1.15),
									size: SIZE * (index === 1 ? 1.08 : 1),
								},
								timeSec: t + bolt.timeSeed,
							};
						});

						gpu!.lightningRenderer.renderStrikes(strikes);
						refreshTexture(gpu!.lightningTexture, gpu!.lightningCanvas);
						lightningAlpha = Math.min(peakAlpha * 1.1, 1);
					} else {
						lightningAlpha = 0;
					}

					requestAnimationFrame(tick);
				};
				requestAnimationFrame(tick);
			});
		} catch (error) {
			console.error('WinLightning strike failed:', error);
		} finally {
			if (generation === strikeGeneration) {
				resetFx();
			}
		}
	};

	context.eventEmitter.subscribeOnMount({
		winLightning: async ({ winGroups }) => {
			if (!gpu) return;
			await strike(winGroups);
		},
		winCycleStop: () => {
			strikeGeneration += 1;
			resetFx();
		},
	});

	onMount(() => {
		return () => {
			gpu?.lightningRenderer.destroy();
			gpu?.prismatic?.renderer.destroy();
			gpu?.lightningTexture.destroy(true);
			gpu?.prismatic?.texture.destroy(true);
		};
	});
</script>

<!-- full canvas, high z-index so HUD/board layers never cover the burst -->
<Container zIndex={PRISMATIC_Z_INDEX}>
	{#if active && gpu}
		{#if gpu.prismatic}
			<BaseSprite
				texture={gpu.prismatic.texture}
				anchor={0}
				x={0}
				y={0}
				width={canvasSizes.width}
				height={canvasSizes.height}
				alpha={prismaticAlpha}
				blendMode="screen"
				zIndex={0}
			/>
		{:else}
			<CanvasSizeRectangle backgroundColor={0x7c3aed} backgroundAlpha={prismaticAlpha * 0.35} />
		{/if}

		{#if lightningAlpha > 0}
			<BaseSprite
				texture={gpu.lightningTexture}
				anchor={0}
				x={0}
				y={0}
				width={canvasSizes.width}
				height={canvasSizes.height}
				alpha={lightningAlpha}
				blendMode="add"
				zIndex={1}
			/>
		{/if}
	{/if}
</Container>
