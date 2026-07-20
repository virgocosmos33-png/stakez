/**
 * Drama Studios HUD house style.
 *
 * Single source of truth for the look of every HUD button, plate and label
 * across ALL games built on this SDK. Keep it here (shared package) so a new
 * game inherits the same premium chrome automatically — like a real provider
 * house style. Per-game theming is limited to the ACCENT hue below.
 *
 * The look: dark glass bodies (top-lit vertical gradient) inside a thin
 * metallic bevel — a dark outer line, a brass/gold main edge and a bright
 * inner highlight. No flat translucent-black circles, no template greens.
 */

export const HUD_THEME = {
	// glass body gradient (top -> bottom)
	bodyTop: 0x353542,
	bodyBottom: 0x0a0a0e,
	bodyTopHover: 0x474756,
	bodyBottomHover: 0x121218,
	bodyTopPressed: 0x0c0c11,
	bodyBottomPressed: 0x24242e,
	bodyAlpha: 0.94,

	// metallic bevel
	edgeDark: 0x000000,
	edgeGold: 0xc99a3f,
	edgeGoldHover: 0xe9c877,
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
	textValue: 0xffffff,
} as const;
