---
name: style-normal-ugc-1
description: "Normal UGC 1" — the name Abik gave the approved reel editing style (Reel 3 v6 / Reel 4); when Abik says "Normal UGC 1" with an A-roll + script, build exactly this
metadata:
  type: project
---

**"Normal UGC 1"** = the approved fanout.sh reel style (named by Abik 2026-10-24). Trigger: Abik sends an A-roll + script and says "Normal UGC 1" → run the full pipeline and deliver a preview first, then the package.

Recipe (full detail in `/Users/abiknewar/Work/Claude Editing 2/EDITING_SYSTEM.md` §1–17, plan template `Fanout Reel 4 plan.json`):
1. A-roll uncut to its last frame (convert to 24 fps if needed); transcribe with mlx-whisper; face-measure; BiRefNet matte on MPS.
2. Beats from the script: hook = full-frame A-roll + 2–3-line title stack under the chin (Instrument Serif Italic + SF Pro box line); product phrases = full-frame 9:16 real browser recordings of the matching fanout.sh pages (tools/record_page.py, cursor visible) behind the cutout, pill at 0.385, with stacked-screenshot slides / list scrolls / push-ins for variety; company names = logo pops + tings over the Company Guides recording; claim lines = full-frame title stacks; "senior engineer" line = movie b-roll full screen with the cutout and the stack above the head; CTA captions; full outro loader.
3. No hard zooms (eased push), cutout tilt only on layout cuts, click SFX before every cut, music −30 dB with tail fade, Faded Film grade.
4. Cutout sized per presenter (hair top ≈ 0.50, head ≈ 0.30 of frame).
5. Deliver: preview MP4 → on approval, `Copied_<name>` folder with .prproj (Premiere-exact writer), FCP7 XML + SRT, media flat, README.

Any variation must pass [[hard-rules-no-slop]] first. See [[fanout-reel-editing-system]], [[reel-feedback-first-build]].
