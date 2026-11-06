# Fanout — "How ChatGPT answers everyone" (explainer piece, our style, first-person, English)

2026-11-02, v1. Reference: https://www.instagram.com/p/DfHUNH8pfR8/ — DevMonk (@devmonk.preetam), "System Design Hindi",
posted 2026-10-30, 356K likes / 2,248 comments at decode time, 138 s, Hindi voiceover, fully animated (no presenter),
caption "Uber knows instantly where the drivers are. How?" + "send this reel to the friend whose cab never gets accepted."

Brief from Abik: same *type* of topic (a product everyone uses, explained as engineering steps), not the same concept or script,
short, in English, for a global audience.

---

## 1. The reference, broken into hook / body / CTA

Voiceover transcribed and translated from the audio (faster-whisper, Hindi → English), on-screen elements from a frame every 2 s.

| Part | Time | What he says (condensed) | What is on screen | Job |
|---|---|---|---|---|
| **HOOK** | 0–11 | "The concert just ended. Thousands of people are booking a cab at once, and the drivers are scattered across the city. Uber knows instantly how many drivers are where. How?" | Real concert clip (credited), then a 3D crowd with "BOOKINGS: 3,000", a stadium on a map with cab icons, a city grid, then one word: **KAISE?** (How?) | A scene the viewer has lived, a fact that sounds impossible, a one-word question. No intro, no name. |
| **BODY 0 · authority** | 11–17 | "This exact question was asked in Uber's system design interview: how would you build a live heatmap of drivers?" | "Uber" wordmark, "SYSTEM DESIGN INTERVIEW" pill, the question in a card. | Authority and stakes in one line: this is a real interview question. |
| **BODY 1 · naive way fails** | 17–24 | "Count every driver every time? Thousands of drivers, new location every few seconds. The map will always be behind." | Driver dots on a grid, a counter "GINTI: 375 → 1,483 → 2,359" racing, red stamp **MAP PEECHE** (map behind). | Gradualization: start where the viewer would start, show it break. |
| **BODY 2 · step 1** | 24–42 | "Step 1. The driver's app sends driver ID, lat, long and time every few seconds. After the concert these updates jump 10×. So first they go into a queue, like Kafka, so nothing is lost in the spike." | Numbered plan (1 location, 2 cell, 3 counter), 3D car with location rings, phone → JSON card, a queue diagram with phones feeding a server, "10× SPIKE", "0 updates lost". | Mechanism, one piece at a time. Named tool after the plain words. |
| **BODY 3 · step 2** | 42–50 | "Step 2. Cut the map into small cells. From lat/long you know which cell the driver is in." | Grid over the map, "lat, lng → cell id", "CELL (5,4)". | Mechanism. |
| **BODY 4 · step 3** | 50–62 | "Step 3. Every cell has a counter, in RAM, like Redis, answering in milliseconds. Driver moves cell: old cell −1, new cell +1. Just two numbers change." | Grid of counts, red "RAM · REDIS" card, −1 / +1 animation. | Mechanism. |
| **BODY 5 · trap 1** | 62–76 | "But: trap. A driver is stopped at a signal and sends his location 10 times from the same cell. +1 every time, one driver becomes ten. So remember each driver's last cell; same cell, change nothing." | One cell, car at a traffic light, **COUNT: 2 → 10 → 1**, "D42 → (6,4)", "SAME → SKIP". | Retention twist: the viewer thought the system was done. Reward for staying. |
| **BODY 6 · trap 2** | 76–88 | "Second trap. Driver's network drops, updates stop, but he is still in the count. So put an expiry on every driver: no update for 30 s, he drops out on his own." | Car with a broken-signal icon, "NETWORK GAYA", a 30 s → 0 s expiry ring. | Second twist, same shape. |
| **BODY 7 · step 4** | 88–99 | "Now colour the count. More drivers, darker. Fewer, lighter. Outside the stadium everything is light: big crowd, few drivers. This is the live heatmap." | Count grid turns into green/orange/red cells, stadium marker, "Live heatmap" card. | Payoff of the build. |
| **BODY 8 · step 5** | 99–118 | "A whole country's cells don't fit on one machine, so split them by city across servers: DB sharding. And real Uber doesn't use squares, it uses hexagons, H3: six neighbours at the same distance, so counts are fair on every side." | Three city grids → Server 1/2/3, "DB Sharding" card, squares vs hexagons, "H3 · Uber's open-source grid". | Depth for the engineers; a named real thing. |
| **BODY 9 · payoff** | 118–130 | "The same cells work for booking too: the system finds the nearest driver in your cell and the neighbouring cells. And the cell with more bookings than drivers is where you see surge pricing." | Hex grid with "TUM" (you) in the middle, neighbours light up, a red hex with "surge" and a ride-app price card. | Ties the whole build to something the viewer has personally paid for. |
| **CTA** | 130–138 | "Understand engineering like this. Follow. And send this reel to the friend whose cab never gets accepted." | Phone mock "Finding your ride… No driver accepted", "FOLLOW @devmonk.preetam", "Dost ko bhejo ➤". | Follow + a share line with a joke in it. |

