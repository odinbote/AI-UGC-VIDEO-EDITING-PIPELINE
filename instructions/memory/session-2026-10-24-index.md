---
name: session-2026-10-24-index
description: "Index of everything built and learned on 2026-10-24 — where the spec, tools, plans, delivered reels and study live; read this first when Abik says \"remember\" or sends a new reel"
metadata:
  node_type: memory
  type: project
  originSessionId: 50ae89ed-a5e9-41ec-bd82-530f1b1ca78b
  modified: 2026-11-09T13:56:48.481Z
---

Public GitHub repo (published 2026-10-28 via GitHub's web uploader through Claude in Chrome, since no git credential exists on the Mac): https://github.com/odinbote/AI-UGC-VIDEO-EDITING-PIPELINE — 31 files (tools, docs, plans, skill, reference sheets); media and Copied_ packages are git-ignored. Local repo at the workspace tracks origin/main; a `git push` still needs a token typed by Abik; Abik prefers the Chrome-upload route ("use browser and push", 2026-11-06). How: /upload/main/<dir> per folder, ≤10 MB per tool call, then `git fetch` + `git reset origin/main` (mixed, never --hard: hard would delete local files that are not on the remote).

2026-11-06: the repo now also holds `dataset/` (raw A-rolls, scripts, word transcripts, face measurements, reference .prproj + render + its input recordings/screenshots, human finals of Reel 3/4, generated previews + packages, page recordings/stills, rejected plan, reference-ad manifest, `labels.json` with Abik's verdict per output) and `instructions/` (reading order + copies of the seven Normal UGC 1 memory notes). 96 files, about 182 MB, local `main` == `origin/main`. Published through Claude in Chrome's uploader (10 MB per tool call), so the ten videos over 10 MB are same-resolution H.264 web copies; full-quality originals are in `dataset_originals/` (local only, listed in `.git/info/exclude`). Scope rule: see [[repo-scope-fanout-ugc-only]]. Never published: Epidemic Sound `ES_*.mp3`, movie clips, third-party logos, other creators' ads, `*_cutout_alpha.mov` (list in `dataset/excluded_third_party.md`).

Workspace: `/Users/abiknewar/Work/Claude Editing 2/`
- `NORMAL_UGC_1_CONTEXT.md` — the single consolidated context/skill file (also installed as the `normal-ugc-1` skill at `~/.claude/skills/normal-ugc-1/SKILL.md` and in the project's `.claude/skills/`). Give Abik this file when they ask for "the context file".
- `EDITING_SYSTEM.md` §1–17 — the complete "Normal UGC 1" spec (reference analysis, corrections, prproj rules, screen-section method, per-presenter cutout sizing).
- `UGC_REFERENCE_STUDY.md` + `UGC_reference_styles_board.png` — 21-ad study, improvement list, five styles.
- `tools/`: `parse_prproj.py` (dump a .prproj), `build_prproj.py` (plan JSON → Premiere-exact .prproj; clones reference exemplars, re-hashes blobs, prunes), `export_fcp7xml.py` (plan → Premiere-dialect FCP7 XML + SRT), `render_preview.py` (plan → graded preview MP4), `face_measure.py` (YuNet framing numbers), `matte_birefnet.py` (BiRefNet-portrait on MPS fp16 → RGBA frames), `record_page.py` (Playwright 9:16 page recordings with cursor, `--mode scroll|drag`, `--vh 1356`), `make_scroll.py` (legacy synthetic scroll).
- Plans: `Fanout Reel 2/3/4 plan.json` — Reel 4 plan is the template (media_flat, preview_grade, recordings as new_media, logos, b-roll, titles with `title:{text,style,size}`, captions with optional `y`).
- Delivered: `Fanout Reel 3/Copied_Fanout Reel 3/` (v6, approved, opens) and `Fanout Reel 4/Copied_Fanout Reel 4/` (approved preview, package built). Reel 2 was the first build (superseded).
- Reel 5 ("the archive", A-roll `~/Downloads/cut 2.mp4`, 1080x1920 source): plan `Fanout Reel 5 plan.json`, preview sent 2026-11-09, Abik then asked for the project file → package at `Fanout Reel 5/Copied_Fanout Reel 5/` (not yet confirmed opened). For a 1080-wide source the numbers are A-roll scale 128, cutout 130 @ y 0.845. Pages now used: `/papers`, `/daily`, `/roadmaps`, `/roadmaps/ai-research`, `/ai/blogs`, `/ai/community`; site header is sticky (88 css px), so crop stills below it.
- Reels 6 and 7 (2026-11-11, multi-clip A-rolls with hooks A/B/C; sources `~/Downloads/learning ai the hard way/` and `~/Downloads/stop winging your system design/`): see [[multi-clip-hook-variants]]. Packages `Fanout Reel 6/Copied_Fanout Reel 6/` and `Fanout Reel 7/Copied_Fanout Reel 7/`, three .prproj + XML + SRT each; previews sent, Abik asked for the project files the same evening (not yet confirmed opened).
- Reel 8 (Discord story, `~/Downloads/hook A/`, six clips, 2026-11-12): first build in Abik's new look. Generator `tools/gen_reel8_plan.py` uses his `Fanout Reel 7 - hook A_1.prproj` (copy in `reference/abik edits 2026-11-12/`) as the reference project, so titles come out in the no-background style; renderer styles `serif-regular` / `plain-bold`. Preview sent 2026-11-12 (`Fanout Reel 8/Fanout_Reel_8_preview.mp4`), project built in `Fanout Reel 8/Copied_Fanout Reel 8/`, verdict not yet given. Story lines use real recordings of the sources named (Discord engineering posts, cassandra.apache.org, scylladb.com, a C++ file on GitHub, rust-lang.org) and fanout's own case study `/system/archive/case-discord-message-storage`.
- Reference project: `/Users/abiknewar/Work/Fanout/AI UGC/Project FIle/Copied_AI UGC 1/AI UGC 1.prproj` + render `AI  UGC 1 d3.mp4` — every exemplar clip is cloned from it, so it must stay in place.
- Scratch (not persistent): `/private/tmp/claude-501/.../scratchpad/` holds the downloaded UGC references, mattes, recordings; re-create if gone.

Pipeline for a new reel ("Normal UGC 1"): convert A-roll to 24 fps copy → mlx-whisper words → face_measure → matte_birefnet (bg) → record pages the script names → write plan from the Reel 4 template → build_prproj → render_preview → send preview → on approval export XML, write README, reveal package.

See [[style-normal-ugc-1]], [[fanout-reel-editing-system]], [[reel-feedback-first-build]], [[ugc-reference-styles]], [[abik-editor-profile]].
