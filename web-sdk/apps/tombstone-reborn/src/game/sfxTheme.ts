/**
 * Tombstone Reborn live SFX. One verb, one file, authored length = 1x beat.
 * Playback rate-locks to fxDur so turbo stays on the animation.
 * Prompts live in tools/sfx_revamp_spec.json (not shipped).
 */
import { fadeExternal, playExternalLoop, playExternalOnce, preloadExternal, stopExternal } from 'utils-sound';

import { fxDur } from './fxTiming';
import type { SoundEffectName } from './sound';

export type ThemedSfx = {
	src: string;
	durationMs: number;
	loop?: boolean;
	volume?: number;
};

const file = (name: string) => `/assets/audio/${name}.mp3`;

export const THEMED_SFX: Partial<Record<SoundEffectName, ThemedSfx>> = {
	sfx_split: { src: file('sfx_split'), durationMs: 450 },
	sfx_split_hit: { src: file('sfx_split_hit'), durationMs: 180 },
	sfx_split_bite: { src: file('sfx_split_bite'), durationMs: 220 },
	sfx_split_thunk: { src: file('sfx_split_thunk'), durationMs: 180 },
	sfx_split_seam_tear: { src: file('sfx_split_seam_tear'), durationMs: 130 },

	// Restored sprite .44 (not the thin A-Z muzzle). Occasional ricochet is
	// layered in playThemedOnce — do not rate-lock these down to a 160ms crack.
	sfx_muzzle: { src: file('sfx_gunshot'), durationMs: 1400 },
	sfx_gunshot: { src: file('sfx_gunshot'), durationMs: 1400 },
	sfx_bullet_ricochet: { src: file('sfx_bullet_ricochet'), durationMs: 1700, volume: 0.7 },
	sfx_shot_reveal: { src: file('sfx_shot_reveal'), durationMs: 280 },
	sfx_gunsmoke: { src: file('sfx_gunsmoke'), durationMs: 900 },
	sfx_lamp_smash: { src: file('sfx_lamp_smash'), durationMs: 400 },
	sfx_celeb_stamp: { src: file('sfx_celeb_stamp'), durationMs: 180 },

	sfx_reel_stop_1: { src: file('sfx_reel_stop_1'), durationMs: 220 },
	sfx_scatter_stop_1: { src: file('sfx_scatter_stop_1'), durationMs: 400 },
	sfx_scatter_stop_2: { src: file('sfx_scatter_stop_2'), durationMs: 480 },
	sfx_scatter_stop_3: { src: file('sfx_scatter_stop_3'), durationMs: 560 },
	sfx_scatter_stop_4: { src: file('sfx_scatter_stop_4'), durationMs: 640 },
	sfx_scatter_stop_5: { src: file('sfx_scatter_stop_5'), durationMs: 720 },
	sfx_tombstone_toll: { src: file('sfx_tombstone_toll'), durationMs: 1000 },
	sfx_wild_land: { src: file('sfx_wild_land'), durationMs: 280 },

	sfx_lane_card: { src: file('sfx_lane_card'), durationMs: 320 },
	sfx_lane_wild: { src: file('sfx_lane_wild'), durationMs: 280 },
	sfx_special_hit: { src: file('sfx_special_hit'), durationMs: 200 },
	sfx_bounty: { src: file('sfx_bounty'), durationMs: 820 },
	sfx_lock_snap: { src: file('sfx_lock_snap'), durationMs: 150 },
	sfx_lock_release: { src: file('sfx_lock_release'), durationMs: 180 },
	sfx_ways_stretch: { src: file('sfx_ways_stretch'), durationMs: 280 },

	sfx_fire_ignite: { src: file('sfx_fire_ignite'), durationMs: 400 },
	sfx_fire_loop: { src: file('sfx_fire_loop'), durationMs: 6000, loop: true, volume: 0.55 },
	sfx_fire_flare: { src: file('sfx_fire_flare'), durationMs: 350 },
	sfx_fire_out: { src: file('sfx_fire_out'), durationMs: 500 },
	sfx_reel_nudge: { src: file('sfx_reel_nudge'), durationMs: 200 },
	sfx_fuse_crackle: { src: file('sfx_fuse_crackle'), durationMs: 600 },
	sfx_ember_whoosh: { src: file('sfx_ember_whoosh'), durationMs: 400 },
	sfx_wild_explode: { src: file('sfx_wild_explode'), durationMs: 800 },

	sfx_anticipation: { src: file('sfx_anticipation'), durationMs: 8000, loop: true, volume: 0.7 },
	sfx_bonus_entry_small: { src: file('sfx_bonus_entry_small'), durationMs: 3000 },
	sfx_bonus_entry_super: { src: file('sfx_bonus_entry_super'), durationMs: 3000 },
	sfx_win_ways: { src: file('sfx_win_ways'), durationMs: 900 },
	sfx_multiplier_up: { src: file('sfx_multiplier_up'), durationMs: 280 },
	sfx_thunder: { src: file('sfx_thunder'), durationMs: 2500 },
	sfx_shovel_strike_1: { src: file('sfx_shovel_strike_1'), durationMs: 200 },
	sfx_shovel_strike_2: { src: file('sfx_shovel_strike_2'), durationMs: 200 },
	sfx_shovel_strike_3: { src: file('sfx_shovel_strike_3'), durationMs: 200 },
	sfx_shovel_settle: { src: file('sfx_shovel_settle'), durationMs: 220 },
	sfx_tombstone_open: { src: file('sfx_tombstone_open'), durationMs: 1000 },

	sfx_btn_general: { src: file('sfx_btn_general'), durationMs: 120 },
	sfx_btn_spin: { src: file('sfx_btn_spin'), durationMs: 150 },
};

