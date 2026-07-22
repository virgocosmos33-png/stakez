/**
 * Drama Studios HUD house style.
 *
 * Single source of truth for the look of every HUD button, plate and label
 * across ALL games built on this SDK. Keep it here (shared package) so a new
 * game inherits the same premium chrome automatically — like a real provider
 * house style.
 *
 * The look: dark glass bodies (top-lit vertical gradient) inside a thin
 * metallic bevel — a dark outer line, a brass/gold main edge and a bright
 * inner highlight. No flat translucent-black circles, no template greens.
 *
 * PER-GAME THEMING (safe, opt-in): every value below is a DEFAULT. A game may
 * override any subset at runtime by calling `setHudThemeOverrides({ ... })`
 * once at startup (see the `ways` app bootstrap, fed from the game-builder
 * config → `hud.generated.ts`). Games that never call the setter render with
 * the byte-identical defaults, so shared behaviour for other games is
 * unchanged. `HUD_THEME_DEFAULTS` keeps a frozen copy for reference/tests.
 */

const HUD_THEME_DEFAULTS = {
	// glass body gradient (top -> bottom)
	bodyTop: 0x353542,
	bodyBottom: 0x0a0a0e,
	bodyTopHover: 0x474756,
	bodyBottomHover: 0x121218,
	bodyTopPressed: 0x0c0c11,
	bodyBottomPressed: 0x24242e,
	bodyAlpha: 0.94,

	// metallic bevel — DARK STEEL/SLATE rims (no gold anywhere on the HUD).
	// (names kept as edgeGold* for call-site compat; values are steel/slate.)
	edgeDark: 0x000000,
	edgeGold: 0x3a4552,
	edgeGoldHover: 0x5a6672,
	innerHighlight: 0xf6e4a6,

	// accent (active state, key CTAs). Change per game if desired.
	accent: 0xffc12e,
	accentGlow: 0xffcf4d,

	// disabled
	disabledTop: 0x2a2a30,
	disabledBottom: 0x141418,
	disabledEdge: 0x55555f,
	disabledIcon: 0x6a6a70,

	// type
	fontDisplay: 'Cinzel, Georgia, serif',
	textPrimary: 0xf4ecd8,
	textSecondary: 0xb9b1c4,
	// shared HUD gold (matches WAYS/WIN/FREE-SPINS labels, marquee, action-pod rim)
	textValue: 0xf0e6d0,

	// --- Per-component tokens (previously hardcoded inside each component). ---
	// Tokenised so a game can theme them via setHudThemeOverrides(); defaults
	// equal the original inline literals so untouched games look identical.
	// SPIN coin (ButtonBet) + armed BuyBonus ring
	spinCoinBody: 0xf7bb0f,
	spinCoinRim: 0xffde6a,
	spinCoinRimHover: 0xffe98a,
	// TURBO lit bolt (ButtonTurbo)
	turboLit: 0xffb400,
	// control-bar / buy-bonus panel fill
	panelFill: 0x10161d,
	// control-bar panel outline / divider (steel-slate)
	panelStroke: 0x2a3542,
	// ± stepper button idle face (ControlInfoBar)
	stepperFill: 0x1c2732,
	// balance / bet value text (ControlInfoBar); defaults to the shared HUD gold
	balanceText: 0xf0e6d0,
	betText: 0xf0e6d0,
};

export type HudTheme = typeof HUD_THEME_DEFAULTS;

/** Frozen snapshot of the shipped defaults (for tests / reset). */
export const HUD_THEME_DEFAULTS_FROZEN: Readonly<HudTheme> = Object.freeze({ ...HUD_THEME_DEFAULTS });

/**
 * Live theme object every component reads from. Mutated IN PLACE by
 * `setHudThemeOverrides` so existing references stay valid. Starts as an exact
 * copy of the defaults.
 */
export const HUD_THEME: HudTheme = { ...HUD_THEME_DEFAULTS };

/**
 * Merge a partial set of overrides into the live HUD theme. No-op keys that
 * aren't real tokens are ignored. Call once at app startup BEFORE the HUD
 * first renders. Inert for any game that never calls it.
 */
export function setHudThemeOverrides(partial: Partial<HudTheme>): void {
	if (!partial) return;
	for (const key of Object.keys(HUD_THEME_DEFAULTS) as (keyof HudTheme)[]) {
		const value = partial[key];
		if (value === undefined || value === null) continue;
		// preserve the value type (number token vs font string)
		(HUD_THEME as Record<string, unknown>)[key] = value;
	}
}

/** Reset the live theme back to the shipped defaults (used by tests/Storybook). */
export function resetHudTheme(): void {
	Object.assign(HUD_THEME, HUD_THEME_DEFAULTS_FROZEN);
}
