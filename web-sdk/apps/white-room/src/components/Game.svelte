<script lang="ts">
	import { onMount } from 'svelte';

	import { EnablePixiExtension } from 'components-pixi';
	import { EnableHotkey } from 'components-shared';
	import { MainContainer } from 'components-layout';
	import { App, Container, Sprite } from 'pixi-svelte';
	import { stateModal, stateMeta, stateUrlDerived } from 'state-shared';

	import { UI, UiGameName } from 'components-ui-pixi';
	import { GameVersion, Modals, ReplayPanel } from 'components-ui-html';

	import { getContext } from '../game/context';
	import { getBetModeMeta } from '../game/betModeMeta';
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
	import TargetLock from './TargetLock.svelte';
	import LockedSlots from './LockedSlots.svelte';
	import CellChassis from './CellChassis.svelte';
	import CellFlameBorder from './CellFlameBorder.svelte';
	import Anticipations from './Anticipations.svelte';
	import Win from './Win.svelte';
	import FreeSpinOutro from './FreeSpinOutro.svelte';
	import Transition from './Transition.svelte';
	import FrameMorphHud from './FrameMorphHud.svelte';
	import BonusLevelBanner from './BonusLevelBanner.svelte';
	import RetriggerBanner from './RetriggerBanner.svelte';
	import CellSealOverlay from './CellSealOverlay.svelte';
	import WildReelSlide from './WildReelSlide.svelte';
	import SplitPanes from './SplitPanes.svelte';
	import CloneMorph from './CloneMorph.svelte';
	import StretchFx from './StretchFx.svelte';
	import StretchWays from './StretchWays.svelte';
	import CellLightning from './CellLightning.svelte';
	import WinSweep from './WinSweep.svelte';
	import WinDim from './WinDim.svelte';
	import WinLightning from './WinLightning.svelte';
	import PlasmaLiner from './PlasmaLiner.svelte';
	import TapToSkip from './TapToSkip.svelte';

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

	// THE WHITE ROOM bet modes drive the buy-bonus menu (THE_INTAKE / HER_SIDE / WHITEOUT);
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

		<MainContainer>
			<Board />
			<Anticipations />
		</MainContainer>

		<!-- Wild Reel: a bottom-slot WILD turns its middle reel wild — the full
			straitjacket "WILD" column slides down over the reel, on top of the
			board symbols but BELOW the special cells + HUD (mounted before them). -->
		<WildReelSlide />

		<!-- STRETCH (wild reel): full wild column rises + a single centred "N WAYS".
			Overflows the board but stays UNDER the special cells + HUD. -->
		<StretchFx />

		<!-- The cell-block chassis: two riveted iron columns bolted either side of
			the board and a beam slung under it. The nine special cells are
			openings punched through this art, so it mounts BEFORE the cells. -->
		<CellChassis />

		<!-- Procedural fire permanently burning around the border of the three
			BOTTOM special-symbol cells. Over the chassis iron (so the outward
			licks show on the metal) but UNDER LockedSlots, whose sockets/
			symbols/bars cover the inward half of the band - the flame reads as
			a burning border, never over the symbol. -->
		<CellFlameBorder />

		<!-- Reserved special-symbol slots framing the board (bottom + side columns):
			empty padded cells behind prison bars; bonus opens them and drops
			premiums/wilds in. Mounted after the wild column so the cell cards
			always sit on top of it. -->
		<LockedSlots />

		<!-- STRETCH (normal reel): each real symbol stretches a little in its own
			cell and, when big (> 5x), shows its per-symbol x-ways. -->
		<StretchWays />

		<!-- SPLIT: the chosen winning symbol cracks into N center-cropped panes that
			snap apart (Madam-Mirror pane split), settling into a slim-seam XN cell. -->
		<SplitPanes />

		<!-- CLONE: every copy of one symbol charges, white-flashes and morphs
			together into the same premium. -->
		<CloneMorph />

		<!-- Marks the symbols a feature is about to hit, just before it fires, so
			the choice is readable instead of lost in the detonation. -->
		<TargetLock />

		<!-- Special cells activation: purple lightning crackles around each cell's
			border in order (bottom L->R, right bottom->top, left top->bottom). -->
		<CellLightning />

		<!-- SceneCharacter REMOVED: the patient beside the reels is gone. The
			right of the board is now empty room by design — do not remount her
			without asking. -->

		<!-- BoardFramePlasma REMOVED: freegame fluorescent frame overlay was blamed
			for dashed cutlines; real dashes were baked into mirror_frame_wide.png
			lips (see tools/strip_frame_quilt_dashes.py). Do not remount. -->

		<WinDim />
		<!-- green plasma liner burns around the linked symbols, above the dim -->
		<PlasmaLiner />
		<WinSweep />
		<CellSealOverlay />

		<!-- mega-win FX: padded-cell strobe + memory-glitch wipe (above board FX) -->
		<WinLightning />

		<!-- Shared skip bus: reel tap + Space → stopButtonClick (slam-stop +
			temp turbo). Win / FS panels / transition also listen on that bus. -->
		<TapToSkip />

		<!-- WAYS / WIN / FREE SPINS morphed into the ONE reel-frame top rail
			(never a second overlapping side panel) -->
		<FrameMorphHud />

		<UI>
			{#snippet gameName()}
				<UiGameName name="THE WHITE ROOM" />
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
		<FreeSpinOutro />
		<!-- mounted after the free-spin panels so the level banner is never
			covered by their dim/plate layers -->
		<BonusLevelBanner />
		<!-- "+N SPINS" award toast when free spins retrigger -->
		<RetriggerBanner />
		<Transition />
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
