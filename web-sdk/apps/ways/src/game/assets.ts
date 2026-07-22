export default {
	// template 'loader' spine removed: Mining-Mayhem miner face + logotype,
	// preloaded on every session but never rendered
	// in this app (LoadingScreen uses the mirrorLoading painting instead)
	pressToContinueText: {
		type: 'sprites',
		src: new URL('../../assets/sprites/pressToContinueText/MM_pressanywhere.json', import.meta.url).href,
		preload: true,
	},
	// Madam Mirror symbol spines (new schema). Shared atlas mm_symbols; each
	// rig is authored 1:1 (scale 1, unlike the legacy scale-2 template rigs)
	// with win / land / postWin animations and class-tinted FX layers. The
	// card is a deformable mesh so postWin ripples the artwork itself.
	H1: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/h1.json', import.meta.url).href,
			scale: 1,
		},
	},
	H2: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/h2.json', import.meta.url).href,
			scale: 1,
		},
	},
	H3: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/h3.json', import.meta.url).href,
			scale: 1,
		},
	},
	H4: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/h4.json', import.meta.url).href,
			scale: 1,
		},
	},
	H5: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/h5.json', import.meta.url).href,
			scale: 1,
		},
	},
	L1: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/l1.json', import.meta.url).href,
			scale: 1,
		},
	},
	L2: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/l2.json', import.meta.url).href,
			scale: 1,
		},
	},
	L3: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/l3.json', import.meta.url).href,
			scale: 1,
		},
	},
	L4: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/l4.json', import.meta.url).href,
			scale: 1,
		},
	},
	L5: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/l5.json', import.meta.url).href,
			scale: 1,
		},
	},
	W: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/w.json', import.meta.url).href,
			scale: 1,
		},
	},
	S: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/s.json', import.meta.url).href,
			scale: 1,
		},
	},
	HM: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/mm_symbols/mm_symbols.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/mm_symbols/hm.json', import.meta.url).href,
			scale: 1,
		},
	},
	explosion: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/symbols3/symbols3.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/symbols3/explosion.json', import.meta.url).href,
			scale: 2,
		},
	},
	reelsFrame: {
		type: 'sprites',
		src: new URL('../../assets/sprites/reelsFrame/reels_frame.json', import.meta.url).href,
	},
	// template 'payFrame' sprite removed: loaded but never referenced
	anticipation: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/anticipation/anticipation.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/anticipation/anticipation.json', import.meta.url).href,
			scale: 2,
		},
	},
	goldFont: {
		type: 'font',
		src: new URL('../../assets/fonts/goldFont/mm_gold.xml', import.meta.url).href,
	},
	// template 'goldBlur' font removed: gold mining blur numerals, no component
	// ever set fontFamily 'goldblur' (spin blur is baked into symbolsStatic)
	silverFont: {
		type: 'font',
		src: new URL('../../assets/fonts/silverFont/mm_silver.xml', import.meta.url).href,
	},
	purpleFont: {
		type: 'font',
		src: new URL('../../assets/fonts/purpleFont/mm_purple.xml', import.meta.url).href,
	},
	// absinthe-green Ghastly Panic variant (channel-swapped from goldFont by
	// tools/make_ghost_font.py) — used for spectral/apparition numerals
	ghostFont: {
		type: 'font',
		src: new URL('../../assets/fonts/ghostFont/mm_ghost.xml', import.meta.url).href,
	},
	// violet Ghastly Panic variant (hue-rotated from goldFont by
	// tools/make_amethyst_font.py) — used for the YOU WON amount
	amethystFont: {
		type: 'font',
		src: new URL('../../assets/fonts/amethystFont/mm_amethyst.xml', import.meta.url).href,
	},
	// template 'bigwin' + 'globalMultiplier' spines removed: gold-western
	// Mining-Mayhem art, superseded by the WinCelebration film reels and the
	// WaysCounter plaque; neither was rendered anywhere in this app
	// template 'fsIntro' / 'fsIntroNumber' / 'fsOutroNumber' spines removed:
	// the Mining-Mayhem plank panel + bracket frame behind the old free-spin
	// intro/outro; superseded by the bespoke haunted-mirror panels
	// (mirrorFsIntro* / mirrorFsOutro) rendered by FreeSpinIntro/FreeSpinOutro
	// template 'foregroundAnimation' / 'foregroundFeatureAnimation' spines
	// removed: the Mining-Mayhem crystal-mine backgrounds were preloaded on
	// every session but Background.svelte renders the mirror parlor paintings
	// (mirrorBgBase / mirrorBgFreespin) instead. 'tumble_*' spines removed:
	// ways games never tumble; nothing referenced them.
	reelhouse: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/reelhouse/reelhouse_glow.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/reelhouse/reelhouse_glow.json', import.meta.url).href,
			scale: 2,
		},
	},
	progressBar: {
		type: 'sprites',
		src: new URL('../../assets/sprites/progressBar/progressBar.json', import.meta.url).href,
		preload: true,
	},
	// template 'freeSpins' + 'winSmall' localized-plate atlases removed:
	// western FREE SPINS / YOU WON / TOTAL WIN lettering, superseded by the
	// baked mirrorFsOutro painting + bitmap-font text in the new overlays
	// (FreeSpinCounter's Frame_FSCounter.png lives in reelsFrame)
	// template 'clusterWin' spine removed: cluster-pays effect, unused in a ways game
	transition: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/transition/transition.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/transition/transition.json', import.meta.url).href,
			scale: 2,
		},
	},
	symbolsStatic: {
		type: 'sprites',
		src: new URL('../../assets/sprites/symbolsStatic/symbolsStatic.json', import.meta.url).href,
	},
	// Madam Mirror generated art
	mirrorBgBase: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/bg_base.webp', import.meta.url).href,
		preload: true,
	},
	mirrorBgBasePortrait: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/bg_base_portrait.webp', import.meta.url).href,
		preload: true,
	},
	mirrorBgFreespin: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/bg_freespin.webp', import.meta.url).href,
		preload: true,
	},
	// Scenario-generated ambient video loop of the free-spin room (candles
	// flicker, sigil pulses, smoke drifts). Pixi loads mp4s as video textures.
	mirrorBgFreespinAnim: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/bg_freespin_anim.mp4', import.meta.url).href,
	},
	// base-game ambient loops baked from the parlor paintings
	// (tools/build_bg_video.py) — landscape + portrait variants
	mirrorBgBaseAnim: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/bg_base_anim.mp4', import.meta.url).href,
	},
	mirrorBgBaseAnimPortrait: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/bg_base_anim_portrait.mp4', import.meta.url).href,
	},
	// --- Lady-Mirror ambient SCENE ------------------------------------------
	// ONE full-scene backdrop (candles/crystal-ball/mirror/lamp ambience baked
	// in) that cover-scales to the viewport as a single unit, plus a right-side
	// Lady-Mirror character. Source-agnostic layers: the *Anim video keys below
	// are registered ONLY once the looping files exist (tools drop mp4/webm into
	// assets/sprites/scene/); until then Background.svelte / SceneCharacter.svelte
	// fall back to these stills. Stills built by tools/prepare_scene_assets.py.
	sceneBg: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/scene_bg.webp', import.meta.url).href,
		preload: true,
	},
	ladyCharacter: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_character.png', import.meta.url).href,
		preload: true,
	},
	// activated bonus/free-spins pose (dramatic stance, glowing violet hand-mirror)
	// swapped in by SceneCharacter while gameType === 'freegame'
	ladyBonus: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_bonus.png', import.meta.url).href,
		preload: true,
	},
	// Lady Mirror as a real Spine rig: her cutout is a deformable mesh with a
	// floating idle (bob + breathing + veil/gown cloth-sway + pulsing ghost
	// aura). SceneCharacter renders this when loaded and falls back to the
	// stills above otherwise. Built by tools/gen_lady_spine.py (shared atlas).
	ladySpine: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/lady/lady.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/lady/lady.json', import.meta.url).href,
			scale: 1,
		},
	},
	ladyBonusSpine: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/lady/lady.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/lady/lady_bonus.json', import.meta.url).href,
			scale: 1,
		},
	},
	// win celebration film reels: grindhouse artwork stills + animated loops
	celebT2: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t2.webp', import.meta.url).href },
	celebT3: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t3.webp', import.meta.url).href },
	celebT4: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t4.webp', import.meta.url).href },
	celebT5: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t5.webp', import.meta.url).href },
	celebT6: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t6.webp', import.meta.url).href },
	celebT7: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t7.webp', import.meta.url).href },
	celebT2Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t2.mp4', import.meta.url).href },
	celebT3Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t3.mp4', import.meta.url).href },
	celebT4Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t4.mp4', import.meta.url).href },
	celebT5Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t5.mp4', import.meta.url).href },
	celebT6Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t6.mp4', import.meta.url).href },
	celebT7Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t7.mp4', import.meta.url).href },
	mirrorIntroSeance: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/intro_seance.webp', import.meta.url).href,
	},
	mirrorIntroOtherside: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/intro_otherside.webp', import.meta.url).href,
	},
	mirrorIntroBloodmoon: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/intro_bloodmoon.webp', import.meta.url).href,
	},
	// haunted-mirror centrepieces for the free-spins "THE VEIL PARTS" intro;
	// one per bonus level, the dark glass oval holds the awarded free-spin
	// count as a glowing apparition
	mirrorFsIntro: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/fs_intro_mirror.webp', import.meta.url).href,
	},
	mirrorFsIntroOtherside: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/fs_intro_mirror_otherside.webp', import.meta.url).href,
	},
	mirrorFsIntroBloodmoon: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/fs_intro_mirror_bloodmoon.webp', import.meta.url).href,
	},
	// ornate amethyst filigree "YOU WON / TOTAL WIN" panel (titles baked into
	// the painting; the centre band stays empty for the runtime amount)
	mirrorFsOutro: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/fs_outro_panel.webp', import.meta.url).href,
	},
	mirrorLoading: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/loading.webp', import.meta.url).href,
		preload: true,
	},
	// "Enter the mirror" intro (Scenario image-to-video from the loading key art).
	// Non-preload so it never delays first paint; the loader finishes ALL
	// non-preload assets before stateApp.loaded flips, and the intro only plays
	// after the carousel (which needs stateApp.loaded), so it is always ready.
	introMirror: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/intro_mirror.mp4', import.meta.url).href,
	},
	introMirrorPortrait: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/intro_mirror_portrait.mp4', import.meta.url).href,
	},
	mirrorLogo: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/logo.png', import.meta.url).href,
		preload: true,
	},
	// emblem used as the in-HUD BONUS button (ButtonBuyBonus reads `buyBonusLogo`)
	buyBonusLogo: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/buy_bonus_logo.webp', import.meta.url).href,
		preload: true,
	},
	mirrorWaysPanel: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/ways_panel.png', import.meta.url).href,
	},
	// Tall left gold side-rail (crystal ball baked in) — flush to the reel frame.
	// Normal: WAYS / WIN. Bonus: FREE SPINS / WAYS / WIN.
	mirrorSideRail: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/side_rail_panel.png', import.meta.url).href,
		preload: true,
	},
	// (split telegraph now draws tiny glass shards in MirrorShatter — no knife sprite)
	mirrorSplitKnife: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/split_knife.png', import.meta.url).href,
		preload: false,
	},
	// Ornate amethyst/silver haunted-mirror counter frames (empty dark-glass
	// display window in the centre; text is overlaid at runtime so nothing is
	// ever baked/garbled). Generated art keyed to transparent PNGs by
	// tools/process_counter_frames.py. Used by WaysCounter / FreeSpinCounter.
	mirrorWaysFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/ways_frame.png', import.meta.url).href,
		preload: true,
	},
	mirrorFsFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/fs_frame.png', import.meta.url).href,
		preload: true,
	},
	// Scenario (Imagen 4) haunted-mirror scrying-glass texture, keyed to a
	// transparent edge-faded overlay (tools/process_counter_texture.py). Laid
	// inside the WAYS / FREE SPINS windows for a premium cracked-glass finish.
	mirrorCounterGlass: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/counter_glass.png', import.meta.url).href,
		preload: true,
	},
	mirrorFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/mirror_frame_wide.png', import.meta.url).href,
	},
	// Bottom morph rail: THREE separated gold compartments (WAYS | FREE SPINS | WIN)
	// — never a single bar. Wells measured as texture fractions in FrameMorphHud.
	mirrorFrameBottomCompartments: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/frame_bottom_compartments.png', import.meta.url).href,
		preload: true,
	},
	glassIntact: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/glass_intact.png', import.meta.url).href,
	},
	glassBroken: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/glass_broken.png', import.meta.url).href,
	},
	rootFrameA: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/root_frame_a.png', import.meta.url).href,
	},
	rootFrameB: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/root_frame_b.png', import.meta.url).href,
	},
	coins: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/coin/SD2_Coin.json', import.meta.url).href,
	},
	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;
