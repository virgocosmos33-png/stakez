<script lang="ts">
	/**
	 * The boarded cover over the LAST-REEL LANE.
	 *
	 * Closed face fills the last-reel slot. Open hinges that same door
	 * OUTWARD on the right post (toward the camera) so the lane shows
	 * through — not a second door pushed into the hole. Next locked
	 * reveal swings it shut. zIndex stays above the sliding gold card.
	 */
	import type { Texture } from 'pixi.js';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { BaseSprite, Container } from 'pixi-svelte';

	import { playExternalOnce } from 'utils-sound';

	import { getContext } from '../game/context';
	import { CELL_PITCH_X } from '../game/constants';
	import { getCellLeft, getReelWindow } from '../game/utils';
	import { fxDur } from '../game/fxTiming';
	import {
		LANE_DOOR_CLOSED_ASSET,
		LANE_DOOR_CLOSED_SMALL_ASSET,
		LANE_DOOR_CLOSE_MS,
		LANE_DOOR_COVER_SCALE_X,
		LANE_DOOR_OPEN_MS,
		LANE_DOOR_SHIFT_Y,
		LANE_DOOR_Z,
	} from '../game/laneDoor';
	import BoardSpace from './BoardSpace.svelte';

	const context = getContext();

	const LAST = context.stateGame.board.length - 1;
	const COVER_W = CELL_PITCH_X * LANE_DOOR_COVER_SCALE_X;
	const DOOR_CREAK = '/assets/audio/sfx_door_creak.mp3';
	/** Leftover leaf width when the door has swung out (edge of the normal door). */
	const OPEN_SLIVER = 0.14;

	const slot = $derived.by(() => {
		const window = getReelWindow(LAST);
		return {
			x: getCellLeft(LAST),
			y: (window.top + window.bottom) / 2,
		};
	});
	/** 0 = shut, 1 = swung out. Stays at 1 while the lane is open. */
	const swing = new Tween(context.stateGame.lidOpen ? 1 : 0, { duration: 0 });
	let wasOpen = context.stateGame.lidOpen;

	$effect(() => {
		const open = context.stateGame.lidOpen;
		if (open === wasOpen) return;
		wasOpen = open;
		if (open) {
			playExternalOnce(DOOR_CREAK);
			void swing.set(1, { duration: fxDur(LANE_DOOR_OPEN_MS), easing: cubicOut });
		} else {
			void swing.set(0, { duration: fxDur(LANE_DOOR_CLOSE_MS) });
		}
	});

	const closedKey = $derived(
		context.stateGame.atmosphere === 'small'
			? LANE_DOOR_CLOSED_SMALL_ASSET
			: LANE_DOOR_CLOSED_ASSET,
	);
	const closedTex = $derived(
		context.stateApp.loadedAssets?.[closedKey] as Texture | undefined,
	);
	const doorH = $derived(
		closedTex ? COVER_W * (closedTex.height / closedTex.width) : 0,
	);
	const hingeX = $derived(slot.x + COVER_W);
	const t = $derived(swing.current);
	const closedSx = $derived(1 - t * (1 - OPEN_SLIVER));
	const toward = $derived(Math.sin(t * Math.PI) * 0.07);
</script>

{#if closedTex}
	<Container zIndex={LANE_DOOR_Z} eventMode="none">
		<BoardSpace>
			<Container
				x={hingeX}
				y={slot.y + LANE_DOOR_SHIFT_Y}
				scale={{ x: closedSx, y: 1 + toward }}
				eventMode="none"
			>
				<BaseSprite
					texture={closedTex}
					x={-COVER_W}
					anchor={{ x: 0, y: 0.5 }}
					width={COVER_W}
					height={doorH}
					eventMode="none"
				/>
			</Container>
		</BoardSpace>
	</Container>
{/if}
