---
name: manual-edit-look
description: The "manual-edit look" — Abik's own Premiere + After Effects edit of a fanout.sh UGC reel (2026-11-13), and the pipeline that reproduces it from a raw A-roll and a script. Trigger: an A-roll + script, and Abik choosing "manual-edit look" when asked. Preview first, then an editable Premiere project plus an After Effects folder.
version: 2026-11-14
---

# Manual-edit look — instructions and context

Read this file first if you are picking the work up in a fresh session. It says what we are doing, where everything is,
how to make the next video, and what is still open. The older style ("Normal UGC 1") is in `NORMAL_UGC_1_CONTEXT.md`;
the full spec with every number is `EDITING_SYSTEM.md` (§22 is this look).

## 0. What we are doing

- **Who:** Abik Newar edits vertical UGC reels (1080x1920) for fanout.sh in Premiere Pro and After Effects.
- **What:** Abik sends a raw talking-head take (an AI-generated presenter clip) and the script. The assistant cuts it in
  Abik's style, sends a **preview MP4 first**, and after his go-ahead builds an **editable Premiere project** and an
  **After Effects folder** that he finishes by hand.
- **Why this repo exists:** it holds the tools, the spec, the plans, and a dataset of inputs, outputs and Abik's verdicts,
  so the style can be reproduced and improved.
- **Where we are (2026-11-14):** on 2026-11-13 Abik re-edited the Reel 9 take himself and said to learn that edit and
  adopt it. Reels 10 to 14 were then made in that look. Previews are sent for all of them; editable packages exist for
  Reels 13 and 14. No reel in this look has a stated verdict yet (see §9).

## 1. Working agreement (do not skip)

1. **Ask which look before every video.** Three options: manual-edit look, titles without background, titles with
   background. Abik chose the manual-edit look for Reels 10 to 14.
2. **Preview first.** Build the project only after Abik says so.
3. **Content comes from the script.** Every on-screen word is a word she says. No invented headlines.
4. **Never cover the face** with text. No visible jump cuts: every cut between two presenter pieces changes the scale.
5. **Dialogue runs to its last frame**, and the outro loader plays to the end.
6. **Recordings are real 9:16 browser recordings** of fanout.sh pages, with a cursor (`tools/record_page.py`).
7. **B-roll is literal to the line**, from the local b-roll library, and never a shot another reel used
   (`B-roll library/used.json`, local only).
8. **No generic ad devices** (stamps, emoji badges, flashes, stroked captions). Abik rejected those as "AI slop"
   (`instructions/memory/hard-rules-no-slop.md`). Any new graphic element needs his OK first. The elements below are his own.

## 2. The look in one screen

| Element | How it is done |
|---|---|
| Pace | Every pause is cut. The voice keeps running under full-screen graphics. |
| Hook text | Word by word. Small white SF Pro Semibold words (68 px, tracking −49) cut in as spoken; one huge yellow `#FADE4E` SF Pro Bold keyword per phrase (up to 270 px, fitted to 75% of the width), above the head. |
| Punch-in line | One word per line, stacked beside the face. |
| All other lines | Peach `#EFB176` pill, SF Pro Medium dark text, 2–3 words. On the chest for presenter beats (y ≈ 0.66), above the cut-out's head over recordings. |
| Lists | Full-screen number cards (After Effects): off-white, giant pale numeral, the fanout course cover sliding in, bold caps title in the cover's dark shade. |
| Cover ring | The five course covers in a 3D ring turning behind the presenter's head (hook of the "sauce" script). |
| Framing | Face high (eyes about 0.36 down the frame). A different scale on every presenter piece (roughly 122–168). |
| B-roll | One shot, full screen, with a whip pan and the keyword in yellow SF Pro Medium. |
| Ending | Logo animation on the chest on "fanout", white end card `{ curated } { mapped } { complete }`, then the loader (72 frames). Only when the script has those words. |
| Sound | Music "Every Living Breathing Moment" at −15 dB; a click on cuts into graphics and recordings; whoosh + button on the first punch-in. |

Reference: `reference/abik manual edit 2026-11-13/` (his `.prproj`, his `.aep`, the collect report, the five covers,
a timeline dump, contact sheets). His export is `dataset/human_finals/Fanout_Reel_9_manual_edit_human_final.mp4`.

## 3. Making a video, step by step

Paths below are relative to the repo root. `N` is the reel number. Working folders `Fanout Reel N/` are local only.

1. **Ask the look** (§1.1). If the script is only a hook, ask "hook only or full reel".
2. **Convert the take to 24 fps** into `Fanout Reel N/Media/<name> aroll.mp4` (`ffmpeg -r 24 -fps_mode cfr`, crf 14).
   All plan frame numbers are frames of this file.
3. **Transcribe** with mlx-whisper large-v3-turbo, `word_timestamps=True`. Word starts are approximate.
4. **Find the pauses**: `ffmpeg -af silencedetect=noise=-36dB:d=0.08`. Speech segments between the silences are the
   beat boundaries. Keep pauses under about 6 frames inside a beat; cut the rest.
