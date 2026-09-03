<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { Container } from 'pixi-svelte';
	import type { Filter } from 'pixi.js';

	import CellClipMask from './CellClipMask.svelte';
	import HighPayBg from './HighPayBg.svelte';
	import LowLinkDrip from './LowLinkDrip.svelte';
	import LowPayBg from './LowPayBg.svelte';
	import Symbol from './Symbol.svelte';
	import SymbolWrap from './SymbolWrap.svelte';
	import { getContext } from '../game/context';
	import {
		getCardHeight,
		getCellCenterY,
		getReelPocket,
		getReelYOffset,
		getSymbolInfo,
		getSymbolX,
	} from '../game/utils';
	import {
		isNudgeBumping,
		isNudgeCoveredCell,
		isNudgeSliding,
		isWildFlipCovered,
	} from '../game/boardCells';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { createGlassDentFilter } from '../game/glassDentFilter';
	import {
		CRUSH_IN_MS,
		CRUSH_OUT_MS,
		DENT_PUNCH_MS,
		DENT_RESIDUAL,
		DENT_SETTLE_MS,
		SPINNER_KNOCK_MS,
		SPINNER_KNOCK_OUT_MS,
		SPINNER_SPIN_MS,
		SPINNER_WOBBLE_DELAY_MS,
		SPINNER_WOBBLE_MS,
		isHighPaySymbol,
		isLowPaySymbol,
		usesHighPayPlate,
		isSpinnerBack,
		spinnerFaceScale,
		spinnerKnockOffset,
		spinnerSpinTo,
		spinnerYaw,
		spinnerYawSign,
	} from '../game/gunsmokeSpin';
	import type { ReelSymbol } from '../game/stateGame.svelte';
	import type { SymbolName } from '../game/types';

	type Props = {
		reelIndex: number;
		row: number;
		reelSymbol: ReelSymbol;
	};

	const props: Props = $props();
	const context = getContext();
	const symbolInfo = $derived(
		getSymbolInfo({ rawSymbol: props.reelSymbol.rawSymbol, state: props.reelSymbol.symbolState }),
	);
	const reelSpinning = $derived(props.reelSymbol.symbolState === 'spin');
	const covered = $derived(isNudgeCoveredCell(props.reelIndex, props.row));
	const sliding = $derived(isNudgeSliding(props.reelIndex, props.row));
	const bumping = $derived(isNudgeBumping(props.reelIndex, props.row));
	const lastReel = context.stateGame.board.length - 1;
	const laneShut = $derived(props.reelIndex === lastReel && !context.stateGame.lidOpen);
	const hide = $derived(
		(covered && !sliding) ||
			laneShut ||
			(props.reelSymbol.rawSymbol.name === 'NW' && !reelSpinning && !sliding) ||
			isWildFlipCovered(props.reelIndex, props.row),
	);
	const shoveY = $derived.by(() => {
		const push = context.stateGame.nudgePush[props.reelIndex];
		const t = push?.t.current ?? 0;
		if (sliding) {
			const pocket = getReelPocket(props.reelIndex);
			const seat = getCellCenterY(props.reelIndex, props.row);
			return t * (pocket.bottom + pocket.cardH - seat);
		}
		if (bumping) return Math.sin(t * Math.PI) * getReelPocket(props.reelIndex).cardH * 0.4;
		return 0;
	});
	const laneSwap = $derived(
		props.reelIndex === lastReel && props.row === 1 ? context.stateGame.laneCardSwap : 0,
	);
	const pocketH = $derived(getCardHeight(props.reelIndex));
	let holdFrom = $state<ReelSymbol['rawSymbol']['name'] | null>(null);
	let revealed = $state(false);
	const shownName = $derived(
		holdFrom && !revealed ? holdFrom : props.reelSymbol.rawSymbol.name,
	);
	const highPay = $derived(isHighPaySymbol(shownName));
	const breathing = $derived(
		highPay && symbolInfo.type === 'spine' && props.reelSymbol.symbolState === 'postWin',
	);
	const lifting = $derived(
		symbolInfo.type === 'spine' &&
			(props.reelSymbol.symbolState === 'land' ||
				props.reelSymbol.symbolState === 'win' ||
				breathing),
	);
	/** Idle high-pay spines use the hat-open T-mask. BoardBase's static
	 *  column clip is card-wide and would still shear the brim, so they
	 *  sit on the unmasked animate layer. Spin sprites stay pocket-clipped. */
	const shownInfo = $derived(
		getSymbolInfo({
			rawSymbol: { ...props.reelSymbol.rawSymbol, name: shownName },
			state: props.reelSymbol.symbolState,
		}),
	);
	const hatOut = $derived(highPay && shownInfo.type === 'spine');

	const NO_FILTERS: Filter[] = [];
	type Dent = ReturnType<typeof createGlassDentFilter>;
	let dent = $state<Dent | null>(null);
	let dentOn = $state(false);
	const dentAmt = new Tween(0);
	const crush = new Tween(0);
	const spin = new Tween(0);
	const knock = new Tween(0);
	const wobble = new Tween(0);
	let knockDir = $state({ x: 0, y: 1 });
	let targetSpin = $state(false);
	const dentFilters = $derived(dentOn && dent ? [dent.filter] : NO_FILTERS);
	const crushX = $derived(1 + 0.1 * crush.current);
	const crushY = $derived(1 - 0.18 * crush.current);
	const yaw = $derived(spinnerYaw(spin.current, wobble.current));
	const face = $derived(spinnerFaceScale(yaw));
	const knockOff = $derived(spinnerKnockOffset(knockDir.x, knockDir.y, knock.current));

	$effect(() => {
		if (!dent) return;
		dent.uniforms.uStrength = dentAmt.current;
	});

	$effect(() => {
		if (!holdFrom || revealed || !targetSpin) return;
		if (isSpinnerBack(yaw)) revealed = true;
	});

	const ensureDent = () => {
		if (dent) return dent;
		dent = createGlassDentFilter();
		return dent;
	};

	const punchGlass = (hitX: number, hitY: number, seed: number) => {
		const live = ensureDent();
		live.uniforms.uHit[0] = hitX;
		live.uniforms.uHit[1] = hitY;
		live.uniforms.uSeed = seed;
		dentOn = true;
		void dentAmt.set(1, { duration: fxDur(DENT_PUNCH_MS), easing: backOut }).then(() => {
			void dentAmt.set(DENT_RESIDUAL, { duration: fxDur(DENT_SETTLE_MS), easing: cubicOut });
		});
		void crush.set(1, { duration: fxDur(CRUSH_IN_MS), easing: backOut }).then(() => {
			void crush.set(0, { duration: fxDur(CRUSH_OUT_MS), easing: cubicOut });
		});
	};

	const punchSpinner = (kx: number, ky: number) => {
		const len = Math.hypot(kx, ky) || 1;
		knockDir = { x: kx / len, y: ky / len };
		targetSpin = true;
		spin.set(0, { duration: 0 });
		knock.set(0, { duration: 0 });
		wobble.set(0, { duration: 0 });
		void knock.set(1, { duration: fxDur(SPINNER_KNOCK_MS), easing: backOut }).then(() => {
			void knock.set(0, { duration: fxDur(SPINNER_KNOCK_OUT_MS), easing: cubicOut });
		});
		void spin.set(spinnerYawSign(kx) * spinnerSpinTo, {
			duration: fxDur(SPINNER_SPIN_MS),
			easing: cubicOut,
		});
		void fxWait(SPINNER_WOBBLE_DELAY_MS).then(() =>
			wobble.set(1, { duration: fxDur(SPINNER_WOBBLE_MS), easing: cubicOut }).then(() => {
				targetSpin = false;
				spin.set(0, { duration: 0 });
				wobble.set(0, { duration: 0 });
			}),
		);
	};

	const clearDent = () => {
		dentOn = false;
		dentAmt.set(0, { duration: 0 });
		crush.set(0, { duration: 0 });
		spin.set(0, { duration: 0 });
		knock.set(0, { duration: 0 });
		wobble.set(0, { duration: 0 });
		targetSpin = false;
		holdFrom = null;
		revealed = false;
	};

	context.eventEmitter.subscribeOnMount({
		gunsmokeMorphHold: ({ reel, row, from }) => {
			if (reel !== props.reelIndex || row !== props.row) return;
			holdFrom = from;
			revealed = false;
		},
		gunsmokeCellDent: ({ reel, row, hitX, hitY, seed, knockX: kx, knockY: ky }) => {
			if (reel !== props.reelIndex || row !== props.row) return;
			punchGlass(hitX, hitY, seed);
			punchSpinner(kx ?? 0, ky ?? 1);
		},
		gunsmokeWoundsClear: () => clearDent(),
		featureFxFallOut: () => clearDent(),
	});

	$effect(() => {
		if (props.reelSymbol.symbolState !== 'spin') return;
		holdFrom = null;
		revealed = false;
	});

	const onSpinLayer = $derived(
		lifting || targetSpin || hatOut || holdFrom != null,
	);

	const finish = () => {
		if (props.reelSymbol.symbolState === 'win') props.reelSymbol.oncomplete();
		if (props.reelSymbol.symbolState === 'land') {
			props.reelSymbol.symbolState = 'static';
			props.reelSymbol.oncomplete();
		}
	};

	onDestroy(() => {
		dent?.filter.destroy();
		dent = null;
	});
