---
name: chitram-film
description: Turn any concept, prompt, product reference (screenshots, logo, URL, footage, voiceover) or reference video into a finished motion-graphics video (MP4) by writing the film as HTML/CSS/GSAP code and rendering it with our own frame-accurate renderer. Use whenever the user asks to make, create, animate, edit or render a video, product film, launch/promo/explainer/social reel, motion graphic, kinetic type, logo sting or title card; asks to "understand/analyse this reference video" or "make it like this video"; asks for a concept or a "detailed prompt"/timecoded brief for a video; or pastes a timecoded video prompt ("00:00–00:03 | THE HOOK …"). Two phases: DIRECTOR.md (understand input → concept → production brief → storyboard) and ENGINE.md (code → QA → render).
---

# Chitram Film — input → concept → brief → storyboard → code → MP4

A film here is **a web page that is a pure function of time**: one HTML file, one paused GSAP
timeline, local assets. `bin/render.mjs` seeks it frame by frame in headless Chromium and encodes
the frames with ffmpeg. Everything After Effects does as keyframes, we do as code — with CSS 3D,
SVG, gradients, blur and real fonts — and every frame is render-exact.

## The flow (always in order; levels never skipped, questions only when they change the film)

```
DIRECTOR.md                                                   ENGINE.md
L0 intake ─ L1 understand ─ L2 concept ─ L3 brief ─ L4 storyboard ─→ layout ─ animate ─ audio ─ QA ─ final look ─ render
   │           │              │            │           │                │                      │
   type,       refs audit,    pitch round  timecoded   frame table      sketch sheet           check.mjs --strict,
   formed?     reference-     (5 concepts, prompt in   + build sheet    (--at scenes)          contact sheet
   mode        video Shot     tail rule)   the user's                                          → MP4
               Log + DNA                   style
```

| Phase | Read | Output |
|---|---|---|
| 1. Direct (L0–L4) | `DIRECTOR.md` | `brief.md`: Product Truth · (Shot Log + Style DNA for reference videos) · concept + message sentence · Production Brief · storyboard proposal · Build Sheet |
| 2. Build | `ENGINE.md` | `index.html` + `cues.json` → `check.mjs` clean → storyboard/contact sheets → `out/film.mp4` |

- Only a prompt wanted (e.g. for another AI tool) → phase 1, then DIRECTOR §11.
- A complete timecoded prompt given → keep its creative verbatim; L2 is the user's concept; L3
  expands it (production layer only) and L4 turns it into the Build Sheet.
- Reference video given → `tools/analyze_video.py` first (DIRECTOR §1.5): borrow grammar, never content.
- Collaborative vs autonomous run modes: DIRECTOR §0. "Just build it / fast" = autonomous, same gates.

## Quick start

```bash
SKILL=.claude/skills/chitram-film
(cd $SKILL && npm install)                                   # once (+ `npx playwright-core install chromium` if no browser)
python3 $SKILL/tools/analyze_video.py ref.mp4 --out refs/ref  # if a reference video was given → read refs/ref/*.md + sheets
node $SKILL/bin/init.mjs films/<name> --duration 30 --size 1920x1080
#  … write films/<name>/brief.md (DIRECTOR), then index.html + cues.json (ENGINE) …
python3 $SKILL/audio/synth.py films/<name>/cues.json films/<name>/assets/score.wav
node $SKILL/bin/check.mjs  films/<name> --strict              # 0 errors, 0 unexplained warnings
node $SKILL/bin/render.mjs films/<name> --at scenes           # storyboard/contact sheet → read it
node $SKILL/bin/render.mjs films/<name> --out films/<name>/out/<name>.mp4
```

## Files

```
SKILL.md          this router
DIRECTOR.md       phase 1: levels & run modes · input paths (incl. reference video) · video types · product truth ·
                  concept pitch round · story math & spine · visual system · effect vocabulary · beat direction ·
                  expansion · audio design · brief / storyboard / build-sheet formats · gates · prompts for other tools
ENGINE.md         phase 2: runtime contract · layering · build procedure & stages · kit API · motion rules &
                  editor guardrails · video composition · recipes & scene shapes · editing · typography · assets ·
                  audio · QA · render · review loop · cost-aware mode
engine/           runtime.js (seek contract, footage sync, preview) · motion-kit.js (MK effects, transitions, rigs) ·
                  kit.css · fonts.css + fonts/ · vendor/gsap.min.js
bin/              init.mjs · render.mjs (video · --draft · --at t1,t2 | scenes | every:N) · check.mjs (QA gate) ·
                  preview.mjs · lib.mjs
audio/            synth.py (cue sheet → score + SFX + VO mix with ducking) · align_vo.py (split/label a voiceover)
tools/            analyze_video.py (watch a reference video) · prep_image.py (crop · unwarp · key · probe · palette) ·
                  prep_video.sh (footage → image sequence/webm)
template/         index.html + cues.json starting point
examples/         aasthi/ (premium fintech film + its brief — the quality reference) · showcase/ (kinetic kit demo) ·
                  recipes/ (recipe tests) · transitions/ (all MK.transition types)
```

## Rules that hold in every film

1. Direction before code. The brief's timecodes and copy are the contract; the film matches them.
2. Only approved copy on screen; brand spelled exactly; logos from the user's file, never redrawn.
3. Deterministic, offline page: no `Math.random`, clocks, CSS animations, CDNs (check.mjs enforces).
4. One reveal per element; exits via `to`; one transform owner per element; no CSS transforms on
   animated elements.
5. No overlaps, no unreadable text: every caption readable before it leaves, never over a
   protected element (`data-clear`), contrast-checked against its real background.
6. Look at the storyboard/contact sheet before the final render. Fix, re-check, render once.
7. Report honestly: what was built, deviations from the brief and why, warnings left and why.

## Choosing effort (keep quality, control cost)

- **Any model, any budget:** follow ENGINE §13. The kit, recipes, scene shapes and the QA gate
  carry the quality; a smaller model gets the same film by following them instead of improvising.
- **Hard creative asks** (custom 3D, unusual transitions, heavy footage): spend effort in the brief
  (precise description, CUSTOM rows) and on snapshots, not on rewriting the engine.
- Expensive steps: full renders and re-reading large files/images. Cheap: `check.mjs`, `--at`
  sheets, `--draft`. Use the cheap ones liberally; render the full film once.
