---
name: doodle-explainer
description: "Produce MS-Paint deadpan doodle explainer videos (Primate Economics / Capybara Economics style) end-to-end: zero-credit Google Flow sprite/scene generation, reverse-alpha Gemini corner-watermark removal, vtracer SVG vectorization, rapid-cut HyperFrames pacing (~1.7–2.5s/cut), and @capybluh-style silence-punchline BGM/SFX mixing. Use when creating or re-editing meme-animal or MS-Paint doodle explainers, viral cartoon economics/science videos, or porting Flow images into rapid-cut SVG videos. For general motion graphics use motion-graphics; for audio-only sound design use sound-effects."
---

# Doodle Explainer

Build deadpan MS-Paint doodle explainers (stark `#FFFFFF` canvas, thick wobbly black outlines, flat paint-bucket fills, zero shading/3D) that hold YouTube retention through **rapid visual cut density (~1.7–2.5s/cut)**, **@capybluh silence-punchline sound design**, and **$0 Google Flow → watermark-free SVG** asset production.

## Core Pipeline

1. **Research & Character Lock**
   - Check competitor saturation before picking a meme mascot (e.g., Gorilla, Penguin, Raccoon are already taken in finance explainers; pick an open animal with a boxy MS-Paint-friendly silhouette and one built-in visual gag prop).
   - Write the spoken script for the ear (short punchy sentences, character dialogue turns, explicit comedic pauses). Never include sponsor filler unless requested.
   - For Vietnamese episodes, spell numbers in spoken words for TTS, use native Vietnamese fonts (`Shantell Sans` 800 for hand-drawn stamps + `Be Vietnam Pro` 700/800 for dialogue — never `Permanent Marker`, which lacks Vietnamese diacritics), and follow the repo's `.okf/` voice decision (e.g., Vibi `eleven_v4` with distinct library voices per character role).

2. **Generate Multi-Frame Assets at `$0` in Google Flow**
   - Use `browser-skill` (`bsk`) in the user's logged-in Chrome profile (`Image`, `16:9`, `x2`, `Nano Banana Pro` = `0 credits`).
   - Lock every prompt with the exact style header:
     `Pure stark #FFFFFF white background, 2D MS-Paint mouse-drawn doodle style, thick wobbly black outlines, flat solid paint-bucket fills, zero shading, zero gradients, zero 3D, zero text labels, ...`
   - Plan **~55–65 unique SVGs** for a 5-minute episode by batching 2–4 well-separated items per Flow generation:
     - **Anchor + pose/expression sheet** (neutral, talking mouth-open, chin-rub thinking, smug, shocked, mic host)
     - **Costumed cast** (rich, banker, cop, parents, auctioneer, rapper, lawyer, taxman, grim reaper)
     - **Tight bust close-ups** for shot-reverse-shot dialogue (talking, thinking, stern banker, laughing rich, shouting auctioneer, raising-paddle bidder, tight mic rapper)
     - **Dedicated micro-gags & environments** (crowd sea, interior rooms, locked door, giant comparison mountains, credit gauges, bespoke rap/list gags)
   - Stop the `bsk` session as soon as all images are downloaded.

3. **Scrub Gemini Watermarks & Vectorize to Transparent SVGs**
   - Every `1376×768` Nano Banana Pro image carries a semi-transparent 4-point Gemini star in the bottom-right corner (`x=1222..1272, y=614..664`, `max_alpha ≈ 0.3125`). Painting white over it ruins dark shoes, fur, or colored panels.
   - Run the bundled cleaner/vectorizer script (uses Python 3.12 because `vtracer` segfaults on Python 3.15):
     ```bash
     uv run --python 3.12 --with vtracer --with pillow --with numpy \
       python scripts/clean_vectorize.py <input-image> <output.svg> \
       --alpha assets/gemini_star_alpha.npy [--crop x0,y0,x1,y1] [--keep-bg]
     ```
   - The script mathematically inverts `I_orig = (I_obs - α·255) / (1 - α)` to restore exact underlying pixels across outlines and flat fills, flood-fills outer `#FFFFFF` to transparent (preserving interior whites like eyes, shirts, and paddles), and vectorizes via `vtracer`.
   - Rasterize contact sheets with `rsvg-convert` (not ImageMagick `magick`, which aborts on macOS SVGs) and inspect every crop and bottom-right corner visually before composing.

