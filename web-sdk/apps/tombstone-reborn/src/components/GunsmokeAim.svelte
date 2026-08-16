<script lang="ts" module>
	/** Revolver overlay on a landed GUNSMOKE card. It sits on the GS cell,
	 *  then turns so the barrel aims at each target's centre before the shot. */
	export type EmitterEventGunsmokeAim =
		| { type: 'gunsmokeGunShow'; cells: { reel: number; row: number }[] }
		| { type: 'gunsmokeGunAim'; reel: number; row: number }
		| { type: 'gunsmokeGunFire' }
		| { type: 'gunsmokeGunHide' };
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite } from 'pixi-svelte';

	import { fallOutFeatureFx } from '../game/featureFallOut.svelte';
	import { filterVisibleCells } from '../game/boardCells';
	import { fxDur, fxWait } from '../game/fxTiming';
	import { getContext } from '../game/context';
	import { getSymbolX, getCellCenterY } from '../game/utils';
	import { SYMBOL_CARD_W as CARD_W, SYMBOL_CARD_H as CARD_H } from '../game/constants';
	import { FEATURE_ART, FX, seqFrame, puffFade } from '../game/featureVfx';
	import FeatureFxSprite from './FeatureFxSprite.svelte';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	/** keyed PNG is 1024×488, barrel pointing +X */
	const GUN_ASPECT = 1024 / 488;
	const GUN_W = CARD_W * 1.42;
	const GUN_H = GUN_W / GUN_ASPECT;
	/** grip / cylinder — the hand that turns the aim */
	const ANCHOR = { x: 0.22, y: 0.56 };
	const BARREL_X = GUN_W * (0.94 - ANCHOR.x);
	const BARREL_Y = GUN_H * (0.4 - ANCHOR.y);
	const REST_ROT = -0.22;

	// fireburst.png: cone originates lower-right, sprays upper-left
	const BURST_SRC_W = 1084;
	const BURST_SRC_H = 888;
	const BURST_ORIGIN = { x: 980 / BURST_SRC_W, y: 680 / BURST_SRC_H };
	const BURST_W = CARD_W * 1.9;
	const BURST_H = BURST_W * (BURST_SRC_H / BURST_SRC_W);
	const BURST_ROT = Math.PI - Math.atan2(680, 980);

	type Gun = { key: string; reel: number; row: number; rot: Tween<number> };

	let guns = $state<Gun[]>([]);
	let show = $state(false);
	const appear = new Tween(0);
	const recoil = new Tween(0);
	const shot = new Tween(0);
	const fallOut = new Tween(0);

	const shortest = (from: number, to: number) => {
		let delta = to - from;
		while (delta > Math.PI) delta -= Math.PI * 2;
		while (delta < -Math.PI) delta += Math.PI * 2;
		return from + delta;
	};

	const placed = $derived.by(() =>
		guns.map((gun) => {
			const aim = gun.rot.current;
			const kick = recoil.current;
			return {
				...gun,
				x: getSymbolX(gun.reel) - Math.cos(aim) * kick * 16,
				y: getCellCenterY(gun.reel, gun.row) - Math.sin(aim) * kick * 16,
				rotation: aim - kick * 0.2,
			};
		}),
	);

	const blast = $derived(shot.current > 0 && shot.current < 0.42 ? 1 - shot.current / 0.42 : 0);
	const smoke = $derived(puffFade(shot.current));

	const sameCells = (incoming: { reel: number; row: number }[]) =>
		show &&
		guns.length === incoming.length &&
		incoming.every((cell, i) => guns[i]?.reel === cell.reel && guns[i]?.row === cell.row);

	const showGuns = async (incoming: { reel: number; row: number }[]) => {
		const visible = filterVisibleCells(incoming);
		if (!visible.length) return;
		if (sameCells(visible)) {
			if (appear.current > 0.85) return;
			await appear.set(1, { duration: fxDur(160), easing: backOut });
			return;
		}
		guns = visible.map((cell) => ({
			key: `${cell.reel}-${cell.row}`,
			reel: cell.reel,
			row: cell.row,
			rot: new Tween(REST_ROT),
		}));
		recoil.set(0, { duration: 0 });
		shot.set(0, { duration: 0 });
		fallOut.set(0, { duration: 0 });
		appear.set(0, { duration: 0 });
		show = true;
		await appear.set(1, { duration: fxDur(240), easing: backOut });
	};

	const aimAt = async (reel: number, row: number) => {
		if (!show || !guns.length) return;
		const tx = getSymbolX(reel);
		const ty = getCellCenterY(reel, row);
		let maxDelta = 0;
		const targets = guns.map((gun) => {
			const gx = getSymbolX(gun.reel);
			const gy = getCellCenterY(gun.reel, gun.row);
			const to = shortest(gun.rot.current, Math.atan2(ty - gy, tx - gx));
			maxDelta = Math.max(maxDelta, Math.abs(to - gun.rot.current));
			return { gun, to };
		});
		if (maxDelta < 0.03) return;
		const ms = 150 + 220 * (maxDelta / Math.PI);
		await Promise.all(
			targets.map(({ gun, to }) => gun.rot.set(to, { duration: fxDur(ms), easing: cubicOut })),
		);
	};

	const fire = async () => {
		if (!show) return;
		shot.set(0, { duration: 0 });
		recoil.set(1, { duration: 0 });
		void recoil.set(0, { duration: fxDur(280), easing: cubicOut });
		void shot.set(1, { duration: fxDur(360), easing: cubicOut });
		await fxWait(90);
	};

	const hide = async () => {
		if (!show) return;
		await appear.set(0, { duration: fxDur(160), easing: cubicOut });
		clear();
	};

	const clear = () => {
		show = false;
		guns = [];
		appear.set(0, { duration: 0 });
		recoil.set(0, { duration: 0 });
		shot.set(0, { duration: 0 });
		fallOut.set(0, { duration: 0 });
	};

	context.eventEmitter.subscribeOnMount({
		gunsmokeGunShow: async ({ cells }) => {
			await showGuns(cells);
		},
		gunsmokeGunAim: async ({ reel, row }) => {
			await aimAt(reel, row);
		},
		gunsmokeGunFire: async () => {
			await fire();
		},
		gunsmokeGunHide: async () => {
			await hide();
		},
		featureFxFallOut: async () => {
			await fallOutFeatureFx(fallOut, show && guns.length > 0);
			clear();
		},
	});
