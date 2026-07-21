<script lang="ts" module>
	// wide enough for full "$10,000,000.00" in the balance column; bet stays tight
	export const INFO_BAR_SIZE = { width: 500, height: 88 };
</script>

<script lang="ts">
	import * as PIXI from 'pixi.js';
	import { Container, Rectangle, Text, Graphics } from 'pixi-svelte';
	import { Button } from 'components-pixi';
	import { stateBet, stateBetDerived, stateConfig, stateModal } from 'state-shared';
	import { numberToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../context';
	import { i18nDerived } from '../i18n/i18nDerived';

	const context = getContext();

	const W = INFO_BAR_SIZE.width;
	const H = INFO_BAR_SIZE.height;
	const PAD = 20;
	// balance column — fits a 7-figure "$1,000,000.00" value comfortably
	const balW = 204;
	const dividerX = PAD + balW + 12;
	// bet label/value sits after the divider; the value grows rightward into a
	// fixed slot that ends well before the +/- stepper column (see minusCx).
	const betX = dividerX + 16;

	// −/+ stepper buttons pinned to the right edge, vertically centred. Their
	// left edge (minusCx - BTN_W/2) stays clear of the widest bet ("$1,000.00"),
	// so the glyphs can never overlap the amount.
	const BTN_W = 42;
	const BTN_H = 50;
	const BTN_GAP = 10;
	const RIGHT_PAD = 20;
	const plusCx = W - RIGHT_PAD - BTN_W / 2;
	const minusCx = plusCx - BTN_W - BTN_GAP;
	const btnCy = H / 2;

	// tap target over the BET label/value: starts just right of the divider and
	// ends a clear 8px before the − button's left edge, so it never overlaps the
	// steppers (nor the balance column to its left).
	const betHitX = dividerX + 6;
	const betHitW = minusCx - BTN_W / 2 - 8 - betHitX;

	// HUD label parchment-cream for TEXT fills — legible on the dark panel
	// (NOT white, NOT gold).
	const HUD_GOLD = 0xf0e6d0;
	// Dark STEEL/SLATE-BLUE for ALL OUTLINES/RIMS/BORDERS. No gold on the HUD.
	const STEEL = 0x3a4552;
	const STEEL_HOVER = 0x5a6672;
	const STEEL_DIM = 0x2a3542;

	const FONT = 'Segoe UI, Arial, sans-serif';
	const labelStyle = {
		fontFamily: FONT,
		fontWeight: '700',
		fontSize: 16,
		fill: HUD_GOLD,
		letterSpacing: 1.1,
	} as const;
	const valueStyle = {
		fontFamily: FONT,
		fontWeight: '700',
		fontSize: 26,
		fill: HUD_GOLD,
		letterSpacing: 0.3,
	} as const;

	const balanceLabel = $derived(i18nDerived.balance().toUpperCase());
	const balanceValue = $derived(numberToCurrencyString(stateBet.balanceAmount));
	const betLabel = $derived(
		(stateBetDerived.activeBetMode()?.text.betAmountLabel || i18nDerived.bet()).toUpperCase(),
	);
	const betValue = $derived(numberToCurrencyString(stateBetDerived.betCost()));

	const isIdle = $derived(context.stateXstateDerived.isIdle());
	const biggest = $derived(stateConfig.betAmountOptions[stateConfig.betAmountOptions.length - 1]);
	const smallest = $derived(stateConfig.betAmountOptions[0]);
	const disabledUp = $derived(!isIdle || stateBet.betAmount >= biggest);
	const disabledDown = $derived(!isIdle || stateBet.betAmount <= smallest);

	const step = (dir: 1 | -1) => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		const sorted = [...stateConfig.betAmountOptions].sort((a, b) => (dir === 1 ? a - b : b - a));
		const next = sorted.find((o) => (dir === 1 ? o > stateBet.betAmount : o < stateBet.betAmount));
		stateBetDerived.setBetAmount(next ?? (dir === 1 ? biggest : smallest));
	};

	const openBetMenu = () => {
		if (!isIdle) return;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateModal.modal = { name: 'betAmountMenu' };
	};

	const drawPanel = (g: PIXI.Graphics) => {
		g.roundRect(0, 0, W, H, 11);
		g.fill({ color: 0x10161d, alpha: 1 });
		g.roundRect(0.75, 0.75, W - 1.5, H - 1.5, 10);
		g.stroke({ color: STEEL_DIM, width: 1.25 });
	};
	const drawDivider = (g: PIXI.Graphics) => {
		g.roundRect(-1, 0, 2, H - 18, 1);
		g.fill({ color: STEEL_DIM, alpha: 0.6 });
	};

	// raised stepper-button chrome, tuned to the mono panel (fill 0x10161d)
	const drawStepFace = (g: PIXI.Graphics, hovered: boolean, pressed: boolean, off: boolean) => {
		const fill = off ? 0x141b23 : pressed ? 0x0d131a : hovered ? 0x28374a : 0x1c2732;
		const border = off ? STEEL_DIM : hovered ? STEEL_HOVER : STEEL;
		g.roundRect(-BTN_W / 2, -BTN_H / 2, BTN_W, BTN_H, 10);
		g.fill({ color: fill });
		g.roundRect(-BTN_W / 2 + 0.75, -BTN_H / 2 + 0.75, BTN_W - 1.5, BTN_H - 1.5, 9.25);
		g.stroke({ color: border, width: 1.25 });
	};
	const GLYPH = 10;
	const GLYPH_TH = 3.6;
	const drawMinus = (g: PIXI.Graphics, off: boolean) => {
		g.roundRect(-GLYPH, -GLYPH_TH / 2, GLYPH * 2, GLYPH_TH, GLYPH_TH / 2);
		g.fill({ color: HUD_GOLD, alpha: off ? 0.3 : 1 });
	};
	const drawPlus = (g: PIXI.Graphics, off: boolean) => {
		g.roundRect(-GLYPH, -GLYPH_TH / 2, GLYPH * 2, GLYPH_TH, GLYPH_TH / 2);
		g.roundRect(-GLYPH_TH / 2, -GLYPH, GLYPH_TH, GLYPH * 2, GLYPH_TH / 2);
		g.fill({ color: HUD_GOLD, alpha: off ? 0.3 : 1 });
	};
