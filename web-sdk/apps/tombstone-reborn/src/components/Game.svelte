<script lang="ts">
	import { EnablePixiExtension } from 'components-pixi';
	import { EnableHotkey } from 'components-shared';
	import { MainContainer } from 'components-layout';
	import { App, Container, Sprite } from 'pixi-svelte';
	import { stateModal, stateMeta, stateUrlDerived } from 'state-shared';

	import { UI } from 'components-ui-pixi';
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
	import { LANE_DOOR_Z } from '../game/laneDoor';
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
	import RoomAtmosphere from './RoomAtmosphere.svelte';
	import BulletHits from './BulletHits.svelte';
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

	/** Mobile/portrait: centered high in the band above the reel frame. */
	const aboveReelsLogo = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const main = context.stateLayoutDerived.mainLayout();
		const canvas = context.stateLayoutDerived.canvasSizes();
		const frameTop = board.visualTop + stateShake.y;
		const screenTop = (0 - canvas.height / 2) / main.scale + main.height / 2;
		const gap = 10;
		const topPad = 4;
		const maxH = Math.max(48, frameTop - gap - topPad);
		const widthBySpace = maxH / LOGO_ASPECT;
		const widthByBoard = (board.visualRight - board.visualLeft) * 0.78;
		const width = Math.min(widthBySpace, widthByBoard);
		const height = width * LOGO_ASPECT;
		// Pin the top of the wordmark near the screen; don't cover the timber.
		const yTop = screenTop + topPad + height;
		const yBoard = frameTop - gap;
		return {
			x: board.x + stateShake.x,
			y: Math.min(yTop, yBoard),
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

		<!-- Plaque numbers / wood in front of the wordmark. Hang chains stay
			on the western Spine scene so they are not drawn twice. -->
		<MainContainer>
			<Container sortableChildren zIndex={2}>
				{#if logoStacked}
					{@const L = aboveReelsLogo}
					<Container zIndex={1} x={L.x} y={L.y}>
						<Sprite
							key="mirrorLogo"
							anchor={{ x: 0.5, y: 1 }}
							width={L.width}
							height={L.height}
						/>
					</Container>
				{/if}
				<Container zIndex={2}>
					<SpecialBar layer="hud" />
				</Container>
			</Container>
			<BoardPlate layer="back" />
		</MainContainer>

		<!-- The baked timber ring rides ABOVE the reels (z 3): cards dropping
			through a window that outgrows the authored ring pass BEHIND the
			planks instead of painting over them. -->
		<MainContainer>
			<Board />
			<BoardPlate layer="ring" />
			<Anticipations />
		</MainContainer>

		<!-- LAST-REEL LANE: one MainContainer so the lid zIndex actually
			sorts above the sliding gold card. The wrapper stays above the
			board (and the timber slot) so the door never sits under a card. -->
		<Container zIndex={LANE_DOOR_Z}>
			<MainContainer>
				<LaneGoldCard />
				<LaneLidLock />
			</MainContainer>
		</Container>

		<!-- CLICK-TO-SHOOT: left-click the idle reel area for a hole, muzzle
			fire, and smoke. Cleared the moment a spin starts. -->
		<BulletHits />

		<!-- Last-reel premium WAYS badge (HUD WIN multi is a separate stack). -->
		<StretchWays />

		<!-- Legacy sideways nudge (old books only). -->
		<NudgeSlide />

		<!-- NUDGE WAYS: full-reel totem slides down; header seats on the board. -->
		<NudgeWays />

		<!-- GUNSMOKE / TOMBSTONE / BOUNTY western bursts. -->
		<FeatureBurst />

		<!-- SPLIT / SUPERSPLIT: fast stab to ~90° → 0.5s hold → cut-drag, then N panes. -->
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
			<!-- Shared skip bus: reel tap + Space → stopButtonClick (slam-stop;
				a tap on moving reels also engages super turbo). Win / FS panels
				/ transition also listen on that bus. -->
			<TapToSkip />

			<!-- WAYS / WIN on the right (SpecialBar); FREE SPINS in the last-reel
				empty frame. This is the narrow-layout fallback only. -->
			<FrameMorphHud />

			<UI>
				{#snippet gameName()}{/snippet}
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

			<!-- Bonus-entry banner. Awaited by freeSpinTrigger AFTER the
				trigger spin resolves (scatters + wins). Mounted last so it
				covers the HUD — a takeover, nothing under it is actionable. -->
			<BonusEntry />
		</Container>
	{/if}
</App>

<RoomAtmosphere />

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
