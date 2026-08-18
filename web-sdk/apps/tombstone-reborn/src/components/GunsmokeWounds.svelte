<script lang="ts" module>
	import type { SymbolName } from '../game/types';
	import type { MuzzleSide } from '../game/gunsmokeSpin';

	export type EmitterEventGunsmokeWounds =
		| {
				type: 'gunsmokeWound';
				reel: number;
				row: number;
				blood?: boolean;
				name?: SymbolName;
				beatMs?: number;
				flightScale?: number;
				side?: MuzzleSide;
		  }
		| {
				type: 'cellFrameStain';
				reel: number;
				row: number;
		  }
		| {
				type: 'gunsmokeCellDent';
				reel: number;
				row: number;
				hitX: number;
				hitY: number;
				seed: number;
		  }
		| { type: 'gunsmokeWoundsClear' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite } from 'pixi-svelte';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { getContext } from '../game/context';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { GUNSMOKE_WOUND_Z, SYMBOL_CARD_W } from '../game/constants';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { fxRandom } from '../game/featureVfx';
	import {
		BLOOD_SPLASH_IN_MS,
		BLOOD_SPLASH_OUT_MS,
		BLOOD_STAIN_RESIDUAL,
		BULLET_DIST_MS,
		BULLET_FAR_SCALE,
		BULLET_MAX_MS,
		BULLET_MS,
		BULLET_NEAR_SCALE,
		BULLET_W,
		CELL_FRAME_MASK_H,
		CELL_FRAME_MASK_KEY,
		CELL_FRAME_MASK_W,
		WOUND_BEAT_MS,
		CRUSH_IN_MS,
		CRUSH_OUT_MS,
		fpsMuzzlePoint,
		frameBloodLayers,
		pickBullet,
		woundImpact,
		type WoundLayer,
	} from '../game/gunsmokeSpin';
	import BoardSpace from './BoardSpace.svelte';
	import MuzzleSmoke from './MuzzleSmoke.svelte';

	const context = getContext();

	type Wound = {
		key: string;
		reel: number;
		row: number;
		layers: WoundLayer[];
		pop: Tween<number>;
		splash: Tween<number>;
		crush: Tween<number>;
	};
	type Round = {
		id: number;
		x0: number;
		y0: number;
		x1: number;
		y1: number;
		travel: number;
		bulletKey: string;
		bulletNative: number;
		t: Tween<number>;
	};
	type Puff = { id: number; x: number; y: number; size: number; heading: number };

	let wounds = $state<Wound[]>([]);
	let rounds = $state<Round[]>([]);
	let puffs = $state<Puff[]>([]);
	const fallOut = new Tween(0);
	let nextId = 0;

	const placed = $derived(
		wounds.map((wound) => ({
			...wound,
			x: getSymbolX(wound.reel),
			y: getCellCenterY(wound.reel, wound.row),
			holes: wound.layers.filter((layer) => layer.kind === 'hole'),
			bloods: wound.layers.filter((layer) => layer.kind === 'blood'),
			scale: 0.8 + 0.2 * wound.pop.current,
			crushX: 1 + 0.1 * wound.crush.current,
			crushY: 1 - 0.18 * wound.crush.current,
		})),
	);

	const flying = $derived(
		rounds.map((round) => {
			const t = round.t.current;
			return {
				...round,
				x: round.x0 + (round.x1 - round.x0) * t,
				y: round.y0 + (round.y1 - round.y0) * t,
				rotation: round.travel - round.bulletNative,
				scale: BULLET_NEAR_SCALE + (BULLET_FAR_SCALE - BULLET_NEAR_SCALE) * t,
			};
		}),
	);

	const hangSmoke = (x: number, y: number, heading: number, seed: number) => {
		puffs = [
			...puffs,
			{
				id: nextId++,
				x: x + Math.cos(heading) * 8 + (fxRandom(seed) - 0.5) * 6,
				y: y + Math.sin(heading) * 8 + (fxRandom(seed + 1) - 0.5) * 6,
				size: SYMBOL_CARD_W * 0.88,
				heading,
			},
			{
				id: nextId++,
				x: x + Math.cos(heading) * 16 + (fxRandom(seed + 3) - 0.5) * 8,
				y: y + Math.sin(heading) * 16 + (fxRandom(seed + 4) - 0.5) * 8,
				size: SYMBOL_CARD_W * 0.68,
				heading,
			},
		];
	};

	const flyRound = async (
		from: { x: number; y: number },
		to: { x: number; y: number },
		flightScale: number,
	) => {
		const travel = Math.atan2(to.y - from.y, to.x - from.x);
		const bullet = pickBullet(travel);
		const id = nextId++;
		const flight = new Tween(0);
		const dist = Math.hypot(to.x - from.x, to.y - from.y);
		rounds = [
			...rounds,
			{
				id,
				x0: from.x,
				y0: from.y,
				x1: to.x,
				y1: to.y,
				travel,
				bulletKey: bullet.key,
				bulletNative: bullet.native,
				t: flight,
			},
		];
		await flight.set(1, {
			duration: fxDur(Math.min(BULLET_MAX_MS, BULLET_MS + dist * BULLET_DIST_MS) * flightScale),
			easing: cubicOut,
		});
		rounds = rounds.filter((item) => item.id !== id);
	};

	const dropPuff = (id: number) => {
		puffs = puffs.filter((item) => item.id !== id);
	};

	const paintStain = (splash: Tween<number>) => {
		void splash.set(1, { duration: fxDur(BLOOD_SPLASH_IN_MS), easing: backOut }).then(() => {
			void splash.set(BLOOD_STAIN_RESIDUAL, { duration: fxDur(BLOOD_SPLASH_OUT_MS), easing: cubicOut });
		});
	};

	const stampHole = async (reel: number, row: number, blood: boolean) => {
		const key = `${reel}-${row}-${wounds.length}`;
		const pop = new Tween(0);
		const splash = new Tween(0);
		const crush = new Tween(0);
		const impact = woundImpact(reel, row + wounds.length * 3, blood);
		wounds = [
			...wounds,
			{
				key,
				reel,
				row,
				layers: impact.layers,
				pop,
				splash,
				crush,
			},
		];
		context.eventEmitter.broadcast({
			type: 'gunsmokeCellDent',
			reel,
			row,
			hitX: impact.hitX,
			hitY: impact.hitY,
			seed: impact.seed,
		});
		void crush.set(1, { duration: fxDur(CRUSH_IN_MS), easing: backOut }).then(() => {
			void crush.set(0, { duration: fxDur(CRUSH_OUT_MS), easing: cubicOut });
		});
		if (blood) paintStain(splash);
		await pop.set(1, { duration: fxDur(160), easing: backOut });
	};

	const stampFrameBlood = (reel: number, row: number) => {
		const key = `${reel}-${row}-stain-${wounds.length}`;
		const pop = new Tween(1);
		const splash = new Tween(0);
		const crush = new Tween(0);
		wounds = [
			...wounds,
			{
				key,
				reel,
				row,
				layers: frameBloodLayers(reel, row, wounds.length),
				pop,
				splash,
				crush,
			},
		];
		paintStain(splash);
	};

	const stamp = async (
		reel: number,
		row: number,
		blood: boolean,
		beatMs = WOUND_BEAT_MS,
		flightScale = 1,
		side: MuzzleSide = 'right',
	) => {
		const main = context.stateLayoutDerived.mainLayout();
		const from = fpsMuzzlePoint(
			context.stateGameDerived.boardLayout(),
			{ left: 0, right: main.width },
			side,
			reel * 17 + row * 11,
		);
		const to = { x: getSymbolX(reel), y: getCellCenterY(reel, row) };
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_gunshot', forcePlay: true });
		await flyRound(from, to, flightScale);
		hangSmoke(to.x, to.y, -Math.PI / 2, reel * 19 + row * 7);
		await stampHole(reel, row, blood);
		if (beatMs > 0) await fxWait(beatMs);
	};

	const clear = () => {
		wounds = [];
		rounds = [];
		puffs = [];
		fallOut.set(0, { duration: 0 });
	};

	context.eventEmitter.subscribeOnMount({
		gunsmokeWound: async ({ reel, row, blood, beatMs, flightScale, side }) => {
			await stamp(reel, row, blood === true, beatMs, flightScale, side);
		},
		cellFrameStain: ({ reel, row }) => {
			stampFrameBlood(reel, row);
		},
		gunsmokeWoundsClear: () => clear(),
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, wounds.length > 0 || rounds.length > 0 || puffs.length > 0);
			clear();
		},
	});
