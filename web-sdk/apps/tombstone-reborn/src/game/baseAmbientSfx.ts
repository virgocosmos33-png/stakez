/**
 * Occasional scary tremolo-guitar stings in the base saloon only.
 * Four takes, picked at random (never the same one twice in a row).
 * Held off during bonus beds and win celebrations.
 */
import { Howl } from 'howler';

import { stateSoundDerived } from 'state-shared';

const SRC = [
	'/assets/audio/sfx_base_tremolo_1.mp3',
	'/assets/audio/sfx_base_tremolo_2.mp3',
	'/assets/audio/sfx_base_tremolo_3.mp3',
	'/assets/audio/sfx_base_tremolo_4.mp3',
] as const;

const VOL = 0.25;
/** About once a minute, with a little drift so it never feels on a grid. */
const FIRST_GAP_MIN_MS = 40_000;
const FIRST_GAP_MAX_MS = 70_000;
const GAP_MIN_MS = 45_000;
const GAP_MAX_MS = 75_000;

const howls: Howl[] = [];
let timer: ReturnType<typeof setTimeout> | null = null;
let lastIndex = -1;
let want = false;
let celebHold = false;
let running = false;

const gap = (min: number, max: number) => min + Math.random() * (max - min);

const track = (index: number) => {
	const existing = howls[index];
	if (existing) return existing;
	const howl = new Howl({
		src: [SRC[index]],
		loop: false,
		preload: true,
		html5: false,
	});
	howls[index] = howl;
	return howl;
};

const pickIndex = () => {
	let index = Math.floor(Math.random() * SRC.length);
	if (SRC.length > 1 && index === lastIndex) index = (index + 1) % SRC.length;
	lastIndex = index;
	return index;
};

const clearTimer = () => {
	if (timer === null) return;
	clearTimeout(timer);
	timer = null;
};

const stopPlaying = () => {
	for (const howl of howls) howl?.stop();
};

const allowed = () => want && !celebHold;

const arm = (delayMs: number) => {
	clearTimer();
	if (!allowed()) return;
	timer = setTimeout(() => {
		timer = null;
		if (!allowed()) return;
		const howl = track(pickIndex());
		howl.volume(VOL * stateSoundDerived.volumeSoundEffect());
		howl.stop();
		howl.play();
		arm(gap(GAP_MIN_MS, GAP_MAX_MS));
	}, delayMs);
};

const sync = () => {
	if (allowed()) {
		if (running) return;
		running = true;
		arm(gap(FIRST_GAP_MIN_MS, FIRST_GAP_MAX_MS));
		return;
	}
	if (!running && timer === null) return;
	running = false;
	clearTimer();
	stopPlaying();
};

export const preloadBaseAmbient = () => {
	for (let i = 0; i < SRC.length; i += 1) track(i);
};

export const setBaseAmbientWanted = (on: boolean) => {
	if (want === on) return;
	want = on;
	sync();
};

export const setBaseAmbientCelebHold = (on: boolean) => {
	if (celebHold === on) return;
	celebHold = on;
	sync();
};
