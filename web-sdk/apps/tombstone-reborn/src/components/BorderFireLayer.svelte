<script lang="ts" module>
	/**
	 * BORDER FIRE LAYER — imperative, pooled port of the user's CodePen "burning
	 * letters" fire, remapped from text pixels to card borders.
	 *
	 * The reference reads as REAL fire because of DENSITY: ~50 spawns per frame
	 * with ~33-frame lifetimes keeps hundreds of soft additive puffs overlapping,
	 * which fuses them into a continuous hot body with yellow-white saturation at
	 * the core. A declarative sprite-per-template-row version can't reach that
	 * count, so this layer owns a plain PIXI.Container of pooled sprites and
	 * steps the exact reference simulation on rAF:
	 *
	 *   init:   spawn on the card outline, ±4px jitter,
	 *           vx = (r−0.5)·1.2, vy = −(1.5 + r·3) px/frame
	 *   update: life −= decay (0.015..0.045), size ×= 0.95, dies at life<=0/size<1
	 *   draw:   soft radial gradient sprite (alpha stops 1 / 0.4 / 0), additive,
	 *           tint rgb(255, 0..140, 0), alpha = life
	 *
	 * The layer stays mounted while the component lives: when the fire douses,
	 * spawning stops but live particles finish their own burn-out naturally.
	 */
	import * as PIXI from 'pixi.js';

	/** the reference's soft glowing flame puff, baked once and tinted per puff */
	let puffTexture: PIXI.Texture | null = null;
	const getPuffTexture = (): PIXI.Texture => {
		if (puffTexture) return puffTexture;
		const size = 64;
		const canvas = document.createElement('canvas');
		canvas.width = canvas.height = size;
		const c = canvas.getContext('2d')!;
		const half = size / 2;
		const grad = c.createRadialGradient(half, half, 0, half, half, half);
		grad.addColorStop(0, 'rgba(255,255,255,1)');
		grad.addColorStop(0.4, 'rgba(255,255,255,0.4)');
		grad.addColorStop(1, 'rgba(255,255,255,0)');
		c.fillStyle = grad;
		c.fillRect(0, 0, size, size);
		puffTexture = PIXI.Texture.from(canvas);
		return puffTexture;
	};

	type FireParticle = {
		sprite: PIXI.Sprite;
		x: number;
		y: number;
		vx: number;
		vy: number;
		life: number;
		decay: number;
		size: number;
	};

	/** hard cap: 12 burning cells × ~14 spawns/frame × ~33 frame lifetime */
	const MAX_PARTICLES = 6000;
	/** reference: 50/frame across one headline ≈ this much per card border */
	const SPAWN_PER_CELL = 14;
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { getContextParent } from 'pixi-svelte';

	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';

	const props: {
		/** burning cell centres, in the parent (MainContainer) space */
		cells: { cx: number; cy: number }[];
		/** ignite × overlay-dim; scales spawn rate and particle alpha */
		burn: number;
	} = $props();

	const HW = SYMBOL_CARD_W / 2;
	const HH = SYMBOL_CARD_H / 2;
	const PERIMETER = 4 * (HW + HH);

	/** point on the card-rect outline at parameter t in 0..1 (the reference's
	 * textPixels sampling, remapped to the border) */
	const borderPoint = (t: number) => {
		let d = t * PERIMETER;
		if (d < SYMBOL_CARD_W) return { x: -HW + d, y: -HH }; // top
		d -= SYMBOL_CARD_W;
		if (d < SYMBOL_CARD_H) return { x: HW, y: -HH + d }; // right
		d -= SYMBOL_CARD_H;
		if (d < SYMBOL_CARD_W) return { x: HW - d, y: HH }; // bottom
		d -= SYMBOL_CARD_W;
		return { x: -HW, y: HH - d }; // left
	};

	const layer = new PIXI.Container();
	layer.zIndex = 1;
	// addToParent destroys the layer (and every pooled sprite) on unmount
	getContextParent().addToParent(layer);

	const pool: FireParticle[] = [];
	const free: number[] = [];

	const alloc = (): FireParticle | null => {
		const idx = free.pop();
		if (idx != null) return pool[idx];
		if (pool.length >= MAX_PARTICLES) return null;
		const sprite = new PIXI.Sprite(getPuffTexture());
		sprite.anchor.set(0.5);
		sprite.blendMode = 'add';
		sprite.visible = false;
		layer.addChild(sprite);
		const particle: FireParticle = { sprite, x: 0, y: 0, vx: 0, vy: 0, life: 0, decay: 1, size: 0 };
		pool.push(particle);
		return particle;
	};

	onMount(() => {
		let raf = 0;
		const tick = () => {
			const { cells, burn } = props;

			// 1. spawn — the reference's per-frame particle burst, per burning cell
			if (burn > 0.02 && cells.length > 0) {
				const count = Math.round(SPAWN_PER_CELL * burn);
				for (const cell of cells) {
					for (let i = 0; i < count; i++) {
						const p = alloc();
						if (!p) break;
						const b = borderPoint(Math.random());
						p.x = cell.cx + b.x + (Math.random() * 8 - 4);
						p.y = cell.cy + b.y + (Math.random() * 8 - 4);
						p.vx = (Math.random() - 0.5) * 1.2;
						p.vy = Math.random() * -3 - 1.5;
						p.life = 1;
						p.decay = Math.random() * 0.03 + 0.015;
						p.size = Math.random() * 15 + 5;
						const heat = Math.floor(Math.random() * 140);
						p.sprite.tint = 0xff0000 | (heat << 8);
						p.sprite.visible = true;
					}
				}
			}

			// 2. update + draw — verbatim reference behaviour
			for (let i = 0; i < pool.length; i++) {
				const p = pool[i];
				if (!p.sprite.visible) continue;
				p.x += p.vx;
				p.y += p.vy;
				p.life -= p.decay;
				p.size *= 0.95;
				if (p.life <= 0 || p.size < 1) {
					p.sprite.visible = false;
					free.push(i);
					continue;
				}
				p.sprite.position.set(p.x, p.y);
				const diameter = p.size * 2;
				p.sprite.width = diameter;
				p.sprite.height = diameter;
				p.sprite.alpha = p.life * Math.min(1, burn * 1.4);
			}

			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>
