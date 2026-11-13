# Abik's Reel Editing System — style name: **"Normal UGC 1"** (approved Reel 3 v6 / Reel 4)

When Abik says "Normal UGC 1" with an A-roll + script, build exactly this system (§1–17; plan template `Fanout Reel 4 plan.json`). Learned from "AI UGC 1"

Source of truth: `/Users/abiknewar/Work/Fanout/AI UGC/Project FIle/Copied_AI UGC 1/AI UGC 1.prproj`
(Premiere Pro 26.5, sequence "Sequence 02_12", 1080x1920, 24 fps, 23.125 s) and the render
`/Users/abiknewar/Work/Fanout/AI UGC/AI  UGC 1 d3.mp4`.

Parsed with `tools/parse_prproj.py` (gunzip the .prproj first). Frame sheets in `reference/`.

---

## 1. Track stack (bottom → top)

| Track | Name (as in project) | Role |
|---|---|---|
| V1 | Aroll | Base talking-head, jump-cut, slight punch (scale 119–163) |
| V2 | Color mate Background | Colour matte `#f5f5f5` from the first layout cut (2.667 s) to the very end |
| V3 | Screen Recording 1 | Product screen recordings / screenshots, top ~55 % of frame |
| V4 | Screen Recording 2 | Second screenshot when two are stacked |
| V5 | Broll 1 | Movie/TV b-roll, full frame |
| V6 | Broll 2 | Second b-roll stacked on top of Broll 1 |
| V7 | Aroll Cutout | AI object-masked talking head (background removed), placed at the bottom over layouts |
| V8 | Aroll Full Screen | Full-frame punch-ins of the A-roll (scale 141–157) for title moments |
| V9 | Logos | Brand logos popping in over the screen recording |
| V10–V12 | Text Graphics 1 / 2 / 3 | One track per title line (line 1 / line 2 / line 3) |
| V13 | Adjustment effects Grains & Fades | Adjustment layer: Lumetri Faded Film 28 + Noise 5 % |
| V14 | Outro Animation | `fanout-loader-alpha-prores4444.mov`, scale 48, centred, on the white matte |
| Captions | Subtitle 1 | Word-by-word captions (green pill), auto-transcribed then split |
| A1 | Aroll Sound | Dialogue, Essential Sound = Dialogue (Repair: noise 7.1, rumble 60; Clarity level 3) |
| A2–A6 | SFX 1–5 | Clicks / whooshes / tings, tagged SFX, stacked so hits can overlap |
| A7 | Background music | `ES_Electronica the Witch` starting at source 14.875 s, full length, tagged Music |

Clip volumes are all left at 0 dB (no volume keyframes); balance comes from Essential Sound tags.

---

## 2. Section grammar (what the reel alternates between)

Every 1.3–3.8 s the layout changes. Every layout change is a HARD CUT landing on a click SFX.

**A. Hook (full-frame A-roll + 3-line title)** — 0.000–1.917 s
- V1 scale 119, position y 0.588 (slightly tight on the face).
- Title lines appear on the spoken word: "This feels like" (f0) → "cheating," (+17 f) → "but" (+31 f). All lines end together on the cut (f46).

**B. Punch-in jump cut** — 1.917–2.667 s
- Same A-roll, 0.29 s of source dropped, scale 163, y 0.698. Whoosh + triple-stacked button click SFX.
- Caption "it works." starts on the cut.

**C. Screen-recording layout** — 2.667–5.708, 7.000–13.875 s
- V2 white matte fills the frame. Screen recording on V3 at scale 68–75, position y 0.37–0.39 (occupies the top ~55 %).
- V7 cutout at scale 102, y 0.818 (head overlaps the bottom edge of the screen recording). Cutout is sometimes rotated and offset to one side: +18° at x 0.304 (left) for 7.0–10.8 s, −11° at x 0.610 (right) for 10.8–13.9 s, centred otherwise.
- Within this layout the "screen" content gets simple motion:
  - Two stacked screenshots slide up and settle: y 0.510→0.447 and y 0.198→0.142 over 27 f, eased (Bezier) — 4.375–5.708 s.
  - Logo pops over the recording (V9): scale 0→18 in 3 f (Netflix), 0→33 in 2 f (Uber), 0→26 in 9 f (Google), eased; each pop has a "ting" + click SFX. Logos sit at y ≈ 0.28.
  - Page scroll: screenshot at scale 165, y 0.791→0.170 LINEAR over 50 f (longer than the 43 f clip, so it never settles) — 10.792–12.583 s.
  - Slow push-in: scale 56→74 over 24 f, eased — 12.583–13.875 s.
- Captions (green pill) sit at y ≈ 0.385, between the recording and the cutout head.

