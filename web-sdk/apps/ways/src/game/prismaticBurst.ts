/** WebGL2 prismatic burst from https://reactbits.dev (PrismaticBurst). */

export type PrismaticBurstOptions = {
	intensity?: number;
	speed?: number;
	animationType?: 'rotate' | 'rotate3d' | 'hover';
	colors?: string[];
	distort?: number;
	rayCount?: number;
};

const VERTEX_SHADER = `#version 300 es
in vec2 position;
void main() {
	gl_Position = vec4(position, 0.0, 1.0);
}
`;

const FRAGMENT_SHADER = `#version 300 es
precision highp float;
precision highp int;
out vec4 fragColor;
uniform vec2 uResolution;
uniform float uTime;
uniform float uIntensity;
uniform float uSpeed;
uniform int uAnimType;
uniform vec2 uMouse;
uniform int uColorCount;
uniform float uDistort;
uniform vec2 uOffset;
uniform sampler2D uGradient;
uniform float uNoiseAmount;
uniform int uRayCount;

float hash21(vec2 p){
	p = floor(p);
	float f = 52.9829189 * fract(dot(p, vec2(0.065, 0.005)));
	return fract(f);
}
mat2 rot30(){ return mat2(0.8, -0.5, 0.5, 0.8); }
float layeredNoise(vec2 fragPx){
	vec2 p = mod(fragPx + vec2(uTime * 30.0, -uTime * 21.0), 1024.0);
	vec2 q = rot30() * p;
	float n = 0.0;
	n += 0.40 * hash21(q);
	n += 0.25 * hash21(q * 2.0 + 17.0);
	n += 0.20 * hash21(q * 4.0 + 47.0);
	n += 0.10 * hash21(q * 8.0 + 113.0);
	n += 0.05 * hash21(q * 16.0 + 191.0);
	return n;
}
vec3 rayDir(vec2 frag, vec2 res, vec2 offset, float dist){
	float focal = res.y * max(dist, 1e-3);
	return normalize(vec3(2.0 * (frag - offset) - res, focal));
}
float edgeFade(vec2 frag, vec2 res, vec2 offset){
	vec2 toC = frag - 0.5 * res - offset;
	float r = length(toC) / (0.5 * min(res.x, res.y));
	float x = clamp(r, 0.0, 1.0);
	float q = x * x * x * (x * (x * 6.0 - 15.0) + 10.0);
	float s = q * 0.5;
	s = pow(s, 1.5);
	float tail = 1.0 - pow(1.0 - s, 2.0);
	s = mix(s, tail, 0.2);
	float dn = (layeredNoise(frag * 0.15) - 0.5) * 0.0015 * s;
	return clamp(s + dn, 0.0, 1.0);
}
mat3 rotX(float a){ float c = cos(a), s = sin(a); return mat3(1.0,0.0,0.0, 0.0,c,-s, 0.0,s,c); }
mat3 rotY(float a){ float c = cos(a), s = sin(a); return mat3(c,0.0,s, 0.0,1.0,0.0, -s,0.0,c); }
mat3 rotZ(float a){ float c = cos(a), s = sin(a); return mat3(c,-s,0.0, s,c,0.0, 0.0,0.0,1.0); }
vec3 sampleGradient(float t){
	t = clamp(t, 0.0, 1.0);
	return texture(uGradient, vec2(t, 0.5)).rgb;
}
vec2 rot2(vec2 v, float a){
	float s = sin(a), c = cos(a);
	return mat2(c, -s, s, c) * v;
}
float bendAngle(vec3 q, float t){
	float a = 0.8 * sin(q.x * 0.55 + t * 0.6)
		+ 0.7 * sin(q.y * 0.50 - t * 0.5)
		+ 0.6 * sin(q.z * 0.60 + t * 0.7);
	return a;
}
void main(){
	vec2 frag = gl_FragCoord.xy;
	float t = uTime * uSpeed;
	float jitterAmp = 0.1 * clamp(uNoiseAmount, 0.0, 1.0);
	vec3 dir = rayDir(frag, uResolution, uOffset, 1.0);
	float marchT = 0.0;
	vec3 col = vec3(0.0);
	float n = layeredNoise(frag);
	vec4 c = cos(t * 0.2 + vec4(0.0, 33.0, 11.0, 0.0));
	mat2 M2 = mat2(c.x, c.y, c.z, c.w);
	float amp = clamp(uDistort, 0.0, 50.0) * 0.15;
	mat3 rot3dMat = mat3(1.0);
	if(uAnimType == 1){
		vec3 ang = vec3(t * 0.31, t * 0.21, t * 0.17);
		rot3dMat = rotZ(ang.z) * rotY(ang.y) * rotX(ang.x);
	}
	mat3 hoverMat = mat3(1.0);
	if(uAnimType == 2){
		vec2 m = uMouse * 2.0 - 1.0;
		vec3 ang = vec3(m.y * 0.6, m.x * 0.6, 0.0);
		hoverMat = rotY(ang.y) * rotX(ang.x);
	}
	for (int i = 0; i < 44; ++i) {
		vec3 P = marchT * dir;
		P.z -= 2.0;
		float rad = length(P);
		vec3 Pl = P * (10.0 / max(rad, 1e-6));
		if(uAnimType == 0){ Pl.xz *= M2; }
		else if(uAnimType == 1){ Pl = rot3dMat * Pl; }
		else { Pl = hoverMat * Pl; }
		float stepLen = min(rad - 0.3, n * jitterAmp) + 0.1;
		float grow = smoothstep(0.35, 3.0, marchT);
		float a1 = amp * grow * bendAngle(Pl * 0.6, t);
		float a2 = 0.5 * amp * grow * bendAngle(Pl.zyx * 0.5 + 3.1, t * 0.9);
		vec3 Pb = Pl;
		Pb.xz = rot2(Pb.xz, a1);
		Pb.xy = rot2(Pb.xy, a2);
		float rayPattern = smoothstep(0.5, 0.7,
			sin(Pb.x + cos(Pb.y) * cos(Pb.z)) * sin(Pb.z + sin(Pb.y) * cos(Pb.x + t)));
		if (uRayCount > 0) {
			float ang = atan(Pb.y, Pb.x);
			float comb = 0.5 + 0.5 * cos(float(uRayCount) * ang);
			comb = pow(comb, 3.0);
			rayPattern *= smoothstep(0.15, 0.95, comb);
		}
		vec3 spectralDefault = 1.0 + vec3(
			cos(marchT * 3.0 + 0.0), cos(marchT * 3.0 + 1.0), cos(marchT * 3.0 + 2.0));
		float saw = fract(marchT * 0.25);
		float tRay = saw * saw * (3.0 - 2.0 * saw);
		vec3 userGradient = 2.0 * sampleGradient(tRay);
		vec3 spectral = (uColorCount > 0) ? userGradient : spectralDefault;
		vec3 base = (0.05 / (0.4 + stepLen)) * smoothstep(5.0, 0.0, rad) * spectral;
		col += base * rayPattern;
		marchT += stepLen;
	}
	col *= edgeFade(frag, uResolution, uOffset);
	col *= uIntensity;
	fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}`;

