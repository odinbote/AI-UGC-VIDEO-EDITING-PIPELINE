#!/usr/bin/env python3
"""
Fanout Reel 14 — "RAG. Agents. MCP. Vector databases." (fourth presenter, 49 s take), in Abik's manual-edit look (§22).
The script has no numbered list and no "curated, mapped & complete" line, so: no number cards, no bracket end card.
One plain cover card on "Fanout teaches AI engineering", one b-roll shot, five page recordings.

    python3 tools/gen_reel14.py          # renders "Fanout Reel 14/Fanout_Reel_14_preview.mp4"
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manual_look as ML, manual_reel as MR
from gen_reel12 import phrase, key_metrics, small_w, MAN, COV, COVERS, cover, CLICK, SV

ROOT = "/Users/abiknewar/Work/Claude Editing 2"
REEL = os.path.join(ROOT, "Fanout Reel 14")
SCRATCH = "/private/tmp/claude-501/-Users-abiknewar-Work-Claude-Editing-2/50ae89ed-a5e9-41ec-bd82-530f1b1ca78b/scratchpad/r14"
M = os.path.join(REEL, "Media") + "/"

# this presenter: eyes at 0.387 of the raw frame, top of her hair bun at 0.248, the coin she holds at about (0.47, 0.565)
EYE, COIN = 0.387, 0.565


def P(scale, eyes=0.36):
    """presenter framing: eyes land `eyes` down the frame at any scale"""
    return {"scale": scale, "pos": [0.5, round(eyes + (0.5 - EYE) * scale / 100, 3)]}


def PP(scale, pills, eyes=0.36):
    """framing + chest pills; the pill sits under the coin in her hand so it never covers it"""
    f = P(scale, eyes)
    coin = f["pos"][1] + (COIN - 0.5) * scale / 100
    y = round(max(0.66, coin + 0.075), 3)
    return {**f, "pills": [(t, a, b, y) for t, a, b in pills]}


def key(text, start, end, y, max_px=ML.KEY_MAX_PX):
    size, _, _ = key_metrics(text, max_px)
    return {"text": text, "style": "key", "x": 0.5, "align": "c", "y": y, "start": start, "end": end, "size": size}


# ---- hook: the four words, each one a yellow keyword above her head, cut in as she says it
BASE = 0.236
hook_a = [key("RAG", 3, 18, BASE), key("Agents", 18, 33, BASE), key("MCP", 33, 56, BASE)] + \
         phrase([("Vector", 56)], "databases", 63, 83, BASE, tall=True)
hook_b = phrase([("Every", 87), ("week", 93), ("there's", 98), ("a", 105), ("new", 108)], "AI word", 115, 135, BASE, tall=True)
# ---- b-roll words (SF Pro Medium): "I build" white, "normal / software" yellow
sz_sw, _, _ = key_metrics("software", 175, 0.73, ML.FONT_SEMI.replace('Semibold', 'Medium'))
broll_words = [{"text": "I build", "style": "med", "x": 0.145, "y": 0.645, "start": 236, "end": 269},
               {"text": "normal", "style": "keymed", "x": 0.865, "align": "r", "y": 0.655, "start": 242, "end": 269, "size": 150},
               {"text": "software", "style": "keymed", "x": 0.5, "align": "c", "y": 0.735, "start": 249, "end": 269, "size": sz_sw}]

CUT = lambda x, scale=105: {"cut_scale": scale, "cut_pos": [x, 0.83], "pill_y": 0.515}
# lesson cards on the course overview, punched in: 120% of the full-width size, the card above her head
CARD_L = {"rec_scale": 120, "rec_pos": [0.848, 0.285]}      # left-column card (Retrieval-augmented generation)
CARD_R = {"rec_scale": 120, "rec_pos": [0.152, 0.285]}      # right-column card (The agent loop)

BEATS = [
    # ---------------- hook: RAG. Agents. MCP. Vector databases.
    {"type": "pres", "src": [1, 83], "scale": {"kf": [[0, 100], [14, 112]]}, "pos": {"kf": [[0, [0.5, 0.5]], [14, [0.5, 0.56]]]}, "words": hook_a},
    # ---------------- Every week there's a new AI word,
    {"type": "pres", "src": [86, 135], "scale": 125, "pos": [0.5, 0.60], "words": hook_b, "whoosh": True},
    # ---------------- and I had no idea what this stack even was / or where to start.
    {"type": "pres", "src": [137, 202], **PP(150, [("and I had no idea", 137, 166), ("what this stack", 166, 181), ("even was", 181, 202)])},
    {"type": "pres", "src": [206, 226], **PP(168, [("or where to start.", 206, 226)])},
    # ---------------- I build normal software all day,
    {"type": "broll", "src": [234, 269], "file": SV, "in_s": 32.6, "frame_w": 1920, "scale": 182,
     "pos": {"kf": [[5, [1.31, 0.5]], [24, [-0.12, 0.5]]]}, "words": broll_words},
    # ---------------- and suddenly every meeting is about AI.
    {"type": "pres", "src": [279, 334], **PP(132, [("and suddenly", 279, 292), ("every meeting", 292, 311), ("is about AI.", 311, 334)])},
    # ---------------- Then someone explained it to me, without the jargon.
    {"type": "pres", "src": [339, 372], **PP(158, [("Then someone", 339, 350), ("explained it to me,", 350, 372)])},
    {"type": "pres", "src": [381, 406], **PP(122, [("without the jargon.", 381, 406)])},
    # ---------------- RAG just means looking it up in your documents first, then answering.
    {"type": "rec", "src": [413, 478], "file": M + "r14_rag.mov", **CARD_L, **CUT(0.5), "click": True,
     "pills": [("RAG just means", 413, 431), ("looking it up", 431, 446), ("in your documents", 446, 462), ("first,", 462, 478)]},
    {"type": "pres", "src": [488, 509], **PP(166, [("then answering.", 488, 509)])},
    # ---------------- An agent is just a model that can use your tools, in a loop, until the job is done.
    {"type": "rec", "src": [516, 592], "file": M + "r14_agents.mov", **CARD_R, **CUT(0.5), "click": True,
     "pills": [("An agent is", 516, 534), ("just a model", 534, 550), ("that can use", 550, 571), ("your tools,", 571, 592)]},
    {"type": "pres", "src": [594, 609], **PP(150, [("in a loop,", 594, 609)])},
    {"type": "pres", "src": [613, 642], **PP(128, [("until the job", 613, 628), ("is done.", 628, 642)])},
    # ---------------- Meaning it's not as hard as it sounds. It's a few simple systems.
    {"type": "pres", "src": [648, 693], **PP(160, [("Meaning it's", 648, 662), ("not as hard", 662, 673), ("as it sounds.", 673, 693)])},
    {"type": "pres", "src": [694, 737], **PP(135, [("It's a few", 694, 707), ("simple systems.", 707, 737)])},
    # ---------------- This is how Fanout teaches / AI engineering.
    # (no logo on the chest here: her hands and the coin fill her chest, so the cover card comes in on "Fanout" instead)
    {"type": "pres", "src": [743, 756], **PP(125, [("This is how", 743, 756)])},
    {"type": "card", "src": [756, 803], "n": None, "col": 5, "cover": cover("75"), "lines": [("AI", "big", 777), ("ENGINEERING", "big", 785)], "click": True},
    # ---------------- Every lesson breaks one of these concepts down
    {"type": "rec", "src": [810, 871], "file": M + "r14_vectors.mov", **CUT(0.42), "click": True,
     "pills": [("Every lesson", 810, 826), ("breaks one of", 826, 842), ("these concepts down", 842, 871)]},
    # ---------------- in a way you'll actually understand,
    {"type": "pres", "src": [876, 925], **PP(148, [("in a way you'll", 876, 890), ("actually understand,", 890, 925)])},
    # ---------------- in the order that makes it easy to learn.
    {"type": "rec", "src": [935, 979], "file": M + "r14_order.mov", **CUT(0.58), "click": True,
     "pills": [("in the order", 935, 947), ("that makes it", 947, 960), ("easy to learn.", 960, 979)]},
    # ---------------- It's wild to me how far ahead I already feel, and I'm seeing it in my work.
    {"type": "pres", "src": [985, 1043], **PP(130, [("It's wild to me", 985, 1005), ("how far ahead", 1005, 1022), ("I already feel,", 1022, 1043)])},
    {"type": "pres", "src": [1045, 1081], **PP(160, [("and I'm seeing it", 1045, 1063), ("in my work.", 1063, 1081)])},
    # ---------------- Try a few modules.
    {"type": "rec", "src": [1088, 1115], "file": M + "r14_modules.mov", **CUT(0.42), "click": True,
     "pills": [("Try a few modules.", 1088, 1115)]},
    # ---------------- There's no better way to learn AI engineering.
    {"type": "pres", "src": [1119, 1177], **PP(138, [("There's no better way", 1119, 1138), ("to learn", 1138, 1149), ("AI engineering.", 1149, 1177)])},
    {"type": "loader", "n_frames": 72},
]


def audio(starts, total):
    L = [{"file": MAN + "Every Living Breathing Moment.mp3", "in_s": 19.854, "start": 0, "end": total - 14, "gain_db": -15, "fade_out": 10}]
    punch = starts[1]
    L += [{"file": MAN + "ES_Swooshes, Whoosh, Airy, Light 03 - Epidemic Sound.mp3", "in_s": 2.878, "start": punch - 8, "end": punch + 11, "gain_db": -15},
          {"file": MAN + "ES_Mechanical, Click, Miniature Button, Multiple Pushes - Epidemic Sound.mp3", "in_s": 1.877, "start": punch - 2, "end": punch + 4, "gain_db": -22}]
    for b, st in zip(BEATS, starts):
        if b.get("click"):
            L.append({"file": CLICK, "in_s": 2.419, "start": st - 4, "end": st + 12, "gain_db": -10})
    return L


PLAN = {"aroll": M + "ai words aroll.mp4", "matte_dir": os.path.join(SCRATCH, "frames"), "covers": COVERS,
        "man": MAN, "loader": MAN + "fanout-loader-alpha-prores4444 (1).mov", "beats": BEATS, "audio": audio}

if __name__ == '__main__':
    json.dump({k: v for k, v in PLAN.items() if k != 'audio'}, open(os.path.join(ROOT, "Fanout Reel 14 look-plan.json"), 'w'), indent=1)
    out = os.path.join(REEL, "Fanout_Reel_14_preview.mp4")
    n, starts = MR.render(PLAN, out, os.path.join(REEL, "preview_work"))
    print(out, n, 'frames', round(n / 24, 2), 's; beat starts', starts)
