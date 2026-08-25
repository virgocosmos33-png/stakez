/** Duck-type the ready TR2 western skeleton. Never use instanceof —
 *  app vs pixi-svelte can load two copies of spine-pixi-v8. */
export const isWesternSceneSkeleton = (data: unknown) => {
	const skeleton = data as { bones?: unknown; animations?: unknown } | undefined;
	return Array.isArray(skeleton?.bones) && Array.isArray(skeleton?.animations);
};

/** lamp_state.json from TR2-Spine-Background-scene. */
export const WESTERN_SCENE_FX = {
	viewW: 1342,
	viewH: 892,
	smoke: true,
	fire: true,
	density: 48,
	speed: 1,
} as const;
