<script lang="ts" module>
	/**
	 * LINKED CELL FIRE — every linked/wild cell gets a CONTINUOUS burning ring
	 * that traces its card border and licks outward, card face fully readable
	 * inside. Ported VERBATIM from the WebGL reference "noisy-ring-portrait (1).html"
	 * (fBm-distorted rounded-rect SDF ring graded ember-red -> orange -> hot-white
	 * core + rising embers). The ONLY change from the reference is the animation:
	 * the reference loops forever; here the front climbs bottom->top once on entry
	 * (~IGNITE_MS) then HOLDS fully lit until douse — the "light it, keep it lit"
	 * behaviour asked for, instead of a repeating wipe.
	 *
	 * Rendered as a Pixi v8 fragment Filter over a Texture.WHITE quad per cell —
	 * the SAME procedural-filter technique already proven in CellFlameBorder.svelte
	 * (stock filter vertex, highp precision, premultiplied finalColor + discard).
	 * This replaced a pre-baked flipbook atlas: the shader is continuous by
	 * construction, needs no atlas bake, and animates live.
	 *
	 * Each cell draws its OWN full ring (no shared-edge suppression): the
	 * reference board shows adjacent burning cells each ringed in fire, seams and
	 * all, so a full ring per cell is the correct picture, not a special case.
	 */
	import { Filter, Texture } from 'pixi.js';

	import { SYMBOL_CARD_W, SYMBOL_CARD_H } from '../game/constants';

	export type EmitterEventCellFire =
		| {
				type: 'cellFireShow';
				/** book positions; pad / off-diamond cells are dropped */
				cells: { reel: number; row: number }[];
				/** link size or multiplier — drives how hard the fire burns */
				level?: number;
		  }
		| { type: 'cellFireHide' };

	/** cap so a huge link can never spawn an unbounded number of sprites */
	const MAX_CELLS = 12;

	// The reference shader draws its ring at a FIXED fraction of the quad:
	// box_half_size = vec2(0.42 * ratio, 0.65) — i.e. the ring outline sits at
	// 42% of the quad half-width and 65% of the quad half-height. So to make the
	// ring hug the CARD border (flames licking into the surrounding margin), the
	// quad must be sized so the card occupies exactly that central 42% x 65%:
	//   quad_W = card_W / 0.42,  quad_H = card_H / 0.65.
	// Do NOT change the 0.42 / 0.65 in the shader — retune these ratios instead.
	const RING_FRAC_X = 0.42;
	const RING_FRAC_Y = 0.65;
	const FIRE_W = SYMBOL_CARD_W / RING_FRAC_X;
	const FIRE_H = SYMBOL_CARD_H / RING_FRAC_Y;
	/** Cell-quad aspect. Tall rings (nudge column) keep this ratio and use uYScale. */
	export const FIRE_RATIO = FIRE_W / FIRE_H;

	// Stock Pixi v8 filter vertex: gives 0..1 across the filtered quad.
	const VERTEX = `
in vec2 aPosition;
out vec2 vTextureCoord;
out vec2 vLocalUv;

uniform vec4 uInputSize;
uniform vec4 uOutputFrame;
uniform vec4 uOutputTexture;

vec4 filterVertexPosition( void )
{
    vec2 position = aPosition * uOutputFrame.zw + uOutputFrame.xy;

    position.x = position.x * (2.0 / uOutputTexture.x) - 1.0;
    position.y = position.y * (2.0*uOutputTexture.z / uOutputTexture.y) - uOutputTexture.z;

    return vec4(position, 0.0, 1.0);
}

vec2 filterTextureCoord( void )
{
    return aPosition * (uOutputFrame.zw * uInputSize.zw);
}

void main(void)
{
    gl_Position = filterVertexPosition();
    vTextureCoord = filterTextureCoord();
    // 0..1 over the filtered quad. Texture-space UVs go wrong on a tall
    // column (Pixi filter atlas ≠ sprite), which shrinks the ring to a
    // centred box. aPosition is the geometry itself.
    vLocalUv = aPosition;
}
`;

	// precision pinned to highp so the vertex/fragment stages agree on the shared
	// uInputSize / uOutputFrame uniforms (see CellFlameBorder for the same note).
	const FRAGMENT = `
precision highp float;
#define TWO_PI 6.28318530718

in vec2 vTextureCoord;
in vec2 vLocalUv;
out vec4 finalColor;

uniform vec4 uInputSize;
uniform vec4 uOutputFrame;

uniform float uTime;       // MILLISECONDS (+ per-cell phase) — matches reference u_time
uniform float uRatio;      // cell-quad width / height (locked; do not pass a tall aspect)
uniform float uIntensity;  // 0..1 overall dim (burstDim when overlays are up)
uniform float uProgress;   // 0..1 ONE-SHOT ignite sweep, bottom -> top, then HOLD
uniform float uFlash;      // 0..1 brief hot pop the instant it fully ignites
uniform float uYScale;     // 1 = one card; visH/cardH for a tall column (keeps flame unstretched)
uniform float uHideTop;    // 1 = drop the top bar AND its rounded corners
uniform float uHideBot;    // 1 = drop the bottom bar AND its rounded corners

float rand(vec2 n) {
    return fract(cos(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
}
float noise(vec2 n) {
    const vec2 d = vec2(0.0, 1.0);
    vec2 b = floor(n), f = smoothstep(vec2(0.0), vec2(1.0), fract(n));
    return mix(mix(rand(b), rand(b + d.yx), f.x), mix(rand(b + d.xy), rand(b + d.yy), f.x), f.y);
}
float fbm(vec2 n) {
    float total = 0.0, amplitude = 0.4;
    for (int i = 0; i < 12; i++) {
        total += noise(n) * amplitude;
        n += n;
        amplitude *= 0.6;
    }
    return total;
}

// Signed distance to a rounded rectangle (box half-size b, corner radius r).
float rounded_box_sdf(vec2 uv, vec2 b, float r) {
    vec2 q = abs(uv) - b + r;
    return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
}
float get_ring_shape(vec2 uv, vec2 boxHalf, float corner, float innerRadius, float outerRadius) {
    float distance = rounded_box_sdf(uv, boxHalf, corner) + innerRadius;
    float line_width = outerRadius - innerRadius;
    float ringValue = smoothstep(innerRadius, innerRadius + line_width, distance);
    ringValue -= smoothstep(outerRadius, outerRadius + line_width, distance);
    return clamp(ringValue, 0.0, 1.0);
}

// Rising embers / fire flakes: a tiled field of glowing dots drifting upward,
// swaying and flickering as they age, then looping back to the bottom.
vec2 hash2(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
    return fract(sin(p) * 43758.5453123);
}
float embers(vec2 uv, float time) {
    float density = 6.0;
    vec2 guv = uv * density;
    vec2 cell = floor(guv);
    vec2 f = fract(guv);
    float total = 0.0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vec2 offs = vec2(float(x), float(y));
            vec2 id = cell + offs;
            vec2 rnd = hash2(id);
            float speed = 0.3 + rnd.x * 0.8;
            float life = fract(time * speed + rnd.y * 6.2831);
            float sway = sin(life * TWO_PI * (1.0 + rnd.y) + rnd.x * 10.0) * 0.25;
            vec2 particlePos = offs + vec2(0.5 + sway, 1.4 * life - 0.2);
            float d = length(f - particlePos);
            float size = mix(0.02, 0.06, rnd.y);
            float glow = smoothstep(size, size * 0.1, d);
            float fade = smoothstep(0.0, 0.12, life) * smoothstep(1.0, 0.8, life);
            total += glow * fade;
        }
    }
    return clamp(total, 0.0, 1.0);
}

void main() {
    // vUv (0..1 over the quad), then to [-1, 1] with aspect correction, exactly
    // the reference's  uv = vUv*2-1; uv.x *= u_ratio . NOTE: Pixi texture space
    // has y DOWN, so +uv.y is the SCREEN BOTTOM here (the reference has y UP).
    vec2 uv01 = vLocalUv;
    vec2 uv = uv01 * 2.0 - 1.0;
    // Ignite sweep stays in quad space so a tall column still lights end-to-end.
    float uvYQuad = uv.y;
    uv.x *= uRatio;
    uv.y *= uYScale;

    float noise_scale = 4.0;
    // reference verbatim: t = .0003 * u_time (u_time in MILLISECONDS)
    float t = 0.0003 * uTime;

    float atg = atan(uv.y, uv.x);
    // (1)5 flame STYLE verbatim: NO +2.2*uv.y climbing phase — that omission is
    // exactly what gives (1)5 its softer, even tongue-fringing all around the
    // border instead of a strongly upward-sparking line. (+1e-4 only to keep
    // pow() finite at the exact centre, which is masked out anyway.)
    vec2 polar_uv = vec2(atg, t + 2.0 / pow(length(uv) + 1e-4, 0.5));
    polar_uv *= noise_scale;
    float noise_left = fbm(polar_uv);
    polar_uv.x = mod(polar_uv.x, noise_scale * TWO_PI);
    float noise_right = fbm(polar_uv);
    float noiseV = mix(noise_right, noise_left, smoothstep(-0.2, 0.2, uv.x));

    // box VERBATIM from (1)5: vec2(.42 * u_ratio, .65), corner .12, radius .55,
    // thickness .16, distortion (.92 + .45*noise). The quad is sized so the CARD
    // border lands on this box, so the ring's inner edge hugs the card and
    // flames lick outward.
    vec2 boxHalf = vec2(0.42 * uRatio, 0.65 * uYScale);
    float corner = 0.12;
    float radius = 0.55;
    float thickness = 0.16;
    vec2 uvN = uv * (0.92 + 0.45 * noiseV);
    float ring_shape = get_ring_shape(uvN, boxHalf, corner, radius - 0.8 * thickness, radius + 0.2 * thickness);
    // Drop the end caps (horizontal bar + the rounded-rect corner blobs).
    // Thresholds are in cell units so a tall column only loses the tips.
    float sideEnd = boxHalf.y - corner;
    float keepFromTop = mix(1.0, smoothstep(-(sideEnd + 0.08), -(sideEnd - 0.02), uv.y), uHideTop);
    float keepFromBot = mix(1.0, smoothstep(sideEnd + 0.08, sideEnd - 0.02, uv.y), uHideBot);
    ring_shape *= keepFromTop * keepFromBot;

    // ENTRY then HOLD (this is the ONLY deliberate change from the reference's
    // forever-loop): the front climbs screen-bottom -> top as uProgress 0->1 and
    // OVERSHOOTS both edges (1.15 -> -1.15) so at progress 0 nothing is lit and
    // at progress 1 the WHOLE ring is lit with no dim leading edge — it then just
    // stays fully lit (steady fire) until douse pulls uProgress back to 0.
    float front_y = mix(1.15, -1.15, uProgress);
    float mask = smoothstep(front_y - 0.15, front_y + 0.15, uvYQuad);
    ring_shape *= mask;

    // bright hot edge riding the climbing front (the ignite "surge"); folds away
    // once fully lit so the held state is clean steady fire, not a stuck glow.
    float climbing = smoothstep(0.02, 0.12, uProgress) * (1.0 - smoothstep(0.88, 1.0, uProgress));
    float front_glow = (1.0 - smoothstep(0.0, 0.22, abs(uvYQuad - front_y))) * climbing;

    // fire gradient VERBATIM: deep ember red -> orange -> bright yellow-white core
    vec3 ember_col = vec3(0.5, 0.03, 0.0);
    vec3 flame_col = vec3(1.0, 0.38, 0.03);
    vec3 hot_core = vec3(1.0, 0.92, 0.55);
    vec3 fire_color = mix(ember_col, flame_col, smoothstep(0.0, 0.55, ring_shape));
    fire_color = mix(fire_color, hot_core, smoothstep(0.55, 1.0, ring_shape));

    vec3 color = fire_color * ring_shape;
    color += hot_core * front_glow * ring_shape * 1.3;
    // brief hot flash across the whole ring the instant it fully ignites
    color += hot_core * uFlash * ring_shape * 1.6;

    // scattered rising sparks near the border (reference embers), gated by mask
    float dist_to_outline = abs(rounded_box_sdf(uvN, boxHalf, corner));
    float ember_mask = smoothstep(0.5, 0.0, dist_to_outline) * mask;
    float spark = embers(uv, 1.6 * t) * ember_mask;
    vec3 spark_color = mix(vec3(1.0, 0.5, 0.08), vec3(1.0, 0.88, 0.45), spark);
    color += spark_color * spark;

    float a = clamp(max(max(color.r, color.g), color.b), 0.0, 1.0) * uIntensity;
    if (a <= 0.01) discard;
    finalColor = vec4(color * a, a); // premultiplied
}
`;

	type RingUniforms = {
		uTime: number;
		uRatio: number;
		uIntensity: number;
		uProgress: number;
		uFlash: number;
		uYScale: number;
		uHideTop: number;
		uHideBot: number;
	};

	export const createFireRingFilter = () =>
		Filter.from({
			gl: { vertex: VERTEX, fragment: FRAGMENT, name: 'linked-cell-fire-ring' },
			resources: {
				ringUniforms: {
					uTime: { value: 0, type: 'f32' },
					uRatio: { value: FIRE_RATIO, type: 'f32' },
					uIntensity: { value: 0, type: 'f32' },
					uProgress: { value: 0, type: 'f32' },
					uFlash: { value: 0, type: 'f32' },
					uYScale: { value: 1, type: 'f32' },
					uHideTop: { value: 0, type: 'f32' },
					uHideBot: { value: 0, type: 'f32' },
				},
			},
		});

	export const fireQuadSize = (cardW: number, cardH: number) => ({
		w: cardW / RING_FRAC_X,
		h: cardH / RING_FRAC_Y,
	});

	/**
	 * 1D edge fire for the nudge column. Four thin strips (L/R/T/B) — never a
	 * rounded-rect SDF, so the long sides cannot grow mid-column corners.
	 * depth=0 is the plaque edge; tongues only grow outward.
	 */
	const EDGE_FRAGMENT = `
precision highp float;

in vec2 vLocalUv;
out vec4 finalColor;

uniform vec4 uInputSize;
uniform vec4 uOutputFrame;

uniform float uTime;
uniform float uIntensity;
uniform float uProgress;
uniform float uHorizontal;
uniform float uFlipDepth;

float rand(vec2 n) {
    return fract(cos(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
}
float noise(vec2 n) {
    const vec2 d = vec2(0.0, 1.0);
    vec2 b = floor(n), f = smoothstep(vec2(0.0), vec2(1.0), fract(n));
    return mix(mix(rand(b), rand(b + d.yx), f.x), mix(rand(b + d.xy), rand(b + d.yy), f.x), f.y);
}
float fbm(vec2 n) {
    float total = 0.0, amplitude = 0.4;
    for (int i = 0; i < 12; i++) {
        total += noise(n) * amplitude;
        n += n;
        amplitude *= 0.6;
    }
    return total;
}

void main() {
    float depth = mix(vLocalUv.x, vLocalUv.y, uHorizontal);
    float along = mix(vLocalUv.y, vLocalUv.x, uHorizontal);
    if (uFlipDepth > 0.5) depth = 1.0 - depth;

    float t = 0.0003 * uTime;
    float n = fbm(vec2(along * 8.0, t * 10.0));
    float reach = 0.38 + n * 0.50;
    float ring = smoothstep(0.0, 0.10, depth) * (1.0 - smoothstep(reach * 0.28, reach, depth));

    float yN = vLocalUv.y * 2.0 - 1.0;
    float front = mix(1.15, -1.15, uProgress);
    float sideMask = smoothstep(front - 0.07, front + 0.07, yN);
    float capMask = mix(
        smoothstep(0.0, 0.16, uProgress),
        smoothstep(0.68, 1.0, uProgress),
        uFlipDepth
    );
    float mask = mix(sideMask, capMask, uHorizontal);
    ring *= mask;

    float heat = 1.0 - smoothstep(0.0, reach * 0.55, depth);
    vec3 ember_col = vec3(0.5, 0.03, 0.0);
    vec3 flame_col = vec3(1.0, 0.38, 0.03);
    vec3 hot_core = vec3(1.0, 0.92, 0.55);
    vec3 fire_color = mix(ember_col, flame_col, smoothstep(0.0, 0.55, heat));
    fire_color = mix(fire_color, hot_core, smoothstep(0.55, 1.0, heat));

    vec3 color = fire_color * ring;
    float climbing = smoothstep(0.02, 0.10, uProgress) * (1.0 - smoothstep(0.80, 1.0, uProgress));
    float front_glow = (1.0 - smoothstep(0.0, 0.16, abs(yN - front))) * climbing;
    color += hot_core * front_glow * ring * 1.9;
    float a = clamp(max(max(color.r, color.g), color.b), 0.0, 1.0) * uIntensity;
    if (a <= 0.01) discard;
    finalColor = vec4(color * a, a);
}
`;

	export type EdgeFireUniforms = {
		uTime: number;
		uIntensity: number;
		uProgress: number;
		uHorizontal: number;
		uFlipDepth: number;
	};

	export const createEdgeFireFilter = () =>
		Filter.from({
			gl: { vertex: VERTEX, fragment: EDGE_FRAGMENT, name: 'nudge-edge-fire' },
			resources: {
				edgeUniforms: {
					uTime: { value: 0, type: 'f32' },
					uIntensity: { value: 1, type: 'f32' },
					uProgress: { value: 0, type: 'f32' },
					uHorizontal: { value: 0, type: 'f32' },
					uFlipDepth: { value: 0, type: 'f32' },
				},
			},
		});
