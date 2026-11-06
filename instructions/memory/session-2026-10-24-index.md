---
name: session-2026-10-24-index
description: "Index of everything built and learned on 2026-10-24 — where the spec, tools, plans, delivered reels and study live; read this first when Abik says \"remember\" or sends a new reel"
metadata:
  node_type: memory
  type: project
  originSessionId: 50ae89ed-a5e9-41ec-bd82-530f1b1ca78b
  modified: 2026-10-24T18:19:58.251Z
---

Public GitHub repo (published 2026-10-28 via GitHub's web uploader through Claude in Chrome, since no git credential exists on the Mac): https://github.com/odinbote/AI-UGC-VIDEO-EDITING-PIPELINE — 31 files (tools, docs, plans, skill, reference sheets); media and Copied_ packages are git-ignored. Local repo at the workspace tracks origin/main; a `git push` still needs a token typed by Abik or the Chrome-upload route.

Workspace: `/Users/abiknewar/Work/Claude Editing 2/`
- `NORMAL_UGC_1_CONTEXT.md` — the single consolidated context/skill file (also installed as the `normal-ugc-1` skill at `~/.claude/skills/normal-ugc-1/SKILL.md` and in the project's `.claude/skills/`). Give Abik this file when they ask for "the context file".
- `EDITING_SYSTEM.md` §1–17 — the complete "Normal UGC 1" spec (reference analysis, corrections, prproj rules, screen-section method, per-presenter cutout sizing).
- `UGC_REFERENCE_STUDY.md` + `UGC_reference_styles_board.png` — 21-ad study, improvement list, five styles.
- `tools/`: `parse_prproj.py` (dump a .prproj), `build_prproj.py` (plan JSON → Premiere-exact .prproj; clones reference exemplars, re-hashes blobs, prunes), `export_fcp7xml.py` (plan → Premiere-dialect FCP7 XML + SRT), `render_preview.py` (plan → graded preview MP4), `face_measure.py` (YuNet framing numbers), `matte_birefnet.py` (BiRefNet-portrait on MPS fp16 → RGBA frames), `record_page.py` (Playwright 9:16 page recordings with cursor, `--mode scroll|drag`, `--vh 1356`), `make_scroll.py` (legacy synthetic scroll).
- Plans: `Fanout Reel 2/3/4 plan.json` — Reel 4 plan is the template (media_flat, preview_grade, recordings as new_media, logos, b-roll, titles with `title:{text,style,size}`, captions with optional `y`).
- Delivered: `Fanout Reel 3/Copied_Fanout Reel 3/` (v6, approved, opens) and `Fanout Reel 4/Copied_Fanout Reel 4/` (approved preview, package built). Reel 2 was the first build (superseded).
- Reference project: `/Users/abiknewar/Work/Fanout/AI UGC/Project FIle/Copied_AI UGC 1/AI UGC 1.prproj` + render `AI  UGC 1 d3.mp4` — every exemplar clip is cloned from it, so it must stay in place.
- Scratch (not persistent): `/private/tmp/claude-501/.../scratchpad/` holds the downloaded UGC references, mattes, recordings; re-create if gone.

Pipeline for a new reel ("Normal UGC 1"): convert A-roll to 24 fps copy → mlx-whisper words → face_measure → matte_birefnet (bg) → record pages the script names → write plan from the Reel 4 template → build_prproj → render_preview → send preview → on approval export XML, write README, reveal package.

See [[style-normal-ugc-1]], [[fanout-reel-editing-system]], [[reel-feedback-first-build]], [[ugc-reference-styles]], [[abik-editor-profile]].
