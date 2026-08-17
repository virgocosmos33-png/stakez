/**
 * Big-win celebration scenes. Each hero plate has its own one-shot track
 * (wincelebrationsaudios/scene 1..6). The plate holds until that track ends,
 * then the next scene starts — unless the player skips.
 *
 * These stay as standalone mp3s, same as the bonus beds. They are too long
 * for the SFX sprite, and they must play once (not loop) so "end" is real.
 */
import { Howl } from 'howler';

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
	bgm_celeb_1: '/assets/audio/bgm_celeb_1.mp3',
	bgm_celeb_2: '/assets/audio/bgm_celeb_2.mp3',
	bgm_celeb_3: '/assets/audio/bgm_celeb_3.mp3',
	bgm_celeb_4: '/assets/audio/bgm_celeb_4.mp3',
	bgm_celeb_5: '/assets/audio/bgm_celeb_5.mp3',
	bgm_celeb_6: '/assets/audio/bgm_celeb_6.mp3',
};

/** Probed lengths of scene 1..6. Count-up pacing and the Howl end-guard use these. */
export const CELEB_SCENE_MS: Record<CelebSceneName, number> = {
	bgm_celeb_1: 20402,
	bgm_celeb_2: 8673,
	bgm_celeb_3: 8699,
	bgm_celeb_4: 17345,
	bgm_celeb_5: 8699,
	bgm_celeb_6: 28369,
};

const AUDIO_END_GUARD_MS = 200;

const howls = new Map<CelebSceneName, Howl>();
let active: CelebSceneName | null = null;
let playGen = 0;
let endTimer: ReturnType<typeof setTimeout> | null = null;

const track = (name: CelebSceneName) => {
	const existing = howls.get(name);
	if (existing) return existing;
	const howl = new Howl({
		src: [SRC[name]],
		loop: false,
		preload: true,
		html5: true,
	});
	howls.set(name, howl);
	return howl;
};

const applyVolume = (howl: Howl) => {
	howl.volume(stateSoundDerived.volumeMusic());
};

const clearEndTimer = () => {
	if (endTimer === null) return;
	clearTimeout(endTimer);
	endTimer = null;
};

export const isCelebSceneBgm = (name: string): name is CelebSceneName =>
	(CELEB_SCENE_NAMES as readonly string[]).includes(name);

export const celebSceneDurationMs = (name: string) =>
	isCelebSceneBgm(name) ? CELEB_SCENE_MS[name] : 0;

export const preloadCelebSceneBgm = () => {
	for (const name of CELEB_SCENE_NAMES) track(name);
};

export const playCelebSceneBgm = (name: CelebSceneName, onEnd?: () => void) => {
	stopCelebSceneBgm();
	pauseModeBeds();

	const howl = track(name);
	const gen = ++playGen;
	const finish = () => {
		if (gen !== playGen) return;
		clearEndTimer();
		howl.off('end', finish);
		onEnd?.();
	};

	applyVolume(howl);
	howl.off('end');
	howl.once('end', finish);
	endTimer = setTimeout(finish, CELEB_SCENE_MS[name] + AUDIO_END_GUARD_MS);
	howl.play();
	active = name;
};

export const stopCelebSceneBgm = () => {
	playGen += 1;
	clearEndTimer();
	if (!active) return;
	const howl = howls.get(active);
	if (howl) {
		howl.off('end');
		howl.stop();
	}
	active = null;
};

export const syncCelebSceneBgmVolume = () => {
	if (active) applyVolume(track(active));
};
