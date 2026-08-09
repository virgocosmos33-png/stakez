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
uniform vec3 uBaseColor;    // flame body (Amaterasu: black)
uniform vec3 uRimColor;     // tongue tips (Amaterasu: white)
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
  vec2 p = (vPos + vec2(0.0, uTime * 70.0)) / uNoiseScale;
  // boosted a touch past the reference: the peaks are what tear off the
  // detached flame pieces, and the hard threshold eats anything timid
  float n = fbm(p + fbm(p)) * 1.25;

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

  vec3 hot = vec3(0.22, 0.22, 0.26); // faint grey heart so the black keeps depth
  vec3 rgb;
  float a;
  if (afront > 0.5) {
    rgb = rim > 0.5 ? uRimColor : mix(uBaseColor, hot, 0.55 * pow(edge, 3.0));
    a = uAlpha;
  } else {
    rgb = mix(uBaseColor, vec3(0.82, 0.86, 0.95), 0.75);
    a = glow * 0.5 * uAlpha;
  }
  if (a <= 0.015) discard;
  finalColor = vec4(rgb * a, a); // premultiplied
}
`;

	// AMATERASU palette: jet-black flame body silhouetted by WHITE tips and a
	// pale cold glow — the black tongues only read against that white fringe.
	const RIM = [0.96, 0.98, 1.0]; // white tips
	const BASE = [0.02, 0.02, 0.03]; // black fire body

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
					uReachIn: { value: 10, type: 'f32' },
					// LONG outward reach: tongues this deep let whole noise blobs
					// pass the threshold in isolation = flame pieces splitting off
					// the main fire, like the reference sphere.
					uReachOut: { value: 48, type: 'f32' },
					uNoiseScale: { value: 30, type: 'f32' },
					uBaseColor: { value: new Float32Array(BASE), type: 'vec3<f32>' },
					uRimColor: { value: new Float32Array(RIM), type: 'vec3<f32>' },
					uAlpha: { value: 1, type: 'f32' },
				},
			},
		});
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, BaseSprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { cellFrames } from '../game/chassisArt';
	import { unlockedCellKeys } from '../game/cellUnlock';

	const context = getContext();

	// quad margin past the cells' bounding box: the outward reach plus a
	// couple px so the tallest lick is never clipped by the filter frame.
	const MARGIN = 52;
	const REACH_OUT = 48;

	// The fire burns ONLY around an OPEN cell group: nothing in the base game;
	// the bonus ignites each group as its level unlocks it (L1 bottom, L2
	// +right, L3 +left) and every flame dies with the bonus. Each group gets
	// its own outline (one quad + one filter) and its own ignite ramp, so a
	// group unlocking mid-bonus catches fire on its own.
	const GROUPS = [
		{ name: 'bottom', keys: ['bottom:0', 'bottom:1', 'bottom:2'] },
		{ name: 'right', keys: ['right:0', 'right:1', 'right:2'] },
		{ name: 'left', keys: ['left:0', 'left:1', 'left:2'] },
	] as const;

	type FlameUniforms = {
		uTime: number;
		uAlpha: number;
		uReachOut: number;
		uQuadSize: Float32Array;
		uCell0: Float32Array;
		uCell1: Float32Array;
		uCell2: Float32Array;
	};
	const entries = GROUPS.map((g) => {
		const filter = createFlameFilter();
		return {
			...g,
			filter,
			uniforms: (filter.resources as Record<string, { uniforms: FlameUniforms }>)
				.flameUniforms.uniforms,
			// 0 = cold, 1 = fully burning
			ignite: new Tween(0),
		};
	});

	// same measured chassis openings LockedSlots fills, so the fire can never
	// drift off the cells it burns around. The fire keys off the SAME per-cell
	// open set the bars use (unlockedCellKeys), not just the bonus group
	// unlocks: a feature buy (N+ SPECIALS / ALL SPECIALS) fires side + bottom
	// cells on a BASE spin with no group unlocked, and those must burn too.
	// Only the OPEN cells of a group join its welded outline.
	const frames = $derived(cellFrames(context.stateGameDerived.boardLayout()));
	const openKeys = $derived(unlockedCellKeys(context.stateGame));
	const boxes = $derived(
		entries.map((entry) => {
			const fs = entry.keys
				.filter((k) => openKeys.has(k))
				.map((k) => frames[k])
				.filter((f) => f != null);
			if (fs.length === 0) return { entry, box: null };
			const minX = Math.min(...fs.map((f) => f.cx - f.w / 2));
			const maxX = Math.max(...fs.map((f) => f.cx + f.w / 2));
			const minY = Math.min(...fs.map((f) => f.cy - f.h / 2));
			const maxY = Math.max(...fs.map((f) => f.cy + f.h / 2));
			return {
				entry,
				box: {
					cx: (minX + maxX) / 2,
					cy: (minY + maxY) / 2,
					w: maxX - minX + MARGIN * 2,
					h: maxY - minY + MARGIN * 2,
					cells: fs,
				},
			};
		}),
	);

	// ignite while the group has any open cell, die out when they all close.
	// The ~1s ramp starts right as the cells open — after the scatters land,
	// the bars retract and the player clicks into the bonus, the fire is what
	// greets them on the first bonus board.
	$effect(() => {
		for (const { entry, box } of boxes) {
			const burning = box != null;
			if (burning && entry.ignite.target !== 1) {
				entry.ignite.set(1, { duration: 1100, easing: cubicOut });
			} else if (!burning && entry.ignite.target !== 0) {
				entry.ignite.set(0, { duration: 450 });
			}
		}
	});

	// keep the silhouette + ignite uniforms in step; mutate the arrays in
	// place, the uniform group re-uploads every render.
	$effect(() => {
		for (const { entry, box } of boxes) {
			if (!box) continue;
			const u = entry.uniforms;
			const ig = entry.ignite.current;
			u.uAlpha = ig;
			// the fire GROWS out of the outline as it ignites
			u.uReachOut = 12 + (REACH_OUT - 12) * ig;
			u.uQuadSize[0] = box.w;
			u.uQuadSize[1] = box.h;
			const targets = [u.uCell0, u.uCell1, u.uCell2];
			box.cells.forEach((f, i) => {
				targets[i][0] = f.cx - box.cx;
				targets[i][1] = f.cy - box.cy;
				targets[i][2] = f.w / 2;
				targets[i][3] = f.h / 2;
			});
			// fewer than 3 open cells: park the unused SDF slots far away so
			// they contribute nothing to the welded outline
			for (let i = box.cells.length; i < targets.length; i++) {
				targets[i][0] = 1e6;
				targets[i][1] = 1e6;
				targets[i][2] = 1;
				targets[i][3] = 1;
			}
		}
	});

	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			const t = (now - start) / 1000;
			for (const entry of entries) entry.uniforms.uTime = t;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
</script>

<!-- Permanently mounted MainContainer (layering skill). One Texture.WHITE quad
	per OPEN group, stretched over the group + margin; the filter paints the
	flame band and discards the rest. Cold groups render nothing at all.
	zIndex keeps the fire ABOVE every default-0 stage sibling: overlays that
	mount mid-feature (StretchFx / StretchWays racked reels, the WinDim dark
	overlay...) are APPENDED to the stage and used to bury the flames — the
	white tips must always stay readable. 9 sits just under CellLightning (10)
	and far under the mega-win strobe (120). -->
<Container zIndex={9}>
	<MainContainer>
		{#each boxes as { entry, box } (entry.name)}
			{#if box && entry.ignite.current > 0.01}
				<Container x={box.cx} y={box.cy} filters={[entry.filter]}>
					<BaseSprite texture={Texture.WHITE} anchor={0.5} width={box.w} height={box.h} />
				</Container>
			{/if}
		{/each}
	</MainContainer>
</Container>
