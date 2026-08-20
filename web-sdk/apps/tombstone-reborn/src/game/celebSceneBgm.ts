/**
 * Big-win celebration scenes. Each hero plate has its own looping bed
 * (scene 1 / 2 / 4 / 6 / 7 / 8). The plate holds for the clip, then the
 * next scene starts — unless the player skips. Music loops until then.
 *
 * These stay as standalone mp3s, same as the bonus beds. They are too long
 * for the SFX sprite.
 */
import { Howl, Howler } from 'howler';

import { stateSoundDerived } from 'state-shared';

import { pauseModeBeds } from './bonusBgm';

export const CELEB_SCENE_NAMES = [
	'bgm_celeb_1',
	'bgm_celeb_2',
	'bgm_celeb_3',
	'bgm_celeb_4',
	'bgm_celeb_5',
	'bgm_celeb_6',
] as const;

export type CelebSceneName = (typeof CELEB_SCENE_NAMES)[number];

const SRC: Record<CelebSceneName, string> = {
	bgm_celeb_1: '/assets/audio/bgm_celeb_1.mp3?v=tr20',
	bgm_celeb_2: '/assets/audio/bgm_celeb_2.mp3?v=tr20',
	bgm_celeb_3: '/assets/audio/bgm_celeb_3.mp3?v=tr20',
	bgm_celeb_4: '/assets/audio/bgm_celeb_4.mp3?v=tr20',
	bgm_celeb_5: '/assets/audio/bgm_celeb_5.mp3?v=tr20',
	bgm_celeb_6: '/assets/audio/bgm_celeb_6.mp3?v=tr20',
};

/** Probed one-shot lengths. Scenes loop, so plate dwell uses the clip, not these. */
export const CELEB_SCENE_MS: Record<CelebSceneName, number> = {
	bgm_celeb_1: 30067,
	bgm_celeb_2: 23353,
	bgm_celeb_3: 11102,
	bgm_celeb_4: 7915,
	bgm_celeb_5: 19722,
	bgm_celeb_6: 18834,
};

const howls = new Map<CelebSceneName, Howl>();
let active: CelebSceneName | null = null;

const track = (name: CelebSceneName) => {
	const existing = howls.get(name);
	if (existing) return existing;
	const howl = new Howl({
		src: [SRC[name]],
		loop: true,
		preload: true,
		html5: false,
	});
	howls.set(name, howl);
	return howl;
};

const applyVolume = (howl: Howl) => {
	howl.volume(stateSoundDerived.volumeMusic());
};

export const isCelebSceneBgm = (name: string): name is CelebSceneName =>
	(CELEB_SCENE_NAMES as readonly string[]).includes(name);

export const celebSceneDurationMs = (name: string) =>
	isCelebSceneBgm(name) ? CELEB_SCENE_MS[name] : 0;

export const preloadCelebSceneBgm = () => {
	for (const name of CELEB_SCENE_NAMES) track(name);
};

export const playCelebSceneBgm = (name: CelebSceneName) => {
	stopCelebSceneBgm();
	pauseModeBeds();

	const howl = track(name);
	applyVolume(howl);
	if (Howler.ctx && Howler.ctx.state !== 'running') void Howler.ctx.resume();
	howl.seek(0);
	howl.play();
	active = name;
};

export const stopCelebSceneBgm = () => {
	if (!active) return;
	const howl = howls.get(active);
	if (howl) howl.stop();
	active = null;
};

export const syncCelebSceneBgmVolume = () => {
	if (active) applyVolume(track(active));
};
