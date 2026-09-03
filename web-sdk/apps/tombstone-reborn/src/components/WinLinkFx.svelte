<script module lang="ts">
	import { Texture } from 'pixi.js';
	import { SLOT_HOLE_SRC_H, SLOT_HOLE_SRC_R, SLOT_HOLE_SRC_W } from '../game/slotFrame';

	const canvasTex = (
		w: number,
		h: number,
		paint: (ctx: CanvasRenderingContext2D, w: number, h: number) => void,
	) => {
		const c = document.createElement('canvas');
		c.width = w;
		c.height = h;
		const ctx = c.getContext('2d');
		if (!ctx) return Texture.EMPTY;
		paint(ctx, w, h);
		return Texture.from(c);
	};

	const sweepTex = canvasTex(256, 256, (ctx, w, h) => {
		const v = ctx.createLinearGradient(0, 0, 0, h);
		v.addColorStop(0, 'rgba(128,8,0,0)');
		v.addColorStop(0.16, 'rgba(128,8,0,0.18)');
		v.addColorStop(0.3, 'rgba(255,77,5,0.5)');
		v.addColorStop(0.44, 'rgba(255,148,18,0.78)');
		v.addColorStop(0.5, 'rgba(255,230,122,0.95)');
		v.addColorStop(0.56, 'rgba(255,148,18,0.78)');
		v.addColorStop(0.7, 'rgba(255,77,5,0.5)');
		v.addColorStop(0.84, 'rgba(128,8,0,0.18)');
		v.addColorStop(1, 'rgba(128,8,0,0)');
		ctx.fillStyle = v;
		ctx.fillRect(0, 0, w, h);
		ctx.globalCompositeOperation = 'lighter';
		for (let i = 0; i < 7; i += 1) {
			const x = ((i + 0.5) / 7) * w;
			const tw = 16 + (i % 3) * 9;
			const g = ctx.createRadialGradient(x, h * 0.5, 1, x, h * 0.48, tw);
			g.addColorStop(0, 'rgba(255,230,122,0.62)');
			g.addColorStop(0.45, 'rgba(255,148,18,0.28)');
			g.addColorStop(1, 'rgba(255,77,5,0)');
			ctx.fillStyle = g;
			ctx.fillRect(x - tw, h * 0.12, tw * 2, h * 0.76);
		}
		const side = ctx.createLinearGradient(0, 0, w, 0);
		side.addColorStop(0, 'rgba(0,0,0,1)');
		side.addColorStop(0.12, 'rgba(0,0,0,0)');
		side.addColorStop(0.88, 'rgba(0,0,0,0)');
		side.addColorStop(1, 'rgba(0,0,0,1)');
		ctx.globalCompositeOperation = 'destination-out';
		ctx.fillStyle = side;
		ctx.fillRect(0, 0, w, h);
	});

	const washTex = canvasTex(128, 160, (ctx, w, h) => {
		const g = ctx.createRadialGradient(w / 2, h * 0.72, 4, w / 2, h * 0.55, w * 0.72);
		g.addColorStop(0, 'rgba(138,83,0,0.28)');
		g.addColorStop(0.55, 'rgba(138,83,0,0.08)');
		g.addColorStop(1, 'rgba(138,83,0,0)');
		ctx.fillStyle = g;
		ctx.fillRect(0, 0, w, h);
	});

	const emberTex = canvasTex(32, 32, (ctx, w, h) => {
		const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
		g.addColorStop(0, 'rgba(255,182,40,1)');
		g.addColorStop(0.22, 'rgba(255,182,40,0.55)');
		g.addColorStop(1, 'rgba(255,182,40,0)');
		ctx.fillStyle = g;
		ctx.fillRect(0, 0, w, h);
	});

	const smokeTex = canvasTex(64, 64, (ctx, w, h) => {
		const g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
		g.addColorStop(0, 'rgba(130,130,140,0.4)');
		g.addColorStop(0.55, 'rgba(130,130,140,0.1)');
		g.addColorStop(1, 'rgba(130,130,140,0)');
		ctx.fillStyle = g;
		ctx.fillRect(0, 0, w, h);
	});

	const rimTex = canvasTex(256, 320, (ctx, w, h) => {
		const inset = 10;
		const r = 22;
		ctx.strokeStyle = 'rgba(138,83,0,0.55)';
		ctx.lineWidth = 10;
		ctx.beginPath();
		ctx.roundRect(inset, inset, w - inset * 2, h - inset * 2, r + 2);
		ctx.stroke();
		ctx.strokeStyle = 'rgba(255,182,40,0.95)';
		ctx.lineWidth = 4;
		ctx.beginPath();
		ctx.roundRect(inset + 4, inset + 4, w - inset * 2 - 8, h - inset * 2 - 8, r);
		ctx.stroke();
	});

	const maskTex = canvasTex(SLOT_HOLE_SRC_W, SLOT_HOLE_SRC_H, (ctx, w, h) => {
		ctx.fillStyle = '#fff';
		ctx.beginPath();
		ctx.roundRect(0, 0, w, h, SLOT_HOLE_SRC_R);
		ctx.fill();
	});
