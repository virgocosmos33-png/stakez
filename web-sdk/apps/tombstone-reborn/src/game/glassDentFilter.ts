/**
 * Cell-hit glass warp. Same idea as Ksenia Kondrashova's broken-glass pen
 * (codepen.io/ksenia-k/pen/abegNPO): voronoi shards around the impact, each
 * piece slides, UVs pinch into the hole, crack lines stay. Applied as a Pixi
 * v8 Filter on the real symbol so the portrait itself deforms.
 */
import { Filter } from 'pixi.js';

import { SYMBOL_CARD_H, SYMBOL_CARD_W } from './constants';

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
    position.y = position.y * (2.0 * uOutputTexture.z / uOutputTexture.y) - uOutputTexture.z;
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

const FRAGMENT = `
precision highp float;

in vec2 vTextureCoord;
out vec4 finalColor;

uniform sampler2D uTexture;
uniform vec2 uHit;
uniform float uStrength;
uniform float uSeed;
uniform float uRatio;

vec2 hash2(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
    return fract(sin(p + uSeed) * 43758.5453123);
}

void shardAt(vec2 uv, out vec2 center, out float edge) {
    float best = 8.0;
    float second = 8.0;
    vec2 bestC = uHit;
    for (int i = 0; i < 12; i++) {
        vec2 rnd = hash2(vec2(float(i) + 0.7, uSeed * 1.37));
        vec2 site = i == 0
            ? uHit
            : uHit + (rnd - 0.5) * vec2(0.92, 0.92 / max(uRatio, 0.2));
        vec2 delta = (uv - site) * vec2(uRatio, 1.0);
        float dist = length(delta);
        if (dist < best) {
            second = best;
            best = dist;
            bestC = site;
        } else if (dist < second) {
            second = dist;
        }
    }
    center = bestC;
    edge = second - best;
}

void main() {
    vec2 uv = vTextureCoord;
    vec2 center;
    float edge;
    shardAt(uv, center, edge);

    vec2 fromHit = (uv - uHit) * vec2(uRatio, 1.0);
    float r = length(fromHit);
    vec2 dir = r > 0.0008 ? fromHit / r : vec2(0.0, 0.0);

    float punch = exp(-r * 3.4) * uStrength;
    vec2 slide = (center - uHit) * uStrength * 0.28;
    vec2 dent = -dir * punch * 0.20;
    vec2 warped = uv + slide + dent;

    vec4 color = texture(uTexture, clamp(warped, 0.0, 1.0));
    if (warped.x < 0.0 || warped.x > 1.0 || warped.y < 0.0 || warped.y > 1.0) {
        color *= 0.0;
    }

    float crack = smoothstep(0.05, 0.0, edge) * uStrength;
    vec3 shade = mix(vec3(0.07, 0.05, 0.04), vec3(0.98, 0.94, 0.86), 0.62);
    color.rgb = mix(color.rgb, shade, crack * 0.9);
    color.rgb *= 1.0 - punch * 0.28;

    vec2 chroma = dir * crack * 0.012;
    float rCh = texture(uTexture, clamp(warped + chroma, 0.0, 1.0)).r;
    float bCh = texture(uTexture, clamp(warped - chroma, 0.0, 1.0)).b;
    color.r = mix(color.r, rCh, crack * 0.65);
    color.b = mix(color.b, bCh, crack * 0.65);

    finalColor = color;
}
`;

export type GlassDentUniforms = {
	uHit: Float32Array;
	uStrength: number;
	uSeed: number;
	uRatio: number;
};

export const createGlassDentFilter = () => {
	const filter = Filter.from({
		gl: { vertex: VERTEX, fragment: FRAGMENT, name: 'gunsmoke-glass-dent' },
		resources: {
			dentUniforms: {
				uHit: { value: new Float32Array([0.5, 0.5]), type: 'vec2<f32>' },
				uStrength: { value: 0, type: 'f32' },
				uSeed: { value: 1, type: 'f32' },
				uRatio: { value: SYMBOL_CARD_W / SYMBOL_CARD_H, type: 'f32' },
			},
		},
	});
	const uniforms = (filter.resources as Record<string, { uniforms: GlassDentUniforms }>)
		.dentUniforms.uniforms;
	filter.padding = 16;
	return { filter, uniforms };
};
