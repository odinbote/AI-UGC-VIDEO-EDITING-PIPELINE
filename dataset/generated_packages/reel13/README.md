# Fanout Reel 13 — "scrolling reels before bed" (manual-edit look)

Built 2026-11-13 by cloning every clip, text graphic, caption and sound from Abik's own manual project
(`AI UGC Manual Edits.prproj`), so the sequence settings, fonts, colours, caption style and keyword animator are his.

## Files

- `Fanout Reel 13.prproj` — the Premiere project (Premiere Pro 2027). Sequence 1080x1920 at your 23.9748 fps, 861 frames.
- Media (not published, see `../../excluded_third_party.md`): the A-roll and her cut-out as frame-for-frame 23.976 copies, three page recordings, the b-roll clip, the loader, music and sound effects.
- The After Effects side is in `Fanout Reel 13 AE folder/` (next to this file here; in the working folder it sits beside `Copied_Fanout Reel 13/`), laid out like your collected folder:
  `Fanout Reel 13.aep` (appears when the build script has run), `(Footage)/`, `Fanout Reel 13Report.txt`, `Build Fanout Reel 13 AE.jsx`.

## Step 1: open the Premiere project

Everything is a normal editable clip:

| Track | What is on it |
|---|---|
| V1 | A-roll pieces (each with its own scale and position), and the "AI ENGINEERING" card |
| V2 | page recordings, the b-roll shot (position keyframes for the pan), the white matte under the end card |
| V3 | her cut-out over the recordings, the first end-card word, the loader |
| V4–V7 | text: one word per clip (small white words, yellow keywords with the text animator), end-card words |
| V10 | the logo animation on her chest (loader at 200%, tinted white) |
| Captions | the peach pills, one caption per phrase |
| A1/A2 | her voice, checkerboarded, every pause cut |
| A3–A7 | click, music, whoosh, button |

The card on V1 is a rendered clip (`r13_card_05.mov`) until step 2 is done.

## Step 2: make the After Effects project

1. In After Effects: save your open project, then File > Scripts > Run Script File… and pick
   `Fanout Reel 13 AE folder/Build Fanout Reel 13 AE.jsx`.
2. It creates a new project with the comp `Fanout Reel 13 Linked Comp 01` (background solid, the cover with position and
   rotation keyframes, two text layers with opacity keyframes and a Camera Lens Blur in), saves it in that folder as
   `Fanout Reel 13.aep`, and writes `ae_comp_ids.json`.
3. Tell Claude it is done. The Premiere project is rebuilt with the card as a Dynamic Link comp, and a copy of the .aep is
   placed next to the .prproj, as in your own package. (Premiere finds a linked comp by its item id inside the .aep,
   which only exists after After Effects has saved it.)

## Not verified

Claude cannot open Premiere or After Effects. The project was parsed back and checked clip by clip against the preview,
and the script was run against a mock of the After Effects scripting objects, but neither file has been opened in the real apps yet.
Text positions are computed from your own graphics' anchor points and may need a small nudge.
