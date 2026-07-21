/** WebGL lightning from https://reactbits.dev/backgrounds/lightning (React Bits). */

export type ReactBitsLightningUniforms = {
	hue: number;
	xOffset: number;
	speed: number;
	intensity: number;
	size: number;
};

const VERTEX_SHADER = `
attribute vec2 aPosition;
void main() {
	gl_Position = vec4(aPosition, 0.0, 1.0);
}
`;

const FRAGMENT_SHADER = `
precision mediump float;
uniform vec2 iResolution;
uniform float iTime;
uniform float uHue;
uniform float uXOffset;
uniform float uSpeed;
uniform float uIntensity;
uniform float uSize;

#define OCTAVE_COUNT 10

vec3 hsv2rgb(vec3 c) {
	vec3 rgb = clamp(abs(mod(c.x * 6.0 + vec3(0.0,4.0,2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0);
	return c.z * mix(vec3(1.0), rgb, c.y);
}

float hash11(float p) {
	p = fract(p * .1031);
	p *= p + 33.33;
	p *= p + p;
	return fract(p);
}

float hash12(vec2 p) {
	vec3 p3 = fract(vec3(p.xyx) * .1031);
	p3 += dot(p3, p3.yzx + 33.33);
	return fract((p3.x + p3.y) * p3.z);
}

mat2 rotate2d(float theta) {
	float c = cos(theta);
	float s = sin(theta);
	return mat2(c, -s, s, c);
}

float noise(vec2 p) {
	vec2 ip = floor(p);
	vec2 fp = fract(p);
	float a = hash12(ip);
	float b = hash12(ip + vec2(1.0, 0.0));
	float c = hash12(ip + vec2(0.0, 1.0));
	float d = hash12(ip + vec2(1.0, 1.0));

	vec2 t = smoothstep(0.0, 1.0, fp);
	return mix(mix(a, b, t.x), mix(c, d, t.x), t.y);
}

float fbm(vec2 p) {
	float value = 0.0;
	float amplitude = 0.5;
	for (int i = 0; i < OCTAVE_COUNT; ++i) {
		value += amplitude * noise(p);
		p *= rotate2d(0.45);
		p *= 2.0;
		amplitude *= 0.5;
	}
	return value;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
	vec2 uv = fragCoord / iResolution.xy;
	uv = 2.0 * uv - 1.0;
	uv.x *= iResolution.x / iResolution.y;
	uv.x += uXOffset;

	uv += 2.0 * fbm(uv * uSize + 0.8 * iTime * uSpeed) - 1.0;

	float dist = abs(uv.x);
	vec3 baseColor = hsv2rgb(vec3(uHue / 360.0, 0.7, 0.8));
	vec3 col = baseColor * pow(mix(0.0, 0.07, hash11(iTime * uSpeed)) / dist, 1.0) * uIntensity;
	col = pow(col, vec3(1.0));
	float a = clamp(max(col.r, max(col.g, col.b)), 0.0, 1.0);
	fragColor = vec4(col, a);
}

void main() {
	mainImage(gl_FragColor, gl_FragCoord.xy);
}
`;

const compileShader = (gl: WebGLRenderingContext, source: string, type: number) => {
	const shader = gl.createShader(type);
	if (!shader) return null;
	gl.shaderSource(shader, source);
	gl.compileShader(shader);
	if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
		console.error('Lightning shader compile error:', gl.getShaderInfoLog(shader));
		gl.deleteShader(shader);
		return null;
	}
	return shader;
};

