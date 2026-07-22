<script lang="ts">
	import { onMount } from 'svelte';
	import { stateBetDerived } from 'state-shared';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, SpineProvider, SpineTrack } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { BOARD_SIZES } from '../game/constants';

	const context = getContext();

	// Lady Mirror stands beside the reels on the RIGHT, roughly board height, in
	// the empty room to the right so she NEVER covers the symbols. She lives in the
	// board's MainContainer design space, so she scales and stays glued beside it
	// at every size, and is hidden on layouts too narrow for her.
	//
	// She is a proper CUT-OUT SPINE rig (tools/gen_lady_spine.py): the cutout is
	// sliced into SEPARATE PARTS — head, torso, mirror-arm, upper skirt, lower
	// skirt/hem, veil — each its own atlas region pinned to its own bone
	// (root->hips->torso->head->veil, hips->skirt chain, torso->arm). The idle
	// moves the BONES (float bob + breathing + head tilt + mirror-arm sway + skirt
	// cloth-sway + veil billow), so nothing is warped. When the spine asset is
	// loaded she FLOATS centered beside the board; otherwise she falls back to the
	// trimmed still with a light code-driven breathing idle.
	//
	// BONUS VARIANT: during free spins (gameType === 'freegame') she swaps to the
	// activated pose with the raised glowing hand-mirror. Both variants share one
	// atlas (lady.webp) and face the reels.
	const CHAR_ASPECT = 1021 / 1744; // base cutout W/H
	const BONUS_ASPECT = 1153 / 1718; // bonus cutout W/H
	const HEIGHT_SCALE = 1.16; // still: a touch taller than the board
	const FLOAT_HEIGHT_SCALE = 1.0; // spine floats ~board height (crown stays on-screen)
	const BOTTOM_NUDGE = 34; // still: hem just below the board bottom line
	const LEFT_GAP = 6; // left edge just past the symbol area (never covers symbols)
	const MIN_WIDTH = 130; // below this the right-side room is too tight -> hide her

	// One z-slot BELOW the default (0) gameplay/overlay layers so the big-win
	// celebration takeover, the WIN/WAYS plaques and every other overlay draw ON
	// TOP of her. Kept above the scene-room background (zIndex -1/-2) so she stays
	// visible, and she doesn't overlap the reels.
	const SCENE_Z_INDEX = -0.5;

	const isBonus = $derived(context.stateGame.gameType === 'freegame');

	const stillKey = $derived(isBonus ? 'ladyBonus' : 'ladyCharacter');
	const spineKey = $derived(isBonus ? 'ladyBonusSpine' : 'ladySpine');
	const aspect = $derived(isBonus ? BONUS_ASPECT : CHAR_ASPECT);

	const hasSpine = $derived(context.stateApp.loadedAssets?.[spineKey] != null);

	// ---- still-fallback code idle (only used when the spine isn't available) ---
	let time = $state(0);
	onMount(() => {
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	const breath = $derived(Math.sin(time * 1.0));
	const idleRotation = $derived(hasSpine ? 0 : 0.012 * Math.sin(time * 0.42 + 0.5));
	const idleScaleY = $derived(hasSpine ? 1 : 1 + 0.013 * breath);
	const idleScaleX = $derived(hasSpine ? 1 : 1 - 0.006 * breath);
	const auraPulse = $derived(0.5 + 0.5 * Math.sin(time * 1.35));
	const auraScale = $derived(1.015 + 0.012 * auraPulse);
	const auraAlpha = $derived(hasSpine ? 0 : 0.05 + 0.08 * auraPulse);

	// geometry, all in the board's design space (rides the same scale as the board)
	const layout = $derived.by(() => {
		const board = context.stateGameDerived.boardLayout();
		const main = context.stateLayoutDerived.mainLayout();
		const boardRight = board.x + BOARD_SIZES.width / 2;
		const boardBottom = board.y + BOARD_SIZES.height / 2;

		const leftEdge = boardRight + LEFT_GAP;
		const availWidth = main.width - leftEdge; // room out to the design's right edge
		const scaleH = hasSpine ? FLOAT_HEIGHT_SCALE : HEIGHT_SCALE;
		const naturalHeight = BOARD_SIZES.height * scaleH;
		const naturalWidth = naturalHeight * aspect;
		// contain within the right-side room so the whole figure stays on-screen
		const width = Math.min(naturalWidth, availWidth);
		const height = width / aspect;

		// only the wide layouts (desktop/landscape) keep the HUD in a bottom bar,
		// leaving the right of the board clear; tablet/portrait hide her.
		const wideLayout = ['desktop', 'landscape'].includes(
			context.stateLayoutDerived.layoutType(),
		);

		return {
			visible: wideLayout && width >= MIN_WIDTH,
			// spine floats centered beside the board; still is hem-pinned
			cx: leftEdge + width / 2,
			cyFloat: board.y + BOARD_SIZES.height * 0.03,
			yHem: boardBottom + BOTTOM_NUDGE,
			width,
			height,
		};
	});
</script>

<!-- MainContainer ALWAYS mounts (only the character is conditional) so this
	layer keeps its z-order slot below the WIN/WAYS plaques regardless of when she
	becomes visible. The wrapping Container carries the negative zIndex so the
	celebration overlay + plaques always draw over her. -->
<Container zIndex={SCENE_Z_INDEX}>
<MainContainer>
	{#if layout.visible}
		{#if hasSpine}
			<!-- floating cut-out Spine rig. The skeleton is authored CENTERED on
				its root (box spans [-W/2..W/2] x [-H/2..H/2]), so passing NO anchor
				keeps the pivot at the true figure centre and she centres on
				(cx,cyFloat) — the head never flies off (the old headless bug came
				from a top-left anchor assumption). -->
			<SpineProvider
				key={spineKey}
				x={layout.cx}
				y={layout.cyFloat}
				height={layout.height}
			>
				<SpineTrack
					loop
					trackIndex={0}
					animationName="idle"
					timeScale={stateBetDerived.timeScale()}
				/>
			</SpineProvider>
		{:else}
			<!-- still fallback: hem-pinned, breathing/swaying about her feet -->
			<Container
				x={layout.cx}
				y={layout.yHem}
				rotation={idleRotation}
				scale={{ x: idleScaleX, y: idleScaleY }}
			>
				{#if auraAlpha > 0.001}
					<Sprite
						key={stillKey}
						anchor={{ x: 0.5, y: 1 }}
						width={layout.width * auraScale}
						height={layout.height * auraScale}
						tint={0x9a6cff}
						blendMode={'add'}
						alpha={auraAlpha}
					/>
				{/if}
				<Sprite
					key={stillKey}
					anchor={{ x: 0.5, y: 1 }}
					width={layout.width}
					height={layout.height}
				/>
			</Container>
		{/if}
	{/if}
</MainContainer>
</Container>
