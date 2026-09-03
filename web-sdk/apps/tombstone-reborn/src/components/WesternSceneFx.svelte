<script lang="ts">
	/**
	 * Street smoke + fire from the Spine scene FX panel (lamp_state.json).
	 * Same step as backgroundSPINE/scene-viewer.html. Not SuperFire.
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
	const fireN = Math.max(8, Math.round(WESTERN_SCENE_FX.density * 0.45));

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

	type Fire = Smoke & {
		hot: boolean;
		life: number;
		max: number;
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

	const resetFire = (p: Fire, seed: boolean) => {
		const depth = 0.28 + Math.random() * 0.72;
		p.depth = depth;
		p.x = seed
			? WESTERN_SCENE_FX.viewW * (0.18 + Math.random() * 0.64)
			: WESTERN_SCENE_FX.viewW * (0.22 + Math.random() * 0.56);
		p.y = WESTERN_SCENE_FX.viewH * (0.72 + depth * 0.22);
		p.size = 22 + depth * 34;
		p.vx = (Math.random() - 0.5) * (8 + depth * 10);
		p.vy = -16 - depth * 22 - Math.random() * 8;
		p.rot = (Math.random() - 0.5) * 0.35;
		p.spin = (Math.random() - 0.5) * 0.12;
		p.alpha = 0.22 + depth * 0.28;
		p.hot = Math.random() > 0.45;
		p.life = seed ? Math.random() * 1.6 : 0;
		p.max = 1.1 + Math.random() * 0.9;
	};

	const smoke: Smoke[] = [];
	for (let i = 0; i < WESTERN_SCENE_FX.density; i += 1) {
		const p = {} as Smoke;
		resetSmoke(p, true);
		smoke.push(p);
	}

	const fire: Fire[] = [];
	for (let i = 0; i < fireN; i += 1) {
		const p = {} as Fire;
		resetFire(p, true);
		fire.push(p);
	}

	const smokeLayer = new PixiContainer();
	smokeLayer.eventMode = 'none';
	smokeLayer.zIndex = 12;
	smokeLayer.visible = WESTERN_SCENE_FX.smoke;

	const fireLayer = new PixiContainer();
	fireLayer.eventMode = 'none';
	fireLayer.zIndex = 13;
	fireLayer.visible = WESTERN_SCENE_FX.fire;

	const smokeSprites: Sprite[] = [];
	const fireSprites: Sprite[] = [];

	const bindSmoke = () => {
		const smokeTex = context.stateApp.loadedAssets?.westernSceneSmoke as Texture | undefined;
		if (!smokeTex) return false;
		if (smokeSprites.length === 0) {
			for (let i = 0; i < smoke.length; i += 1) {
				const spr = new Sprite(smokeTex);
				spr.anchor.set(0.5);
				spr.blendMode = 'add';
				spr.eventMode = 'none';
				smokeLayer.addChild(spr);
				smokeSprites.push(spr);
			}
		}
		return true;
	};

	const bindFire = () => {
		const lick = context.stateApp.loadedAssets?.westernSceneFire as Texture | undefined;
		const hot = context.stateApp.loadedAssets?.westernSceneFireHot as Texture | undefined;
		if (!lick) return false;
		if (fireSprites.length === 0) {
			for (let i = 0; i < fire.length; i += 1) {
				const spr = new Sprite(lick);
				spr.anchor.set(0.5, 0.72);
				spr.eventMode = 'none';
				fireLayer.addChild(spr);
				fireSprites.push(spr);
			}
		}
		return { lick, hot };
	};

	parent.addToParent(smokeLayer);
	parent.addToParent(fireLayer);

	onMount(() => {
		let raf = 0;
		let prev = performance.now();
		const tick = (now: number) => {
			const dt = Math.min(0.033, (now - prev) / 1000) * WESTERN_SCENE_FX.speed;
			prev = now;
			if (WESTERN_SCENE_FX.smoke && bindSmoke()) {
				for (let i = 0; i < smoke.length; i += 1) {
					const p = smoke[i];
					p.x += p.vx * dt;
					p.y += p.vy * dt;
					p.rot += p.spin * dt;
					if (p.x < -p.size * 0.45 || p.y < WESTERN_SCENE_FX.viewH * 0.5) {
						resetSmoke(p, false);
					}
					const spr = smokeSprites[i];
					const s = p.size * sx;
					spr.x = p.x * sx;
					spr.y = p.y * sy;
					spr.width = s;
					spr.height = s;
					spr.rotation = p.rot;
					spr.alpha = p.alpha;
				}
			}
			const fireTex = WESTERN_SCENE_FX.fire ? bindFire() : null;
			if (fireTex) {
				for (let i = 0; i < fire.length; i += 1) {
					const p = fire[i];
					p.life += dt;
					p.x += p.vx * dt;
					p.y += p.vy * dt;
					p.rot += p.spin * dt;
					if (p.life >= p.max || p.y < WESTERN_SCENE_FX.viewH * 0.52) {
						resetFire(p, false);
					}
					const fade =
						p.life < 0.2
							? p.life / 0.2
							: p.life > p.max * 0.75
								? (p.max - p.life) / (p.max * 0.25)
								: 1;
					const spr = fireSprites[i];
					const w = p.size * sx;
					spr.texture = p.hot && fireTex.hot ? fireTex.hot : fireTex.lick;
					spr.x = p.x * sx;
					spr.y = p.y * sy;
					spr.width = w;
					spr.height = w * 1.25;
					spr.rotation = p.rot;
					spr.alpha = p.alpha * Math.max(0, fade);
				}
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => {
			cancelAnimationFrame(raf);
			smokeLayer.parent?.removeChild(smokeLayer);
			fireLayer.parent?.removeChild(fireLayer);
			smokeLayer.destroy({ children: true });
			fireLayer.destroy({ children: true });
		};
	});
</script>
