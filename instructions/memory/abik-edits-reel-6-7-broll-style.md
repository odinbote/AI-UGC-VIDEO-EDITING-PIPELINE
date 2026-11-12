---
name: abik-edits-reel-6-7-broll-style
description: What Abik changed in his own edits of Reels 6 and 7 (2026-11-12, `_1.prproj` files) — b-roll usage, new title style, punch-ins, trims; and his instruction to vary b-roll across videos and pick it by the line
metadata:
  type: feedback
---

Abik re-edited my six Reel 6/7 projects in Premiere 2027 (saved as `<name>_1.prproj` beside mine; exports in `/Users/abiknewar/Work/Fanout/AI UGC/New Scripts/`) and on 2026-11-12 told me to learn from them, "mainly the b-roll part": use other b-rolls on other videos ("like I have used something here you need to change on another video"), go with the context, find the lines where b-roll fits, and find movies about Silicon Valley, computer engineering, hacking and coding.

What his edits show (read from the project files and exports):
- **B-roll is literal to the words and cut fast.** 2–3 shots per line, 14–24 frames each. "AI tutorials" → a tutorial playing on a monitor, then on a phone. "software engineers are learning AI" → code on a dark screen, hands typing. "You've shipped real systems" → a terminal on a monitor. "design YouTube" → Gilfoyle at his monitors. "it's not that you don't know the parts" → Dinesh and Gilfoyle staring at a screen.
- **Hooks get b-roll too.** In Reel 6 he cut full-screen b-roll (no cutout) into the middle of each hook, with the title running over it, and used different footage for hooks A, B and C. In the body b-roll usually sits behind the cutout; one line used full-screen b-roll with no presenter.
- **He reframes b-roll** (position/scale per shot) so the subject sits beside the title, not under it.
- **Sources he reached for:** the Silicon Valley and Social Network files plus Artlist stock from `~/Downloads` (hacker screen, typing, tutorial on monitor/phone). He is fine with stock when it matches the line.
- **Two title styles**, with background (green box) and without background (bold white); numbers in [[ask-title-style-every-video]] and `EDITING_SYSTEM.md` §21. The letter-by-letter reveal is the same Text Animator in-transition as before. Some stacks became sequential (line 1 replaced by line 2).
- **Hard punch-ins between phrases on full-frame beats** (scale 114 → 173–214 on the close-up presenter, 140 → 197–226 on the far one), i.e. the "no hard zoom" rule applies inside a phrase, not at phrase boundaries.
- **He removed lines:** "Page three. First equation. Laptop closed." was cut from all three Reel 6 variants, and dead air before "That's the part Fanout shows." was trimmed.

**Why:** the same body b-roll across the three hook variants, and no b-roll at all in Reel 6, read as repetitive; he wants variety across videos and b-roll that illustrates the exact line.

**How to apply:** for every new video, mark the lines that name something visual (a tool, an action, a place, a person type) and give each 2–3 short shots that show exactly that; never reuse a shot another video in the same batch uses; put b-roll in the hook as well; frame the subject clear of the title. His `_1.prproj` files round-trip byte-exact through `tools/build_prproj.py` (`Project(path).save()`), so b-roll can be swapped or added directly in his edited projects. Shots are picked from [[broll-library]] (catalogue, theme index, used-shots ledger). Scope confirmed by Abik on 2026-11-12: apply this to **future videos only**; the six existing variants stay as he exported them, and he did not want any video made that day ("I just want you to learn").

See [[multi-clip-hook-variants]], [[hard-rules-no-slop]], [[style-normal-ugc-1]].