**Shape:** scene → impossible fact → "How?" → real interview question → the naive way breaks → step 1 → step 2 → step 3 → trap → trap → step 4 (the thing you see) → step 5 (depth) → "this is why *you* pay surge" → follow + send-to-a-friend.
No presenter, no face. Dark navy blueprint grid, monospace labels, one accent colour per idea (red = trap, green = fix). Every beat has a label top-left ("STEP 1 · LOCATION", "TRAP 1 · …"). Voice: second person, calm teacher, short sentences, "Trap!" said like a game.

---

## 2. Learnings

**Used by the reference (we take these):**

1. The hook is a *scene* the viewer has lived (concert ends, everyone books), then an impossible-sounding fact, then one word: "How?" No product, no intro.
2. "This was asked in Uber's interview" gives the explanation stakes in four seconds.
3. Show the obvious approach and break it before the real one. The viewer feels smart for seeing why.
4. Numbered steps, one job each, plain words first, the named tool after ("in RAM, like Redis").
5. **Traps.** Two "you thought it was done" twists in the middle keep the back half alive. Each trap is a bug the viewer could have shipped.
6. The payoff lands on something the viewer has personally paid for (surge). That is the share trigger.
7. The share line has a joke in it ("the friend whose cab never gets accepted").
8. Labels never cover the subject; the layout is calm and typographic even though it is animated.

**Not used by the reference (also learnings, for a brand piece):**

9. 138 s and five steps. Ours is one idea, three decisions, under 40 s. The depth (hexagons, sharding) is what the product is for, not what the reel is for.
10. No product, follow-only CTA. Ours bridges to fanout *after* the payoff so the explanation still stands on its own.
11. Fully animated blueprint diagrams. Not our grammar. Same jobs here: title stacks for the step words, the rose box for the key word, real recordings of the fanout lessons and labs that teach the exact mechanism, b-roll with the cutout for the scene.
12. Second person. Ours stays first person, a presenter telling a friend.

---

## 3. Intake (playbook)

