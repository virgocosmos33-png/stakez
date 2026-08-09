# Asset Checklist — TOMBSTONE REBORN

Drop the produced files at the listed paths (under `web-sdk/apps/tombstone-reborn/assets/`)
and the config layer picks them up. Sprites are transparent **webp** cards;
spines are Spine 4.x (`.atlas` + `.json` + page png) authored at scale 1.

Split into **MAIN GAME** (wired now in `src/game/assets.ts`) and **FEATURE PASS**
(added when Revenge Spins / bonuses land).

---

# MAIN GAME (current build)

## Symbol cards (sprites) — `assets/sprites/`
- [ ] `h1.webp` Gunslinger · `h2.webp` Duchess · `h3.webp` Butcher · `h4.webp` Card Shark · `h5.webp` Preacher
- [ ] `l1.webp` bullet · `l2.webp` whiskey · `l3.webp` spur · `l4.webp` horseshoe · `l5.webp` playing card
- [ ] `w.webp` revolver (wild)

## Symbol spines — `assets/spines/tr_symbols/` (`tr_symbols.atlas` + `{h1..h5,l1..l5}.json`)
Each rig needs animations: `<id>` (win), `<id>_land`, `<id>_postwin`. The
character-specific **death animations** (chandelier, caught cleaver, Ace of
Spades, last rite) can start as simple win idles now and be upgraded in the
feature pass.
- [ ] H1–H5 premiums — win / land / postwin
- [ ] L1–L5 lows — win / land / postwin (simple)

## Background — `assets/sprites/`
- [ ] `bg_graveyard.webp`

## Audio — `assets/audio/`
- [ ] `music_base.mp3` · `sfx_gunshot.mp3` · `sfx_reel_stop.mp3`

---

# FEATURE PASS (later — not wired yet)

Added when Revenge Spins, the KILL MULTIPLIER and the six win cutscenes land.
- [ ] `s.webp` tombstone (scatter)
- [ ] The Smile face rig — `assets/spines/gunslinger_face/` (`face_grim/faint/smirk/grin/evil`)
- [ ] Win cutscenes — `assets/spines/cutscene_{return,first_blood,payback,killer,last_rite,max_win}/`
- [ ] `bg_town.webp` (Revenge Spins)
- [ ] Audio — `music_revenge.mp3`, `sfx_reload.mp3` (CLICK×3), `sfx_church_bell.mp3` (DONG), `sfx_thump.mp3`, `sfx_scatter_stop.mp3`, `sfx_kill.mp3`, `vo_i_feel_better.mp3`

---

### Remaining engineering (beyond this config layer)
The `src/game/` config, types, board geometry and asset registry are done. To
make the app *run* in Storybook / against the mock RGS, still needed (copy the
patterns from `web-sdk/apps/white-room/` and `apps/ways/`):
- `package.json`, `svelte.config.js`, `vite.config.ts`, `.storybook/`
- `src/routes/` entry + `src/components/` (Board, Reel, Symbol, Win presentation)
- `src/game/` runtime glue: `stateGame.svelte.ts`, `actor.ts`,
  `bookEventHandlerMap.ts`, `typesBookEvent.ts`.
- `utils.ts` with `getReelYOffset` to centre the short reels into the coffin
  silhouette (see white-room `utils.ts`).