5. **Measure the face**: `python3 tools/face_measure.py <aroll> 2 8 14 20 …` → eyes, chin, head top as fractions of the
   frame. Presenter framing is `pos_y = 0.36 + (0.5 − eyes_raw) × scale/100`.
6. **Cut out the presenter**: `python3 tools/matte_birefnet.py <aroll> <frames dir>` (BiRefNet-portrait, about 0.8 s per
   frame on Apple Silicon). Needed for recordings, the ring and text behind the head.
7. **Record the pages**: `python3 tools/record_page.py <url> out.mov --mode scroll --frames F --speed S --start Y --lead 6 --vh 1356`.
   See §5 for what to record.
8. **Pick b-roll** by the words of the line; check the ledger; log the shot.
9. **Write the beat plan** `tools/gen_reelN.py` (copy `tools/gen_reel14.py`; §4 explains the format) and run it:
   `python3 tools/gen_reelN.py` → `Fanout Reel N/Fanout_Reel_N_preview.mp4`.
10. **Check frames from every beat** before sending: text off the face, nothing important under a pill, no toast or
    paywall in a recording, the logo not on her hands. Check the peak level (`volumedetect`).
11. **Send the preview** and say plainly what differs from his look and what was not verified.
12. **After his go-ahead, build the editable package** (§6).

## 4. The beat plan

A reel is a Python list `BEATS`. Every beat except the loader names the A-roll source frames (`src: [in, out]`) whose
sound plays under it, so pause cuts and voice-under-graphics both come from the list. All times inside a beat are A-roll
source frames. Renderer: `tools/manual_reel.py`; text helpers: `tools/manual_look.py`.

| `type` | Picture | Keys |
|---|---|---|
| `pres` | Presenter full frame | `scale`, `pos` (number, or `{"kf": [[frame, value], [frame, value]]}` for a push), `words`, `pills`, `ring`, `logo_chest` |
| `rec` | Page recording with her cut-out in front | `file`, `rec_scale` (70.8 = full width), `rec_pos`, `cut_scale`, `cut_pos`, `pill_y`, `pills`, `in_f`, `max_f` |
| `broll` | Full-screen b-roll | `file`, `in_s`, `frame_w`, `scale`, `pos` (keyframes = the pan), `words`, `pills` |
| `card` | Number card | `n` (numeral, or `None` for a plain cover card + `col`), `cover`, `lines` `[(text, 'lead'|'big', frame)]` |
| `end` | Bracket end card | `words` `[(text, in, out)]` |
| `loader` | Fanout loader on white | `n_frames` (72) |

- `words`: `{"text", "style": small|key|med|keymed, "x", "y" (baseline), "start", "end", "size", "align", "behind"}`.
  `phrase(smalls, key, key_frame, end_frame, base_y, tall=…)` in `tools/gen_reel12.py` lays out one small row over one
  keyword. Use `tall=True` when the keyword has ascenders.
- `pills`: `(text, in, out)` or `(text, in, out, y)`.
- `"click": True` on a beat adds the click sound at its cut.

Numbers that held up across Reels 10 to 14:

- Hook keyword baseline y 0.24–0.27, above the head; first piece pushes 100 → 112–114 over 14 frames.
- Cut-out over a recording: scale 95–105, centre y 0.76–0.83; pill just above her head (y 0.47–0.52).
- Lesson card punched in from the overview page: `rec_scale` 120, card centre y ≈ 0.29.
- B-roll 1920 wide at scale 182 fills the frame; pan `pos x` so the subject, not an empty wall, opens the shot.
- Logo on the chest starts about 20 frames before the cut so the wordmark has time to form.
- Audio is limited at −1 dB (`alimiter=limit=0.89`).

## 5. What to record on fanout.sh

- Course overview (`/ai-engineering/overview`): the ordered module list. Good for "modules", "in order", "everything in one place".
- Open lessons (modules 01–02, for example `/ai-engineering/lessons/vector-embeddings-semantic-space`): scroll cleanly, real lesson text and diagrams.
- **Pro lessons** (RAG, the agent loop, MCP): the page shows a "Continue this lesson with Pro" card with prices right
  under the intro. Do not record those pages. Record the lesson's **card on the overview page**, punched in.
- Daily paper pages (`/daily/…`): scroll slowly (about 1.8 px per frame) and stop before the paywall card.
- `record_page.py` removes the desktop banner, the coupon popup and the purchase toasts on every frame. Look at the
  frames anyway.

## 6. The editable package

**Premiere.** `python3 -I tools/build_manual_prproj.py N` reads `BEATS` and `tools/reelN_package.json` and writes
`Fanout Reel N/Copied_Fanout Reel N/Fanout Reel N.prproj` plus the media. It clones every clip, text graphic, caption
and sound from Abik's manual project, so the sequence settings, fonts, colours, caption style and keyword animator are his.

- His sequence runs at 23.9748 fps (10595108966 ticks per frame). The A-roll and the cut-out go in as frame-for-frame
  23.976 copies (`setpts=N*1001/24000/TB`, `atempo=0.999000999`; cut-out as ProRes 4444).
