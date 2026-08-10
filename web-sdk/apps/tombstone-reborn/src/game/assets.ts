export default {
	// template 'loader' spine removed: Mining-Mayhem miner face + logotype,
	// preloaded on every session but never rendered
	// in this app (LoadingScreen uses the mirrorLoading painting instead)
	pressToContinueText: {
		type: 'sprites',
		src: new URL('../../assets/sprites/mirror/pressToContinueText/MM_pressanywhere.json', import.meta.url).href,
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
	// THE WHITE ROOM per-game face (tools/make_clinical_font.py). face="clinical".
	// Do NOT reuse silverFont (Mining-Mayhem western slab) or goldFont (Madam drip)
	// for player-facing win/outro amounts — every game must ship a unique font.
	whiteRoomFont: {
		type: 'font',
		src: new URL('../../assets/fonts/whiteRoomFont/wr_clinical.xml', import.meta.url).href,
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
	// THE WHITE ROOM clinical observation-chrome bar (assets.loading.bar).
	// Regenerated via tools/make_loading_chrome.py — NOT Madam rocky/purple.
	progressBar: {
		type: 'sprites',
		src: new URL('../../assets/sprites/progressBar/progressBar.json', import.meta.url).href,
		preload: true,
	},
	// Falling loading debris (assets.loading.particles) — ceramic/pills/paper/lint/buckles.
	// ZERO Madam Mirror glass shards.
	loadingParticles: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/loadingParticles/loadingParticles.json', import.meta.url).href,
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
	// --- ambient SCENE --------------------------------------------------------
	// ONE full-scene backdrop that cover-scales to the viewport as a single
	// unit. Built by tools/prepare_scene_assets.py.
	// v5 = cold clinical grade (desat→hist-match→cool tint). The cell-block
	// plate was too dark behind the iron chassis, so this is the clinical white
	// room, which reads as the ward with the chassis bolted into it.
	//
	// The right-side character ("the patient" / Lady Mirror) that used to stand
	// here is REMOVED, along with her stills, idle webms and Spine rigs. The art
	// is still on disk under assets/sprites/scene/ and assets/spines/lady/ but
	// nothing loads it — do not re-register these without asking.
	sceneBg: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/scene_bg_v5.webp', import.meta.url).href,
		preload: true,
	},
	// THE WHITE ROOM win celebration loops (folder masters; wire_celeb copies roots)
	celebT2: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t2.webp', import.meta.url).href },
	celebT3: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t3.webp', import.meta.url).href },
	celebT4: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t4.webp', import.meta.url).href },
	celebT5: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t5.webp', import.meta.url).href },
	celebT6: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t6.webp', import.meta.url).href },
	celebT7: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t7.webp', import.meta.url).href },
	celebT2Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t2/celeb_t2.mp4', import.meta.url).href },
	celebT3Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t3/celeb_t3.mp4', import.meta.url).href },
	celebT4Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t4/celeb_t4.mp4', import.meta.url).href },
	celebT5Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t5/celeb_t5.mp4', import.meta.url).href },
	celebT6Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t6/celeb_t6.mp4', import.meta.url).href },
	celebT7Anim: { type: 'sprite', src: new URL('../../assets/sprites/celeb/celeb_t7/celeb_t7.mp4', import.meta.url).href },
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
	// observation-pane centrepieces for free-spins THE INTAKE / HER SIDE / WHITEOUT intro;
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
	// Full-bleed padded-cell still (from bg_base). Never ship the old title-card
	// composite that baked a PNG transparency checkerboard into the centre plate.
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
	// THE WHITE ROOM stacked brand mark (Scenario GPT Image 2 + Photoroom alpha).
	// Cache-bust: logo_v3.png — transparent clinical stack, no plate.
	mirrorLogo: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/logo_v3.png', import.meta.url).href,
		preload: true,
	},
	// emblem used as the in-HUD BONUS button (ButtonBuyBonus reads `buyBonusLogo`)
	buyBonusLogo: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/buy_bonus_logo.webp', import.meta.url).href,
		preload: true,
	},
	// Shared NEW UI chrome plates (same family as HTML paytable / Bonus Buy /
	// buy-confirm). Blank plates + runtime Text — never bake CONTINUE labels.
	uiCtaActivate: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/buy_ui/cta_activate.png', import.meta.url).href,
	},
	uiSectionMagentaWide: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/buy_ui/section_magenta_wide.png', import.meta.url).href,
	},
	uiRibbonBlank: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/buy_ui/ribbon_blank.png', import.meta.url).href,
	},
	uiBtnCloseMagenta: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/buy_ui/btn_close_magenta.png', import.meta.url).href,
	},
	uiChevronPlate: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/buy_ui/chevron_plate.png', import.meta.url).href,
	},
	uiAccentStain: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/buy_ui/accent_stain.png', import.meta.url).href,
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
	// legacy knife sprite unused — telegraph is intakeShot Graphics in MirrorShatter
	mirrorSplitKnife: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/split_knife.png', import.meta.url).href,
		preload: false,
	},
	// WAYS / FREE SPINS counter frames (clinical white/silver plaques).
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
	// Clinical observation-glass texture for counter wells (not violet scrying glass).
	mirrorCounterGlass: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/counter_glass.png', import.meta.url).href,
		preload: true,
	},
	// THE WHITE ROOM WILD card (generated straitjacket "WILD" art, transparent PNG).
	// Sprite-only symbol (see SYMBOL_INFO_MAP.W) so it renders identically on the
	// board, in unlocked slots, and as a risen Wild Reel.
	wrWild: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_wild.png', import.meta.url).href,
		preload: true,
	},
	// The EXPANDING wild: same jacket, plus a rising arrow stencilled below the
	// wordmark. Shown for the wild that drops into a bottom cell and grows its
	// reel (see SYMBOL_INFO_MAP.W / RawSymbol.expanding). The arrow deliberately
	// sits near the card's middle — bottom cells clip a card's height.
	// Built by tools/make_expanding_wild.py.
	wrWildExpand: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_wild_expand.png', import.meta.url).href,
		preload: true,
	},
	// SCATTER faces, one per landing position (1st..5th), matching the five
	// scatter stop sounds: MEMORY / DOUBT / REGRET / REVELATION / OBLIVION.
	// Built by tools/make_scatter_words.py.
	wrScatter1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_scatter_1.png', import.meta.url).href,
		preload: true,
	},
	wrScatter2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_scatter_2.png', import.meta.url).href,
		preload: true,
	},
	wrScatter3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_scatter_3.png', import.meta.url).href,
		preload: true,
	},
	wrScatter4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_scatter_4.png', import.meta.url).href,
		preload: true,
	},
	wrScatter5: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_scatter_5.png', import.meta.url).href,
		preload: true,
	},
	// Spin smear for all five faces. The atlas s_blur.png is the old head card,
	// so a streaking reel has to use this instead.
	wrScatterBlur: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_scatter_blur.png', import.meta.url).href,
		preload: true,
	},
	// Full-reel-column WILD art (straitjacket figure in a padded cell). Slides
	// down over a middle reel when a bottom-slot WILD turns it into a Wild Reel
	// (WildReelSlide.svelte). True-alpha PNG keyed from a magenta plate.
	wrReel: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_reel.png', import.meta.url).href,
		preload: true,
	},
	// Full-reel-column WILD variants: each premium inmate (H1..H5) standing in a
	// padded cell (512x1680). A Wild Reel / Stretch picks one of these at random
	// per appearance (see WILD_REEL_ARTS). Full-bg PNGs — cover-fit + masked.
	wrReelH1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_reel_h1.png', import.meta.url).href,
		preload: true,
	},
	wrReelH2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_reel_h2.png', import.meta.url).href,
		preload: true,
	},
	wrReelH3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_reel_h3.png', import.meta.url).href,
		preload: true,
	},
	wrReelH4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_reel_h4.png', import.meta.url).href,
		preload: true,
	},
	wrReelH5: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_reel_h5.png', import.meta.url).href,
		preload: true,
	},
	// ONE wild-reel column is a full VIDEO with audio (1080x1920, 6s). Pixi loads
	// the mp4 as a video texture; WildReelSlide plays it once WITH sound then
	// freezes on the last frame (audio never repeats). The other columns stay as
	// the still PNGs above.
	wrReelWildH3Video: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_reel_wild_h3.mp4', import.meta.url).href,
		preload: true,
	},
	// New special-cell feature symbols (Stretch / Split / Clone). Keyed
	// transparent PNG cards shown inside the reserved cells (LockedSlots).
	wrStretch: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_stretch.png', import.meta.url).href,
		preload: true,
	},
	wrSplit: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_split.png', import.meta.url).href,
		preload: true,
	},
	wrClone: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/wr_clone.png', import.meta.url).href,
		preload: true,
	},
	// (The reserved-slot cage overlay is drawn procedurally by LockedSlots.svelte
	// now — the old prison_bars_closed/open PNGs are no longer registered.)
	// SPLIT (legacy claw atlas — kept loaded so ColumnClawStrike / any leftover
	// refs do not 404; the symbol split now uses splitHoles instead).
	splitClaw: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/split_claw.json', import.meta.url).href,
		preload: true,
	},
	// SPLIT: bullet-hole impact decals stamped onto scored cells. Three variants
	// packed by tools/make_bullet_hole_atlas.py; shot count scales with the
	// cell's multiplier (up to 4).
	splitHoles: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/split_holes.json', import.meta.url).href,
		preload: true,
	},
	// SPLIT / lock western VFX (Kenney particle + smoke packs, recolored).
	// tools/make_tombstone_split_vfx_atlas.py — brass sparks, gunsmoke, scorch,
	// scope ring. Replaces clinical white brackets / clinic sparkles.
	tombstoneSplitVfx: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/tombstone_split_vfx.json', import.meta.url).href,
		preload: true,
	},
	// CELL-BLOCK CHASSIS art is GONE: the iron cage columns and beam were
	// removed — the side special cells are sockets of the board plate itself
	// (BoardPlate.svelte), with only the prison bars (LockedSlots) over them.
	// STRETCH feature rig (tools/make_stretch_chain.py): a vertically-tileable
	// heavy chain strip and the two-jaw clamp that grips the reel edge to pull it.
	stretchChain: {
		type: 'sprite',
		src: new URL('../../assets/sprites/stretch/chain_tile.png', import.meta.url).href,
		preload: true,
	},
	stretchClamp: {
		type: 'sprite',
		src: new URL('../../assets/sprites/stretch/clamp.png', import.meta.url).href,
		preload: true,
	},
	// HIGH-symbol outline frame UI element (hollow bezel). Replaces Graphics grey stroke.
	// Built by tools/make_symbol_outline_frame.py — NOT baked into symbol card art.
	symbolOutlineFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/symbol_outline_frame.png', import.meta.url).href,
		preload: true,
	},
	mirrorFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/mirror_frame_wide.png', import.meta.url).href,
	},
	// SPECIAL BAR (the six-cell rail beside the board). Scenario GPT Image 2
	// transparent PNGs, alpha-cropped by tools/make_special_bar_art.py.
	// Empty slots use the hollow tintable frame; revealed cards use the
	// per-kind plaques with baked embossed labels (no runtime Text).
	barRail: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_rail.webp', import.meta.url).href,
		preload: true,
	},
	barPlaque: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueGang: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_gang.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueOutlaw: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_outlaw.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueSmoke: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_smoke.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueOpen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_open.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueDigup: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_digup.png', import.meta.url).href,
		preload: true,
	},
	// Bottom morph rail: THREE separated compartments (WAYS | FREE SPINS | WIN).
	mirrorFrameBottomCompartments: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/frame_bottom_compartments.png', import.meta.url).href,
		preload: true,
	},
	// SINGLE-CELL observation panes (make_observation_panes.py). Runtime HM overlay
	// uses drawObservationPane Graphics; these remain for asset-gap / fallback.
	glassIntact: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/observation_pane_intact.png', import.meta.url).href,
	},
	glassBroken: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/observation_pane_cracked.png', import.meta.url).href,
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
	// Cell Seal full-reel characters (H1–H5): still + expand (gif/mp4) + looping idle webm
	// + GodMode Spine (idle). Overlay prefers expand *video* (play-once→loop-last-3s) →
	// idle webm → expand gif → Spine → full.webp.
	cellSealH1Full: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H1_full.webp', import.meta.url).href,
	},
	cellSealH2Full: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H2_full.webp', import.meta.url).href,
	},
	cellSealH3Full: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H3_full.webp', import.meta.url).href,
	},
	cellSealH4Full: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H4_full.webp', import.meta.url).href,
	},
	cellSealH5Full: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H5_full.webp', import.meta.url).href,
	},
	// Aliases used by older overlay key lookups
	cellSealH1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H1_full.webp', import.meta.url).href,
	},
	cellSealH2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H2_full.webp', import.meta.url).href,
	},
	cellSealH3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H3_full.webp', import.meta.url).href,
	},
	cellSealH4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H4_full.webp', import.meta.url).href,
	},
	cellSealH5: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H5_full.webp', import.meta.url).href,
	},
	cellSealH1Expand: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H1_expand.gif', import.meta.url).href,
	},
	cellSealH2Expand: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H2_expand.gif', import.meta.url).href,
	},
	// H3 The Grin — Scenario expand video (play once, then loop last 3s in CellSealOverlay).
	cellSealH3Expand: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H3_expand.mp4', import.meta.url).href,
	},
	cellSealH4Expand: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H4_expand.gif', import.meta.url).href,
	},
	cellSealH5Expand: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H5_expand.gif', import.meta.url).href,
	},
	cellSealH1Idle: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H1_idle.webm', import.meta.url).href,
	},
	cellSealH2Idle: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H2_idle.webm', import.meta.url).href,
	},
	cellSealH3Idle: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H3_idle.webm', import.meta.url).href,
	},
	cellSealH4Idle: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H4_idle.webm', import.meta.url).href,
	},
	cellSealH5Idle: {
		type: 'sprite',
		src: new URL('../../assets/sprites/cellSeal/H5_idle.webm', import.meta.url).href,
	},
	cellSealH1Spine: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/cellSeal/cellSeal.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/cellSeal/H1.json', import.meta.url).href,
			scale: 1,
		},
	},
	cellSealH2Spine: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/cellSeal/cellSeal.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/cellSeal/H2.json', import.meta.url).href,
			scale: 1,
		},
	},
	cellSealH3Spine: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/cellSeal/cellSeal.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/cellSeal/H3.json', import.meta.url).href,
			scale: 1,
		},
	},
	cellSealH4Spine: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/cellSeal/cellSeal.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/cellSeal/H4.json', import.meta.url).href,
			scale: 1,
		},
	},
	cellSealH5Spine: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/cellSeal/cellSeal.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/cellSeal/H5.json', import.meta.url).href,
			scale: 1,
		},
	},
	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;
