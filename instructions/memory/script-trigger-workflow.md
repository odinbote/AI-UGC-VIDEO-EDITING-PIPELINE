---
name: script-trigger-workflow
description: "Standing rule (2026-10-29): when Abik says \"Script\" and pastes a video reference, decode the reference and write a scroll-stopping fanout.sh script in our style, applying the AVB playbook; what to deliver and what not to do"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8627121c-1143-4576-8491-73057dbba3f5
  modified: 2026-10-29T10:29:58.184Z
---

Trigger: Abik writes **"Script"** and pastes a reference (Instagram / TikTok / YouTube link, or a file). No other instruction needed. Also fires without the word "Script": a pasted reference plus "I want something like this" (2026-11-02, see [[devmonk-explainer-reference]]).

**Why:** Abik set this up 2026-10-29 after the Base44 "Can't is dead" reference produced the "Mapped." script. They want the same loop every time: a reference that stops the scroll → a fanout script that does the same, in fanout's voice, with every playbook rule handled. Earlier iterations taught what they reject: a wordy script, a mirror copy of the reference, and "Senior" as the identity word.

**How to apply:**
1. **Decode the reference first** (no login needed): og meta tags, muted real-time playback with zoomed screenshots every ~3 s, yt-dlp `--get-description` and `--write-auto-subs --sub-langs en-orig --sub-format json3` for the voiceover. Write down: hook type and why it stops the scroll, beat structure with timings, voice (person/tense/temperature), typography and visual grammar, music energy, tagline mechanics.
2. **Intake from [[avb-ad-playbook]]**: one desire (fanout = status, "what senior AI engineers know that I don't"), awareness level, objective, framework(s), sophistication (ed-tech L5 → fanout is "not a course"; never use the word "course" for fanout).
3. **Write similar, not a copy.** Keep what makes the reference work (structure, energy, rhythm, the puncture moment); change the words, the images and the argument to fanout's own. Default voice: **first-person, warm, a presenter telling a friend.** Identity word is **"Engineers"**, not "Senior". **Short and on the point**: 15–40 s, ~3 words/second, every beat does one job. No product in the first 3 s. CTA = "Start at step one. fanout.sh" (no "free", see wording rules below).
4. **Verify every claim on fanout.sh** before using it (20K+ engineers, weekly maintenance, free tracks, 18k req/s Labs instrument, logo strip names).
5. **Deliver in chat by default (2026-11-02, see [[script-delivery-in-chat]]); only as a `.md` when asked.** Former step: Deliver as a `.md` in the repo (next to `Fanout anthem script.md`): keep/change table vs the reference, intake block, timecoded script table with a shot column in Normal UGC 1 grammar (title lines, rose-box keyword in bold, pill captions, recordings, b-roll with cutout, logo pops, white card + loader), a 15-second cut, 2–3 swap-in hooks, a rules-check table, a claims list. Shot column uses existing [[style-normal-ugc-1]] elements only; new graphics need Abik's sign-off ([[hard-rules-no-slop]]).
6. Don't commit unless asked. Don't ask which variant to shoot; offer it in one line at the end.

**Wording rules added 2026-10-30 (Abik, on the "Out of order" script):**
- Never use the word **"free"** in a fanout script, hook or CTA. CTA = "Start at step one. fanout.sh."
- **Easy to understand**: no jargon in the spoken line (no "queue", "requests a second", "inference", "research to inference"). Say "crashed under load", "step by step". The technical instrument can still play on screen.
- "Straight to the point": ~25–30 s, ~80 words, one job per line, no warm-up lines ("here's what nobody says").
- **About engineering** (2026-10-30): the subject is AI engineering, the engineer's own pain (demo works, production falls over, can't explain the system), and the count is "twenty thousand engineers".
- **Use "mapped" sometimes** (2026-10-30): it is fanout's brand word ("Everything an OpenAI L7 knows. Mapped."). Plant it mid-script, pay it off at the close ("It's all mapped. fanout.sh"). No count / social-proof number unless asked; "Updated weekly" became "the map keeps up every week, as the field moves".