</script>

<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut, cubicInOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { filterVisibleCells } from '../game/boardCells';
	import { fxDur } from '../game/fxTiming';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	// The one-shot ignite: the fire climbs visibly bottom -> top over this long,
	// then HOLDS fully lit (see the uProgress sweep in the shader). Kept slow
	// enough (~1s) that the climb actually reads on screen instead of popping.
	// Douse pulls the sweep back down over DOUSE_MS.
	const IGNITE_MS = 1000;
	const DOUSE_MS = 260;
	// Brief hot pop the instant the sweep completes.
	const FLASH_MS = 180;

	let cells = $state<{ reel: number; row: number }[]>([]);
	const ignite = new Tween(0);

	/**
	 * FIRE YIELDS TO FEATURE OVERLAYS. A feature burst / nudge slide can be up over
	 * the same board; a full-strength fire pulled contrast off them. While any is
	 * up the fire drops to BURST_DIM, then swells back. Ref-counted so an
	 * overlapping second overlay hiding does not un-dim, and featureFxFallOut (the
	 * reveal wipe) hard-resets it.
	 */
	const BURST_DIM = 0.45;
	const BURST_DIM_MS = 240;
	const burstDim = new Tween(1);
	let activeOverlays = 0;
	const pushOverlay = () => {
		activeOverlays += 1;
		if (activeOverlays === 1) burstDim.set(BURST_DIM, { duration: BURST_DIM_MS, easing: cubicOut });
	};
	const popOverlay = () => {
		activeOverlays = Math.max(0, activeOverlays - 1);
		if (activeOverlays === 0) burstDim.set(1, { duration: BURST_DIM_MS, easing: cubicOut });
	};
	const resetOverlays = () => {
		activeOverlays = 0;
		burstDim.set(1, { duration: BURST_DIM_MS, easing: cubicOut });
	};

	// One ring filter per possible cell: identical shader, but each carries its
	// own time phase so adjacent cells never animate in lockstep (no clone look).
	const pool = Array.from({ length: MAX_CELLS }, () => {
		const filter = createFireRingFilter();
		return {
			filter,
			uniforms: (filter.resources as Record<string, { uniforms: RingUniforms }>).ringUniforms
				.uniforms,
		};
	});

	const placed = $derived.by(() =>
		cells
			.filter((cell) => cell.reel !== context.stateGame.nudgeCoverReel)
			.slice(0, MAX_CELLS)
			.map((cell) => ({
				key: `${cell.reel}-${cell.row}`,
				cx: getSymbolX(cell.reel),
				cy: getCellCenterY(cell.reel, cell.row),
			})),
	);

	/**
	 * FIRE AUDIO LIFECYCLE. ONE burn bed for the whole feature, never one per
	 * cell. The loop player ignores a second play while running; `burning` makes a
	 * re-show with more cells flare instead of re-triggering the bed. The bed stops
	 * on douse AND destroy so a feature that ends early can never leave fire under
	 * the next spin.
	 */
	let burning = false;
	let burningCells = 0;

	// ignition flash pulse (armed on each fresh cellFireShow, decays over FLASH_MS)
	let hasFlashed = false;
	let flashStart = -1;

	const startFire = (cellCount: number) => {
		if (burning) {
			if (cellCount > burningCells) {
				context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fire_flare', forcePlay: true });
			}
			burningCells = Math.max(burningCells, cellCount);
			return;
		}
		burning = true;
		burningCells = cellCount;
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fire_ignite' });
		context.eventEmitter.broadcast({ type: 'soundLoop', name: 'sfx_fire_loop' });
	};

	const stopFire = (withTail: boolean) => {
		if (!burning) return;
		burning = false;
		burningCells = 0;
		context.eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_fire_loop' });
		if (withTail) context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_fire_out' });
	};

	onDestroy(() => stopFire(false));

	context.eventEmitter.subscribeOnMount({
		cellFireShow: ({ cells: incoming }) => {
			const visible = filterVisibleCells([...incoming]);
			if (!visible.length) return;
			// MERGE — a later feature (gunsmoke after split) adds cells; it
			// must not replace the ones already burning. Lit cells stay lit
			// until the next spin's fall-out.
			const seen = new Set(cells.map((cell) => `${cell.reel}-${cell.row}`));
			const added = visible.filter((cell) => !seen.has(`${cell.reel}-${cell.row}`));
			if (!added.length && cells.length) {
				startFire(cells.length);
				return;
			}
			cells = [...cells, ...added];
			startFire(cells.length);
			if (ignite.current < 0.99) {
				hasFlashed = false;
				flashStart = -1;
				ignite.set(1, { duration: fxDur(IGNITE_MS), easing: cubicInOut });
			}
		},
		cellFireHide: async () => {
			if (!cells.length) return;
			stopFire(true);
			await ignite.set(0, { duration: fxDur(DOUSE_MS) });
			cells = [];
		},
		// dim the fire while a feature overlay owns the foreground, restore after
		featureBurstShow: () => pushOverlay(),
		featureBurstHide: () => popOverlay(),
		nudgeSlideShow: () => pushOverlay(),
		nudgeSlideHide: () => popOverlay(),
		nudgeWaysShow: () => pushOverlay(),
		nudgeWaysHide: () => popOverlay(),
		// next spin: this is the ONLY place fire goes out. Split / morph hide
		// must not douse it mid-round.
		featureFxFallOut: async () => {
			resetOverlays();
			if (!cells.length) return;
			stopFire(true);
			await ignite.set(0, { duration: fxDur(DOUSE_MS) });
			cells = [];
		},
	});

	$effect(() => {
		if (!cells.length) return;
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			const ms = now - start;
			const progress = ignite.current;
			if (!hasFlashed && ignite.target === 1 && progress > 0.985) {
				hasFlashed = true;
				flashStart = now;
			}
			const flash =
				hasFlashed && flashStart >= 0 ? Math.max(0, 1 - (now - flashStart) / FLASH_MS) : 0;

			const n = Math.min(cells.length, pool.length);
			for (let i = 0; i < n; i++) {
				pool[i].uniforms.uTime = ms + i * 3170;
				pool[i].uniforms.uIntensity = burstDim.current;
				pool[i].uniforms.uProgress = progress;
				pool[i].uniforms.uFlash = flash;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<!-- zIndex 8: over the board and feature overlays (0), under CellFlameBorder (9)
	/ CellLightning (10) and the screen panels at 20. One Texture.WHITE quad per
	burning cell; the ring filter paints the fire and discards the rest. -->
<Container zIndex={8}>
	<MainContainer>
		<BoardSpace>
		{#if ignite.current > 0.01}
			{#each placed as cell, i (cell.key)}
				<Container x={cell.cx} y={cell.cy} filters={[pool[i].filter]}>
					<BaseSprite texture={Texture.WHITE} anchor={0.5} width={FIRE_W} height={FIRE_H} />
				</Container>
			{/each}
		{/if}
		</BoardSpace>
	</MainContainer>
</Container>
