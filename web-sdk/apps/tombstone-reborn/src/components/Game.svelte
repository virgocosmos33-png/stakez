<script lang="ts">
	import { EnablePixiExtension } from 'components-pixi';
	import { EnableHotkey } from 'components-shared';
	import { MainContainer } from 'components-layout';
	import { App, Container, Sprite } from 'pixi-svelte';
	import { stateModal, stateMeta, stateUrlDerived } from 'state-shared';

	import { UI, UiGameName } from 'components-ui-pixi';
	import { GameVersion, Modals, ReplayPanel, setGameInfo } from 'components-ui-html';

	import { getContext } from '../game/context';
	import { getBetModeMeta } from '../game/betModeMeta';
	import {
		WHITE_ROOM_SPECIALS,
		WHITE_ROOM_INFO_SECTIONS,
		WHITE_ROOM_PAY_KINDS,
		WHITE_ROOM_HIGH_SYMBOLS,
		WHITE_ROOM_LOW_SYMBOLS,
	} from '../game/gameInfo';
	import { applyHudTheme } from '../game/hudInit';
	import { stateShake } from '../game/stateShake.svelte';
	import EnableSound from './EnableSound.svelte';
	import EnableGameActor from './EnableGameActor.svelte';
	import ResumeBet from './ResumeBet.svelte';
	import Sound from './Sound.svelte';
	import Background from './Background.svelte';
	import LoadingScreen from './LoadingScreen.svelte';
	import Board from './Board.svelte';
	import BoardPlate from './BoardPlate.svelte';
	import SpecialBar from './SpecialBar.svelte';
	import TargetLock from './TargetLock.svelte';
	import Anticipations from './Anticipations.svelte';
	import Win from './Win.svelte';
	import Transition from './Transition.svelte';
	import FrameMorphHud from './FrameMorphHud.svelte';
	import SplitPanes from './SplitPanes.svelte';
	import CloneMorph from './CloneMorph.svelte';
	import WildFlip from './WildFlip.svelte';
	import GunsmokeWounds from './GunsmokeWounds.svelte';
	import LinkedCellFire from './LinkedCellFire.svelte';
	import StretchWays from './StretchWays.svelte';
	import NudgeSlide from './NudgeSlide.svelte';
	import NudgeWays from './NudgeWays.svelte';
	import FeatureBurst from './FeatureBurst.svelte';
	import WinSweep from './WinSweep.svelte';
	import TapToSkip from './TapToSkip.svelte';
	import BonusEntry from './BonusEntry.svelte';
	import BulletHits from './BulletHits.svelte';
	import SaloonLampHit from './SaloonLampHit.svelte';
	import LaneLidLock from './LaneLidLock.svelte';
	import LaneGoldCard from './LaneGoldCard.svelte';

	const context = getContext();

	// sheriff wordmark — bloody wanted-poster type (1514×717)
	const LOGO_ASPECT = 717 / 1514;

	// portrait / tablet → above reels; desktop / landscape → Layout* top-right slot
	const logoStacked = $derived.by(() => {
		const t = context.stateLayoutDerived.layoutType();
		return t === 'portrait' || t === 'tablet';
	});

	/** Mobile/portrait: centered just above the reel frame. */
	const aboveReelsLogo = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const frameTop = board.visualTop + stateShake.y;
		const gap = 10;
		const topPad = 28;
		// Fit the wide wordmark into the band above the frame.
		const maxH = Math.max(48, frameTop - gap - topPad);
		const widthBySpace = maxH / LOGO_ASPECT;
		const widthByBoard = (board.visualRight - board.visualLeft) * 0.78;
		const width = Math.min(widthBySpace, widthByBoard);
		const height = width * LOGO_ASPECT;
		return {
			x: board.x + stateShake.x,
			// anchor y=1 → bottom edge sits `gap` above the frame top
			y: frameTop - gap,
			width,
			height,
		};
	});

	/** Desktop/landscape: Layout* parks this at canvas width-20, y=0 (top-right). */
	const cornerLogo = $derived.by(() => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const layoutType = context.stateLayoutDerived.layoutType();
		// Readable mark; leave room for spin/HUD bottom bar and board crest.
		const width =
			layoutType === 'landscape'
				? Math.min(240, Math.max(168, canvas.height * 0.28))
				: Math.min(280, Math.max(200, canvas.height * 0.26));
		return {
			width,
			height: width * LOGO_ASPECT,
			topPad: layoutType === 'landscape' ? 10 : 14,
		};
	});

	// Config-driven HUD theming: push this game's hud.generated colours into the
	// shared components-ui-pixi theme BEFORE the HUD renders. Inert for other games.
	applyHudTheme();

	// Tombstone bet modes drive the buy-bonus menu (small / super single-spin buys);
	// social mode rewrites prohibited gambling terms for stake.us
	stateMeta.betModeMeta = getBetModeMeta(stateUrlDerived.social());

	// Install Tombstone Reborn info / pay-table prose (info menu + HUD marquee)
	// before either first renders. Pay rows are 6 / 5 / 4 / 3 of a kind.
	setGameInfo(WHITE_ROOM_SPECIALS, WHITE_ROOM_INFO_SECTIONS, {
		kinds: WHITE_ROOM_PAY_KINDS,
		highs: WHITE_ROOM_HIGH_SYMBOLS,
		lows: WHITE_ROOM_LOW_SYMBOLS,
		wilds: [{ key: 'w', name: 'Wild — The Revolver', pays: [10] }],
		wildsNote:
			'Wilds only win on their own when they connect on every column of the board — 6 wide — at 10× bet per way.',
	});

	// Do NOT force showLoadingScreen=true on mount: StoryGameTemplate sets
	// showLoadingScreen = !skipLoadingScreen once assets load, and createLayout
	// already defaults it to true for real sessions. Forcing true here races
	// Storybook skip and can leave the board unmounted after HMR remounts.

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

		<!-- BoardFrame REMOVED: diamond board (4-3-2-3-4) renders with no frame
			behind the symbols. -->

		<!-- Mobile/portrait: brand logo centered above the reel frame (logo_v3). -->
		{#if logoStacked}
			<MainContainer>
				{@const L = aboveReelsLogo}
				<Container x={L.x} y={L.y}>
					<Sprite
						key="mirrorLogo"
						anchor={{ x: 0.5, y: 1 }}
						width={L.width}
						height={L.height}
					/>
				</Container>
			</MainContainer>
		{/if}

		<!-- Chains (z 0) under the timber (z 1), boxes (z 2) in front.
			Same MainContainer so zIndex actually sorts them. -->
		<MainContainer>
			<SpecialBar />
			<BoardPlate />
		</MainContainer>

		<MainContainer>
			<Board />
			<Anticipations />
		</MainContainer>

		<!-- LAST-REEL LANE: door sits ABOVE the board plate (z 12) so the
			timber slot never shows as a grey strip beside it. -->
		<Container zIndex={12}>
			<LaneLidLock />
			<LaneGoldCard />
		</Container>

		<!-- CLICK-TO-SHOOT: left-click the idle reel area for a hole, muzzle
			fire, and smoke. Cleared the moment a spin starts. -->
		<BulletHits />
		<!-- Left lantern globe: smash the glass, kill the light until next spin. -->
		<SaloonLampHit />

		<!-- BOUNTY: the landed premium's WIN multiplier badge. -->
		<StretchWays />

		<!-- Legacy sideways nudge (old books only). -->
		<NudgeSlide />

		<!-- NUDGE WAYS: full-reel totem, clipped from the top, grows down. -->
		<NudgeWays />

		<!-- GUNSMOKE / TOMBSTONE / BOUNTY western bursts. -->
		<FeatureBurst />

		<!-- SPLIT / SUPERSPLIT: knife slash, then N panes (up to 4). -->
		<SplitPanes />

		<!-- GUNSMOKE: every copy of one symbol morphs into the revolver WILD. -->
		<CloneMorph />

		<!-- Any symbol becoming a WILD flips to show the bottle on the back. -->
		<WildFlip />

		<!-- Marks the symbols a feature is about to hit. -->
		<TargetLock />

		<!-- Linked / connected cells burn: cell borders and the reel edges they
			sit on. Split cells now carry their own thin pane seams. -->
		<LinkedCellFire />

		<!-- GUNSMOKE / special hits: blood stains clip to the iron cell frame. -->
		<GunsmokeWounds />

		<!-- SceneCharacter REMOVED: the patient beside the reels is gone. The
			right of the board is now empty room by design — do not remount her
			without asking. -->

		<!-- BoardFramePlasma REMOVED: freegame fluorescent frame overlay was blamed
			for dashed cutlines; real dashes were baked into mirror_frame_wide.png
			lips (see tools/strip_frame_quilt_dashes.py). Do not remount. -->

		<WinSweep />

		<!-- SCREEN-LEVEL PRESENTATION — one zIndex layer ABOVE the cell effects.
			CellFlameBorder (9) / CellLightning (10) carry a zIndex so stretch /
			overlay remounts can't cover them, which also lifts them over every
			zIndex-0 sibling mounted later — including these panels. Anything
			that dims the whole screen or banners over it lives in this
			container so the flames can never burn through a win panel. -->
		<Container zIndex={20}>
			<!-- Shared skip bus: reel tap + Space → stopButtonClick (slam-stop +
				temp turbo). Win / FS panels / transition also listen on that bus. -->
			<TapToSkip />

			<!-- WAYS / WIN on the right (SpecialBar); FREE SPINS in the last-reel
				empty frame. This is the narrow-layout fallback only. -->
			<FrameMorphHud />

			<UI>
				{#snippet gameName()}
					<UiGameName name="TOMBSTONE REBORN" />
				{/snippet}
				{#snippet logo()}
					{#if !logoStacked}
						{@const C = cornerLogo}
						<!-- LayoutDesktop / LayoutLandscape: Container at (canvasW-20, 0).
							anchor x=1 → hangs from top-right with a small top pad. -->
						<Sprite
							key="mirrorLogo"
							anchor={{ x: 1, y: 0 }}
							y={C.topPad}
							width={C.width}
							height={C.height}
						/>
					{/if}
				{/snippet}
			</UI>
			<Win />
			<Transition />

			<!-- Bought-bonus announcement: DEAD MAN'S HAND (bonus_small) /
				OPEN GRAVE (bonus_super), awaited by playBet at round start so
				the enhanced spin waits for it. Mounted LAST in this container so
				it covers the HUD as well — it is a takeover, and the player has
				already committed the buy, so nothing under it is actionable. -->
			<BonusEntry />
		</Container>
	{/if}
</App>

<Modals>
	{#snippet version()}
		<GameVersion version="0.0.0" />
	{/snippet}
</Modals>

<!-- Bet Replay intro / "replay again" card. Held back until the loading screen
	is gone so the two never stack. -->
{#if !context.stateLayout.showLoadingScreen}
	<ReplayPanel />
{/if}
