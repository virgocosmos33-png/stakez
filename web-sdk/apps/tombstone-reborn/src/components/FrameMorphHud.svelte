<script lang="ts" module>
	export type EmitterEventFrameMorphHud =
		| { type: 'waysCounterUpdate'; ways: number }
		| { type: 'waysCounterHide' }
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	/**
	 * Bottom of the reel frame: a CLINICAL STEEL CONSOLE with three recessed
	 * glass readouts (WAYS | FREE SPINS / info marquee | WIN).
	 *
	 * Drawn procedurally in Pixi (no baked PNG) so it stays razor-sharp at any
	 * size and shares the board cages' dark-steel material instead of the old
	 * white padded-quilt photo. A thin blood-red hairline ties it to the brand;
	 * tiny stencil labels sit over cold bone-white values.
	 *
	 * Sits just under BoardPlate; boardLayout lifts the board when the bet/spin
	 * bar would otherwise force this console up into the reels.
	 */
	import * as PIXI from 'pixi.js';
	import { MainContainer } from 'components-layout';
	import { Container, Graphics, Text } from 'pixi-svelte';
	import { stateBet, stateUi } from 'state-shared';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';

	import { getContext } from '../game/context';
	import config from '../game/config';
	import { BOARD_PLATE_PAD } from '../game/constants';
	import { COLUMN_ROW_OFFSET } from '../game/chassisArt';
	import { stateShake } from '../game/stateShake.svelte';
	import { hudColor } from '../game/hud.generated';
	import InfoMarquee from './InfoMarquee.svelte';

	const context = getContext();

	// cold bone-white readout value colour — config-driven (hud.colors.text)
	const VALUE_COLOR = hudColor('text', 0xf0e6d0);
	// cool steel grey for the tiny stencil labels
	const LABEL_COLOR = 0x8b93a0;
	const LABEL_FAMILY = '"Arial Narrow", "Segoe UI Semibold", "Segoe UI", Arial, sans-serif';
	const VALUE_FAMILY = '"Segoe UI", Arial, Helvetica, sans-serif';

	// Console sizing (BoardFrame is gone — no gold trim lockstep).
	const GAP = 6;
	/** air between BoardPlate bottom lip and the WAYS/WIN console top */
	const PLATE_CLEAR = 14;

	const BASE_WAYS = config.numRows.reduce((total, rows) => total * rows, 1);
	let ways = $state(BASE_WAYS);
	let spinsShow = $state(false);
	let spinsCurrent = $state(0);
	let spinsTotal = $state(0);

	context.eventEmitter.subscribeOnMount({
		waysCounterUpdate: (e) => {
			ways = e.ways;
		},
		waysCounterHide: () => {
			ways = BASE_WAYS;
		},
		freeSpinCounterShow: () => {
			spinsShow = true;
		},
		freeSpinCounterHide: () => {
			spinsShow = false;
		},
		freeSpinCounterUpdate: (e) => {
			if (e.current !== undefined) spinsCurrent = e.current;
			if (e.total !== undefined) spinsTotal = e.total;
		},
	});

	// Geometry ONLY — deliberately reads neither the win/ways VALUES nor
	// stateShake, so the gradient-heavy console redraw fires only on a real
	// resize, not on every win count-up frame or shake frame. Shake is applied
	// as a cheap Container translate in the template; values live in their own
	// $state and drive just the Text nodes.
	const layout = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const bw = board.width;
		const bh = board.height;
		const frameY = board.y;

		// Base rail width = the NORMAL reels' plate exactly (the dark matte behind
		// the cards), NOT side cages. Wells grow PAST this base when a value needs room.
		const baseW = bw + 2 * GAP;
		const railH = 56;
		// the CARDS (and the plate that hugs them) sit COLUMN_ROW_OFFSET right of
		// the board box's centre (0.53 reel padding) — centre the rail on the
		// cards, not the box, or it rides a few px left of the plate
		const railX = board.x + COLUMN_ROW_OFFSET;
		// Preferred: console sits JUST BELOW the BoardPlate bottom lip.
		// (Old math reserved LOCKED_SLOTS_BOTTOM_EXTENT for number plates that
		// no longer exist, then railFloor clamped the console UP into the plate.)
		const plateBottom = frameY + bh / 2 + BOARD_PLATE_PAD;
		const preferredRailY = plateBottom + PLATE_CLEAR + railH / 2;
		// The bet/spin controls hug the REAL screen bottom — clamp the rail so it
		// never runs into them (boardLayout also lifts the board when needed).
		const main = context.stateLayoutDerived.mainLayout();
		const canvasH = context.stateLayoutDerived.canvasSizes().height;
		const hudTopScreen = stateUi.hudBarTopScreenY;
		const HUD_CLEAR_PX = 12; // breathing room above the controls, screen px
		const railFloor =
			hudTopScreen > 0
				? main.height / 2 + (hudTopScreen - HUD_CLEAR_PX - canvasH / 2) / main.scale - railH / 2
				: Number.POSITIVE_INFINITY;
		const railY = Math.min(preferredRailY, railFloor);

		// --- three recessed wells that GROW to fit their content --------------
		const railRadius = railH * 0.24;
		const vPad = railH * 0.15;
		const wellH = railH - 2 * vPad;
		const wellRadius = wellH * 0.26;
		const sidePad = baseW * 0.024;
		const gap = baseW * 0.022;
		// at the base width the three wells split the rail evenly
		const baseShare = (baseW - 2 * sidePad - 2 * gap) / 3;

		const valueFontSize = Math.max(12, Math.floor(wellH * 0.44));
		const labelFontSize = Math.max(8, Math.floor(wellH * 0.24));

		// Width a well needs to hold its label + value at full size. This is what
		// lets a huge WAYS count or a big foreign-currency WIN push its box wider
		// (like the bet field) instead of cramming/clipping the number.
		const innerPadX = wellH * 0.85;
		const contentW = (label: string, value: string) => {
			const valueW = value.length * valueFontSize * 0.6;
			const labelW = label.length * (labelFontSize * 0.62 + 2);
			return Math.max(valueW, labelW) + innerPadX;
		};

		const waysValue = `${ways}`;
		const winValue = bookEventAmountToCurrencyString(stateBet.winBookEventAmount);
		const spinsValue = `${spinsTotal - spinsCurrent}/${spinsTotal}`;

		// left/right grow to their content; the centre keeps the base share (its
		// ticker scrolls, so it never needs to grow) unless the FREE SPINS
		// counter is showing there.
		const leftW = Math.max(baseShare, contentW('WAYS', waysValue));
		const rightW = Math.max(baseShare, contentW('WIN', winValue));
		const centerW = Math.max(baseShare, spinsShow ? contentW('FREE SPINS', spinsValue) : 0);

		const railW = leftW + centerW + rightW + 2 * gap + 2 * sidePad;

		// well centres laid out left→right. local = relative to the rail centre
		// (drives the shake-free Graphics draw); world = absolute (drives Text).
		let cursor = -railW / 2 + sidePad;
		const localWells = [leftW, centerW, rightW].map((w) => {
			const cx = cursor + w / 2;
			cursor += w + gap;
			return { cx, cy: 0, w, h: wellH, r: wellRadius };
		});
		const wells = localWells.map((lw) => ({
			cx: railX + lw.cx,
			cy: railY,
			w: lw.w,
			h: lw.h,
			r: lw.r,
		}));

		const slots = [
			{ well: wells[0], label: 'WAYS', value: waysValue, show: true },
			{ well: wells[1], label: 'FREE SPINS', value: spinsValue, show: spinsShow },
			{ well: wells[2], label: 'WIN', value: winValue, show: true },
		];

		return {
			railX,
			railY,
			railW,
			railH,
			railRadius,
			localWells,
			wells,
			slots,
			valueFontSize,
			labelFontSize,
		};
	});

	type Layout = typeof layout;

	// Gradients are colour-constant, so build them ONCE (not per redraw): the
	// costly step is generating the gradient texture, and reusing the object
	// keeps the console's per-frame redraw (win count-ups) cheap. textureSpace
	// 'local' remaps each gradient across whatever rect fills with it.
	const vGradient = (stops: Array<[number, number]>) =>
		new PIXI.FillGradient({
			type: 'linear',
			start: { x: 0, y: 0 },
			end: { x: 0, y: 1 },
			colorStops: stops.map(([offset, color]) => ({ offset, color })),
			textureSpace: 'local',
		});
	// Sampled off the live board so the console reads as PART of the machine:
	// plate between cards #0f1012, lit plate edges #1d1e20.
	const STEEL_GRAD = vGradient([
		[0, 0x1d1f23],
		[0.5, 0x131417],
		[1, 0x0c0d0f],
	]);
	const GLASS_GRAD = vGradient([
		[0, 0x08090c],
		[1, 0x020304],
	]);

	/** paint the whole console, in rail-local coords (shake is a Container) */
	const drawConsole = (g: PIXI.Graphics, L: Layout) => {
		const rw = L.railW;
		const rh = L.railH;
		const rr = L.railRadius;

		// soft drop shadow under the plate
		g.roundRect(-rw / 2, -rh / 2 + 4, rw, rh, rr).fill({ color: 0x000000, alpha: 0.38 });

		// brushed-steel plate — matches the board's dark cell cages
		g.roundRect(-rw / 2, -rh / 2, rw, rh, rr).fill(STEEL_GRAD);
		// top bevel highlight + hard outer edge (board-plate tones)
		g.roundRect(-rw / 2 + 1.5, -rh / 2 + 1.5, rw - 3, rh - 3, rr - 1).stroke({
			color: 0x33363c,
			width: 1.5,
			alpha: 0.6,
		});
		g.roundRect(-rw / 2, -rh / 2, rw, rh, rr).stroke({ color: 0x050607, width: 2 });

		// recessed glass wells (local coords → shake handled by the Container)
		for (const w of L.localWells) {
			const cx = w.cx;
			const cy = w.cy;
			const x = cx - w.w / 2;
			const y = cy - w.h / 2;
			// seat shadow
			g.roundRect(x - 1, y - 1, w.w + 2, w.h + 2, w.r + 1).fill({ color: 0x000000, alpha: 0.6 });
			// dark glass
			g.roundRect(x, y, w.w, w.h, w.r).fill(GLASS_GRAD);
			// top glass sheen
			g.roundRect(x + 2, y + 2, w.w - 4, w.h * 0.42, w.r).fill({ color: 0xffffff, alpha: 0.05 });
			// warm inner glow pooled low in the well
			g.roundRect(cx - w.w * 0.32, cy - w.h * 0.02, w.w * 0.64, w.h * 0.42, w.r * 0.6).fill({
				color: 0x6b5a3a,
				alpha: 0.1,
			});
			// steel bezel ring + inner recess line (board-plate tones)
			g.roundRect(x, y, w.w, w.h, w.r).stroke({ color: 0x2a2d32, width: 1.5, alpha: 0.9 });
			g.roundRect(x + 1.5, y + 1.5, w.w - 3, w.h - 3, w.r).stroke({
				color: 0x030405,
				width: 1,
				alpha: 0.85,
			});
		}
	};

	const fitFontSize = (base: number, text: string, maxW: number) =>
		Math.max(9, Math.min(base, Math.floor(maxW / (text.length * 0.6))));

	// Base game: the centre well shows a scrolling info ticker instead of sitting
	// empty. During free spins the FREE SPINS counter owns that well, so the two
	// are mutually exclusive (counter takes precedence).
	const showMarquee = $derived(!spinsShow && context.stateGame.gameType !== 'freegame');