**D. Full-screen A-roll + title** — 5.708–7.000, 13.875–17.083, 19.250–21.042 s
- V8 punch-in scale 141–157, y 0.61–0.69. 3-line title block over the chest (block centre y ≈ 0.63–0.67).
- When the title ends before the cut (15.917 s), captions take over for the remaining words.
- Captions here sit lower, y ≈ 0.70.

**E. B-roll + cutout + title** — 17.083–19.250 s
- Broll 1 full-frame (scale 180, x 0.332), Broll 2 cut in on top at 18.167 s (scale 370). V7 cutout centred at bottom. Two consecutive 3-line / 2-line titles. UI-click SFX on each b-roll cut.

**F. Outro** — 21.042–23.125 s
- Dialogue ends, white matte + fanout loader animation (scale 48). Music runs to the end.

---

## 3. Title system (Essential Graphics, V10–V12)

- One Graphic clip per line, one track per line. Lines stagger in on the spoken word; the typical stagger is 6–17 frames between lines, and all lines end together on the next cut.
- Fonts: **Instrument Serif Italic** (white, ~110 px) for lead/tail lines; **SF Pro Semibold / Medium / Bold** (white, ~130–140 px) for the keyword line, which has a rose box behind it (rendered `#a05450` after the Faded Film grade; ~155 px tall, ~20 px padding, 8–24 px corner radius).
- Layout: lead line left of centre, keyword centred, tail line right of centre (a stepped, hand-placed look). Positions were set per clip via Vector Motion, e.g. (0.447, 0.505) / (0.5, 0.568) / (0.670, 0.630).
- Scale 100, no stroke, no shadow visible.

### In animation (identical on every one of the 14 titles) — "Text Animator" on the text layer
```
Type = In         Preset = Custom (0)        Start 0 → End 100
Ease In  = 0      Ease Out = 80
Fade     = 75     Push Position = (0, +0.0495)  → text starts ~95 px lower and pushes UP
Zoom     = 0      Spin = 0      Distribution = 32   Word Bias 5   Line Bias 51
Motion Blur ON = 35
```
Measured on the render: fully visible after ~10–11 frames (≈0.45 s): frame 1 is ~25 % opacity and ~95 px low, opacity and position ease out, last 3 frames barely move.

### Out animation
**None.** Every title clip is cut hard on the A-roll edit. The exit is the picture cut itself. Do not add fades.

---

## 4. Caption system (caption track "Subtitle 1")

- Transcribe (Speech to Text), then split captions to 1–2 words each (4–20 frames, median ≈ 11 f / 0.45 s). 28 captions in 23 s.
- Style: Instrument Serif Italic ~70 px white on a dark-green pill `#183020` (rendered), ~90–105 px tall, ~20 px side padding, ~12 px radius, centred horizontally.
- Vertical position: y ≈ 0.385 in screen-recording layouts, y ≈ 0.70 in full-frame sections (moved per section).
- No in/out animation: hard pop on, hard pop off, boundaries aligned to the picture cuts.
- Captions are NOT shown while a title block is on screen; they fill the gaps between title moments.

Full caption list with timing is in `reference/timeline_dump.txt` (section "Subtitle 1" from the parser run) and in the memory notes.

---

## 5. Cutout (V7)

- Same A-roll clip, AI object mask (Premiere "Mask2" with tracker; mask data lives in `AI UGC 1 Masks/*.prmf`), feather 0, expansion 0, Opacity blend mode left at default.
- Scale 102, y 0.818 — the head overlaps the screen recording's bottom edge, shoulders bleed off the bottom of frame.
- Five separate cutout clips, one per layout section, so each can have its own rotation/offset.

---

## 6. Sound design rules

- Every picture cut gets a click: `ES_Mechanical, Click, Buttons, Switches…` (0.37–0.88 s pieces) or `ES_User Interface, Click, On & Off, Small, Short 02` (0.17–0.25 s) for b-roll cuts.
- The punch-in gets a whoosh (`Transition_Woosh.mp3` + `ES_Swooshes, Whoosh, Airy, Light 03`) plus the miniature-button click stacked 3× at 120 % speed.
- Each logo pop gets `ES_User Interface, Misc, Pings, Tings` (0.625 s).
- SFX start 2–12 frames BEFORE the cut they belong to (e.g. whoosh at 1.542 for the 1.917 cut; click 2.625 for 2.667; click 12.458 for 12.583).
- Music: one Epidemic track for the whole reel, trimmed to start mid-song (14.875 s in), untouched volume, Essential Sound Music tag.
- Dialogue: Essential Sound Dialogue preset with Repair (Reduce Noise ≈7, Reduce Rumble 60) and Clarity (Enhance Speech 3).

