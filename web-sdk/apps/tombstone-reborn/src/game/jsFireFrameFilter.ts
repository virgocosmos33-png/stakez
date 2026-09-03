/**
 * js-fire-frame — the pasted proto, unstretched.
 * Cell 160×224 (5/7), pad 22, wrap 204×268. Uniform scale only.
 */
import { Filter } from 'pixi.js';

import { SYMBOL_CARD_H } from './constants';

const PROTO_CELL_W = 160;
const PROTO_CELL_H = 224;
const PROTO_PAD = 22;
const PROTO_WRAP_W = PROTO_CELL_W + PROTO_PAD * 2;
const PROTO_WRAP_H = PROTO_CELL_H + PROTO_PAD * 2;
const SCALE = SYMBOL_CARD_H / PROTO_CELL_H;
export const CELL_FIRE_W = PROTO_WRAP_W * SCALE;
export const CELL_FIRE_H = PROTO_WRAP_H * SCALE;
/** Extra canvas above the wrap so tongues overflow the cell top. Never clip. */
const PROTO_TOP_OVERFLOW = 240;
export const CELL_FIRE_TOP_OVERFLOW = PROTO_TOP_OVERFLOW * SCALE;

/**
 * Timed to `fire blaze up.mp3` peak (~480ms). The old running-max RMS table
 * held for ~140ms then snapped — that was the hitch. Cubic-out is C1-smooth
 * and still whooshes (fast start, settle into the hold).
 */
export const CELL_FIRE_CLIMB_MS = 480;

/** Proto is 1. Set back to 1 to undo the density bump. */
export const CELL_FIRE_DENSITY = 1.18;

/** Proto is 1. Tongue height. Set back to 1 to undo. */
export const CELL_FIRE_HEIGHT = 2.2;

/** Continuous blaze-up. No plateaus, no end snap. */
export const fireAttackEase = (t: number) => {
	const x = t < 0 ? 0 : t > 1 ? 1 : t;
	const r = 1 - x;
	return 1 - r * r * r;
};

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
    vLocalUv = aPosition;
}
`;

const FRAGMENT = `
precision highp float;

in vec2 vTextureCoord;
in vec2 vLocalUv;
out vec4 finalColor;

uniform vec4 uInputSize;
uniform vec4 uOutputFrame;