const GUNSHOT_NAMES = new Set<SoundEffectName>(['sfx_gunshot', 'sfx_muzzle']);
/** About one in three shots, so a volley is not a ricochet machine-gun. */
const RICOCHET_CHANCE = 0.32;

const maybeRicochet = () => {
	if (Math.random() >= RICOCHET_CHANCE) return;
	const spec = THEMED_SFX.sfx_bullet_ricochet;
	if (!spec) return;
	playExternalOnce(spec.src, {
		durationMs: fxDur(spec.durationMs),
		forcePlay: true,
		volume: spec.volume,
	});
};

export const playThemedOnce = (
	name: SoundEffectName,
	options?: { forcePlay?: boolean; volume?: number },
) => {
	const spec = THEMED_SFX[name];
	if (!spec || spec.loop) return false;
	playExternalOnce(spec.src, {
		durationMs: fxDur(spec.durationMs),
		forcePlay: options?.forcePlay,
		volume: options?.volume ?? spec.volume,
	});
	if (GUNSHOT_NAMES.has(name)) maybeRicochet();
	return true;
};

export const playThemedLoop = (name: SoundEffectName) => {
	const spec = THEMED_SFX[name];
	if (!spec?.loop) return false;
	playExternalLoop(spec.src, { volume: spec.volume });
	return true;
};

export const stopThemed = (name: SoundEffectName | string) => {
	const spec = THEMED_SFX[name as SoundEffectName];
	if (!spec) return false;
	stopExternal(spec.src);
	if (GUNSHOT_NAMES.has(name as SoundEffectName)) {
		const ricochet = THEMED_SFX.sfx_bullet_ricochet;
		if (ricochet) stopExternal(ricochet.src);
	}
	return true;
};

export const fadeThemed = (
	name: SoundEffectName | string,
	from: number,
	to: number,
	durationMs: number,
) => {
	const spec = THEMED_SFX[name as SoundEffectName];
	if (!spec) return false;
	const peak = spec.volume ?? 1;
	return fadeExternal(spec.src, from * peak, to * peak, durationMs);
};

export const preloadThemedSfx = () => {
	const seen = new Set<string>();
	for (const spec of Object.values(THEMED_SFX)) {
		if (!spec || seen.has(spec.src)) continue;
		seen.add(spec.src);
		preloadExternal(spec.src);
	}
};
