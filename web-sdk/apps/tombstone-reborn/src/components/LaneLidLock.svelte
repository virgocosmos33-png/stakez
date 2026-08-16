<script lang="ts">
	/**
	 * The boarded cover over the LAST-REEL LANE.
	 *
	 * One box: the last-reel board slot. Closed face fills it. Open plays
	 * the full 16-frame swing, then holds. Next locked reveal slams shut
	 * in 10 poses (impact on the last). Super-bonus keeps lidOpen.
	 */
	import * as PIXI from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { MainContainer } from 'components-layout';
	import { BaseSprite, Container } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { CELL_PITCH_X } from '../game/constants';
	import { getCellLeft, getReelWindow } from '../game/utils';
	import { fxDur, fxWait } from '../game/fxTiming';
	import {
		LANE_DOOR_ASSET,
		LANE_DOOR_CLOSE_MS,
		LANE_DOOR_CLOSE_SLAM,
		LANE_DOOR_COVER_SCALE_X,
		LANE_DOOR_COVER_SCALE_Y,
		LANE_DOOR_FRAME_COUNT,
		LANE_DOOR_OPEN_MS,
	} from '../game/laneDoor';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	const LAST = context.stateGame.board.length - 1;
	const COVER_W = CELL_PITCH_X * LANE_DOOR_COVER_SCALE_X;

	const slot = $derived.by(() => {
		const window = getReelWindow(LAST);
		const h = window.bottom - window.top;
		return {
			x: getCellLeft(LAST),
			y: (window.top + window.bottom) / 2,
			h: h * LANE_DOOR_COVER_SCALE_Y,
		};
	});

	/** 0 = closed face, 1 = last swing frame. Stays at 1 while the lane is open. */
	const swing = new Tween(context.stateGame.lidOpen ? 1 : 0, { duration: 0 });
	let pose = $state(context.stateGame.lidOpen ? LANE_DOOR_FRAME_COUNT - 1 : 0);
	let wasOpen = context.stateGame.lidOpen;
	let slamGen = 0;

	const slamShut = async (gen: number) => {
		const last = LANE_DOOR_CLOSE_SLAM.length - 1;
		const stepMs = LANE_DOOR_CLOSE_MS / LANE_DOOR_CLOSE_SLAM.length;
		for (let i = 0; i < LANE_DOOR_CLOSE_SLAM.length; i += 1) {
			if (gen !== slamGen) return;
			pose = LANE_DOOR_CLOSE_SLAM[i];
			if (i < last) {
				// last gap is the impact — shorter than the steps into it
				const ms = i === last - 1 ? stepMs * 0.55 : stepMs;
				await fxWait(ms);
			}
		}
		if (gen === slamGen) void swing.set(0, { duration: 0 });
	};

	$effect(() => {
		if (!context.stateGame.lidOpen) return;
		pose = Math.min(
			LANE_DOOR_FRAME_COUNT - 1,
			Math.floor(swing.current * (LANE_DOOR_FRAME_COUNT - 0.001)),
		);
	});

	$effect(() => {
		const open = context.stateGame.lidOpen;
		if (open === wasOpen) return;
		wasOpen = open;
		slamGen += 1;
		if (open) {
			void swing.set(1, { duration: fxDur(LANE_DOOR_OPEN_MS), easing: cubicOut });
		} else {
			void slamShut(slamGen);
		}
	});

	const frames = $derived(
		(context.stateApp.loadedAssets?.[LANE_DOOR_ASSET] as PIXI.Texture[] | undefined) ?? [],
	);
	const texture = $derived(frames[pose]);
</script>

{#if texture}
	<MainContainer>
		<Container zIndex={12} eventMode="none">
			<BoardSpace>
				<BaseSprite
					{texture}
					x={slot.x}
					y={slot.y}
					anchor={{ x: 0, y: 0.5 }}
					width={COVER_W}
					height={slot.h}
					eventMode="none"
				/>
			</BoardSpace>
		</Container>
	</MainContainer>
{/if}