- Tracks: V1 A-roll and cards; V2 recordings and b-roll; V3 cut-out and loader; V4 and up one text word per clip;
  captions = the pills; A1/A2 voice checkerboarded; A3 clicks; A4 music; A5–A7 hook sounds.
- Text placement: Vector Motion position = target − scale × (text origin − 0.5). Text origins in his graphics:
  small (0.25558, 0.12151), keyword (0.12048, 0.16250), b-roll words (0.125, 0.37135).
- Caption height: his caption blobs store y as a float at byte 228; caption y = preview pill y − 0.007.
- His project carries preview renders of his own timeline; the builder removes them.
- `reelN_package.json`: `aroll`, `cutout`, `aroll_frames`, `rec_retarget` (his three recordings → yours), `rec_frames`,
  `rec_new` (extra recordings), `broll`.

**After Effects.** `python3 -I tools/gen_ae_script.py N` writes `Fanout Reel N/Fanout Reel N AE folder/`, laid out like
Abik's collected folder: `(Footage)/`, `Fanout Reel NReport.txt` and `Build Fanout Reel N AE.jsx`. The `.aep` itself can
only be written by After Effects, so **Abik runs the script once** (File > Scripts > Run Script File). It builds one comp
per card ("Fanout Reel N Linked Comp 01", …), saves `Fanout Reel N.aep` and writes `ae_comp_ids.json`. Run the Premiere
builder again after that: it swaps the rendered card clips for Dynamic Link comps (Premiere finds a comp by its item id,
stored in the media's `ImporterPrefs`).

**Not verified, say so every time:** the assistant cannot open Premiere or After Effects. Projects are parsed back and
checked against the preview; the AE script is run against a mock of the scripting objects. Text positions may need a nudge.

## 7. Presenters so far

| Reel | Take | Eyes (raw) | Notes |
|---|---|---|---|
| 9 | red-haired woman, white T-shirt, bright office | 0.462 | Abik's manual edit uses this take |
| 10 | second presenter, hook only | 0.394 | word stack at x 0.15 |
| 11, 12, 13 | third presenter | 0.444–0.467 | built with `pos_y = 0.36 + 0.054 × scale/100` |
| 14 | fourth presenter, holds a coin at chest height | 0.382–0.387 | hair bun top at 0.248; pills go under the coin; no logo on the chest |

All six are in `dataset/raw_aroll/face_measurements.json`.

## 8. Files

- Tools: `tools/manual_look.py`, `tools/manual_reel.py`, `tools/gen_reel10_hook.py`, `tools/gen_sauce_hook.py`,
  `tools/gen_reel12.py`, `tools/gen_reel13.py`, `tools/gen_reel14.py`, `tools/build_manual_prproj.py`,
  `tools/gen_ae_script.py`, `tools/reel13_package.json`, `tools/reel14_package.json`. Shared with the older style:
  `build_prproj.py`, `parse_prproj.py`, `record_page.py`, `face_measure.py`, `matte_birefnet.py`.
- Plans at the repo root: `Fanout Reel 10|11 hook look-plan.json`, `Fanout Reel 12|13|14 look-plan.json` (the beat list
  as data), `Fanout Reel 13|14 prproj-plan.json` (every Premiere item).
- Dataset: `dataset/raw_aroll/reel9…reel14_*.mp4` with scripts and word transcripts, `dataset/generated_previews/`,
  `dataset/generated_packages/reel13|reel14/`, `dataset/page_recordings/reel9|13|14/`, `dataset/labels.json`.
- Rules and notes: `instructions/README.md`, `instructions/memory/abik-manual-edit-style-2026-11-13.md`.

## 9. Status and open items (2026-11-14)

| Reel | Script | Look | Preview | Editable package | Abik's verdict |
|---|---|---|---|---|---|
| 9 | "sauce for engineers", full | titles without background | sent | Premiere project built | none stated; he re-edited the take by hand instead (the reference for this look) |
| 10 | same script, hook only | manual-edit | sent | not built | pending |
| 11 | same script, hook only | manual-edit | sent | not built | pending |
| 12 | same script, full | manual-edit | sent | not built | pending |
| 13 | "scrolling reels before bed" | manual-edit | sent | Premiere + AE folder | pending; not yet opened by him |
| 14 | "RAG. Agents. MCP. Vector databases." | manual-edit | sent | Premiere + AE folder | he said "Build the project"; no verdict on the look |

Open:

1. Abik runs the AE build script for Reels 13 and 14; then rebuild both Premiere projects with linked comps.
2. Confirm the projects open and the text sits where the preview shows it; fix what does not.
3. Packages for Reels 10, 11 and 12. Reel 12 needs the cover-ring comp added to `gen_ae_script.py`.
4. The plain cover card (no numeral) in Reels 13 and 14 is the assistant's variant of his number card; he has not judged it.

## 10. What is not in this repo

Licensed music and sound effects, movie and TV b-roll, the b-roll library and its ledger, third-party logos, the ProRes
cut-out mattes and the working `Copied_*` media folders. See `dataset/excluded_third_party.md`. Finished renders in
`dataset/` do contain the music bed and a few seconds of movie b-roll, as any exported reel does.
