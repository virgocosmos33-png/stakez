import { Mesh } from 'pixi.js';

import { SALOON_LAMPS } from './saloonLamps';
import { LAMP_GLOBE } from './saloonLampSmash';

/** Dense enough that the globe reads as a smooth dent, not a rubber quad. */
export const LAMP_MESH_COLS = 20;
export const LAMP_MESH_ROWS = 20;

const L = SALOON_LAMPS.L;

/** Globe centre in the lamp sprite's local pixels (origin = top-left of the PNG). */
export const lampHitLocal = () => ({
	x: L.anchorX * L.width + LAMP_GLOBE.x,
	y: L.anchorY * L.height + LAMP_GLOBE.y,
});

export type LampMeshGrid = {
	rest: Float32Array;
	uvs: Float32Array;
	indices: Uint32Array;
};

export const buildLampMeshGrid = (width: number, height: number): LampMeshGrid => {
	const cols = LAMP_MESH_COLS;
	const rows = LAMP_MESH_ROWS;
	const verts = (cols + 1) * (rows + 1);
	const rest = new Float32Array(verts * 2);
	const uvs = new Float32Array(verts * 2);
	const indices = new Uint32Array(cols * rows * 6);

	let i = 0;
	for (let row = 0; row <= rows; row += 1) {
		for (let col = 0; col <= cols; col += 1) {
			const u = col / cols;
			const v = row / rows;
			rest[i] = u * width;
			rest[i + 1] = v * height;
			uvs[i] = u;
			uvs[i + 1] = v;
			i += 2;
		}
	}

	let t = 0;
	for (let row = 0; row < rows; row += 1) {
		for (let col = 0; col < cols; col += 1) {
			const a = row * (cols + 1) + col;
			const b = a + 1;
			const c = a + (cols + 1);
			const d = c + 1;
			indices[t] = a;
			indices[t + 1] = b;
			indices[t + 2] = c;
			indices[t + 3] = b;
			indices[t + 4] = d;
			indices[t + 5] = c;
			t += 6;
		}
	}

	return { rest, uvs, indices };
};

/**
 * Perspective-project the lamp mesh into the room. The chain mount stays
 * planted; the globe takes the hit and shrinks toward a vanish point behind
 * the lantern (into the plate).
 */
export const punchLampVertices = (
	out: Float32Array,
	rest: Float32Array,
	punch: number,
	width: number,
	height: number,
) => {
	if (Math.abs(punch) <= 0.0008) {
		out.set(rest);
		return;
	}

	const hit = lampHitLocal();
	const vanishX = hit.x + 64;
	const vanishY = hit.y - 28;
	const sigma = 240;
	const sigma2 = sigma * sigma;

	for (let i = 0; i < rest.length; i += 2) {
		const x = rest[i];
		const y = rest[i + 1];
		const dx = x - hit.x;
		const dy = y - hit.y;
		const impact = Math.exp(-(dx * dx + dy * dy) / sigma2);
		const hang = Math.pow(Math.min(1, y / (height * 0.55)), 0.72);
		const z = punch * (0.7 * impact + 0.38 * hang);
		const persp = 1 / Math.max(0.38, 1 + z * 0.58);
		let px = vanishX + (x - vanishX) * persp;
		let py = vanishY + (y - vanishY) * persp;
		px += (vanishX - hit.x) * punch * impact * 0.16;
		py += (vanishY - hit.y) * punch * impact * 0.12;
		out[i] = px;
		out[i + 1] = py;
	}
};

export const applyLampPunch = (
	mesh: Mesh,
	rest: Float32Array,
	punch: number,
	width: number,
	height: number,
) => {
	const buffer = mesh.geometry.getBuffer('aPosition');
	const data = buffer.data as Float32Array;
	punchLampVertices(data, rest, punch, width, height);
	buffer.update();
};