| | |
|---|---|
| Desire | **Status**: be the engineer who can explain how the real system works, not the one who says "it's just an API call". |
| Belief to work with | "ChatGPT is a model behind an API. The hard part is the model." |
| Pain | Demo answers one person; production has to answer a city. Engineers can build the demo and can't explain the rest. |
| Awareness | Problem-unaware for most (they never asked the question) → problem-aware by 0:10 → solution-aware at the bridge. |
| Objective | Awareness piece with a soft conversion CTA. |
| Framework | EDUCATOR shape from the reference (scene → how? → naive → steps → traps → payoff), BRIDGE into the product, CTA. |
| Sophistication | L5. Fanout is not called a course. |
| Psychology | Camouflage (reads as a lesson), gradualization (the obvious way first), mechanization (three named decisions), identification ("yours still answers instantly", "demo vs product"), specificity (one word at a time, the seat, the chip's memory). |
| Why this subject | Same *type* as Uber: a product everyone on earth uses, a fact that sounds impossible, explained as steps. It is AI engineering (fanout's subject), it maps one-to-one onto fanout's Inference Engineering lessons and two labs, and it is global: ChatGPT needs no translation. |

---

## 4. "How ChatGPT answers everyone" v1 (2026-11-02, ~39 s, ~130 words)

Bold = rose-box keyword, one per stack. Plain words in speech; the technical names only appear on screen in the recordings.

| Time | Part | Line | Shot (Normal UGC 1) |
|---|---|---|---|
| 0–5 | **HOOK** | "Right now, millions of people are typing into ChatGPT. And yours still answers **instantly**. How?" | B-roll: crowd / people on phones, full screen, cutout over it, title stack above the head: *millions typing* / **instantly** / *how?* Click SFX. |
| 5–8 | BODY · naive way | "One person, then the next? You'd wait for **hours**." | Full frame, no screen. Title under the chin: *one at a time* / **hours long**. |
| 8–13 | BODY · step 1 | "Step one. One word at a time, for you, for me, for everyone, in the **same** trip." | Pill caption: **step one**. Then the Inference Engineering curriculum recording with cursor, slow scroll resting on *Continuous Batching*. Cutout overlapping the screen bottom. |
| 13–20 | BODY · trap 1 | "Trap. Mine is three words, yours is an essay. Nobody waits for the longest. A **seat** opens, the next person takes it, mid sentence." | Full frame. Title under the chin: *trap* / **the seat** / *mid sentence*. |
| 20–27 | BODY · trap 2 | "Second trap. Every conversation keeps its **memory** on the chip. Too many, and the whole thing falls over. So it knows its limit, before it breaks." | Pill caption: **second trap**. Labs recording: *Inference Memory and KV Cache* lab, cursor pushing the slider up until the memory bar fills. Push-in on the bar. |
| 27–30 | BODY · payoff | "The demo answers one person. The product answers a **city**." | Full frame. Title under the chin: *a demo answers one* / **a product answers a city**. |
| 30–37 | BODY · product | "Fanout **maps** the real system: the memory, the seats, the breaking point. Step by step, with labs where you break it yourself." | Logo pop on "Fanout". Curriculum fast-scroll (*Build a KV Cache* → *Continuous Batching* → *Find Saturation, SLO Failure & OOM Boundaries*), then the Labs grid recording for one second. Cutout overlapping the screen bottom. |
| 37–39 | **CTA** | "Start at step one. It's all **mapped**. fanout.sh" | Full frame. White card: *Everything.* / **Mapped.** Loader plays out to the last frame. |

"Mapped" is fanout's own word (homepage: "Everything an OpenAI L7 knows. Mapped."). Planted at the product line, paid off at the close.

The reference's "Trap!" device is kept as a *spoken* beat and a title word, not a graphic. If Abik wants a red "trap" marker on screen, that is a new element and needs sign-off ([[hard-rules-no-slop]]). The restrained version is the word *trap* in Instrument Serif at the top of the stack.

**Alternates (same job, pick by ear):**

| Line | Options |
|---|---|
| hook | "Millions of people hit send on ChatGPT in the same second. Yours still answers right away. How?" · "ChatGPT has more users than most countries have people. And it never makes you wait in line. How?" |
| payoff | "The demo is the model. The product is everything around it." · "Anyone can call the model. Few can make it answer a city." |
| product | "Fanout maps the whole thing for engineers: the memory, the seats, the breaking point, in order, with labs where you push it until it falls over." |
| CTA | "Learn how the real ones work. It's all mapped. fanout.sh" · "Everything, mapped. fanout.sh" |

## 4a. Read-aloud, A-roll (chosen 2026-11-02: the 39 s script)

One take, straight to camera, run to the last line and hold a beat; the outro loader needs the tail. Pause where the line breaks. Say "trap" like a game, not a warning.

Right now, millions of people are typing into ChatGPT.
And yours still answers instantly. How?

One person, then the next? You'd wait for hours.

Step one. One word at a time.
For you, for me, for everyone, in the same trip.

Trap. Mine is three words, yours is an essay.
Nobody waits for the longest.
A seat opens, the next person takes it, mid sentence.

Second trap. Every conversation keeps its memory on the chip.
Too many, and the whole thing falls over.
So it knows its limit, before it breaks.

The demo answers one person.
The product answers a city.

Fanout maps the real system: the memory, the seats, the breaking point.
Step by step, with labs where you break it yourself.

Start at step one. It's all mapped. fanout.sh

Swap "the chip" for "the graphics card" if that is easier to say. Everything else stays as written; the title stacks and the pill captions are cut from these exact words.

---

### 23-second cut (house standard length, 75 words)

"Millions of people are typing into ChatGPT right now, and yours still answers instantly. How? (0–5)
It writes one word for you, one for me, one for everyone, in the same trip. When a seat opens, the next person takes it, mid sentence. (5–13)
And every conversation keeps its memory on the chip, so the system knows its exact limit before it breaks. (13–18)
Fanout maps how the real systems work, step by step. It's all mapped. fanout.sh (18–23)"

### Swap-in hooks (same job, test as hook takes only)

- "ChatGPT doesn't answer you first. It answers everyone at once. Here's how."
- "If ChatGPT answered one person at a time, you'd be waiting until tomorrow."
- "The model is the easy part. Here's what actually answers a million people."

### Swap-in subjects (same shape, if Abik wants a non-AI product like the reference)

Both map onto fanout's System Design chapters (verified 2026-11-02: *05 Caching and fast reads*, *11 Realtime, social and feeds*, *12 Geo, matching and recs*). Same beat structure: scene → how? → naive way breaks → three decisions → trap → payoff → bridge.

| Subject | Hook | The three decisions | Note |
|---|---|---|---|
| Instagram feed | "You open Instagram and the feed is already there. Thousands of friends, millions of posts, before you finish blinking. How?" | Don't build the feed when you open the app; build it the moment a friend posts, and drop a copy into every follower's inbox. Trap: a celebrity with 50 million followers would mean 50 million copies per post, so for them, flip it: fetch on read. Keep the inbox in memory, not on disk. | The industry name for "copy into every follower's inbox" is **fan-out**. The brand word is in the subject. Strong, but check it doesn't read as a pun. |
| Google Maps traffic | "Google Maps knows the road is jammed before you reach it. Nobody reported it. How?" | Every phone with Maps open is a sensor sending speed and position. Cut the roads into segments; average the speeds per segment. Trap: a parked phone or a bus stop looks like a jam, so weight by movement and drop the outliers. | Closest to the reference's geo subject. |

---

## 5. Debug pass — what is wrong, in the reference and in ours

**In the reference**

- 138 s is long for a reel; the depth beats (sharding, H3) are for the already-convinced. Ours stops at three decisions.
- Two traps in a row then two more steps: the energy sags between 88 and 118 s. Ours puts the payoff right after the second trap.
- Animated diagrams throughout; nobody to trust. Works for a faceless channel, not for a presenter brand.
- Follow-only CTA. Fine for a creator.

**In ours (fixed or flagged)**

- *"millions of people are typing into ChatGPT right now"*: OpenAI has publicly reported hundreds of millions of weekly users; "millions right now" is the safe form. Do not say a per-second number.
- *"one word at a time"*: the model generates one token per step; "word" is the plain-words form and is the house rule (no jargon in speech). Correct enough for a viewer, and the lesson title on screen (*Continuous Batching*) carries the precise term.
- *"a seat opens"*: continuous batching, a finished sequence's slot is refilled by a waiting request mid-generation. Lesson *Continuous Batching* is on fanout.sh/inference-eng (verified 2026-11-02).
- *"keeps its memory on the chip"*: the KV cache lives in GPU memory; past the limit the server hits out-of-memory. Lessons *Build a KV Cache* and *Find Saturation, SLO Failure & OOM Boundaries*, lab *Inference Memory and KV Cache* (fanout.sh/labs, verified 2026-11-02). "Chip" is the plain word for GPU; if the presenter prefers "graphics card", swap it.
- *"labs where you break it yourself"*: the Labs page lists *Fanout Scale* and *Inference Memory and KV Cache* (verified 2026-11-02); the homepage Labs instrument was verified 2026-10-29. The recording must show a real slider being pushed, with the cursor.
- *"the demo answers one person, the product answers a city"*: fanout's own inference page says the track is for engineers "moving from model demos to production traffic" (verified 2026-11-02). It is their framing, not ours.
- No "free", no "course", no social-proof count, no "Senior". Identity word is "engineers".
- Pace: about 130 words in 39 s, 3.3 words a second. Longer than the 25–30 s house standard because the ask was an explanation; the 23-second cut below is the standard-length version.
- Rules check: hook in 5 s with no product ✔ · one desire (status) ✔ · one keyword per stack ✔ · product first appears at 32 s ✔ · no number in speech ✔ · CTA without "free" ✔ · no text on face ✔ · existing elements only (titles, pill, recordings, b-roll with cutout, logo pop, white card, loader) ✔ · first-person, warm ✔ · nothing copied from the reference's subject (no Uber, no drivers, no cells, no heatmap) ✔ · English, no local reference ✔.

---

## 6. Post caption (the reference gets its comments from the caption)

"Send this to the engineer who says it's just an API call."
Then a question: "Which app should I open up next? Instagram feed, Maps traffic, or Spotify shuffle?"

---

## 7. Reference assets (session scratchpad, not in repo)

Video, audio, Hindi transcript, English translation and three frame sheets for the reference live in the session scratchpad under `ref/`. Re-decode with yt-dlp + faster-whisper (pass the WAV as a numpy array; the installed `av` is too new for faster-whisper's file loader) if needed; the post is public.
