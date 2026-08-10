export const INFINITY_MARK = '∞';

export const AUTO_SPINS_TEXT_OPTIONS = [
	'10',
	'25',
	'50',
	'75',
	'100',
	'250',
	'500',
	'1000',
	INFINITY_MARK,
] as const;
export type AutoSpinsText = (typeof AUTO_SPINS_TEXT_OPTIONS)[number];
export const AUTO_SPINS_TEXT_OPTION_MAP = {
	'10': 10,
	'25': 25,
	'50': 50,
	'75': 75,
	'100': 100,
	'250': 250,
	'500': 500,
	'1000': 1000,
	[INFINITY_MARK]: Infinity,
};

export const LOSS_LIMIT_TEXT_OPTIONS = ['5×', '10×', '25×', '50×', '100×', INFINITY_MARK] as const;
export type LossLimitText = (typeof LOSS_LIMIT_TEXT_OPTIONS)[number];
export const AUTO_SPINS_LOSS_LIMIT_MULTIPLIER_MAP = {
	'5×': 5,
	'10×': 10,
	'25×': 25,
	'50×': 50,
	'100×': 100,
	[INFINITY_MARK]: Infinity,
};

export const SINGLE_WIN_LIMIT_TEXT_OPTIONS = [
	'5×',
	'10×',
	'25×',
	'50×',
	'100×',
	INFINITY_MARK,
] as const;
export type SingleWinLimitText = (typeof SINGLE_WIN_LIMIT_TEXT_OPTIONS)[number];
export const AUTO_SPINS_SINGLE_WIN_LIMIT_MULTIPLIER_MAP = {
	'5×': 5,
	'10×': 10,
	'25×': 25,
	'50×': 50,
	'100×': 100,
	[INFINITY_MARK]: Infinity,
};

export type UIConfigMode = 'default' | 'replay';

export const stateUi = $state({
	autoSpinsText: '10' as AutoSpinsText,
	autoSpinsLossLimitText: INFINITY_MARK as LossLimitText,
	autoSpinsSingleWinLimitText: INFINITY_MARK as SingleWinLimitText,
	freeSpinCounterShow: false,
	freeSpinCounterCurrent: 0,
	freeSpinCounterTotal: 0,
	menuOpen: false,
	drawerFold: false,
	drawerButtonShow: false,
	// Outer width of the reel frame, in the game's main-layout design px, as
	// published by the game (e.g. BoardFrame). 0 = not published yet. The HUD
	// layouts read this to fit the bottom control row to the frame's width so
	// they always line up at any screen size. Kept here (shared UI state) so the
	// shared components-ui-pixi layouts can consume it without importing the app.
	boardFrameWidth: 0,
	// Top edge of the bottom control bar, in canvas px, as published by whichever
	// HUD layout is mounted. 0 = not published (or the mounted layout has no
	// bottom bar). A game that draws its own furniture under the board reads
	// this to keep clear of the controls: the HUD is laid out in the STANDARD
	// design box and the game in its own, the two scale to the window
	// independently, so canvas px is the only space both can agree on.
	hudBarTopScreenY: 0,
	config: {
		mode: 'default' as UIConfigMode,
	}
});
