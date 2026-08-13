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
	// TOMBSTONE REBORN per-game face (tools/make_tombstone_font.py). face="tombstone".
	// Wanted-poster serif, branded gold body on a dark iron rim.
	//
	// This replaces face "clinical" (whiteRoomFont / wr_clinical) — the condensed
	// light-grey Madam Mirror plaque face that was still rendering every win title
	// and amount. Do NOT reuse silverFont (Mining-Mayhem western slab) or
	// goldFont / amethystFont / ghostFont (Madam drip) either; every game must
	// ship a unique player-facing face.
	tombstoneFont: {
		type: 'font',
		src: new URL('../../assets/fonts/tombstoneFont/tr_tombstone.xml', import.meta.url).href,
	},
	// template 'bigwin' + 'globalMultiplier' spines removed: gold-western
	// Mining-Mayhem art, superseded by the WinCelebration hero plates and the
	// WaysCounter plaque; neither was rendered anywhere in this app
	// template 'fsIntro' / 'fsIntroNumber' / 'fsOutroNumber' spines removed:
	// the Mining-Mayhem plank panel + bracket frame behind the old free-spin
	// intro/outro. This game has no free spins at all, so nothing replaces them.
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
	// western FREE SPINS / YOU WON / TOTAL WIN lettering. Win amounts render as
	// bitmap-font text on the WinCelebration plates; there is no free-spin
	// counter panel because there are no free spins.
	// template 'clusterWin' spine removed: cluster-pays effect, unused in a ways game
	transition: {
		type: 'spine',
		src: {
			atlas: new URL('../../assets/spines/transition/transition.atlas', import.meta.url).href,
			skeleton: new URL('../../assets/spines/transition/transition.json', import.meta.url).href,
			scale: 2,
		},
	},
	// EVERY paying symbol face lives in here: h1..h5 / l1..l5 cards, their spin
	// smears, and the hm/me cards. It is flattened into loadedAssets under its
	// FRAME names, so a symbol asks for `h2.webp`, not for `symbolsStatic`.
	//
	// preload is NOT optional. AssetsLoader renders the whole game as soon as the
	// PRELOAD batch resolves, and Board mounts as soon as stateLayout
	// .showLoadingScreen is false — which it already is on any in-place remount
	// of <App> (Svelte HMR, a Storybook re-render; stateApp.reset() exists for
	// exactly that). Left non-preload, the board draws during the window where
	// loadedAssets holds preloaded assets ONLY, so every reel cell resolves to
	// Texture.EMPTY: dark empty boxes plus a `Sprite: key "h2.webp" is not found
	// in the loadedAssets` per cell. Every other symbol card (wrWild, wrScatter*,
	// wrStretch/Split/Clone) is already preloaded; this one was the odd one out.
	// tools/qa_symbol_coverage.py fails if any symbol asset stops being preloaded.
	symbolsStatic: {
		type: 'sprites',
		// v13 = full-bleed premiums (figure to all edges, no paper gap), used raw
		// (no code grade/tint) with faint baked rank bg tint + monochrome lows
		src: new URL('../../assets/sprites/symbolsStatic/symbolsStatic.v13.json', import.meta.url).href,
		preload: true,
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
		src: new URL('../../assets/sprites/scene/scene_bg_v2.webp', import.meta.url).href,
		preload: true,
	},
	// WIN CELEBRATION hero plates, one per big tier — dark western / graveyard
	// scenes generated on Layer AI (FLUX.1 [dev]) and graded by
	// tools/make_win_celebration_art.py.
	//
	// These REPLACE celebT2..celebT7 (+ celebT*Anim), which were photographic
	// Madam Mirror "White Room" footage of a straitjacketed woman in a padded
	// asylum cell — tier 7 was a literal white-out. Those files no longer ship;
	// do not re-register them, there is deliberately no fallback to them.
	winTierBounty: { type: 'sprite', src: new URL('../../assets/sprites/celeb/win_tier_bounty.webp', import.meta.url).href },
	winTierShowdown: { type: 'sprite', src: new URL('../../assets/sprites/celeb/win_tier_showdown.webp', import.meta.url).href },
	winTierHighnoon: { type: 'sprite', src: new URL('../../assets/sprites/celeb/win_tier_highnoon.webp', import.meta.url).href },
	winTierLaststand: { type: 'sprite', src: new URL('../../assets/sprites/celeb/win_tier_laststand.webp', import.meta.url).href },
	winTierBloodmoney: { type: 'sprite', src: new URL('../../assets/sprites/celeb/win_tier_bloodmoney.webp', import.meta.url).href },
	winTierBoothill: { type: 'sprite', src: new URL('../../assets/sprites/celeb/win_tier_boothill.webp', import.meta.url).href },
	// Weathered timber + branded-iron frame with a punched-through window, in
	// place of the old thin amber CCTV-monitor bezel. Carries NO thin outline: the
	// gold inlay hairline it used to bake around the window read as a stray vector
	// outline once minified onto the panel, so the takeover's edge is now the warm
	// window spill plus the runtime god-rays. Do not re-add a stroke here.
	winFrame: { type: 'sprite', src: new URL('../../assets/sprites/celeb/win_frame.png', import.meta.url).href },
	// Celebration light shapes (god-rays, lantern glow, bell rings) and particles
	// (starburst pops, spark streaks, dust plumes, gunsmoke, embers).
	// Frame order contract: src/game/winCelebrationArt.ts.
	winCelebLight: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/win_celeb_light.json', import.meta.url).href,
	},
	winCelebVfx: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/win_celeb_vfx.json', import.meta.url).href,
	},
	// BONUS-ENTRY BANNER hero plates, one per real buy mode — DEAD MAN'S HAND for
	// bonus_small (80x, the six-card special bar awake) and OPEN GRAVE for
	// bonus_super (1000x, the sealed last-reel lane cracked open). Dark western
	// scenes generated on Layer AI (FLUX.1 [dev], the same model and grade as the
	// win tiers above) and baked by tools/make_bonus_entry_art.py.
	//
	// TWO keys, because the math has exactly two buy modes and each is a SINGLE
	// enhanced spin. Contract: src/game/bonusEntryArt.ts.
	bonusEntrySmall: { type: 'sprite', src: new URL('../../assets/sprites/celeb/bonus_entry_small.webp', import.meta.url).href },
	bonusEntrySuper: { type: 'sprite', src: new URL('../../assets/sprites/celeb/bonus_entry_super.webp', import.meta.url).href },
	// Two frames, both from the same timber/iron family. DEAD MAN'S HAND wears the
	// 74px band with a single gold inlay; OPEN GRAVE wears a heavier build — deeper
	// band, oversized corner straps, a strap on every mid-edge, double gold inlay.
	//
	// bonusFrameSmall is NOT `winFrame` above, although it started as a copy of it:
	// the win takeover was asked to lose the thin outline tracing its panel, the
	// banner was asked to keep its framing, so the banner owns the outlined build.
	bonusFrameSmall: { type: 'sprite', src: new URL('../../assets/sprites/celeb/bonus_frame_small.png', import.meta.url).href },
	bonusFrameSuper: { type: 'sprite', src: new URL('../../assets/sprites/celeb/bonus_frame_super.png', import.meta.url).href },
	// The banner's light shapes and particles are `winCelebLight` / `winCelebVfx`
	// above, reused as-is. Do NOT add a parallel bonus VFX atlas.
	//
	// FREE-SPIN / BONUS-LEVEL ART REMOVED. mirrorIntroSeance / mirrorIntroOtherside /
	// mirrorIntroBloodmoon (bonus-level paintings), mirrorFsIntro /
	// mirrorFsIntroOtherside / mirrorFsIntroBloodmoon (free-spin intro
	// observation panes) and mirrorFsOutro ("YOU WON / TOTAL WIN" filigree
	// panel) were Madam Mirror White Room art titled "THE INTAKE" / "HER SIDE" /
	// "WHITEOUT". Tombstone Reborn has NO free spins and NO bonus levels — its
	// bonuses are single enhanced spins — so the five overlays that rendered
	// these were dead code and are deleted along with the .webp files. There is
	// deliberately no replacement key: do not re-register these.
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
	// The NUDGE WILD: the card the last-lane nudge rider wears and leaves behind
	// in every cell it racks through (see SYMBOL_INFO_MAP.W / RawSymbol.nudged).
	// Skeletal hand on a spur wheel with left-pointing arrows — generated over
	// wr_wild.png as the style reference and baked onto the same 300x300 canvas
	// with wr_wild's own alpha (tools/make_nudge_wild_card.py).
	trNudgeWild: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_nudge_wild.png', import.meta.url).href,
		preload: true,
	},
	// The SCATTER: the cracked BONUS tombstone. 3 on a base spin trigger the
	// SMALL BONUS round, 4+ the BIG BONUS (see SYMBOL_INFO_MAP.S). Generated
	// art baked onto the same 300x300 canvas with wr_wild's own alpha
	// (tools/make_scatter_card.py).
	trScatter: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_scatter.png', import.meta.url).href,
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
	// SPLIT: bullet-hole impact decals stamped onto scored cells. Six splintered
	// wood holes packed by tools/make_bullet_hole_atlas.py; shot count scales
	// with the cell's multiplier (up to 4).
	splitHoles: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/split_holes.json', import.meta.url).href,
		preload: true,
	},
	// BULLET EXPLOSION for high-multiplier split cells (count > 10): a one-shot
	// gunpowder blast flipbook baked from Kenney explosions/Explosion_1 by
	// tools/make_split_explosion_atlas.py. Frame order is src/game/splitExplosion.ts.
	splitExplosion: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/split_explosion.json', import.meta.url).href,
		preload: true,
	},
	// SPLIT / lock western VFX: Scenario muzzle flashes, dust plume, gold
	// starburst and sparkler, over Kenney particle + smoke supporting layers
	// (tools/make_tombstone_split_vfx_atlas.py).
	tombstoneSplitVfx: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/tombstone_split_vfx.json', import.meta.url).href,
		preload: true,
	},
	// LINKED CELL FIRE: real flame tongues sliced out of the reference fire band,
	// plus Kenney's Black smoke sequence, a light mask, and warm spark embers
	// (tools/make_cell_fire_atlas.py). Frame order is the contract in
	// src/game/cellFire.ts.
	cellFire: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/cell_fire.json', import.meta.url).href,
		preload: true,
	},
	// NON-SPLIT feature VFX (nudge / gunsmoke / coffin open / dig up /
	// special-bar hit / bounty): Kenney gunsmoke, dust, muzzle flash, grave
	// burst, dirt, scorch, sparks, splats, rings and light shafts, recoloured
	// to the graveyard palette (tools/make_tombstone_feature_vfx_atlas.py).
	// Frame order is the contract in src/game/featureVfx.ts.
	tombstoneFeatureVfx: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/tombstone_feature_vfx.json', import.meta.url).href,
		preload: true,
	},
	// Hero plates for the same events, from the Scenario team library and baked
	// by the script above (alpha-bled, RGB zeroed under transparency).
	fxMuzzleFlash: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_muzzle_flash.png', import.meta.url).href,
		preload: true,
	},
	fxDustPlume: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_dust_plume.png', import.meta.url).href,
		preload: true,
	},
	// DIG UP hero art, generated in Layer AI and cut by tools/make_digup_shovel.py:
	// the spade that plants itself in a dug cell, and the turned earth under it.
	fxShovel: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_shovel.png', import.meta.url).href,
		preload: true,
	},
	fxDigScar: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_dig_scar.png', import.meta.url).href,
		preload: true,
	},
	// Cracked-strike decal stamped on the symbol where the spade bites, so the
	// dig reads as a real IMPACT on the card, not a spade quietly placed on it.
	// Layer GPT Image 2 gen on a black void, keyed by tools/make_digup_shovel.py.
	fxDigImpact: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_dig_impact.png', import.meta.url).href,
		preload: true,
	},
	// NUDGE furniture, generated in Layer AI and cut by tools/make_nudge_ui.py.
	// The frame's centre is open, so the riding symbol reads through it; the
	// plaque is shared by the nudge and bounty multiplier badges.
	fxRiderFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_rider_frame.png', import.meta.url).href,
		preload: true,
	},
	fxMultPlaque: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_mult_plaque.png', import.meta.url).href,
		preload: true,
	},
	// CELL-BLOCK CHASSIS art is GONE: the iron cage columns and beam were
	// removed — the side special cells are sockets of the board plate itself
	// (BoardPlate.svelte), with only the prison bars (LockedSlots) over them.
	// BOARD REEL-FRAME art (tools/make_board_frame_art.py): the weathered
	// timber-and-iron chassis BoardPlate.svelte is skinned with. The plate is a
	// dark-graded Layer AI FLUX.1 [dev] plank render clipped to the diamond
	// staircase; the socket is one crafted recessed window drawn per visible
	// cell; the bracket is a bolted iron corner boss on the plate's PAD overhang.
	// This REPLACES the old procedural Pixi Graphics frame (flat plank fill +
	// hand-drawn sockets + nail dots). Preloaded: the board mounts the instant
	// the loading screen clears, so these must be in loadedAssets by then.
	boardPlate: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/board_plate_light.webp', import.meta.url).href,
		preload: true,
	},
	boardCellSocket: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/board_cell_socket.png', import.meta.url).href,
		preload: true,
	},
	// TOMBSTONE REBORN board frame: a crafted, TRANSPARENT weathered-grey barn-wood
	// window (iron corner straps + bolts + faint blood) drawn once per VISIBLE cell
	// so the diamond staircase reads as one bolted timber rig, the scene showing
	// outside. Replaces the stretched plank field + flat sockets in BoardPlate.
	boardCellFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/board_cell_frame.png', import.meta.url).href,
		preload: true,
	},
	// TOMBSTONE REBORN board = two masked fields (no per-cell frames, so borders
	// never double up between neighbours): a grey weathered-timber ring clipped to
	// the OUTER staircase silhouette, and a pale stone field clipped to the INNER
	// silhouette on top of it. The wood ring hugs the diamond and fills the empty
	// step gaps left by reel-height differences; symbols draw over the stone.
	boardWoodField: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/board_wood_grey.webp', import.meta.url).href,
		preload: true,
	},
	// The frame itself is ONE baked transparent PNG, pre-shaped to the authored
	// staircase (tools/make_board_frame_image.py): grey timber ring + bevels +
	// keylines + iron bolts + the shadow it casts inward. Placed 1:1 at the
	// authored outer box — re-bake whenever the board shape changes.
	boardFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/board_frame.png', import.meta.url).href,
		preload: true,
	},
	boardStoneField: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/board_stone_grey.webp', import.meta.url).href,
		preload: true,
	},
	// Per-slot frame drawn in EVERY visible cell (behind the card): a thin
	// weathered iron border with corner rivets, transparent center. Tiles flush
	// edge-to-edge so the board reads as a grid of framed slots (Tombstone R.I.P.
	// look) instead of cards floating on the stone.
	boardSlotFrame: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/board_slot_frame.png', import.meta.url).href,
		preload: true,
	},
	// White-on-transparent shattered-glass bullet holes, spawned at the click point
	// on an IDLE board (see BulletHits.svelte). Five variants, picked at random per
	// shot; all cleared the instant a spin starts.
	bulletCrack1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/bullet_crack_1.png', import.meta.url).href,
		preload: true,
	},
	bulletCrack2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/bullet_crack_2.png', import.meta.url).href,
		preload: true,
	},
	bulletCrack3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/bullet_crack_3.png', import.meta.url).href,
		preload: true,
	},
	bulletCrack4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/bullet_crack_4.png', import.meta.url).href,
		preload: true,
	},
	bulletCrack5: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/bullet_crack_5.png', import.meta.url).href,
		preload: true,
	},
	boardCornerBracket: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/board_corner_bracket.png', import.meta.url).href,
		preload: true,
	},
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
	// Ornate cast-iron/bronze nameplate for the WAYS (top) + WIN (bottom) readouts
	// on the vertical rail. Layer GPT Image 2 gen, keyed transparent + trimmed
	// (tools/make_readout_plaque.py). 1.5:1, dark inset panel hosts gold text.
	barReadoutPlaque: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_readout_plaque.png', import.meta.url).href,
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
	// LAST-REEL LANE (tools/_wire_lane_specials.py):
	// laneLidLock — boarded-up chained cover shown over the lane whenever it is
	// locked (every base/small spin until DIG UP; open all through the super
	// bonus). laneGold* — the golden sheriff cards flashed in the lane when its
	// special fires (BOUNTY star / SUPER SPLIT revolvers / NUDGE spur).
	laneLidLock: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/lane_lid_lock.webp', import.meta.url).href,
		preload: true,
	},
	laneGoldBounty: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/lane_gold_bounty.webp', import.meta.url).href,
		preload: true,
	},
	laneGoldSupersplit: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/lane_gold_supersplit.webp', import.meta.url).href,
		preload: true,
	},
	laneGoldNudge: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/lane_gold_nudge.webp', import.meta.url).href,
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
	// Win-scatter particles: aged gold coins at many rotations plus brass rifle
	// cartridges and spent casings, cut out of a Layer AI sheet by
	// tools/make_win_celebration_art.py.
	//
	// This REPLACES `coins` (assets/sprites/coin/SD2_Coin.json), which was the
	// Samurai Dogs 2 template coin sheet — the generic gold-coin confetti. That
	// sheet is no longer registered.
	winScatter: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/win_scatter.json', import.meta.url).href,
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
