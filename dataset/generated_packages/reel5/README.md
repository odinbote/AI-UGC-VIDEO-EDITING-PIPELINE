# Fanout Reel 5 — "The archive"

Open `Fanout Reel 5.prproj` (Premiere Pro 26.5) or import `Fanout Reel 5.xml` (Final Cut Pro 7 XML; `Fanout Reel 5 captions.srt` carries the captions). All media sits beside them.
Sequence "Fanout Reel 5": 1080x1920, 24 fps, 26.2 s (629 frames). `cut2 aroll.mp4` is your raw file (`cut 2.mp4`, already 1080x1920 at 24 fps), untouched and used uncut to its last frame. Its six built-in jump cuts (frames 104, 223, 294, 317, 379, 468) each sit under a layout cut with a click.

| Frames | Beat | What's on it |
|---|---|---|
| 0–104 | Hook | Full-frame A-roll (scale 128, eased push to 139 on "amazing"), "I came across this" / "amazing archive" / "I keep going back." under the chin; whoosh + button click on the push |
| 104–134 | "It's called Fanout." | Home page recording behind the cutout (scale 130, y 0.845) |
| 134–190 | "The papers that built modern AI," | `/papers` recording, cutout tilted left |
| 190–223 | "in the order to read them." | Two stacked stills sliding up: START HERE row, THEN 2 row |
| 223–294 | "The books, the blogs, the people worth following." | Books list (`/system/resources`) → blogs grid (`/ai/blogs`, slow push) → Who to follow (`/ai/community`, drift); cutout tilted right |
| 294–317 | Title | "Already" / "sorted." |
| 317–379 | "A new paper explained every day." | `/daily` recording → push-in on the November calendar still |
| 379–468 | "And a roadmap that tells you what to learn next." | `/roadmaps` recording (cutout left) → fast scroll of the AI Research roadmap list (cutout right) |
| 468–579 | Title + CTA | "Everything I had in" / "400 tabs." then low captions "Inside" / "fanout.sh" |
| 579–629 | Outro | fanout loader, music fades |

Caption pill at y 0.385 on every screen beat, 0.70 on the CTA.
Mix: dialogue 0 dB, music −30 dB with a 7-frame constant-power tail, clicks −10 dB (4 frames before each cut), UI click −15 dB on the outro, whoosh −15 dB, button clicks −25 dB.
Note: the raw A-roll's own audio peaks over 0 dBFS on "Already" (about 12.4 s); pull that word down if it distorts on export.
Grade: adjustment layer (Faded Film 28 + Noise 5 %) over the dialogue.
Cutout: BiRefNet alpha matte (`cut2_cutout_alpha.mov`, ProRes 4444, 1.2 GB); swap for Object Mask on the raw clip if preferred (identical in/out points).
Page recordings were made on 2026-11-09 from the live site at 763x1356 CSS px, 2x, with the cursor.
The project's bins still list the Silicon Valley / Social Network clips from the reference project; they are not used in this sequence.
After an XML import, re-apply: title box / pill styles, Text Animator in-transitions, the grade.
