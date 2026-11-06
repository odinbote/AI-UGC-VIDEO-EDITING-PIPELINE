---
name: abik-editor-profile
description: "Who Abik is — Premiere Pro 26.5 editor making vertical UGC reels for fanout.sh; how they like to work with Claude (preview first, named styles, package deliverables)"
metadata:
  node_type: memory
  type: user
  originSessionId: 50ae89ed-a5e9-41ec-bd82-530f1b1ca78b
  modified: 2026-10-24T18:19:44.625Z
---

Abik Newar edits short vertical UGC reels (1080x1920, 24 fps) in Adobe Premiere Pro 26.5 for fanout.sh (AI-engineering learning platform; pages: /, /system/overview, /system/company-guides, /ai-engineering/overview, /inference-eng, /papers, /roadmap, /labs/*). Uses Epidemic Sound SFX/music, Instrument Serif Italic + SF Pro type, AI object-mask cutouts.

How they work with Claude:
- Sends an A-roll + script (sometimes pre-cut: never recut it) and the style name. Expects a **preview MP4 first**, approves or lists changes, then gets the package.
- Package = `Copied_<name>` folder with `.prproj` (opens in Premiere), FCP7 `.xml` + captions `.srt` (imports), all media flat, README. Both deliverables confirmed working.
- Gives feedback as short numbered lists; values: text never on the face, captions never on screens, real page recordings not static scrolls, no visible jump cuts, music quiet, outro complete, b-roll with the cutout on top.
- Named their house style **"Normal UGC 1"** and wants more named styles built from the UGC reference study.
- Machine: Apple Silicon Mac, Python 3.14, no ffmpeg on PATH (use imageio_ffmpeg / PyAV), MPS for BiRefNet, Chrome + Playwright for captures.

See [[style-normal-ugc-1]], [[fanout-reel-editing-system]], [[reel-feedback-first-build]], [[ugc-reference-styles]], [[session-2026-10-24-index]].
