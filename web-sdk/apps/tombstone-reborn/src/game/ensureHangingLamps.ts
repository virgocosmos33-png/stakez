import * as SPINE_PIXI from '@esotericsoftware/spine-pixi-v8';
import { Rectangle, Texture } from 'pixi.js';
import type { LoadedAssets } from 'pixi-svelte';

/** Same public folder assets.ts / Spine fetch. Do not import these as Vite modules:
 *  Storybook staticDirs serves them as raw JSON/text, so `?import` is not ESM
 *  and ModeBaseBook dies with "Failed to fetch dynamically imported module". */
const HANGING_LAMPS_PUBLIC = '/assets/spines/hanging_lamps';

type LampSources = {
	atlasText: string;
	lampL: object;
	lampR: object;
};

let sources: LampSources | null = null;
let sourcesPromise: Promise<LampSources> | null = null;

const readOk = async (url: string, as: 'text' | 'json') => {
	const res = await fetch(url);
	if (!res.ok) throw new Error(`[HangingLamps] ${url} ${res.status}`);
	return as === 'json' ? res.json() : res.text();
};

export const loadHangingLampSources = (): Promise<LampSources> => {
	if (sources) return Promise.resolve(sources);
	if (!sourcesPromise) {
		sourcesPromise = Promise.all([
			readOk(`${HANGING_LAMPS_PUBLIC}/hanging_lamps.atlas`, 'text') as Promise<string>,
			readOk(`${HANGING_LAMPS_PUBLIC}/hanging_lamp_l.json`, 'json') as Promise<object>,
			readOk(`${HANGING_LAMPS_PUBLIC}/hanging_lamp_r.json`, 'json') as Promise<object>,
		]).then(([atlasText, lampL, lampR]) => {
			sources = { atlasText, lampL, lampR };
			return sources;
		});
	}
	return sourcesPromise;
};

/** Atlas regions for the body stills (same sheet Spine uses). Nail is the top. */
export const LAMP_BODY = {
	L: { x: 2, y: 2, w: 124, h: 464 },
	R: { x: 476, y: 2, w: 124, h: 464 },
} as const;

export const lampBodyTexture = (atlas: Texture, side: keyof typeof LAMP_BODY) => {
	const f = LAMP_BODY[side];
	return new Texture({ source: atlas.source, frame: new Rectangle(f.x, f.y, f.w, f.h) });
};

export const isLampSkeleton = (value: unknown): boolean => {
	if (!value || typeof value !== 'object') return false;
	const data = value as { bones?: unknown; animations?: unknown };
	return Array.isArray(data.bones) && Array.isArray(data.animations);
};

/** Build hangingLampL/R SkeletonData from the already-loaded atlas PNG. */
export const ensureHangingLampSkeletons = (
	loaded: LoadedAssets,
	src: LampSources,
): LoadedAssets => {
	if (isLampSkeleton(loaded.hangingLampL) && isLampSkeleton(loaded.hangingLampR)) return loaded;
	const page = loaded.hangingLampsAtlas as Texture | undefined;
	if (!page?.source) return loaded;
	const atlas = new SPINE_PIXI.TextureAtlas(src.atlasText);
	const spineTex = SPINE_PIXI.SpineTexture.from(page.source);
	for (const p of atlas.pages) p.setTexture(spineTex);
	const loader = new SPINE_PIXI.AtlasAttachmentLoader(atlas);
	const next = { ...loaded };
	if (!isLampSkeleton(next.hangingLampL)) {
		const parser = new SPINE_PIXI.SkeletonJson(loader);
		next.hangingLampL = parser.readSkeletonData(src.lampL);
	}
	if (!isLampSkeleton(next.hangingLampR)) {
		const parser = new SPINE_PIXI.SkeletonJson(loader);
		next.hangingLampR = parser.readSkeletonData(src.lampR);
	}
	return next;
};