4. **Build Master Audio (`@capybluh` Contrast Mix)**
   - Generate all VO lines first (caching WAVs per line ID), trim dead silence gently (`-45 dB`), and auto-detect quiet clause pauses inside multi-beat sentences so visual cuts land cleanly mid-sentence.
   - Analyze every BGM track with `librosa` + `<120 Hz` low-pass kick detection; shift the BGM offset so visual cuts land on real kick drums (save `beatgrid*.png`).
   - Apply `@capybluh` contrast rules (details in [references/pacing-and-sound.md](references/pacing-and-sound.md)):
     - Keep BGM `-14` to `-17 dB` under narration, ducking slightly more under active VO.
     - **Hard-cut BGM to `0.0` silence** (`25ms` ramp) on every deadpan punchline or shock reveal so dry voice + 1 crisp CC0 SFX hits with maximum contrast.
     - **Swap BGM grooves on structural pivots** (e.g., upbeat pop groove for story → silence break → 97 BPM hip-hop beat for a rap/list montage → hard stop on punchline).
     - Use real CC0 SFX only (never synthesized beeps) — one purposeful sound per visual intent, normalized and mastered to `-16 LUFS` (`±0.5 LU`) with true peak `<= -4.0 dBFS` on both stereo and mono fold-down.

5. **Compose Rapid-Cut HyperFrames Video**
   - Generate `index.html` programmatically from `timeline.json` so every `<section data-start data-duration>` and GSAP cue is mathematically locked to the audio master.
   - Enforce the pacing, voice-to-cut, and motion rules in [references/pacing-and-sound.md](references/pacing-and-sound.md):
     - Target **`1.7 – 2.5s` average visual cut pace** (`~24–34 cuts/min`). Never hold any layout unchanged longer than `3.5 – 4.0s`.
     - Every character voice switch triggers an instant hard cut (`±30ms`) to that speaker's close-up or pose.
     - Never hold one static split-screen template across a montage or auction; alternate tight performer close-ups with full-screen gag illustrations every `1.5 – 2.0s`.
     - Never mix inline CSS `transform` with GSAP `x`/`y`/`scale` tweens on the same element — put initial `scale`/`x`/`y` inside `tl.fromTo(...)` so `hyperframes lint` passes with `0` errors.
     - For localized building/prop signs baked into SVGs (`BANK` → `NGÂN HÀNG`, `SOLD` → `ĐÃ BÁN`), wrap the `<img>` in a `.sprite-wrap` container and overlay a color-sampled flat patch (trapezoid `clip-path` inside diagonal roofs) using the embedded display webfont so the sign moves glued to the prop.

## Verification Gates (Required Before Delivery)

- **Composition checks:** `npx hyperframes lint` (`0` errors) and `npx hyperframes validate` (`0` console errors).
- **Cut-density check:** Measure real visual cuts on the exported MP4:
  ```bash
  ffmpeg -i out.mp4 -vf "select='gt(scene,0.08)',showinfo" -f null - 2>&1 | grep -c "pts_time:"
  ```
  Confirm pace is `>= 22 cuts/min` (for a 5-minute video, `>= 110` cuts). If under target, break up the longest holds into close-ups and micro-gags before delivering.
- **Visual & watermark audit:** Extract `10–12` frames across all acts into contact sheets, inspect with your eyes for text overlaps, diacritics, sign seams, and bottom-right corner cleanliness.
- **Audio audit:** Measure stereo and mono `ffmpeg -filter_complex ebur128=peak=true` on the exported MP4 (`~ -16 LUFS`, true peak `< -4 dBFS`), listen to key dialogue/beat-drop/silence excerpts, write `CREDITS.txt`, and report **5 headphone-check timestamps** (never claim "it sounds good").
- **Hygiene:** Confirm zero stray `chrome-headless`/`ffmpeg` render processes and zero open `bsk` sessions.

## Reference & Bundled Assets

- [references/pacing-and-sound.md](references/pacing-and-sound.md): Exact cut-cadence table by emotion, voice-to-frame mapping, `@capybluh` silence/SFX rules, and smart MS-Paint motion physics.
- `scripts/clean_vectorize.py`: Run via `uv run --python 3.12` to invert Gemini corner watermarks, flood-fill outer white, and vectorize to SVG.
- `assets/gemini_star_alpha.npy`: Calibrated `1376×768` Nano Banana Pro 4-point Gemini star alpha map.
