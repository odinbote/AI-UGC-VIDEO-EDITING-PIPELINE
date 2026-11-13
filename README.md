# Normal UGC 1 — AI-assisted Premiere Pro reel pipeline

Tools, spec and plans for reproducing a human-edited vertical UGC reel style ("Normal UGC 1", built for fanout.sh) from a raw A-roll and a script. The pipeline transcribes the A-roll, measures the presenter, mattes them, records the real product pages in a 9:16 browser, writes an edit plan, and generates a **Premiere Pro project (.prproj)** plus a **Final Cut Pro 7 XML** by cloning clips from a reference project.

**Continuing the work? Read [`MANUAL_EDIT_LOOK_CONTEXT.md`](MANUAL_EDIT_LOOK_CONTEXT.md) first.** It gives the instructions and context for the current look (the editor's own manual edit of 2026-11-13, used for Reels 10 to 14): what we are doing, the step-by-step pipeline, the beat-plan format, the editable Premiere + After Effects package, and the status of every reel. It is also packaged as a Claude Code skill (`.claude/skills/manual-edit-look/`).

**The original style:** [`NORMAL_UGC_1_CONTEXT.md`](NORMAL_UGC_1_CONTEXT.md) (the whole system in one file, also usable as a Claude Code skill).
Full spec: [`EDITING_SYSTEM.md`](EDITING_SYSTEM.md) (§21 is what the editor changed in his own re-edit: two title styles, b-roll rules, punch-ins; §22 is his manual edit, the look to follow now; §23 is how Reels 10 to 14 were built in it). Reference study of 21 creator ads: [`UGC_REFERENCE_STUDY.md`](UGC_REFERENCE_STUDY.md).

## Tools (`tools/`)

| Script | What it does |
|---|---|
| `parse_prproj.py` | Dumps a .prproj timeline: tracks, clips, effects, keyframes, captions |
| `build_prproj.py` | Plan JSON → Premiere-exact `.prproj` (clones exemplar clips from a reference project, re-targets media, rewrites title/caption text, re-hashes binary blocks, prunes orphans) |
| `export_fcp7xml.py` | Plan JSON → FCP7 XML in Premiere's own dialect + captions SRT |
| `render_preview.py` | Plan JSON → graded preview MP4 (PIL compositor + ffmpeg mix) |
| `face_measure.py` | YuNet face measurement → punch-in scale / title / cutout placement |
| `matte_birefnet.py` | BiRefNet-portrait alpha matte on Apple MPS (fp16) |
| `record_page.py` | Playwright 9:16 browser recordings with cursor (`--mode scroll` / `--mode drag`) |
| `make_scroll.py` | Legacy synthetic scroll from a tall screenshot |
| `gen_reel67_plans.py`, `gen_reel8_plan.py` | Plan generators for multi-clip A-rolls with hook variants: beats written in clip-local frames, one plan per hook; Reel 8 builds on the editor's own re-edited project |
| `gen_reel9_plan.py` | Plan generator for Reel 9 (one take, titles without background, library b-roll) |
| `manual_look.py`, `manual_reel.py` | Preview compositor for the manual-edit look: word-by-word hook text with a yellow keyword, peach caption pills, the cover ring, number cards, recordings with the presenter cut-out, b-roll with a pan, the bracket end card, the loader, and the audio mix |
| `gen_reel10_hook.py`, `gen_sauce_hook.py`, `gen_reel12.py`, `gen_reel13.py`, `gen_reel14.py` | Beat plans for Reels 10 to 14; running one renders its preview |
| `build_manual_prproj.py` + `reel13_package.json`, `reel14_package.json` | Beat plan → editable Premiere project, cloned clip by clip from the editor's manual project (23.9748 fps sequence, one text word per clip, captions as pills, Dynamic Link to After Effects comps) |
| `gen_ae_script.py` | Writes the After Effects folder for a reel: an ExtendScript that builds the card comps and saves the `.aep`, the footage, and a collect-style report |
| `catalog_shots.py` | Shot catalogue for b-roll sources: cut detection, in/out per shot, thumbnail sheets |
| `overlays.py` | Ad-style overlay devices from the reference study. Rejected by the editor, kept as a negative example (see `dataset/rejected/`) |

Plans for the manual-edit look: `Fanout Reel 10|11 hook look-plan.json`, `Fanout Reel 12|13|14 look-plan.json` (the beat list) and `Fanout Reel 13|14 prproj-plan.json` (every Premiere item). `Fanout Reel 9 plan.json` is the last plan in the older format.

Earlier plans: `Fanout Reel 5`, `6 - hook A|B|C`, `7 - hook A|B|C` and `8` are the newest; `Fanout Reel 4 plan.json` is the original template; `Fanout Reel 2/3 plan.json` show the evolution; `Fanout Reel 4 v2 plan.json` is the latest revision.

## Dataset and instruction set

- [`dataset/`](dataset/README.md): the raw A-rolls with scripts, word-level transcripts and face measurements; the human-edited reference project (`AI UGC 1.prproj`) with its render and input recordings; the generated previews and packages; the editor's own final exports of Reel 3 and Reel 4; real page recordings and stills; the rejected plan; a manifest of the 21 reference ads. Reels 9 to 14 (added 2026-11-14) include the editor's manual-edit export, the takes, previews, packages and page recordings made in that look. [`dataset/labels.json`](dataset/labels.json) records the editor's verdict and corrections for every output.
- [`instructions/`](instructions/README.md): the rules, in reading order, including a copy of the assistant's persistent memory notes for this style (hard rules, style definition, feedback rounds).

Videos over 10 MB are published as H.264 web copies at the original resolution and frame rate; see [`dataset/README.md`](dataset/README.md#web-copies).

## What is not in this repo
Licensed music and sound effects, movie b-roll clips and the b-roll library, third-party logos, other creators' ad videos, and the ProRes cutout mattes (regenerable with `tools/matte_birefnet.py`). The working `Copied_*` packages stay local because they contain those files; their project files are published under `dataset/generated_packages/`. Full list with reasons: [`dataset/excluded_third_party.md`](dataset/excluded_third_party.md).

## Requirements
Python 3.14, `imageio-ffmpeg`, `av`, `pillow`, `numpy`, `opencv-python-headless`, `mlx-whisper`, `torch` + `transformers` (BiRefNet), `playwright` (+ `playwright install chromium`), `rembg` (optional). Apple Silicon assumed for the matte step.

## Key findings about Premiere's .prproj format
See `EDITING_SYSTEM.md` §15: byte-exact serialization, binary-block definition order and re-hashing, linked clips, caption/title blob layout. These are what make a generated project open without the "damaged file" error.

MIT licensed. Built with Claude Code.
