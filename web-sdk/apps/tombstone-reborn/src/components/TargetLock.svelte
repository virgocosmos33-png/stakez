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
	import { Tween } from 'svelte/motion';
	import { cubicOut, quadIn } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { filterSplitCells } from '../game/boardCells';
	import {
		SYMBOL_CARD_W as CARD_W,
		SYMBOL_CARD_H as CARD_H,
	} from '../game/constants';
	import { TARGET_ACCENT, TOMBSTONE_FX } from '../game/tombstoneVfx';
	import { fxDur, fxWait } from '../game/fxTiming';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	// WANTED-POSTER LOCK: four bold iron corner brackets snap inward onto the
	// card, with an additive Kenney spark "muzzle snap" flashing at the moment of
	// lock. No thin scope ring, iron-sight notch/post, HUD discs, or white wash.
	const STAGGER = 0.16;
	const LOCK_MS = 340;
	const HOLD_MS = 130;
	const FADE_MS = 170;
	const APPROACH = 30;
	/** Kenney celebration spark used as the muzzle-snap flash on lock */
	const SPARK_KEY = 'win_celeb_light_07.png';

	type Mark = { key: string; cx: number; cy: number };

	let marks = $state<Mark[]>([]);
	let tone = $state<TargetTone>('split');
	let time = $state(0);

	const lock = new Tween(0);
	const fade = new Tween(0);

	const layout = (cells: { reel: number; row: number }[]) => {
		marks = filterSplitCells(cells).map((c) => ({
			key: `${c.reel}-${c.row}`,
			cx: getSymbolX(c.reel),
			cy: getCellCenterY(c.reel, c.row),
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
				duration: fxDur(LOCK_MS + marks.length * STAGGER * LOCK_MS),
				easing: cubicOut,
			});
			await fxWait(HOLD_MS);
			// the sight releasing as the reticle lets go
			context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_lock_release' });
			await fade.set(0, { duration: fxDur(FADE_MS), easing: quadIn });
			marks = [];
		},
		targetLockHide: () => {
			fade.set(0, { duration: 0 });
			marks = [];
		},
	});

	$effect(() => {
		if (!marks.length) return;
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
	 * Bold wanted-poster iron corner brackets snapping onto a cell. The brackets
	 * ride in from `APPROACH` px out and bite the card corners; an accent-tinted
	 * inner keyline (per feature tone) sharpens as they lock, and a faint accent
	 * border breathes once settled. No scope ring / sight notch / white wash —
	 * the muzzle spark (Sprite, below) carries the "snap".
	 */
	const drawMark = (g: import('pixi.js').Graphics, p: number) => {
		if (p <= 0) return;
		const accent = TARGET_ACCENT[tone];
		const halfW = CARD_W / 2;
		const halfH = CARD_H / 2;
		const out = APPROACH * (1 - p);
		const arm = 22 + 6 * p;
		const settled = p >= 1;
		const breathe = settled ? 0.7 : 0;

		for (const sx of [-1, 1]) {
			for (const sy of [-1, 1]) {
				const x = sx * (halfW + out);
				const y = sy * (halfH + out);
				// heavy iron bracket
				g.moveTo(x, y - sy * arm);
				g.lineTo(x, y);
				g.lineTo(x - sx * arm, y);
				g.stroke({ color: TOMBSTONE_FX.iron, width: 5, alpha: 0.9 });
				// accent-tinted inner keyline, brightening as it locks
				g.moveTo(x - sx * 2.2, y - sy * (arm - 4) - sy * 2.2);
				g.lineTo(x - sx * 2.2, y - sy * 2.2);
				g.lineTo(x - sx * (arm - 4), y - sy * 2.2);
				g.stroke({ color: accent, width: 1.9, alpha: 0.35 + 0.45 * p + 0.2 * breathe });
			}
		}

		if (settled) {
			// faint accent frame, breathing, to hold the lock read
			g.roundRect(-halfW, -halfH, CARD_W, CARD_H, 8);
			g.stroke({ color: accent, width: 2, alpha: 0.26 + 0.22 * breathe });
		}
	};

	/** additive muzzle-snap spark: spikes as the brackets lock (p -> 1), then
	 * holds a soft breathing glow while the lock is settled. */
	const sparkAlpha = (p: number) => {
		if (p <= 0) return 0;
		const flash = p > 0.72 ? (p - 0.72) / 0.28 : 0;
		const glow = p >= 1 ? 0.28 + 0.14 * Math.sin(time * 7) : 0;
		return Math.min(1, Math.max(flash, glow));
	};
</script>

{#if marks.length}
	<MainContainer>
		<BoardSpace>
		<Container alpha={fade.current}>
			{#each marks as mark, index (mark.key)}
				{@const p = progressOf(index)}
				<Container x={mark.cx} y={mark.cy}>
					<Sprite
						key={SPARK_KEY}
						anchor={0.5}
						width={CARD_W * 1.05}
						height={CARD_W * 1.05}
						tint={TARGET_ACCENT[tone]}
						alpha={sparkAlpha(p)}
						blendMode="add"
					/>
					<Graphics draw={(g) => drawMark(g, p)} />
				</Container>
			{/each}
		</Container>
		</BoardSpace>
	</MainContainer>
{/if}
