# DIRECTOR — understand the input, write the production brief

Phase 1 of 2. Input: whatever the user gave (a one-line idea, a long timecoded prompt, product
screenshots, a logo, a URL, footage, a voiceover). Output: a **Production Brief** (human-readable,
timecoded) and a **Build Sheet** (machine-ready scene table) that `ENGINE.md` turns into code.

Nothing in this phase writes HTML. Do not skip it, even for "make it fast" requests: a 5-minute
brief is what makes the build correct the first time. Fast means *fewer questions*, not *no brief*.

---

## 0. The levels (follow in order, every time)

The direction work runs in five levels. Each level has one output; nothing later re-asks what an
earlier level settled.

| Level | Name | Output | Sections |
|---|---|---|---|
| **L0** | Intake & triage | input path(s), video type, formed/unformed, run mode | §1, §1.6 |
| **L1** | Understand | Reference audit + Product Truth; for reference *videos*: Shot Log + Style DNA | §2, §1.5 |
| **L2** | Concept | one chosen concept (the "telling"), with the message sentence | §4.0 |
| **L3** | Brief | Production Brief (timecoded, the user's prompt style), expanded and gated | §3–§8, §9.1, §10 |
| **L4** | Storyboard | frame-table proposal + Build Sheet (+ optional sketch sheet) → hand-off to ENGINE | §9.2, §9.3 |

Procedure:
1. **Classify the input** (§1) → pick the intake path(s) and video type (§1.6); mark it *formed*
   (message + material + occasion are readable) or *unformed* (a subject with no take on it).
2. **Understand** (§2, §1.5) → Product Truth; Shot Log + Style DNA for every reference video.
3. **Concept** (§4.0): formed requests keep the user's concept; unformed ones get a pitch round.
4. **Lock the format** (§3): duration, aspect, fps, audio mode, finish-by time.
5. **Write the story** (§4) → beats with durations that add up exactly.
6. **Design the visual system** (§5).
7. **Direct each beat** (§6, §6.5, §7) and the audio (§8). Expand, never pass through (§6.6).
8. **Gate** (§10). Fix anything that fails.
9. **Emit** the Production Brief (§9.1) + Storyboard proposal and Build Sheet (§9.2–9.3) into
   `brief.md`. Hand off to `ENGINE.md`. If the user only asked for a prompt, stop and adapt (§11).

### Run modes
- **Collaborative** (default when the user is present and the request is unformed or big):
  pause after L2 (show the pitch round) and after L4 (show the storyboard proposal); after the
  build, show the storyboard sheet before the final render.
- **Autonomous** ("just build it", "create fast", "don't ask", or a complete prompt was given):
  make every decision yourself, write each one down with a one-line reason ("receipt"), post the
  L2/L4 summaries as heads-ups without waiting, and still show a contact sheet with the delivery.
  Autonomous never means skipping a level — the gates still run.
- In both modes: ask a question only when the answer changes the film and can't be defaulted
  (§1 "When to ask"), one question per message, recommended option first with its reason.

---

## 1. Classify the input

| Path | What the user gave | What you do |
|---|---|---|
| **A. Full brief** | A timecoded prompt with scenes/copy/audio (like the AASTHI or SnapCaption prompts) | **Do not rewrite their creative.** Parse it into the Build Sheet. Only fill gaps (missing timings, colours, sizes) and flag conflicts (timings that overlap, copy that can't be read in the time given, effects that need footage you don't have). |
| **B. Concept** | An idea: "a launch video for my budgeting app", "30s film for NRIs investing in India" | Write the whole brief yourself using §4–§8. Offer 2 story directions in one line each only if the concept is truly ambiguous; otherwise pick the strongest and go. |
| **C. Product refs** | Screenshots, mockups, logo, URL, footage, brand guide, VO | Audit (§2) first; the refs define the palette, copy and devices. Then continue as B (or A if a prompt came with them). |
| **D. Vibe only** | "something premium", "like Apple", "CRED-style" | Translate the vibe with the Style Lexicon (§5.6) into a concrete visual system, then continue as B. |

| **E. Reference video(s)** | "make it like this", a competitor ad, a film they love, their old video | Deconstruct it (§1.5) into a Shot Log + Style DNA. Borrow its grammar for the user's product; never copy its content. |

Inputs are usually mixed (e.g. A + C, or B + E). Apply every path that matches.

**Partial prompts.** If the prompt is cut off (starts mid-scene, e.g. "…00:38.5–00:42 | THE STATEMENT
STACK"), build what is specified, keep its timecodes, and ask for the missing part **once** in your
reply while you proceed with what you have. Never invent the missing scenes silently.

### When to ask questions
Ask only if the answer changes the build and cannot be defaulted. Max 3 questions, one message.
Blocking: brand name spelling when refs disagree; a required asset you don't have (e.g. "creator
footage" — you cannot fabricate a real person); legal claims ("guaranteed returns"). Everything else
takes a default:

| Unknown | Default |
|---|---|
| Duration | 30 s (social teaser 15 s, explainer 45–60 s) |
| Aspect | 16:9 1920×1080. "reel / story / TikTok / shorts" → 9:16 1080×1920. "feed / post" → 1:1 1080×1080 or 4:5 1080×1350 |
| FPS | 30 (60 only if asked; doubles render time) |
| Audio | Original synthesized score + SFX, no narration |
| Finish-by | All reveals done by `duration − 1.5 s`; hold the final frame (logo + tagline) to the end |
| Tone | Premium, calm, confident |
| Copy | Short lowercase lines; brand names and acronyms keep their case |

### 1.5 Reference video → Shot Log + Style DNA (path E)

A model can't watch video, so turn the video into things you *can* read:

```bash
python3 $SKILL/tools/analyze_video.py ref.mp4 --out refs/<name>_analysis
```
It writes `analysis.md` (shots with cut times, camera-motion guess, brightness, palette; *beats*
inside continuous shots; audio tempo, hits and quiet spans; motion-energy curve) and image sheets:
`shots_NN.jpg` (4 frames across every shot), `timeline_NN.jpg` (a frame every ~0.5–1 s — the film
as a flipbook) and `overview.jpg`. **Read `analysis.md`, then every sheet.** Then write two blocks
into `brief.md`:

**Shot Log** — one row per beat (use the analysis times; correct them from the sheets):
```
| # | time        | frame / subject                  | camera            | type on screen            | enters by / exits by     | sound         |
|---|-------------|----------------------------------|-------------------|---------------------------|--------------------------|---------------|
| 1 | 0.00–3.50   | black void, centred serif line   | locked            | 2 lines, blur-in, sweep   | fade in / fade to cream  | pad + piano   |
| 2 | 3.50–7.50   | laptop rises into cream studio   | orbit 3/4→front   | serif caption left        | continuous / push-in     | soft impact   |
```

**Style DNA** — what makes it *that* video, in transferable terms:
```
Structure:     hook → reveal → 3 proofs → trust → logo (6 beats in 30 s, avg beat 4.1 s)
Rhythm:        slow-BUILD-breathe-PEAK(whip @ 50%)-breathe-hold; cuts on beat: 0% (continuous film)
Camera:        weightless orbits + push-ins on one hero object; never cuts
Transitions:   push through screen, light-streak whip ×1, fade through black ×2
Type system:   lowercase serif 90–120 px, captions beside the hero, 1 idea per line, blur-in + sweep
Palette logic: cream day / near-black night alternation; one brand accent per scene
Signature:     UI cards peel off the screen into depth; gold light sweep over letters
Sound:         warm pad bed, pulse from the reveal, shimmer per card, chime on the logo
Density:       sparse — 1 hero + ≤ 1 caption per frame, ≥ 40 % empty space
```

**Transfer rules (style transfer, not copying):**
- Borrow **grammar**: structure, beat lengths, rhythm, camera language, transition kinds, type
  scale/placement logic, palette *logic*, sound logic, signature *mechanics*.
- Never borrow **content**: their brand name, copy, logos, product UI, characters/people, music,
  or distinctive artwork. Re-skin everything with the user's product truth and palette.
- Scale the structure to the user's duration (keep the proportions of the beats, §4.1 shares).
- If the reference has people/footage and the user has none, translate those beats into
  product/typography beats (device, UI, kinetic type) and say so.
- If several references disagree, pick one as the **spine** (structure/rhythm) and take only
  named elements from the others ("spine: ref A; card-peel mechanic from ref B").

### 1.6 Video type (the route) — decides the story template and defaults

| Type | Recognise it by | Default length / aspect | Story template (§4.2) | Notes |
|---|---|---|---|---|
| **Product launch / brand film** | a product, site, app, screenshots, "launch/promo/ad" | 20–45 s · 16:9 | launch | device hero, UI peel-offs, trust, logo |
| **Site / app showcase** | "show our site/app as it is" | 30–60 s · 16:9 | app demo | the real screens are the star; captions beside |
| **Explainer (faceless)** | a topic, article, notes; nothing to sell | 30–90 s | explainer | invented diagrams, kinetic type, data (only real data) |
| **Motion graphic / sting** | < 10 s, no narration, motion *is* the message: logo sting, title, stat, lower-third | 3–10 s | one beat | autonomous; at most one question |
| **Music-driven** | a track given, "beat-synced", "lyric video" | track length | beat grid | analyse the track (analyze_video/align tools), cut on beats |
| **Changelog / code** | a PR, release notes | 20–90 s | explainer | value first, code as evidence |
| **Captions on footage** | talking-head clip + "captions/subtitles" | clip length | none | footage untouched; caption layer only |
| **Overlays on footage** | talking-head + titles/lower-thirds/callouts | clip length | none | footage untouched; cards synced to speech |
| **Social teaser** | reel/story/short/TikTok | 8–15 s · 9:16 | teaser | hook in frame 1; brand by 80 % |
| **Other / custom** | anything else | as asked | closest template | — |

Decks/interactive slides are not videos — say so and offer a video version instead.

---

## 2. Reference audit → Product Truth

For **each** reference, write one block (keep it in `brief.md`):

```
REF <n>: <filename>
  what it is:      e.g. "dark hero landing page on a silver MacBook, frontal"
  exact copy:      every readable string, verbatim (spelling, case, punctuation)
  colours:         run `python3 tools/prep_image.py palette <file>`; name each hex (bg, text, accent)
  device & angle:  frontal / 3-4 left / 3-4 right / top-down; screen corners in pixels if you'll unwarp
  usable as:       screen texture (crop|unwarp) | logo (key) | photo | style reference only
  keep exact:      what must never change (logo shape, UI layout, wording)
```

**User labels can be wrong.** If the user says "@Image4 = hero page" but image 4 is the logo, trust
the **content**, map by what you see, and say so in one line of your reply.

Then write the **Product Truth** (≤ 10 lines):

```
Brand:        AASTHI            (exact spelling, case — copy from the logo/wordmark)
What it is:   platform for NRIs to invest in India's private markets
Audience:     NRIs abroad (US, UK, UAE…), 28–50, finance-literate
One promise:  invest in India. from anywhere.
Proof points: KYC verified · risk disclosed · IFSCA regulated
Tone:         calm, trustworthy, premium (CRED-like)
Must not:     fake numbers/returns, real third-party logos, people unless footage is provided
Assets:       hero screen (crop), how-it-works screen (rebuild in HTML), trust grid (rebuild), logo (key)
```

**Regulated or sensitive products** (finance, health, legal, kids): no invented numbers, no
"guaranteed", charts without axis values, disclaimers stay legible if present in refs.

**Rebuild vs. crop.** A screenshot seen straight-on at ≥ 800 px wide → crop it and use it as a
screen texture. A screenshot seen at an angle, or UI that will be shown large or have parts
lifted off it → **rebuild it in HTML/CSS** with the exact same copy, layout and colours (sharper,
animatable). Photos inside UI (hero images) → always crop from the reference.

---

## 3. Lock the format

Write this block at the top of the brief. The Build Sheet must sum to exactly `DURATION`.

```
FORMAT:   16:9 · 1920×1080 · 30 fps · 30.0 s
AUDIO:    score + sfx (no VO)        | or: user VO synced to captions | or: silent
FINISH:   all reveals complete by 28.5 s; hold logo + tagline 28.5–30.0
DELIVER:  MP4 H.264 + AAC
```

**Voiceover changes the clock.** If the user gives a VO, the VO's phrase timings drive the
choreography (captions appear when their words are spoken). Measure it first
(`audio/align_vo.py`), then fit the beats to it. If VO is longer than the requested duration,
propose the smallest fix in this order: (1) tighten gaps between phrases, (2) speed VO ≤ 1.08×,
(3) extend the ending, (4) cut a line. Tell the user which you chose.

---

## 4. Story

### 4.0 Concept — the telling (L2)

Facts don't make a film; a *telling* does. "Make a video about our app" is formed about the facts
and unformed about the telling. Before any beat math:

**If the user already has a concept** (a full prompt, or a clear picture): that is the concept.
Echo it as the message sentence and move on.

**If the request is unformed → pitch round.** Work this gate privately, then present.
1. Answer four questions *specifically* for this subject:
   - What does the subject look like — its own visual world (materials, places, objects, UI)?
   - What does the target emotion look like as a frame (longing = space the eye wants to fill;
     urgency = compression; trust = stillness and order; awe = one thing too big for the frame)?
   - What does the playback surface demand (feed: win the first second; lobby screen: ambient;
     vertical story: fast and close)?
   - What does *every other* video on this subject look like? That is the thing to avoid.
2. Write **five concepts from five different paths**: (a) the subject's own world, (b) the emotion,
   (c) the audience (meet or break their expectation), (d) the cliché inverted, (e) an unusual
   format (a letter, a countdown, a receipt, a front page, a map, a single continuous shot).
3. **Tail rule:** estimate privately how likely a typical model would be to produce each concept.
   At least **two** must be unlikely (< 10 %). If all five are typical, start over.
4. **Silhouette rule:** sketch each concept's main shapes as rough boxes; two concepts with the
   same silhouette are one concept — replace one.
5. Present each in three lines: the idea in one sentence · its visual world (naming the one or
   two effects/capabilities it rides, in plain words: "the UI cards peel off the laptop") · its
   opening hook. Show all five, then recommend one with a reason. Mixing is a valid answer.
6. **Autonomous:** run the same gate, pick the winner, and in the heads-up name the direction you
   chose, why, and the most typical direction you deliberately left behind.
7. **User knows nothing about video:** don't pitch or quiz. Offer 2–3 decision surfaces that
   really change the result (where it plays · how long · how it should feel), each with 2–4 plain
   options and a marked default; decide the rest and show the concept inside the brief summary.

End L2 with the **message sentence**: *"This film tells [audience] that [one message]."* Every
beat must trace back to it; a beat that can't is cut, not decorated.

### 4.1 The arc
Every film, any length, follows this spine. Name each beat in the brief.

| Beat | Job | Share of runtime |
|---|---|---|
| **Hook** | One line that creates tension or recognition. Dark or minimal frame, text only. | 8–12 % |
| **Reveal** | The product/hero object appears. Biggest single move of the film. | 12–15 % |
| **Promise** | What it does, in one line, over the hero. | 10 % |
| **Proof / How** | 2–4 short beats: features, steps, benefits. Parallel copy ("apply. verify. get access."). | 35–45 % |
| **Trust / Payoff** | Why believe it (security, results, social proof without fake numbers). | 10–12 % |
| **Resolution** | Brand line → logo lockup → tagline (+ CTA). Hold. | 10–15 % |

### 4.2 Arc templates by video type

- **Product launch / brand film (20–45 s):** Hook (problem in 5 words) → device rises with the
  product → push into the product's signature visual → 3 feature beats with UI lifting off the
  screen → trust triad → brand line + logo.
- **Feature explainer (30–60 s):** Hook (question) → the old way (grey, slow) → the new way (colour,
  fast) → 3 steps numbered → result → CTA.
- **Social teaser (8–15 s, often 9:16):** Hook in the first 1.0 s (big type, motion from frame 1)
  → one hero effect → brand + CTA by 80 % of runtime. No slow fades at the start.
- **App demo (30–60 s):** phone rig → each screen = one beat; tap = click SFX + ripple; captions
  beside the phone, never over the UI.
- **Offer / event (10–20 s):** Headline → the offer (big, one line) → date/place → CTA; loud
  kinetic type, beat-synced cuts.
- **Caption/creator tool (like SnapCaption):** creator footage inset → captions appear karaoke-style
  → style variety wall → aspect-ratio phone rotation → statement stack → brand + CTA.

### 4.3 Beat math (use it; don't guess)

- **Reading time** for a caption: `0.6 s + 0.22 s × words` (min 0.8 s, cap 2.5 s) of *full
  visibility*, not counting its reveal and exit. A 5-word line needs ≥ 1.7 s fully visible.
- **Reveal** 0.5–1.1 s, **exit** 0.35–0.6 s. So a 5-word caption costs ≈ 1.0 + 1.7 + 0.5 = 3.2 s.
- **Captions per beat:** 1 headline, or a list of ≤ 3 short items (1–3 words each) that stack.
- **Max words on screen at once:** 12 (headline) · 18 (headline + sub).
- **Scene count** ≈ `duration / 3.5` for premium pacing, `duration / 2` for kinetic/social.
- **Transitions** 0.4–1.0 s each; budget them inside the scene that ends.
- **End hold:** ≥ 1.5 s of a static, fully revealed logo/tagline frame (only a gentle glow may move).
- Sum every beat. It must equal the duration to 0.1 s. Write the running timecodes.

### 4.4 Copy rules

- Write for the eye: short lines, one idea per line, no commas where a line break works.
- Parallel triads land: "apply. verify. get access." · "discover. review. choose."
- Luxury register: lowercase, full stops, understatement. Tech register: sentence case, verbs.
  Playful register: short punchy words, one exclamation max.
- Brand names, acronyms and proper nouns keep their case inside lowercase lines
  ("invest in India. from anywhere.", "KYC verified.", "IFSCA regulated.").
- **Only the copy the user gave or approved appears on screen.** UI rebuilt from refs uses the refs'
  exact copy. Placeholder UI uses **skeleton bars**, not invented words or numbers.
- Spell the brand exactly as the logo does. Put the spelling in QUALITY AND CONSTRAINTS.

### 4.5 Story spine (value first)
- **The hook speaks the viewer's language** — what they gain, avoid or finally feel — never the
  product's internal vocabulary (feature names, file names, section headings). Numbers only when
  they carry stakes and are real.
- **The value claim (the message) lands by the second beat.** Everything after is evidence.
  Self-test: delete the evidence beats — the rest must still state the value; delete the value
  beats — if the film still "works", it was a feature tour, not a story.
- **Visuals come from the source.** Mine the product's own screens, words, objects and motifs for
  props before inventing any. If a prop could appear unchanged in another brand's video, replace it
  with something only this product has.

---

## 5. Visual system

### 5.1 Palette (from refs first)
Run `tools/prep_image.py palette` on the logo and main screen. Build 5–7 tokens:

```
--bg-dark   #0B0B0E   near-black void (dark scenes)
--bg-light  #F7F1EC   studio cream (light scenes)   → gradient to #CDB3AA at the floor
--ink       #1A1A1A   text on light
--paper     #FFFFFF   text on dark
--brand     #7B6CF6   logo violet (glows, streaks)   gradient #8F7CF8 → #2E2496
--accent    #E3B34A   gold (highlight words, icons)
--ui        #1B2A5E   navy (buttons, step numbers)
```
Rules: 60 % background, 30 % neutral/secondary, 10 % accent. One accent colour per scene for
highlight words. Alternate dark and light scenes to create rhythm (dark hook → light product →
dark trust → dark/brand resolution works well).

### 5.2 Typography pairings (all bundled, see ENGINE.md §9)

| Register | Headline | Captions / UI |
|---|---|---|
| Luxury / fintech / fashion | Cormorant Garamond 500 (lowercase), or Instrument Serif | Inter 500, tracking .12–.16em |
| Editorial / premium tech | Fraunces 400–600, or Playfair Display 400 | Inter / Manrope |
| Modern SaaS / creator tools | Manrope 800 (tight −.03em), Plus Jakarta Sans 800 | Manrope 600 |
| Tech / dev | Space Grotesk 700 | JetBrains Mono 400 |
| Bold display, warm | DM Serif Display | Plus Jakarta Sans |

Size scale at 1920×1080: hero 110–130 px · headline 84–100 · sub 60–72 · caption 40–48 ·
eyebrow/label 22–28 (tracked). 9:16 (1080×1920): hero 120–150 · headline 88–100 · caption 48–56.
Text block width 30–50 % of the frame. Serif display lines: leading 1.02–1.08.

### 5.3 Backgrounds
- **Studio void:** seamless gradient, lighter at the top-left key light, darker at the floor, soft
  floor shadow under floating objects.
- **Dark void:** near-black with a subtle brand-colour lift in the centre (radial, 20 % opacity).
- **Ambience:** 4–6 defocused bokeh blooms at frame edges in brand colours, drifting slowly.
  Never more; "excessive particles" is always a constraint.
- **Graphic:** gradient washes with soft light pools, big pale repeated type walls (6–8 % opacity).

### 5.4 Materials & light (describe them; the engine has presets)
Brushed aluminium, frosted glass, dark UI glass, glossy specular sweeps, rim light on edges,
soft key from upper-left. Say "no grain, no harsh flares, no lens flares" unless asked.

### 5.5 Motion personality → pick ONE for the whole film

| Personality | Feel | Eases | Typical durations | Transitions |
|---|---|---|---|---|
| **Weightless premium** (CRED, Apple) | slow, floating, confident | power2/3.out, sine.inOut | reveals 0.9–1.2 s, camera 2.5–4 s | push-in through screen, fade through black, light-streak whip |
| **Kinetic modern** (SaaS, creator) | snappy, rhythmic, beat-synced | power4.out, expo.out, back.out(1.7) | reveals 0.35–0.6 s, moves 0.5–0.9 s | blob wipe, block wipe, hard cut on beat, ribbon wipe |
| **Playful** (consumer, food, kids) | bouncy, elastic | back.out(2.5), elastic.out(1,.5) | 0.4–0.7 s | pop, scale-through, colour wipe |
| **Editorial calm** (luxury, culture) | still frames, typography-led | power1.inOut, none (linear drifts) | 1.2–2 s | slow crossfade, mask rise |

### 5.6 Style lexicon (vibe words → concrete choices)

| User says | Means |
|---|---|
| "CRED-style", "luxury product film" | Weightless premium; cream/black voids; lowercase serif; device hero; glossy light; no cuts |
| "Apple-style" | White/black void; SF-like sans (Inter 600); huge centred type; slow rotations; one idea per frame |
| "Stripe / Linear" | Dark UI glass, gradient glows, precise small type, grid lines, fast eased moves |
| "kinetic", "motion graphics", "After Effects vibe" | Kinetic modern; block/glitch reveals; shapes travelling; beat-synced |
| "minimal" | 1–2 colours, one element per scene, lots of negative space |
| "premium" | Slower than you think, fewer elements, bigger type, real materials |

---

## 6. Effect vocabulary (only use buildable effects)

Every effect in the choreography must map to a kit function or a documented recipe in
`ENGINE.md` §6. Write the effect in plain language in the brief and put the function in the Build
Sheet. If the user asks for something not listed, describe it precisely (what moves, from where,
how long, what it reveals) and mark it `CUSTOM` in the Build Sheet.

| Effect (brief wording) | Kit / recipe |
|---|---|
| text resolves from blur to sharp with a soft light sweep | `MK.blurIn` |
| line rises from behind an invisible edge | `MK.maskRise` |
| words rise one by one | `MK.wordsRise` |
| cream block wipe reveals each line | `MK.blockWipe` |
| last line pops in with a small overshoot | `MK.popIn` |
| text types in with a caret | `MK.typewriter` |
| karaoke word highlight | `MK.karaoke` |
| glitch-block text reveal | `MK.glitchIn` |
| gradient highlight block wipes across a word | `MK.highlight` |
| line-art draws on / erases | `MK.lineDraw` / `MK.lineErase` |
| line wipes out through a horizontal blur mask | `MK.blurWipeOut` |
| gold-and-violet light-streak whip | `MK.whip` |
| large rounded blob sweeps in as a wipe | `MK.blobWipe` |
| fade through black / colour | `MK.fadeThrough` |
| scene crossfade ("this continues") · blur crossfade · zoom through · push · whip pan · iris · blinds · shutter · colour dip · hard cut ("wake up") | `MK.transition` type `crossfade` · `blur` · `zoom` · `push` · `whipPan` · `iris` · `blinds` · `shutter` · `dip` · `cut` |
| defocused bokeh drifting at the edges | `MK.bokeh` + `MK.drift` |
| floating silver laptop, orbit, push-in to screen | `MK.laptop` + rig tweens (recipe 6.1) |
| UI cards peel off the screen and float in depth | `MK.lift` / `MK.settle` (recipe 6.2) |
| phone rotating between aspect ratios | `MK.phone` (recipe 6.6) |
| text riding a circle arc | `MK.arcText` |
| rotating dimensional band with text on it | `MK.band` |
| pale repeated typography wall | `MK.typeWall` + `MK.wallScroll` |
| glowing tube threading through blocks | `MK.tube` + `MK.tubeDraw` (recipe 6.9) |
| rosette / flower mark rolls in, becomes a bullet | `MK.rosette` (recipe 6.8) |
| glossy specular sweep across a device | `MK.gloss` |
| hover bob | `MK.hover` |
| breathing glow behind the logo | `MK.breathe` |
| pill morphs into a ring with a spark | recipe 6.10 |
| rotating square releases a shape | recipe 6.11 |
| ribbon weaves behind and in front of an inset | recipe 6.12 |
| floating glass UI assembly | recipe 6.3 |
| chart line draws on with glow (no numbers) | recipe 6.4 |
| logo lockup resolve (mark + wordmark + tagline) | recipe 6.5 |

### 6.5 Direct each beat (a world, not a layout)

For every beat write five things — before any pixels:
1. **Concept** — 1–2 sentences: what world are we in, what should the viewer *feel*. ("The laptop
   drifts up out of the dark like something surfacing; the studio warms around it.")
2. **Mood references** in words, not hex ("Apple keynote product float", "Bauhaus colour study",
   "editorial magazine spread").
3. **Depth layers** — BG (void, glow, ghost type, light pools) · MG (the message: device, cards,
   headline) · FG (accents: bokeh passing, hairlines, labels). At least two layers per beat.
4. **A motion verb for every element.** If you can't name the verb, the element isn't designed.
   Verbs by character — impact: *slams, drops, stamps* · directional: *slides, pushes, wipes* ·
   reveal/build: *draws, fills, assembles, types on* · organic: *floats, drifts, breathes, orbits* ·
   mechanical: *snaps, clicks, locks in, steps*. The verb follows the concept, not an "energy" level.
5. **Transition out** with type and parameters ("light-streak whip, 0.8 s, streaks gold/violet,
   stage blurs out right and back in from the left") and its **SFX**.

Then declare the film's **rhythm** in one line before detailing scenes, e.g.
`slow-BUILD · breathe · PUSH · list · WHIP · list · breathe · trust · HOLD`. Rhythm comes from the
brand and message, not the duration: a 15 s ad for an architect and one for a game have different
rhythms.

### 6.6 Expand — never pass through

Every brief, even a complete user prompt, gets enriched before the build. Keep the user's content
and wording exactly; **add only the production layer** they didn't write:
- atmosphere per scene (2–5 background elements: glows, ghost type, light pools, hairlines, bokeh),
- a secondary (ambient) motion for each decorative (breathe, drift, pulse, orbit — finite loops),
- transition choreography at the object level ("the card settles back *into* the screen and the
  screen's content dissolves to the dashboard"), with duration and ease,
- pacing inside each beat: build (first ~30 %) → breathe (~40 %, one ambient motion) → resolve,
- exact values from the visual system (hex, font, size, ease) so the build guesses nothing.

Never add: new on-screen copy, claims, numbers, logos, people, scenes or effects that change the
story. Enrichment is decoration and precision, not new content.

---

## 7. Choreography rules

- **One hero move at a time.** The camera move, the device move and the text reveal must not all
  peak together. Stagger: move starts → text reveals 0.3–0.6 s after the move begins.
- **Text never sits on busy content.** Put captions beside the hero (left third when the device is
  right, and vice versa). If text must overlay a screen, darken/blur the screen behind it.
- **Depth:** background 0 → ambience → hero object → lifted cards (in front of the hero) → text →
  transition layer. Cards lift toward the camera and away from the caption side.
- **Continuity:** the hero object stays the same object (same device, same finish) across scenes;
  scene changes happen *on* it (screen content wipes) or through a transition — never a jump.
- **Rhythm:** alternate long (3–5 s) and short (1–2 s) beats. Land reveals on the beat grid when
  there's a pulse (bpm 90–120 → one beat = 0.5–0.67 s).
- **Readability first:** every main phrase fully readable before it leaves (§4.3 math).
- **Finish early, hold long:** everything revealed by the finish-by time; only ambient glow moves
  during the hold.

---

## 8. Audio design

Default is an **original synthesized score** (no licensing issues), built by `audio/synth.py`
from a cue sheet. Describe it in the brief; the Build Sheet lists every cue time.

| Film mood | `mood` | bpm | Chords |
|---|---|---|---|
| Premium warm (fintech, luxury) | warm | 90–100 | major 9ths/add9 (D, Bm11, Gmaj9, A6/9) |
| Bright modern (SaaS, creator) | bright | 105–120 | A, F#m, D, E (sus, add9) |
| Dark trust/security | dark | 80–90 | Em9, Cmaj7, Am9 |
| Playful | playful | 110–128 | C, F, G, Am with plucks |

**SFX map (motion → sound):** card lift / sparkle → `shimmer` · light-streak whip / big
transition → `whoosh` · ribbon, band, blob wipe → `swoosh` · object lands / big reveal → `impact`
· toggle, dropdown, karaoke word → `click` · glitch-block reveal → `tick` (+ `glitch` on the first)
· overshoot pop / sticker → `pop` · into a new section → `riser` (ends on the section start) · logo
→ `chime` · travelling shapes, rosette → `plucks`.

Rules: pulse stops for whips and for the final hold; the chime lands on the logo reveal; fade
the last 0.8–1.0 s; no narration unless provided; VO always ducks the music (`vo.duck` 0.5–0.6).

---

## 9. Output format

### 9.1 Production Brief (this exact structure)

```
TITLE — <Brand> · <film type> · <duration> · <aspect>

FORMAT
16:9 · 1920×1080 · 30 fps · 30.0 s · finish reveals by 28.5 s, hold to 30.0 s

STYLE
<2–3 sentences: genre, references in words, what it must feel like, what it must not be.>

REFERENCES
REF1 = <what it is> → used as <screen texture / rebuilt UI / logo / style only>. Keep exact: <…>
REF2 = …

CREATIVE APPROACH
The story: <beat → beat → beat → … in one line>.
<2–4 sentences on the hero object, how scenes connect, where type lives.>

VISUAL SYSTEM
Background: … Brand colours: … (hex) Materials: … Lighting: …

TYPOGRAPHY
Headlines: <font, weight, case, colour per background>. Captions: … Size range: … Width: 30–50 %.

MOVEMENT
<motion personality, camera language, how cards/text/transitions move, eases in words>

EXACT CHOREOGRAPHY
00:00–00:03 | THE HOOK
<what the frame is, what moves, exact copy in quotes, effect names, where it sits, when it leaves>
00:03–00:07 | THE REVEAL
…
00:27–00:30 | BRAND RESOLUTION
… Finish revealing everything by 00:28.5. Hold … until 00:30.

AUDIO
<score description, then one line per SFX family with when it plays; ending tone time; VO or "no narration">

QUALITY AND CONSTRAINTS
Keep every headline readable before it transitions. Generate only the specified copy.
Spell "<Brand>" exactly. Preserve the logo exactly. <product-specific musts and must-nots>
No people/hands (unless footage provided), no fake numbers, no real third-party logos, no
excessive particles, no harsh flares, no watermarks.
```

This is the same style as the AASTHI and SnapCaption prompts the user writes — keep that voice:
present tense, concrete nouns, exact copy in quotes, timecodes on every scene.

### 9.2 Build Sheet (hand-off to ENGINE)

One row per timed action. Times are absolute seconds. Every copy line appears exactly once as a
`text` row. `layer` names become element ids.

```
| t_in  | t_out | scene | layer/id   | kind   | content / copy                        | effect (kit fn, key params)                 | sfx          |
|-------|-------|-------|------------|--------|---------------------------------------|---------------------------------------------|--------------|
| 0.25  | 3.45  | hook  | c0         | text   | "you moved to the US."                | fadeIn y10 · blurOut 2.95                   |              |
| 1.40  | 3.60  | hook  | h0         | text   | "your investments don't need to."     | blurIn dur1.0 blur22 sweep · blurOut 3.0    | piano D5@1.5 |
| 3.00  | 4.30  | rise  | bgLight    | bg     | cream void                            | opacity 0→1 1.3s IO                         | impact@3.0   |
| 3.20  | 6.20  | rise  | laptop.rig | device | hero screen = REF1 crop               | y 900→110 3.0s power3.out, rotY −40→−9      |              |
| 10.95 | 15.5  | apply | L1         | card   | step card 01 (rebuilt, exact copy)    | MK.lift z230 x−150 y−40 rotY−10             | shimmer@10.95|
| 15.00 | 16.00 | whip  | fx         | trans  | gold/violet streaks                   | MK.whip stage=#stage                        | whoosh@15.0  |
| …     |       |       |            |        |                                       |                                             |              |
```

Also list at the end: **assets to prepare** (crop/unwarp/key commands), **fonts**, **tokens**,
**cue sheet** summary (mood, bpm, chord changes with times).

### 9.3 Storyboard proposal (what the user reviews)

Present the plan as a proposal, not a listing:

> This film tells **NRIs abroad** that **they can invest in India's private markets from anywhere**.

| # | beat · time | on screen | why (traced to the message) |
|---|---|---|---|
| 01 | hook · 0–3 s | "you moved to the US." → "your investments don't need to." on black | names the tension in the viewer's words |
| 02 | reveal · 3–7 s | laptop rises into cream studio, hero page glowing | the promise arrives as an object |
| … | | | |

Footer: rhythm line · palette · type · duration · audio. Then ask (collaborative) *"approve, or
which frames change?"* — revise only the frames named. Autonomous: post it and continue.

**Sketch sheet (optional, recommended for > 4 scenes):** after ENGINE builds the static layout
(ENGINE §3 step 4), run `render.mjs --at scenes` and show `contact-sheet.png` as the storyboard:
real fonts, colours, copy and placement, no motion yet. A confirmed sheet locks the layout; the
build dresses it and must not redraw it. If the user wanted only a storyboard, stop here.

### 9.4 Hand-off summary
Before building, one message: the locked brief in brief form, with **what the user stated** and
**what you inferred or defaulted** as two separate lists (with reasons). Corrections to it are not
approval — fold them in and show it again.

---

## 10. Brief quality gate (all must be YES)

- [ ] Beats sum to the duration; timecodes are continuous; no scene has two hero moves peaking together.
- [ ] Every caption passes the reading-time math (§4.3) including reveal and exit.
- [ ] Every on-screen string is either user-given, from a reference (verbatim), or approved. No invented numbers.
- [ ] Brand spelled exactly; logo preserved; refs mapped by content.
- [ ] Every effect maps to a kit function or recipe, or is marked CUSTOM with a precise description.
- [ ] Text never overlays busy content without a scrim/blur plan.
- [ ] Palette ≤ 7 tokens, one accent per scene; motion personality is single and consistent.
- [ ] Finish-by time and end hold are stated; audio ending lands on the logo.
- [ ] Constraints list includes the user's must-nots verbatim.
- [ ] If VO: every phrase has a film time; total fits (or the chosen fix is stated).
- [ ] Message sentence written; every beat's "why" traces to it; value lands by beat 2.
- [ ] Every beat has concept · depth layers · a verb per element · transition out + SFX; rhythm declared.
- [ ] Enrichment added (atmosphere, ambient motion, object-level transitions) and no new copy/claims.
- [ ] Reference videos: Shot Log + Style DNA written; only grammar borrowed, no content copied.
- [ ] **Integration check:** read all decisions together for a consequence no single one shows
      (9:16 + a dense dashboard = unreadable on a phone; 15 s + 6 beats = noise; a light palette +
      thin serif at 40 px = low contrast) and fix it now.

---

## 11. Writing prompts for other tools (when asked "give me the prompt")

Sometimes the user wants a prompt for an AI video model (Veo, Kling, Sora, Runway, Hailuo) or an
image model, not a coded film. Start from the same Production Brief, then adapt:

- **AI video generators:** split into shots of ≤ 8–10 s. One prompt per shot: subject, action,
  camera move, lens/framing, lighting, palette, mood, duration. On-screen text is unreliable in
  these models → keep text out of the shot prompt and add it in post (our engine can overlay it).
  Carry a shared "LOCK" paragraph (product look, palette, lighting) at the top of every shot.
- **Image models (keyframes):** one still per beat; describe composition, materials, light, colour
  hex, aspect ratio; no motion words.
- **Our engine (default):** the full Production Brief + Build Sheet above.

Always tell the user which target the prompt is written for.

---

## 12. Worked examples

### 12.1 From a full brief (path A + C): AASTHI, 30 s → 36.5 s with VO
Input: long timecoded prompt + 4 refs (hero page, trust grid, how-it-works page, logo) + later a VO.
Decisions that made it work:
- Refs were labelled wrong by the user → mapped by content.
- Hero page (frontal) → cropped screen texture. How-it-works and trust pages (angled) → rebuilt in
  HTML with verbatim copy so cards could lift crisply.
- Dashboard had no reference → built "in the hero's visual language" with skeleton bars and a gold
  line that draws on, no numbers (regulated product).
- Push-in over the hero page put the new headline over the page's own headline → blurred the page
  except the A-frame photo (radial mask) and darkened the studio.
- VO (36.2 s) exceeded 30 s → placed each phrase on its caption, sped VO 1.08×, split the dashboard
  headline into three lines revealed with the words, extended the ending to 36.5 s.
See `examples/aasthi/` for the finished film code.

### 12.2 From a one-line concept (path B)
"30-second launch film for Brewly, a coffee subscription app. Warm, playful."
→ Product Truth: Brewly · coffee beans delivered on your schedule · 25–40 urban · promise "fresh
coffee, on your schedule." · proofs: roasted this week · skip anytime · delivered free.
→ Format 9:16? No platform given → 16:9 default.
→ Personality: Playful + warm palette (#2B1B14 espresso, #F3E6D3 crema, #D9822B caramel accent),
  Fraunces 600 headlines + Plus Jakarta Sans captions.
→ Arc: Hook "monday. no coffee." (dark, 0–3) → phone rises with the app, cup icon pops (3–7) →
  "fresh coffee, on your schedule." (7–10) → three benefit cards pop out of the phone with plucks
  (10–19) → wobble-free trust line "skip anytime." (19–23) → blob wipe to crema → logo + "brew it
  forward." + "get brewly" (23–30, reveals done by 28.5).
Then the full Production Brief (§9.1) and Build Sheet (§9.2).

### 12.3 From a reference video (path E + C)
"Make the launch of Kosh (our budgeting app) feel like this reference" + app screenshots + logo.
→ `analyze_video.py ref.mp4` → 14 shots, avg 2.1 s, cuts on beat 71 %, ~118 bpm, white void,
  black type, one device per shot, hard cuts + 2 zoom-throughs.
→ Style DNA: kinetic modern on a white void; hard cuts on the beat; huge centred sans; one device
  per shot rotating in; a single colour accent per shot.
→ Transfer: keep 14-beat structure scaled to 30 s (≈ 2.1 s beats), cut on the synth's beat grid
  (bpm 118), white void + the app's own accent (#2F6BFF) instead of theirs, Manrope 800 instead of
  their typeface, our phone rig with the user's screenshots. Nothing of theirs appears on screen.
→ Brief states "structure and rhythm borrowed from the reference; all content is Kosh's".

### 12.4 How a model should read these examples
Copy the *decisions pattern*, not the words: every choice has a reason tied to the product truth,
the message sentence or a reference's Style DNA. When you finish a brief, you should be able to
point at any frame and say which of those three it came from.
