---
name: fanout-reel-editing-system
description: "Abik's Premiere Pro vertical-reel editing system (learned 2026-10-24 from \"AI UGC 1\" fanout reel) — layout grammar, title/caption styles, in/out animation rules, SFX rules, where the spec lives"
metadata:
  node_type: memory
  type: project
  originSessionId: 50ae89ed-a5e9-41ec-bd82-530f1b1ca78b
  modified: 2026-10-24T10:16:47.692Z
---

Full spec: `/Users/abiknewar/Work/Claude Editing 2/EDITING_SYSTEM.md` (parser in `tools/parse_prproj.py`, frame sheets + timeline dump in `reference/`).
Reference project: `/Users/abiknewar/Work/Fanout/AI UGC/Project FIle/Copied_AI UGC 1/AI UGC 1.prproj` (Premiere 26.5, 1080x1920, 24 fps, 23 s), render `AI  UGC 1 d3.mp4`.

Core rules (short form):
- 14 video tracks: Aroll / Color matte #f5f5f5 / Screen Rec 1 / Screen Rec 2 / Broll 1 / Broll 2 / Aroll Cutout (AI object mask, scale 102, y 0.818) / Aroll Full Screen (scale 141–157) / Logos / Text Graphics 1-2-3 (one track per title line) / Adjustment (Lumetri Faded Film 28 + Noise 5 %) / Outro (fanout loader). Caption track "Subtitle 1". Audio: Aroll, SFX 1–5, Music.
- Sections alternate every 1.3–3.8 s: full-frame A-roll + 3-line title ↔ white-matte layout with screen recording on top (scale 68–75, y 0.37–0.39) and cutout at bottom (sometimes rotated ±11–18°, offset to a side) ↔ b-roll. All layout changes are hard cuts on a click SFX.
- Titles: Instrument Serif Italic ~110 px white lead/tail lines, SF Pro Semibold/Bold ~135 px white keyword on rose box (#a05450 after grade). Lines stagger in on spoken words (6–17 f apart), end together on the cut.
- Title IN animation (identical on all): Text Animator custom — Ease In 0 / Ease Out 80 / Fade 75 / Push Position (0, +0.0495) i.e. push up ~95 px / Motion Blur 35 on. ~10–11 frames to settle. Title OUT: none — hard cut with the picture. Never add fades.
- Captions: 1–2 words each (4–20 f), Instrument Serif Italic ~70 px white on dark-green pill #183020, y ≈ 0.385 in layouts / 0.70 full-frame, hard on/off, never shown while a title block is up.
- Screen-content motion: stacked screenshots slide up ~60–107 px over 27 f eased; logo pops scale 0→N in 2–9 f eased with "ting" SFX; page scroll y 0.79→0.17 linear over 50 f; slow push scale 56→74 over 24 f.
- SFX start 2–12 f before the cut. Punch-in jump cut (0.29 s dropped, scale 119→163) gets whoosh + button click stacked 3× at 120 %. Music one Epidemic track trimmed mid-song, 0 dB; dialogue uses Essential Sound Dialogue preset.
- prproj facts: ticks 254016000000/s; keyframe times carry +3600 s offset; text content is FlatBuffer blobs (Source Text / FormattedTextData); 28 Text Animators = 14 titles × (source + instance copy).

Build pipeline (first used 2026-10-24 for "Fanout Reel 2", 8 s Veo A-roll, output in `/Users/abiknewar/Work/Claude Editing 2/Fanout Reel 2/`): mlx-whisper word timings (needs an `ffmpeg` shim on PATH from imageio_ffmpeg) → headless Chrome 2x captures of fanout.sh (`--headless=new --force-device-scale-factor=2`, no popup) → rembg `isnet-general-use` alpha matte as ProRes 4444 (birefnet-portrait is cleaner but ~35 s/frame on CPU) → `tools/build_prproj.py` clones exemplar clips from the reference XML per a plan JSON, retargets media, prunes orphans → `tools/render_preview.py` for a PIL preview. Title in-animations are `VideoTransitionTrackItem`s (18 f long titles / 4–12 f short); caption text is the tail string of the blob, y-position float at byte 232.

Paused state (2026-10-24): Reel 3 v2 mid-revision — see `/Users/abiknewar/Work/Claude Editing 2/Fanout Reel 3/STATUS.md` (open items: dark fill for serif titles on the matte, b-roll in-point 1148.5 s, then re-render preview and send).

.prproj generation rules (confirmed opening 2026-10-24, EDITING_SYSTEM.md §15): Premiere-exact serialization (`<X/>`, `&#10;` in text, double newline at end); no empty TrackItems; keep ContentAndMetadataState; BinaryHash blocks are defined once at first occurrence (data) and referenced by empty elements after — re-hash every block inside cloned objects (fresh 24-hex key + len+12 suffix), enforce definition-first, re-materialise pruned definitions from the reference. Both deliverables now work: .prproj (native) and FCP7 XML.

Reel 4 (2026-10-24, 28 s, new presenter with a large head): cutout must be sized per presenter (hair top ≈ 0.5, head ≈ 0.30 of frame → scale 120 @ y 0.81 here vs 153 @ 0.837 before); 25 fps A-roll converted to 24 fps first; recorder waits for load (not network-idle); dimmed headless captures → take stills via record_page. Reel 4 package: /Users/abiknewar/Work/Claude Editing 2/Fanout Reel 4/Copied_Fanout Reel 4/.

**Why:** Abik wants future raw A-roll edited to this exact system and delivered as a Premiere project file.
**How to apply:** when a new raw A-roll + platform link arrives, follow EDITING_SYSTEM.md §9 (jump-cut → transcribe → title/caption plan → clone the project XML → user re-tracks the object mask in Premiere). See [[abik-editor-profile]].
