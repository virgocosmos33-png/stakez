<script lang="ts">
	/**
	 * Street smoke from TR2-Spine-Background-scene/fx/smoke-element.png.
	 * Viewer panel: smoke ON, fire OFF, density 8, speed 1.00x.
	 * On in base and bonus.
	 */
	import { onMount } from 'svelte';
	import { Sprite, Container as PixiContainer, type Texture } from 'pixi.js';
	import { getContextParent } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SCENE_ART } from '../game/saloonLamps';
	import { WESTERN_SCENE_FX } from '../game/westernScene';

	const context = getContext();
	const parent = getContextParent();
	const sx = SCENE_ART.width / WESTERN_SCENE_FX.viewW;
	const sy = SCENE_ART.height / WESTERN_SCENE_FX.viewH;

	type Smoke = {
		depth: number;
		x: number;
		y: number;
		size: number;
		vx: number;
		vy: number;
		rot: number;
		spin: number;
		alpha: number;
	};

	const resetSmoke = (p: Smoke, seed: boolean) => {
		const depth = 0.22 + Math.random() * 0.78;
		p.depth = depth;
		p.x = seed
			? WESTERN_SCENE_FX.viewW * (0.04 + Math.random() * 0.92)
			: WESTERN_SCENE_FX.viewW + 40 + Math.random() * 80;
		p.y = WESTERN_SCENE_FX.viewH * (0.58 + depth * 0.34);
		p.size = 170 + depth * 190;
		p.vx = -11 - depth * 9;
		p.vy = -2.2 - depth * 2.6;
		p.rot = Math.random() * Math.PI * 2;
		p.spin = (Math.random() - 0.5) * 0.18;
		p.alpha = 0.11 + depth * 0.1;
	};

	const smoke: Smoke[] = [];
	for (let i = 0; i < WESTERN_SCENE_FX.density; i += 1) {
		const p = {} as Smoke;
		resetSmoke(p, true);
		smoke.push(p);
	}

	const layer = new PixiContainer();
	layer.eventMode = 'none';
	layer.zIndex = 0.5;
	layer.visible = WESTERN_SCENE_FX.smoke;

	const smokeSprites: Sprite[] = [];

	const bindSprites = () => {
		const smokeTex = context.stateApp.loadedAssets?.westernSceneSmoke as Texture | undefined;
		if (!smokeTex) return false;
		if (smokeSprites.length === 0) {
			for (let i = 0; i < smoke.length; i += 1) {
				const spr = new Sprite(smokeTex);
				spr.anchor.set(0.5);
				spr.blendMode = 'add';
				spr.eventMode = 'none';
				layer.addChild(spr);
				smokeSprites.push(spr);
			}
		}
		return true;
	};

	parent.addToParent(layer);

	onMount(() => {
		let raf = 0;
		let prev = performance.now();
		const tick = (now: number) => {
			const dt = Math.min(0.033, (now - prev) / 1000) * WESTERN_SCENE_FX.speed;
			prev = now;
			if (!WESTERN_SCENE_FX.smoke || !bindSprites()) {
				raf = requestAnimationFrame(tick);
				return;
			}
			for (let i = 0; i < smoke.length; i += 1) {
				const p = smoke[i];
				p.x += p.vx * dt;
				p.y += p.vy * dt;
				p.rot += p.spin * dt;
				if (p.x < -p.size * 0.45 || p.y < WESTERN_SCENE_FX.viewH * 0.5) resetSmoke(p, false);
				const spr = smokeSprites[i];
				const s = p.size * sx;
				spr.x = p.x * sx;
				spr.y = p.y * sy;
				spr.width = s;
				spr.height = s;
				spr.rotation = p.rot;
				spr.alpha = p.alpha;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>
