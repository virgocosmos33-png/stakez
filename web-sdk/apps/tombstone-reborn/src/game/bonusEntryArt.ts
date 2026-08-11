/**
 * Tombstone Reborn BONUS-ENTRY BANNER contract.
 *
 * TWO tiers, because the math has exactly two buy modes (betModeMeta.ts /
 * math-sdk game_config.py) and both are a SINGLE enhanced spin:
 *
 *   bonus_small   80x    DEAD MAN'S HAND   the six-card special bar is awake
 *   bonus_super  1000x   OPEN GRAVE        the bar plus the sealed grave lane
 *
 * The names are the mechanic, not decoration. The small buy wakes the six-card
 * special bar — a dealt hand — and the super buy additionally cracks open the
 * sealed grave cell on the last reel. Both read as siblings to the win ladder
 * (BOUNTY / SHOWDOWN / HIGH NOON / LAST STAND / BLOOD MONEY / BOOT HILL) and
 * neither implies a run of free spins, which this game does not have.
 *
 * ART REUSE, deliberately: the plates and both frames are baked by
 * tools/make_bonus_entry_art.py, but every light shape and particle comes from
 * the win ladder's already-shipped `winCelebLight` / `winCelebVfx` atlases. There
 * is no second VFX system here — see winCelebrationArt.ts for the frame-order
 * contract.
 *
 * WHY THE BANNER HAS ITS OWN FRAMES: the SMALL tier used to wear the win ladder's
 * `winFrame`. The win takeover was then asked to drop the thin outline tracing its
 * panel — its gold inlay hairline, iron edge line, strap outlines and nail rims
 * are gone and the panel edge is carried by light alone — while the banner was
 * asked to keep its framing exactly as it is. Sharing `winFrame` would have
 * silently stripped the banner too, so the banner owns `bonusFrameSmall`, which is
 * that outlined build kept intact.
 *
 * Nothing in this file goes near 0xf4f1ec: the cloned game's near-white glow is
 * the single most complained-about survivor, so the palette is imported from the
 * celebration's warm gold / iron set rather than redeclared.
 */
import { WIN_PALETTE } from './winCelebrationArt';

export const BONUS_ENTRY_SMALL_ASSET = 'bonusEntrySmall';
export const BONUS_ENTRY_SUPER_ASSET = 'bonusEntrySuper';
export const BONUS_FRAME_SMALL_ASSET = 'bonusFrameSmall';
export const BONUS_FRAME_SUPER_ASSET = 'bonusFrameSuper';

/** Bet mode keys that open a banner. Matches betModeMeta.ts exactly. */
export const BONUS_ENTRY_MODES = ['bonus_small', 'bonus_super'] as const;
export type BonusEntryTier = (typeof BONUS_ENTRY_MODES)[number];

export type BonusEntryArt = {
	/** hero title, on the branded-iron plate */
	title: string;
	/** the mechanic, in one line. Never implies more than one spin. */
	subtitle: string;
	/** hero plate asset key */
	plateKey: string;
	/** frame asset key */
	frameKey: string;
	/**
	 * Uniform timber/iron band around the 1280x720 hero window, as a fraction of
	 * the plate width — the frames are baked at different pad thicknesses
	 * (bonus_frame_small 74px, bonus_frame_super 112px), and the banner needs it
	 * to keep the frame window aligned to the plate at any scale.
	 */
	framePadFrac: number;
	/** god-ray shafts behind the frame */
	rays: number;
	rayAlpha: number;
	/** rising gold embers over the canvas */
	embers: number;
	/** drifting grave dust across the plate */
	dust: number;
	/** entry starburst scale, in frame widths */
	popScale: number;
	/** radiating spark streaks on entry */
	streaks: number;
	/** screen kick on entry, in pixels */
	kick: number;
	/** slow Ken-Burns push over the banner's dwell */
	push: number;
	/** expanding gold rings per second (0 = none) — SUPER only */
	rings: number;
	/** muzzle flares raking in from the sides on entry — SUPER only */
	flares: number;
	/** how long the banner holds before it hands off, in ms (pre-turbo) */
	holdMs: number;
};

/**
 * SUPER is escalated on every lever at once, so it is physically bigger on
 * screen rather than the same frame with a different word: a heavier frame, more
 * than double the god-rays and embers, three times the dust, a starburst twice
 * the size, expanding gold rings, muzzle flares raking in, three times the kick
 * and a longer hold.
 */
export const BONUS_ENTRY_ART: Record<BonusEntryTier, BonusEntryArt> = {
	bonus_small: {
		title: "DEAD MAN'S HAND",
		subtitle: 'ONE SPIN · THE BAR IS AWAKE',
		plateKey: BONUS_ENTRY_SMALL_ASSET,
		frameKey: BONUS_FRAME_SMALL_ASSET,
		framePadFrac: 74 / 1280,
		rays: 4,
		rayAlpha: 0.24,
		embers: 20,
		dust: 2,
		popScale: 0.52,
		streaks: 8,
		kick: 8,
		push: 1.06,
		rings: 0,
		flares: 0,
		holdMs: 2200,
	},
	bonus_super: {
		title: 'OPEN GRAVE',
		subtitle: 'ONE SPIN · THE LANE IS OPEN',
		plateKey: BONUS_ENTRY_SUPER_ASSET,
		frameKey: BONUS_FRAME_SUPER_ASSET,
		framePadFrac: 112 / 1280,
		rays: 10,
		rayAlpha: 0.52,
		embers: 62,
		dust: 6,
		popScale: 1.15,
		streaks: 22,
		kick: 24,
		push: 1.12,
		rings: 0.7,
		flares: 2,
		holdMs: 3000,
	},
};

/** The banner's ink and plate colours — the celebration's, not a second set. */
export const BONUS_PALETTE = WIN_PALETTE;

/** Is this bet mode key one that opens a banner? Case-insensitive, because
 * stateBet.activeBetModeKey is set from several places (buy confirm, resume,
 * replay URL) and is not consistently cased. */
export const bonusEntryTierOf = (betModeKey: string): BonusEntryTier | null => {
	const key = betModeKey.toLowerCase();
	return (BONUS_ENTRY_MODES as readonly string[]).includes(key)
		? (key as BonusEntryTier)
		: null;
};
