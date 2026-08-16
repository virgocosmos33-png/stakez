export default {
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
	// TOMBSTONE REBORN per-game face (tools/make_tombstone_font.py). face="tombstone".
	// Wanted-poster serif, branded gold body on a dark iron rim.
	//
	// Do NOT re-register goldFont / silverFont / purpleFont / ghostFont /
	// amethystFont / goldBlur — those are Madam Mirror and Mining Mayhem faces
	// and their page PNGs 403 on Stake when this game loads them.
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
	// --- ambient SCENE --------------------------------------------------------
	// ONE full-scene backdrop that cover-scales to the viewport as a single
	// unit. Base game: the saloon still (basemodebgimagetomsbstonereborn.png
	// baked to scene_bg_v2.webp, 1679x937).
	sceneBg: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/scene_bg_v2.webp', import.meta.url).href,
		preload: true,
	},
	// Live saloon room (fire-frame lady-spine), baked by tools/bake_saloon_room.py.
	// Plate has no lanterns; saloonLampL/R are the hanging fixtures. Must
	// preload: SaloonScene mounts as soon as preloaded assets land.
	saloonPlate: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/saloon_plate.webp', import.meta.url).href,
		preload: true,
	},
	saloonLampL: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/saloon_lamp_l.png', import.meta.url).href,
		preload: true,
	},
	// Click-smashed left lantern: glass cracked, bulb dead, baked halo gone.
	// Restored on the next spin (SaloonScene + saloonLamp.svelte.ts).
	saloonLampLSmashed: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/saloon_lamp_l_smashed.png', import.meta.url).href,
		preload: true,
	},
	saloonLampR: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/saloon_lamp_r.png', import.meta.url).href,
		preload: true,
	},
	// Soft cream wash that rides the left lamp so the wall lifts as it swings.
	saloonLampGlow: {
		type: 'sprite',
		src: new URL('../../assets/sprites/scene/saloon_lamp_glow.png', import.meta.url).href,
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
	// Brand mark: bloody sheriff wordmark (TOMBSTONE / REBORN).
	mirrorLogo: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_logo.png', import.meta.url).href,
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
	// WILD card: whiskey bottle with WILD on the label, same 300x300 canvas
	// and wr_wild alpha as every other symbol.
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
	trScatterSuper: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_scatter_super.png', import.meta.url).href,
		preload: true,
	},
	// Feature symbols that land ON the board (tools/make_feature_cards.py).
	trSP: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_sp.png', import.meta.url).href,
		preload: true,
	},
	trGS: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_gs.png', import.meta.url).href,
		preload: true,
	},
	trTS: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_ts.png', import.meta.url).href,
		preload: true,
	},
	trNW: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_nw.png', import.meta.url).href,
		preload: true,
	},
	// Legacy keys so older showcase books still resolve a texture.
	trSG: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_sp.png', import.meta.url).href,
		preload: true,
	},
	trSO: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_sp.png', import.meta.url).href,
		preload: true,
	},
	trDU: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_ts.png', import.meta.url).href,
		preload: true,
	},
	trCF: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_ts.png', import.meta.url).href,
		preload: true,
	},
	fxNudgeFire: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_nudge_fire.png', import.meta.url).href,
		preload: true,
	},
	// Full-reel NUDGE WAYS totem. One tall iron column (header + ratchet +
	// arrow foot), clipped from the top of the reel in NudgeWays.svelte.
	fxNudgeColumn: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/fx_nudge_column.png', import.meta.url).href,
		preload: true,
	},
	trSH: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_sh.png', import.meta.url).href,
		preload: true,
	},
	trSS: {
		type: 'sprite',
		src: new URL('../../assets/sprites/mirror/tr_ss.png', import.meta.url).href,
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
	// SPLIT: transparent Bowie + horizontal ember slash (tools/make_split_knife.py).
	// The knife flies right→left; the slash is the cut it leaves. Panes snap on impact.
	splitKnife: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/tr_split_knife.png', import.meta.url).href,
		preload: true,
	},
	splitSlash: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/tr_split_slash.png', import.meta.url).href,
		preload: true,
	},
	// GUNSMOKE: prop_19 revolver on the landed GS card. It wheel-spins
	// clockwise and fires prop_22/23/24 rounds (tools/bake_gunsmoke_props.py).
	gunsmokeRevolver: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/tr_gunsmoke_revolver.png', import.meta.url).href,
		preload: true,
	},
	gunsmokeBulletA: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gunsmoke_bullet_a.png', import.meta.url).href,
		preload: true,
	},
	gunsmokeBulletB: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gunsmoke_bullet_b.png', import.meta.url).href,
		preload: true,
	},
	gunsmokeBulletC: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gunsmoke_bullet_c.png', import.meta.url).href,
		preload: true,
	},
	gsMuzzleGlow: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_muzzle_glow.png', import.meta.url).href,
		preload: true,
	},
	gsMuzzleStreak: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_muzzle_streak.png', import.meta.url).href,
		preload: true,
	},
	gsWoundHole1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_hole_1.png', import.meta.url).href,
		preload: true,
	},
	gsWoundHole2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_hole_2.png', import.meta.url).href,
		preload: true,
	},
	gsWoundHole3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_hole_3.png', import.meta.url).href,
		preload: true,
	},
	gsWoundHole4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_hole_4.png', import.meta.url).href,
		preload: true,
	},
	gsWoundHole5: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_hole_5.png', import.meta.url).href,
		preload: true,
	},
	gsWoundHole6: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_hole_6.png', import.meta.url).href,
		preload: true,
	},
	gsWoundHole7: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_hole_7.png', import.meta.url).href,
		preload: true,
	},
	gsWoundHole8: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_hole_8.png', import.meta.url).href,
		preload: true,
	},
	gsWoundBlood1: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_blood_1.png', import.meta.url).href,
		preload: true,
	},
	gsWoundBlood2: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_blood_2.png', import.meta.url).href,
		preload: true,
	},
	gsWoundBlood3: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_blood_3.png', import.meta.url).href,
		preload: true,
	},
	gsWoundBlood4: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_blood_4.png', import.meta.url).href,
		preload: true,
	},
	gsWoundBlood5: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_blood_5.png', import.meta.url).href,
		preload: true,
	},
	gsWoundBlood6: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_blood_6.png', import.meta.url).href,
		preload: true,
	},
	gsWoundBlood7: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_blood_7.png', import.meta.url).href,
		preload: true,
	},
	gsWoundBlood8: {
		type: 'sprite',
		src: new URL('../../assets/sprites/fx/gs_wound_blood_8.png', import.meta.url).href,
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
	// FPS revolver that follows the pointer over an idle board (BulletHits.svelte).
	// Recoil + muzzle flash live on this sprite; the OS cursor is hidden over the
	// catcher. Source art: pistol.png / fireburst.png (black already keyed out).
	pistolAim: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/pistol.png', import.meta.url).href,
		preload: true,
	},
	muzzleBurst: {
		type: 'sprite',
		src: new URL('../../assets/sprites/board/fireburst.png', import.meta.url).href,
		preload: true,
	},
	// Kenney whitePuff00-24 (kenney_smoke-particles), packed + dusty-tinted by
	// tools/make_muzzle_smoke_atlas.py. Plays once at the barrel after each shot.
	muzzleSmoke: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/muzzle_smoke.json', import.meta.url).href,
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
	// Ornate cast-iron/bronze nameplate — unused by the live HUD (kept for the
	// parked rail). Live WAYS / MULTI / WIN use the woodReadout* carpentry boxes.
	barReadoutPlaque: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_readout_plaque.png', import.meta.url).href,
		preload: true,
	},
	// HUD timber boxes (tools/make_hud_wood_boxes.py) — same carpentry language
	// as the staircase, cut from a separate plank/scrap sheet (not the reel frame).
	woodReadoutWays: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/wood_readout_ways.png', import.meta.url).href,
		preload: true,
	},
	woodReadoutMulti: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/wood_readout_multi.png', import.meta.url).href,
		preload: true,
	},
	woodReadoutWin: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/wood_readout_win.png', import.meta.url).href,
		preload: true,
	},
	// Two rusty hanging chains drawn behind the HUD timber boxes.
	hudHangChain: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/hud_hang_chain.png', import.meta.url).href,
		preload: true,
	},
	// One unstretched rusty chain column for HUD hangers (never scale Y independently).
	hudChain: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/hud_chain.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueSplit: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_split.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueTombstone: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_tombstone.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueNudge: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_nudge.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueGang: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_split.png', import.meta.url).href,
		preload: true,
	},
	barPlaqueOutlaw: {
		type: 'sprite',
		src: new URL('../../assets/sprites/tombstone/bar_plaque_split.png', import.meta.url).href,
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
		src: new URL('../../assets/sprites/tombstone/bar_plaque_tombstone.png', import.meta.url).href,
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
	// LAST-REEL LANE door swing (tools/make_lane_door_atlas.py) — replaces the
	// static boarded cover when SUPER scatter / DIG UP opens the grave lane.
	laneDoor: {
		type: 'spriteSheet',
		src: new URL('../../assets/sprites/fx/lane_door.json', import.meta.url).href,
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
	sound: {
		type: 'audio',
		src: new URL('../../assets/audio/sounds.json', import.meta.url).href,
		preload: true,
	},
} as const;
