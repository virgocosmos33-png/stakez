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
	coc = mix(0.0637, 0.7004, coc);
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
				uRadius: { value: 4.08, type: 'f32' },
			},
		},
	});
	fieldBlurFilter.padding = 12;

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

	export const BG_PLATE_FILTERS = [bgGrade, fieldBlurFilter, grainFilter];
	export const tickBgGrain = (seconds: number) => {
		grainUniforms.uTime = seconds;
	};
	export const tickBgGrade = (seconds: number, sat: number, warm: number, ember: number) => {
		bgGradeU.uTime = seconds;
		bgGradeU.uSat = sat;
		bgGradeU.uWarm = warm;
		bgGradeU.uEmber = ember;
	};

	/** tungsten / kerosene — a bit warmer than the raw PNG, retro against the BW plate */
	const LAMP_WARM = 0xffe2b8;
	const LAMP_GLOW_WARM = 0xffb24d;
</script>

<script lang="ts">
	/**
	 * Live saloon room: plate + the LEFT hanging lamp. A click swaps the lit
	 * lantern for the unlit PNG until the next spin.
	 */
	import { onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';

	import { SALOON_LAMPS } from '../game/saloonLamps';
	import { saloonLamp } from '../game/saloonLamp.svelte';
	import { LAMP_GLOBE } from '../game/saloonLampSmash';
	import { getContext } from '../game/context';
	import SuperFire from './SuperFire.svelte';

	const context = getContext();

	const IDLE_PERIOD_MS = 4000;
	const IDLE_AMP_L = (4.4 * Math.PI) / 180;

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
	const showLamp = $derived(context.stateGame.atmosphere === 'base');
	const showFire = $derived(context.stateGame.atmosphere === 'super');

	let swayOrigin = $state(performance.now());
	let rotL = $state(0);
	/** Shot: light is already out, but the globe still rides the sway until
	 *  the next pass through hanging-straight, then it parks. */
	let settling = $state(false);
	let prevRot = 0;

	$effect(() => {
		if (!context.stateXstateDerived.isIdle() && saloonLamp.smashed) {
			saloonLamp.smashed = false;
			settling = false;
		}
	});

	$effect(() => {
		if (saloonLamp.smashed) settling = true;
		else settling = false;
	});

	onMount(() => {
		let raf = 0;
		const tick = (now: number) => {
			if (context.stateGame.atmosphere !== 'base') {
				if (rotL !== 0) rotL = 0;
				raf = requestAnimationFrame(tick);
				return;
			}
			const phase = ((now - swayOrigin) / IDLE_PERIOD_MS) * Math.PI * 2;
			const idle = Math.sin(phase) * IDLE_AMP_L;
			if (!saloonLamp.smashed) {
				if (Math.abs(idle - rotL) > 0.0004) rotL = idle;
				prevRot = idle;
			} else if (settling) {
				const crossed = prevRot !== 0 && idle * prevRot <= 0;
				if (crossed || Math.abs(idle) < 0.0015) {
					if (rotL !== 0) rotL = 0;
					prevRot = 0;
					settling = false;
				} else {
					if (Math.abs(idle - rotL) > 0.0004) rotL = idle;
					prevRot = idle;
				}
			} else if (rotL !== 0) {
				rotL = 0;
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
				key={plateKey}
				x={SCENE_ART.width / 2}
				y={SCENE_ART.height / 2}
				width={SCENE_ART.width}
				height={SCENE_ART.height}
				anchor={0.5}
			/>
		</Container>
		{#if showLamp}
			<Container x={L.x} y={L.y} rotation={rotL}>
				<Sprite
					key="saloonLampGlow"
					x={FLAME.x}
					y={FLAME.y + 80}
					anchor={0.5}
					width={980}
					height={1100}
					alpha={saloonLamp.smashed ? 0 : 0.4}
					tint={LAMP_GLOW_WARM}
					blendMode="add"
					eventMode="none"
				/>
				<Sprite
					key="saloonLampL"
					x={-L.anchorX * L.width}
					y={-L.anchorY * L.height}
					width={L.width}
					height={L.height}
					anchor={0}
					alpha={saloonLamp.smashed ? 0 : 1}
					tint={LAMP_WARM}
				/>
				<Sprite
					key="saloonLampLSmashed"
					x={-L.anchorX * L.width}
					y={-L.anchorY * L.height}
					width={L.width}
					height={L.height}
					anchor={0}
					alpha={saloonLamp.smashed ? 1 : 0}
				/>
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