</script>

<!-- Stage z: nested 11 never beat a remounted boardFrameSmall at App sort. -->
<Container zIndex={GUNSMOKE_WOUND_Z} eventMode="none">
<MainContainer>
	{#if placed.length || flying.length || puffs.length}
		<BoardSpace yOffset={fallOut.current}>
			<Container eventMode="none">
				{#each flying as round (round.id)}
					<Sprite
						key={round.bulletKey}
						x={round.x}
						y={round.y}
						anchor={0.5}
						width={BULLET_W * round.scale}
						height={BULLET_W * round.scale}
						rotation={round.rotation}
					/>
				{/each}
				{#each puffs as puff (puff.id)}
					<MuzzleSmoke
						x={puff.x}
						y={puff.y}
						size={puff.size}
						heading={puff.heading}
						oncomplete={() => dropPuff(puff.id)}
					/>
				{/each}
				{#each placed as wound (wound.key)}
					<Container x={wound.x} y={wound.y} scale={{ x: wound.crushX, y: wound.crushY }}>
						{#each wound.holes as layer, i (`${wound.key}-hole-${i}`)}
							<Sprite
								key={layer.key}
								x={layer.x}
								y={layer.y}
								anchor={0.5}
								width={layer.width}
								height={layer.height}
								rotation={layer.rotation}
								alpha={layer.alpha * wound.pop.current}
							/>
						{/each}
						{#if wound.bloods.length}
							<Container>
								<Sprite
									isMask
									key={CELL_FRAME_MASK_KEY}
									anchor={0.5}
									width={CELL_FRAME_MASK_W}
									height={CELL_FRAME_MASK_H}
									renderable={false}
								/>
								{#each wound.bloods as layer, i (`${wound.key}-blood-${i}`)}
									<Sprite
										key={layer.key}
										x={layer.x}
										y={layer.y}
										anchor={0.5}
										width={layer.width * wound.scale}
										height={layer.height * wound.scale}
										rotation={layer.rotation}
										alpha={layer.alpha * wound.splash.current}
									/>
								{/each}
							</Container>
						{/if}
					</Container>
				{/each}
			</Container>
		</BoardSpace>
	{/if}
</MainContainer>
</Container>
