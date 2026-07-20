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
	const balW = 260;
	const betW = 78;
	const chevW = 28;
	const dividerX = PAD + balW + 10;
	const betX = dividerX + 12;
	const chevX = betX + betW + 2;

	const FONT = 'Segoe UI, Arial, sans-serif';
	const labelStyle = {
		fontFamily: FONT,
		fontWeight: '700',
		fontSize: 16,
		fill: 0x8b96a3,
		letterSpacing: 1.1,
	} as const;
	const valueStyle = {
		fontFamily: FONT,
		fontWeight: '700',
		fontSize: 26,
		fill: 0xffffff,
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
		g.stroke({ color: 0x2a3542, width: 1.25 });
	};
	const drawDivider = (g: PIXI.Graphics) => {
		g.roundRect(-1, 0, 2, H - 18, 1);
		g.fill({ color: 0x2a3542 });
	};
	const drawUnderline = (g: PIXI.Graphics) => {
		g.roundRect(0, 0, 16, 2, 1);
		g.fill({ color: 0x5a6672 });
	};
	const drawChevron = (g: PIXI.Graphics, up: boolean, off: boolean) => {
		const s = 9;
		const tip = up ? -s * 0.45 : s * 0.45;
		const base = up ? s * 0.4 : -s * 0.4;
		g.moveTo(-s, base);
		g.lineTo(0, tip);
		g.lineTo(s, base);
		g.stroke({ color: 0xffffff, width: 3.5, cap: 'round', join: 'round', alpha: off ? 0.35 : 1 });
	};
</script>

<Graphics draw={drawPanel} />

<!-- BALANCE -->
<Text anchor={{ x: 0, y: 0.5 }} x={PAD} y={H * 0.34} text={balanceLabel} style={labelStyle} />
<Text anchor={{ x: 0, y: 0.5 }} x={PAD} y={H * 0.64} text={balanceValue} style={valueStyle} />

<Graphics x={dividerX} y={12} draw={drawDivider} />

<!-- BET (tap to open the bet menu) -->
<Container eventMode="static" cursor={isIdle ? 'pointer' : 'not-allowed'} onpointerup={openBetMenu}>
	<Rectangle x={betX} y={0} width={betW} height={H} backgroundColor={0xffffff} backgroundAlpha={0.001} />
	<Text anchor={{ x: 0, y: 0.5 }} x={betX} y={H * 0.32} text={betLabel} style={labelStyle} />
	<Text anchor={{ x: 0, y: 0.5 }} x={betX} y={H * 0.6} text={betValue} style={valueStyle} />
	<Graphics x={betX} y={H * 0.82} draw={drawUnderline} />
</Container>

<!-- ▲ increase -->
<Button
	x={chevX + chevW / 2}
	y={H * 0.32}
	sizes={{ width: chevW, height: H * 0.42 }}
	anchor={0.5}
	disabled={disabledUp}
	onpress={() => step(1)}
>
	{#snippet children({ center })}
		<Rectangle {...center} anchor={0.5} width={chevW} height={H * 0.42} backgroundColor={0xffffff} backgroundAlpha={0.001} />
		<Graphics {...center} draw={(g: PIXI.Graphics) => drawChevron(g, true, disabledUp)} />
	{/snippet}
</Button>

<!-- ▼ decrease -->
<Button
	x={chevX + chevW / 2}
	y={H * 0.68}
	sizes={{ width: chevW, height: H * 0.42 }}
	anchor={0.5}
	disabled={disabledDown}
	onpress={() => step(-1)}
>
	{#snippet children({ center })}
		<Rectangle {...center} anchor={0.5} width={chevW} height={H * 0.42} backgroundColor={0xffffff} backgroundAlpha={0.001} />
		<Graphics {...center} draw={(g: PIXI.Graphics) => drawChevron(g, false, disabledDown)} />
	{/snippet}
</Button>
