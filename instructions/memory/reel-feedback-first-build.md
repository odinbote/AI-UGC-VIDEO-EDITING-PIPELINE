---
name: reel-feedback-first-build
description: "Abik's corrections after the first generated reel (2026-10-24) — preview before project, decide content from the script, never cover the face, music −30 dB, outro must finish"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 50ae89ed-a5e9-41ec-bd82-530f1b1ca78b
  modified: 2026-10-24T11:16:04.297Z
---

After the first "Fanout Reel 2" build Abik asked for four things, and a workflow change: **deliver a preview first; build the .prproj only after they confirm the preview.**

1. Content is not copy-paste: next time the script and the person differ, so derive beats (title moment / layout with matching site page / b-roll / caption) from the transcript and pick fanout.sh pages that show what is said.
2. Text must never overlap the face, and words on one line need proper spacing ("Instead of" + "memorizing" ran together in the preview). Measure the face (tools/face_measure.py, YuNet), put the title block at the chin and below; Premiere renders titles at 0.92× nominal width, anchor = centre, vertical offset per exemplar family (+0.096 / −0.27).
3. Background music was far too loud in the preview: the reference uses Audio Gain −30 dB on the music clip plus a 7-frame constant-power fade; SFX −10 to −25 dB. The generated project had the gain, the preview did not — always mix the preview with the real gains.
4. The outro was cut off in the preview (loader extracted at 60 fps instead of 24). Outro = full 2.083 s loader, sequence ends after it.

Abik confirmed the corrected preview (2026-10-24): title block at the chin with 0.92× metrics and per-exemplar offsets, music −30 dB + fade, full outro. That is the accepted look.

Second round (Reel 3, 2026-10-24): (a) matte + cutout look everywhere except real b-roll (no full-frame raw video); (b) "perfect cutout" = BiRefNet-portrait on MPS fp16 (tools/matte_birefnet.py, 5 min per 427 frames), not isnet; (c) captions never on screenshots — screens in a zone above the pill (y 0.03–0.34), pill at 0.415, titles on the matte above the head; (d) a pre-cut A-roll must not be recut; (e) senior-engineer b-roll = engineer scenes from Silicon Valley / Social Network / Mr Robot (Abik supplies Mr Robot).

Third round (Reel 3 v4): screens must be scrolling recordings of the real pages in a narrow portrait browser (tools/make_scroll.py from 763px-wide 2x captures, 1526x1100 viewport, scale 66 at y 0.22); title lines stack tightly (pitch 0.063) and staggered left/centre/right like the reference; b-roll beats are full screen without the cutout; full-frame A-roll for hook/title/CTA beats.

Deliverable format (2026-10-24, Reel 3): Abik does NOT want a .prproj — deliver **Final Cut Pro 7 XML** (`tools/export_fcp7xml.py`), packaged like the reference (one folder, media flat beside the XML, plus a captions .srt). The XML must mirror Premiere's own FCP export schema (xmeml version 4, uuid, masterclipid, pproTicks, alphatype, stereo audio as linked channel pairs on paired tracks, logging/colour/label blocks) — a generic xmeml v5 file imported silently as nothing. Confirmed importing correctly in Premiere 26.5. After import Abik re-applies: title box/pill styles, Text Animator in-transitions, adjustment-layer grade.

Comparison round (2026-10-24, after Reel 3 opened): Abik's reference screen sections = REAL browser recordings in a tall narrow window (1526x1900), continuous brisk scroll already in motion at the cut (no holds), ~1.5–2 screens/s, cursor/hover present, filling the width and ~65 % of frame height with the cutout head overlapping the bottom and the pill over the recording at y 0.385; variety every 1–1.5 s (recording → stacked screenshots slide → list scroll → push-in → logo pops); logged-in lesson page showing the actual animation canvas. Mine (v4) = synthetic eased scrolls from static captures in a 1526x1100 window, with holds, placed small in the top third, pill in a gap below, no cursor, no screenshot variety, lesson page top instead of the animation. Fix list: real recordings (Playwright with wheel scrolling, cursor overlay), tall window + reference placement, continuous motion, alternate recordings with screenshot moves, logged-in lesson capture (needs Abik's session or a recording from him).

APPROVED look (Reel 3 v6, 2026-10-24): real 9:16 browser recordings (tools/record_page.py --vh 1356, 1526x2712, scale 70.8) as the FULL-FRAME background with cursor, cutout on top, pill at 0.385; movie b-roll full screen WITH the cutout and the title stack above the head; no hard zooms (eased push), cutout tilt only on layout cuts; screenshot beats (stacked slide, list scroll) on the matte for variety; dialogue to the file's last frame; grade in preview.

**Why:** the preview is what Abik judges; it must be faithful to what Premiere will render, and layout must adapt to each new face/framing.
**How to apply:** follow EDITING_SYSTEM.md §11; run face_measure before planning; render preview with tools/render_preview.py (gains, offsets, FONT_SCALE built in); send preview; wait for confirmation; then build_prproj.py. See [[fanout-reel-editing-system]].
