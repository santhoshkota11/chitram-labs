---
name: chitram-film
description: Turn any concept, prompt, or product reference (screenshots, logo, URL, footage, voiceover) into a finished motion-graphics video (MP4) by writing the film as HTML/CSS/GSAP code and rendering it with our own frame-accurate renderer. Use whenever the user asks to make, create, animate, edit or render a video, product film, launch/promo/explainer/social reel, motion graphic, kinetic type, logo sting or title card, asks for a "detailed prompt" or timecoded brief for a video, or pastes a timecoded video prompt ("00:00–00:03 | THE HOOK …"). Two phases: DIRECTOR.md (understand input → production brief + build sheet) and ENGINE.md (code → QA → render).
---

# Chitram Film — concept → brief → code → MP4

A film here is **a web page that is a pure function of time**: one HTML file, one paused GSAP
timeline, local assets. `bin/render.mjs` seeks it frame by frame in headless Chromium and encodes
the frames with ffmpeg. You get motion-design freedom (CSS 3D, SVG, gradients, blur, real fonts)
with render-exact results.

## The two phases (always both, in order)

| Phase | Read | Input → Output |
|---|---|---|
| 1. Direct | `DIRECTOR.md` | user concept/prompt/refs → **Production Brief** (timecoded, human-readable) + **Build Sheet** (scene table), saved to `brief.md` |
| 2. Build | `ENGINE.md` | brief → `index.html` + `cues.json` → check → snapshots → `out/film.mp4` |

If the user only wants the prompt/brief (e.g. for another AI video tool), do phase 1 and stop
(DIRECTOR §11). If the user gives a complete timecoded prompt, phase 1 is short: parse it into the
Build Sheet without rewriting their creative.

## Quick start

```bash
SKILL=.claude/skills/chitram-film
(cd $SKILL && npm install)                        # once: playwright-core (+ `npx playwright-core install chromium` if no browser)
node $SKILL/bin/init.mjs films/<name> --duration 30 --size 1920x1080
#  … write films/<name>/brief.md (DIRECTOR), then index.html + cues.json (ENGINE) …
python3 $SKILL/audio/synth.py films/<name>/cues.json films/<name>/assets/score.wav
node $SKILL/bin/check.mjs  films/<name>                     # must print 0 error(s)
node $SKILL/bin/render.mjs films/<name> --at 2,6,11,17,24,29  # snapshots → read contact-sheet.png
node $SKILL/bin/render.mjs films/<name> --out films/<name>/out/<name>.mp4
```

## Files

```
SKILL.md          this router
DIRECTOR.md       phase 1: intake, product audit, story math, visual system, effect vocabulary, audio design, brief + build-sheet formats
ENGINE.md         phase 2: runtime contract, layering, kit API, motion rules, recipes, editing, typography, assets, audio, QA, render, cost-aware mode
engine/           runtime.js (seek contract, footage sync, preview player) · motion-kit.js (MK effects & rigs) · kit.css · fonts.css + fonts/ · vendor/gsap.min.js
bin/              init.mjs · render.mjs (video, --draft, --at snapshots) · check.mjs (QA gate) · preview.mjs · lib.mjs
audio/            synth.py (cue sheet → score + SFX + VO mix with ducking) · align_vo.py (split/label a voiceover)
tools/            prep_image.py (crop · unwarp · key logo · probe · palette) · prep_video.sh (footage → image sequence/webm)
template/         index.html + cues.json starting point
examples/         aasthi/ (36.5 s premium fintech film with VO — the quality reference) · showcase/ (kinetic kit demo) · recipes/ (recipe tests)
```

## Rules that hold in every film

1. Brief before code. The brief's timecodes and copy are the contract; the film matches them.
2. Only approved copy on screen; brand spelled exactly; logos used from the user's file, never redrawn.
3. Deterministic, offline page: no `Math.random`, clocks, CSS animations, CDNs (check.mjs enforces).
4. One reveal per element; exits via `to`; never CSS transforms on animated elements.
5. Every caption readable before it leaves; reveals finish before the end hold; logo frame holds.
6. Look at snapshots before the final render. Fix, re-snapshot, then render once.
7. Report honestly: what was built, what deviates from the brief and why, what wasn't verified.

## Choosing effort (keep quality, control cost)

- **Any model, any budget:** follow ENGINE §13 (cost-aware mode). Kit functions and recipes carry
  the quality; the QA loop catches mistakes. Don't improvise effects the kit has.
- **Hard creative asks** (custom 3D, unusual transitions, heavy footage work): spend effort in the
  brief (precise description) and on snapshots, not on rewriting the engine.
- The expensive steps are full renders and re-reading big files. Snapshots and `check.mjs` are
  cheap — use them liberally; render the full film once.
