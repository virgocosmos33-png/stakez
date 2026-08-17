<script lang="ts" module>
	/**
	 * Shared grade + inferno filters. Same look on the saloon and the timber:
	 * desaturate in base, warm colour in small bonus, ember + drifting smoke
	 * in the big bonus.
	 */
	import { Filter, Texture } from 'pixi.js';

	const VERTEX = `
in vec2 aPosition;
out vec2 vTextureCoord;
out vec2 vLocalUv;
uniform vec4 uInputSize;
uniform vec4 uOutputFrame;
uniform vec4 uOutputTexture;
vec4 filterVertexPosition(void) {
	vec2 position = aPosition * uOutputFrame.zw + uOutputFrame.xy;
	position.x = position.x * (2.0 / uOutputTexture.x) - 1.0;
	position.y = position.y * (2.0 * uOutputTexture.z / uOutputTexture.y) - uOutputTexture.z;
	return vec4(position, 0.0, 1.0);
}
void main(void) {
	gl_Position = filterVertexPosition();
	vTextureCoord = aPosition * (uOutputFrame.zw * uInputSize.zw);
	vLocalUv = aPosition;
}
`;

	const GRADE_FRAGMENT = `
precision highp float;
in vec2 vTextureCoord;
in vec2 vLocalUv;
out vec4 finalColor;
uniform sampler2D uTexture;
uniform vec4 uInputSize;
uniform vec4 uOutputFrame;
uniform float uSat;
uniform float uWarm;
uniform float uEmber;
uniform float uTime;
void main() {
	vec4 src = texture(uTexture, vTextureCoord);
	if (src.a <= 0.01) discard;
	float grey = dot(src.rgb, vec3(0.299, 0.587, 0.114));
	vec3 sat = mix(vec3(grey), src.rgb, uSat);
	vec3 warm = sat * vec3(1.0 + 0.38 * uWarm, 1.0 + 0.10 * uWarm, 1.0 - 0.30 * uWarm);
	float flicker = 0.82 + 0.18 * sin(uTime * 6.4 + vLocalUv.x * 14.0 + vLocalUv.y * 9.0);
	float edge = 1.0 - src.r * 0.35;
	vec3 ember = vec3(1.0, 0.34, 0.04) * uEmber * flicker * edge * 0.42;
	finalColor = vec4(warm + ember, src.a);
}
`;

	const INFERNO_FRAGMENT = `
precision highp float;
in vec2 vTextureCoord;
in vec2 vLocalUv;
out vec4 finalColor;
uniform vec4 uInputSize;
uniform vec4 uOutputFrame;
uniform float uTime;
uniform float uSmoke;
uniform float uFire;
float hash12(vec2 p) {
	vec3 p3 = fract(vec3(p.xyx) * 0.1031);
	p3 += dot(p3, p3.yzx + 33.33);
	return fract((p3.x + p3.y) * p3.z);
}
float noise(vec2 n) {
	vec2 i = floor(n);
	vec2 f = smoothstep(vec2(0.0), vec2(1.0), fract(n));
	float a = hash12(i);
	float b = hash12(i + vec2(1.0, 0.0));
	float c = hash12(i + vec2(0.0, 1.0));
	float d = hash12(i + vec2(1.0, 1.0));
	return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}
float fbm(vec2 n) {
	float t = 0.0;
	float a = 0.5;
	for (int i = 0; i < 5; i++) {
		t += noise(n) * a;
		n *= 2.05;
		a *= 0.5;
	}
	return t;
}
void main() {
	vec2 uv = vLocalUv;
	float t = uTime;
	vec2 drift = vec2(t * 0.07, t * 0.018);
	float n = fbm(uv * vec2(1.7, 1.15) - drift);
	float n2 = fbm(uv * vec2(2.4, 1.6) + drift * 1.4 + 17.0);
	float veil = smoothstep(0.28, 0.72, n) * smoothstep(0.22, 0.7, n2);
	veil *= mix(0.35, 1.0, 1.0 - uv.y);
	vec3 smoke = vec3(0.10, 0.07, 0.05) * veil * uSmoke * 0.85;
	float floorFire = exp(-uv.y * 2.4) * (0.55 + 0.45 * n);
	float sideFire = exp(-min(uv.x, 1.0 - uv.x) * 7.5) * (0.35 + 0.4 * n2);
	float lick = floorFire + sideFire * 0.7;
	vec3 flame = vec3(1.0, 0.28, 0.03) * lick * uFire * 0.72;
	vec3 color = smoke + flame;
	float a = clamp(max(max(color.r, color.g), color.b), 0.0, 1.0);
	if (a <= 0.01) discard;
	finalColor = vec4(color * a, a);
}
`;

	export type GradeUniforms = {
		uSat: number;
		uWarm: number;
		uEmber: number;
		uTime: number;
	};

	export type InfernoUniforms = {
		uTime: number;
		uSmoke: number;
		uFire: number;
	};

	export const createGradeFilter = () =>
		Filter.from({
			gl: { vertex: VERTEX, fragment: GRADE_FRAGMENT, name: 'tr-atmosphere-grade' },
			resources: {
				gradeUniforms: {
					uSat: { value: 0, type: 'f32' },
					uWarm: { value: 0, type: 'f32' },
					uEmber: { value: 0, type: 'f32' },
					uTime: { value: 0, type: 'f32' },
				},
			},
		});

	export const createInfernoFilter = () =>
		Filter.from({
			gl: { vertex: VERTEX, fragment: INFERNO_FRAGMENT, name: 'tr-atmosphere-inferno' },
			resources: {
				infernoUniforms: {
					uTime: { value: 0, type: 'f32' },
					uSmoke: { value: 0, type: 'f32' },
					uFire: { value: 0, type: 'f32' },
				},
			},
		});

	export const gradeUniformsOf = (filter: Filter) =>
		(filter.resources as Record<string, { uniforms: GradeUniforms }>).gradeUniforms.uniforms;

	export const infernoUniformsOf = (filter: Filter) =>
		(filter.resources as Record<string, { uniforms: InfernoUniforms }>).infernoUniforms
			.uniforms;
</script>

<script lang="ts">
	import { Container, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { atmoFire, atmoSmoke } from '../game/atmosphere.svelte';

	const context = getContext();
	const inferno = createInfernoFilter();
	inferno.padding = 0;
	const infernoU = infernoUniformsOf(inferno);

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const show = $derived(atmoSmoke.current > 0.01 || atmoFire.current > 0.01);

	$effect(() => {
		if (!show) return;
		let raf = 0;
		const origin = performance.now();
		const tick = (now: number) => {
			infernoU.uTime = (now - origin) / 1000;
			infernoU.uSmoke = atmoSmoke.current;
			infernoU.uFire = atmoFire.current;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

{#if show}
	<Container zIndex={-1} filters={[inferno]}>
		<BaseSprite
			texture={Texture.WHITE}
			x={0}
			y={0}
			width={canvas.width}
			height={canvas.height}
		/>
	</Container>
{/if}
