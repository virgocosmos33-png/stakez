<script lang="ts">
	/**
	 * Particle fire locked to the burning pockets on the super plate.
	 * Lives in SCENE_ART space so cover-fit keeps it on the painted flames.
	 */
	import { onMount } from 'svelte';
	import { Texture, Sprite, Container as PixiContainer } from 'pixi.js';
	import { getContextParent } from 'pixi-svelte';

	import { FIRE_PALETTE, SUPER_FIRE_POCKETS, fireScene } from '../game/superFire';

	const parent = getContextParent();
	const W = fireScene.width;
	const H = fireScene.height;

	const hexRgb = (hex: string) => [
		parseInt(hex.slice(1, 3), 16),
		parseInt(hex.slice(3, 5), 16),
		parseInt(hex.slice(5, 7), 16),
	] as const;

	const PAL = FIRE_PALETTE.map(hexRgb);

	const lerpColor = (t: number) => {
		const u = Math.min(Math.max(t, 0), 0.9999);
		const n = PAL.length - 1;
		const idx = u * n;
		const i0 = Math.floor(idx);
		const i1 = Math.min(i0 + 1, n);
		const f = idx - i0;
		const a = PAL[i0];
		const b = PAL[i1];
		return (
			(Math.round(a[0] + (b[0] - a[0]) * f) << 16) |
			(Math.round(a[1] + (b[1] - a[1]) * f) << 8) |
			Math.round(a[2] + (b[2] - a[2]) * f)
		);
	};

	const hash12 = (x: number, y: number) => {
		let n = Math.sin(x * 127.1 + y * 311.7) * 43758.5453;
		return n - Math.floor(n);
	};

	const noise2 = (x: number, y: number) => {
		const ix = Math.floor(x);
		const iy = Math.floor(y);
		const fx = x - ix;
		const fy = y - iy;
		const u = fx * fx * (3 - 2 * fx);
		const v = fy * fy * (3 - 2 * fy);
		const a = hash12(ix, iy);
		const b = hash12(ix + 1, iy);
		const c = hash12(ix, iy + 1);
		const d = hash12(ix + 1, iy + 1);
		return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
	};

	const blobTex = (() => {
		const s = 64;
		const c = document.createElement('canvas');
		c.width = s;
		c.height = s;
		const ctx = c.getContext('2d');
		if (!ctx) return Texture.WHITE;
		const g = ctx.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
		g.addColorStop(0, 'rgba(255,255,255,1)');
		g.addColorStop(0.45, 'rgba(255,255,255,0.5)');
		g.addColorStop(1, 'rgba(255,255,255,0)');
		ctx.fillStyle = g;
		ctx.fillRect(0, 0, s, s);
		return Texture.from(c);
	})();

	type Ember = {
		x: number;
		y: number;
		vx: number;
		vy: number;
		life: number;
		maxLife: number;
		size: number;
		wobble: number;
		wobbleSpeed: number;
		seed: number;
		pocket: number;
	};

	const rand = (a: number, b: number) => a + Math.random() * (b - a);
	const SPEED = 0.42;

	const spawn = (pocket: number): Ember => {
		const p = SUPER_FIRE_POCKETS[pocket];
		return {
			x: (p.cx + rand(-0.5, 0.5) * p.w) * W,
			y: p.cy * H + rand(0, 8),
			vx: rand(-0.08, 0.08) * SPEED,
			vy: rand(-1.15, -0.65) * p.rise * SPEED,
			life: 0,
			maxLife: rand(110, 210) / Math.max(p.rise, 0.5),
			size: p.size * rand(0.7, 1.15),
			wobble: rand(0, Math.PI * 2),
			wobbleSpeed: rand(0.008, 0.022),
			seed: Math.random() * 1000,
			pocket,
		};
	};

	const embers: Ember[] = [];
	for (let i = 0; i < SUPER_FIRE_POCKETS.length; i += 1) {
		for (let n = 0; n < SUPER_FIRE_POCKETS[i].n; n += 1) embers.push(spawn(i));
	}

	const layer = new PixiContainer();
	layer.eventMode = 'none';
	layer.blendMode = 'add';
	const sprites = embers.map(() => {
		const s = new Sprite(blobTex);
		s.anchor.set(0.5);
		s.blendMode = 'add';
		s.eventMode = 'none';
		layer.addChild(s);
		return s;
	});
	layer.zIndex = 8;
	parent.addToParent(layer);

	onMount(() => {
		let raf = 0;
		let lastDraw = 0;
		let prev = performance.now();
		const tick = (now: number) => {
			const dt = Math.min((now - prev) / 16.6667, 3);
			prev = now;
			for (let i = 0; i < embers.length; i += 1) {
				const e = embers[i];
				const pocket = SUPER_FIRE_POCKETS[e.pocket];
				e.life += dt;
				const t = e.life / e.maxLife;
				if (t >= 1) {
					embers[i] = spawn(e.pocket);
					continue;
				}
				const n = (noise2(e.x * 0.004 + e.seed, e.y * 0.004 - e.life * 0.008) - 0.5) * 2;
				e.vx += n * 0.1 * SPEED;
				e.vx *= 0.985;
				e.wobble += e.wobbleSpeed;
				e.x += (e.vx + Math.sin(e.wobble) * 0.16) * dt;
				e.y += e.vy * pocket.rise * dt;
			}
			if (now - lastDraw >= 33) {
				lastDraw = now;
				for (let i = 0; i < embers.length; i += 1) {
					const e = embers[i];
					const t = e.life / e.maxLife;
					const sizeT = Math.sin(t * Math.PI);
					const radius = Math.max(2, e.size * (0.32 + sizeT * 0.8));
					const alpha = Math.max(0, (1 - t) * 0.72 * sizeT + (1 - t) * 0.12);
					const spr = sprites[i];
					spr.x = e.x;
					spr.y = e.y;
					spr.scale.set(radius / 32);
					spr.alpha = alpha;
					spr.tint = lerpColor(t);
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
