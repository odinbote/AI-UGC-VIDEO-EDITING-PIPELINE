---
name: normal-ugc-1
description: "Normal UGC 1" — Abik's house style for fanout.sh vertical UGC reels. Trigger: an A-roll + script + the words "Normal UGC 1". Preview first, then a Copied_ package (.prproj + FCP7 XML + media). Everything needed to reproduce the style from a fresh session.
version: 2026-10-25
---

# Normal UGC 1 — context file

Use this file as the single source of truth. It compresses `EDITING_SYSTEM.md` (§1–17), the approved reels, Abik's feedback across four rounds, the Premiere file-format rules, the tool set, and the UGC reference study.

## 0. Who / what / where

- **Client:** Abik Newar, Premiere Pro 26.5 editor, fanout.sh (AI-engineering learning platform). Machine: Apple Silicon Mac, Python 3.14, no ffmpeg on PATH (use `imageio_ffmpeg` binary or PyAV), MPS GPU, Chrome + Playwright.
- **Workspace:** `/Users/abiknewar/Work/Claude Editing 2/`
  - `EDITING_SYSTEM.md` (full spec), `UGC_REFERENCE_STUDY.md`, `UGC_reference_styles_board.png`
  - `tools/` — `parse_prproj.py`, `build_prproj.py`, `export_fcp7xml.py`, `render_preview.py`, `face_measure.py` (+ `face_detection_yunet_2023mar.onnx`), `matte_birefnet.py`, `record_page.py`, `make_scroll.py` (legacy)
  - `Fanout Reel 4 plan.json` — the plan template; `Fanout Reel 3/4/Copied_*` — delivered packages
  - `reference/` — parsed timeline dump + frame sheets of the reference reel
- **Reference project (must stay in place; every generated clip is cloned from it):** `/Users/abiknewar/Work/Fanout/AI UGC/Project FIle/Copied_AI UGC 1/AI UGC 1.prproj`; its render `/Users/abiknewar/Work/Fanout/AI UGC/AI  UGC 1 d3.mp4`.
- **Workflow contract:** A-roll + script arrive → deliver a **preview MP4 first** → Abik approves or sends a numbered change list → re-render → on approval deliver the package. Never build the final before approval.

## 1. The look (approved Reel 3 v6 / Reel 4)

Frame 1080x1920, 24 fps. Raw A-roll used **uncut to its last frame** (convert 25/30 fps sources to a 24 fps copy; audio untouched).

**Beat grammar** (sections change every ~1.5–3 s, always on a click SFX):
1. **Hook** — full-frame A-roll (scale ≈158 for 720p sources), 2–3-line title stack under the chin.
2. **Product phrases** — white matte `#f5f5f5`; a **real 9:16 browser recording** of the matching fanout.sh page fills the frame (1526x2712 at scale 70.8, cursor visible, already scrolling at the cut); the **cutout** (AI matte of the presenter) sits on top at the bottom; caption pill on the recording at y 0.385. Variety: recording → interaction recording (slider drag on a Labs page) → recording → two stacked screenshots sliding up (scale 70, y 0.215→0.175 and 0.585→0.545 over 27 f) → fast curriculum list scroll (scale 165, y 0.95→0.40 linear over 50 f) → slow push-in on a notes still (scale 52→58 over 24 f). Never the same move twice in a row. Cutout tilt (+18° at x 0.304 / −11° at x 0.610) changes only on a layout cut, at most every ~3 s.
3. **Company names** — Company Guides recording + logo pops (scale 0→N over 2–9 f eased) with "ting" SFX.
4. **Claim lines** — full-frame A-roll + title stack.
5. **"Senior engineer" line** — movie b-roll full screen (Silicon Valley 582.5 s, Social Network 93 s + 298 s) **with the cutout on top** and the title stack above the head; UI click on each cut.
6. **CTA** — full-frame A-roll with low captions.
7. **Outro** — fanout loader (scale 48) on the matte, full 2.083 s; music fades.

