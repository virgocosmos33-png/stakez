/**
 * Ways-skim fire sheet.
 *
 * Fire colour steps from Godot "2D fire" (Febucci → godotshaders), CC0:
 * https://godotshaders.com/shader/2d-fire/
 * https://www.febucci.com/2019/05/fire-shader/
 *
 * Hash / value noise from Radiant "Burning Film" (Paul Bakaus), MIT:
 * https://github.com/pbakaus/radiant/blob/main/static/burning-film.html
 * https://radiant-shaders.com/shader/burning-film
 *
 * Noise tex is the high-pay grunge plate (`highPayBg`). Ribbon shape is a
 * traveling lash, not a campfire blob.
 */
import { Filter } from 'pixi.js';

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
    vLocalUv = aPosition;
}
`;

const FRAGMENT = `
precision highp float;

in vec2 vTextureCoord;
in vec2 vLocalUv;
out vec4 finalColor;

uniform sampler2D uTexture;
uniform float uTime;

// Radiant Burning Film — MIT, Paul Bakaus
float hash21(vec2 p) {
    p = fract(p * vec2(443.897, 441.423));
    p += dot(p, p + 19.19);
    return fract(p.x * p.y);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float a = hash21(i);
    float b = hash21(i + vec2(1.0, 0.0));
    float c = hash21(i + vec2(0.0, 1.0));
    float d = hash21(i + vec2(1.0, 1.0));
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

float fbm(vec2 p) {
    float v = 0.0;
    float a = 0.5;
    vec2 shift = vec2(100.0);
    mat2 rot = mat2(0.866, 0.5, -0.5, 0.866);
    for (int i = 0; i < 5; i++) {
        v += a * noise(p);
        p = rot * p * 2.0 + shift;
        a *= 0.5;
    }
    return v;
}

void main() {
    vec2 uv = vLocalUv;
    float t = uTime;

    // Febucci noise_tex + TIME — the high-pay plate, not a stretched sprite UV.
    vec2 plate_uv = fract(vec2(uv.x * 1.15 + t * 0.08, uv.y * 0.72 - t * 0.55));
    vec2 plate_uv2 = fract(vec2(uv.x * 1.85 - t * 0.05, uv.y * 1.1 - t * 0.92));
    float plate = texture(uTexture, plate_uv).r;
    float plate2 = texture(uTexture, plate_uv2).r;
    float noise_value = plate * 0.72 + plate2 * 0.18 + fbm(vec2(uv.x * 4.0, uv.y * 2.2 - t * 1.4)) * 0.1;

    float ribbon = 1.0 - pow(abs(uv.y - 0.5) * 2.0, 1.12);
    ribbon *= smoothstep(0.0, 0.1, uv.x) * smoothstep(1.0, 0.9, uv.x);
    float gradient_value = ribbon * 0.92;

    // Febucci / godotshaders 2D fire: fire where gradient beats noise.
    // smoothstep = the softer edges the 2D-fire notes recommend.
    float step1 = smoothstep(0.0, 0.07, gradient_value - noise_value);
    float step2 = smoothstep(0.0, 0.07, gradient_value - 0.2 - noise_value);
    float step3 = smoothstep(0.0, 0.07, gradient_value - 0.4 - noise_value);

    vec3 brighter_color = vec3(1.0, 0.8, 0.0);
    vec3 middle_color = vec3(1.0, 0.56, 0.0);
    vec3 darker_color = vec3(0.64, 0.2, 0.05);
    vec3 bd_color = mix(brighter_color, darker_color, step1 - step2);
    vec3 col = mix(bd_color, middle_color, step2 - step3);
    col = mix(col, vec3(1.0, 0.94, 0.52), step3 * 0.55);

    float a = step1;
    if (a <= 0.02) discard;
    finalColor = vec4(col * a, a);
}
`;

export type WipeFireUniforms = {
	uTime: number;
};

export const createWipeFireFilter = () => {
	const filter = Filter.from({
		gl: { vertex: VERTEX, fragment: FRAGMENT, name: 'wipe-fire' },
		resources: {
			wipeFireUniforms: {
				uTime: { value: 0, type: 'f32' },
			},
		},
	});
	filter.padding = 10;
	return filter;
};

export const setWipeFireTime = (filter: Filter, seconds: number) => {
	const block = (filter.resources as Record<string, { uniforms: WipeFireUniforms }>)
		.wipeFireUniforms;
	if (block?.uniforms) block.uniforms.uTime = seconds;
};
