<script lang="ts" module>
	import { BlurFilter, Filter } from 'pixi.js';

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

	const FIELD_BLUR_FRAGMENT = `
precision highp float;
in vec2 vTextureCoord;
out vec4 finalColor;
uniform sampler2D uTexture;
uniform vec4 uInputSize;
uniform vec4 uOutputFrame;
uniform float uRadius;
void main() {
	vec2 uv = vTextureCoord;
	vec2 focus = vec2(0.50, 0.52);
	float coc = smoothstep(0.28, 0.92, length((uv - focus) * vec2(1.05, 1.2)));
	coc = max(coc, smoothstep(0.16, 0.0, uv.y) * 0.35);
	coc = mix(0.045, 0.48, coc);
	vec2 px = uInputSize.zw * uRadius * coc;
	vec4 acc = texture(uTexture, uv) * 0.36;
	acc += texture(uTexture, uv + vec2(1.0, 0.0) * px) * 0.16;
	acc += texture(uTexture, uv + vec2(-1.0, 0.0) * px) * 0.16;
	acc += texture(uTexture, uv + vec2(0.0, 1.0) * px) * 0.16;
	acc += texture(uTexture, uv + vec2(0.0, -1.0) * px) * 0.16;
	finalColor = acc;
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
	vec2 cell = floor(vTextureCoord * vec2(1679.0, 937.0));
	float n = hash12(vec2(hash12(cell + 0.13), frame));
	finalColor = vec4(mix(color.rgb, vec3(n), uAmount), color.a);
}
`;

	const fieldBlurFilter = Filter.from({
		gl: { vertex: FILTER_VERTEX, fragment: FIELD_BLUR_FRAGMENT, name: 'saloon-bg-field-blur' },
		resources: {
			fieldUniforms: {
				uRadius: { value: 2.7, type: 'f32' },
			},
		},
	});
	fieldBlurFilter.padding = 10;

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

	// Same plate stack as before — Gaussian + field blur — just dialed down.
	const bgSeeBlur = new BlurFilter({ strength: 2.5, quality: 3 });
	bgSeeBlur.padding = 16;

	export const BG_PLATE_FILTERS = [bgGrade, fieldBlurFilter, grainFilter, bgSeeBlur];
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
	 * Live saloon room: plate + the LEFT hanging lamp. A click kills the
	 * light and kicks a damped spherical pendulum; the mesh recedes and
	 * the globe goes soft as it comes toward the lens.
	 */
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicInOut } from 'svelte/easing';
	import { Container, Sprite } from 'pixi-svelte';

	import { SALOON_LAMPS } from '../game/saloonLamps';
	import { flushLamp, resetLamp, saloonLamp, stepLamp } from '../game/saloonLamp.svelte';
	import { LAMP_GLOBE } from '../game/saloonLampSmash';
	import { STEP_DT, STEP_MAX } from '../game/saloonLampPhysics';
	import { getContext } from '../game/context';
	import SuperFire from './SuperFire.svelte';
	import SaloonLampMesh from './SaloonLampMesh.svelte';

	const context = getContext();

	const L = SALOON_LAMPS.L;
	const FLAME = { x: LAMP_GLOBE.x, y: LAMP_GLOBE.y };

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

	const hasRoom = $derived(
		Boolean(context.stateApp.loadedAssets?.['saloonPlate']) &&
			Boolean(context.stateApp.loadedAssets?.['saloonLampL']),
	);
	const plateKey = $derived(
		context.stateGame.atmosphere === 'super'
			? 'saloonPlateSuper'
			: context.stateGame.atmosphere === 'small'
				? 'saloonPlateSmall'
				: 'saloonPlate',
	);

	// CROSSFADE the room plate instead of hard-cutting it. The atmosphere only
	// flips behind the bonus banner's dark veil now, but the veil is not fully
	// opaque — a hard cut still reads as a blink through it. The old plate
	// stays underneath while the new one fades in over it.
	let shownPlate = $state(
		context.stateGame.atmosphere === 'super'
			? 'saloonPlateSuper'
			: context.stateGame.atmosphere === 'small'
				? 'saloonPlateSmall'
				: 'saloonPlate',
	);
	let fadingPlate = $state<string | null>(null);
	const plateFade = new Tween(1);

	$effect(() => {
		const next = plateKey;
		if (next === shownPlate || next === fadingPlate) return;
		fadingPlate = next;
		plateFade.set(0, { duration: 0 });
		plateFade.set(1, { duration: 700, easing: cubicInOut }).then(() => {
			// A second flip mid-fade supersedes this one — only commit our own.
			if (fadingPlate !== next) return;
			shownPlate = next;
			fadingPlate = null;
		});
	});
	const showLamp = $derived(context.stateGame.atmosphere === 'base');
	const showFire = $derived(context.stateGame.atmosphere === 'super');

	const punchAmt = $derived(saloonLamp.punch);
	const lampScale = $derived(Math.min(1.1, Math.max(0.88, 1 - punchAmt * 0.04)));
	const nearLens = $derived(Math.max(0, -punchAmt));
	const lampFilters = [lampFocus];

	$effect(() => {
		lampFocusU.uFocus = nearLens;
		lampFocus.padding = 8 + Math.ceil(nearLens * nearLens * 36);
	});

	$effect(() => {
		if (!context.stateXstateDerived.isIdle() || context.stateGame.atmosphere !== 'base') {
			resetLamp();
		}
	});

	onMount(() => {
		let raf = 0;
		let last = performance.now();
		let acc = 0;
		const tick = (now: number) => {
			let dt = (now - last) / 1000;
			last = now;
			if (dt > 0.05) dt = 0.05;
			if (context.stateGame.atmosphere === 'base') {
				acc += dt;
				let steps = 0;
				while (acc >= STEP_DT && steps < STEP_MAX) {
					stepLamp(STEP_DT);
					acc -= STEP_DT;
					steps += 1;
				}
				if (steps === STEP_MAX) acc = 0;
				if (steps > 0) flushLamp();
			} else if (acc !== 0) {
				acc = 0;
			}
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

</script>

<Container x={fit.x} y={fit.y} scale={fit.scale} pivot={fit.pivot}>
	{#if hasRoom}
		<Container filters={BG_PLATE_FILTERS}>
			<Sprite
				key={shownPlate}
				x={SCENE_ART.width / 2}
				y={SCENE_ART.height / 2}
				width={SCENE_ART.width}
				height={SCENE_ART.height}
				anchor={0.5}
			/>
			{#if fadingPlate !== null}
				<Sprite
					key={fadingPlate}
					x={SCENE_ART.width / 2}
					y={SCENE_ART.height / 2}
					width={SCENE_ART.width}
					height={SCENE_ART.height}
					anchor={0.5}
					alpha={plateFade.current}
				/>
			{/if}
		</Container>
		{#if showLamp}
			<Container
				x={L.x + punchAmt * 14}
				y={L.y + punchAmt * 5}
				rotation={saloonLamp.theta}
				scale={{ x: lampScale, y: lampScale * (1 - punchAmt * 0.02) }}
				filters={lampFilters}
			>
				<Sprite
					key="saloonLampGlow"
					x={FLAME.x}
					y={FLAME.y + 80}
					anchor={0.5}
					width={980}
					height={1100}
					alpha={saloonLamp.lit ? 0.4 * (1 - Math.max(0, punchAmt) * 0.18) : 0}
					tint={LAMP_GLOW_WARM}
					blendMode="add"
					eventMode="none"
				/>
				<SaloonLampMesh punch={punchAmt} lit={saloonLamp.lit} tint={LAMP_WARM} />
			</Container>
		{/if}
		{#if showFire}
			<SuperFire />
		{/if}
	{:else}
		<Container filters={BG_PLATE_FILTERS}>
			<Sprite
				key="sceneBg"
				x={SCENE_ART.width / 2}
				y={SCENE_ART.height / 2}
				width={SCENE_ART.width}
				height={SCENE_ART.height}
				anchor={0.5}
			/>
		</Container>
	{/if}
</Container>
