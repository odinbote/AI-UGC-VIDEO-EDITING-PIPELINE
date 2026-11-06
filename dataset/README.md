# Dataset

Everything the pipeline was taught from and everything it produced, with the human editor's verdict on each output.
Editor: Abik Newar. Format: vertical 1080x1920, 24 fps, fanout.sh UGC reels, Premiere Pro 26.5.

Read `labels.json` first: it maps each generated output to its plan, the verdict, and the feedback that followed.

| Folder | What it is | Role |
|---|---|---|
| `reference_edit/` | `AI UGC 1.prproj` (the human-edited Premiere project), its final render, and the screen recordings + screenshots the editor used as inputs | The teaching example: the editing system in `../EDITING_SYSTEM.md` was reverse-engineered from this project |
| `raw_aroll/` | The three raw talking-head A-rolls, the scripts spoken in them, word-level transcripts, face measurements | Model inputs |
| `generated_previews/` | Preview renders produced by `tools/render_preview.py` | Model outputs (labelled in `labels.json`) |
| `generated_packages/` | The delivered `.prproj` + FCP7 `.xml` + `.srt` + README for Reel 3 and Reel 4 (no media) | Model outputs, project form |
| `human_finals/` | The editor's own final exports of Reel 3 and Reel 4, made from the generated packages | Ground truth: what the human kept or changed |
| `page_recordings/` | Real 9:16 browser recordings of fanout.sh pages made by `tools/record_page.py` (H.264 proxies of the ProRes originals) | Generated b-roll |
| `page_stills/` | Full-page stills of the same pages | Generated b-roll |
| `rejected/` | The plan that was rejected as "AI slop" | Negative example |
| `ugc_reference_ads/` | Manifest of the 21 creator ads studied (metadata + style notes only, no videos) | Taste reference |

Related, at the repo root: `Fanout Reel N plan.json` (the edit decision for each reel: every clip, title, caption, keyframe), `reference/` (timeline dump and frame sheets of the reference edit), and `instructions/` (the rules).

## Pairs you can train or evaluate on

- **Input -> edit decision:** `raw_aroll/<clip>.mp4` + `raw_aroll/scripts.md` + `raw_aroll/transcripts/<clip>_words.json` -> `../Fanout Reel N plan.json`
- **Edit decision -> render:** plan -> `generated_previews/…mp4` and `generated_packages/reelN/*.prproj`
- **Generated vs human:** `generated_previews/reel3_preview_v6_approved.mp4` vs `human_finals/Fanout_Reel_3_human_final.mp4` (same for Reel 4); written comparison in `../Fanout Reel 3/` and `../EDITING_SYSTEM.md`
- **Feedback as labels:** `labels.json` (verdict + the exact corrections requested per round); the consolidated rules are `../instructions/memory/hard-rules-no-slop.md`

## Files

- `raw_aroll/reel2_veo31_take3.mp4` 1080x1920, 8.0 s. `reel3_timeline1.mp4` 720x1280, 17.8 s (delivered pre-cut). `reel4_timeline11.mp4` 720x1280, 28.4 s, 25 fps.
- `raw_aroll/transcripts/*_words.json`: mlx-whisper large-v3-turbo word timestamps, seconds.
- `raw_aroll/face_measurements.json`: eye / chin / head-top lines as a fraction of frame height (YuNet), plus the cutout scale and position chosen per presenter.
- `page_recordings/*`: recorded at 763x1356 CSS px, device scale 2, cursor drawn in.

## Web copies

The repo was filled through GitHub's browser uploader, which carries at most 10 MB per file here. Every video above that size is an H.264 re-encode (two-pass, preset slow) at the **same resolution, frame rate and duration** as the original, with the same file name. Timing, layout and text are intact; fine grain and sharpness are reduced. The full-quality originals are on the editor's machine.

| File | Original | Published |
|---|---|---|
| `raw_aroll/reel3_timeline1.mp4` | 14.9 MB, 6.7 Mbps | 9.2 MB, 4.1 Mbps |
| `raw_aroll/reel4_timeline11.mp4` | 19.6 MB, 5.5 Mbps | 9.2 MB, 2.6 Mbps |
| `generated_previews/reel3_preview_v6_approved.mp4` | 21.1 MB, 8.5 Mbps | 9.3 MB, 3.7 Mbps |
| `generated_previews/reel4_preview_approved.mp4` | 40.2 MB, 10.5 Mbps | 9.4 MB, 2.4 Mbps |
| `generated_previews/reel4_preview_v2.mp4` | 40.6 MB, 10.7 Mbps | 9.4 MB, 2.4 Mbps |
| `human_finals/Fanout_Reel_3_human_final.mp4` | 64.7 MB, 26.1 Mbps | 9.4 MB, 3.7 Mbps |
| `human_finals/Fanout_Reel_4_human_final.mp4` | 101.3 MB, 26.6 Mbps | 9.4 MB, 2.4 Mbps |
| `reference_edit/AI_UGC_1_human_final.mp4` | 76.9 MB, 26.6 Mbps | 9.3 MB, 3.2 Mbps |
| `reference_edit/inputs/Screen_Recording_…1.08.06_AM.mov` | 54.8 MB, 19.5 Mbps | 9.5 MB, 3.3 Mbps |
| `reference_edit/inputs/Screen_Recording_…1.16.51_AM.mov` | 19.4 MB, 6.5 Mbps | 9.4 MB, 3.1 Mbps |

Everything else (`raw_aroll/reel2_veo31_take3.mp4`, the page recordings, project files, stills, text data) is the original file.

## What is not here

See `excluded_third_party.md`. In short: licensed music and sound effects, movie clips, other creators' ad videos, third-party logos, and the cutout mattes are not published. The finished renders (`human_finals/`, `generated_previews/`, `reference_edit/AI_UGC_1_human_final.mp4`) do contain the music bed at low level and a few seconds of movie b-roll, as any exported reel does.

## Licence

Code in this repo is MIT (see `../LICENSE`). The footage, renders and project files in `dataset/` are Abik Newar's work and are shared for study of the pipeline; third-party material embedded in the finished renders remains the property of its owners.
