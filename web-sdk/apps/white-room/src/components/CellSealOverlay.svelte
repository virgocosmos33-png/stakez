<script lang="ts" module>
	import type { SymbolName } from '../game/types';

	export type EmitterEventCellSeal =
		| {
				type: 'cellSealShow';
				label: string;
				sealHardenLabel: string;
				seals: {
					reel: number;
					symbol: SymbolName;
					highlightRow: number;
					ways: number;
					hardenBumps: number;
				}[];
		  }
		| {
				type: 'sealHardenShow';
				label: string;
				updates: { reel: number; ways: number; hardenBumps: number }[];
		  }
		| { type: 'cellSealHide' };
</script>

<script lang="ts">
	import type { Texture, VideoSource } from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { cubicOut, backOut } from 'svelte/easing';
	import { stateBetDerived } from 'state-shared';
	import { MainContainer } from 'components-layout';
	import {
		Container,
		Graphics,
		BitmapText,
		Sprite,
		SpineProvider,
		SpineTrack,
		Rectangle,
	} from 'pixi-svelte';

	import { getContext } from '../game/context';
	import {
		SYMBOL_SIZE,
		CELL_PITCH_X,
		SYMBOL_CARD_W,
		SYMBOL_CARD_H,
		BOARD_DIMENSIONS,
		NUM_ROWS,
		MAX_ROWS,
	} from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { fxNum, fxColors, fxStr } from '../game/fx.generated';
	import { winFontFamily, winFontTint } from '../game/winFont';
	import { drawObservationConduitHandshake } from '../game/clinicalFx';

	const context = getContext();

	// THE WHITE ROOM — observation-pane expand chrome.
	// NO arcade yellow feature-name badge over character art.
	const HIGHLIGHT_MS = fxNum('cellSeal', 'highlightMs', 420);
	const EXPAND_MS = fxNum('cellSeal', 'expandMs', 720);
	const BEZEL_W = fxNum('cellSeal', 'bezelWidth', 5);
	const BRACKET_LEN = fxNum('cellSeal', 'bracketLen', 22);
	const BRACKET_W = fxNum('cellSeal', 'bracketWidth', 3.2);
	const TUBE_GLOW = fxNum('cellSeal', 'tubeGlow', 0.55);
	const SCAN_COUNT = Math.max(2, Math.floor(fxNum('cellSeal', 'scanlineCount', 4)));
	const BADGE_SCALE = fxNum('cellSeal', 'badgeScale', 1.2);
	/** Nominal reel-column art size used when texture dims are unavailable. */
	const REEL_ART = { width: 512, height: 1680 };
	// showFeatureLabel: 0 = gone (default). Anything else reserved for rare clinical stamp.
	const SHOW_FEATURE_LABEL = fxNum('cellSeal', 'showFeatureLabel', 0) > 0.5;
	const SEAL_COLORS = fxColors('cellSeal', 'colors', [
		0x8a8680, // bezel steel
		0xc8c4bc, // frost rim
		0xf4f1ec, // fluorescent
		0x2a2826, // plaque face
		0x6b2a28, // blood stamp
		0xf4f1ec, // mult text
	]);
	const COL_STEEL = SEAL_COLORS[0] ?? 0x8a8680;
	const COL_FROST = SEAL_COLORS[1] ?? 0xc8c4bc;
	const COL_FLUOR = SEAL_COLORS[2] ?? 0xf4f1ec;
	const COL_PLAQUE = SEAL_COLORS[3] ?? 0x2a2826;
	const COL_BLOOD = SEAL_COLORS[4] ?? 0x6b2a28;
	const COL_MULT = SEAL_COLORS[5] ?? winFontTint();
	const MODE = fxStr('cellSeal', 'mode', 'observationPane');
	const FEATURE_LABEL = fxStr('cellSeal', 'label', 'Cell Seal');
	const AMOUNT_FAMILY = winFontFamily();
	/** Observation Conduit Handshake — link VFX between 2+ seals. */
	const CONNECTION_MODE = fxStr('cellSeal', 'connectionMode', 'observationConduitHandshake');
	const CONDUIT_HOUSING_H = fxNum('cellSeal', 'conduitHousingH', 12);
	const CONDUIT_SCAN_SPEED = fxNum('cellSeal', 'conduitScanSpeed', 0.72);
	const CONDUIT_BUCKLES = Math.max(2, Math.floor(fxNum('cellSeal', 'conduitBuckleCount', 4)));

	type SealView = {
		reel: number;
		symbol: string;
		highlightRow: number;
		ways: number;
		hardenBumps: number;
		cx: number;
		cy: number;
		fullW: number;
		fullH: number;
		fullKey: string;
		expandKey: string;
		idleKey: string;
		spineKey: string;
	};

	let seals = $state<SealView[]>([]);
	let label = $state(FEATURE_LABEL);
	let hardenLabel = $state('Seal Hardens');
	let phase = $state<'idle' | 'highlight' | 'expand' | 'hold'>('idle');
	const highlightT = new Tween(0);
	const expandT = new Tween(0);
	const badgePop = new Tween(0);
	let animTime = $state(0);
	/** Expand videos: play full once, then seek/loop only the last N seconds. */
	const EXPAND_LOOP_TAIL_S = 3;

	const hasAsset = (key: string) => Boolean(context.stateApp.loadedAssets?.[key]);

	const videoOf = (key: string): HTMLVideoElement | undefined => {
		const tex = context.stateApp.loadedAssets?.[key] as Texture | undefined;
		return (tex?.source as VideoSource | undefined)?.resource as HTMLVideoElement | undefined;
	};

	const isVideoAsset = (key: string) => Boolean(videoOf(key));

	const stopH3ExpandAudio = () => {
		context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_cell_seal_h3_expand' });
		// Legacy loop cue — stop if anything still has it running; loop phase is silent.
		context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_cell_seal_h3_loop' });
	};

	const playExpandAudio = (activeSeals: SealView[]) => {
		const hasH3 = activeSeals.some((s) => String(s.symbol).toUpperCase() === 'H3');
		if (hasH3) {
			// H3: full expand bed once (audio ON). Visual last-3s loop is silent — no loop SFX.
			stopH3ExpandAudio();
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_cell_seal_h3_expand' });
			return;
		}
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_cell_seal_expand' });
	};

	const textureSizeOf = (key: string) => {
		const tex = context.stateApp.loadedAssets?.[key] as Texture | undefined;
		const w = Number(tex?.width) || Number(tex?.source?.width) || 0;
		const h = Number(tex?.height) || Number(tex?.source?.height) || 0;
		if (w > 1 && h > 1) return { width: w, height: h };
		return REEL_ART;
	};

	/** CSS object-fit: cover — fill reel column, crop overflow (never letterbox). */
	const coverFit = (reelW: number, reelH: number, artW: number, artH: number) => {
		const scale = Math.max(reelW / Math.max(1, artW), reelH / Math.max(1, artH));
		return {
			width: artW * scale,
			height: artH * scale,
		};
	};

	const assetKeysFor = (symbol: string) => {
		const id = String(symbol || 'H1').toUpperCase();
		const safe = ['H1', 'H2', 'H3', 'H4', 'H5'].includes(id) ? id : 'H1';
		const fullCandidates = [`cellSeal${safe}`, `cellSeal${safe}Full`];
		const expandCandidates = [`cellSeal${safe}Expand`];
		const idleCandidates = [`cellSeal${safe}Idle`];
		const spineCandidates = [`cellSeal${safe}Spine`];
		const pick = (keys: string[]) => keys.find((k) => hasAsset(k)) || keys[0];
		return {
			fullKey: pick(fullCandidates),
			expandKey: pick(expandCandidates),
			idleKey: pick(idleCandidates),
			spineKey: pick(spineCandidates),
		};
	};

	const layoutSeal = (
		reel: number,
		highlightRow: number,
		ways: number,
		symbol: string,
		hardenBumps: number,
	): SealView => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		// diamond: seal art spans only THIS reel's rows, centered on the board mid-line
		const rows = NUM_ROWS[reel] ?? BOARD_DIMENSIONS.y;
		const cx = originX + getSymbolX(reel);
		const cy = originY + (MAX_ROWS * 0.5) * SYMBOL_SIZE;
		const keys = assetKeysFor(symbol);
		return {
			reel,
			symbol,
			highlightRow,
			ways,
			hardenBumps,
			cx,
			cy,
			fullW: CELL_PITCH_X,
			fullH: rows * SYMBOL_SIZE,
			...keys,
		};
	};

	context.eventEmitter.subscribeOnMount({
		cellSealShow: async (e) => {
			label = e.label || FEATURE_LABEL;
			hardenLabel = e.sealHardenLabel || 'Seal Hardens';
			seals = e.seals.map((s) =>
				layoutSeal(s.reel, s.highlightRow, s.ways, String(s.symbol), s.hardenBumps),
			);
			phase = 'highlight';
			highlightT.set(0, { duration: 0 });
			expandT.set(0, { duration: 0 });
			badgePop.set(0, { duration: 0 });
			await highlightT.set(1, { duration: HIGHLIGHT_MS, easing: cubicOut });
			phase = 'expand';
			// Reset expand videos to t=0 so each seal show plays full → last-3s loop.
			for (const s of seals) {
				const video = videoOf(s.expandKey);
				if (!video) continue;
				try {
					video.pause();
					video.currentTime = 0;
				} catch {
					/* seek may throw before metadata */
				}
			}
			playExpandAudio(seals);
			await expandT.set(1, { duration: EXPAND_MS, easing: backOut });
			phase = 'hold';
			badgePop.set(0, { duration: 0 });
			await badgePop.set(1, { duration: 280, easing: backOut });
		},
		sealHardenShow: async (e) => {
			if (!seals.length) return;
			hardenLabel = e.label || hardenLabel;
			seals = seals.map((s) => {
				const u = e.updates.find((x) => x.reel === s.reel);
				return u ? { ...s, ways: u.ways, hardenBumps: u.hardenBumps } : s;
			});
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_cell_seal_harden' });
			// buckle flash on harden — pulse frame + re-pop plaque
			await highlightT.set(1.2, { duration: 100, easing: cubicOut });
			badgePop.set(0.7, { duration: 0 });
			await Promise.all([
				highlightT.set(1, { duration: 160, easing: cubicOut }),
				badgePop.set(1, { duration: 220, easing: backOut }),
			]);
		},
		cellSealHide: () => {
			stopH3ExpandAudio();
			seals = [];
			phase = 'idle';
			highlightT.set(0, { duration: 0 });
			expandT.set(0, { duration: 0 });
			badgePop.set(0, { duration: 0 });
		},
	});

	// scanline / buckle presence clock while visible
	$effect(() => {
		if (!seals.length || phase === 'idle') return;
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			animTime = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	/**
	 * Video playback while seals are up:
	 * - expand *video*: muted, play once in full, then loop only the last 3s
	 * - idle.webm (and other non-expand videos): muted full loop
	 */
	$effect(() => {
		if (!seals.length || phase === 'idle' || phase === 'highlight') return;
		const cleanups: Array<() => void> = [];
		for (const s of seals) {
			const expandVideo = videoOf(s.expandKey);
			if (expandVideo) {
				expandVideo.loop = false;
				expandVideo.muted = true;
				expandVideo.playsInline = true;
				const onTimeUpdate = () => {
					const d = expandVideo.duration;
					if (!Number.isFinite(d) || d <= EXPAND_LOOP_TAIL_S + 0.05) return;
					const nearEnd = expandVideo.currentTime >= d - 0.08;
					if (!nearEnd) return;
					try {
						expandVideo.currentTime = Math.max(0, d - EXPAND_LOOP_TAIL_S);
					} catch {
						/* ignore seek races */
					}
				};
				const onEnded = () => {
					const d = expandVideo.duration;
					const seekTo =
						Number.isFinite(d) && d > EXPAND_LOOP_TAIL_S
							? Math.max(0, d - EXPAND_LOOP_TAIL_S)
							: 0;
					try {
						expandVideo.currentTime = seekTo;
					} catch {
						/* ignore */
					}
					expandVideo.play().catch(() => {});
				};
				expandVideo.addEventListener('timeupdate', onTimeUpdate);
				expandVideo.addEventListener('ended', onEnded);
				cleanups.push(() => {
					expandVideo.removeEventListener('timeupdate', onTimeUpdate);
					expandVideo.removeEventListener('ended', onEnded);
				});
				if (expandVideo.paused) expandVideo.play().catch(() => {});
			}
			const idleVideo = videoOf(s.idleKey);
			// Only drive idle when expand is NOT a video (expand video is preferred on-screen).
			if (idleVideo && !expandVideo) {
				idleVideo.loop = true;
				idleVideo.muted = true;
				idleVideo.playsInline = true;
				if (idleVideo.paused) idleVideo.play().catch(() => {});
			}
		}
		return () => {
			for (const dispose of cleanups) dispose();
		};
	});

	/** Restraint-strap corner brackets (L-corners) — clinical, not neon rect. */
	const drawCornerBrackets = (
		g: import('pixi.js').Graphics,
		x: number,
		y: number,
		w: number,
		h: number,
		alpha: number,
		len = BRACKET_LEN,
	) => {
		const bw = BRACKET_W;
		const corners: [number, number, number, number][] = [
			// TL
			[x, y, len, bw],
			[x, y, bw, len],
			// TR
			[x + w - len, y, len, bw],
			[x + w - bw, y, bw, len],
			// BL
			[x, y + h - bw, len, bw],
			[x, y + h - len, bw, len],
			// BR
			[x + w - len, y + h - bw, len, bw],
			[x + w - bw, y + h - len, bw, len],
		];
		for (const [cx, cy, cw, ch] of corners) {
			g.rect(cx, cy, cw, ch);
			g.fill({ color: COL_STEEL, alpha });
		}
		// buckle studs at each corner
		const stud = 3.2;
		const inset = 5;
		for (const [sx, sy] of [
			[x + inset, y + inset],
			[x + w - inset, y + inset],
			[x + inset, y + h - inset],
			[x + w - inset, y + h - inset],
		] as const) {
			g.circle(sx, sy, stud);
			g.fill({ color: COL_FROST, alpha: alpha * 0.9 });
			g.circle(sx, sy, stud * 0.35);
			g.fill({ color: COL_PLAQUE, alpha: alpha * 0.85 });
		}
	};

	/** Fluorescent tube edge glow + frost crack rim + pulse scanline. */
	const drawObservationChrome = (
		g: import('pixi.js').Graphics,
		x: number,
		y: number,
		w: number,
		h: number,
		alpha: number,
		pulse: number,
	) => {
		const flicker =
			MODE === 'observationPane'
				? 0.72 + 0.28 * Math.sin(animTime * 11) * (Math.sin(animTime * 37) > 0.92 ? 0.35 : 1)
				: 1;
		const a = alpha * flicker;

		// charcoal housing lip
		g.rect(x - 3, y - 3, w + 6, h + 6);
		g.stroke({ width: BEZEL_W + 2, color: 0x1a1816, alpha: a * 0.75 });

		// steel observation bezel
		g.rect(x, y, w, h);
		g.stroke({ width: BEZEL_W, color: COL_STEEL, alpha: a });

		// frost / glass inner rim
		g.rect(x + 3, y + 3, w - 6, h - 6);
		g.stroke({ width: 1.4, color: COL_FROST, alpha: a * 0.7 });

		// fluorescent tube edge — top + bottom rails
		const tubeA = a * TUBE_GLOW * (0.85 + 0.15 * pulse);
		g.rect(x + 6, y + 1.5, w - 12, 2.2);
		g.fill({ color: COL_FLUOR, alpha: tubeA });
		g.rect(x + 6, y + h - 3.7, w - 12, 2.2);
		g.fill({ color: COL_FLUOR, alpha: tubeA * 0.85 });
		// side micro-tubes
		g.rect(x + 1.5, y + 8, 2, h - 16);
		g.fill({ color: COL_FLUOR, alpha: tubeA * 0.45 });
		g.rect(x + w - 3.5, y + 8, 2, h - 16);
		g.fill({ color: COL_FLUOR, alpha: tubeA * 0.45 });

		// rare blood-sparse speck on bezel (clinical stain, not neon)
		g.rect(x + w * 0.72, y - 1, 7, 2.5);
		g.fill({ color: COL_BLOOD, alpha: a * 0.35 });

		drawCornerBrackets(g, x - 1, y - 1, w + 2, h + 2, a * (0.85 + 0.15 * pulse));

		// CCTV-style scanline sweep inside pane
		for (let i = 0; i < SCAN_COUNT; i++) {
			const sy = y + ((animTime * 55 + i * (h / SCAN_COUNT)) % h);
			g.rect(x + 4, sy, w - 8, 1.2);
			g.fill({ color: COL_FLUOR, alpha: a * 0.1 });
		}
	};

	const drawHighlight = (g: import('pixi.js').Graphics, s: SealView) => {
		g.clear();
		if (phase === 'idle') return;
		const boardLayout = context.stateGameDerived.boardLayout();
		const originY = boardLayout.y - boardLayout.height * 0.5;
		const cellCy = originY + getCellCenterY(s.reel, s.highlightRow);
		const alpha =
			phase === 'highlight' ? highlightT.current : Math.max(0.15, 1 - expandT.current * 1.1);
		if (alpha < 0.02) return;
		const pulse = 1 + Math.sin(highlightT.current * Math.PI) * 0.04;
		// hugs the portrait card, not the square cell, so the chrome doesn't
		// float out over the gap between reels
		const w = SYMBOL_CARD_W * pulse;
		const h = SYMBOL_CARD_H * pulse;
		drawObservationChrome(g, s.cx - w / 2, cellCy - h / 2, w, h, alpha, pulse);
	};

	const drawReelFrame = (g: import('pixi.js').Graphics, s: SealView) => {
		g.clear();
		if (phase === 'idle' || phase === 'highlight') return;
		const t = expandT.current;
		const h = SYMBOL_SIZE + (s.fullH - SYMBOL_SIZE) * t;
		const w = s.fullW;
		const alpha = 0.5 + 0.5 * t;
		const hasAny =
			hasAsset(s.spineKey) ||
			hasAsset(s.idleKey) ||
			hasAsset(s.expandKey) ||
			hasAsset(s.fullKey);
		if (!hasAny) {
			g.rect(s.cx - w / 2, s.cy - h / 2, w, h);
			g.fill({ color: 0x2a3038, alpha: alpha * 0.95 });
		}
		const pulse = 0.5 + 0.5 * Math.sin(animTime * 6);
		drawObservationChrome(g, s.cx - w / 2, s.cy - h / 2, w, h, alpha, pulse);

		// soft glass refraction veil along left edge
		g.rect(s.cx - w / 2 + 4, s.cy - h / 2 + 6, 5, h - 12);
		g.fill({ color: COL_FLUOR, alpha: alpha * 0.06 * (0.7 + 0.3 * pulse) });
	};

	/** Stamped ceramic/steel hospital plaque — ways multiplier, bottom of reel. */
	const drawBadge = (g: import('pixi.js').Graphics, s: SealView) => {
		g.clear();
		if (phase === 'idle' || phase === 'highlight') return;
		const t = Math.max(expandT.current, badgePop.current * 0.01);
		const badgeW = 96 * BADGE_SCALE;
		const badgeH = 46 * BADGE_SCALE;
		const x = s.cx - badgeW / 2;
		const y = s.cy + s.fullH * 0.5 - badgeH - 8;
		const a = Math.min(1, t);

		// steel outer plate
		g.roundRect(x - 3, y - 3, badgeW + 6, badgeH + 6, 3);
		g.fill({ color: COL_STEEL, alpha: 0.95 * a });
		// ceramic / charcoal plaque face
		g.roundRect(x, y, badgeW, badgeH, 2);
		g.fill({ color: COL_PLAQUE, alpha: 0.96 * a });
		// frost inner rule
		g.roundRect(x + 4, y + 4, badgeW - 8, badgeH - 8, 1.5);
		g.stroke({ width: 1.4, color: COL_FROST, alpha: 0.85 * a });
		// blood-corner clinical stamp
		g.rect(x + 6, y + 6, 16, 5);
		g.fill({ color: COL_BLOOD, alpha: 0.75 * a });
		g.rect(x + badgeW - 14, y + badgeH - 10, 8, 4);
		g.fill({ color: COL_BLOOD, alpha: 0.4 * a });
		// fluorescent land flash
		const flash = Math.max(0, 1 - badgePop.current) * (phase === 'hold' ? 0 : 1);
		if (flash > 0.02 || (badgePop.current > 0.01 && badgePop.current < 0.55)) {
			const f = badgePop.current < 0.55 ? 1 - badgePop.current / 0.55 : flash;
			g.roundRect(x - 6, y - 6, badgeW + 12, badgeH + 12, 4);
			g.fill({ color: COL_FLUOR, alpha: 0.28 * f * a });
		}
		// micro scan across plaque
		const scanY = y + ((animTime * 36) % badgeH);
		g.rect(x, scanY, badgeW, 1.5);
		g.fill({ color: COL_FLUOR, alpha: 0.1 * a });
	};

	/**
	 * Observation Conduit Handshake — cinematic link between sealed reels (2+).
	 * Fluorescent housing + steel couplers + restraint buckles + CCTV scan packet.
	 * Replaces arcade flower/gear + trailing dots.
	 */
	const drawSealLinks = (g: import('pixi.js').Graphics) => {
		g.clear();
		if (seals.length < 2 || phase === 'idle' || phase === 'highlight') return;
		if (CONNECTION_MODE !== 'observationConduitHandshake') return;
		const drawProgress = Math.max(0.12, expandT.current);
		const sorted = [...seals].sort((a, b) => a.reel - b.reel);
		for (let i = 0; i < sorted.length - 1; i++) {
			const left = sorted[i];
			const right = sorted[i + 1];
			const x0 = left.cx + left.fullW * 0.48;
			const x1 = right.cx - right.fullW * 0.48;
			const y0 = left.cy;
			const y1 = right.cy;
			drawObservationConduitHandshake(g, {
				x0,
				y0,
				x1,
				y1,
				time: animTime,
				drawProgress,
				alpha: 0.55 + 0.45 * drawProgress,
				seed: 11 + i * 17 + left.reel * 3,
				housingHeight: CONDUIT_HOUSING_H,
				buckleCount: CONDUIT_BUCKLES,
				scanSpeed: CONDUIT_SCAN_SPEED,
			});
		}
	};
</script>

{#if seals.length}
	<MainContainer>
		<!-- Link VFX behind seals so chrome/badge stay on top -->
		{#if seals.length >= 2 && (phase === 'expand' || phase === 'hold')}
			<Graphics draw={(g) => drawSealLinks(g)} />
		{/if}
		{#each seals as s (s.reel)}
			{@const t = Math.max(expandT.current, phase === 'hold' ? 1 : 0.01)}
			{@const h = SYMBOL_SIZE + (s.fullH - SYMBOL_SIZE) * t}
			{@const w = s.fullW}
			{@const showChar = phase === 'expand' || phase === 'hold'}
			<!-- Prefer expand *video* (play-once→loop-last-3s) over idle.webm.
				Else idle.webm over expand.gif (Pixi often freezes gif on frame 0).
				Spine after anims; full.webp poster last. -->
			{@const expandIsVideo = showChar && hasAsset(s.expandKey) && isVideoAsset(s.expandKey)}
			{@const useExpand = showChar && hasAsset(s.expandKey) && (expandIsVideo || !hasAsset(s.idleKey))}
			{@const useIdle = showChar && !useExpand && hasAsset(s.idleKey)}
			{@const useSpine = showChar && !useIdle && !useExpand && hasAsset(s.spineKey)}
			{@const useFull = showChar && !useIdle && !useExpand && !useSpine && hasAsset(s.fullKey)}
			{@const spriteKey = useExpand ? s.expandKey : useIdle ? s.idleKey : useFull ? s.fullKey : ''}
			{@const art = spriteKey ? textureSizeOf(spriteKey) : REEL_ART}
			{@const cover = coverFit(w, h, art.width, art.height)}
			{@const badgeY = s.cy + s.fullH * 0.5 - 8 - (46 * BADGE_SCALE) / 2}
			{@const popScale = 0.72 + 0.28 * Math.max(badgePop.current, phase === 'hold' ? 1 : 0)}
			<Container>
				<Graphics draw={(g) => drawHighlight(g, s)} />
				<Graphics draw={(g) => drawReelFrame(g, s)} />
				{#if useSpine}
					<!-- Masked reel column — spine scaled to cover -->
					<Container x={s.cx} y={s.cy}>
						<Rectangle isMask anchor={0.5} width={w} height={h} backgroundColor={0xffffff} />
						<SpineProvider
							key={s.spineKey}
							x={0}
							y={0}
							height={cover.height}
							width={cover.width}
						>
							<SpineTrack
								loop
								trackIndex={0}
								animationName="idle"
								timeScale={stateBetDerived.timeScale()}
							/>
						</SpineProvider>
					</Container>
				{:else if spriteKey}
					<!-- Cover-fit + mask: video fills reel edge-to-edge, crop overflow.
					     Never stretch-letterbox (width/height alone on padded webm left bars). -->
					<Container x={s.cx} y={s.cy} alpha={0.7 + 0.3 * t}>
						<Rectangle isMask anchor={0.5} width={w} height={h} backgroundColor={0xffffff} />
						<Sprite
							key={spriteKey}
							x={0}
							y={0}
							anchor={0.5}
							width={cover.width}
							height={cover.height}
						/>
					</Container>
				{/if}
				{#if showChar}
					<Graphics draw={(g) => drawBadge(g, s)} />
					<Container x={s.cx} y={badgeY} scale={popScale} alpha={t}>
						<!-- ASCII "x" — clinical bitmap font has no U+00D7 × glyph (silent drop → bare "4"). -->
						<BitmapText
							text={`x${s.ways}`}
							anchor={0.5}
							style={{
								fontFamily: AMOUNT_FAMILY,
								fontSize: Math.round(30 * BADGE_SCALE),
								fill: COL_MULT,
								letterSpacing: 1,
							}}
						/>
					</Container>
					<!-- Feature name OFF by default — never float arcade yellow on art.
					     Opt-in only via fx.cellSeal.showFeatureLabel > 0 (tiny clinical stamp). -->
					{#if SHOW_FEATURE_LABEL}
						{@const stamp = s.hardenBumps > 0 ? hardenLabel : label}
						<Container
							x={s.cx}
							y={s.cy - s.fullH * 0.5 + 14}
							alpha={t * 0.85}
						>
							<Graphics
								draw={(g) => {
									g.clear();
									const tw = Math.min(110, 10 + stamp.length * 7);
									const th = 14;
									g.roundRect(-tw / 2, -th / 2, tw, th, 1);
									g.fill({ color: COL_PLAQUE, alpha: 0.9 });
									g.roundRect(-tw / 2, -th / 2, tw, th, 1);
									g.stroke({ width: 1, color: COL_STEEL, alpha: 0.9 });
									g.rect(-tw / 2 + 3, -th / 2 + 2, 8, 3);
									g.fill({ color: COL_BLOOD, alpha: 0.65 });
								}}
							/>
							<BitmapText
								text={stamp.toUpperCase()}
								anchor={0.5}
								style={{
									fontFamily: AMOUNT_FAMILY,
									fontSize: 10,
									fill: COL_FROST,
									letterSpacing: 1.5,
								}}
							/>
						</Container>
					{/if}
				{/if}
			</Container>
		{/each}
	</MainContainer>
{/if}
