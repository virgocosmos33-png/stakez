/**
 * Player-facing win / outro / celebration amount typography.
 * Source of truth: config.fx.winAmountFont → fx.generated.ts (panel FX tab + DramaStudioMCP).
 *
 * Per-game rule: every game ships its OWN bitmap face. Do NOT default to shared
 * template fonts (silver = Mining-Mayhem western slab, gold/amethyst/ghost = Madam drip).
 */
import { SYMBOL_SIZE } from './constants';
import { fxColors, fxNum, fxStr } from './fx.generated';

const FALLBACK_FAMILY = 'clinical';
const FALLBACK_TINT = 0xf4f1ec;

export function winFontFamily(): string {
	return fxStr('winAmountFont', 'fontFamily', FALLBACK_FAMILY);
}

export function winFontTint(): number {
	return fxColors('winAmountFont', 'colors', [FALLBACK_TINT])[0] ?? FALLBACK_TINT;
}

export function winFontSize(scale = 1): number {
	return SYMBOL_SIZE * scale * fxNum('winAmountFont', 'fontSizeScale', 1);
}

export function winFontStyle(opts: {
	fontSize: number;
	align?: 'left' | 'center' | 'right';
	fontWeight?: string;
	letterSpacing?: number;
}) {
	return {
		fontFamily: winFontFamily(),
		fontSize: opts.fontSize,
		align: opts.align ?? 'center',
		fontWeight: opts.fontWeight ?? 'bold',
		letterSpacing: opts.letterSpacing ?? 0,
	};
}
