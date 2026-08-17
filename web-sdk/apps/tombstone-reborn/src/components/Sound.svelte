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

	import { playExternalOnce, preloadExternal } from 'utils-sound';

	import { getContext } from '../game/context';
	import {
		isBonusBgm,
		pauseBonusBgm,
		playBonusBgm,
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

	const context = getContext();

	const SPRITE_BEDS: MusicName[] = ['bgm_main'];

	const playModeMusic = (name: MusicName) => {
		if (isCelebSceneBgm(name)) {
			for (const bed of SPRITE_BEDS) sound.stop({ name: bed });
			pauseBonusBgm();
			playCelebSceneBgm(name);
			return;
		}
		stopCelebSceneBgm();
		if (isBonusBgm(name)) {
			for (const bed of SPRITE_BEDS) sound.stop({ name: bed });
			playBonusBgm(name);
			return;
		}
		pauseBonusBgm();
		sound.players.music.play({ name });
	};

	context.eventEmitter.subscribeOnMount({
		// Bought / scatter bonus rounds switch beds in freeSpinTrigger and
		// presentBonusEntry. The lobby / base spin stays on bgm_main.
		soundBetMode: () => playModeMusic('bgm_main'),
		soundPressGeneral: () => sound.players.once.play({ name: 'sfx_btn_general' }),
		soundPressBet: () => sound.players.once.play({ name: 'sfx_btn_spin' }),
		// scatterCounter
		soundScatterCounterIncrease: () => (context.stateGame.scatterCounter = context.stateGame.scatterCounter + 1), // prettier-ignore
		soundScatterCounterClear: () => (context.stateGame.scatterCounter = 0),
		// game
		soundMusic: ({ name }) => playModeMusic(name),
		soundLoop: ({ name }) => sound.players.loop.play({ name }),
		soundOnce: ({ name, forcePlay }) => {
			if (name === 'sfx_win_ways') {
				playExternalOnce(WAYS_WIN_SFX);
				return;
			}
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
			sound.stop({ name });
		},
		soundFade: async ({ name, duration, from, to }) => await sound.fade({ name, duration, from, to }), // prettier-ignore
	});

	onMount(() => {
		preloadExternal(WAYS_WIN_SFX);
		preloadCelebSceneBgm();
		sound.players.music.play({ name: 'bgm_main' });
	});

	$effect(() => {
		stateSoundDerived.volumeMusic();
		syncBonusBgmVolume();
		syncCelebSceneBgmVolume();
	});
</script>