const hexToRgb = (hex: string): [number, number, number] => {
	let h = hex.trim().replace('#', '');
	if (h.length === 3) h = h.split('').map((c) => c + c).join('');
	const n = parseInt(h.slice(0, 6), 16);
	return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};

const compileShader = (gl: WebGL2RenderingContext, source: string, type: number) => {
	const shader = gl.createShader(type);
	if (!shader) return null;
	gl.shaderSource(shader, source);
	gl.compileShader(shader);
	if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
		console.error('PrismaticBurst shader error:', gl.getShaderInfoLog(shader));
		gl.deleteShader(shader);
		return null;
	}
	return shader;
};

const ANIM_MAP = { rotate: 0, rotate3d: 1, hover: 2 } as const;

type GlState = {
	gl: WebGL2RenderingContext;
	program: WebGLProgram;
	vertexShader: WebGLShader;
	fragmentShader: WebGLShader;
	vertexBuffer: WebGLBuffer;
	gradientTex: WebGLTexture;
	aPosition: number;
	uResolution: WebGLUniformLocation | null;
	uTime: WebGLUniformLocation | null;
	uIntensity: WebGLUniformLocation | null;
	uSpeed: WebGLUniformLocation | null;
	uAnimType: WebGLUniformLocation | null;
	uMouse: WebGLUniformLocation | null;
	uColorCount: WebGLUniformLocation | null;
	uDistort: WebGLUniformLocation | null;
	uOffset: WebGLUniformLocation | null;
	uGradient: WebGLUniformLocation | null;
	uNoiseAmount: WebGLUniformLocation | null;
	uRayCount: WebGLUniformLocation | null;
};

