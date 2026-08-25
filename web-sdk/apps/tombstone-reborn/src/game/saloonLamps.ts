import { HANGING_LAMPS } from './hangingLamps.generated';

/** Live plate is western_scene2 (Crystal 2684). Layout seats: Desktop western_scene2.psd ×2. */

export const SCENE_ART = { width: 2684, height: 1784 } as const;

/** Nail line on the street beam (SCENE_ART px). Top of each PSD lamp chain. */
export const SCENE_BEAM_HOOK_Y = HANGING_LAMPS.L.y;

/** Cover-fit scene pixel → main layout space (same transform as SaloonScene). */
export const sceneToMain = (
	sceneX: number,
	sceneY: number,
	canvas: { width: number; height: number },
	main: { width: number; height: number; scale: number },
) => {
	const sceneScale = Math.max(canvas.width / SCENE_ART.width, canvas.height / SCENE_ART.height);
	return {
		x: main.width / 2 + ((sceneX - SCENE_ART.width / 2) * sceneScale) / main.scale,
		y: main.height / 2 + ((sceneY - SCENE_ART.height / 2) * sceneScale) / main.scale,
	};
};

export type SceneRect = { left: number; top: number; right: number; bottom: number };

/** PSD bbox in SCENE_ART → main-space sprite rect (anchor 0,0). */
export const sceneRectToMain = (
	rect: SceneRect,
	canvas: { width: number; height: number },
	main: { width: number; height: number; scale: number },
) => {
	const a = sceneToMain(rect.left, rect.top, canvas, main);
	const b = sceneToMain(rect.right, rect.bottom, canvas, main);
	return {
		x: a.x,
		y: a.y,
		w: Math.max(1, b.x - a.x),
		h: Math.max(1, b.y - a.y),
	};
};

export type SaloonLamp = {
	/** Chain mount in SCENE_ART pixels. */
	x: number;
	y: number;
	width: number;
	height: number;
	/** Pivot inside the full lamp layer (0–1), at the chain mount. */
	anchorX: number;
	anchorY: number;
};

export const SALOON_LAMPS: { L: SaloonLamp; R: SaloonLamp } = {
	L: {
		x: 299.38,
		y: -42.82,
		width: 1952,
		height: 1862,
		anchorX: 0.4804,
		anchorY: 0,
	},
	R: {
		x: 3032.62,
		y: -42.82,
		width: 1952,
		height: 1862,
		anchorX: 0.4938,
		anchorY: 0,
	},
};
