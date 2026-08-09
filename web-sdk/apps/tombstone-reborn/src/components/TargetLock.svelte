<script lang="ts" module>
	/** which feature is about to fire — only changes the accent colour */
	export type TargetTone = 'split' | 'clone' | 'stretch';

	// Marks the cells a feature is ABOUT to hit, before it hits them. Without
	// this the features detonate with no warning and the player never sees which
	// symbols were chosen — the whole point of the feature is lost in the flash.
	export type EmitterEventTargetLock =
		| { type: 'targetLockShow'; cells: { reel: number; row: number }[]; tone: TargetTone }
		| { type: 'targetLockHide' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut, quadIn } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import {
		SYMBOL_SIZE,
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
	} from '../game/constants';
	import { WHITE_ROOM_PALETTE } from '../game/clinicalFx';

	const context = getContext();

	// A diagnostic instrument locking onto a subject: four brackets drive in from
	// outside the cell and clamp onto the card, a scanline rakes down it, and a
	// contracting ring closes on the centre.
	const ACCENT: Record<TargetTone, number> = {
		split: 0xff2d2d,
		clone: 0x9fe8ff,
		stretch: 0xbfe3ff,
	};

	/** how far behind cell i-1 cell i starts locking, as a fraction of the run */
	const STAGGER = 0.16;
	const LOCK_MS = 340;
	const HOLD_MS = 130;
	const FADE_MS = 170;
	/** how far outside the card the brackets start */
	const APPROACH = 30;

	type Mark = { key: string; cx: number; cy: number };

	let marks = $state<Mark[]>([]);
	let tone = $state<TargetTone>('split');
	let time = $state(0);

	const lock = new Tween(0);
	const fade = new Tween(0);

	const layout = (cells: { reel: number; row: number }[]) => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const originX = boardLayout.x - boardLayout.width * 0.5;
		const originY = boardLayout.y - boardLayout.height * 0.5;
		marks = cells.map((c) => ({
			key: `${c.reel}-${c.row}`,
			cx: originX + getSymbolX(c.reel),
			cy: originY + getCellCenterY(c.reel, c.row),
		}));
	};

	// per-cell progress, so the marks land one after another left to right
	const progressOf = (index: number) => {
		const span = 1 + STAGGER * Math.max(marks.length - 1, 0);
		return Math.min(Math.max(lock.current * span - STAGGER * index, 0), 1);
	};

	context.eventEmitter.subscribeOnMount({
		targetLockShow: async ({ cells, tone: incoming }) => {
			if (!cells.length) return;
			tone = incoming;
			layout(cells);
			lock.set(0, { duration: 0 });
			fade.set(1, { duration: 0 });
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_anticipation_start' });
			await lock.set(1, {
				duration: LOCK_MS + marks.length * STAGGER * LOCK_MS,
				easing: cubicOut,
			});
			await new Promise((resolve) => window.setTimeout(resolve, HOLD_MS));
			await fade.set(0, { duration: FADE_MS, easing: quadIn });
			marks = [];
		},
		targetLockHide: () => {
			fade.set(0, { duration: 0 });
			marks = [];
		},
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	const drawMark = (g: import('pixi.js').Graphics, p: number) => {
		if (p <= 0) return;
		const accent = ACCENT[tone];
		const halfW = CARD_W / 2;
		const halfH = CARD_H / 2;
		const out = APPROACH * (1 - p);
		const arm = 15;
		const settled = p >= 1;

		// four corner brackets driving in
		for (const sx of [-1, 1]) {
			for (const sy of [-1, 1]) {
				const x = sx * (halfW + out);
				const y = sy * (halfH + out);
				g.moveTo(x, y - sy * arm);
				g.lineTo(x, y);
				g.lineTo(x - sx * arm, y);
				g.stroke({ color: WHITE_ROOM_PALETTE.bone, width: 2.4, alpha: 0.35 + 0.6 * p });
				g.moveTo(x, y - sy * (arm - 4));
				g.lineTo(x, y);
				g.lineTo(x - sx * (arm - 4), y);
				g.stroke({ color: accent, width: 1, alpha: 0.5 * p });
			}
		}

		// ring closing on the centre
		const radius = halfH * (1.25 - 0.62 * p);
		g.circle(0, 0, radius);
		g.stroke({ color: accent, width: 1.2, alpha: 0.4 * (1 - p * 0.55) });

		// scanline raking down the card
		if (!settled) {
			const y = -halfH + p * CARD_H;
			g.rect(-halfW, y - 1, CARD_W, 2);
			g.fill({ color: WHITE_ROOM_PALETTE.bone, alpha: 0.55 });
			g.rect(-halfW, y - 5, CARD_W, 10);
			g.fill({ color: accent, alpha: 0.14 });
		}

		// held lock: crosshair ticks + a slow breathing wash so it reads as armed
		if (settled) {
			const breathe = 0.55 + 0.45 * Math.sin(time * 9);
			for (const sx of [-1, 1]) {
				g.moveTo(sx * (halfW - 4), 0);
				g.lineTo(sx * (halfW - 13), 0);
				g.stroke({ color: accent, width: 1.4, alpha: 0.5 + 0.4 * breathe });
			}
			g.roundRect(-halfW, -halfH, CARD_W, CARD_H, 8);
			g.fill({ color: accent, alpha: 0.05 + 0.05 * breathe });
		}
	};
</script>

{#if marks.length}
	<MainContainer>
		<Container alpha={fade.current}>
			{#each marks as mark, index (mark.key)}
				<Container x={mark.cx} y={mark.cy}>
					<Graphics draw={(g) => drawMark(g, progressOf(index))} />
				</Container>
			{/each}
		</Container>
	</MainContainer>
{/if}