/** displayCanvas = 2D canvas Pixi reads; WebGL renders to an internal offscreen canvas. */
export const createPrismaticBurst = (
	displayCanvas: HTMLCanvasElement,
	options: PrismaticBurstOptions = {},
) => {
	const glCanvas = document.createElement('canvas');
	const blitCtx = displayCanvas.getContext('2d', { alpha: true });
	if (!blitCtx) throw new Error('2D context required for PrismaticBurst display');

	const colors = options.colors ?? ['#A855F7', '#7C3AED', '#6366F1'];
	const intensity = options.intensity ?? 2;
	const speed = options.speed ?? 0.5;
	const animType = ANIM_MAP[options.animationType ?? 'rotate3d'];
	const distort = options.distort ?? 0;
	const rayCount = options.rayCount ?? 0;

	let state: GlState | null = null;

	const bindDrawState = (glState: GlState) => {
		const { gl, program, vertexBuffer, gradientTex, aPosition, uGradient } = glState;
		gl.useProgram(program);
		gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
		gl.enableVertexAttribArray(aPosition);
		gl.vertexAttribPointer(aPosition, 2, gl.FLOAT, false, 0, 0);
		gl.activeTexture(gl.TEXTURE0);
		gl.bindTexture(gl.TEXTURE_2D, gradientTex);
		gl.uniform1i(uGradient, 0);
		gl.uniform1f(glState.uNoiseAmount, 0.8);
		gl.uniform2f(glState.uMouse, 0.5, 0.5);
	};

	const initGl = () => {
		if (state) {
			const { gl, program, vertexShader, fragmentShader, vertexBuffer, gradientTex } = state;
			gl.deleteTexture(gradientTex);
			gl.deleteProgram(program);
			gl.deleteShader(vertexShader);
			gl.deleteShader(fragmentShader);
			gl.deleteBuffer(vertexBuffer);
		}

		const gl = glCanvas.getContext('webgl2', {
			alpha: true,
			premultipliedAlpha: false,
			preserveDrawingBuffer: true,
		});
		if (!gl) throw new Error('WebGL2 not supported for PrismaticBurst');

		const vertexShader = compileShader(gl, VERTEX_SHADER, gl.VERTEX_SHADER);
		const fragmentShader = compileShader(gl, FRAGMENT_SHADER, gl.FRAGMENT_SHADER);
		if (!vertexShader || !fragmentShader) throw new Error('PrismaticBurst shader init failed');

		const program = gl.createProgram();
		if (!program) throw new Error('PrismaticBurst program init failed');
		gl.attachShader(program, vertexShader);
		gl.attachShader(program, fragmentShader);
		gl.linkProgram(program);
		if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
			throw new Error(`PrismaticBurst link error: ${gl.getProgramInfoLog(program)}`);
		}

		const vertices = new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]);
		const vertexBuffer = gl.createBuffer()!;
		gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
		gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
		const aPosition = gl.getAttribLocation(program, 'position');

		const gradientTex = gl.createTexture()!;
		gl.activeTexture(gl.TEXTURE0);
		gl.bindTexture(gl.TEXTURE_2D, gradientTex);
		gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
		gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
		gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
		gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

		const colorData = new Uint8Array(colors.length * 4);
		colors.forEach((hex, i) => {
			const [r, g, b] = hexToRgb(hex);
			colorData[i * 4] = r;
			colorData[i * 4 + 1] = g;
			colorData[i * 4 + 2] = b;
			colorData[i * 4 + 3] = 255;
		});
		gl.texImage2D(
			gl.TEXTURE_2D,
			0,
			gl.RGBA,
			colors.length,
			1,
			0,
			gl.RGBA,
			gl.UNSIGNED_BYTE,
			colorData,
		);

		state = {
			gl,
			program,
			vertexShader,
			fragmentShader,
			vertexBuffer,
			gradientTex,
			aPosition,
			uResolution: gl.getUniformLocation(program, 'uResolution'),
			uTime: gl.getUniformLocation(program, 'uTime'),
			uIntensity: gl.getUniformLocation(program, 'uIntensity'),
			uSpeed: gl.getUniformLocation(program, 'uSpeed'),
			uAnimType: gl.getUniformLocation(program, 'uAnimType'),
			uMouse: gl.getUniformLocation(program, 'uMouse'),
			uColorCount: gl.getUniformLocation(program, 'uColorCount'),
			uDistort: gl.getUniformLocation(program, 'uDistort'),
			uOffset: gl.getUniformLocation(program, 'uOffset'),
			uGradient: gl.getUniformLocation(program, 'uGradient'),
			uNoiseAmount: gl.getUniformLocation(program, 'uNoiseAmount'),
			uRayCount: gl.getUniformLocation(program, 'uRayCount'),
		};

		bindDrawState(state);
		gl.viewport(0, 0, glCanvas.width, glCanvas.height);
	};

	initGl();

	return {
		resize(width: number, height: number) {
			const w = Math.max(1, Math.round(width));
			const h = Math.max(1, Math.round(height));
			if (glCanvas.width !== w || glCanvas.height !== h) {
				glCanvas.width = w;
				glCanvas.height = h;
				displayCanvas.width = w;
				displayCanvas.height = h;
				// changing canvas dimensions resets WebGL state — rebuild the pipeline
				initGl();
			}
			state!.gl.viewport(0, 0, w, h);
		},
		render(timeSec: number, burstIntensity = 1) {
			if (!state) return;
			const { gl, uResolution, uTime, uIntensity, uSpeed, uAnimType, uColorCount, uDistort, uOffset, uRayCount } =
				state;

			bindDrawState(state);
			gl.clearColor(0, 0, 0, 0);
			gl.clear(gl.COLOR_BUFFER_BIT);
			gl.uniform2f(uResolution, glCanvas.width, glCanvas.height);
			gl.uniform1f(uTime, timeSec);
			gl.uniform1f(uIntensity, intensity * burstIntensity);
			gl.uniform1f(uSpeed, speed);
			gl.uniform1i(uAnimType, animType);
			gl.uniform1i(uColorCount, colors.length);
			gl.uniform1f(uDistort, distort);
			gl.uniform2f(uOffset, 0, 0);
			gl.uniform1i(uRayCount, rayCount);
			gl.drawArrays(gl.TRIANGLES, 0, 6);
			gl.finish();

			blitCtx.clearRect(0, 0, displayCanvas.width, displayCanvas.height);
			blitCtx.drawImage(glCanvas, 0, 0);
		},
		destroy() {
			if (!state) return;
			const { gl, program, vertexShader, fragmentShader, vertexBuffer, gradientTex } = state;
			gl.deleteTexture(gradientTex);
			gl.deleteProgram(program);
			gl.deleteShader(vertexShader);
			gl.deleteShader(fragmentShader);
			gl.deleteBuffer(vertexBuffer);
			state = null;
		},
	};
};
