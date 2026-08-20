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

	// Some games (e.g. White Room's Wild Reel) grow/shrink a reel's height at
	// runtime. Resize the reactive symbol array to match the incoming board
	// before rewriting it. For fixed-height games the lengths always match, so
	// neither branch runs and behaviour is unchanged.
	const resizeSymbolsTo = (length: number) => {
		if (length > reelState.symbols.length) {
			for (let symbolIndex = reelState.symbols.length; symbolIndex < length; symbolIndex++) {
				reelState.symbols.push(
					createReelSymbol({ rawSymbol: reelState.symbols[0]?.rawSymbol, symbolIndex }),
				);
			}
		} else if (length < reelState.symbols.length) {
			reelState.symbols.splice(length);
		}
	};

	const updateSymbols = (value: TRawSymbol[]) => {
		resizeSymbolsTo(value.length);
		return reelState.symbols.map((reelSymbol, symbolIndex) => {
			reelSymbol.rawSymbol = value[symbolIndex];
			reelSymbol.symbolState = 'static' as TSymbolState;
			// Growing/shrinking reuses ReelSymbol objects; snap every row back to
			// its rest Y so a longer strip never leaves a cell parked off-window.
			const restY = getSymbolY(symbolIndex - 1);
			if (reelSymbol.symbolY.current !== restY) {
				reelSymbol.symbolY.set(restY, { duration: 0 });
			}
		});
	};

	// Restore the reel to its authored height (used before a fresh spin so a
	// previously grown reel starts clean). No-op for fixed-height reels.
	const resetToInitialHeight = () => {
		if (reelState.symbols.length === reelOptions.initialSymbols.length) return;
		resizeSymbolsTo(reelOptions.initialSymbols.length);
		reelState.symbols.forEach((reelSymbol, symbolIndex) => {
			reelSymbol.rawSymbol = reelOptions.initialSymbols[symbolIndex];
			reelSymbol.symbolState = reelOptions.initialSymbolState;
		});
	};

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
		// a slam-stop can jump a reel straight from fallingOut to stopped,
		// skipping 'hanging' - the readyToSpin gate must fire in that case too
		// or the reveal spin waits forever (frozen round, dead HUD)
		slammed: false,
		readyToSpin: () => {},
		spinOptions: () => ({}) as CascadingReelSpinOptions,
	});
	// One reel-step, not this reel's symbol count. Accumulating `length ×
	// multiplier` and then dividing by a short last reel (diamond / lane
	// boards) used to inflate that column's hang. Equal-height boards keep
	// the same cadence: delay = reelFallInDelay × (paddingSize - 1).
	const basePaddingSize = () => reelState.spinOptions().reelPaddingMultiplierNormal;
	const anticipatedPaddingSize = () =>
		reelState.spinOptions().reelPaddingMultiplierAnticipated;

	// internal states
	let targetSymbols = reelOptions.initialSymbols;
	let onSpinFinishing: () => void = () => {};
	let noStop = false;
	let paddingSize = 0;
	let slamStop = false;

	// A slam must cut an ALREADY-RUNNING symbol tween, not just the gaps between
	// them. Svelte's Tween.set() resolves only when the tween finishes (aborting
	// it never resolves the promise), and interruptible.interrupt() only releases
	// the hang wait - so a reel caught mid-fall would otherwise keep animating to
	// completion while its neighbours snap. This signal is raced against every
	// blocking tween await; stop() resolves it, releasing all reels at once.
	let resolveSlamSignal: () => void = () => {};
	let slamSignal: Promise<void> = new Promise((resolve) => (resolveSlamSignal = resolve));
	const resetSlamSignal = () => {
		slamStop = false;
		reelState.slammed = false;
		slamSignal = new Promise((resolve) => (resolveSlamSignal = resolve));
	};
	// resolves as soon as EITHER the tween completes or a slam fires
	const raceSlam = (promise: Promise<unknown>) => Promise.race([promise, slamSignal]);

	// slamming DURING fall-out completes the fall-out instantly (symbols snap
	// off-board, reel ends 'hanging') instead of snapping the old board back
	// on. This keeps every reel in the same phase after a skip: they all sit
	// hanging and then drop the reveal board in together, rather than some
	// reels visibly falling out twice
	const slamFallOutToHanging = async () => {
		reelState.motion = 'hanging';

		await moveAllSymbolsWith(async (reelSymbol) => {
			const y = getSymbolY(reelSymbol.symbolIndexOfBoard + reelLength);
			await reelSymbol.symbolY.set(y, { duration: 0 });
		});
	};

	const slamToStopped = async () => {
		updateSymbols(targetSymbols);
		reelState.anticipating = false;
		reelState.motion = 'stopped';
		reelState.slammed = true;

		await moveAllSymbolsWith(async (reelSymbol) => {
			const y = getSymbolY(reelSymbol.symbolIndexOfBoard);
			reelSymbol.symbolState = 'static' as TSymbolState;
			await reelSymbol.symbolY.set(y, { duration: 0 });
		});
	};

	const delaySpinByReelIndex = async () => {
		// raced so a slam during the pre-spin stagger releases every reel at
		// once instead of each waiting out its own start delay
		await raceSlam(
			waitForTimeout(reelState.spinOptions().reelFallOutDelay * reelOptions.reelIndex),
		);
	};

	const preSpin = async ({
		isTurboBeforeAll,
	}: {
		isTurboBeforeAll: boolean; // To avoid previous spinType has effect on "getSpinOption" in "slideDownLoop"
	}) => {
		// a slam from the PREVIOUS round is stale - it must not cut this fresh
		// pre-spin short or leak through the readyToSpin gate
		resetSlamSignal();
		reelState.spinType = isTurboBeforeAll ? 'fast' : 'normal';
		if (!isTurboBeforeAll) await delaySpinByReelIndex();
		await fallOut();
	};

	const moveAllSymbolsWith = async (moveSymbol: (reelSymbol: ReelSymbol) => Promise<void>) => {
		await Promise.all(reelState.symbols.map(moveSymbol));
	};

	const fallOut = async () => {
		if (slamStop) {
			await slamFallOutToHanging();
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

			await raceSlam(waitForTimeout(delay));
			if (slamStop) return;
			reelSymbol.symbolState = 'spin' as TSymbolState;
			await raceSlam(reelSymbol.symbolY.set(newSymbolY, { duration }));
		});

		if (slamStop) {
			await slamFallOutToHanging();
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
		const fallInDelayMultiplier = paddingSize - 1;
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
			await raceSlam(
				reelSymbol.symbolY.set(newSymbolY - bounceDistance, {
					duration: landDuration,
					delay,
				}),
			);
			if (slamStop) return;
			reelSymbol.symbolState = 'land' as TSymbolState;
			reelOptions.onSymbolLand({ rawSymbol: reelSymbol.rawSymbol });
			if (reelSymbol.symbolIndexOfBoard === reelLengthInBoard - 1) {
				onSpinFinishing();
			}
			// the bounce must be raced too: the first reel lands (and bounces)
			// earliest, and moveAllSymbolsWith waits for EVERY symbol - an
			// un-raced bounce would keep that reel visibly animating while the
			// other reels (still in their fall-in wait) snap instantly
			await raceSlam(
				reelSymbol.symbolY.set(newSymbolY, {
					duration: bounceDuration,
					easing: backOut,
				}),
			);
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
			// a slam during fallOut leaves the reel 'hanging' (empty), NOT
			// finished - fall through so hanging()/fallIn() slam the final
			// board in, otherwise the reel would end the round blank
			await fallOut();
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
		resetSlamSignal();

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
		// release any in-flight symbol tween immediately (raceSlam), then the
		// hang wait (interruptible) - so every reel bails on the same frame
		resolveSlamSignal();
		interruptible.interrupt();
	};

	const readyToSpinEffect = () => {
		$effect(() => {
			// 'slammed' also releases the gate: a slam-stopped reel never reaches
			// 'hanging', and reading readyToSpin inside the branch keeps the
			// effect re-running when the reveal assigns its resolver late
			if (reelState.motion === 'hanging' || reelState.slammed) {
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
		resetToInitialHeight,
		readyToSpinEffect,
	};
}
