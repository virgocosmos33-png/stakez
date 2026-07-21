<script lang="ts">
	import { onMount } from 'svelte';

	import { EnablePixiExtension } from 'components-pixi';
	import { EnableHotkey } from 'components-shared';
	import { MainContainer } from 'components-layout';
	import { App, Sprite, REM } from 'pixi-svelte';
	import { stateModal, stateMeta, stateUrlDerived } from 'state-shared';

	import { UI, UiGameName } from 'components-ui-pixi';
	import { GameVersion, Modals } from 'components-ui-html';

	import { getContext } from '../game/context';
	import { getBetModeMeta } from '../game/betModeMeta';
	import EnableSound from './EnableSound.svelte';
	import EnableGameActor from './EnableGameActor.svelte';
	import ResumeBet from './ResumeBet.svelte';
	import Sound from './Sound.svelte';
	import Background from './Background.svelte';
	import LoadingScreen from './LoadingScreen.svelte';
	import BoardFrame from './BoardFrame.svelte';
	import BoardFramePlasma from './BoardFramePlasma.svelte';
	import Board from './Board.svelte';
	import Anticipations from './Anticipations.svelte';
	import Win from './Win.svelte';
	import FreeSpinOutro from './FreeSpinOutro.svelte';
	import Transition from './Transition.svelte';
	import ApparitionOverlay from './ApparitionOverlay.svelte';
	import SceneCharacter from './SceneCharacter.svelte';
	import FrameMorphHud from './FrameMorphHud.svelte';
	import BonusLevelBanner from './BonusLevelBanner.svelte';
	import MirrorShatter from './MirrorShatter.svelte';
	import WinSweep from './WinSweep.svelte';
	import WinDim from './WinDim.svelte';
	import WinLightning from './WinLightning.svelte';
	import PlasmaLiner from './PlasmaLiner.svelte';
	import TapToSkip from './TapToSkip.svelte';

	const context = getContext();

	// Madam Mirror bet modes drive the buy-bonus menu (3 buyable bonus levels);
	// social mode rewrites prohibited gambling terms for stake.us
	stateMeta.betModeMeta = getBetModeMeta(stateUrlDerived.social());

	onMount(() => (context.stateLayout.showLoadingScreen = true));

	context.eventEmitter.subscribeOnMount({
		buyBonusConfirm: () => {
			stateModal.modal = { name: 'buyBonusConfirm' };
		},
	});
</script>

<App>
	<EnableSound />
	<EnableHotkey />
	<EnableGameActor />
	<EnablePixiExtension />

	<Background />

	{#if context.stateLayout.showLoadingScreen}
		<LoadingScreen onloaded={() => (context.stateLayout.showLoadingScreen = false)} />
	{:else}
		<ResumeBet />
		<!--
			The reason why <Sound /> is rendered after clicking the loading screen:
			"Autoplay with sound is allowed if: The user has interacted with the domain (click, tap, etc.)."
			Ref: https://developer.chrome.com/blog/autoplay
		-->
		<Sound />

		<MainContainer>
			<BoardFrame />
		</MainContainer>

		<MainContainer>
			<Board />
			<Anticipations />
		</MainContainer>

		<!-- Lady Mirror mascot standing beside the reels on the right; lives in the
			board's design space so she scales with it and never drifts, and is
			positioned clear of the symbols (hidden on layouts too narrow to fit) -->
		<SceneCharacter />

		<!-- purple mirror-fire ring around the frame (free spins), above the reels -->
		<BoardFramePlasma />

		<ApparitionOverlay />
		<WinDim />
		<!-- green plasma liner burns around the linked symbols, above the dim -->
		<PlasmaLiner />
		<WinSweep />
		<MirrorShatter />

		<!-- mega-win FX: full-canvas prismatic + board lightning (must sit above board FX) -->
		<WinLightning />

		<!-- tap/click anywhere over the reels to slam-stop / skip the spin
			(NLC-style); only active while a spin/animation is in progress -->
		<TapToSkip />

		<!-- WAYS / WIN / FREE SPINS morphed into the ONE reel-frame top rail
			(never a second overlapping side panel) -->
		<FrameMorphHud />

		<UI>
			{#snippet gameName()}
				<UiGameName name="MADAM MIRROR" />
			{/snippet}
			{#snippet logo()}
				<!-- logo art is 1024x641; anchored to the top-right corner of the canvas -->
				<Sprite
					key="mirrorLogo"
					anchor={{ x: 1, y: 0 }}
					y={REM * 0.5}
					width={REM * 5.5}
					height={REM * 5.5 * (641 / 1024)}
				/>
			{/snippet}
		</UI>
		<Win />
		<FreeSpinOutro />
		<!-- mounted after the free-spin panels so the level banner is never
			covered by their dim/plate layers -->
		<BonusLevelBanner />
		<Transition />
	{/if}
</App>

<Modals>
	{#snippet version()}
		<GameVersion version="0.0.0" />
	{/snippet}
</Modals>
