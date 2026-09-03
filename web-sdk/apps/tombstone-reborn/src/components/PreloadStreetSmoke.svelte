<script lang="ts">
	/**
	 * Dust smoke on the preload street. Same puff as WesternSceneFx
	 * (westernSceneSmoke), no fire, no cell pillars.
	 */
	import { onMount } from 'svelte';
	import { Sprite, Container as PixiContainer, type Texture } from 'pixi.js';
	import { getContextParent } from 'pixi-svelte';

	import { getContext } from '../game/context';

	type Props = {
		width: number;
		height: number;
	};

	const props: Props = $props();
	const context = getContext();
	const parent = getContextParent();

	const PLATE_W = 1536;
	const PLATE_H = 1024;
	const COUNT = 36;
	const SPEED = 1;

	type Puff = {
		x: number;
		y: number;
		size: number;
		vx: number;
		vy: number;
		rot: number;
		spin: number;
		alpha: number;
		depth: number;
	};

	const reset = (p: Puff, seed: boolean) => {
		const depth = 0.22 + Math.random() * 0.78;
		p.depth = depth;
		p.x = seed ? PLATE_W * (0.04 + Math.random() * 0.92) : PLATE_W + 40 + Math.random() * 80;
		p.y = PLATE_H * (0.56 + depth * 0.36);
		p.size = 170 + depth * 190;
		p.vx = -11 - depth * 9;
		p.vy = -2.2 - depth * 2.6;
		p.rot = Math.random() * Math.PI * 2;
		p.spin = (Math.random() - 0.5) * 0.18;
		p.alpha = 0.11 + depth * 0.1;
	};

	const puffs: Puff[] = [];
	for (let i = 0; i < COUNT; i += 1) {
		const p = {} as Puff;
		reset(p, true);
		puffs.push(p);
	}

	const layer = new PixiContainer();
	layer.eventMode = 'none';
	const sprites: Sprite[] = [];

	const bind = () => {
		const tex = context.stateApp.loadedAssets?.westernSceneSmoke as Texture | undefined;
		if (!tex) return false;
		if (sprites.length === 0) {
			for (let i = 0; i < puffs.length; i += 1) {
				const spr = new Sprite(tex);
				spr.anchor.set(0.5);
				spr.blendMode = 'add';
				spr.eventMode = 'none';
				layer.addChild(spr);
				sprites.push(spr);
			}
		}
		return true;
	};

	parent.addToParent(layer);

	onMount(() => {
		let raf = 0;
		let prev = performance.now();
		const tick = (now: number) => {
			const dt = Math.min(0.033, (now - prev) / 1000) * SPEED;
			prev = now;
			if (bind()) {
				const sx = props.width / PLATE_W;
				const sy = props.height / PLATE_H;
				for (let i = 0; i < puffs.length; i += 1) {
					const p = puffs[i];
					p.x += p.vx * dt;
					p.y += p.vy * dt;
					p.rot += p.spin * dt;
					if (p.x < -p.size * 0.45 || p.y < PLATE_H * 0.48) reset(p, false);
					const spr = sprites[i];
					const s = p.size * sx;
					spr.x = p.x * sx;
					spr.y = p.y * sy;
					spr.width = s;
					spr.height = s;
					spr.rotation = p.rot;
					spr.alpha = p.alpha;
				}
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => {
			cancelAnimationFrame(raf);
			layer.parent?.removeChild(layer);
			layer.destroy({ children: true });
		};
	});
</script>