</script>

<MainContainer>
	{@const L = layout}
	<!-- shake is a cheap Container translate so it never re-runs the console
		draw (geometry is computed shake-free) -->
	<Container x={stateShake.x} y={stateShake.y}>
		<!-- procedural clinical steel console: plate + three recessed glass wells -->
		<Graphics x={L.railX} y={L.railY} draw={(g) => drawConsole(g, L)} />

		{#each L.slots as s (s.label + String(s.show))}
			{#if s.show}
				<!-- tiny stencil label above the cold bone-white value -->
				<Container x={s.well.cx} y={s.well.cy}>
				<Text
					x={0}
					y={-s.well.h * 0.26}
					anchor={0.5}
					text={s.label}
					eventMode="none"
					style={{
						fill: LABEL_COLOR,
						fontSize: fitFontSize(L.labelFontSize, s.label, s.well.w * 0.9),
						fontWeight: '600',
						fontFamily: LABEL_FAMILY,
						letterSpacing: 2,
					}}
				/>
				<Text
					x={0}
					y={s.well.h * 0.16}
					anchor={0.5}
					text={s.value}
					eventMode="none"
					style={{
						fill: VALUE_COLOR,
						fontSize: fitFontSize(L.valueFontSize, s.value, s.well.w * 0.88),
						fontWeight: '700',
						fontFamily: VALUE_FAMILY,
						letterSpacing: 0.3,
						stroke: { color: 0x05070a, width: 2 },
						dropShadow: { color: 0x000000, blur: 3, distance: 1, alpha: 0.6, angle: Math.PI / 2 },
					}}
				/>
			</Container>
		{/if}
	{/each}

	<!-- centre well: base-game info ticker (hidden while the FREE SPINS counter
		occupies the same well during the bonus) -->
	{#if showMarquee}
		{@const c = L.slots[1].well}
		<InfoMarquee x={c.cx} y={c.cy} width={c.w * 0.9} height={c.h * 0.82} fontSize={L.valueFontSize} />
	{/if}
	</Container>
</MainContainer>
