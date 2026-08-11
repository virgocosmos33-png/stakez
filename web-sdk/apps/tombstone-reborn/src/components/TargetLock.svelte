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
	import { filterVisibleCells } from '../game/boardCells';
	import {
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
	} from '../game/constants';
	import { TARGET_ACCENT, TOMBSTONE_FX } from '../game/tombstoneVfx';

	const context = getContext();

	// Iron sights + wanted-poster corner ticks + thin brass scope ring.
	// No white L-brackets, pale HUD discs, clinical scanlines, or soft white wash.
	const STAGGER = 0.16;
	const LOCK_MS = 340;
	const HOLD_MS = 130;
	const FADE_MS = 170;
	const APPROACH = 28;

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
		marks = filterVisibleCells(cells).map((c) => ({
			key: `${c.reel}-${c.row}`,
			cx: originX + getSymbolX(c.reel),
			cy: originY + getCellCenterY(c.reel, c.row),
		}));
	};

	const progressOf = (index: number) => {
		const span = 1 + STAGGER * Math.max(marks.length - 1, 0);
		return Math.min(Math.max(lock.current * span - STAGGER * index, 0), 1);
	};

	context.eventEmitter.subscribeOnMount({
		targetLockShow: async ({ cells, tone: incoming }) => {
			tone = incoming;
			layout(cells);
			if (!marks.length) return;
			lock.set(0, { duration: 0 });
			fade.set(1, { duration: 0 });
			// iron gunsight snapping onto the target
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_lock_snap' });
			await lock.set(1, {
				duration: LOCK_MS + marks.length * STAGGER * LOCK_MS,
				easing: cubicOut,
			});
			await new Promise((resolve) => window.setTimeout(resolve, HOLD_MS));
			// the sight releasing as the reticle lets go
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_lock_release' });
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

	/**
	 * Iron gun sights closing on a cell.
	 *
	 * The previous pass drew a full circle with a coloured stroke laid over it,
	 * which is the thin ring reticle this reskin exists to remove — recolouring
	 * it was never going to help, because the *shape* was the problem. Sights
	 * are drawn instead: a broken iron ring (never a closed circle), a rear
	 * notch, a front post, and wanted-poster corner ticks.
	 */
	const drawMark = (g: import('pixi.js').Graphics, p: number) => {
		if (p <= 0) return;
		const accent = TARGET_ACCENT[tone];
		const halfW = CARD_W / 2;
		const halfH = CARD_H / 2;
		const out = APPROACH * (1 - p);
		const arm = 14;
		const settled = p >= 1;

		// Wanted-poster iron corner ticks, single weight, no coloured overstroke.
		for (const sx of [-1, 1]) {
			for (const sy of [-1, 1]) {
				const x = sx * (halfW + out - 2);
				const y = sy * (halfH + out - 2);
				g.moveTo(x, y - sy * arm);
				g.lineTo(x, y);
				g.lineTo(x - sx * arm, y);
				g.stroke({ color: TOMBSTONE_FX.iron, width: 4.2, alpha: 0.85 + 0.15 * p });
				g.moveTo(x - sx * 1.2, y - sy * (arm - 3) - sy * 1.2);
				g.lineTo(x - sx * 1.2, y - sy * 1.2);
				g.lineTo(x - sx * (arm - 3), y - sy * 1.2);
				g.stroke({ color: TOMBSTONE_FX.ironEdge, width: 1.3, alpha: 0.5 * p });
			}
		}

		// Converging iron edge ticks. A "broken sight ring" used to sit here:
		// four arcs on one radius, which still draws a circle on the card, and
		// the circle is the single shape being purged from every cell
		// decoration. Short dark ticks ride in against the card edges instead,
		// so the approach reads square, like the corner marks.
		if (!settled) {
			const stand = halfH * (0.3 - 0.28 * p);
			const alpha = 0.6 * (1 - p * 0.3);
			for (const sy of [-1, 1]) {
				g.moveTo(-halfW * 0.34, sy * (halfH + stand));
				g.lineTo(halfW * 0.34, sy * (halfH + stand));
				g.stroke({ color: TOMBSTONE_FX.iron, width: 3.4, alpha });
			}
			for (const sx of [-1, 1]) {
				g.moveTo(sx * (halfW + stand), -halfH * 0.3);
				g.lineTo(sx * (halfW + stand), halfH * 0.3);
				g.stroke({ color: TOMBSTONE_FX.iron, width: 3.4, alpha });
			}

			// rear notch at the bottom, front post rising to meet it
			const notchY = halfH * 0.72;
			g.moveTo(-16, notchY);
			g.lineTo(-5, notchY);
			g.lineTo(-5, notchY - 7);
			g.stroke({ color: TOMBSTONE_FX.iron, width: 3.2, alpha: 0.8 });
			g.moveTo(16, notchY);
			g.lineTo(5, notchY);
			g.lineTo(5, notchY - 7);
			g.stroke({ color: TOMBSTONE_FX.iron, width: 3.2, alpha: 0.8 });
			const postY = -halfH * 0.2 + p * halfH * 0.85;
			g.moveTo(0, postY - 11);
			g.lineTo(0, postY + 3);
			g.stroke({ color: TOMBSTONE_FX.iron, width: 3.4, alpha: 0.85 });
			g.moveTo(0, postY - 11);
			g.lineTo(0, postY - 4);
			g.stroke({ color: accent, width: 1.4, alpha: 0.5 });
		}

		if (settled) {
			const breathe = 0.55 + 0.45 * Math.sin(time * 7);
			// sights lined up: two iron blades biting the card edges
			for (const sx of [-1, 1]) {
				g.moveTo(sx * (halfW - 4), -7);
				g.lineTo(sx * (halfW - 4), 7);
				g.stroke({ color: TOMBSTONE_FX.iron, width: 3.4, alpha: 0.6 + 0.25 * breathe });
				g.moveTo(sx * (halfW - 15), 0);
				g.lineTo(sx * (halfW - 4), 0);
				g.stroke({ color: TOMBSTONE_FX.ironEdge, width: 1.6, alpha: 0.45 + 0.2 * breathe });
			}
			// powder wash + iron edge, no coloured border
			g.roundRect(-halfW, -halfH, CARD_W, CARD_H, 6);
			g.fill({ color: TOMBSTONE_FX.powder, alpha: 0.12 + 0.05 * breathe });
			g.roundRect(-halfW + 1, -halfH + 1, CARD_W - 2, CARD_H - 2, 5);
			g.stroke({ color: TOMBSTONE_FX.iron, width: 1.8, alpha: 0.4 + 0.2 * breathe });
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
