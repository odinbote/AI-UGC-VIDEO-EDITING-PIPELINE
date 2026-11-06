# Fanout Reel 4 — "Cheat code for engineers"

Open `Fanout Reel 4.prproj` (Premiere Pro 26.5) or import `Fanout Reel 4.xml` (Final Cut Pro 7 XML; `Fanout Reel 4 captions.srt` carries the captions). All media sits beside them.
Sequence "Fanout Reel 4": 1080x1920, 24 fps, 30.5 s. `Timeline 11 aroll.mp4` is your raw file converted to 24 fps (video re-encoded at CRF 16, audio untouched), used uncut to its last frame.

| Frames | Beat | What's on it |
|---|---|---|
| 0–70 | Hook | Full-frame A-roll (scale 158), "This is basically" / "a cheat code" / "for engineers." under the chin |
| 70–286 | Courses & resources | Full-frame page recordings behind the cutout (scale 120, y 0.81): homepage → System Design → AI Engineering (stacked stills sliding) → Inference → Papers → notes push-in → Resources; pill at y 0.385 |
| 286–329 | Title | "to help you" / "level up" / "your skills." |
| 329–469 | Netflix / Uber / AI eng | Company Guides recording with Netflix and Uber logo pops (+ tings), then AI Engineering curriculum scroll |
| 469–567 | Title | "Fanout helps you" / "go deeper" / "into the concepts", captions "behind what" / "you're building." |
| 567–632 | B-roll | Silicon Valley 582.5 s, Social Network 93 s and 298 s with the cutout on top; "If you want to start" / "thinking like" / "a senior engineer," above the head |
| 632–682 | CTA | Captions "check out" / "Fanout.sh" |
| 682–732 | Outro | fanout loader, music fades |

Mix: dialogue 0 dB, music −30 dB with a 7-frame constant-power tail, clicks −10 dB, UI clicks −15 dB, tings −10 dB.
Grade: adjustment layer (Faded Film 28 + Noise 5 %) over the dialogue.
Cutout: BiRefNet alpha matte (`timeline11_cutout_alpha.mov`); swap for Object Mask on the raw clip if preferred (identical in/out points).
After an XML import, re-apply: title box / pill styles, Text Animator in-transitions, the grade.
