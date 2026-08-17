<script lang="ts" module>
	import { ColorMatrixFilter } from 'pixi.js';

	import {
		LANE_DOOR_GRADE_BRIGHTNESS,
		LANE_DOOR_GRADE_SATURATE,
	} from '../game/laneDoor';

	const WOOD_GRADE = new ColorMatrixFilter();
	WOOD_GRADE.saturate(LANE_DOOR_GRADE_SATURATE);
	WOOD_GRADE.brightness(LANE_DOOR_GRADE_BRIGHTNESS, true);
	const WOOD_GRADE_FILTERS = [WOOD_GRADE];
</script>

<script lang="ts">
	/**
	 * The boarded cover over the LAST-REEL LANE.
	 *
	 * One box: the last-reel board slot. Left edge on the cell, full pitch
	 * cover so the timber never shows as a grey strip. Height is the inner
	 * opening (sill to lintel), not 16% past the wood. Closed face fills it.
	 * Open plays the swing, then holds. Next locked reveal slams shut.
	 * zIndex stays above the sliding gold card so a remount cannot cover
	 * the hinge post.
	 */
	import * as PIXI from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
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
		LANE_DOOR_FRAME_COUNT,
		LANE_DOOR_FRAME_LIP,
		LANE_DOOR_OPEN_MS,
		LANE_DOOR_Z,
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
			h: h - LANE_DOOR_FRAME_LIP * 2,
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
	<Container zIndex={LANE_DOOR_Z} eventMode="none">
		<BoardSpace>
			<Container filters={WOOD_GRADE_FILTERS} eventMode="none">
				<BaseSprite
					{texture}
					x={slot.x}
					y={slot.y}
					anchor={{ x: 0, y: 0.5 }}
					width={COVER_W}
					height={slot.h}
					eventMode="none"
				/>
			</Container>
		</BoardSpace>
	</Container>
{/if}
