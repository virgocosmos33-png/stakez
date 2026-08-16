import { SCENE_ART, SALOON_LAMPS } from './saloonLamps';

/** Glass globe in left-lamp container space (origin = chain mount). */
export const LAMP_GLOBE = { x: 0, y: 240, rx: 50, ry: 60 } as const;

/** Canvas-space AABB over the swinging globe. Sized loose so the idle sway
 * still sits inside the hit. */
export const lampGlobeCanvas = (canvas: { width: number; height: number }) => {
	const L = SALOON_LAMPS.L;
	const sceneX = L.x + LAMP_GLOBE.x;
	const sceneY = L.y + LAMP_GLOBE.y;
	const scale = Math.max(canvas.width / SCENE_ART.width, canvas.height / SCENE_ART.height);
	return {
		x: canvas.width / 2 + (sceneX - SCENE_ART.width / 2) * scale,
		y: canvas.height / 2 + (sceneY - SCENE_ART.height / 2) * scale,
		width: LAMP_GLOBE.rx * 2 * 1.65 * scale,
		height: LAMP_GLOBE.ry * 2 * 1.65 * scale,
	};
};
