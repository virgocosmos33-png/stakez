import { backOut } from 'svelte/easing';
import { Tween } from 'svelte/motion';

import { stateBet } from 'state-shared';
import { waitForTimeout } from 'utils-shared/wait';
import { createInterruptible } from 'utils-shared/interruptible';

import type { CascadingReelCreateOptions, CascadingReelSpinOptions, SpinType } from './types';

export type CascadingReelMotion = 'fallingOut' | 'hanging' | 'fallingIn' | 'stopped';
export type CascadingReelSymbolState = 'static' | 'land' | 'spin';

export function createReelForCascading<TRawSymbol extends object, TSymbolState extends string>(
	reelOptions: CascadingReelCreateOptions<TRawSymbol, TSymbolState>,
) {
	// reelSymbols
	const getSymbolY = (symbolIndexOfBoard: number) =>
		(symbolIndexOfBoard + 0.5) * reelOptions.symbolHeight;

	const createReelSymbol = (reelSymbolOptions: { rawSymbol: TRawSymbol; symbolIndex: number }) => {
		const symbolIndexOfBoard = reelSymbolOptions.symbolIndex - 1;
		const rawSymbol = reelSymbolOptions.rawSymbol;
		const symbolState = reelOptions.initialSymbolState;

		const initY = getSymbolY(symbolIndexOfBoard);
		const symbolY = new Tween(initY);
		const oncomplete = () => {};

		const reelSymbol = $state({
			rawSymbol,
			symbolIndexOfBoard,
			symbolY,
			symbolState,
			oncomplete,
		});

		return reelSymbol;
	};

	type ReelSymbol = ReturnType<typeof createReelSymbol>;

	const createReelSymbols: (value: TRawSymbol[]) => ReelSymbol[] = (rawSymbols) => {
		const reelSymbols = rawSymbols.map((rawSymbol, symbolIndex) =>
			createReelSymbol({ rawSymbol, symbolIndex }),
		);

		return reelSymbols;
	};

	const updateSymbols = (value: TRawSymbol[]) =>
		reelState.symbols.map((reelSymbol, symbolIndex) => {
			reelSymbol.rawSymbol = value[symbolIndex];
			reelSymbol.symbolState = 'static' as TSymbolState;
		});

	// constants
	const reelLength = reelOptions.initialSymbols.length;
	const reelLengthInBoard = reelLength - 2;

	// interruptible
	const interruptible = createInterruptible();

	// reactive states
	const reelState = $state({
		symbols: createReelSymbols(reelOptions.initialSymbols),
		motion: 'stopped' as CascadingReelMotion,
		spinType: 'normal' as SpinType,
		anticipating: false,
		readyToSpin: () => {},
		spinOptions: () => ({}) as CascadingReelSpinOptions,
	});
	const basePaddingSize = () => reelLength * reelState.spinOptions().reelPaddingMultiplierNormal;
	const anticipatedPaddingSize = () =>
		reelLength * reelState.spinOptions().reelPaddingMultiplierAnticipated;

	// internal states
	let targetSymbols = reelOptions.initialSymbols;
	let onSpinFinishing: () => void = () => {};
	let noStop = false;
	let paddingSize = 0;
	let slamStop = false;

	const slamToStopped = async () => {
		updateSymbols(targetSymbols);
		reelState.anticipating = false;
		reelState.motion = 'stopped';

		await moveAllSymbolsWith(async (reelSymbol) => {
			const y = getSymbolY(reelSymbol.symbolIndexOfBoard);
			reelSymbol.symbolState = 'static' as TSymbolState;
			await reelSymbol.symbolY.set(y, { duration: 0 });
		});
	};

	const delaySpinByReelIndex = async () => {
		await waitForTimeout(reelState.spinOptions().reelFallOutDelay * reelOptions.reelIndex);
	};

	const preSpin = async ({
		isTurboBeforeAll,
	}: {
		isTurboBeforeAll: boolean; // To avoid previous spinType has effect on "getSpinOption" in "slideDownLoop"
	}) => {
		reelState.spinType = isTurboBeforeAll ? 'fast' : 'normal';
		if (!isTurboBeforeAll) await delaySpinByReelIndex();
		await fallOut();
	};

	const moveAllSymbolsWith = async (moveSymbol: (reelSymbol: ReelSymbol) => Promise<void>) => {
		await Promise.all(reelState.symbols.map(moveSymbol));
	};

	const fallOut = async () => {
		if (slamStop) {
			await slamToStopped();
			return;
		}

		reelState.motion = 'fallingOut';

		await moveAllSymbolsWith(async (reelSymbol) => {
			if (slamStop) return;

			const oldSymbolY = reelSymbol.symbolY.current;
			const newSymbolY = getSymbolY(reelSymbol.symbolIndexOfBoard + reelLength);
			const distance = newSymbolY - oldSymbolY;
			const duration = distance / reelState.spinOptions().symbolFallOutSpeed;
			const delay =
				reelState.spinOptions().symbolFallOutInterval *
				(reelLengthInBoard - reelSymbol.symbolIndexOfBoard);

			await waitForTimeout(delay);
			if (slamStop) return;
			reelSymbol.symbolState = 'spin' as TSymbolState;
			await reelSymbol.symbolY.set(newSymbolY, { duration });
		});

		if (slamStop) {
			await slamToStopped();
			return;
		}

		reelState.motion = 'hanging';
	};

	const hanging = async () => {
		if (slamStop) {
			await slamToStopped();
			return;
		}

		updateSymbols(targetSymbols);

		await moveAllSymbolsWith(async (reelSymbol) => {
			const newSymbolY = getSymbolY(reelSymbol.symbolIndexOfBoard - reelLength + 0.5);
			const duration = 0;

			await reelSymbol.symbolY.set(newSymbolY, { duration });
		});

		if (slamStop) {
			await slamToStopped();
		}
	};

	const fallIn = async () => {
		const fallInDelayMultiplier = paddingSize / reelLength - 1;
		const waitToStartFallingIn = async () =>
			await waitForTimeout(reelState.spinOptions().reelFallInDelay * fallInDelayMultiplier);

		// Slam-stop / turbo fast-forwards EVERYTHING, including anticipated
		// (scatter) reels. A tap or space toggles turbo on, so the hang is cut
		// instantly instead of forcing the player to watch it. Played normally
		// the hang still shows, but it stays interruptible on every reel so a
		// click can skip even the 2nd / 3rd scatter anticipation.
		if (stateBet.isTurbo) {
			// skip
		} else if (noStop) {
			await interruptible.add(waitToStartFallingIn);
		} else {
			await interruptible.add(waitToStartFallingIn);
		}

		if (slamStop) {
			await slamToStopped();
			return;
		}

		reelState.motion = 'fallingIn';

		await moveAllSymbolsWith(async (reelSymbol) => {
			if (slamStop) return;

			const oldSymbolY = reelSymbol.symbolY.current;
			const newSymbolY = getSymbolY(reelSymbol.symbolIndexOfBoard);
			const distance = newSymbolY - oldSymbolY;
			const delay =
				reelState.spinOptions().symbolFallInInterval *
				(reelLengthInBoard - reelSymbol.symbolIndexOfBoard);
			const bounceDistance =
				reelOptions.symbolHeight * reelState.spinOptions().symbolFallInBounceSizeMulti;
			const bounceDuration = bounceDistance / reelState.spinOptions().symbolFallInBounceSpeed;
			const landDuration = (distance - bounceDistance) / reelState.spinOptions().symbolFallInSpeed;

			// falling symbols show the 'spin' state (motion smear) until they
			// hit the row; they start above the board where they are culled,
			// so flipping the state before the delayed tween is invisible
			reelSymbol.symbolState = 'spin' as TSymbolState;
			await reelSymbol.symbolY.set(newSymbolY - bounceDistance, {
				duration: landDuration,
				delay,
			});
			if (slamStop) return;
			reelSymbol.symbolState = 'land' as TSymbolState;
			reelOptions.onSymbolLand({ rawSymbol: reelSymbol.rawSymbol });
			if (reelSymbol.symbolIndexOfBoard === reelLengthInBoard - 1) {
				onSpinFinishing();
			}
			await reelSymbol.symbolY.set(newSymbolY, {
				duration: bounceDuration,
				easing: backOut,
			});
		});

		if (slamStop) {
			await slamToStopped();
			return;
		}

		reelState.motion = 'stopped';
	};

	const generalSpin = async () => {
		const isHanging = reelState.motion === 'hanging';

		if (!isHanging) {
			await fallOut();
			if (slamStop) return;
		}
		await hanging();
		if (slamStop) return;
		await fallIn();
	};

	// Keep redundancy here for the comparison to createSpinningReel
	const fastSpin = () => generalSpin();
	const normalSpin = () => generalSpin();
	const anticipatedSpin = () => generalSpin();

	const SPIN_MAP = {
		fast: fastSpin,
		normal: normalSpin,
		anticipated: anticipatedSpin,
	};

	const prepareToSpin = (prepareToSpinOptions: {
		noStop: boolean;
		spinType: SpinType;
		symbols: TRawSymbol[];
		paddingPosition: number;
		onSpinFinishing: () => void;
		previousPaddingSize: number;
	}) => {
		reelState.spinType = prepareToSpinOptions.spinType;
		slamStop = false;

		noStop = prepareToSpinOptions.noStop;
		targetSymbols = prepareToSpinOptions.symbols;
		onSpinFinishing = prepareToSpinOptions.onSpinFinishing;

		const GET_PADDING_SIZE_MAP = {
			fast: 0,
			normal: prepareToSpinOptions.previousPaddingSize + basePaddingSize(),
			anticipated: prepareToSpinOptions.previousPaddingSize + anticipatedPaddingSize(),
		};

		paddingSize = GET_PADDING_SIZE_MAP[prepareToSpinOptions.spinType];

		return paddingSize;
	};

	const spin = async () => {
		await SPIN_MAP[reelState.spinType]();
	};

	const setSymbolsWithRawSymbols = (value?: TRawSymbol[]) => {
		reelState.motion = 'stopped';
		if (value) {
			updateSymbols(value);
		}
	};

	const stop = () => {
		slamStop = true;
		reelState.spinType = 'fast';
		interruptible.interrupt();
	};

	const readyToSpinEffect = () => {
		$effect(() => {
			if (reelState.motion === 'hanging') {
				reelState.readyToSpin();
			}
		});
	};

	return {
		// from options
		reelIndex: reelOptions.reelIndex,
		symbolHeight: reelOptions.symbolHeight,
		onReelStopping: reelOptions.onReelStopping,
		reelLength,
		// reactive states
		reelState,
		// methods
		preSpin,
		prepareToSpin,
		spin,
		stop,
		setSymbolsWithRawSymbols,
		readyToSpinEffect,
	};
}