export const createReactBitsLightning = (canvas: HTMLCanvasElement) => {
	const gl = canvas.getContext('webgl', {
		alpha: true,
		premultipliedAlpha: false,
		preserveDrawingBuffer: true,
	});
	if (!gl) throw new Error('WebGL not supported for React Bits lightning');

	const vertexShader = compileShader(gl, VERTEX_SHADER, gl.VERTEX_SHADER);
	const fragmentShader = compileShader(gl, FRAGMENT_SHADER, gl.FRAGMENT_SHADER);
	if (!vertexShader || !fragmentShader) throw new Error('Lightning shader init failed');

	const program = gl.createProgram();
	if (!program) throw new Error('Lightning program init failed');
	gl.attachShader(program, vertexShader);
	gl.attachShader(program, fragmentShader);
	gl.linkProgram(program);
	if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
		throw new Error(`Lightning program link error: ${gl.getProgramInfoLog(program)}`);
	}

	const vertices = new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]);
	const vertexBuffer = gl.createBuffer();
	if (!vertexBuffer) throw new Error('Lightning buffer init failed');
	gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
	gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

	const aPosition = gl.getAttribLocation(program, 'aPosition');
	const iResolutionLocation = gl.getUniformLocation(program, 'iResolution');
	const iTimeLocation = gl.getUniformLocation(program, 'iTime');
	const uHueLocation = gl.getUniformLocation(program, 'uHue');
	const uXOffsetLocation = gl.getUniformLocation(program, 'uXOffset');
	const uSpeedLocation = gl.getUniformLocation(program, 'uSpeed');
	const uIntensityLocation = gl.getUniformLocation(program, 'uIntensity');
	const uSizeLocation = gl.getUniformLocation(program, 'uSize');

	const bindState = () => {
		gl.useProgram(program);
		gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
		gl.enableVertexAttribArray(aPosition);
		gl.vertexAttribPointer(aPosition, 2, gl.FLOAT, false, 0, 0);
	};

	bindState();

	const drawPass = (uniforms: ReactBitsLightningUniforms, timeSec: number) => {
		bindState();
		gl.uniform2f(iResolutionLocation, canvas.width, canvas.height);
		gl.uniform1f(iTimeLocation, timeSec);
		gl.uniform1f(uHueLocation, uniforms.hue);
		gl.uniform1f(uXOffsetLocation, uniforms.xOffset);
		gl.uniform1f(uSpeedLocation, uniforms.speed);
		gl.uniform1f(uIntensityLocation, uniforms.intensity);
		gl.uniform1f(uSizeLocation, uniforms.size);
		gl.drawArrays(gl.TRIANGLES, 0, 6);
	};

	return {
		resize(width: number, height: number) {
			const w = Math.max(1, Math.round(width));
			const h = Math.max(1, Math.round(height));
			canvas.width = w;
			canvas.height = h;
			bindState();
			gl.viewport(0, 0, w, h);
		},

		render(uniforms: ReactBitsLightningUniforms, timeSec: number) {
			gl.clearColor(0, 0, 0, 0);
			gl.clear(gl.COLOR_BUFFER_BIT);
			drawPass(uniforms, timeSec);
		},

		/** Draw any number of additive bolts, each with its own time seed. */
		renderStrikes(
			strikes: Array<{ uniforms: ReactBitsLightningUniforms; timeSec: number } | null>,
		) {
			gl.clearColor(0, 0, 0, 0);
			gl.clear(gl.COLOR_BUFFER_BIT);
			gl.enable(gl.BLEND);
			gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
			for (const strike of strikes) {
				if (strike && strike.uniforms.intensity > 0.01) {
					drawPass(strike.uniforms, strike.timeSec);
				}
			}
			gl.disable(gl.BLEND);
		},

		/** Exactly two bolts max — second pass is additive with its own time seed. */
		renderDual(
			bolt1: ReactBitsLightningUniforms | null,
			bolt2: ReactBitsLightningUniforms | null,
			timeSec: number,
			timeSec2: number,
		) {
			gl.clearColor(0, 0, 0, 0);
			gl.clear(gl.COLOR_BUFFER_BIT);
			if (bolt1 && bolt1.intensity > 0.01) {
				drawPass(bolt1, timeSec);
			}
			if (bolt2 && bolt2.intensity > 0.01) {
				gl.enable(gl.BLEND);
				gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
				drawPass(bolt2, timeSec2);
				gl.disable(gl.BLEND);
			}
		},

		renderMulti(
			xOffsets: number[],
			base: Omit<ReactBitsLightningUniforms, 'xOffset'>,
			timeSec: number,
		) {
			gl.clearColor(0, 0, 0, 0);
			gl.clear(gl.COLOR_BUFFER_BIT);
			gl.enable(gl.BLEND);
			gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
			for (const xOffset of xOffsets) {
				drawPass({ ...base, xOffset, intensity: base.intensity * 0.82 }, timeSec);
			}
			gl.disable(gl.BLEND);
		},

		destroy() {
			gl.deleteProgram(program);
			gl.deleteShader(vertexShader);
			gl.deleteShader(fragmentShader);
			gl.deleteBuffer(vertexBuffer);
		},
	};
};