</script>

<script lang="ts">
	/**
	 * Linked-cell energy. The skim is a y-only tween on the Pixi ticker —
	 * same clock as the renderer. No Graphics mask, no second RAF, no
	 * per-frame width/height. That was the hitch.
	 *
	 * `rim` stays under the cards. `wipe` is the additive scan band only.
	 * No color-burn — that stained the faces. The sheet is the Febucci /
	 * Radiant fire filter so the skim is carved flame, not a bar.
	 */
	import { untrack } from 'svelte';
	import { Container, Filter, Sprite } from 'pixi.js';
	import type { Texture } from 'pixi.js';
	import { getContextParent } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_CARD_W } from '../game/constants';
	import { getSymbolX, getCellCenterY, getCardHeight, getRowPitch } from '../game/utils';
	import { slotFrameHole } from '../game/slotFrame';
	import { fxRandom } from '../game/featureVfx';
	import { stopThemed } from '../game/sfxTheme';
	import { SHINE_SWEEP_COUNT, SHINE_SWEEP_MS } from '../game/shineTiming';
	import { createWipeFireFilter, setWipeFireTime } from '../game/wipeFireFilter';

	type Layer = 'rim' | 'wipe';
	const props: { layer: Layer } = $props();
	const isWipe = props.layer === 'wipe';

	const SWEEP_MS = SHINE_SWEEP_MS;
	const SWEEP_COUNT = SHINE_SWEEP_COUNT;
	const EMBER_N = 6;
	const WIPE_EMBER_N = 8;
	const SMOKE_N = 3;
	const BAND_H = 0.34;

	const game = getContext();
	const parent = getContextParent();
	const root = new Container();
	root.eventMode = 'none';
	parent.addToParent(root);

	type Bit = {
		sprite: Sprite;
		seed: number;
		ox: number;
		period: number;
		baseW: number;
		baseH: number;
		kind: 'ember' | 'smoke';
	};

	type CellFx = {
		h: number;
		wrap: Container;
		band: Sprite | null;
		fires: Filter[];
		embers: Bit[];
		smoke: Bit[];
	};

	let layers: CellFx[] = [];
	let builtKeys = '';
	let sweepBorn = 0;
	let sweepLive = false;
	let whipPass = -1;
	let lastShineGen = 0;

	const stopWhip = () => {
		if (!isWipe) return;
		stopThemed('sfx_link_whip');
	};

	const easeSweep = (t: number) =>
		t < 0.5 ? 2 * t * t : 1 - 2 * (1 - t) * (1 - t);

	const spr = (texture: Texture, add: boolean) => {
		const s = new Sprite(texture);
		s.anchor.set(0.5);
		s.eventMode = 'none';
		if (add) s.blendMode = 'add';
		return s;
	};

	const wipePlateTex = () =>
		(game.stateApp.loadedAssets?.highPayBg as Texture | undefined) ?? sweepTex;

	const buildCell = (reel: number, row: number): CellFx => {
		const w = SYMBOL_CARD_W;
		const h = getCardHeight(reel);
		const wrap = new Container();
		wrap.eventMode = 'none';
		wrap.x = getSymbolX(reel);
		wrap.y = getCellCenterY(reel, row);

		const hole = slotFrameHole(getRowPitch(reel));
		const masked = new Container();
		masked.eventMode = 'none';
		const mask = spr(maskTex, false);
		mask.width = hole.w;
		mask.height = hole.h;
		masked.addChild(mask);
		masked.mask = mask;

		let band: Sprite | null = null;
		const fires: Filter[] = [];
		const embers: Bit[] = [];
		const smoke: Bit[] = [];

		if (isWipe) {
			const plate = wipePlateTex();
			band = spr(plate, true);
			band.width = w * 1.08;
			band.height = h * BAND_H;
			band.alpha = 0.95;
			band.visible = false;
			const bandFire = createWipeFireFilter();
			band.filters = [bandFire];
			fires.push(bandFire);
			masked.addChild(band);
			const key = `${reel}-${row}`;
			for (let i = 0; i < WIPE_EMBER_N; i += 1) {
				const seed = key.length * 23 + i * 41;
				const sprite = spr(emberTex, true);
				sprite.width = 9;
				sprite.height = 11;
				sprite.visible = false;
				masked.addChild(sprite);
				embers.push({
					sprite,
					seed,
					ox: (fxRandom(seed + 5) - 0.5) * w * 0.84,
					period: 520,
					baseW: 9,
					baseH: 11,
					kind: 'ember',
				});
			}
		} else {
			const rim = spr(rimTex, false);
			rim.width = w + 8;
			rim.height = h + 8;
			wrap.addChild(rim);

			const wash = spr(washTex, false);
			wash.width = w * 0.92;
			wash.height = h * 0.92;
			wash.alpha = 0.7;
			masked.addChild(wash);

			const key = `${reel}-${row}`;
			for (let i = 0; i < SMOKE_N; i += 1) {
				const seed = key.length * 17 + i * 31;
				const sprite = spr(smokeTex, false);
				const baseW = 18 + fxRandom(seed + 2) * 6;
				const baseH = 24 + fxRandom(seed + 3) * 8;
				sprite.width = baseW;
				sprite.height = baseH;
				masked.addChild(sprite);
				smoke.push({
					sprite,
					seed,
					ox: (fxRandom(seed + 1) - 0.5) * w * 0.7,
					period: 4200,
					baseW,
					baseH,
					kind: 'smoke',
				});
			}

			for (let i = 0; i < EMBER_N; i += 1) {
				const seed = key.length * 23 + i * 41;
				const sprite = spr(emberTex, true);
				sprite.width = 10;
				sprite.height = 10;
				masked.addChild(sprite);
				embers.push({
					sprite,
					seed,
					ox: (fxRandom(seed + 5) - 0.5) * w * 0.84,
					period: 2000,
					baseW: 10,
					baseH: 10,
					kind: 'ember',
				});
			}
		}

		wrap.addChild(masked);
		root.addChild(wrap);
		return { h, wrap, band, fires, embers, smoke };
	};

	const clearLayers = () => {
		stopWhip();
		for (const layer of layers) {
			for (const fire of layer.fires) fire.destroy();
			if (!layer.wrap.destroyed) layer.wrap.destroy({ children: true });
		}
		layers = [];
		sweepLive = false;
		whipPass = -1;
	};

	const applyPositions = (
		positions: { reel: number; row: number }[],
		shineGen: number,
	) => {
		const keys = positions.map((p) => `${p.reel}-${p.row}`).join('|');
		const shine = shineGen !== lastShineGen;
		if (shine) lastShineGen = shineGen;
		if (!keys) {
			if (builtKeys) {
				builtKeys = '';
				clearLayers();
			}
			return;
		}
		if (keys !== builtKeys) {
			clearLayers();
			builtKeys = keys;
			layers = positions.map((p) => buildCell(p.reel, p.row));
		}
		// Rim layer keeps the chrome. Only the wipe layer arms a skim.
		if (isWipe && shine) {
			sweepBorn = performance.now();
			sweepLive = true;
			whipPass = -1;
		}
	};

	$effect(() => {
		const positions = game.stateGame.slotWinPositions ?? [];
		const shineGen = game.stateGame.winLinkShineGen;
		untrack(() => applyPositions(positions, shineGen));
	});

	const tickBits = (now: number, bits: Bit[], h: number) => {
		for (const bit of bits) {
			const life = (now / bit.period + fxRandom(bit.seed)) % 1;
			const s = bit.sprite;
			if (bit.kind === 'smoke') {
				const scale = 0.6 + life * 1.1;
				s.x = bit.ox;
				s.y = h * (0.48 - life * 1.15);
				s.alpha = life < 0.12 ? (life / 0.12) * 0.5 : (1 - life) * 0.5;
				s.scale.set((bit.baseW / 64) * scale, (bit.baseH / 64) * scale);
			} else {
				s.x = bit.ox + (fxRandom(bit.seed + 4) - 0.5) * 30 * life;
				s.y = h * (0.5 - life * 1.2);
				s.alpha = life < 0.1 ? life / 0.1 : 1 - life;
			}
		}
	};

	const onTick = () => {
		const now = performance.now();
		const age = now - sweepBorn;
		const sweeping = sweepLive && age >= 0 && age < SWEEP_MS * SWEEP_COUNT;
		if (sweeping) {
			const pass = Math.min(SWEEP_COUNT - 1, Math.floor(age / SWEEP_MS));
			if (pass !== whipPass) {
				whipPass = pass;
				// One voice. forcePlay stacked the 601ms tail on the next lash
				// and that tail was the leftover hit after the visual wipe.
				stopWhip();
				game.eventEmitter.broadcast({
					type: 'soundOnce',
					name: 'sfx_link_whip',
				});
			}
		}
		const t = (((age % SWEEP_MS) + SWEEP_MS) % SWEEP_MS) / SWEEP_MS;
		const rise = 0.7 - easeSweep(t) * 1.4;
		const fireSec = now * 0.001;
		const flick =
			0.78 +
			0.14 * (0.5 + 0.5 * Math.sin(now * 0.041)) +
			0.08 * (0.5 + 0.5 * Math.sin(now * 0.093));
		for (const layer of layers) {
			if (layer.wrap.destroyed) continue;
			if (layer.band) {
				if (sweeping) {
					layer.band.visible = true;
					layer.band.y = rise * layer.h;
					layer.band.alpha = 0.88 * flick;
					layer.band.height = layer.h * (BAND_H * (0.86 + 0.28 * flick));
				} else if (layer.band.visible) {
					layer.band.visible = false;
				}
			}
			if (isWipe) {
				if (sweeping) {
					for (const fire of layer.fires) setWipeFireTime(fire, fireSec);
				}
				for (const bit of layer.embers) {
					const life = (now / bit.period + fxRandom(bit.seed)) % 1;
					const s = bit.sprite;
					s.visible = sweeping;
					if (!sweeping) continue;
					s.x = bit.ox + (fxRandom(bit.seed + 4) - 0.5) * 22 * life;
					s.y = rise * layer.h + (0.35 - life) * layer.h * 0.22;
					s.alpha = (life < 0.12 ? life / 0.12 : 1 - life) * flick;
				}
			} else {
				tickBits(now, layer.smoke, layer.h);
				tickBits(now, layer.embers, layer.h);
			}
		}
		if (!sweeping && sweepLive) {
			sweepLive = false;
			stopWhip();
		}
	};

	const endSkim = () => {
		sweepLive = false;
		whipPass = SWEEP_COUNT;
		stopWhip();
		if (!isWipe) return;
		for (const layer of layers) {
			if (layer.wrap.destroyed) continue;
			if (layer.band) layer.band.visible = false;
			for (const bit of layer.embers) bit.sprite.visible = false;
		}
	};

	game.eventEmitter.subscribeOnMount({
		// Skip / money overlay: kill an in-flight lash so it cannot hit under the chip.
		winShow: endSkim,
	});

	$effect(() => {
		const ticker = game.stateApp.pixiApplication?.ticker;
		if (!ticker) return;
		ticker.add(onTick);
		return () => ticker.remove(onTick);
	});
</script>
