# Fanout Reel 6 — "Learning AI the hard way" (hooks A, B, C)

Three sequences, one per hook, sharing the same body edit and the same media:
`Fanout Reel 6 - hook A.prproj`, `Fanout Reel 6 - hook B.prproj`, `Fanout Reel 6 - hook C.prproj` (Premiere Pro 26.5).
Each also has a Final Cut Pro 7 XML (`... hook X.xml`) and a captions file (`... hook X captions.srt`). All media sits beside them.
Sequences: 1080x1920, 24 fps. hook A: 906 frames (37.8 s), hook B: 910 frames (37.9 s), hook C: 942 frames (39.2 s).

## How the clips are stitched
`learnai aroll.mp4` is hook A, hook B, hook C and the body clips joined end to end, untrimmed (video re-encoded at CRF 14, audio 48 kHz stereo). Every generated clip is its own item on the Aroll track with its own linked audio on Aroll Sound, trimmed to the speech (the same in/out points as your `hooks A B C + body.xml` cut). The handles are still in the file, so you can roll or slip any cut. Every clip join sits under a layout change with a click, so no jump cut shows.
`learnai_cutout_alpha.mov` is the BiRefNet matte of the same file, frame for frame, so cutout items use the same in/out points as the A-roll.

## Beats
| Line | What's on it |
|---|---|
| Hook A / B / C | Full-frame A-roll (scale 140, eased push to 150 with whoosh), title stack under the chin. A: "Most software engineers / are learning AI / the hard way." B: "Watching more / AI tutorials / is exactly why" then captions. C: "Most engineers / learn AI top-down." then "The ones who get it / start from the paper." |
| "A YouTube video on transformers," | YouTube search results recording behind the cutout |
| "a paper you save for later," | arXiv abstract page of Attention Is All You Need, cutout tilted left |
| "and forty tabs you never close." | Fast YouTube results scroll, cutout tilted right |
| "But the video skips the part..." | Full-frame title: "But the video / skips the part / the paper assumes you already know," |
| "so you open the paper anyway." | arXiv HTML paper recording |
| "Page three." | Fast list scroll down the paper (still) |
| "First equation. Laptop closed." | Push-in on Equation 1 (still) |
| "The problem isn't you. It's the order..." | Full-frame titles: "The problem / isn't you." then "It's the order / you're learning it in." |
| "Fanout flips the order." | fanout.sh home recording |
| "Its AI Research archive..." | /papers recording, then the Attention Is All You Need explainer (shown at scale 90, top-aligned), then two stacked stills sliding up |
| "So by page three, you already know..." | Math Decoder recording, then its worked-formula list with a slow push |
| "Next time a paper lands... open it on Fanout.sh first." | Full-frame title "Next time a paper lands / in your team chat," then low captions; fanout loader |

Caption pill at y 0.385 on screen beats, 0.61 on mid full-frame captions, 0.70 on the CTA.
Mix: dialogue 0 dB, music -30 dB with a 7-frame tail, clicks -10 dB four frames before each layout cut, UI click -15 dB on b-roll cuts and the outro, whoosh -15 dB, tings -10 dB.
Grade: adjustment layer (Faded Film 28 + Noise 5 %) over the dialogue.
Page recordings were made on 2026-11-11 from the live sites at 763x1356 CSS px, 2x, with the cursor.
The YouTube recordings show other creators' thumbnails; swap or blur if you prefer. The fanout explainer page is Pro-gated below the fold, so that recording barely scrolls.
After an XML import, re-apply: title box / pill styles, Text Animator in-transitions, the grade.
