# Normal UGC 1 — AI-assisted Premiere Pro reel pipeline

Tools, spec and plans for reproducing a human-edited vertical UGC reel style ("Normal UGC 1", built for fanout.sh) from a raw A-roll and a script. The pipeline transcribes the A-roll, measures the presenter, mattes them, records the real product pages in a 9:16 browser, writes an edit plan, and generates a **Premiere Pro project (.prproj)** plus a **Final Cut Pro 7 XML** by cloning clips from a reference project.

**Start here:** [`NORMAL_UGC_1_CONTEXT.md`](NORMAL_UGC_1_CONTEXT.md) (the whole system in one file, also usable as a Claude Code skill).
Full spec: [`EDITING_SYSTEM.md`](EDITING_SYSTEM.md). Reference study of 21 creator ads: [`UGC_REFERENCE_STUDY.md`](UGC_REFERENCE_STUDY.md).

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

Plans: `Fanout Reel 4 plan.json` is the current template; `Fanout Reel 2/3 plan.json` show the evolution.

## What is not in this repo
Media (A-roll footage, mattes, page recordings, Epidemic Sound music/SFX, movie b-roll) and the generated `Copied_*` packages are git-ignored: they are licensed or personal and several GB. The reference project the generator clones from (`AI UGC 1.prproj`) is private to the author. Set `reference` in the plan to your own Premiere project to use the generator.

## Requirements
Python 3.14, `imageio-ffmpeg`, `av`, `pillow`, `numpy`, `opencv-python-headless`, `mlx-whisper`, `torch` + `transformers` (BiRefNet), `playwright` (+ `playwright install chromium`), `rembg` (optional). Apple Silicon assumed for the matte step.

## Key findings about Premiere's .prproj format
See `EDITING_SYSTEM.md` §15: byte-exact serialization, binary-block definition order and re-hashing, linked clips, caption/title blob layout. These are what make a generated project open without the "damaged file" error.

MIT licensed. Built with Claude Code.
