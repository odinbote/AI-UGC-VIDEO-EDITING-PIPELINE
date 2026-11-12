---
name: multi-clip-hook-variants
description: How to edit a folder of generated UGC clips with hooks A/B/C + body in Normal UGC 1 (stitched A-roll, one clip per timeline item, one project per hook); generator tools/gen_reel67_plans.py
metadata:
  type: project
---

When Abik hands over a generated-clip folder (`hook A|B|C/clip_01_final.mp4`, `body/clip_NN_final.mp4`, `hooks.txt`, a `... hooks A B C + body.xml` cut) and asks to "stitch and edit" it, the working recipe (Reels 6 and 7, 2026-11-11) is:

1. Stitch hook A, B, C + body clips **untrimmed** into one A-roll with the ffmpeg concat *filter* (48 kHz stereo). The concat demuxer with `-r 24` duplicated frame 0 and put video one frame late; always verify each clip's first/last frame against its source.
2. Matte the stitched file once (cutout matches frame for frame).
3. Take trim points from the existing XML in the folder, then check them against audio energy and a transcript. Generated takes can keep talking after the line (system-design hook A had garbled speech after "design."): cut it and tell Abik.
4. One plan/project per hook (`<Reel> - hook X`), all in one `Copied_` folder sharing media. Every clip is its own Aroll item with its own linked audio (handles kept), which is what "fully editable" meant.
5. Every clip join is a jump cut, so each join needs a layout change (full-frame ↔ cutout over a screen or b-roll, or a different screen with a cutout tilt change). Plan beats so no two full-frame beats meet across a join.
6. `tools/gen_reel67_plans.py` holds the beat DSL (clip-local frames → timeline) and both reels' beats; copy it for the next one. Clear `preview_work/vid_*` and `Broll_*` between variant renders (the cache is keyed by start frame only).

Numbers: far/small presenter (Reel 6) full-frame 140, cutout 155 @ y 0.882; close-up presenter (Reel 7) full-frame 114 @ y 0.436, cutout 108 @ y 0.81 with only ±4° tilt (her arms reach the frame edges). Movie b-roll: Silicon Valley at 215 @ y 0.40 keeps the actor's face above the title stack; Social Network needs 365 to clear its letterbox bars. Non-fanout recordings used for problem lines: YouTube search results and arXiv abs/HTML pages (both load in Playwright). Many fanout lesson and explainer pages are Pro-gated below the first screen: keep those recordings near the top or use the curriculum grid instead.

Abik's reaction: after the first three previews, "ok give me the project files and also give me other videos" (no change requests). See [[style-normal-ugc-1]], [[fanout-ugc-generation-pipeline]], [[ugc-clip-gaps]].