---

## 7. Grade

- Adjustment layer over 0–21.042 s only (not the outro): Lumetri Creative → Faded Film 28, Noise 5 % (colour noise off / default).
- No grade on the A-roll clips themselves (the A-roll source is a pre-rendered sequence export).

---

## 8. Assets to collect for a new reel

1. Raw A-roll (talking head, vertical) + the platform link for screen recordings.
2. Screen recordings (`.mov`, ~16:10 browser) and screenshots of the key pages (hero, curriculum list, lesson page).
3. Logos as PNG/WebP (transparent) for the "companies" beat.
4. Optional movie/TV b-roll clips (1–2 s).
5. Epidemic SFX set listed above, one music track, `fanout-loader-alpha-prores4444.mov` outro.

## 9. Reproduction plan (next session)

1. Jump-cut the raw A-roll (remove pauses, keep one 0.29 s punch-in jump near the hook).
2. Transcribe → word-level timings → decide title moments (3 per full-screen section) vs caption words.
3. Build the sequence by cloning this project's XML: duplicate the existing Graphic / caption / Motion blocks, rewrite Start/End/InPoint/OutPoint ticks (254016000000 ticks = 1 s; keyframe times carry a +3600 s offset) and media paths. Text strings live in FlatBuffer blobs (`Source Text` / `FormattedTextData`), so each new title/caption must be re-encoded or copied from an existing clip with the same style.
4. Re-link the AI object mask in Premiere (mask tracking cannot be generated outside Premiere) — the cutout clips need a one-time "Object mask → track" pass after opening the generated project.

---

## 10. Facts learned while building "Fanout Reel 2" (2026-10-24)

- **Title in-animation lives in a `VideoTransitionTrackItem`** (MatchName `AE.AE_Impact_Text_Animator`) listed in the track's `TransitionItems`, aligned to the clip head. Length is hand-trimmed: 18 f (0.75 s default) on titles ≥ ~40 f long, 8–12 f on 20–30 f titles, 4 f on a 6 f title. There are 28 animator components because each title has a source copy and an instance copy; there is no out-animator anywhere.
- **Exact title font sizes** (from the Source Text FlatBuffers): Instrument Serif Italic 85–87; SF Pro keyword boxes: "cheating," Semibold 121, "senior engineers" Medium 116, "random concepts" Semibold 106, "Systems" Bold 147, "they are?" Bold 127. Box padding value 28.
- **Caption blob (`FormattedTextData`)**: text is the last length-prefixed string; no run-length elsewhere, so text can be swapped by rewriting the tail and the size prefix (`len − 12`). Vertical placement is one float at byte 232: `-0.5521`/`-0.5594` = layout position (y≈0.385), `-0.2307` = low full-frame (y≈0.70); a shorter 432-byte variant with float `-0.338` at byte 220 = mid full-frame (y≈0.61). `BinaryHash` = 28 hex + 8-hex size; give edited blobs a fresh one.
- **Linked A/V clips** are `Link` objects (TrackItemGroup of the video + audio track item) listed under `Sequence/Links`.
- Premiere writes projects with zero unreachable objects, so a generated file should be pruned to the reachable set.
- Keyframe times = source time (stills/graphics use the 3600 s base, video uses real source ticks). Audio sample rate = 254016000000 / FrameRate ticks.
- macOS screen-recording filenames contain U+202F before "AM"; normalise when matching names.
- Generator: `tools/build_prproj.py` + a plan JSON (`Fanout Reel 2 plan.json` is the template). Preview compositor: `tools/render_preview.py`.
- Framing must adapt to the raw: with this raw (chin at y 0.42, eyes 0.28) the full-screen punch-in is scale 140 / y 0.57 and the cutout sits at y 0.88 so the head top lands at ≈0.49 like the original.

## 11. Corrections from Abik after the first build (2026-10-24) — apply every time

Workflow: **preview first, project file only after Abik confirms the preview.**

1. **Content must be decided from the script, not copied.** Read the transcript, split it into beats, and for each beat choose: full-frame title moment (the punchy claim: 2–3 lines, keyword gets the box), layout beat (product mention → screen capture of the matching fanout.sh page + caption words), b-roll beat (metaphor/joke), or plain caption beat. Pick site pages that literally show what is said (curriculum list for "learning paths", a lesson with a diagram for "interactive animations", company guides + logos for company names). The person/framing changes every time → run `tools/face_measure.py` first.
2. **Never cover the face.** Measure the face box per section (YuNet). Full-frame punch-in: scale/position so eyes ≈ 0.26 and chin ≈ 0.46 of the frame (tool prints it). The title block starts at the chin (first line centre ≈ chin + 0.02…0.05) and grows downward. Cutout layout: head top lands at ≈ 0.49 so the caption pill (y 0.385) sits just above the head. In the reference the title line sits exactly on the chin (face box bottom 0.584, line 0.562–0.593); same for us.
   - Title layout: Premiere renders these graphics at **0.92×** the nominal font width; horizontal anchor = text centre; vertical screen centre = Vector Motion position + per-exemplar offset (+0.096 for the "This feels like / Instead of" family, −0.27 for the "Why / Systems" family). Words on one line need a full space gap: compute widths with the real fonts × 0.92 and place centres accordingly, or make the line one graphic. Preview must use the same metrics so it is truthful.