uniform float uTime;
uniform float uReveal;
uniform float uIntensity;
uniform float uSize;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(
        mix(hash(i),               hash(i + vec2(1.0, 0.0)), u.x),
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

float embers(vec2 uv, float time, float mask, float density) {
    float total = 0.0;
    for (int pass = 0; pass < 2; pass++) {
        float dens = (pass == 0 ? 5.0 : 11.0) * mix(0.55, 1.65, clamp(density * 0.5, 0.0, 1.5));
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

vec2 entry_mask(vec2 uv, vec2 box, float progress) {
    // Tween owns the ease. Extra hermite + a fat soft band made the whoosh crawl.
    float p = clamp(progress, 0.0, 1.0);
    float soft = 0.12;
    float front_y = mix(-box.y - 0.16, box.y + 0.26, p);
    float lit = 1.0 - smoothstep(front_y - soft, front_y + soft, uv.y);
    float front = 1.0 - smoothstep(0.0, 0.18, abs(uv.y - front_y));
    return vec2(clamp(lit, 0.0, 1.0), clamp(front, 0.0, 1.0));
}

void main() {
    // Proto wrap is 204×268, pinned to the BOTTOM of the filter quad.
    // Extra height is top overflow only. Width-lock so the ring never stretches.
    const float PW = 204.0;
    const float PH = 268.0;
    vec2 frame = max(uOutputFrame.zw, vec2(1.0));
    float fit = frame.x / PW;
    vec2 protoSize = vec2(PW, PH) * fit;
    vec2 origin = vec2(0.5 * (frame.x - protoSize.x), frame.y - protoSize.y);
    vec2 protoPx = (vLocalUv * frame - origin) / fit;
    if (protoPx.x < 0.0 || protoPx.x > PW || protoPx.y > PH) discard;

    vec2 vUv = vec2(protoPx.x / PW, 1.0 - protoPx.y / PH);
    vec2 uv = vUv * 2.0 - 1.0;
    uv.x *= PW / PH;
    vec2 box = vec2(160.0 / PH, 224.0 / PH);
    float corner = min(0.08, min(box.x, box.y) * 0.22);
    float sd = rounded_box_sdf(uv, box, corner);
    float stroke_dist = abs(sd);

    float t = uTime;
    vec2 entry = entry_mask(uv, box, uReveal);
    float lit = entry.x;
    float frontBand = entry.y;

    float e = 0.0025;
    vec2 grad = vec2(
        rounded_box_sdf(uv + vec2(e, 0.0), box, corner) - rounded_box_sdf(uv - vec2(e, 0.0), box, corner),
        rounded_box_sdf(uv + vec2(0.0, e), box, corner) - rounded_box_sdf(uv - vec2(0.0, e), box, corner)
    );
    float gLen = length(grad);
    grad = gLen > 1e-5 ? grad / gLen : vec2(0.0, 1.0);

    float dens = ${CELL_FIRE_DENSITY.toFixed(2)};
    float size = max(uSize, 0.01);
    float thickMul = ${(1 + (CELL_FIRE_DENSITY - 1) * 0.55).toFixed(2)};

    vec2 np = uv * vec2(2.8, 3.6) * dens;
    np.y -= t * 2.6;
    np.x += (noise(vec2(uv.y * 4.0 * dens, t * 1.5)) - 0.5) * 0.08;

    float n_big = fbm(np * 1.05);
    float n_mid = fbm(np * 2.7 + 17.0);
    float n_sml = fbm(np * 7.0 + 41.0);

    float tonguePow = mix(1.4, 2.6, clamp((dens - 0.35) / 2.15, 0.0, 1.0));
    float tongues = pow(n_big, tonguePow);
    float body = pow(n_mid, 1.35);
    float wisps = n_sml;
    float n = clamp(tongues * 0.75 + body * 0.5 + wisps * 0.28, 0.0, 1.6);

    float d_out = max(sd, 0.0);
    float outside = smoothstep(-0.002, 0.01, sd);

    vec2 closest = uv - grad * d_out;
    vec2 dlt = uv - closest;
    float rise = max(dlt.y, 0.0);
    float sink = max(-dlt.y, 0.0);
    float lateral = abs(dlt.x);

    float maxRise = (0.05 + n * 0.22 + tongues * 0.2) * size;
    maxRise *= 1.0 + max(grad.y, 0.0) * 0.85;
    maxRise *= 1.0 - max(-grad.y, 0.0) * 0.45;

    float maxLat = (0.02 + body * 0.035 + wisps * 0.02) * thickMul;
    maxLat *= 1.0 + abs(grad.x) * 0.35;

    float vert = rise / max(maxRise, 0.001);
    float horiz = (lateral + sink * 3.0) / max(maxLat, 0.001);
    float flameShape = length(vec2(horiz, vert));
    float flame = 0.0;
    if (sd > 0.0) {
        flame = 1.0 - smoothstep(0.0, 1.0, flameShape);
        float edgePow = mix(2.05, 1.2, clamp((thickMul - 0.35) / 2.15, 0.0, 1.0));
        flame = pow(clamp(flame, 0.0, 1.0), edgePow);
        flame *= pow(clamp(n - vert * 0.55, 0.0, 1.2), 1.15);
    }

    float baseBand = (1.0 - smoothstep(0.0, 0.018 * thickMul, d_out)) * outside;
    baseBand = pow(clamp(baseBand, 0.0, 1.0), 1.4) * 0.55;
    flame = max(flame, baseBand * mix(0.7, 1.15, n));
    flame *= outside;

    float ribbonW = (0.012 + wisps * 0.015) * thickMul;
    float ribbon = 1.0 - smoothstep(0.0, ribbonW, stroke_dist);
    ribbon = pow(ribbon, 1.5);

    float fire = max(flame, ribbon * 0.85) * lit;

    float heat = 0.0;
    if (sd > 0.0) {
        heat = 1.0 - clamp(vert * 0.65 + horiz * 0.35, 0.0, 1.0);
        heat = max(heat, 1.0 - clamp(d_out / max(0.02 * thickMul, 0.001), 0.0, 1.0));
    }
    heat = max(heat, ribbon) * lit;

    float coreW = 0.007 * thickMul;
    float coreSoftW = 0.024 * thickMul;
    float core = (1.0 - smoothstep(0.0, coreW, stroke_dist)) * lit;
    float core_soft = (1.0 - smoothstep(0.0, coreSoftW, stroke_dist)) * lit;

    float bloom = fire * fire * 0.4;

    float front = frontBand * lit;
    front *= smoothstep(0.1, 0.0, stroke_dist);

    vec3 c_tip  = vec3(0.50196078, 0.03137255, 0.0);
    vec3 c_mid  = vec3(1.0, 0.30196078, 0.01960784);
    vec3 c_body = vec3(1.0, 0.58039216, 0.07058824);
    vec3 c_hot  = vec3(1.0, 0.90196078, 0.47843137);
    vec3 c_wire = vec3(1.0, 0.98039216, 0.90196078);
    vec3 c_spark = vec3(1.0, 0.4, 0.03921569);

    float h = clamp(heat, 0.0, 1.0);
    vec3 fire_col = mix(c_tip, c_mid, smoothstep(0.0, 0.3, h));
    fire_col = mix(fire_col, c_body, smoothstep(0.25, 0.55, h));
    fire_col = mix(fire_col, c_hot, smoothstep(0.5, 0.92, h));

    vec3 col = fire_col * fire * 1.75;
    col += c_mid * bloom;
    col += c_wire * core * 1.5;
    col += c_hot * core_soft * 0.75;
    col += c_hot * front * fire * 0.85;

    float flash = smoothstep(0.88, 0.96, uReveal) * (1.0 - smoothstep(0.96, 1.0, uReveal));
    col += c_hot * flash * (fire + core) * 1.1;

    float ember_zone = lit * outside * smoothstep(0.25 * size, 0.0, d_out) * smoothstep(0.0, 0.12, fire + core);
    ember_zone = max(ember_zone, lit * ribbon * 0.35);
    float spark = embers(uv, t * 1.2, ember_zone, dens);
    col += mix(c_spark, c_hot, clamp(spark, 0.0, 1.0)) * spark;

    col = clamp(col, 0.0, 1.0);
    float a = max(max(col.r, col.g), col.b) * uIntensity;
    if (a <= 0.01) discard;
    finalColor = vec4(col * a, a);
}
`;

export type CellFireUniforms = {
	uTime: number;
	uReveal: number;
	uIntensity: number;
	uSize: number;
};

export const createCellFireFilter = () => {
	const filter = Filter.from({
		gl: { vertex: VERTEX, fragment: FRAGMENT, name: 'js-fire-frame' },
		resources: {
			fireUniforms: {
				uTime: { value: 0, type: 'f32' },
				uReveal: { value: 0, type: 'f32' },
				uIntensity: { value: 1, type: 'f32' },
				uSize: { value: CELL_FIRE_HEIGHT, type: 'f32' },
			},
		},
	});
	filter.padding = 0;
	return filter;
};
