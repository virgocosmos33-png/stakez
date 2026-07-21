import type { BaseBet } from 'utils-bet';
import { stateMeta } from './stateMeta.svelte';

export type Currency = string;
export type BetToResume = BaseBet | null;
export type BetModeKey = string;

export const stateBet = $state({
	currency: 'USD' as Currency,
	balanceAmount: 0,
	betAmount: 1,
	wageredBetAmount: 1,
	betToResume: null as BetToResume,
	activeBetModeKey: 'BASE' as BetModeKey,
	winBookEventAmount: 0,
	autoSpinsLoss: 0,
	autoSpinsCounter: 0,
	autoSpinsLossLimitAmount: Infinity,
	autoSpinsSingleWinLimitAmount: Infinity,
	isSpaceHold: false,
	isTurbo: false,
	// second turbo tier ("super turbo"). isTurbo stays the master "turbo engaged"
	// flag (skip/fast-spin logic reads it); isSuperTurbo only bumps the speed.
	isSuperTurbo: false,
});

const correctBetAmount = (value: number) => {
	if (value <= 0) return 0;
	const costMultiplier = betCostMultiplier();
	if (costMultiplier === 0) return 0;
	const max = stateBet.balanceAmount / costMultiplier;
	if (value >= max) return max;
	return value;
};

const setBetAmount = (value: number) => {
	stateBet.betAmount = correctBetAmount(value);
};

const updateBetAmount = (update: (value: number) => number) => {
	stateBet.betAmount = correctBetAmount(update(stateBet.betAmount));
};

let isTurboLocked = false;

const updateIsTurbo = (value: boolean, options: { persistent: boolean }) => {
	const { persistent } = options;

	if (!persistent && isTurboLocked) return;
	if (persistent) isTurboLocked = value;

	stateBet.isTurbo = value;
	// a transient slam-stop never engages the super tier; only the button does
	if (!value) stateBet.isSuperTurbo = false;
};

// turbo button cycle: OFF -> TURBO -> SUPER TURBO -> OFF
const cycleTurbo = () => {
	if (stateBet.isSuperTurbo) {
		stateBet.isTurbo = false;
		stateBet.isSuperTurbo = false;
		isTurboLocked = false;
	} else if (stateBet.isTurbo) {
		stateBet.isSuperTurbo = true;
		isTurboLocked = true;
	} else {
		stateBet.isTurbo = true;
		isTurboLocked = true;
	}
};

// 0 = off, 1 = turbo, 2 = super turbo (drives the two-bolt button display)
const turboLevel = () => (stateBet.isSuperTurbo ? 2 : stateBet.isTurbo ? 1 : 0);

const activeBetMode = () => stateMeta.betModeMeta?.[stateBet.activeBetModeKey.toUpperCase()]
	?? stateMeta.betModeMeta?.[stateBet.activeBetModeKey.toLowerCase()]
	?? null;
const isContinuousBet = () => stateBet.autoSpinsCounter > 1 || stateBet.isSpaceHold;
// Two turbo tiers (both fast-forward every tween/spine/count-up that reads
// timeScale). Turbo = a bit faster; super turbo = full hacksaw-near-instant.
const timeScale = () => {
	if (stateBet.isSuperTurbo) return 2.5;
	if (stateBet.isTurbo) return 1.75;
	return 1;
};
const betCostMultiplier = () =>
	stateBetDerived.activeBetMode().type === 'activate'
		? stateBetDerived.activeBetMode().costMultiplier
		: 1;
const betCost = () => stateBet.betAmount * betCostMultiplier();
const isBetCostAvailable = () => betCost() > 0 && betCost() <= stateBet.balanceAmount;
const hasAutoBetCounter = () => stateBet.autoSpinsCounter !== 0;

export const stateBetDerived = {
	setBetAmount,
	updateBetAmount,
	updateIsTurbo,
	cycleTurbo,
	turboLevel,
	activeBetMode,
	isContinuousBet,
	timeScale,
	betCost,
	isBetCostAvailable,
	hasAutoBetCounter,
};
