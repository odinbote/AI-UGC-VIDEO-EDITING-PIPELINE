# Fanout Reel 7 — "Stop winging your system design" (hooks A, B, C)

Three sequences, one per hook, sharing the same body edit and the same media:
`Fanout Reel 7 - hook A.prproj`, `Fanout Reel 7 - hook B.prproj`, `Fanout Reel 7 - hook C.prproj` (Premiere Pro 26.5).
Each also has a Final Cut Pro 7 XML (`... hook X.xml`) and a captions file (`... hook X captions.srt`). All media sits beside them.
Sequences: 1080x1920, 24 fps. hook A: 909 frames (37.9 s), hook B: 941 frames (39.2 s), hook C: 948 frames (39.5 s).

## How the clips are stitched
`sysdesign aroll.mp4` is hook A, hook B, hook C and the body clips joined end to end, untrimmed (video re-encoded at CRF 14, audio 48 kHz stereo). Every generated clip is its own item on the Aroll track with its own linked audio on Aroll Sound, trimmed to the speech (the same in/out points as your `hooks A B C + body.xml` cut). The handles are still in the file, so you can roll or slip any cut. Every clip join sits under a layout change with a click, so no jump cut shows.
`sysdesign_cutout_alpha.mov` is the BiRefNet matte of the same file, frame for frame, so cutout items use the same in/out points as the A-roll.

## Beats
| Line | What's on it |
|---|---|
| Hook A / B / C | Full-frame A-roll (scale 114 at y 0.436, eased push with whoosh), title stack under the chin. A: "Stop winging / your system design." B: "You don't fail / system design rounds / because you don't know Kafka." C: "Junior engineers / draw boxes." then "Senior engineers / explain why / the boxes break." |
| "You've shipped real systems for years." | Silicon Valley 582.5 s then Social Network 93 s, full screen with the cutout; title above the head |
| "Then someone says design YouTube" | Social Network 298 s (equation on the window) with the cutout; title "Then someone says / design YouTube" |
| "and your mind goes blank. But it's not..." | Full-frame title "and your mind / goes blank." then mid captions |
| "You know Kafka, caches, load balancers." | Three quick recordings of the System Design curriculum at the Kafka-style log, caching and load-balancer lessons |
| "You've just never watched them work together under load. So you draw boxes and hope." | Full-frame titles, two blocks |
| "And the interviewer can tell the second they ask," | Silicon Valley 583.98 s and 586.66 s with the cutout; title above the head |
| "what happens when this fails?" | Full-frame title |
| "That's the part Fanout shows." | fanout.sh home recording |
| "...systems at Netflix and Uber actually work," | Company Guides recording with Netflix and Uber logo pops + tings |
| "piece by piece, in interactive animations." | Two stacked stills of the video-platform lesson, then the Latency Numbers lab with the slider being dragged |
| "You've built systems. Now you can explain them." | Full-frame title |
| "If your design round is this month, check out Fanout.sh before it." | System Design roadmap recording, then full-frame low captions; fanout loader |

Caption pill at y 0.385 on screen beats, 0.61 on mid full-frame captions, 0.70 on the CTA.
Mix: dialogue 0 dB, music -30 dB with a 7-frame tail, clicks -10 dB four frames before each layout cut, UI click -15 dB on b-roll cuts and the outro, whoosh -15 dB, tings -10 dB.
Grade: adjustment layer (Faded Film 28 + Noise 5 %) over the dialogue.
Page recordings were made on 2026-11-11 from the live sites at 763x1356 CSS px, 2x, with the cursor.
Hook A's source clip has garbled extra speech after "design." (the generated take keeps talking), so the hook is trimmed to 2.3 s; the rest of that clip is still there if you roll the edit out. Silicon Valley is punched in to 215 and raised, Social Network to 365 to clear its letterbox bars.
After an XML import, re-apply: title box / pill styles, Text Animator in-transitions, the grade.