**Pages that match words:** `/` (hero → logos → paths), `/system/overview`, `/system/company-guides`, `/ai-engineering/overview`, `/inference-eng`, `/papers`, `/system/resources`, `/roadmap`, `/labs/model-router-and-pareto-explorer` (slider), lesson `/system/archive/sql-backed-key-value-store` (notes).

**Titles:** one Graphic per line, one track per line (Text Graphics 1/2/3). Instrument Serif Italic 85–87 white lead/tail lines; SF Pro Semibold/Bold 106–147 white keyword on a rose box. Stagger in on the spoken words (6–17 f apart), all end on the cut. Line pitch 0.063 of frame height; lead left of centre (x 0.44–0.45), box centred, tail right (x 0.56–0.60). Block starts under the chin on full-frame beats (first line ≈ chin + 0.04), above the head on b-roll beats. **In** = Text Animator: Ease In 0 / Ease Out 80 / Fade 75 / Push up 0.0495 / Motion Blur 35 (18 f on long titles, 4–12 f on short). **Out** = none (hard cut). Premiere renders titles at 0.92× nominal width; screen centre = Vector Motion position + 0.096 (serif/box family) or −0.27 (Why/Systems family).

**Captions:** 1–2 words (4–20 f), Instrument Serif Italic ~70 white on dark-green pill `#183020`; y 0.385 in layouts, 0.61 mid full-frame, 0.70 low full-frame; hard on/off; never while a title block is up; never on a screenshot.

**Cutout:** BiRefNet-portrait matte as ProRes 4444; **sized per presenter** so hair top ≈ 0.50–0.52 and head ≈ 0.30 of frame (Reel 3: scale 153 @ y 0.837; Reel 4 big head: scale 120 @ y 0.81). Measure with `face_measure.py` (+ ~0.1 for hair/updo).

**Motion rules:** no hard zooms (eased push, e.g. 158→174 over a phrase); every framing change hides behind a layout cut with a click; no visible jump cuts.

**Sound:** mechanical click −10 dB 3 f before each layout cut; UI click −15 dB on b-roll cuts and the outro; whoosh −15/−17 dB + button click ×3 at −25 dB on a punch-in; ting −10 dB on logo pops; music (ES_Electronica the Witch from 14.875 s) **−30 dB** with 7 f constant-power tail; dialogue 0 dB, Essential Sound Dialogue.

**Grade:** adjustment layer Lumetri Faded Film 28 + Noise 5 % over the dialogue only (preview approximates it).

## 2. Pipeline (one pass)

1. `ffmpeg -r 24` copy of the A-roll if not 24 fps → `deliver_media/<name> aroll.mp4` (stereo 48 kHz).
2. `mlx-whisper` large-v3-turbo with word timestamps (shim `ffmpeg` onto PATH from imageio_ffmpeg; pass the script as `initial_prompt`).
3. `tools/face_measure.py aroll.mp4` → chin/eyes/head top → punch-in scale and cutout placement.
4. `tools/matte_birefnet.py aroll.mp4 frames/` (MPS fp16, ~0.7 s/frame) → `ffmpeg -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le` → `<name>_cutout_alpha.mov`.
5. `tools/record_page.py URL out.mov --mode scroll --frames N --speed 40–52 --start S --lead 6 --vh 1356` per page (`--mode drag --selector "input[type=range]" --index 2` for a lab); stills via a 2-frame speed-0 recording.
6. Write `plan.json` from the Reel 4 template: `media`, `media_copy`, `retarget` (A-roll replaces `Sequence 02_12.mp4`; stills replace the reference screenshots), `new_media` (cutout + recordings cloned from the loader / screen-recording exemplars), `items` (video / graphic with `title:{text,style,size}` / caption with optional `y` / audio with `gain_db`, `fade_out_f`, `link`).
7. `python3 -I tools/build_prproj.py plan.json` → `.prproj` (+ prints prune/blob stats). `tools/render_preview.py plan.json preview.mp4` (set `preview_grade: true`, `media_flat: true`). Check a 2–3 fps contact sheet before sending.
8. On approval: `tools/export_fcp7xml.py plan.json "<name>.xml"` (+ captions `.srt`), `gunzip -c` the prproj to an uncompressed `.xml`, write README, reveal the `Copied_<name>` folder (media flat beside the files).