</script>

<Graphics draw={drawPanel} />

<!-- BALANCE -->
<Text anchor={{ x: 0, y: 0.5 }} x={PAD} y={H * 0.34} text={balanceLabel} style={labelStyle} />
<Text anchor={{ x: 0, y: 0.5 }} x={PAD} y={H * 0.64} text={balanceValue} style={valueStyle} />

<Graphics x={dividerX} y={12} draw={drawDivider} />

<!-- BET (tap the amount to open the bet menu; the −/+ buttons only step it) -->
<Container eventMode="static" cursor={isIdle ? 'pointer' : 'not-allowed'} onpointerup={openBetMenu}>
	<Rectangle x={betHitX} y={0} width={betHitW} height={H} backgroundColor={0xffffff} backgroundAlpha={0.001} />
	<Text anchor={{ x: 0, y: 0.5 }} x={betX} y={H * 0.32} text={betLabel} style={labelStyle} />
	<Text anchor={{ x: 0, y: 0.5 }} x={betX} y={H * 0.6} text={betValue} style={valueStyle} />
</Container>

<!-- − decrease -->
<Button
	x={minusCx}
	y={btnCy}
	sizes={{ width: BTN_W, height: BTN_H }}
	anchor={0.5}
	disabled={disabledDown}
	onpress={() => step(-1)}
>
	{#snippet children({ center, hovered, pressed })}
		<Rectangle {...center} anchor={0.5} width={BTN_W} height={BTN_H} backgroundColor={0xffffff} backgroundAlpha={0.001} />
		<Graphics {...center} draw={(g: PIXI.Graphics) => drawStepFace(g, hovered, pressed, disabledDown)} />
		<Graphics {...center} draw={(g: PIXI.Graphics) => drawMinus(g, disabledDown)} />
	{/snippet}
</Button>

<!-- + increase -->
<Button
	x={plusCx}
	y={btnCy}
	sizes={{ width: BTN_W, height: BTN_H }}
	anchor={0.5}
	disabled={disabledUp}
	onpress={() => step(1)}
>
	{#snippet children({ center, hovered, pressed })}
		<Rectangle {...center} anchor={0.5} width={BTN_W} height={BTN_H} backgroundColor={0xffffff} backgroundAlpha={0.001} />
		<Graphics {...center} draw={(g: PIXI.Graphics) => drawStepFace(g, hovered, pressed, disabledUp)} />
		<Graphics {...center} draw={(g: PIXI.Graphics) => drawPlus(g, disabledUp)} />
	{/snippet}
</Button>
