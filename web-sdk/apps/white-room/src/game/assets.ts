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
	// --- Lady-Mirror ambient SCENE ------------------------------------------
	// ONE full-scene backdrop (candles/crystal-ball/mirror/lamp ambience baked
	// in) that cover-scales to the viewport as a single unit, plus a right-side
	// Lady-Mirror character. Source-agnostic layers: the *Anim video keys below
	// are registered ONLY once the looping files exist (tools drop mp4/webm into
	// assets/sprites/scene/); until then Background.svelte / SceneCharacter.svelte
	// fall back to these stills. Stills built by tools/prepare_scene_assets.py.
	// v5 = same cold clinical grade as lady_idle_*_v5 (desat→hist-match→cool tint)
	// Cell-block ward backdrop: the bright padded room read as pasted-on behind
	// the black iron chassis, so the scene is now the dark block itself, with an
	// empty unlit corridor down the middle for the reels to sit in.
	sceneBg: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/scene_bg_cellblock.webp', import.meta.url).href,
		preload: true,
	},
	ladyCharacter: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_character.png', import.meta.url).href,
		preload: true,
	},
	// activated bonus/free-spins pose (White Room restraint / clinical stance)
	// swapped in by SceneCharacter while gameType === 'freegame'
	ladyBonus: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_bonus.png', import.meta.url).href,
		preload: true,
	},
	// Alpha-webm Patient idle loops (SceneCharacter breath×5 → mid×1 → move×1).
	// Register ONLY when files exist under assets/sprites/scene/ — missing
	// .webm URLs make PIXI.Assets.load hang forever (~95% load bar).
	// SceneCharacter prefers these over Spine/stills.
	// v5 = v4 ping-pong + shared cold clinical grade-match (desat→hist-match→cool tint):
	//   breath asset_jDxAn1p25Vx1MfNXqZmpXHMf, move asset_7ryyhvZcpJjEh7zAmmSJ6qSo
	// mid v1 = same grade/ping-pong pipeline: asset_YaH9ZZ6PMrcWmn9es1NyeDhr
	// Each file = 1 loop (forward then reverse). New filename = cache bust. Muted.
	ladyIdleBreath: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_idle_breath_v5.webm', import.meta.url).href,
		preload: true,
	},
	ladyIdleMid: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_idle_mid_v1.webm', import.meta.url).href,
		preload: true,
	},
	ladyIdleMove: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_idle_move_v5.webm', import.meta.url).href,
		preload: true,
	},
	// Legacy alias → breath (no preload — sequencer keys above already load it).
	ladyIdleBase: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_idle_breath_v5.webm', import.meta.url).href,
	},
	// Bonus/freegame side character v12 (graded to base idle v5):
	//   intro = A fwd → A rev (drop peak join, audio ON)
	//   loop  = C ping-pong [0..N-1]+[N-2..0] (audio ON)
	// Grade: Rec.709 desat → hist-match clinical ref → tint R*0.969 G*1.002 B*1.069
	// SceneCharacter: play intro once, then SWAP to loop clip (no long-file seek).
	// Build: tools/_build_lady_idle_bonus_v12.py
	ladyIdleBonus: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_idle_bonus_v12_intro.webm', import.meta.url).href,
		preload: true,
	},
	ladyIdleBonusLoop: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/lady_idle_bonus_v12_loop.webm', import.meta.url).href,
		preload: true,
	},
	// Local cutout Spine fallback (GodMode sequences remain quarantined).
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
	// Reserved-slot cage overlay, drawn OVER the symbol reeling inside a chassis
	// opening (LockedSlots.svelte): closed while the cell is locked, swung open
	// once the bonus unlocks that group. True-alpha PNGs keyed from a magenta
	// plate; the closed bars are transparent BETWEEN the bars so the symbol shows
	// through. (The old cellBg housing layer is gone — the cell-block chassis art
	// is the housing now.)
	prisonBarsClosed: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/prison_bars_closed.png', import.meta.url).href,
		preload: true,
	},
	prisonBarsOpen: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/prison_bars_open.png', import.meta.url).href,
		preload: true,
	},
	// CELL-BLOCK CHASSIS — the heavy iron structure holding the nine reserved
	// special cells (CellChassis.svelte). Built by tools/make_chassis_assets.py,
	// which keys the magenta plate AND the punched cell openings to alpha in one
	// pass, then measures where those openings landed; chassisArt.ts places the
	// cells from those measurements rather than from hand-tuned constants.
	// chassisSideR is chassisSideL MIRRORED, so both columns stay identical and
	// the frame reads symmetrical — which is why the plates are blank and the
	// cell numbers are drawn as runtime Text (mirrored art would reverse them).
	chassisSideL: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/chassis_side_l.png', import.meta.url).href,
		preload: true,
	},
	chassisSideR: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/chassis_side_r.png', import.meta.url).href,
		preload: true,
	},
	chassisBeam: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/chassis_beam.png', import.meta.url).href,
		preload: true,
	},
	// Moving parts, cut out of the blocks above so they can turn/travel when a
	// cell opens (see CellChassis + make_chassis_assets.py). One gear serves all
	// four sockets; the chain is mirrored per column like the block art.
	chassisCog: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/chassis_cog.png', import.meta.url).href,
		preload: true,
	},
	chassisChainL: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/chassis_chain_l.png', import.meta.url).href,
		preload: true,
	},
	chassisChainR: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/chassis_chain_r.png', import.meta.url).href,
		preload: true,
	},
	chassisSwag: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/chassis_swag.png', import.meta.url).href,
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
