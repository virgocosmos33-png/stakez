import { setHudThemeOverrides } from 'components-ui-pixi';

import { hudColor } from './hud.generated';

let applied = false;

/**
 * Push this game's config-driven HUD colours (game-builder config →
 * hud.generated.ts) into the SHARED components-ui-pixi theme. Called once at
 * app startup before the HUD first renders.
 *
 * Cross-game safety: this is the ONLY place the setter is invoked. Other games
 * on the SDK never call it, so they keep the package's byte-identical defaults.
 * Each override falls back to the shipped default when a key is missing.
 */
export function applyHudTheme(): void {
	if (applied) return;
	applied = true;
	setHudThemeOverrides({
		accent: hudColor('accent', 0xffc12e),
		textValue: hudColor('text', 0xf0e6d0),
		spinCoinBody: hudColor('spinButton', 0xf7bb0f),
		turboLit: hudColor('turbo', 0xffb400),
		panelFill: hudColor('panelFill', 0x10161d),
		panelStroke: hudColor('panelStroke', 0x2a3542),
		stepperFill: hudColor('stepper', 0x1c2732),
		balanceText: hudColor('balanceText', 0xf0e6d0),
		betText: hudColor('betText', 0xf0e6d0),
	});
}