## 3. Premiere file-format rules (what made the .prproj open)

- Serialize exactly like Premiere: `<X/>` without a space, newlines inside text as `&#10;` except the literal newline+tabs before a closing tag after base64, file ends `\n\n`. The writer round-trips the reference byte-for-byte.
- Never leave an empty `<TrackItems>`; never remove `ContentAndMetadataState` from a Media; no `<Gain>` for 0 dB.
- `BinaryHash` blocks: defined once with data at the first occurrence in file order; later occurrences are empty elements with the same hash. Hash = 24-hex key + 8-hex (blob length + 12). Premiere rejects a reference whose definition was pruned and a known hash reappearing on a cloned object → re-hash every block inside cloned objects (consistently file-wide), enforce definition-first, re-materialise pruned definitions from the reference blob table. The key is not md5/sha/xxhash and is not verified.
- Linked A/V = `Link` objects under `Sequence/Links`. Title in-animations are `VideoTransitionTrackItem`s in the track's `TransitionItems`. Caption text = last length-prefixed string of the `FormattedTextData` blob; its y = float at byte 232 (`(y−0.385)/0.98−0.5521`). Ticks 254016000000/s; graphic/still keyframes carry a +3600 s base.
- FCP7 XML must mirror Premiere's own export (xmeml v4, uuid, masterclipid, pproTicks, alphatype, stereo audio as linked channel pairs on paired tracks, logging/colour/label blocks); generic xmeml v5 imports as nothing. After import Abik re-applies title/pill styles, Text Animator in-transitions, and the grade.
- macOS screen-recording filenames contain U+202F before "AM"; normalise when matching names.

## 4. Feedback history (why the rules exist)

1. First build: preview before project; content decided from the script, not copied; text never on the face; music was too loud (→ −30 dB); outro was cut (→ full loader).
2. Reel 3 round 2: "perfect cutout" (→ BiRefNet); captions never on screenshots; don't recut a pre-cut A-roll; engineer movie b-roll.
3. Round 3: text placement like the reference (tight stagger); screens must be scrolling recordings of the real pages.
4. Round 4: real browser recordings full frame with the cursor; cutout over b-roll; cuts hidden behind layout changes; ending voice must not be cut.
5. Approved: Reel 3 v6 and Reel 4. Deliverable: both `.prproj` and XML work.

## 5. Reference study (21 creator ads) — improvement queue and five styles

Patterns: good references change the frame every 1.5–2.3 s but never jump-cut the head (the overlay layer changes); captions 1–3 words with ONE keyword in a brand colour; headline cards at the top above the head; verdict stamps (OVERRATED red / UNDERRATED green) and counting-number cards; product UI as phone-in-hand, full-screen UI + presenter bubble, or split frame; dark-navy animated diagrams beat page scrolls for "how it works"; rhythm beats (0.5 s blurred freeze + giant number, flash-to-white, 1 s tinted stock); dedicated CTA end card.

Queue for Normal UGC 1: keyword colour; stamp + counter presets; top headline card; rhythm beats; diagram inserts; split-frame layout; social-proof stacks; CTA end card; emoji pops; optional 60 s ad cut.

Styles to build (presets on the same pipeline): **Stamp UGC** (Aliyan), **Motion-Graphic Explainer** (Faraz), **Top-Card Authority** (newline), **Product-Bubble Walkthrough** (Grind / Devmaxx), **Lo-fi Pop** (vibe coding / Hiring Funnel).

## 6. Checklist before sending a preview

- [ ] A-roll uncut, 24 fps, runs to the last frame; dialogue clip = full length
- [ ] Face measured; title blocks under the chin (full-frame) / above the head (b-roll); nothing on the face
- [ ] Recordings real, full frame, cursor visible, moving at frame 0; no two identical moves in a row
- [ ] Pill at 0.385 on recordings, never on a screenshot
- [ ] Cutout sized to this presenter; tilt changes only on layout cuts; no hard zooms
- [ ] B-roll full screen with cutout + title stack
- [ ] Music −30 dB + fade; clicks before every cut; outro complete
- [ ] Contact sheet reviewed; mix levels measured
