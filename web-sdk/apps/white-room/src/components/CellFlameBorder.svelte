<script lang="ts" module>
	// FLAME BORDER: procedural fire burning around the OUTLINE of the bottom
	// special-symbol slots — one flame around the union silhouette of the three
	// cells (smooth-min of their rounded-rect SDFs), not three separate rings.
	//
	// Port of the Three.js "burning sphere" reference the user supplied. What
	// makes that one read as real fire, reproduced here:
	//   - fbm(p + fbm(p)) value noise with a slow upward scroll;
	//   - the two hard tone thresholds (back = golden body, front-minus-back =
	//     dark ember TIPS where the tongues lick furthest);
	//   - UnrealBloom. Pixi has no bloom pass here, so the bloom is faked in
	//     the same shader: a soft warm halo (smooth falloff, noise-modulated)
	//     rendered under and beyond the hard tongues.
	// The reference's vertical uv gradient becomes a distance-to-outline band:
	// tight on the inside (never covers the symbols), long on the outside so
	// the tongues have room to lick.
	import { Filter, Texture } from 'pixi.js';

	// Pixi v8's stock filter vertex: vTextureCoord * uInputSize.xy /
	// uOutputFrame.zw is exactly the 0..1 position across the filtered quad.
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

	// precision pinned to highp: Pixi compiles its vertex stage highp but would
	// default this fragment to mediump, and the shared uInputSize/uOutputFrame
	// uniforms then fail to link ("precisions differ between VERTEX and
	// FRAGMENT"). Declaring it ourselves keeps both stages in agreement.
	const FRAGMENT = `
precision highp float;
#define NUM_OCTAVES 5

in vec2 vTextureCoord;
out vec4 finalColor;

uniform vec4 uInputSize;
uniform vec4 uOutputFrame;

uniform float uTime;        // seconds
uniform vec2 uQuadSize;     // quad size in board px
uniform vec4 uCell0;        // (cx, cy, halfW, halfH) in quad-local px
uniform vec4 uCell1;
uniform vec4 uCell2;
uniform float uCornerRadius;
uniform float uReachIn;     // band inside the outline, px (keep SMALL)
uniform float uReachOut;    // band outside the outline, px (the flames)
uniform float uNoiseScale;  // px per noise unit (tongue size)
uniform vec3 uBaseColor;    // golden flame body
uniform vec3 uRimColor;     // dark ember tips
uniform float uAlpha;

float rand(vec2 n) {
  return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453);
}

float noise(vec2 p) {
  vec2 ip = floor(p);
  vec2 u = fract(p);
  u = u*u*(3.0-2.0*u);
  float res = mix(
    mix(rand(ip), rand(ip+vec2(1.0,0.0)), u.x),
    mix(rand(ip+vec2(0.0,1.0)), rand(ip+vec2(1.0,1.0)), u.x), u.y);
  return res*res;
}

float fbm(vec2 x) {
  float v = 0.0;
  float a = 0.5;
  vec2 shift = vec2(100.0);
  mat2 rot = mat2(cos(0.5), sin(0.5), -sin(0.5), cos(0.5));
  for (int i = 0; i < NUM_OCTAVES; ++i) {
    v += a * noise(x);
    x = rot * x * 2.0 + shift;
    a *= 0.5;
  }
  return v;
}

// signed distance to one rounded rect (negative inside)
float sdCell(vec2 pos, vec4 cell) {
  vec2 q = abs(pos - cell.xy) - (cell.zw - vec2(uCornerRadius));
  return length(max(q, vec2(0.0))) + min(max(q.x, q.y), 0.0) - uCornerRadius;
}

// polynomial smooth-min: welds the three cells into ONE outline
float smin(float a, float b, float k) {
  float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
  return mix(b, a, h) - k * h * (1.0 - h);
}

void main() {
  vec2 uv = vTextureCoord * uInputSize.xy / uOutputFrame.zw;
  vec2 vPos = (uv - 0.5) * uQuadSize;

  // +time: Pixi y points down, so pushing the sample coords down makes the
  // tongues travel UP, like the reference's -time with y up.
  vec2 p = (vPos + vec2(0.0, uTime * 55.0)) / uNoiseScale;
  float n = fbm(p + fbm(p));

  // ONE silhouette for all three cells
  float sd = sdCell(vPos, uCell0);
  sd = smin(sd, sdCell(vPos, uCell1), 10.0);
  sd = smin(sd, sdCell(vPos, uCell2), 10.0);

  // asymmetric band: barely bleeds inward, licks far outward
  float reach = sd < 0.0 ? uReachIn : uReachOut;
  float edge = 1.0 - clamp(abs(sd) / reach, 0.0, 1.0);

  // the reference's two hard tone thresholds
  float aback  = step(0.99, edge * (1.0 + n));        // golden body
  float afront = step(0.99, edge * 1.08 + n * edge);  // body + tips
  float rim = afront - aback;                          // dark ember tips

  // faked UnrealBloom: soft warm halo under/past the tongues
  float glow = pow(edge, 2.0) * (0.45 + 0.75 * n);

  vec3 hot = vec3(1.0, 0.92, 0.62); // near-white heart right on the outline
  vec3 rgb;
  float a;
  if (afront > 0.5) {
    rgb = rim > 0.5 ? uRimColor : mix(uBaseColor, hot, 0.55 * pow(edge, 3.0));
    a = uAlpha;
  } else {
    rgb = mix(uBaseColor, vec3(1.0, 0.45, 0.08), 0.35);
    a = glow * 0.5 * uAlpha;
  }
  if (a <= 0.015) discard;
  finalColor = vec4(rgb * a, a); // premultiplied
}
`;

	// reference palette: dark ember tips rgb(74,30,0) over golden base
	// rgb(201,158,72) — reads as real fire, do not cool it down.
	const RIM = [74 / 255, 30 / 255, 0];
	const BASE = [201 / 255, 158 / 255, 72 / 255];

	const createFlameFilter = () =>
		Filter.from({
			gl: { vertex: VERTEX, fragment: FRAGMENT, name: 'cell-flame-border-filter' },
			resources: {
				flameUniforms: {
					uTime: { value: 0, type: 'f32' },
					uQuadSize: { value: new Float32Array([1, 1]), type: 'vec2<f32>' },
					uCell0: { value: new Float32Array([0, 0, 1, 1]), type: 'vec4<f32>' },
					uCell1: { value: new Float32Array([0, 0, 1, 1]), type: 'vec4<f32>' },
					uCell2: { value: new Float32Array([0, 0, 1, 1]), type: 'vec4<f32>' },
					uCornerRadius: { value: 7, type: 'f32' }, // = LockedSlots CELL_CLIP_RADIUS
					uReachIn: { value: 9, type: 'f32' },
					uReachOut: { value: 26, type: 'f32' },
					uNoiseScale: { value: 20, type: 'f32' },
					uBaseColor: { value: new Float32Array(BASE), type: 'vec3<f32>' },
					uRimColor: { value: new Float32Array(RIM), type: 'vec3<f32>' },
					uAlpha: { value: 1, type: 'f32' },
				},
			},
		});
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { MainContainer } from 'components-layout';
	import { Container, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { cellFrames } from '../game/chassisArt';

	const context = getContext();

	// quad margin past the cells' bounding box: the outward reach plus a
	// couple px so the tallest lick is never clipped by the filter frame.
	const MARGIN = 30;
	const KEYS = ['bottom:0', 'bottom:1', 'bottom:2'] as const;

	// ONE filter for the whole bottom group (single outline, single quad)
	const filter = createFlameFilter();
	const uniforms = (
		filter.resources as Record<string, { uniforms: Record<string, unknown> }>
	).flameUniforms.uniforms as {
		uTime: number;
		uQuadSize: Float32Array;
		uCell0: Float32Array;
		uCell1: Float32Array;
		uCell2: Float32Array;
	};

	// same measured chassis openings LockedSlots fills, so the fire can never
	// drift off the cells it burns around.
	const frames = $derived(cellFrames(context.stateGameDerived.boardLayout()));
	const box = $derived.by(() => {
		const fs = KEYS.map((k) => frames[k]).filter((f) => f != null);
		if (fs.length !== KEYS.length) return null;
		const minX = Math.min(...fs.map((f) => f.cx - f.w / 2));
		const maxX = Math.max(...fs.map((f) => f.cx + f.w / 2));
		const minY = Math.min(...fs.map((f) => f.cy - f.h / 2));
		const maxY = Math.max(...fs.map((f) => f.cy + f.h / 2));
		return {
			cx: (minX + maxX) / 2,
			cy: (minY + maxY) / 2,
			w: maxX - minX + MARGIN * 2,
			h: maxY - minY + MARGIN * 2,
			cells: fs,
		};
	});

	// keep the silhouette uniforms in step with the measured frames; mutate the
	// arrays in place, the uniform group re-uploads every render.
	$effect(() => {
		if (!box) return;
		uniforms.uQuadSize[0] = box.w;
		uniforms.uQuadSize[1] = box.h;
		const targets = [uniforms.uCell0, uniforms.uCell1, uniforms.uCell2];
		box.cells.forEach((f, i) => {
			targets[i][0] = f.cx - box.cx;
			targets[i][1] = f.cy - box.cy;
			targets[i][2] = f.w / 2;
			targets[i][3] = f.h / 2;
		});
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			uniforms.uTime = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<!-- Permanently mounted MainContainer (layering skill); the quad inside only
	needs the frames measured. Texture.WHITE stretched over the group + margin;
	the filter paints the flame band and discards the rest. -->
<MainContainer>
	{#if box}
		<Container x={box.cx} y={box.cy} filters={[filter]}>
			<BaseSprite texture={Texture.WHITE} anchor={0.5} width={box.w} height={box.h} />
		</Container>
	{/if}
</MainContainer>
