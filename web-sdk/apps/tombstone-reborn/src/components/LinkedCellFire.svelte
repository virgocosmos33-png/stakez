<script lang="ts" module>
	/**
	 * LINKED CELL FIRE — js-fire-frame on each split cell (the pasted proto).
	 * Tongues grow off the card: fat on top, thin on the sides. Climb once, HOLD.
	 * Nudge totems still use createFireRingFilter below.
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

	// Ring outline sits at this fraction of the quad so the SDF lands on the
	// card bezel. Do NOT change these in the shader — retune the ratios here.
	const RING_FRAC_X = 0.42;
	const RING_FRAC_Y = 0.65;
	// Card bezel is 16px on a 300px frame (WinSweep). In shader units the box
	// half-height is RING_FRAC_Y, so the matching corner is 16/292 * 1.3.
	const RING_CORNER = 0.12;
	/** Reference HTML (1) thickness. Top keeps this; sides pinch in the shader. */
	const RING_THICKNESS = 0.2;
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
uniform float uBoxX;       // ring half-width as a fraction of the quad (cell = 0.42)
uniform float uBoxY;       // ring half-height as a fraction of the quad (cell = 0.65)
uniform float uCorner;     // rounded-rect radius in shader units (cell = 0.12)
uniform float uThickness;  // ring thickness in shader units (cell stroke)
uniform float uLockBox;    // 1 = noise offsets distance (tall totem); 0 = cell uv-scale

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
    // Reference +2.2*uv.y climbs +Y (up in WebGL). Pixi Y is down, so flip.
    vec2 polar_uv = vec2(atg, t - 2.2 * uv.y + 2.0 / pow(length(uv) + 1e-4, 0.5));
    polar_uv *= noise_scale;
    float noise_left = fbm(polar_uv);
    polar_uv.x = mod(polar_uv.x, noise_scale * TWO_PI);
    float noise_right = fbm(polar_uv);
    float noiseV = mix(noise_right, noise_left, smoothstep(-0.2, 0.2, uv.x));

    vec2 boxHalf = vec2(uBoxX * uRatio, uBoxY * uYScale);
    float corner = uCorner;
    float radius = 0.55;
    float thickness = uThickness;
    // Reference warp: uv * (0.9 + 0.55 * noise). Full on TOP. Pinch X on
    // the sides so the card stays a rectangle, not a puffy oval.
    float topN = smoothstep(-boxHalf.y * 0.08, -boxHalf.y * 0.62, uv.y);
    float sideN = smoothstep(boxHalf.x * 0.48, boxHalf.x * 0.90, abs(uv.x)) * (1.0 - topN * 0.85);
    float warp = 0.9 + 0.55 * noiseV;
    vec2 uvFire = vec2(uv.x * mix(warp, 1.0, sideN * 0.90), uv.y * mix(mix(1.05, warp, 0.40), warp, topN));
    float thick = mix(thickness * 0.40, thickness, topN);
    float ring_shape = get_ring_shape(uvFire, boxHalf, corner, radius - 0.8 * thick, radius + 0.2 * thick);

    // Tall totem only: offset distance, never UV-scale the full height.
    float locked = rounded_box_sdf(uv, boxHalf, corner) - (noiseV - 0.5) * thick * 2.2;
    float locked_inner = radius - 0.8 * thick;
    float locked_outer = radius + 0.2 * thick;
    float locked_w = locked_outer - locked_inner;
    float locked_ring = smoothstep(locked_inner, locked_inner + locked_w, locked + locked_inner);
    locked_ring -= smoothstep(locked_outer, locked_outer + locked_w, locked + locked_inner);
    ring_shape = mix(ring_shape, clamp(locked_ring, 0.0, 1.0), uLockBox);
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

    float dist_to_outline = abs(rounded_box_sdf(uvFire, boxHalf, corner));
    float ember_mask = smoothstep(mix(0.22, 0.5, topN), 0.0, dist_to_outline) * mask;
    float spark = embers(uv, 1.6 * t) * ember_mask;
    vec3 spark_color = mix(vec3(1.0, 0.5, 0.08), vec3(1.0, 0.88, 0.45), spark);
    color += spark_color * spark;

    float a = clamp(max(max(color.r, color.g), color.b), 0.0, 1.0) * uIntensity;
    if (a <= 0.01) discard;
    finalColor = vec4(color * a, a); // premultiplied
}
`;

	export type RingUniforms = {
		uTime: number;
		uRatio: number;
		uIntensity: number;
		uProgress: number;
		uFlash: number;
		uYScale: number;
		uHideTop: number;
		uHideBot: number;
		uBoxX: number;
		uBoxY: number;
		uCorner: number;
		uThickness: number;
		uLockBox: number;
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
					uBoxX: { value: RING_FRAC_X, type: 'f32' },
					uBoxY: { value: RING_FRAC_Y, type: 'f32' },
					uCorner: { value: RING_CORNER, type: 'f32' },
					uThickness: { value: RING_THICKNESS, type: 'f32' },
					uLockBox: { value: 0, type: 'f32' },
				},
			},
		});

	export const fireQuadSize = (
		cardW: number,
		cardH: number,
		fracX = RING_FRAC_X,
		fracY = RING_FRAC_Y,
	) => ({
		w: cardW / fracX,
		h: cardH / fracY,
	});

	/**
	 * Tall totem ring (NUDGE header + shaft + x16). Pixel-space SDF so fBm
	 * cannot shrink the box — the cell shader's `uv * noise` pull is a % of
	 * the FULL height, which ate the header. Distortion only offsets distance.
	 */
	const COLUMN_FRAGMENT = `