3. **Mix.** Music clip Audio Gain **−30 dB** (reference value, music ends ~12 dB under dialogue) with a 7-frame constant-power fade at the tail. SFX gains: mechanical click −10 dB, UI click −15 dB, whoosh −15/−17 dB, stacked button click −25 dB, ting −10 dB. Dialogue 0 dB, Essential Sound Dialogue preset. The preview must apply the same gains.
4. **Outro must play out.** Loader clip = full 2.083 s (the logo completes at ~1.0 s and holds). Extract loader frames at the sequence frame rate (it is a 60 fps file); never end the sequence before the loader clip ends.

## 12. Reel 3 revisions (2026-10-24) — Abik's second round of corrections

- **Matte + cutout look everywhere** except the real b-roll beat: hook, title beats and CTA are the cutout on the white matte (no full-frame raw video). Titles then sit on the matte above the head (block y ≈ 0.17–0.32, head top ≈ 0.49); the punch-in is a scale bump on the cutout (153 → 185).
- **Captions must never sit on a screenshot.** Screens live in a zone y ≈ 0.03–0.34 (centre 0.185, ≤ 600 px tall, ≤ 1000 px wide: pre-crop each capture to a panel), the pill goes in the gap at y ≈ 0.415, head top at 0.49. Caption height is set by the float at byte 232 of the caption blob: v = (y − 0.385)/0.98 − 0.5521.
- **Do not recut a raw file that was already cut.** If the A-roll arrives pre-cut, keep source time = sequence time (one dialogue clip, one base clip).
- **B-roll for "senior engineer" lines:** engineer moments from movies/series (Silicon Valley desk 1145 s, Social Network typing 190.5 s and window equations 297 s in Abik's files; Mr Robot wanted — Abik supplies the file). Three cuts across the line with UI clicks.
- **Perfect cutout:** BiRefNet-portrait via transformers on MPS in fp16 (`tools/matte_birefnet.py`, ~0.7 s/frame, 427 frames in 5 min) — much cleaner than isnet/u2net (no hair halo). rembg's onnx birefnet on CPU/CoreML is unusable (35 s/frame, CoreML compile hangs).

## 13. Reel 3 round three (2026-10-24) — screens, titles, b-roll

- **Screen content = scrolling recordings of the real pages in a narrow portrait browser window** (reference recordings are 1526x1900 and 1350x1892, ~40–58 fps, no audio). Reproduce with `tools/make_scroll.py`: capture the page at 763 css px wide, 2x (`--window-size=763,5500 --force-device-scale-factor=2`, fresh profile, `--virtual-time-budget=2500` to dodge the coupon popup), then pan a 1526x1100 viewport with ease-in-out (0.2 s hold, 1.2–1.9 s move, 0.6 s tail) → ProRes 422. Place at scale 66, y 0.22 (fills the width, ends ≈ 0.41); pill at 0.445; cutout head top 0.49.
- **Title stacks are tight and staggered**, measured on the reference: line pitch 0.063 of frame height, lead line left of centre (x ≈ 0.44–0.45), keyword box centred, tail line right (x ≈ 0.56–0.67). Block starts under the chin on full-frame beats (first line centre ≈ chin + 0.04).
- **B-roll beats are full screen with no cutout** (Abik's call for Reel 3): titles stacked over the footage. Picks: Silicon Valley 582.5 s (engineer at monitors), Social Network 93 s (typing), 298 s (equations on the window).
- Full-frame A-roll for hook / title / CTA beats, matte + cutout only behind the product recordings.

## 14. Deliverable = Final Cut Pro 7 XML (confirmed 2026-10-24)

Abik imports an XML, not a .prproj. `tools/export_fcp7xml.py plan.json out.xml` writes the sequence in Premiere's own FCP-XML dialect (xmeml v4, uuid, masterclipid, pproTicks, alphatype, stereo audio as linked channel pairs, logging/colour/labels). Package: one folder with the XML, the captions .srt and every media file flat beside it. A generic xmeml v5 file imports as nothing — keep the Premiere dialect. Not carried by XML (re-apply in Premiere): Text Animator in-transitions, keyword box / caption pill styling, Essential Sound tags, adjustment-layer grade.

## 15. .prproj generation — what Premiere requires (confirmed opening, 2026-10-24)

1. Serialize exactly like Premiere: `<X/>` without a space, newlines inside text as `&#10;` (except the literal newline+tabs before a closing tag after base64 blocks), file ends with two newlines. `tools/build_prproj.py` round-trips the reference byte-for-byte.
2. Never leave an empty `<TrackItems>` container; never remove `ContentAndMetadataState` from a Media.
3. **Binary blocks (`BinaryHash`)**: each hash is defined once with data at its FIRST occurrence in file order; later occurrences are empty elements with the same hash. Hash = 24-hex key + 8-hex (blob length + 12). Premiere rejects (a) a reference whose definition was pruned, (b) a known hash reappearing on a cloned object. So: every hash inside a cloned object gets a fresh key (remapped consistently file-wide), definition-first order is enforced, dangling refs are re-materialised from the reference's blob table. Rewritten text blocks (titles/captions) get a fresh hash with size = len+12.
4. The hash key is not md5/sha/xxhash/murmur of the data — unknown, but Premiere does not verify it.

## 16. Screen sections, final method (2026-10-24, from the reference comparison)

- Record the REAL site with `tools/record_page.py` (Playwright, 763 css px × 950, 2x → 1526x1900, 24 fps, cursor overlay, hover states, banner/popup removed). `--mode scroll` for pages (constant ~50 px/frame, already moving at frame 0 via `--lead`), `--mode drag` to pull a slider on a Labs instrument (/labs/model-router-and-pareto-explorer) for "interactive" beats.
- Pages that literally match the words: homepage (hero → logos → paths), /system/company-guides (what the reference recorded for "breaks down how Netflix, Uber, Google…"), /ai/overview, /roadmap, /system/overview curriculum list.
- Placement = reference: scale 68 at y 0.372 (fills the width, top ~65 %), cutout at 0.837 overlapping the bottom, pill at 0.385 on the recording.
- Variety: never two identical moves in a row — recording → interaction recording → recording → two stacked screenshots sliding up (scale 70, y 0.215→0.175 and 0.585→0.545 over 27 f) → fast list scroll (scale 165, y 0.95→0.40).
- No jump cuts: no hard scale bumps mid-sentence (use a keyframed push, e.g. 158→174 over the phrase); change the cutout tilt at most every ~3 s and only on a layout cut; run the dialogue clip to the end of the file so the last word's tail is never cut.

## 17. Reel 4 notes (2026-10-24)

- **Cutout size follows the presenter.** Target: hair top ≈ 0.50–0.52 of the frame, head (hair top → chin) ≈ 0.30 of the frame, so the recording stays readable and the pill (0.385) never touches the face. Measure hair top, not just the YuNet face box (face box top + ~0.1 for a bun/updo). Reel 3 presenter: scale 153 at y 0.837; Reel 4 presenter (big head, chin at 0.61 raw): scale 120 at y 0.81. Full-frame title blocks sit just under the chin: 0.66 / 0.723 / 0.786 for a low chin.
- A 25 fps A-roll is converted to a 24 fps copy (`ffmpeg -r 24`, audio untouched) before matte and timing; frame counts come from the copy.
- Headless-Chrome captures can arrive dimmed by the coupon dialog; take stills from `record_page.py` (2-frame scroll at speed 0) instead. The recorder waits for `load` + 2.5 s, not network-idle (the site keeps a live connection open).
- Company names in the script → logo pops on the Logos track (Netflix/Uber assets from the reference) with tings, over the company-guides recording.

## 18. "Normal UGC 1 + study upgrades" (first built 2026-10-28 on the Reel 4 A-roll, preview only)

`tools/overlays.py` adds the devices from the UGC reference study as plan `overlays` (drawn by `render_preview.py` over the normal composite; no .prproj mapping yet):
`caption_kw` (bold SF Pro, white + one brand-orange keyword, black stroke, optional dark pill, y ≈ 0.70), `topcard` (white rounded headline card at y 0.13, navy uppercase, orange highlight span, slides in 8 f), `counter` (dark card, label + number counting up over 14 f, orange sub-line; site numbers: System design 200 lessons/18 modules, AI engineering 43/9, Inference 226/32, AI research 108/12), `stamp` (glowing green/red verdict pill, overshoot pop 6 f), `emoji` (Apple Color Emoji at 160 px, pop), `freeze` (blurred, darkened presenter frame + giant orange number, 12–14 f), `diagram` (navy grid, boxes + green arrows drawing in sequence), `split` (presenter bottom half + recording top half in rounded cards on dark grey), `flash` (white flash 6 f), `endcard` (light matte, loader logo, serif headline, orange pill button, mono URL, 2 s before the loader).
Plan template: `Fanout Reel 4 upgraded plan.json` (captions replaced by `caption_kw`, late title stacks replaced by topcard/stamp, total 780 f with the end card at 682–730 and the loader after).

## 19. REJECTED: §18 "study upgrades" cut (2026-10-28) — hard rules

Abik: "Looks slop, AI kind of edit." The generic devices (bold stroked captions, white top cards, glowing stamps, emoji badges, giant-number freezes, navy diagrams, flash, template end card) are OUT. Keep Normal UGC 1's own language only. Full never-do list: memory `hard-rules-no-slop` (also §11–§17 here). Any new graphic element needs Abik's OK before it appears in a preview.

## 20. Multi-clip A-rolls with hook variants (Reels 6 and 7, 2026-11-11)

Folders of generated clips (`hook A|B|C/clip_01_final.mp4`, `body/clip_NN_final.mp4`) are stitched untrimmed into one A-roll with the ffmpeg concat filter, matted once, and cut as one timeline item per clip with linked audio (handles kept). One project per hook in one `Copied_` folder. Every clip join needs a layout change. Generator: `tools/gen_reel67_plans.py`. Verify each clip's first and last frame against its source after stitching (the concat demuxer duplicated frame 0).

## 21. What Abik changed in his own edit of Reels 6 and 7 (2026-11-12)

Source: his `_1.prproj` files (Premiere 2027; copies in `reference/abik edits 2026-11-12/`) and his exports. These files round-trip byte-exact through `build_prproj.Project(path).save()`, so they can be edited directly or used as the reference project for new builds.

### Two title styles. Ask Abik which one before every video.

**A. Without background** (his Reel 7 edits; also Reel 6 hooks B and C)
- Key phrase: SF Pro **Bold**, white, no box. Size 110–154 (125.5 most common; 145 for "real systems", 153.8 for "goes blank.").
- Lead and tail lines: Instrument Serif **Regular**, white, 63–85 (67.6 most common).
- Key line centred (x 0.5). Lead line above it, usually left of centre (x 0.31–0.51), about 0.05–0.06 of frame height higher. Tail line below, right of centre (x up to 0.76).
- Exemplars in `Fanout Reel 7 - hook A_1.prproj`: key = Text Graphics 2 at 6.875 s ("goes blank."), lead = Text Graphics 1 at 6.125 s ("and your mind").

**B. With background** (his Reel 6 body and hook A)
- Key phrase: SF Pro Semibold or Medium, white, size about 90, on a **green** box (about `#1C7C08`). The reference reel's box was rose; he changed it to green.
- Lead lines: Instrument Serif **Italic**, white, 65 (85 on the CTA line).
- Compact: lead line sits directly above the box (about 0.05 higher), x 0.40–0.50.
- Exemplars in `Fanout Reel 6 - hook A_1.prproj`: key = Text Graphics 3 at 2.25 s ("the hard way."), lead = Text Graphics 1 at 0 s.

Both styles
- Under the chin on full-frame beats (Vector Motion y 0.44–0.56), above the head on b-roll beats (y 0.17–0.32).
- Lines often replace each other instead of stacking: lead line first, then a second serif line takes its place, then the key phrase lands.
- In-animation is unchanged: Impact Text Animator (per-letter fade and push up, Distribution 32), 6–18 frames. Out is a hard cut.
- Captions keep the green pill.

### B-roll
- Literal to the words, 2–3 shots per line, 14–24 frames each. Hooks get full-screen b-roll with no cutout and the title over it; each hook variant gets different footage. In the body b-roll sits behind the cutout; one line per video may go full-screen with no presenter.
- Each shot is reframed (scale 169–246, x shifted) so the subject sits beside the title.
- Never repeat a shot across videos. Library, shot catalogue, theme index and the used-shots ledger: `B-roll library/README.md`.

### Framing and pacing
- Hard punch-ins between phrases on full-frame beats: close presenter 114 → 173–214, far presenter 140 → 197–226, with the position nudged to keep the eyes in place. No zoom inside a phrase.
- He cuts lines that slow the video ("Page three. First equation. Laptop closed." was removed) and trims dead air between sentences.

## 22. Abik's manual edit of the "sauce for engineers" reel (2026-11-13) — the style to follow from here

Source: `reference/abik manual edit 2026-11-13/` (his `.prproj`, the `.aep` with six linked comps, the collect report, the five course-cover PNGs, `timeline_dump.txt`, contact sheets of every sixth frame). Export: `dataset/human_finals/Fanout_Reel_9_manual_edit_human_final.mp4` (web copy; original at `/Users/abiknewar/Work/Fanout/AI UGC manual edits/EXO/IliiUD5WCcn_Eb6udsbzeg.mp4`). Same A-roll and script as my Reel 9 build (§ Reel 9, `tools/gen_reel9_plan.py`), so the two can be compared beat for beat.

**Format.** 1080x1920, 23.976 fps (the A-roll's own rate, not 24), 999 frames = 41.67 s. Flat timeline: V1 A-roll and AE comps, V2 b-roll / recordings / colour mattes, V3–V12 one text word per track plus the presenter cut-outs. No adjustment layer, no grain, no grade in Premiere (the AE comps carry Add Grain).

**Pace.** Every pause is cut. The 41.9 s take becomes 16 A-roll pieces; speech runs 38.7 s. Dialogue is checkerboarded on A1/A2 with a few frames of overlap at each join. The voice keeps running under full-screen graphics (number cards, end card), so the presenter is off screen for those words.

**Presenter framing.** Head high in frame: Position y 0.33–0.41, eyes about one third down. Scale changes at almost every cut: 100→116 (push over the first 14 frames), 168, 146, 159, 139, 144, 130, 128, 166. Never two consecutive A-roll pieces at the same scale.

**Hook text: word by word, one yellow keyword.**
- Small words: SF Pro Semibold, white, about 68 px, tracking −49. Each word is its own graphic on its own track, cut in on the frame it is spoken; all words of the phrase cut out together.
- Keyword: SF Pro Bold, yellow `#FADE4E`, about 265 px (3.9x the small words, 60–70% of the frame width), tracking −49, Impact Text Animator in. It sits directly under the small line with almost no gap, small line overlapping its ascenders.
- One keyword per phrase: "I'm about to **reveal**", "some sauce for **engineers**", "become a **senior engineers**" (two lines, second line a little smaller).
- Placement: top of the frame above the head (y 0.13–0.27). It goes over the ceiling, the light and the exit sign without worry; yellow bold reads on anything.
- On the punch-in ("that's not out there") the words stack vertically, left of the face at shoulder height (x 0.21, y 0.62–0.75), one word per line.
- Over b-roll the same idea in SF Pro Medium: "a few" white, "senior / engineers" yellow, lower middle of the frame.

**Captions (all non-keyword lines).** SF Pro Medium, dark text on a peach pill `#EFB176`, rounded corners, 2–3 words per caption, about 50 px text / 75 px pill height. On full-frame presenter beats the pill sits on the chest (y ≈ 0.66), which solves the white T-shirt. Over a recording it sits just above the cut-out's head (y 0.43–0.51).

**Preview ring (hook, "this is all you need to know to actually become a senior engineer").** AE comp 01, 71 frames: the five fanout course covers arranged in a 3D ring (radius 700, covers at 35%, one turn per 12 s, camera zoom 1800 at distance 2200; `3D_Horizontal_Image_Ring.jsx`) rotating behind the presenter's head. The presenter is rotoscoped in AE (Object Matte & Refine Edge) so the covers pass behind him. SFX under it: a ratchet mechanism at 60% speed and a rotating-dials clock beat.

**Number cards (one per list item).** AE comps 02–06, full screen, each exactly as long as the spoken heading (33–60 frames):
- off-white background, a giant numeral filling the frame in a pale tint of the cover's colour;
- the course cover drops in from the left to upper centre (centre y ≈ 0.40);
- title under it in SF Pro Bold capitals, tight tracking, in a dark shade of the cover's colour: small lead line ("MATH BEHIND", "THE FAMOUS") then big words ("MACHINE / LEARNING", "AI RESEARCH / PAPERS"), each word arriving with its spoken word through a short lens-blur;
- voice continues underneath; hard cut back to the presenter for the explanation.
Covers: `covers/Group 1321316747…775.png` (System design, Mathematics for Machine learning, AI research, Inference engineering, AI engineering).

**Explanations.** Alternate presenter-with-pills and recording-with-cut-out. He kept four of my recordings (YouTube search, dev.to blogs, company guides, the Attention explainer) at scale 70.8 / 98 and added his own screen recording for AI engineering. Presenter cut-outs are Premiere masks on a duplicate A-roll clip (`AEMask2`, `.prmf` files), scale 81–105, bottom of frame, head top ≈ 0.53–0.59. Netflix and Uber logos as before, Uber now with Invert + Luma Key so only the wordmark shows.

**B-roll.** One shot only (Silicon Valley, 1048.2 s), full screen with no presenter, with a keyframed whip pan across it (Position x 0.83 → −0.01 in 28 frames, eased). He dropped my other seven shots: the number cards do that job.

**Ending.** "only on fanout": punch-in (166) and the fanout logo animation (loader at 200%, tinted white, scale 44) plays on his chest. Then a white colour matte with `{ curated }`, `{ mapped }`, `{ complete }` (SF Pro Semibold, dark, tracking −83), centred, one at a time for 17–19 frames each while he says them, then the loader on the same white for 72 frames.

**Sound.** Music "Every Living Breathing Moment" at −15 dB (starts at −10 dB and settles over the first 1.3 s). The same mechanical click on seven cuts into graphics or recordings, whoosh + button on the first punch-in, tings on the logos, ratchet + clock under the ring. Far fewer SFX than my builds.

**What I did differently in Reel 9, and what changes.**
| My Reel 9 | His edit | From now on |
|---|---|---|
| Kept the take whole, 43.6 s | Cut every pause, 41.7 s | Trim every pause; voice may run under graphics |
| Serif lead + bold white key, two-line stacks | Word-by-word small white + one huge yellow keyword | His hook text |
| Number and name as a title over the presenter | Full-screen number card with the course cover | Number cards for lists |
| Green serif pills only over recordings | Peach SF Pro pills on every non-keyword line | His pills, on the chest for presenter beats |
| Eight b-roll shots | One shot with a whip pan | B-roll only where a graphic does not do the job better |
| Face pushed low to free the ceiling for titles | Face high, text over the ceiling | Face high |
| Ended on the presenter | Logo on "fanout", bracket end card, loader | His ending |
| Music −30 dB | −15 dB | Ask; level depends on the track |

## 23. Building in the manual-edit look (Reels 10 to 14, 2026-11-13) — what held up

Working instructions are in `MANUAL_EDIT_LOOK_CONTEXT.md`; this section records the findings behind them.

**Preview.** `tools/manual_reel.py` renders a list of beats (`pres`, `rec`, `broll`, `card`, `end`, `loader`). Each beat names the A-roll frames whose sound plays under it, so pause cuts and voice-under-graphics come from the same list. `tools/manual_look.py` holds the tracked text, the keyword fit (up to 270 px, 75% of the width) and the cover ring (each cover makes one right-to-left pass). Plans: `tools/gen_reel10_hook.py`, `gen_sauce_hook.py`, `gen_reel12.py`, `gen_reel13.py`, `gen_reel14.py`.

**Framing per presenter.** Eyes at 0.36 of the frame at any scale: `pos_y = 0.36 + (0.5 − eyes_raw) × scale/100`. With eyes_raw 0.387 the frame only fills from scale 105 up. Hook text above the head needs the head lower: push to 112–114 with pos y 0.54–0.57 and keep the keyword baseline at 0.24–0.27; check the hair, not the forehead line the face detector reports.

**Text.** Raise the small word row when the keyword has ascenders (`tall=True`). A keyword block behind the head (ring beat) needs the frame at about 135 @ y 0.675. When the presenter holds something at chest height, put the pill under it and drop the logo-on-chest; bring the cover card in on "Fanout" instead.

**Recordings.** Pro lesson pages on fanout.sh show a paywall card with prices right under the intro; record the lesson's card on the course overview punched in (`rec_scale` 120) instead. Daily paper pages: 1.8 px per frame and stop before the paywall. The recorder removes purchase toasts ("bought", "started the monthly plan").

**Editable Premiere project.** `tools/build_manual_prproj.py` clones every item from Abik's manual project. Facts: his sequence is 23.9748 fps (10595108966 ticks per frame); tracks are unnamed and addressed by position; A-roll and cut-out go in as frame-for-frame 23.976 copies; his sequence's stale preview renders must be removed; text origins inside his graphics are small (0.25558, 0.12151), keyword (0.12048, 0.16250), b-roll words (0.125, 0.37135), and Vector Motion position = target − scale × (origin − 0.5); his caption blobs keep y as a float at byte 228 with the same mapping as the older family at byte 232 (y 0.385 → −0.5521, slope 1/0.98).

**After Effects.** Premiere's Dynamic Link identifies a comp by its item id inside the `.aep`: the linked media has `ImporterPrefs` = base64 of UTF-16LE `"%08x-0000-0000-0000-000000000000" % id` and Title `<comp name>/<file>.aep`. An `.aep` can only be written by After Effects, so `tools/gen_ae_script.py` writes an ExtendScript that Abik runs once; it builds the card comps, saves the `.aep` and writes the comp ids for the Premiere builder. Folder layout mirrors his collected folder: `(Footage)/`, `<project>Report.txt`.

**Not verified as of 2026-11-14:** neither the generated Premiere projects (Reels 13, 14) nor the AE scripts have been opened in the real apps.
