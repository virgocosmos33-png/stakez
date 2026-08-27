<script lang="ts" module>
	import { sound, type MusicName, type SoundEffectName, type SoundName } from '../game/sound';

	export type EmitterEventSound =
		| { type: 'soundMusic'; name: MusicName }
		| { type: 'soundOnce'; name: SoundEffectName; forcePlay?: boolean }
		| { type: 'soundLoop'; name: SoundEffectName }
		| { type: 'soundStop'; name: SoundName }
		| { type: 'soundFade'; name: SoundName; from: number; to: number; duration: number }
		| { type: 'soundScatterCounterIncrease' }
		| { type: 'soundScatterCounterClear' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';

	import { stateSoundDerived } from 'state-shared';

	import { preloadExternal } from 'utils-sound';
	import { fadeThemed, playThemedLoop, playThemedOnce, preloadThemedSfx, stopThemed } from '../game/sfxTheme';

	import { getContext } from '../game/context';
	import {
		preloadBaseAmbient,
		setBaseAmbientWanted,
	} from '../game/baseAmbientSfx';
	import {
		isBonusBgm,
		playBonusBgm,
		preloadBonusBgm,
		restoreBaseMusic,
		stopBonusBgm,
		syncBonusBgmVolume,
	} from '../game/bonusBgm';
	import {
		isCelebSceneBgm,
		playCelebSceneBgm,
		preloadCelebSceneBgm,
		stopCelebSceneBgm,
		syncCelebSceneBgmVolume,
	} from '../game/celebSceneBgm';

	const WAYS_WIN_SFX = '/assets/audio/sfx_win_ways.mp3';
	const CELEB_SCENE_CUT_SFX = '/assets/audio/sfx_celeb_scene_cut.mp3';

	const context = getContext();

	const playModeMusic = (name: MusicName) => {
		if (isCelebSceneBgm(name)) {
			playCelebSceneBgm(name);
			return;
		}
		stopCelebSceneBgm();
		if (isBonusBgm(name)) {
			sound.players.music.pause();
			playBonusBgm(name);
			return;
		}
		restoreBaseMusic();
	};

	context.eventEmitter.subscribeOnMount({
		// Bought / scatter bonus rounds switch beds in freeSpinTrigger and
		// presentBonusEntry. The lobby / base spin stays on bgm_main.
		soundBetMode: () => playModeMusic('bgm_main'),
		soundPressGeneral: () => {
			if (!playThemedOnce('sfx_btn_general')) sound.players.once.play({ name: 'sfx_btn_general' });
		},
		soundPressBet: () => {
			if (!playThemedOnce('sfx_btn_spin')) sound.players.once.play({ name: 'sfx_btn_spin' });
		},
		// scatterCounter
		soundScatterCounterIncrease: () => (context.stateGame.scatterCounter = context.stateGame.scatterCounter + 1), // prettier-ignore
		soundScatterCounterClear: () => (context.stateGame.scatterCounter = 0),
		// game
		soundMusic: ({ name }) => playModeMusic(name),
		soundLoop: ({ name }) => {
			if (playThemedLoop(name)) return;
			sound.players.loop.play({ name });
		},
		soundOnce: ({ name, forcePlay }) => {
			if (playThemedOnce(name, { forcePlay })) return;
			sound.players.once.play({ name, forcePlay });
		},
		soundStop: ({ name }) => {
			if (isCelebSceneBgm(name)) {
				stopCelebSceneBgm();
				return;
			}
			if (isBonusBgm(name)) {
				stopBonusBgm();
				return;
			}
			stopThemed(name);
			sound.stop({ name });
		},
		soundFade: async ({ name, duration, from, to }) => {
			if (fadeThemed(name, from, to, duration)) return;
			await sound.fade({ name, duration, from, to });
		},
	});

	onMount(() => {
		preloadExternal(WAYS_WIN_SFX);
		preloadExternal(CELEB_SCENE_CUT_SFX);
		preloadThemedSfx();
		preloadCelebSceneBgm();
		preloadBonusBgm();
		preloadBaseAmbient();
		sound.players.music.play({ name: 'bgm_main' });
	});

	$effect(() => {
		const inBase =
			context.stateGame.gameType === 'basegame' &&
			context.stateGame.atmosphere === 'base' &&
			!context.stateLayout.showLoadingScreen;
		setBaseAmbientWanted(inBase);
	});

	$effect(() => {
		stateSoundDerived.volumeMusic();
		syncBonusBgmVolume();
		syncCelebSceneBgmVolume();
	});
</script>
