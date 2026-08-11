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
	import LinkedCellFire from './LinkedCellFire.svelte';
	import StretchWays from './StretchWays.svelte';
	import NudgeSlide from './NudgeSlide.svelte';
	import FeatureBurst from './FeatureBurst.svelte';
	import WinSweep from './WinSweep.svelte';
	import WinDim from './WinDim.svelte';
	import TapToSkip from './TapToSkip.svelte';
	import BonusEntry from './BonusEntry.svelte';
	import BulletHits from './BulletHits.svelte';
	import LaneLidLock from './LaneLidLock.svelte';
	import LaneGoldCard from './LaneGoldCard.svelte';

	const context = getContext();

	// Lockstep with BoardFrame.svelte outer size (slim trim — NOT bak-locked rails).
	const LOGO_FRAME_SCALE = 0.34;
	const LOGO_GOLD_INNER_Y = 101;
	const LOGO_FRAME_GAP = 6;
	// logo_v3 master ~2048×2082 (Scenario transparent stack)
	const LOGO_ASPECT = 2082 / 2048;

	// portrait / tablet → above reels; desktop / landscape → Layout* top-right slot
	const logoStacked = $derived.by(() => {
		const t = context.stateLayoutDerived.layoutType();
		return t === 'portrait' || t === 'tablet';
	});

	/** Mobile/portrait: centered just above the reel frame. */
	const aboveReelsLogo = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const outerH =
			board.height + 2 * LOGO_FRAME_GAP + 2 * LOGO_GOLD_INNER_Y * LOGO_FRAME_SCALE;
		const frameTop = board.y + stateShake.y - outerH / 2;
		const gap = 10;
		const topPad = 28;
		// Fit into the clear band above the frame (logo_v3 is nearly square).
		const maxH = Math.max(56, frameTop - gap - topPad);
		const widthBySpace = maxH / LOGO_ASPECT;
		const widthByBoard = board.width * 0.72;
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
				? Math.min(128, Math.max(96, canvas.height * 0.17))
				: Math.min(172, Math.max(132, canvas.height * 0.155));
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

		<!-- The steel plate the symbols are recessed into. Its own MainContainer,
			mounted first, so a board remount can never shuffle it in front. -->
		<MainContainer>
			<BoardPlate />
		</MainContainer>

		<!-- Six special-card nameplates, one per reel, on a plank rail down the
			LEFT of the board (always visible; a card lights its plaque on the
			specialBar book event). Lies down above the board when the side margin
			is too narrow — see SpecialBar.svelte. Needs the MainContainer around
			it: the rail is a raw nine-slice attached to this parent. -->
		<MainContainer>
			<SpecialBar />
		</MainContainer>

		<MainContainer>
			<Board />
			<Anticipations />
		</MainContainer>

		<!-- LAST-REEL LANE: boarded-shut cover while the lane is locked (every
			base/small spin until DIG UP; open all round in the super bonus), and
			the golden sheriff card that flashes when the lane's special fires. -->
		<LaneLidLock />
		<LaneGoldCard />

		<!-- CLICK-TO-SHOOT: left-click the idle reel area to punch a shattered-glass
			bullet hole at the cursor. Cleared the moment a spin starts. -->
		<BulletHits />

		<!-- BOUNTY: the landed premium's WIN multiplier badge. -->
		<StretchWays />

		<!-- NUDGE: premium slides LEFT from the last lane, WIN mult climbs. -->
		<NudgeSlide />

		<!-- GUNSMOKE / TOMBSTONE OPEN / DIG UP / BOUNTY western bursts. -->
		<FeatureBurst />

		<!-- SPLIT-GANG / SPLIT-OUTLAWS / SUPERSPLIT pane tear. -->
		<SplitPanes />

		<!-- GUNSMOKE: every copy of one symbol morphs into the revolver WILD. -->
		<CloneMorph />

		<!-- Marks the symbols a feature is about to hit. -->
		<TargetLock />

		<!-- Linked / connected cells burn: cell borders and the reel edges they
			sit on. This is the connector language now that split cells draw no
			divider at all. -->
		<LinkedCellFire />

		<!-- SceneCharacter REMOVED: the patient beside the reels is gone. The
			right of the board is now empty room by design — do not remount her
			without asking. -->

		<!-- BoardFramePlasma REMOVED: freegame fluorescent frame overlay was blamed
			for dashed cutlines; real dashes were baked into mirror_frame_wide.png
			lips (see tools/strip_frame_quilt_dashes.py). Do not remount. -->

		<WinDim />
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

			<!-- WAYS / WIN / FREE SPINS morphed into the ONE reel-frame top rail
				(never a second overlapping side panel) -->
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
