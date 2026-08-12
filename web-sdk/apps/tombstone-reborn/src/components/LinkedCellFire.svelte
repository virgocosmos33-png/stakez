<script lang="ts" module>
	/**
	 * LINKED CELL FIRE — every linked/wild cell gets a CONTINUOUS burning frame
	 * that traces its card border and licks outward, card face fully readable
	 * inside. Ported VERBATIM from the WebGL reference "final fire frame.html":
	 * ONE rounded-rect SDF stroke, fire generated from distance-to-stroke only,
	 * with GRAVITY (tongues stretch upward along the outward normal), multi-octave
	 * fBm tongues/body/wisps, a bright ribbon core, bloom and two-pass rising
	 * embers, graded tip-red -> orange -> hot-white.
	 *
	 * Two deliberate changes from the reference:
	 *   1. Entry: the reference loops (climb 1.8s, hold 1s, fade, repeat). Here the
	 *      front climbs bottom->top ONCE on entry (~IGNITE_MS, driven by uProgress)
	 *      then HOLDS fully lit until douse — "light it, keep it lit".
	 *   2. Compositing: the reference draws opaque on black; here alpha comes from
	 *      the fire's own intensity so it composites over the board (transparent
	 *      where there is no flame), premultiplied, with a discard.
	 * The frame stroke size is fed as uBox (card half-size), so the outline lands
	 * exactly on the card border and the flames fill the FLAME_PAD margin.
	 *
	 * Rendered as a Pixi v8 fragment Filter over a Texture.WHITE quad per cell —
	 * the SAME procedural-filter technique proven in CellFlameBorder.svelte (stock
	 * filter vertex, highp precision, premultiplied finalColor + discard).
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

	// "final fire frame.html" takes the frame stroke half-size as a uniform
	// (u_box) and adds a flat FLAME_PAD margin of empty canvas all around so the
	// gravity-stretched flame tongues (reach up to ~0.42 in y-normalized UV) have
	// room to lick outward without clipping. So the quad = card + pad on every
	// side, and u_box is the CARD half-size normalised by the quad HEIGHT exactly
	// as the reference does (halfX = w/cssH, halfY = h/cssH). This makes the
	// burning outline land EXACTLY on the card border at any card aspect.
	const FLAME_PAD = Math.round(SYMBOL_CARD_H * 0.42);
	const FIRE_W = SYMBOL_CARD_W + FLAME_PAD * 2;
	const FIRE_H = SYMBOL_CARD_H + FLAME_PAD * 2;
	const FIRE_RATIO = FIRE_W / FIRE_H;
	// reference: halfX = w / cssH, halfY = h / cssH (BOTH divided by height)
	const BOX_X = SYMBOL_CARD_W / FIRE_H;
	const BOX_Y = SYMBOL_CARD_H / FIRE_H;

	// Stock Pixi v8 filter vertex: gives 0..1 across the filtered quad.
	const VERTEX = `
in vec2 aPosition;
out vec2 vTextureCoord;

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
}
`;

	// precision pinned to highp so the vertex/fragment stages agree on the shared
	// uInputSize / uOutputFrame uniforms (see CellFlameBorder for the same note).
	const FRAGMENT = `
precision highp float;

in vec2 vTextureCoord;
out vec4 finalColor;

uniform vec4 uInputSize;
uniform vec4 uOutputFrame;

uniform float uTime;       // MILLISECONDS (+ per-cell phase) — reference u_time
uniform float uRatio;      // quad width / height (reference u_ratio)
uniform vec2  uBox;        // card half-size in y-normalised UV (reference u_box)
uniform float uIntensity;  // 0..1 overall dim (burstDim when overlays are up)
uniform float uProgress;   // 0..1 ONE-SHOT ignite climb bottom -> top, then HOLD
uniform float uFlash;      // 0..1 brief hot pop the instant it fully ignites

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}
float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(
        mix(hash(i),                 hash(i + vec2(1.0, 0.0)), u.x),
        mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x),
        u.y
    );
}
float fbm(vec2 p) {
    float v = 0.0;
    float a = 0.5;
    for (int i = 0; i < 6; i++) {
        v += a * noise(p);
        p *= 2.02;
        a *= 0.5;
    }
    return v;
}
float rounded_box_sdf(vec2 p, vec2 b, float r) {
    vec2 q = abs(p) - b + r;
    return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
}
vec2 hash2(vec2 p) {
    return fract(sin(vec2(
        dot(p, vec2(127.1, 311.7)),
        dot(p, vec2(269.5, 183.3))
    )) * 43758.5453);
}
// Two-pass rising embers (reference): a coarse field of larger sparks plus a
// fine field of small ones, drifting upward and fading as they age.
float embers(vec2 uv, float time, float mask) {
    float total = 0.0;
    for (int pass = 0; pass < 2; pass++) {
        float dens = pass == 0 ? 5.0 : 11.0;
        vec2 g = uv * dens;
        vec2 cell = floor(g);
        vec2 f = fract(g);
        for (int y = -1; y <= 1; y++) {
            for (int x = -1; x <= 1; x++) {
                vec2 off = vec2(float(x), float(y));
                vec2 id = cell + off + float(pass) * 17.0;
                vec2 rnd = hash2(id);
                float life = fract(time * (0.3 + rnd.x * 0.85) + rnd.y * 6.28);
                vec2 p = off + vec2(
                    0.5 + (rnd.y - 0.5) * 0.28 * life,
                    life * (1.75 + 0.45 * float(pass)) - 0.06
                );
                float d = length(f - p);
                float sz = mix(pass == 0 ? 0.018 : 0.007, pass == 0 ? 0.055 : 0.028, rnd.x);
                float glow = smoothstep(sz, 0.0, d);
                float fade = smoothstep(0.0, 0.1, life) * smoothstep(1.0, 0.68, life);
                total += glow * fade * (pass == 0 ? 1.0 : 0.55);
            }
        }
    }
    return clamp(total * mask, 0.0, 1.4);
}

void main() {
    // Filter uv 0..1 over the quad, then FLIP Y so +uv.y is the SCREEN TOP. The
    // reference is y-UP (gravity reaches toward +y, ignite climbs -y -> +y); Pixi
    // texture space is y-DOWN. Flipping here lets the reference run verbatim and
    // read correctly on screen — flames reach UP, ignite climbs from the bottom.
    vec2 uv01 = vTextureCoord * uInputSize.xy / uOutputFrame.zw;
    vec2 uv = vec2(uv01.x, 1.0 - uv01.y) * 2.0 - 1.0;
    uv.x *= uRatio;

    vec2 box = uBox;
    float corner = min(0.08, min(box.x, box.y) * 0.22);
    float sd = rounded_box_sdf(uv, box, corner);
    float stroke_dist = abs(sd);

    float t = uTime * 0.001;

    // ENTRY (climb bottom -> top) then HOLD — replaces the reference's forever
    // loop. uProgress 0->1 (driven over IGNITE_MS) sweeps the front up and
    // OVERSHOOTS the top (+0.85) so at progress 1 the whole frame is lit; there
    // is no loop fade-out, it simply holds fully lit until douse.
    float progress = clamp(uProgress, 0.0, 1.0);
    progress = progress * progress * (3.0 - 2.0 * progress);
    float front_y = mix(-box.y - 0.25, box.y + 0.85, progress);
    float lit = 1.0 - smoothstep(front_y - 0.28, front_y + 0.35, uv.y);

    // outward normal of the stroke (for gravity: tongues stretch up the normal)
    float e = 0.0025;
    vec2 grad = vec2(
        rounded_box_sdf(uv + vec2(e, 0.0), box, corner) - rounded_box_sdf(uv - vec2(e, 0.0), box, corner),
        rounded_box_sdf(uv + vec2(0.0, e), box, corner) - rounded_box_sdf(uv - vec2(0.0, e), box, corner)
    );
    float gLen = length(grad);
    grad = gLen > 1e-5 ? grad / gLen : vec2(0.0, 1.0);

    vec2 np = uv * vec2(2.8, 3.6);
    np.y -= t * 2.6;
    np.x += (noise(vec2(uv.y * 4.0, t * 1.5)) - 0.5) * 0.08;

    float n_big = fbm(np * 1.05);
    float n_mid = fbm(np * 2.7 + 17.0);
    float n_sml = fbm(np * 7.0 + 41.0);

    float tongues = pow(n_big, 2.1);
    float body    = pow(n_mid, 1.35);
    float wisps   = n_sml;
    float n = clamp(tongues * 0.75 + body * 0.5 + wisps * 0.28, 0.0, 1.6);

    float reach = 0.015 + n * 0.14 + tongues * 0.12;
    float up_amt = max(grad.y, 0.0);
    float side_amt = abs(grad.x);
    float down_amt = max(-grad.y, 0.0);
    float grav_scale = 1.0 + up_amt * 1.4 + side_amt * 0.25 - down_amt * 0.4;
    float thickness = min(reach * grav_scale, 0.42);

    float d_out = max(sd, 0.0);
    float flame = 1.0 - smoothstep(0.0, thickness, d_out);
    flame = pow(clamp(flame, 0.0, 1.0), 1.55);
    flame *= mix(0.5, 1.25, clamp(n * 0.9, 0.0, 1.0));
    flame *= smoothstep(-0.006, 0.012, sd);

    float ribbon = 1.0 - smoothstep(0.0, 0.012 + wisps * 0.015, stroke_dist);
    ribbon = pow(ribbon, 1.5);

    float fire = max(flame, ribbon * 0.85) * lit;

    float heat = 1.0 - clamp(d_out / max(thickness, 0.001), 0.0, 1.0);
    heat *= smoothstep(-0.006, 0.012, sd);
    heat = max(heat, ribbon) * lit;

    float core = (1.0 - smoothstep(0.0, 0.007, stroke_dist)) * lit;
    float core_soft = (1.0 - smoothstep(0.0, 0.024, stroke_dist)) * lit;

    float bloom = fire * fire * 0.4;

    float front = (1.0 - smoothstep(0.0, 0.32, abs(uv.y - front_y))) * lit;
    front *= smoothstep(0.1, 0.0, stroke_dist);

    vec3 c_tip   = vec3(0.5, 0.03, 0.0);
    vec3 c_mid   = vec3(1.0, 0.3, 0.02);
    vec3 c_body  = vec3(1.0, 0.58, 0.07);
    vec3 c_hot   = vec3(1.0, 0.9, 0.48);
    vec3 c_white = vec3(1.0, 0.98, 0.9);

    float h = clamp(heat, 0.0, 1.0);
    vec3 fire_col = mix(c_tip, c_mid, smoothstep(0.0, 0.3, h));
    fire_col = mix(fire_col, c_body, smoothstep(0.25, 0.55, h));
    fire_col = mix(fire_col, c_hot, smoothstep(0.5, 0.92, h));

    vec3 col = fire_col * fire * 1.75;
    col += c_mid * bloom;
    col += c_white * core * 1.5;
    col += c_hot * core_soft * 0.75;
    col += c_hot * front * fire * 0.85;

    // brief hot pop the instant it fully ignites (reference's climb-end flash,
    // here driven by the component's one-shot uFlash pulse)
    col += c_hot * uFlash * (fire + core) * 1.1;

    float ember_zone = lit * smoothstep(0.25, 0.0, stroke_dist) * smoothstep(0.0, 0.12, fire + core);
    float spark = embers(uv, t * 1.2, ember_zone);
    col += mix(vec3(1.0, 0.4, 0.04), vec3(1.0, 0.85, 0.4), clamp(spark, 0.0, 1.0)) * spark;

    col = clamp(col, 0.0, 1.0);

    // Composite over the board: alpha from the fire's OWN intensity so it fades
    // to TRANSPARENT where there is no flame (the reference draws opaque on
    // black). Premultiplied, with a discard on empty pixels.
    float a = clamp(max(col.r, max(col.g, col.b)), 0.0, 1.0) * uIntensity;
    if (a <= 0.004) discard;
    finalColor = vec4(col * a, a);
}
`;

	type RingUniforms = {
		uTime: number;
		uRatio: number;
		uBox: Float32Array;
		uIntensity: number;
		uProgress: number;
		uFlash: number;
	};

	const createFireRingFilter = () =>
		Filter.from({
			gl: { vertex: VERTEX, fragment: FRAGMENT, name: 'linked-cell-fire-frame' },
			resources: {
				ringUniforms: {
					uTime: { value: 0, type: 'f32' },
					uRatio: { value: FIRE_RATIO, type: 'f32' },
					// constant per card: the stroke half-size the flame frame traces
					uBox: { value: new Float32Array([BOX_X, BOX_Y]), type: 'vec2<f32>' },
					uIntensity: { value: 0, type: 'f32' },
					uProgress: { value: 0, type: 'f32' },
					uFlash: { value: 0, type: 'f32' },
				},
			},
		});
</script>

<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { filterVisibleCells } from '../game/boardCells';

	const context = getContext();

	// Fast entry so the cell catches fire hard for impact (~0.3s), then holds
	// full. Douse pulls the sweep back down over DOUSE_MS.
	const IGNITE_MS = 300;
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

	const placed = $derived.by(() => {
		const layout = context.stateGameDerived.boardLayout();
		const originX = layout.x - layout.width * 0.5;
		const originY = layout.y - layout.height * 0.5;
		return cells.slice(0, MAX_CELLS).map((cell) => ({
			key: `${cell.reel}-${cell.row}`,
			cx: originX + getSymbolX(cell.reel),
			cy: originY + getCellCenterY(cell.reel, cell.row),
		}));
	});

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
			cells = visible;
			startFire(visible.length);
			// arm the ignition flash for this fresh light-up
			hasFlashed = false;
			flashStart = -1;
			ignite.set(1, { duration: IGNITE_MS, easing: cubicOut });
		},
		cellFireHide: async () => {
			if (!cells.length) return;
			stopFire(true);
			await ignite.set(0, { duration: DOUSE_MS });
			cells = [];
		},
		// dim the fire while a feature overlay owns the foreground, restore after
		featureBurstShow: () => pushOverlay(),
		featureBurstHide: () => popOverlay(),
		nudgeSlideShow: () => pushOverlay(),
		nudgeSlideHide: () => popOverlay(),
		featureFxFallOut: () => resetOverlays(),
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			// uTime is MILLISECONDS (reference `u_time`); the flame noise/embers
			// formulas expect ms. Each cell gets its own ms phase so adjacent
			// rings never animate in lockstep (no clone look).
			const ms = now - start;
			// The ignite ramp IS the one-shot sweep (bottom -> top). Once it
			// reaches 1 the sweep holds full, so the ring STAYS on fire until a
			// hide pulls it back down. burstDim only dims (never resets) the fire
			// while a feature overlay owns the foreground.
			const progress = ignite.current;

			// fire a single hot pop the instant the sweep completes
			if (!hasFlashed && ignite.target === 1 && progress > 0.985) {
				hasFlashed = true;
				flashStart = now;
			}
			const flash =
				hasFlashed && flashStart >= 0 ? Math.max(0, 1 - (now - flashStart) / FLASH_MS) : 0;

			for (let i = 0; i < pool.length; i++) {
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
		{#if ignite.current > 0.01}
			{#each placed as cell, i (cell.key)}
				<Container x={cell.cx} y={cell.cy} filters={[pool[i].filter]}>
					<BaseSprite texture={Texture.WHITE} anchor={0.5} width={FIRE_W} height={FIRE_H} />
				</Container>
			{/each}
		{/if}
	</MainContainer>
</Container>