precision highp float;
#define TWO_PI 6.28318530718

in vec2 vTextureCoord;
in vec2 vLocalUv;
out vec4 finalColor;

uniform vec4 uInputSize;
uniform vec4 uOutputFrame;

uniform float uTime;
uniform float uIntensity;
uniform float uProgress;
uniform float uQuadW;
uniform float uQuadH;
uniform float uTotemW;
uniform float uTotemH;
uniform float uCorner;
uniform float uThickness;

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
float rounded_box_sdf(vec2 uv, vec2 b, float r) {
    vec2 q = abs(uv) - b + r;
    return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
}

void main() {
    vec2 px = vec2(vLocalUv.x * uQuadW, vLocalUv.y * uQuadH);
    vec2 center = vec2(uQuadW, uQuadH) * 0.5;
    vec2 halfBox = vec2(uTotemW, uTotemH) * 0.5;
    float dist = rounded_box_sdf(px - center, halfBox, uCorner);

    float t = 0.0003 * uTime;
    vec2 fromC = px - center;
    float atg = atan(fromC.y, fromC.x);
    float n = fbm(vec2(atg * 2.4, t * 10.0));
    dist -= (n - 0.32) * uThickness * 1.6;

    float inner = -2.0;
    float outer = uThickness;
    float ring = smoothstep(inner - 3.0, inner, dist) * (1.0 - smoothstep(outer, outer + 6.0, dist));

    float uvYQuad = vLocalUv.y * 2.0 - 1.0;
    float front_y = mix(1.15, -1.15, uProgress);
    ring *= smoothstep(front_y - 0.15, front_y + 0.15, uvYQuad);

    vec3 ember_col = vec3(0.5, 0.03, 0.0);
    vec3 flame_col = vec3(1.0, 0.38, 0.03);
    vec3 hot_core = vec3(1.0, 0.92, 0.55);
    float heat = 1.0 - smoothstep(inner, outer, dist);
    vec3 fire_color = mix(ember_col, flame_col, smoothstep(0.0, 0.55, heat));
    fire_color = mix(fire_color, hot_core, smoothstep(0.55, 1.0, heat));

    vec3 color = fire_color * ring;
    float a = clamp(max(max(color.r, color.g), color.b), 0.0, 1.0) * uIntensity;
    if (a <= 0.01) discard;
    finalColor = vec4(color * a, a);
}
`;

	export type ColumnFireUniforms = {
		uTime: number;
		uIntensity: number;
		uProgress: number;
		uQuadW: number;
		uQuadH: number;
		uTotemW: number;
		uTotemH: number;
		uCorner: number;
		uThickness: number;
	};

	export const createColumnFireFilter = () =>
		Filter.from({
			gl: { vertex: VERTEX, fragment: COLUMN_FRAGMENT, name: 'nudge-column-fire' },
			resources: {
				columnUniforms: {
					uTime: { value: 0, type: 'f32' },
					uIntensity: { value: 1, type: 'f32' },
					uProgress: { value: 0, type: 'f32' },
					uQuadW: { value: 1, type: 'f32' },
					uQuadH: { value: 1, type: 'f32' },
					uTotemW: { value: 1, type: 'f32' },
					uTotemH: { value: 1, type: 'f32' },
					uCorner: { value: 14, type: 'f32' },
					uThickness: { value: 16, type: 'f32' },
				},
			},
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
    float sideMask = smoothstep(front - 0.15, front + 0.15, yN);
    // caps stay fully on once the column is lit — a progress gate was
    // hiding the top/bottom bars and leaving the corners empty
    float mask = mix(sideMask, 1.0, uHorizontal);
    ring *= mask;

    float heat = 1.0 - smoothstep(0.0, reach * 0.55, depth);
    vec3 ember_col = vec3(0.5, 0.03, 0.0);
    vec3 flame_col = vec3(1.0, 0.38, 0.03);
    vec3 hot_core = vec3(1.0, 0.92, 0.55);
    vec3 fire_color = mix(ember_col, flame_col, smoothstep(0.0, 0.55, heat));
    fire_color = mix(fire_color, hot_core, smoothstep(0.55, 1.0, heat));

    vec3 color = fire_color * ring;
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
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { BOARD_FIRE_Z } from '../game/constants';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { filterVisibleCells, isNudgeCoveredReel } from '../game/boardCells';
	import { fxDur } from '../game/fxTiming';
	import { playThemedOnce, stopThemed } from '../game/sfxTheme';
	import { sound } from '../game/sound';
	import {
		CELL_FIRE_CLIMB_MS,
		CELL_FIRE_H,
		CELL_FIRE_HEIGHT,
		CELL_FIRE_TOP_OVERFLOW,
		CELL_FIRE_W,
		createCellFireFilter,
		fireAttackEase,
		type CellFireUniforms,
	} from '../game/jsFireFrameFilter';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	// Bottom-to-top whoosh. Smooth cubic-out — no RMS stairs.
	const IGNITE_MS = CELL_FIRE_CLIMB_MS;
	const DOUSE_MS = 260;

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
		const filter = createCellFireFilter();
		return {
			filter,
			uniforms: (filter.resources as Record<string, { uniforms: CellFireUniforms }>).fireUniforms
				.uniforms,
		};
	});

	const placed = $derived.by(() =>
		cells
			.filter((cell) => !isNudgeCoveredReel(cell.reel))
			.slice(0, MAX_CELLS)
			.map((cell) => ({
				key: `${cell.reel}-${cell.row}`,
				cx: getSymbolX(cell.reel),
				cy: getCellCenterY(cell.reel, cell.row),
			})),
	);

	/**
	 * FIRE AUDIO. One burst + one burn bed for the whole feature, never per
	 * cell. The burn file is a one-shot (not a loop). Stop both on douse.
	 */
	let burning = false;
	let burningCells = 0;
	/** Persist across extra cells so the tongues do not rewind. */
	let clockOrigin = 0;
	let loopKick: number | null = null;

	const startFire = (cellCount: number) => {
		if (burning) {
			burningCells = Math.max(burningCells, cellCount);
			return;
		}
		burning = true;
		burningCells = cellCount;
		sound.stop({ name: 'sfx_fire_ignite' });
		sound.stop({ name: 'sfx_fire_loop' });
		playThemedOnce('sfx_fire_ignite', { forcePlay: true });
		// The burn bed is a long file. Start it on the next frame so decode/start
		// does not stall the first blaze paint.
		if (loopKick != null) cancelAnimationFrame(loopKick);
		loopKick = requestAnimationFrame(() => {
			loopKick = null;
			if (!burning) return;
			playThemedOnce('sfx_fire_loop', { forcePlay: true });
		});
	};

	const stopFire = (_withTail: boolean) => {
		if (!burning) return;
		burning = false;
		burningCells = 0;
		if (loopKick != null) {
			cancelAnimationFrame(loopKick);
			loopKick = null;
		}
		stopThemed('sfx_fire_ignite');
		stopThemed('sfx_fire_loop');
		sound.stop({ name: 'sfx_fire_ignite' });
		sound.stop({ name: 'sfx_fire_loop' });
	};

	onDestroy(() => stopFire(false));

	context.eventEmitter.subscribeOnMount({
		cellFireShow: async ({ cells: incoming }) => {
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
				await ignite.set(1, { duration: fxDur(IGNITE_MS), easing: fireAttackEase });
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
		if (!cells.length) {
			clockOrigin = 0;
			return;
		}
		if (!clockOrigin) clockOrigin = performance.now();
		const origin = clockOrigin;
		let raf = 0;
		const tick = (now: number) => {
			const sec = (now - origin) / 1000;
			const progress = ignite.current;
			const n = Math.min(cells.length, pool.length);
			for (let i = 0; i < n; i++) {
				pool[i].uniforms.uTime = sec + i * 0.37;
				pool[i].uniforms.uIntensity = burstDim.current;
				pool[i].uniforms.uReveal = progress;
				pool[i].uniforms.uSize = CELL_FIRE_HEIGHT;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	// Compile the fire program once at mount so the first blaze does not hitch.
	const warmFilter = createCellFireFilter();
</script>

<!-- Over pocket wood / split faces, under slash and win panels. -->
<Container zIndex={BOARD_FIRE_Z}>
	<MainContainer>
		<BoardSpace>
		<Container x={-4096} y={-4096} alpha={0.01} eventMode="none">
			<Container filters={[warmFilter]}>
				<BaseSprite texture={Texture.WHITE} width={8} height={8} />
			</Container>
		</Container>
		{#each placed as cell, i (cell.key)}
			<Container x={cell.cx} y={cell.cy - CELL_FIRE_TOP_OVERFLOW / 2} filters={[pool[i].filter]}>
				<BaseSprite
					texture={Texture.WHITE}
					anchor={0.5}
					width={CELL_FIRE_W}
					height={CELL_FIRE_H + CELL_FIRE_TOP_OVERFLOW}
				/>
			</Container>
		{/each}
		</BoardSpace>
	</MainContainer>
</Container>
