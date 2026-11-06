# Fanout — "How Instagram's feed is already there" (explainer piece, our style, first-person, English)

2026-11-02, v1. Second script from the DevMonk reference (https://www.instagram.com/p/DfHUNH8pfR8/, Uber live heatmap, Hindi, 138 s).
The full decode of the reference, the learnings and the shape live in `Fanout script — How ChatGPT answers everyone.md` §1–2; not repeated here.
This one takes the swap-in subject Abik picked: a non-AI product everyone uses, closest to the reference's feel, and the mechanism carries the brand word.

Shape (from the reference): lived scene → impossible fact → "How?" → the obvious way breaks → step → trap → trap → payoff on the viewer's own experience → bridge → CTA.

---

## 1. Intake (playbook)

| | |
|---|---|
| Desire | **Status**: be the engineer who can explain the thing everyone uses, not the one who shrugs "it's cached". |
| Belief to work with | "The feed is a query: get posts from people I follow, sort by time." |
| Pain | The query works for ten users and dies at a million. Engineers can write it and can't explain why the real one is built backwards. |
| Awareness | Problem-unaware (nobody asked why the feed is instant) → problem-aware by 0:08 → solution-aware at the bridge. |
| Objective | Awareness piece with a soft conversion CTA. |
| Framework | EDUCATOR shape from the reference, BRIDGE into the product, CTA. |
| Sophistication | L5. Fanout is not called a course. |
| Psychology | Camouflage (reads as a lesson), gradualization (the obvious query first), mechanization (three decisions: build on post, flip for celebrities, keep it in memory), identification ("you open the app", "you'd never reach the rest"), specificity (one copy per follower, fifty million copies, a few hundred posts). |
| Why this subject | Same *type* as Uber: a product used worldwide, a fact that sounds impossible, explained as steps. Needs no translation. Maps onto fanout's System Design chapters *05 Caching and fast reads*, *11 Realtime, social and feeds*, *18 Engineering case studies*, and two public lessons. And the industry name for step one is fan-out. |

---

## 2. "How Instagram's feed is already there" v1 (2026-11-02, ~40 s, ~138 words)

Bold = rose-box keyword, one per stack. Plain words in speech; lesson names only appear on screen in the recordings.

| Time | Part | Line | Shot (Normal UGC 1) |
|---|---|---|---|
| 0–5 | **HOOK** | "You open Instagram and the feed is just there. Hundreds of accounts, millions of posts, before you **blink**. How?" | B-roll: thumb scrolling a phone, full screen, cutout over it, title stack above the head: *millions of posts* / **before you blink** / *how?* Click SFX. |
| 5–9 | BODY · naive way | "Find everyone you follow, every time you open the app? You'd watch a **spinner**." | Full frame, no screen. Title under the chin: *every time you open* / **a spinner**. |
| 9–15 | BODY · step 1 | "Step one. Build the feed when someone posts, not when you open it. One copy into every follower's **inbox**. Fan-out." | Pill caption: **step one**. System Design curriculum recording with cursor, resting on *11 Realtime, social and feeds*, then the social-graph lesson scrolled to *Handle a very large follower list deliberately*. Cutout overlapping the screen bottom. |
| 15–22 | BODY · trap 1 | "Trap. A celebrity posts. Fifty million followers, fifty million copies. So for them, **flip it**. You pull their posts when you open." | Full frame. Title under the chin: *trap* / *fifty million copies* / **flip it**. |
| 22–29 | BODY · trap 2 | "Second trap. Disk is slow, so the inbox lives **in memory**. Memory is small, so it keeps a few hundred posts. The rest, you never reach." | Pill caption: **second trap**. Recording of the *Caching layers* lesson, cursor on the Redis / Memcached row, slow push-in. |
| 29–33 | BODY · payoff | "Just a feed, no wait. The work was done **before you asked**." | Full frame. Title under the chin: *no wait* / **before you asked**. |
| 33–38 | BODY · product | "Fanout **maps** the real system: the inbox, the flip, the memory. Step by step, with the Instagram case study." | Logo pop on "Fanout". Curriculum fast-scroll (*05 Caching and fast reads* → *11 Realtime, social and feeds* → *18 Engineering case studies*), then the case studies page for one second. Cutout overlapping the screen bottom. |
| 38–40 | **CTA** | "Start at step one. It's all **mapped**. fanout.sh" | Full frame. White card: *Everything.* / **Mapped.** Loader plays out to the last frame. |

"Fan-out" at the end of step one is the real engineering name for the mechanism (fan-out on write). The viewer hears the word, then the logo pop at 33 s pays it off without a joke being made. If it reads as a gimmick in the take, drop the one word "Fan-out." and nothing else changes.

"Mapped" is fanout's own word (homepage: "Everything an OpenAI L7 knows. Mapped."). Planted at the product line, paid off at the close.

**Alternates (same job, pick by ear):**

| Line | Options |
|---|---|
| hook | "Two billion people open Instagram, and the feed is already waiting. Nobody waits. How?" · "Your feed loads before the app finishes opening. Here's why." |
| naive | "Run the query every time you open the app? For two billion people? You'd never see a post." |
| trap 1 | "Trap. One celebrity posts, and fifty million inboxes get a copy. For one photo. So for them, nothing is copied: you fetch their posts when you open." |
| payoff | "The feed isn't fetched. It's waiting." · "Instant isn't fast. It's done early." |
| product | "Fanout maps the real system, step by step: the inbox, the flip, the memory, who follows who, with the Instagram case study." |
| CTA | "Learn how the real ones work. It's all mapped. fanout.sh" · "Everything, mapped. fanout.sh" |

### 2a. Read-aloud, A-roll

One take, straight to camera, run to the last line and hold a beat; the outro loader needs the tail. Pause where the line breaks. Say "trap" like a game, not a warning.

You open Instagram and the feed is just there.
Hundreds of accounts, millions of posts, before you blink. How?

Find everyone you follow, every time you open the app?
You'd watch a spinner.

Step one. Build the feed when someone posts, not when you open it.
One copy into every follower's inbox. Fan-out.

Trap. A celebrity posts.
Fifty million followers, fifty million copies.
So for them, flip it. You pull their posts when you open.

Second trap. Disk is slow, so the inbox lives in memory.
Memory is small, so it keeps a few hundred posts.
The rest, you never reach.

Just a feed, no wait.
The work was done before you asked.

Fanout maps the real system: the inbox, the flip, the memory.
Step by step, with the Instagram case study.

Start at step one. It's all mapped. fanout.sh

### 23-second cut (house standard length, ~72 words)

"You open Instagram and the feed is just there. Millions of posts, before you blink. How? (0–5)
It's built when someone posts, not when you open it: one copy into every follower's inbox. A celebrity would mean fifty million copies, so for them, flip it. (5–14)
And it lives in memory, a few hundred posts, so there's nothing to wait for. (14–18)
Fanout maps the real system, step by step. It's all mapped. fanout.sh (18–23)"

### Swap-in hooks (same job, test as hook takes only)

- "Instagram doesn't load your feed. It's been sitting there waiting for you."
- "The feed is the only thing on your phone that never spins. That's not luck."
- "Every post you see was delivered before you asked for it. Here's how."

---

## 3. Debug pass — what is wrong, in the reference and in ours

**In the reference**

- Same notes as the ChatGPT doc: 138 s, five steps, the energy sags after the second trap, faceless, follow-only CTA.

**In ours (fixed or flagged)**

- *"hundreds of accounts, millions of posts"*: people follow hundreds on average; Instagram has over two billion users and far more than a million posts a day. Safe at this precision. Do not say a per-day number.
- *"Build the feed when someone posts… one copy into every follower's inbox"*: fan-out on write (push model). Fanout's own lesson *Social graph follows and FlockDB* ends on the choice "whether to write feed references when a post appears or collect posts when a reader opens the page" and has a section *Handle a very large follower list deliberately* (fanout.sh/system/archive/social-graph-follows-and-flockdb, verified 2026-11-02). That is our step one and trap one, in their words.
- *"Fifty million followers, fifty million copies"*: the celebrity problem; the fix is the hybrid (pull for high-follower accounts). Standard in every feed design; the number is illustrative and well under the biggest accounts.
- *"the inbox lives in memory… a few hundred posts"*: the per-user feed list kept in a memory store (Redis-style) with a cap. Fanout's lesson *Caching layers* has the Redis / Memcached row (fanout.sh/system/archive/caching-layers, verified 2026-11-02). Instagram's early public architecture used Redis for exactly this; today's feed is ranked by models on top of the same delivery layer. Our lines describe the delivery layer, which is the part an engineer builds; we never say "this is Instagram's exact code".
- *"the Instagram case study"*: fanout.sh/system/case-studies says "findings from Instagram, Stripe, Discord, Amazon and GitLab" (verified 2026-11-02). The recording must land on that line.
- Chapter names *05 Caching and fast reads*, *11 Realtime, social and feeds*, *18 Engineering case studies*: verified on fanout.sh/system 2026-11-02.
- No "free", no "course", no social-proof count, no "Senior". Identity word stays "engineers" (it is not in the spoken lines this time; the subject is the viewer).
- "Fan-out" is the one technical word spoken. It is one word, it is the brand, and the next line explains it by showing it. Flagged above; removable.
- Pace: about 138 words in 40 s, 3.4 words a second. Same length as the chosen ChatGPT script; the 23-second cut is the house-standard version.
- Rules check: hook in 5 s with no product ✔ · one desire (status) ✔ · one keyword per stack ✔ · product first appears at 33 s ✔ · no social-proof number ✔ · CTA without "free" ✔ · no text on face ✔ · existing elements only (titles, pill, recordings, b-roll with cutout, logo pop, white card, loader) ✔ · first-person, warm ✔ · nothing copied from the reference's subject ✔ · English, no local reference ✔.

---

## 4. Post caption

"Send this to the engineer who says it's just a query."
Then the question: "Which one next? ChatGPT answering millions at once, or Maps knowing the road is jammed?"
