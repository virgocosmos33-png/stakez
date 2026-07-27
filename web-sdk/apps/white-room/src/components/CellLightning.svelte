<script lang="ts" module>
	// Black & white electric lightning that crackles around the BORDER of the
	// special cell whose FEATURE is currently executing. The feature handlers
	// drive it: `cellLightningOn` fades the lightning in on that feature's cell
	// (a bottom cell {reel} or a side slot {side, slotRow}) and keeps it crackling
	// for as long as the feature animation runs; `cellLightningOff` fades it out
	// so the next feature's cell can light up. Features fire in the fixed order
	// (bottom L->R, right bottom->top, left top->bottom) from the math events.
	export type LightningCell = { reel?: number; side?: 'left' | 'right'; slotRow?: number };
	export type EmitterEventCellLightning =
		| { type: 'cellLightningOn'; cells: LightningCell[] }
		| { type: 'cellLightningOff' }
		| { type: 'cellLightningHide' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { BOARD_DIMENSIONS } from '../game/constants';
	import { cellFrames } from '../game/chassisArt';

	const context = getContext();

	const SPEED = 1;
	const INTENSITY = 1;
	const SIZE = 1;
	// black & white palette: white-hot core, soft white mid, dark contrast halo.
	const CORE = 0xffffff;
	const GLOW = 0xf2f2f2;
	const DEEP = 0x0a0a0a;

	const FADE_IN = 180;
	const FADE_OUT = 260;
	const SIDE_SLOTS = 3;
	const BOTTOM_START = (BOARD_DIMENSIONS.x - 3) / 2; // bottom cells sit under reels 1-3
	const OUTSET = 3; // trace just outside the iron so the bolt reads clear of it

	// the openings are not square, so the ring is traced per-axis
	type Cell = { cx: number; cy: number; hx: number; hy: number; seed: number };

	let cells = $state<Cell[]>([]);
	let show = $state(false);
	let time = $state(0);
	let onAt = 0;
	let offAt = 0; // 0 = still on

	// Reads the SAME measured chassis openings LockedSlots fills, so the ring can
	// never drift off the cell it is supposed to be electrifying.
	const locate = (c: { reel?: number; side?: 'left' | 'right'; slotRow?: number }): Cell | null => {
		const frames = cellFrames(context.stateGameDerived.boardLayout());
		let key: string | null = null;
		let seed = 0;
		if (c.side != null && c.slotRow != null && c.slotRow < SIDE_SLOTS) {
			key = `${c.side}:${c.slotRow}`;
			seed = (c.side === 'right' ? 20 : 30) + c.slotRow;
		} else if (c.reel != null && c.reel >= BOTTOM_START && c.reel < BOTTOM_START + 3) {
			// only reels 1-3 have a rendered bottom cell (outer wild reels don't)
			key = `bottom:${c.reel - BOTTOM_START}`;
			seed = c.reel;
		}
		const frame = key ? frames[key] : null;
		if (!frame) return null;
		return {
			cx: frame.cx,
			cy: frame.cy,
			hx: frame.w / 2 + OUTSET,
			hy: frame.h / 2 + OUTSET,
			seed,
		};
	};

	// unit-square perimeter samples with outward normal + tangent (clockwise from
	// top-left). Jittered along the normal (crackle) with a little tangent wobble.
	const PER_EDGE = 9;
	type Sample = { x: number; y: number; nx: number; ny: number; tx: number; ty: number };
	const base: Sample[] = (() => {
		const out: Sample[] = [];
		const edges = [
			{ ax: -1, ay: -1, bx: 1, by: -1, nx: 0, ny: -1 },
			{ ax: 1, ay: -1, bx: 1, by: 1, nx: 1, ny: 0 },
			{ ax: 1, ay: 1, bx: -1, by: 1, nx: 0, ny: 1 },
			{ ax: -1, ay: 1, bx: -1, by: -1, nx: -1, ny: 0 },
		];
		for (const e of edges) {
			for (let i = 0; i < PER_EDGE; i++) {
				const f = i / PER_EDGE;
				out.push({
					x: e.ax + (e.bx - e.ax) * f,
					y: e.ay + (e.by - e.ay) * f,
					nx: e.nx,
					ny: e.ny,
					tx: e.ny,
					ty: -e.nx,
				});
			}
		}
		return out;
	})();

	const fract = (v: number) => v - Math.floor(v);
	const rand = (n: number) => fract(Math.sin(n * 12.9898) * 43758.5453);
	const crackle = (seed: number, t: number) =>
		0.6 * Math.sin(seed * 1.3 + t) +
		0.4 * Math.sin(seed * 2.7 + t * 1.7) +
		(rand(seed + Math.floor(t * 30)) - 0.5) * 0.8;

	context.eventEmitter.subscribeOnMount({
		cellLightningOn: ({ cells: incoming }) => {
			const located = incoming
				.map(locate)
				.filter((c): c is Cell => c !== null);
			if (!located.length) return;
			cells = located;
			onAt = performance.now();
			offAt = 0;
			show = true;
		},
		cellLightningOff: () => {
			if (show && offAt === 0) offAt = performance.now();
		},
		cellLightningHide: () => {
			show = false;
			cells = [];
			offAt = 0;
		},
	});

	onMount(() => {
		let raf = 0;
		const tick = (now: number) => {
			time = now;
			// fully faded after an off -> stop drawing
			if (show && offAt > 0 && now - offAt > FADE_OUT) {
				show = false;
				cells = [];
				offAt = 0;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	// brightness envelope: fade in when switched on, hold while the feature runs,
	// fade out once the handler switches it off.
	const envelope = (now: number) => {
		const up = Math.min(1, (now - onAt) / FADE_IN);
		const down = offAt > 0 ? Math.max(0, 1 - (now - offAt) / FADE_OUT) : 1;
		return up * down;
	};

	const strokeLoop = (
		g: import('pixi.js').Graphics,
		pts: { x: number; y: number }[],
		color: number,
		width: number,
		alpha: number,
	) => {
		if (alpha <= 0.01 || pts.length < 2) return;
		g.moveTo(pts[0].x, pts[0].y);
		for (let i = 1; i < pts.length; i++) g.lineTo(pts[i].x, pts[i].y);
		g.lineTo(pts[0].x, pts[0].y);
		g.stroke({ color, width, alpha, cap: 'round', join: 'round' });
	};

	const drawAll = (g: import('pixi.js').Graphics, now: number) => {
		if (!cells.length) return;
		const b = envelope(now);
		if (b <= 0.02) return;
		const tt = (now / 1000) * 9 * SPEED;
		for (const cell of cells) {
			const amp = (1.6 + 4.6 * INTENSITY * b) * SIZE;
			const pts = base.map((s, idx) => {
				const c = crackle(cell.seed * 13.1 + idx * 0.9, tt + idx * 0.5);
				const w = crackle(cell.seed * 5.3 + idx * 2.1, tt * 1.3) * 0.4;
				return {
					x: cell.cx + s.x * cell.hx + s.nx * c * amp + s.tx * w * amp,
					y: cell.cy + s.y * cell.hy + s.ny * c * amp + s.ty * w * amp,
				};
			});
			strokeLoop(g, pts, DEEP, 15 * SIZE, 0.28 * b);
			strokeLoop(g, pts, GLOW, 6.5 * SIZE, 0.5 * b);
			strokeLoop(g, pts, CORE, 2.4 * SIZE, 0.98 * b);
			// a bright spark racing around the border while this cell is active
			const sp = (tt * 0.06) % 1;
			const p = pts[Math.floor(sp * pts.length) % pts.length];
			g.circle(p.x, p.y, 7 * SIZE);
			g.fill({ color: GLOW, alpha: 0.5 * b });
			g.circle(p.x, p.y, 3.2 * SIZE);
			g.fill({ color: CORE, alpha: 0.98 * b });
		}
	};
</script>

{#if show}
	<MainContainer>
		{@const now = time}
		<Container>
			<Graphics draw={(g) => drawAll(g, now)} />
		</Container>
	</MainContainer>
{/if}
