<script lang="ts" module>
	import { Filter } from 'pixi.js';

	import { SCENE_ART as SCENE_ART_SRC } from '../game/saloonLamps';
	import { createGradeFilter, gradeUniformsOf } from './AtmosphereFx.svelte';

	export const SCENE_ART = SCENE_ART_SRC;

	const bgGrade = createGradeFilter();
	const bgGradeU = gradeUniformsOf(bgGrade);

	const FILTER_VERTEX = `
in vec2 aPosition;
out vec2 vTextureCoord;
uniform vec4 uInputSize;
uniform vec4 uOutputFrame;
uniform vec4 uOutputTexture;
vec4 filterVertexPosition(void) {
	vec2 position = aPosition * uOutputFrame.zw + uOutputFrame.xy;
	position.x = position.x * (2.0 / uOutputTexture.x) - 1.0;
	position.y = position.y * (2.0 * uOutputTexture.z / uOutputTexture.y) - uOutputTexture.z;
	return vec4(position, 0.0, 1.0);
}
vec2 filterTextureCoord(void) {
	return aPosition * (uOutputFrame.zw * uInputSize.zw);
}
void main(void) {
	gl_Position = filterVertexPosition();
	vTextureCoord = filterTextureCoord();
}
`;

	const GRAIN_FRAGMENT = `
precision highp float;
in vec2 vTextureCoord;
out vec4 finalColor;
uniform sampler2D uTexture;
uniform vec4 uInputSize;
uniform vec4 uOutputFrame;
uniform float uTime;
uniform float uAmount;
float hash12(vec2 p) {
	vec3 p3 = fract(vec3(p.xyx) * 0.1031);
	p3 += dot(p3, p3.yzx + 33.33);
	return fract((p3.x + p3.y) * p3.z);
}
void main() {
	vec4 color = texture(uTexture, vTextureCoord);
	float frame = floor(uTime * 24.0);
	vec2 cell = floor(vTextureCoord * vec2(1342.0, 892.0));
	float n = hash12(vec2(hash12(cell + 0.13), frame));
	finalColor = vec4(mix(color.rgb, vec3(n), uAmount), color.a);
}
`;

	const grainFilter = Filter.from({
		gl: { vertex: FILTER_VERTEX, fragment: GRAIN_FRAGMENT, name: 'saloon-bg-grain' },
		resources: {
			grainUniforms: {
				uTime: { value: 0, type: 'f32' },
				uAmount: { value: 0.015, type: 'f32' },
			},
		},
	});
	const grainUniforms = (
		grainFilter.resources as Record<string, { uniforms: { uTime: number; uAmount: number } }>
	).grainUniforms.uniforms;

	export const BG_PLATE_FILTERS = [bgGrade, grainFilter];
	export const tickBgGrain = (seconds: number) => {
		grainUniforms.uTime = seconds;
	};
	export const tickBgGrade = (seconds: number, sat: number, warm: number, ember: number) => {
		bgGradeU.uTime = seconds;
		bgGradeU.uSat = sat;
		bgGradeU.uWarm = warm;
		bgGradeU.uEmber = ember;
	};

	const LENS_FOCUS_FRAGMENT = `
precision highp float;
in vec2 vTextureCoord;
out vec4 finalColor;
uniform sampler2D uTexture;
uniform vec4 uInputSize;
uniform float uFocus;
vec4 lensTap(vec2 uv, vec2 o) {
	vec2 ca = o * 0.08;
	return vec4(
		texture(uTexture, uv + o + ca).r,
		texture(uTexture, uv + o).g,
		texture(uTexture, uv + o - ca).b,
		texture(uTexture, uv + o).a
	);
}
void main() {
	vec2 uv = vTextureCoord;
	if (uFocus < 0.004) {
		finalColor = texture(uTexture, uv);
		return;
	}
	// Thin-lens CoC through a 6-blade iris. Disc + longitudinal CA, not a Gaussian.
	float coc = uFocus * uFocus * 12.0;
	vec2 px = uInputSize.zw * coc;
	vec4 acc = texture(uTexture, uv) * 0.28;
	float wsum = 0.28;
	for (int i = 0; i < 6; i++) {
		float a = (float(i) + 0.5) / 6.0 * 6.2831853;
		float hex = 1.0 / max(abs(cos(a)), abs(cos(a - 1.0471976)));
		hex = mix(1.0, hex, 0.28);
		vec2 o = vec2(cos(a), sin(a)) * hex * px;
		acc += lensTap(uv, o) * 0.12;
		wsum += 0.12;
	}
	finalColor = acc / max(wsum, 0.001);
}
`;

	/** tungsten / kerosene — a bit warmer than the raw PNG, retro against the BW plate */
	const LAMP_WARM = 0xffe2b8;
	const LAMP_GLOW_WARM = 0xffb24d;

	const lampFocus = Filter.from({
		gl: { vertex: FILTER_VERTEX, fragment: LENS_FOCUS_FRAGMENT, name: 'saloon-lamp-lens' },
		resources: {
			lensUniforms: {
				uFocus: { value: 0, type: 'f32' },
			},
		},
	});
	lampFocus.padding = 36;
	const lampFocusU = (
		lampFocus.resources as Record<string, { uniforms: { uFocus: number } }>
	).lensUniforms.uniforms;
</script>

<script lang="ts">
	/**
	 * Live western room from TR2-Spine-Background-scene.
	 * Spine paints sky / clouds / town in PSD Z order when loaded.
	 * Flatten plate is fallback only. Hanging lamps always paint.
	 */
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import BarrelLampGlow from './BarrelLampGlow.svelte';
	import HangingLamps from './HangingLamps.svelte';
	import WesternRedFilter from './WesternRedFilter.svelte';
	import WesternSceneFx from './WesternSceneFx.svelte';
	import WesternSceneSpine from './WesternSceneSpine.svelte';
	import { isWesternSceneSkeleton } from '../game/westernScene';

	const context = getContext();

	const fit = $derived.by(() => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const scale = Math.max(canvas.width / SCENE_ART.width, canvas.height / SCENE_ART.height);
		return {
			x: canvas.width / 2,
			y: canvas.height / 2,
			scale: { x: scale, y: scale },
			pivot: { x: SCENE_ART.width / 2, y: SCENE_ART.height / 2 },
		};
	});

	const hasScene = $derived(isWesternSceneSkeleton(context.stateApp.loadedAssets?.westernScene));
	const plateKey = $derived(
		hasScene
			? null
			: context.stateApp.loadedAssets?.westernSceneBg
				? 'westernSceneBg'
				: context.stateApp.loadedAssets?.saloonPlate
					? 'saloonPlate'
					: null,
	);
</script>

<Container x={fit.x} y={fit.y} scale={fit.scale} pivot={fit.pivot} sortableChildren>
	{#if plateKey}
		<Sprite
			key={plateKey}
			x={0}
			y={0}
			width={SCENE_ART.width}
			height={SCENE_ART.height}
			zIndex={0}
		/>
	{/if}
	<WesternRedFilter />
	<WesternSceneFx />
	<WesternSceneSpine />
	<BarrelLampGlow />
	<HangingLamps />
</Container>