</script>

<SymbolWrap
	reelIndex={props.reelIndex}
	x={getSymbolX(props.reelIndex)}
	y={props.reelSymbol.symbolY.current + getReelYOffset(props.reelIndex) + shoveY}
	stay={sliding || bumping}
	zIndex={sliding || targetSpin ? 5 : onSpinLayer ? 6 : 0}
	animating={onSpinLayer}
>
	<Container alpha={hide ? 0 : 1} blendMode="normal">
		<Container
			x={knockOff.x}
			y={knockOff.y}
			scale={{ x: crushX * face.x, y: crushY * face.y }}
			blendMode="normal"
		>
			{#if holdFrom}
				<Container alpha={revealed ? 0 : 1} eventMode="none">
					{@render card(holdFrom, isHighPaySymbol(holdFrom), 'static')}
				</Container>
				<Container alpha={revealed ? 1 : 0} eventMode="none">
					{@render card('W', false, props.reelSymbol.symbolState)}
				</Container>
			{:else}
				{@render card(shownName, hatOut, props.reelSymbol.symbolState)}
			{/if}
		</Container>
	</Container>
</SymbolWrap>

{#snippet card(name: SymbolName, openHat: boolean, state: ReelSymbol['symbolState'])}
	{#if usesHighPayPlate(name)}
		<HighPayBg reelIndex={props.reelIndex} />
	{:else if isLowPaySymbol(name)}
		<LowPayBg reelIndex={props.reelIndex} />
	{/if}
	<Container blendMode="normal">
		<CellClipMask reelIndex={props.reelIndex} {openHat} />
		<Container y={laneSwap * pocketH} filters={dentFilters}>
			<Symbol
				{state}
				rawSymbol={{ ...props.reelSymbol.rawSymbol, name }}
				oncomplete={finish}
			/>
			{#if isLowPaySymbol(name)}
				<LowLinkDrip reelIndex={props.reelIndex} row={props.row} />
			{/if}
		</Container>
	</Container>
{/snippet}