</script>

<MainContainer>
	{#if show && guns.length}
		<BoardSpace yOffset={fallOut.current}>
			{#each placed as gun (gun.key)}
				<Container
					x={gun.x}
					y={gun.y}
					rotation={gun.rotation}
					alpha={appear.current}
					scale={0.82 + 0.18 * appear.current}
				>
					<Sprite
						key={FEATURE_ART.revolver}
						anchor={ANCHOR}
						width={GUN_W}
						height={GUN_H}
					/>
					{#if blast > 0.04}
						<Sprite
							key="muzzleBurst"
							anchor={BURST_ORIGIN}
							x={BARREL_X}
							y={BARREL_Y}
							width={BURST_W * (0.85 + (1 - blast) * 0.45)}
							height={BURST_H * (0.85 + (1 - blast) * 0.45)}
							rotation={BURST_ROT}
							alpha={blast}
							blendMode="add"
						/>
						<FeatureFxSprite
							tex={seqFrame(FX.muzzle, 1 - blast)}
							x={BARREL_X + CARD_W * 0.18}
							y={BARREL_Y}
							width={CARD_W * (1.15 + (1 - blast) * 0.9)}
							height={CARD_W * (1.15 + (1 - blast) * 0.9)}
							rotation={Math.PI * 0.5}
							alpha={0.9 * blast}
							blendMode="add"
						/>
						<FeatureFxSprite
							tex={seqFrame(FX.flash, 1 - blast)}
							x={BARREL_X}
							y={BARREL_Y}
							width={CARD_W * (0.7 + (1 - blast) * 0.5)}
							height={CARD_W * (0.7 + (1 - blast) * 0.5)}
							alpha={0.7 * blast}
							blendMode="add"
						/>
					{/if}
					{#if smoke > 0.04}
						<FeatureFxSprite
							tex={seqFrame(FX.gunsmoke, shot.current)}
							x={BARREL_X + CARD_W * 0.22 * shot.current}
							y={BARREL_Y - CARD_H * 0.18 * shot.current}
							width={CARD_W * (0.7 + shot.current * 0.85)}
							height={CARD_W * (0.7 + shot.current * 0.85)}
							alpha={0.65 * smoke}
						/>
					{/if}
				</Container>
			{/each}
		</BoardSpace>
	{/if}
</MainContainer>
