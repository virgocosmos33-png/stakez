<script lang="ts">
	import { onMount } from 'svelte';
	import type { Texture, VideoSource } from 'pixi.js';
	import { stateBetDerived } from 'state-shared';
	import { MainContainer } from 'components-layout';
	import { Container, Sprite, SpineProvider, SpineTrack } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { BOARD_SIZES } from '../game/constants';
	import { charLayoutNum } from '../game/character.generated';

	const context = getContext();

	// Lady Mirror stands beside the reels on the RIGHT, roughly board height, in
	// the empty room to the right so she NEVER covers the symbols. She lives in the
	// board's MainContainer design space, so she scales and stays glued beside it
	// at every size, and is hidden on layouts too narrow for her.
	//
	// Prefer Scenario / local alpha-webm idle loops (lady_idle_*.webm) from
	// whiteroomcharnormalmode.png. GodMode sidescroll Spine is QUARANTINED
	// (double-chair / geometry break) — do not prefer it until QA-clean.
	// Fallback order: idle webm → hem-pinned still. Local cutout Spine is
	// kept registered but only used if neither idle nor still is available.
	//
	// BASE IDLE SEQUENCE (v5 + mid v1): each shipped webm already contains one
	// baked ping-pong (forward+reverse) cycle — that file play = 1 loop.
	// Order: breath ×5 → mid ×1 → move ×1 → repeat. Muted. Mid is BASE ONLY.
	// BONUS (v12): freegame swaps to lady_idle_bonus_v12_intro — play once
	// (A fwd→A rev, audio ON, grade-matched to base v5), then SWAP to
	// lady_idle_bonus_v12_loop (C ping-pong, HTML loop=true, audio ON).
	// Do NOT seek the intro — async seek = hitch/freeze. Dual-clip handoff only.
	// (Unlike H3 Cell Seal expand, which still seeks + mutes its tail loop.)
	const CHAR_ASPECT = 716 / 1259; // whiteroomcharnormalmode cutout W/H
	const BONUS_ASPECT = 720 / 1280; // Scenario bonus 720×1280
	const HEIGHT_SCALE = charLayoutNum('heightScale', 1.28);
	const FLOAT_HEIGHT_SCALE = 1.0; // spine floats ~board height (crown stays on-screen)
	const BOTTOM_NUDGE = charLayoutNum('bottomNudge', 200); // chair feet on padded-cell floor
	const LEFT_GAP = charLayoutNum('leftGap', 6); // left edge past symbols
	const MIN_WIDTH = charLayoutNum('minWidth', 130); // hide when right room too tight
	const ANCHOR_Y = charLayoutNum('anchorY', 0.95); // chair-leg contact (not trailing toes)

	/** Completions of the baked ping-pong breath file before switching to mid. */
	const BREATH_LOOPS = 5;
	/** Completions of the baked ping-pong mid file before switching to move. */
	const MID_LOOPS = 1;
	/** Completions of the baked ping-pong move file before returning to breath. */
	const MOVE_LOOPS = 1;

	// One z-slot BELOW the default (0) gameplay/overlay layers so the big-win
	// celebration takeover, the WIN/WAYS plaques and every other overlay draw ON
	// TOP of her. Kept above the scene-room background (zIndex -1/-2) so she stays
	// visible, and she doesn't overlap the reels.
	const SCENE_Z_INDEX = -0.5;

	const isBonus = $derived(context.stateGame.gameType === 'freegame');

	const stillKey = $derived(isBonus ? 'ladyBonus' : 'ladyCharacter');
	const spineKey = $derived(isBonus ? 'ladyBonusSpine' : 'ladySpine');
	const aspect = $derived(isBonus ? BONUS_ASPECT : CHAR_ASPECT);

	type IdlePhase = 'breath' | 'mid' | 'move';
	let idlePhase = $state<IdlePhase>('breath');
	/** How many full ping-pong file plays completed in the current phase. */
	let phaseLoopsDone = $state(0);
	/** Bonus: full intro clip once, then dedicated short loop clip. */
	type BonusPhase = 'full' | 'loop';
	let bonusPhase = $state<BonusPhase>('full');

	const breathTexture = $derived(
		context.stateApp.loadedAssets?.['ladyIdleBreath'] as Texture | undefined,
	);
	const midTexture = $derived(
		context.stateApp.loadedAssets?.['ladyIdleMid'] as Texture | undefined,
	);
	const moveTexture = $derived(
		context.stateApp.loadedAssets?.['ladyIdleMove'] as Texture | undefined,
	);
	const bonusTexture = $derived(
		context.stateApp.loadedAssets?.['ladyIdleBonus'] as Texture | undefined,
	);
	const bonusLoopTexture = $derived(
		context.stateApp.loadedAssets?.['ladyIdleBonusLoop'] as Texture | undefined,
	);

	const baseIdleKey = $derived(
		idlePhase === 'breath'
			? 'ladyIdleBreath'
			: idlePhase === 'mid'
				? 'ladyIdleMid'
				: 'ladyIdleMove',
	);
	const bonusIdleKey = $derived(
		bonusPhase === 'loop' && bonusLoopTexture != null ? 'ladyIdleBonusLoop' : 'ladyIdleBonus',
	);
	const idleKey = $derived(isBonus && bonusTexture != null ? bonusIdleKey : baseIdleKey);

	const basePhaseTexture = $derived(
		idlePhase === 'breath'
			? breathTexture
			: idlePhase === 'mid'
				? midTexture
				: moveTexture,
	);
	const idleTexture = $derived(
		isBonus && bonusTexture != null
			? bonusPhase === 'loop' && bonusLoopTexture != null
				? bonusLoopTexture
				: bonusTexture
			: basePhaseTexture ?? breathTexture ?? midTexture ?? moveTexture,
	);
	const idleVideoEl = $derived(
		(idleTexture?.source as VideoSource | undefined)?.resource as
			| HTMLVideoElement
			| undefined,
	);
	// Prefer idle when either sequencer clip loaded (base) or bonus clip (freegame).
	const hasIdleVideo = $derived(
		isBonus
			? bonusTexture != null || breathTexture != null || midTexture != null || moveTexture != null
			: breathTexture != null || midTexture != null || moveTexture != null,
	);

	const nextBasePhase = (phase: IdlePhase): IdlePhase => {
		if (phase === 'breath') return midTexture != null ? 'mid' : 'move';
		if (phase === 'mid') return 'move';
		return 'breath';
	};
	const loopsForPhase = (phase: IdlePhase): number => {
		if (phase === 'breath') return BREATH_LOOPS;
		if (phase === 'mid') return MID_LOOPS;
		return MOVE_LOOPS;
	};
	const hasStill = $derived(context.stateApp.loadedAssets?.[stillKey] != null);
	// Spine only if idle webm missing (keeps quarantined/broken GodMode off-path)
	const hasSpine = $derived(
		!hasIdleVideo && context.stateApp.loadedAssets?.[spineKey] != null,
	);

	const muteVideo = (video: HTMLVideoElement) => {
		video.muted = true;
		video.defaultMuted = true;
		video.volume = 0;
		video.playsInline = true;
		video.setAttribute('playsinline', 'true');
		video.setAttribute('webkit-playsinline', 'true');
		video.setAttribute('muted', '');
		video.disableRemotePlayback = true;
	};

	const unmuteVideo = (video: HTMLVideoElement) => {
		video.muted = false;
		video.defaultMuted = false;
		video.volume = 1;
		video.playsInline = true;
		video.setAttribute('playsinline', 'true');
		video.setAttribute('webkit-playsinline', 'true');
		video.removeAttribute('muted');
		video.disableRemotePlayback = true;
	};

	const videoFromTexture = (tex: Texture | undefined): HTMLVideoElement | undefined => {
		const el = (tex?.source as VideoSource | undefined)?.resource;
		return el instanceof HTMLVideoElement ? el : undefined;
	};

	const pauseReset = (video: HTMLVideoElement | undefined) => {
		if (!video) return;
		video.pause();
		muteVideo(video);
		try {
			video.currentTime = 0;
		} catch {
			/* seek may fail before loaded */
		}
	};

	// ---- BASE: muted breath×5 → mid×1 → move×1 sequencer ----
	// Files already contain forward+reverse → loop=false; each 'ended' = 1 loop.
	$effect(() => {
		if (isBonus && bonusTexture != null) {
			// Bonus owns playback — keep base clips silent/paused.
			pauseReset(videoFromTexture(breathTexture));
			pauseReset(videoFromTexture(midTexture));
			pauseReset(videoFromTexture(moveTexture));
			return;
		}

		// Skip mid phase if asset missing (breath→move still works).
		if (idlePhase === 'mid' && midTexture == null) {
			idlePhase = 'move';
			phaseLoopsDone = 0;
			return;
		}

		const key = baseIdleKey;
		const phase = idlePhase;
		const tex = basePhaseTexture ?? breathTexture ?? midTexture ?? moveTexture;
		const video = videoFromTexture(tex);
		if (!video) {
			if (tex) {
				console.warn(`[SceneCharacter] idle asset ${key} loaded but is not HTMLVideoElement`);
			}
			return;
		}

		// Pause bonus + the other base clips so we never fight BGM / decode all.
		pauseReset(videoFromTexture(bonusTexture));
		pauseReset(videoFromTexture(bonusLoopTexture));
		const others = [
			videoFromTexture(breathTexture),
			videoFromTexture(midTexture),
			videoFromTexture(moveTexture),
		];
		for (const other of others) {
			if (!other || other === video) continue;
			other.pause();
			try {
				other.currentTime = 0;
			} catch {
				/* seek may fail before loaded */
			}
		}

		video.loop = false;
		muteVideo(video);
		try {
			if (video.ended || video.currentTime > 0.05) video.currentTime = 0;
		} catch {
			/* seek may fail before loaded */
		}

		const kick = () => {
			muteVideo(video);
			void video
				.play()
				.then(() => {
					const src = tex?.source as VideoSource | undefined;
					if (src && 'autoUpdate' in src) src.autoUpdate = true;
				})
				.catch((err) => {
					console.warn(`[SceneCharacter] idle play() blocked for ${key}`, err);
				});
		};
		kick();
		video.addEventListener('loadeddata', kick);
		video.addEventListener('canplay', kick);
		video.addEventListener('canplaythrough', kick);
		video.addEventListener('suspend', kick);
		video.addEventListener('stalled', kick);

		const onEnded = () => {
			const need = loopsForPhase(phase);
			const nextDone = phaseLoopsDone + 1;
			if (nextDone >= need) {
				phaseLoopsDone = 0;
				idlePhase = nextBasePhase(phase);
				return;
			}
			phaseLoopsDone = nextDone;
			try {
				video.currentTime = 0;
			} catch {
				/* ignore */
			}
			kick();
		};
		video.addEventListener('ended', onEnded);

		const t0 = video.currentTime;
		const proof = window.setTimeout(() => {
			const playing = !video.paused && !video.ended && video.readyState >= 2;
			const advanced = Math.abs(video.currentTime - t0) > 0.05;
			const payload = {
				mode: 'base',
				key,
				phase,
				phaseLoopsDone,
				breathLoops: BREATH_LOOPS,
				midLoops: MID_LOOPS,
				moveLoops: MOVE_LOOPS,
				paused: video.paused,
				ended: video.ended,
				readyState: video.readyState,
				currentTime: video.currentTime,
				duration: video.duration,
				advanced,
				playing,
				loop: video.loop,
				muted: video.muted,
				videoWidth: video.videoWidth,
				videoHeight: video.videoHeight,
			};
			(window as unknown as { __ladyIdleProof?: typeof payload }).__ladyIdleProof = payload;
			console.info('[SceneCharacter] idle video proof', payload);
			if (!advanced || !playing) {
				console.warn(
					`[SceneCharacter] idle webm not advancing for ${key} — check decode/autoplay`,
				);
			}
		}, 700);

		return () => {
			window.clearTimeout(proof);
			video.removeEventListener('ended', onEnded);
			video.removeEventListener('loadeddata', kick);
			video.removeEventListener('canplay', kick);
			video.removeEventListener('canplaythrough', kick);
			video.removeEventListener('suspend', kick);
			video.removeEventListener('stalled', kick);
		};
	});

	// Keep base sequencer clips paused whenever freegame owns the slot
	// (separate from bonus playback so late-loading breath/mid/move don't restart).
	$effect(() => {
		if (!isBonus || bonusTexture == null) return;
		pauseReset(videoFromTexture(breathTexture));
		pauseReset(videoFromTexture(midTexture));
		pauseReset(videoFromTexture(moveTexture));
	});

	// Reset bonus intro→loop phase when leaving freegame.
	$effect(() => {
		if (isBonus && bonusTexture != null) return;
		bonusPhase = 'full';
		pauseReset(videoFromTexture(bonusTexture));
		pauseReset(videoFromTexture(bonusLoopTexture));
	});

	const kickBonusPlay = (video: HTMLVideoElement, tex: Texture) => {
		unmuteVideo(video);
		void video
			.play()
			.then(() => {
				const src = tex.source as VideoSource | undefined;
				if (src && 'autoUpdate' in src) src.autoUpdate = true;
			})
			.catch((err) => {
				// Autoplay-with-sound can fail if gesture chain was lost —
				// retry muted then immediately unmute (keeps visual alive).
				console.warn('[SceneCharacter] bonus play() with audio blocked; retry', err);
				muteVideo(video);
				void video
					.play()
					.then(() => {
						unmuteVideo(video);
						const src = tex.source as VideoSource | undefined;
						if (src && 'autoUpdate' in src) src.autoUpdate = true;
					})
					.catch((err2) => {
						console.warn('[SceneCharacter] bonus play() blocked', err2);
					});
			});
	};

	// ---- BONUS: unmuted intro once (A fwd→A rev) → SWAP to C ping-pong loop ----
	$effect(() => {
		if (!isBonus || bonusTexture == null) return;

		const fullVideo = videoFromTexture(bonusTexture);
		if (!fullVideo) {
			console.warn('[SceneCharacter] ladyIdleBonus loaded but is not HTMLVideoElement');
			return;
		}
		const loopVideo = videoFromTexture(bonusLoopTexture);

		// --- LOOP PHASE: dedicated short clip, native loop (no long-file seek) ---
		if (bonusPhase === 'loop' && loopVideo && bonusLoopTexture) {
			fullVideo.pause();
			muteVideo(fullVideo);

			loopVideo.loop = true;
			unmuteVideo(loopVideo);
			try {
				if (loopVideo.ended || loopVideo.currentTime > 0.05) loopVideo.currentTime = 0;
			} catch {
				/* seek may fail before loaded */
			}

			const kick = () => kickBonusPlay(loopVideo, bonusLoopTexture);
			kick();
			loopVideo.addEventListener('loadeddata', kick);
			loopVideo.addEventListener('canplay', kick);
			loopVideo.addEventListener('canplaythrough', kick);

			const payload = {
				mode: 'bonus',
				phase: 'loop' as const,
				key: 'ladyIdleBonusLoop',
				paused: loopVideo.paused,
				ended: loopVideo.ended,
				readyState: loopVideo.readyState,
				currentTime: loopVideo.currentTime,
				duration: loopVideo.duration,
				loop: loopVideo.loop,
				muted: loopVideo.muted,
				volume: loopVideo.volume,
			};
			(window as unknown as { __ladyIdleProof?: typeof payload }).__ladyIdleProof = payload;
			console.info('[SceneCharacter] bonus idle → loop clip', payload);

			return () => {
				loopVideo.removeEventListener('loadeddata', kick);
				loopVideo.removeEventListener('canplay', kick);
				loopVideo.removeEventListener('canplaythrough', kick);
			};
		}

		// --- FULL PHASE: play intro once; preload/warm decode the loop clip ---
		if (loopVideo) {
			loopVideo.loop = true;
			loopVideo.preload = 'auto';
			// Mute while warming — do not overlap intro bed audio.
			muteVideo(loopVideo);
			loopVideo.pause();
			try {
				loopVideo.currentTime = 0;
			} catch {
				/* ignore */
			}
			// Decode first frame so handoff is ready when full ends.
			const warm = () => {
				if (bonusPhase !== 'full') return;
				muteVideo(loopVideo);
				void loopVideo
					.play()
					.then(() => {
						if (bonusPhase !== 'full') return;
						loopVideo.pause();
						muteVideo(loopVideo);
						try {
							loopVideo.currentTime = 0;
						} catch {
							/* ignore */
						}
					})
					.catch(() => {});
			};
			if (loopVideo.readyState >= 2) warm();
			else loopVideo.addEventListener('canplay', warm, { once: true });
		}

		fullVideo.loop = false;
		unmuteVideo(fullVideo);
		try {
			fullVideo.currentTime = 0;
		} catch {
			/* seek may fail before loaded */
		}

		const kick = () => kickBonusPlay(fullVideo, bonusTexture);
		kick();
		fullVideo.addEventListener('loadeddata', kick);
		fullVideo.addEventListener('canplay', kick);
		fullVideo.addEventListener('canplaythrough', kick);

		const onEnded = () => {
			if (loopVideo && bonusLoopTexture) {
				// Instant swap to short clip — no seek on the long file.
				bonusPhase = 'loop';
				fullVideo.pause();
				muteVideo(fullVideo);
				return;
			}
			// Fallback if loop asset missing: cheap seek-to-0 on full (not ideal).
			try {
				fullVideo.currentTime = 0;
			} catch {
				/* ignore */
			}
			unmuteVideo(fullVideo);
			fullVideo.play().catch(() => {});
		};
		fullVideo.addEventListener('ended', onEnded);

		const t0 = fullVideo.currentTime;
		const proof = window.setTimeout(() => {
			const playing = !fullVideo.paused && !fullVideo.ended && fullVideo.readyState >= 2;
			const advanced = Math.abs(fullVideo.currentTime - t0) > 0.05;
			const payload = {
				mode: 'bonus',
				phase: 'full' as const,
				key: 'ladyIdleBonus',
				hasLoopAsset: loopVideo != null,
				paused: fullVideo.paused,
				ended: fullVideo.ended,
				readyState: fullVideo.readyState,
				currentTime: fullVideo.currentTime,
				duration: fullVideo.duration,
				advanced,
				playing,
				loop: fullVideo.loop,
				muted: fullVideo.muted,
				volume: fullVideo.volume,
				videoWidth: fullVideo.videoWidth,
				videoHeight: fullVideo.videoHeight,
			};
			(window as unknown as { __ladyIdleProof?: typeof payload }).__ladyIdleProof = payload;
			console.info('[SceneCharacter] bonus idle video proof', payload);
		}, 700);

		return () => {
			window.clearTimeout(proof);
			fullVideo.removeEventListener('ended', onEnded);
			fullVideo.removeEventListener('loadeddata', kick);
			fullVideo.removeEventListener('canplay', kick);
			fullVideo.removeEventListener('canplaythrough', kick);
			// Leaving freegame / effect re-run: silence both bonus clips.
			if (!isBonus) {
				pauseReset(fullVideo);
				pauseReset(loopVideo);
			}
		};
	});

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
	const idleRotation = $derived(hasSpine ? 0 : 0.008 * Math.sin(time * 0.35 + 0.5));
	const idleScaleY = $derived(hasSpine ? 1 : 1 + 0.01 * breath);
	const idleScaleX = $derived(hasSpine ? 1 : 1 - 0.005 * breath);
	// fluorescent observation flicker (hard on/off) — NOT soft séance aura bloom
	const fluoroOn = $derived(!hasSpine && Math.sin(time * 13.5) > 0.55);
	const fluoroAlpha = $derived(fluoroOn ? 0.14 : 0);

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
		{#if hasIdleVideo}
			<!-- Preferred: Patient alpha-webm (base breath/mid/move OR bonus v6 / v10_loop) -->
			<Sprite
				key={idleKey}
				x={layout.cx}
				y={layout.yHem}
				anchor={{ x: 0.5, y: ANCHOR_Y }}
				width={layout.width}
				height={layout.height}
			/>
		{:else if hasSpine}
			<!-- floating cut-out Spine rig (only when idle webm absent). -->
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
		{:else if hasStill}
			<!-- still fallback: hem-pinned; fluorescent strobe silhouette (no additive aura) -->
			<Container
				x={layout.cx}
				y={layout.yHem}
				rotation={idleRotation}
				scale={{ x: idleScaleX, y: idleScaleY }}
			>
				{#if fluoroAlpha > 0.001}
					<Sprite
						key={stillKey}
						anchor={{ x: 0.5, y: ANCHOR_Y }}
						width={layout.width * 1.02}
						height={layout.height * 1.02}
						tint={0xf4f1ec}
						blendMode={'screen'}
						alpha={fluoroAlpha}
					/>
				{/if}
				<Sprite
					key={stillKey}
					anchor={{ x: 0.5, y: ANCHOR_Y }}
					width={layout.width}
					height={layout.height}
				/>
			</Container>
		{/if}
	{/if}
</MainContainer>
</Container>
