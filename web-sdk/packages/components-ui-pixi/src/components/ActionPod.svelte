<script lang="ts" module>
	export type PodCircle = { x: number; y?: number; r: number };
</script>

<script lang="ts">
	/**
	 * ActionPod — a single continuous "metaball" backing that fuses a row of
	 * round action buttons (turbo · SPIN · autoplay) into one liquid pod with
	 * smooth CONCAVE fillets between neighbours. Drawn BEHIND the buttons so the
	 * icons stay on top and keep working.
	 *
	 * REVERSIBLE: this whole feature is gated behind the `MORPH_BUTTONS` flag in
	 * the layout files that mount it. Set that flag to `false` (or remove the
	 * `<ActionPod .../>` block + import) to fully revert. Nothing else changes.
	 */
	import * as PIXI from 'pixi.js';
	import { Graphics } from 'pixi-svelte';

	type Props = {
		/** button circle centres + radii, in the SAME coord space as the buttons */
		circles: PodCircle[];
		/** concave connecting-arc radius (bigger = softer/shallower valley) */
		fillet?: number;
		/** extra radius added to each circle so a thin rim peeks around each button */
		pad?: number;
		fill?: number;
		fillAlpha?: number;
		/** subtle top-lit sheen colour */
		sheen?: number;
		rim?: number;
		rimWidth?: number;
		rimAlpha?: number;
		/** soft outer glow */
		glow?: number;
		glowWidth?: number;
		glowAlpha?: number;
	};

	// Dark STEEL/SLATE-BLUE rim: the same steel every HUD button/border uses.
	// NO GOLD anywhere on the HUD. The glow is a very subtle steel wash (nearly
	// a dark shadow) so the pod reads as chrome, never brass/yellow.
	const HUD_STEEL = 0x3a4552;

	const {
		circles,
		fillet = 44,
		pad = 6,
		fill = 0x15151d,
		fillAlpha = 0.98,
		sheen = 0x3a3a48,
		rim = HUD_STEEL,
		rimWidth = 3,
		rimAlpha = 0.92,
		glow = HUD_STEEL,
		glowWidth = 10,
		glowAlpha = 0.1,
	}: Props = $props();

	const TWO_PI = Math.PI * 2;
	const norm = (a: number) => {
		while (a <= -Math.PI) a += TWO_PI;
		while (a > Math.PI) a -= TWO_PI;
		return a;
	};

	type Neck = {
		Lt: [number, number];
		Lb: [number, number];
		Rt: [number, number];
		Rb: [number, number];
		topC: [number, number];
		botC: [number, number];
	} | null;

	/** Build the single closed outline (flat [x0,y0,x1,y1,...]) for the pod. */
	const buildBoundary = (cs: PodCircle[], rf: number, extra: number): number[] => {
		const n = cs.length;
		if (n === 0) return [];
		const cx = cs.map((c) => c.x);
		const cy = cs.map((c) => c.y ?? 0);
		const r = cs.map((c) => c.r + extra);

		// pairwise necks (external fillet tangent to both circles, both sides)
		const necks: Neck[] = [];
		for (let i = 0; i < n - 1; i++) {
			const xL = cx[i];
			const rL = r[i];
			const xR = cx[i + 1];
			const rR = r[i + 1];
			const d = xR - xL;
			if (d <= 0) {
				necks.push(null);
				continue;
			}
			const fx = (xL + xR) / 2 + ((rL - rR) * (rL + rR + 2 * rf)) / (2 * d);
			const val = (rL + rf) * (rL + rf) - (fx - xL) * (fx - xL);
			if (val <= 0) {
				necks.push(null);
				continue;
			}
			const fy = Math.sqrt(val);
			const Lb: [number, number] = [xL + (rL / (rL + rf)) * (fx - xL), (rL / (rL + rf)) * fy];
			const Rb: [number, number] = [xR + (rR / (rR + rf)) * (fx - xR), (rR / (rR + rf)) * fy];
			const Lt: [number, number] = [Lb[0], -Lb[1]];
			const Rt: [number, number] = [Rb[0], -Rb[1]];
			necks.push({ Lt, Lb, Rt, Rb, topC: [fx, -fy], botC: [fx, fy] });
		}

		const pts: number[] = [];
		const ang = (p: [number, number], ox: number, oy: number) => Math.atan2(p[1] - oy, p[0] - ox);
		const arc = (ox: number, oy: number, rad: number, a0: number, a1: number, steps: number) => {
			for (let i = 0; i <= steps; i++) {
				const a = a0 + (a1 - a0) * (i / steps);
				pts.push(ox + rad * Math.cos(a), oy + rad * Math.sin(a));
			}
		};
		// minor arc between two points that both lie on the fillet circle
		const filletArc = (c: [number, number], rad: number, p0: [number, number], p1: [number, number]) => {
			const a0 = ang(p0, c[0], c[1]);
			const a1 = a0 + norm(ang(p1, c[0], c[1]) - a0);
			arc(c[0], c[1], rad, a0, a1, 14);
		};

		const ARC_STEPS = 26;

		// ---- TOP edge: left -> right, over the tops ----
		for (let i = 0; i < n; i++) {
			const left = i === 0 ? -Math.PI : ang(necks[i - 1]!.Rt, cx[i], cy[i]);
			const right = i === n - 1 ? 0 : ang(necks[i]!.Lt, cx[i], cy[i]);
			arc(cx[i], cy[i], r[i], left, right, ARC_STEPS);
			if (i < n - 1 && necks[i]) filletArc(necks[i]!.topC, rf, necks[i]!.Lt, necks[i]!.Rt);
		}
		// ---- BOTTOM edge: right -> left, under the bottoms ----
		for (let i = n - 1; i >= 0; i--) {
			const right = i === n - 1 ? 0 : ang(necks[i]!.Lb, cx[i], cy[i]);
			const left = i === 0 ? Math.PI : ang(necks[i - 1]!.Rb, cx[i], cy[i]);
			arc(cx[i], cy[i], r[i], right, left, ARC_STEPS);
			if (i > 0 && necks[i - 1]) filletArc(necks[i - 1]!.botC, rf, necks[i - 1]!.Rb, necks[i - 1]!.Lb);
		}
		return pts;
	};

	const outline = $derived(buildBoundary(circles, fillet, pad));

	const draw = (g: PIXI.Graphics) => {
		if (outline.length < 6) return;

		// soft outer glow
		g.poly(outline);
		g.stroke({ color: glow, width: glowWidth, alpha: glowAlpha, alignment: 0.5, join: 'round' });

		// dark body
		g.poly(outline);
		g.fill({ color: fill, alpha: fillAlpha });

		// top-lit sheen (upper half wash) — faint, so it just gives volume
		const sheenPts: number[] = [];
		let minX = Infinity;
		let maxX = -Infinity;
		let minY = Infinity;
		for (let i = 0; i < outline.length; i += 2) {
			minX = Math.min(minX, outline[i]);
			maxX = Math.max(maxX, outline[i]);
			minY = Math.min(minY, outline[i + 1]);
		}
		for (let i = 0; i < outline.length; i += 2) {
			if (outline[i + 1] <= 0) sheenPts.push(outline[i], outline[i + 1]);
		}
		if (sheenPts.length >= 6) {
			g.poly(sheenPts);
			g.fill({ color: sheen, alpha: 0.16 });
		}

		// dark separation line then steel rim
		g.poly(outline);
		g.stroke({ color: 0x000000, width: rimWidth + 1.5, alpha: 0.5, alignment: 0.5, join: 'round' });
		g.poly(outline);
		g.stroke({ color: rim, width: rimWidth, alpha: rimAlpha, alignment: 0.5, join: 'round' });
	};
</script>

<Graphics {draw} />
