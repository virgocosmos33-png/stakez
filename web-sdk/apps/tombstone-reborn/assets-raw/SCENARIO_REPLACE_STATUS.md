# Tombstone Kenney + Scenario replace status (2026-08-10)

## Approach (updated)
- **Visuals: Kenney FIRST** (canonical lib `C:\Users\Emex33\Documents\kenney assets\kenney assets`)
- **Audio: Scenario Sonilo only** (Kenney has no SFX)

## DONE — visuals (Kenney)
### Packs used
1. `kenney_particle-pack` — sparks, muzzle, smoke, dirt, scorch, slash, scratch, circle, flame, light
2. `kenney_smoke-particles` — White puff (25), Black smoke (25), Flash (9), Explosion (9)
3. `kenney_light-masks-1.0` — 20 Transparent circle/ring/cone/fan/window masks
4. `kenney_splat-pack` — 8 splat variants (blood-rust accents)
5. `kenney_fantasy-ui-borders` — border/divider samples for celebration chrome

Haul root: `assets-raw/kenney_haul_western/` (**161 PNGs**)
Atlas contract frames: `assets-raw/tombstone_vfx/` (all 17 Kenney copies present)
Baked: `static/assets/sprites/fx/tombstone_split_vfx.png` via `tools/make_tombstone_split_vfx_atlas.py`

### Live Game-mounted clinical → western
| Surface | Change |
|---------|--------|
| Anticipation.svelte | `drawDustAnticipation` (gunsmoke shaft) |
| WinSweep.svelte | `drawGunsmokeSweep` (no `drawMirrorSweep`) |
| WinCoins.svelte | `TOMBSTONE_COIN_FALL` brass/dust palette |
| WinCelebration.svelte | iron/brass bezel, dust damage, no CRT/fluorescent |
| CloneMorph.svelte | brass/dust charge+flash (no white/glass) |
| WinLightning.svelte | `drawPowderStrobe` (emitter type; not currently mounted) |
| Shared | helpers in `src/game/tombstoneVfx.ts` |

### Left alone (already Tombstone)
BulletHoleMark, TargetLock, SplitPanes powder seams, special bar plaques, board/HUD layout

## DONE — audio (partial, prior run)
Western Sonilo samples already in `assets-raw/audio_gen/` and baked into sprite for:
UI clicks, btn, reel stops, symbol/royal landing, scatter family, bullet wood/ricochet, claw_split, bgm_main, bgm_freespin

## BLOCKED — Scenario rate limit (2026-08-10)
MCP `model_run` Sonilo returned:
```
429 RateLimitError — wait ~2321s (~39 min) before retry
cooldownSeconds: 2700
```
Earlier VFX path also hit team CU plan limit (`PlanLimitReachedError`). Visuals no longer need Scenario (Kenney covers).

### Exact remaining SFX queue (44 cues — regenerate then `python tools/rebuild_audio_sprite.py`)
Priority player-facing:
- `sfx_anticipation_start`, `sfx_anticipation`
- `sfx_wild_explode`
- `sfx_multiplier_landing`, `sfx_multiplier_combine_a`, `sfx_multiplier_combine_b`
- `sfx_madams_eye`, `sfx_thunder`
- winlevels: `sfx_winlevel_small/nice/standard/substantial/end`, `sfx_youwon_panel`, `sfx_bigwin_coinloop`
- multipliers: `sfx_multiplier_explosion_a/b/c`, `sfx_multiplier_reset/up/update/win`
- FS: `sfx_fs_respins`, `sfx_superfreespin`, `jng_intro_fs`
- celeb: `sfx_celeb_*` (whoosh/swell/wobble/buildup/hit/maxslam)
- cell seal: `sfx_cell_seal_*`
- tumble: `tumble_win_1..5`
- misc: `sfx_mirror_break`, `sfx_xways_split`

Superseded: audio no longer comes from Scenario. The whole set is generated
through Layer AI and assembled locally:

```powershell
python tools/fetch_layer_stems.py
python tools/build_tombstone_audio.py
python tools/rebuild_audio_sprite.py
```

The music beds are the exception: `bgm_main`, `bgm_freespin` and
`bgm_celeb_1..6` are finished tracks living in `assets-raw/audio_gen`, not
composed from stems. No key points at an old Madam / White Room sample.

## NOT DONE this pass
- Transition spine debris art still clinical (asset regen out of scope without Scenario CU; Transition is Game-mounted)
- CellSealOverlay / LockedSlots / FreeSpinIntro-Outro clinical chrome (sibling surfaces; not in priority list)
- Live Storybook visual QA of anticipation/win stories after hard refresh
