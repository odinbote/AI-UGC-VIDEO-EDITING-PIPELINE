# Fanout Reel 3 — "Cheat code" (packaged like AI UGC 1)

Open `Fanout Reel 3.prproj` (Premiere Pro 26.5). All media sits beside it, same as the Copied_ project you gave me.
`Fanout Reel 3 (uncompressed).xml` is the same project as plain XML for inspection; Premiere opens the .prproj.

Sequence "Fanout Reel 3": 1080x1920, 24 fps, 19.8 s (v6, approved). Raw A-roll used uncut to its last frame (sequence time = source time).

| Frames | Beat | What's on it |
|---|---|---|
| 0–41 | Hook | Full-frame A-roll (scale 158), "This is basically" / "a cheat code" under the chin |
| 41–88 | Push | Eased scale 158→174 (no hard cut), captions "for becoming" / "a better engineer." |
| 88–277 | Product layouts | Full-frame browser recordings (rec_home / rec_lab_drag / rec_company_guides, 1526x2712 at scale 70.8) with cursor, then two stacked AI Research screenshots sliding up and the curriculum list fast-scroll on the white matte; caption pill at y 0.385; cutout (timeline1_cutout_alpha.mov, scale 153, y 0.837; tilted on the guides/AI beats and the list beat) |
| 277–314 | Title beat | Full-frame A-roll, "all in" / "one place." |
| 314–373 | B-roll | Silicon Valley 582.5 s, Social Network 93 s and 298 s full screen with the cutout on top, title stack above the head: "If you want to start" / "thinking like" / "a senior engineer," |
| 373–426 | CTA | Full-frame A-roll, captions "check out" / "Fanout.sh" |
| 426–476 | Outro | fanout loader on the matte, music fades out |

Mix: dialogue 0 dB (Essential Sound Dialogue), music −30 dB with a 7-frame constant-power tail, mechanical clicks −10 dB, UI clicks −15 dB, whooshes −15/−17 dB, button click −25 dB.
Grade: adjustment layer (Faded Film 28 + Noise 5 %) over the dialogue.

Notes for Premiere:
- The cutout clips use the BiRefNet alpha matte. To use Object Mask instead, drop `Timeline 1 aroll.mp4` on V7 in place of them (in/out points are identical) and track.
- `Timeline 1 aroll.mp4` is your raw file with audio converted to 48 kHz stereo (video untouched).
- The old A-roll/screenshot media entries were re-pointed to the new files, so Premiere may show "media pending" briefly on first open.

## Final Cut Pro 7 XML (`Fanout Reel 3.xml`)

Import with File > Import in Premiere (or DaVinci). Same timeline as the project: every cut, in/out point, scale / position / rotation with keyframes, the colour matte, audio clips with gain and the music fade, A-roll video+audio linked. Media paths point at this folder.

Not expressible in this format, so re-apply after import: the Text Animator in-transitions on titles, the rose keyword box and green caption pill (titles and captions arrive as plain text generators with the right font, size and position), Essential Sound tags, and the adjustment-layer grade (Faded Film 28 + Noise 5 %). `Fanout Reel 3 captions.srt` carries the 16 captions with exact timing for File > Import as a caption track.
