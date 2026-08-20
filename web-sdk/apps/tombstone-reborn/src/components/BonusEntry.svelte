<script lang="ts" module>
	import type { BonusEntryTier } from '../game/bonusEntryArt';

	/**
	 * SOUND HOOKS. This component owns no audio — these two events are the hooks
	 * the audio agent attaches to (see the header comment for the requested keys).
	 *
	 * `bonusEntryShow` is broadcast with broadcastAsync and AWAITED by
	 * freeSpinTrigger — after the trigger spin's scatters and wins have
	 * already resolved. `bonusEntryHandoff` fires as the banner lets go.
	 */
	export type EmitterEventBonusEntry =
		| { type: 'bonusEntryShow'; tier: BonusEntryTier }
		| { type: 'bonusEntryHandoff'; tier: BonusEntryTier };
</script>

<script lang="ts">
	/**
	 * TOMBSTONE REBORN bonus-entry banner.
	 *
	 * Announces the bonus AFTER the trigger spin has fully resolved (scatters
	 * landed, any wins paid). Bought and natural use the same beat:
	 *
	 *   freespins     THE WAKE      10 spins, special bar awake
	 *   superspins    THE RECKONING 10 spins, grave lane open
	 *
	 * Fired from freeSpinTrigger. The room grades behind this veil; the first
	 * freegame reveal after hand-off drops the bonus deck.
	 *
	 * Wait screen: the banner stays up until PRESS ANYWHERE / Space / stop,
	 * or a 5-minute safety auto-start if nobody taps. Entrance tweens still
	 * follow turbo via fxDur; the wait itself does not. A missing hero plate
	 * resolves immediately so a bought round cannot wedge.
	 *
	 * SOUND, one sting per tier plus the hand-off accent:
	 *   sfx_bonus_entry_small    DEAD MAN'S HAND entry: cards riffled and slapped
	 *                            down on plank, a tin star ringing, low bass hit
	 *   sfx_bonus_entry_super    OPEN GRAVE entry: coffin lid splintering, earth
	 *                            tearing, a rising brass swell over it
	 *   sfx_bonus_handoff        the accent as the banner clears into the spin:
	 *                            a hammer cocking and a dust-settle tail
	 * The sting is broadcast from the bonusEntryShow handler rather than from an
	 * effect on `tier`, so it fires once per bought round and cannot re-trigger
	 * when a tween or a resize re-runs the entrance. The hand-off rides finish(),
	 * which is already guarded to run once by `handedOff`.
	 *
	 * Performance: every animated layer is a sprite transform. The only Graphics in
	 * the tree are Rectangles with constant geometry, so nothing redraws per frame.
	 */
	import { Tween } from 'svelte/motion';
	import { backOut, cubicOut } from 'svelte/easing';
	import type { Texture } from 'pixi.js';
	import { BaseSprite, Container, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { CanvasSizeRectangle, MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnHotkey } from 'components-shared';
	import { waitForResolve } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import type { SoundEffectName } from '../game/sound';
	import { SYMBOL_SIZE } from '../game/constants';
	import { atmosphereFromMode, syncAtmosphere } from '../game/atmosphere.svelte';
	import { fxDur } from '../game/fxTiming';
	import {
		WIN_CELEB_LIGHT_ASSET,
		WIN_CELEB_VFX_ASSET,
		WIN_LIGHT,
		WIN_VFX,
		WIN_VFX_CELL,
		winRand,
	} from '../game/winCelebrationArt';
	import { BONUS_ENTRY_ART, BONUS_PALETTE } from '../game/bonusEntryArt';
	import { playBonusWait, stopBonusWait } from '../game/bonusBgm';
	import {
		TR_INK_IRON,
		fitFontSize,
		trAccentStyle,
		trHeroTitleStyle,
		trLabelStyle,
	} from '../game/typography';

	const context = getContext();

	/** Which sting announces each bought mode. The bonus ROUNDS reuse the
	 * matching single-spin stings until they get their own recordings. */
	const ENTRY_SFX: Record<BonusEntryTier, SoundEffectName> = {
		bonus_small: 'sfx_bonus_entry_small',
		bonus_super: 'sfx_bonus_entry_super',
		freespins: 'sfx_bonus_entry_small',
		superspins: 'sfx_bonus_entry_super',
	};

	/** Banner stays until a press, or this long — then the round auto-starts. */
	const BANNER_WAIT_MAX_MS = 5 * 60 * 1000;

	let tier = $state<BonusEntryTier | null>(null);
	let oncomplete = $state(() => {});
	let handedOff = false;

	const art = $derived(tier ? BONUS_ENTRY_ART[tier] : null);

	/** Grade the room to the tier's atmosphere. Called once the dark veil is
	 * fully up, so the background crossfade happens BEHIND the banner instead
	 * of in the player's face — this banner is now the ONLY place the room
	 * flips on a bonus entry (bought, natural or the small→super upgrade). */
	const gradeRoom = (forTier: BonusEntryTier) => {
		syncAtmosphere(atmosphereFromMode(forTier) ?? 'small');
	};

	/** Resolve the awaited `bonusEntryShow` exactly once and unmount. */
	const finish = () => {
		if (tier === null || handedOff) return;
		handedOff = true;
		// A tap can skip the banner before the veil-cover timer fires; the round
		// is entered either way, so make sure the room is graded before we let
		// go of the screen. syncAtmosphere no-ops when already there.
		gradeRoom(tier);
		stopBonusWait();
		context.eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_bonus_handoff' });
		context.eventEmitter.broadcast({ type: 'bonusEntryHandoff', tier });
		oncomplete();
		tier = null;
	};

	const broadcastSkip = () => {
		if (tier === null) return;
		context.eventEmitter.broadcast({ type: 'stopButtonClick' });
	};

	context.eventEmitter.subscribeOnMount({
		bonusEntryShow: async (emitterEvent) => {
			handedOff = false;
			// A missing hero plate must never wedge the bought round: resolve
			// straight away rather than mounting a Sprite on an unloaded key.
			const plateKey = BONUS_ENTRY_ART[emitterEvent.tier].plateKey;
			if (!context.stateApp.loadedAssets?.[plateKey]) {
				console.error(
					`[BonusEntry] hero plate "${plateKey}" missing from loadedAssets — skipping banner`,
				);
				return;
			}
			tier = emitterEvent.tier;
			// After the plate check, so a skipped banner stays silent rather than
			// announcing a takeover the player never sees. Wait bed loops until
			// PRESS ANYWHERE / auto hand-off, then the bonus score starts.
			playBonusWait(emitterEvent.tier);
			context.eventEmitter.broadcast({
				type: 'soundOnce',
				name: ENTRY_SFX[emitterEvent.tier],
			});
			// Flip the room's atmosphere once the veil has fully covered the
			// screen (its fade-in is fxDur(220)): the old→new background
			// crossfade plays out hidden behind the dark overlay, and the reels
			// underneath keep the faces they were dealt — the new deck only
			// arrives with the first reveal after the banner hands off.
			const cover = window.setTimeout(() => gradeRoom(emitterEvent.tier), fxDur(240));
			const safety = window.setTimeout(() => {
				console.warn('[BonusEntry] banner wait elapsed — auto starting');
				finish();
			}, BANNER_WAIT_MAX_MS);
			try {
				await waitForResolve((resolve) => (oncomplete = resolve));
			} finally {
				window.clearTimeout(cover);
				window.clearTimeout(safety);
			}
		},
		// PRESS ANYWHERE / Space / HUD stop — the only way out before 5 minutes.
		stopButtonClick: () => finish(),
	});

	// ------------------------------------------------------------------
	// entrance + hold
	// ------------------------------------------------------------------
	/** 1 → 0 over the entry punch: drives the starburst, streaks and flares. */
	const pop = new Tween(0);
	/** slam settle on the frame */
	const slam = new Tween(1);
	/** slow Ken-Burns push on the hero plate */
	const zoom = new Tween(1);
	/** 0 → 1 fade of the whole banner, and back to 0 on hand-off */
	const veil = new Tween(0);

	let time = $state(0);

	$effect(() => {
		const current = art;
		if (current === null) return;
		// Entrance only. The banner then waits for a press (or the 5-minute
		// auto-start). Turbo still shortens the slam, not the wait.
		const isSuper = current.rings > 0;
		veil.set(0, { duration: 0 });
		veil.set(1, { duration: fxDur(220) });
		pop.set(1, { duration: 0 });
		pop.set(0, { duration: fxDur(isSuper ? 1200 : 900), easing: cubicOut });
		slam.set(isSuper ? 1.26 : 1.12, { duration: 0 });
		slam.set(1, { duration: fxDur(isSuper ? 640 : 440), easing: backOut });
		zoom.set(1, { duration: 0 });
		zoom.set(current.push, { duration: fxDur(current.holdMs + 1500), easing: cubicOut });
	});

	$effect(() => {
		if (tier === null) return;
		let raf = 0;
		const start = performance.now();
		const tick = (now: number) => {
			time = (now - start) / 1000;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});

	// ------------------------------------------------------------------
	// art
	// ------------------------------------------------------------------
	const lightTextures = $derived(
		(context.stateApp.loadedAssets?.[WIN_CELEB_LIGHT_ASSET] as Texture[] | undefined) ?? [],
	);
	const vfxTextures = $derived(
		(context.stateApp.loadedAssets?.[WIN_CELEB_VFX_ASSET] as Texture[] | undefined) ?? [],
	);
	const light = (index: number) => lightTextures[index];
	const vfx = (index: number) => vfxTextures[index];
	const frameLoaded = $derived(
		art !== null && Boolean(context.stateApp.loadedAssets?.[art.frameKey]),
	);

	// ------------------------------------------------------------------
	// geometry — same construction as the win takeover, so the two surfaces
	// sit at the same size and the frame window stays aligned to the plate
	// ------------------------------------------------------------------
	const boardW = $derived(context.stateGameDerived.boardLayout().width);
	const frameW = $derived(boardW * 1.02);
	const frameH = $derived(frameW * (9 / 16));
	const padFrac = $derived(art?.framePadFrac ?? 74 / 1280);
	const frameOuterW = $derived(frameW * (1 + padFrac * 2));
	const frameOuterH = $derived(frameH + frameW * padFrac * 2);

	/** CSS object-fit: cover — fill the window, crop overflow, never letterbox. */
	const plateCover = $derived.by(() => {
		const scale = Math.max(frameW / 1280, frameH / 720);
		return { width: 1280 * scale, height: 720 * scale };
	});

	const mainW = $derived(context.stateLayoutDerived.mainLayout().width);
	const mainH = $derived(context.stateLayoutDerived.mainLayout().height);
	const contentH = $derived(frameOuterH + SYMBOL_SIZE * 1.9);
	const fit = $derived(Math.min(1, (mainH * 0.94) / contentH));
	const centerShift = $derived(SYMBOL_SIZE * 0.8);
	const fieldW = $derived(mainW / Math.max(fit, 0.2));
	const fieldH = $derived(mainH / Math.max(fit, 0.2));

	// ------------------------------------------------------------------
	// animated layers — allocated at the SUPER count and modulated by alpha,
	// so switching tier never churns the display list
	// ------------------------------------------------------------------
	const RAYS = Array.from({ length: 10 }, (_, i) => i);
	const EMBERS = Array.from({ length: 62 }, (_, i) => i);
	const STREAKS = Array.from({ length: 22 }, (_, i) => i);
	const DUST = Array.from({ length: 6 }, (_, i) => i);

	const kick = $derived(pop.current * (art?.kick ?? 0));
	const kickX = $derived((winRand(Math.floor(time * 40) * 7 + 3) - 0.5) * kick);
	const kickY = $derived((winRand(Math.floor(time * 40)) - 0.5) * kick);
	/** lantern breathe — never a hard strobe, the plates are high contrast */
	const lantern = $derived(0.9 + 0.1 * Math.sin(time * 1.7));

	// ------------------------------------------------------------------
	// type — every face comes from the shared typography tokens
	// ------------------------------------------------------------------
	const titlePlateW = $derived(frameW * 0.78);
	const titlePlateH = $derived(SYMBOL_SIZE * 0.82);
	const titleY = $derived(frameOuterH / 2 - titlePlateH * 0.15);
	const TITLE_SPACING = 2;
	const titleSize = $derived(
		fitFontSize(art?.title ?? '', {
			role: 'display',
			base: titlePlateH * 0.56,
			maxWidth: titlePlateW * 0.86,
			min: 20,
			letterSpacing: TITLE_SPACING,
		}),
	);
	const subtitleSize = $derived(
		fitFontSize(art?.subtitle ?? '', {
			role: 'accent',
			base: SYMBOL_SIZE * 0.2,
			maxWidth: frameW * 0.82,
			min: 10,
			letterSpacing: 1,
		}),
	);
	const pressSize = $derived(SYMBOL_SIZE * 0.17);
</script>

{#if art !== null && tier !== null}
	<!-- Deep enough that the HUD cannot read through it. The graveyard behind
		still shows as silhouette and light, just not as copy. -->
	<CanvasSizeRectangle
		backgroundColor={0x07060a}
		backgroundAlpha={(art.rings > 0 ? 0.96 : 0.94) * veil.current}
	/>
	<MainContainer>
		<Container x={mainW * 0.5} y={mainH * 0.5}>
			<Container x={kickX} y={kickY - centerShift} scale={fit} alpha={veil.current}>
				<!-- god-rays raking down behind the frame -->
				{#if light(WIN_LIGHT.rayFan)}
					<Container alpha={art.rayAlpha * lantern}>
						{#each RAYS as index (index)}
							{#if index < art.rays}
								{@const seed = index * 3 + 1}
								{@const sway = Math.sin(time * (0.16 + winRand(seed) * 0.22) + index) * 0.09}
								{@const spread = (index / Math.max(art.rays - 1, 1) - 0.5) * 1.5}
								<BaseSprite
									texture={index % 3 === 0
										? light(WIN_LIGHT.rayStreaks)
										: index % 3 === 1
											? light(WIN_LIGHT.rayFan)
											: light(WIN_LIGHT.rayCone)}
									anchor={{ x: 0.5, y: 0 }}
									x={spread * frameW * 0.42}
									y={-frameOuterH * 0.62}
									width={frameW * (0.3 + winRand(seed * 5) * 0.22)}
									height={fieldH * 0.92}
									rotation={spread * 0.3 + sway}
									blendMode="add"
									alpha={0.55 + 0.45 * winRand(seed * 11)}
								/>
							{/if}
						{/each}
					</Container>
				{/if}

				<!-- warm lantern bloom behind the panel -->
				{#if light(WIN_LIGHT.glowWarm)}
					<BaseSprite
						texture={light(WIN_LIGHT.glowWarm)}
						anchor={0.5}
						width={frameOuterW * 1.5}
						height={frameOuterH * 1.7}
						blendMode="add"
						alpha={0.2 + art.rayAlpha * 0.45 * lantern}
					/>
				{/if}

				<!-- OPEN GRAVE only: gold rings rolling out of the opened grave -->
				{#if art.rings > 0 && light(WIN_LIGHT.ringSoft)}
					{#each [0, 1, 2] as ring (ring)}
						{@const phase = (time * art.rings + ring / 3) % 1}
						<BaseSprite
							texture={ring % 2 === 0 ? light(WIN_LIGHT.ringSoft) : light(WIN_LIGHT.ringHard)}
							anchor={0.5}
							width={frameOuterW * (0.35 + phase * 1.5)}
							height={frameOuterW * (0.35 + phase * 1.5)}
							blendMode="add"
							alpha={0.45 * (1 - phase) * (1 - phase)}
						/>
					{/each}
				{/if}

				<Container scale={slam.current}>
					<!-- hero plate, cover-fit into the frame window, Ken-Burns push -->
					<Container alpha={lantern}>
						<Rectangle isMask anchor={0.5} width={frameW} height={frameH} borderRadius={2} />
						<Sprite
							key={art.plateKey}
							anchor={0.5}
							width={plateCover.width * zoom.current}
							height={plateCover.height * zoom.current}
							x={Math.sin(time * 0.22) * frameW * 0.008}
						/>

						<!-- grave dust drifting across the plate -->
						{#if vfx(WIN_VFX.dustPuffA)}
							{#each DUST as index (index)}
								{#if index < art.dust}
									{@const seed = index * 7 + 2}
									{@const drift = (time * (0.045 + winRand(seed) * 0.05) + winRand(seed * 3)) % 1}
									<BaseSprite
										texture={index % 3 === 0
											? vfx(WIN_VFX.dustPlume)
											: index % 2 === 0
												? vfx(WIN_VFX.dustPuffA)
												: vfx(WIN_VFX.dustPuffB)}
										anchor={0.5}
										x={(drift - 0.5) * frameW * 1.7}
										y={(winRand(seed * 5) - 0.3) * frameH * 0.62}
										width={frameW * (0.24 + winRand(seed * 9) * 0.3)}
										height={frameW * (0.24 + winRand(seed * 9) * 0.3)}
										rotation={winRand(seed * 13) * 6.28}
										alpha={0.3 * Math.sin(drift * Math.PI)}
									/>
								{/if}
							{/each}
						{/if}
					</Container>

					<!-- weathered timber + branded-iron frame. SMALL wears the win
						ladder's frame; OPEN GRAVE gets the heavier build. -->
					{#if frameLoaded}
						<Sprite key={art.frameKey} anchor={0.5} width={frameOuterW} height={frameOuterH} />
					{/if}
				</Container>

				<!-- entry punch: gold starburst + radiating spark streaks -->
				{#if pop.current > 0.01 && vfx(WIN_VFX.starburst)}
					{@const burst = 1 - pop.current}
					<BaseSprite
						texture={vfx(WIN_VFX.starburst)}
						anchor={0.5}
						width={frameW * art.popScale * (0.35 + burst * 1.1)}
						height={frameW * art.popScale * (0.35 + burst * 1.1)}
						rotation={burst * 0.5}
						blendMode="add"
						alpha={pop.current}
					/>
					<BaseSprite
						texture={vfx(WIN_VFX.flashPop)}
						anchor={0.5}
						width={frameW * art.popScale * (0.2 + burst * 0.9)}
						height={frameW * art.popScale * (0.2 + burst * 0.9)}
						blendMode="add"
						alpha={pop.current * 0.85}
					/>
					{#each STREAKS as index (index)}
						{#if index < art.streaks}
							{@const angle = (index / art.streaks) * Math.PI * 2 + winRand(index) * 0.3}
							{@const reach = burst * frameW * 0.5 * (0.6 + winRand(index * 3) * 0.7)}
							<BaseSprite
								texture={index % 4 === 0 ? vfx(WIN_VFX.starPoint) : vfx(WIN_VFX.sparkStreak)}
								anchor={0.5}
								x={Math.cos(angle) * reach}
								y={Math.sin(angle) * reach}
								width={frameW * 0.12}
								height={frameW * 0.12}
								rotation={angle + Math.PI / 2}
								blendMode="add"
								alpha={pop.current * 0.9}
							/>
						{/if}
					{/each}
					<!-- OPEN GRAVE only: muzzle flares raking in from both sides -->
					{#each [-1, 1] as side (side)}
						{#if art.flares > 0 && vfx(WIN_VFX.muzzleWide)}
							<BaseSprite
								texture={side < 0 ? vfx(WIN_VFX.muzzleFlare) : vfx(WIN_VFX.muzzleWide)}
								anchor={0.5}
								x={side * frameW * (0.62 - burst * 0.2)}
								y={frameH * 0.06}
								scale={{
									x: side * ((frameW * 0.5) / WIN_VFX_CELL),
									y: (frameW * 0.5) / WIN_VFX_CELL,
								}}
								blendMode="add"
								alpha={pop.current * 0.8}
							/>
						{/if}
					{/each}
				{/if}

				<!-- rising gold embers over the whole banner -->
				{#if vfx(WIN_VFX.emberMote)}
					{#each EMBERS as index (index)}
						{#if index < art.embers}
							{@const seed = index * 13 + 4}
							{@const speed = 0.055 + winRand(seed) * 0.12}
							{@const phase = (time * speed + winRand(seed * 3)) % 1}
							{@const size = fieldW * (0.006 + winRand(seed * 7) * 0.014)}
							<BaseSprite
								texture={index % 5 === 0 ? vfx(WIN_VFX.starSmall) : vfx(WIN_VFX.emberMote)}
								anchor={0.5}
								x={(winRand(seed * 5) - 0.5) * fieldW +
									Math.sin(time * 0.7 + index) * fieldW * 0.012}
								y={(0.55 - phase) * fieldH}
								width={size}
								height={size}
								rotation={time * (0.4 + winRand(seed * 11))}
								blendMode="add"
								alpha={0.75 * Math.sin(phase * Math.PI)}
							/>
						{/if}
					{/each}
				{/if}

				<!-- tier title: branded iron plate nailed across the frame's bottom
					edge, revolver emblems flanking, gold serif display face -->
				<Container y={titleY} scale={slam.current}>
					<Rectangle
						anchor={0.5}
						width={titlePlateW}
						height={titlePlateH}
						borderRadius={4}
						backgroundColor={BONUS_PALETTE.iron}
						backgroundAlpha={0.94}
						borderColor={BONUS_PALETTE.gold}
						borderWidth={art.rings > 0 ? 3 : 2}
						borderAlpha={0.85}
					/>
					{#if vfx(WIN_VFX.revolverEmblem)}
						{#each [-1, 1] as side (side)}
							{@const emblem = (titlePlateH * 1.5) / WIN_VFX_CELL}
							<!-- negative x scale mirrors the revolver so the pair face
								outward; scale rather than width/height because those two
								props fight each other on a PIXI.Sprite -->
							<BaseSprite
								texture={vfx(WIN_VFX.revolverEmblem)}
								anchor={0.5}
								x={side * titlePlateW * 0.56}
								scale={{ x: side * emblem, y: emblem }}
								alpha={0.85}
							/>
						{/each}
					{/if}
					<Text
						anchor={0.5}
						text={art.title}
						eventMode="none"
						style={trHeroTitleStyle({
							fontSize: titleSize,
							metal: 'gold',
							letterSpacing: TITLE_SPACING,
						})}
					/>
				</Container>

				<!-- the mechanic, in one line. Says ONE SPIN so nothing here can be
					read as a run of free spins. -->
				<Container y={titleY + titlePlateH * 0.86}>
					<Text
						anchor={0.5}
						text={art.subtitle}
						eventMode="none"
						style={trAccentStyle({
							fontSize: subtitleSize,
							fill: BONUS_PALETTE.boneDust,
							letterSpacing: 1,
							stroke: { color: TR_INK_IRON, width: subtitleSize * 0.16, join: 'round' },
						})}
					/>
				</Container>

				<!-- stays up until this is pressed, or 5 minutes elapse -->
				<Container
					y={titleY + titlePlateH * 1.52}
					alpha={0.66 + 0.2 * Math.sin(time * 3.2)}
				>
					<Text
						anchor={0.5}
						text="PRESS ANYWHERE"
						eventMode="none"
						style={trLabelStyle({
							fontSize: pressSize,
							fill: BONUS_PALETTE.goldPale,
							letterSpacing: 3,
						})}
					/>
				</Container>
			</Container>
		</Container>
	</MainContainer>

	<!-- Both skip paths, exactly as the win takeover wires them. -->
	<OnHotkey hotkey="Space" onpress={broadcastSkip} />
	<OnPressFullScreen onpress={broadcastSkip} />
{/if}
