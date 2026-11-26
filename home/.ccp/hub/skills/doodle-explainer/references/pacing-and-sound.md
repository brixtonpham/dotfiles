# Pacing, Voice-to-Frame, Sound & Motion Rulebook

Derived from empirical teardown of *Primate Economics* (`iWrLYpTv6GU`, `247` cuts in `7m10s` ≈ `34 cuts/min`) and `@capybluh` Shorts (`1.1M–3.6M` views).

## 1. Visual Cut Cadence by Emotional / Narrative State

| Beat Type | Target Cut Cadence | Visual Beats per Sentence | Rationale |
|---|---|---|---|
| **Explanatory setup** (`4–6s` sentence) | `1.8 – 2.5s` / cut | 2–3 shots (split on comma: *Premise → Metaphor / Math*) | Prevents slide-deck fatigue while keeping comprehension crisp |
| **Dialogue / Comedy exchange** (2+ voices) | `0.8 – 1.8s` / cut | 1 hard cut per speaker turn (*Wide → Tight A → Tight B → Reaction*) | Eye naturally tracks speaker switches; matches sitcom rhythm |
| **Montage / List / Rap** (8+ rapid items) | `1.5 – 2.1s` / cut | 2 beats per item (*Tight Performer ↔ Full-Screen Gag*) | Resets visual attention every bar instead of stale split-screen templates |
| **Deadpan punchline / Shock** | `1.8 – 2.8s` hold | 1 abrupt impact cut + brief hold (`~0.5s` breathing room after line) | Cutting too fast over a punchline kills the laugh |
| **Hard ceiling (any shot)** | Never `> 3.5 – 4.0s` static | Insert pose swap, zoom punch, or prop reveal before `3.5s` | Eliminates dead spots across 3–6 min runtimes |

## 2. Voice Delivery → Visual Pairing

- **Voice switch = mandatory hard cut (`±30ms`):** When another character speaks, cut straight to their close-up or talking pose on the exact voice entrance. Never let a new character's voice play over the previous wide framing.
- **Rising energy / faster WPM** (auction bidding war, rap bars) → compress cut durations to `1.0 – 1.5s`, add crowd inserts and micro camera shake.
- **Pitch drop / deadpan pause** (*"Your card was declined"*, *"Lời thề... tử thần."*) → cut to a minimal stark frame with high negative space and one focal subject.
- **Mid-sentence twists:** Auto-detect the quietest `80ms` RMS trough near the clause boundary inside the VO WAV so the hard cut lands on the exact spoken breath.

## 3. `@capybluh` BGM & SFX Architecture

- **Contrast beats volume:** Keep BGM `-14` to `-17 dB` below VO (`-31.5 dBFS` RMS vs `-17.5 dBFS` VO RMS), ducked to `0.65x` during speech (`0.78x` during rap bars).
- **Hard-silence punchline dropouts:** Ramp BGM to `0.0` over `25ms` right before a deadpan punchline or shock hit, hold pure silence through the punchline + `0.5s` reaction beat, then ramp back in over `25ms` on the next scene cut.
- **Structural BGM pivots:** Use one light bouncy groove (e.g., `120 BPM` funk/pop) for explanations, cut to dead silence before a special sequence (rap/montage), drop a distinct beat (e.g., `97 BPM` boom-bap hip-hop), and hard-stop on the punchline.
- **Kick-aligned cuts:** Low-pass BGM `< 120 Hz` (`4th`-order Butterworth) and measure median offset from `librosa` beats to actual bass-kick peaks; shift BGM start by that offset when `|offset| > 25ms`.
- **One real CC0 SFX per visual intent:**
  - Hard scene cut → fast whoosh / chop (`-4` to `-5 dB`)
  - Sprite pop-in / pose swap → mouth-pop / plop / kit pop (`-3` to `-5 dB`)
  - Card decline / credit glitch → interface glitch buzz (`-1.5 dB`)
  - Shock / gavel / stamp slam → heavy punch or dramatic hit (`-1` to `-2.5 dB`)
  - Approval / house payoff → soft bell ding (`-4` to `-6 dB`)
- **Loudness target on final exported MP4:** Stereo and mono fold-down `~ -16.0 LUFS` (`±0.5 LU`), True Peak `<= -4.0 dBFS` (also satisfies YouTube `-14 ± 2 LUFS` / `<= -1 dBTP`).

## 4. Smart On-Screen Motion (Expressive, Not Floaty)

- **Snappy pop-in + crisp hold:** `140–220ms` `back.out(1.7–2.0)` entrance from `scale: 0.85, y: 30` so sprites land like physical stickers, then hold deadpan stillness so expressions read clearly. Avoid slow continuous floating/bobbing.
- **BPM-locked 2-frame stepped motion:** Use `ease: "steps(2)"` at exact half-beat duration (`30 / BPM` seconds, e.g., `0.309s` for `97 BPM`) for rhythmic head-bobs, clock ticks, and talking bounces.
- **Physics matched to the gag:**
  - Camera shake (`x: ±16px, 0.04s, repeat: 6, yoyo: true`) exclusively on gavel slams, crashes, and shock hits.
  - Vertical up-down bounce exclusively for literal up-down metaphors (elevator / adjustable rate).
  - Instant `0.01s` opacity swaps for deadpan expression flips (neutral → smug).
  - Slow ominous zoom (`scale: 1.0 → 1.13`) only on dread/shock holds.

## 5. Vietnamese Localization Standards

- **Fonts:** Use Google Fonts with verified `/* vietnamese */` unicode subsets — **`Shantell Sans`** (`wght@700;800`) for chunky hand-drawn marker titles/stamps and **`Be Vietnam Pro`** (`wght@600;700;800`) for dialogue and labels.
- **Sign localization:** Never leave baked-in English signs (`BANK`, `LOANS`, `SOLD`) inside animated props. Wrap the `<img>` in a positioned `.sprite-wrap` container, sample the exact flat RGB hex of the sign interior, and place a matching flat patch (with trapezoid `clip-path` when inside a triangular roof pediment) carrying the Vietnamese text in `Shantell Sans`.
