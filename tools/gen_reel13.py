#!/usr/bin/env python3
"""
Fanout Reel 13 — "scrolling reels before bed" (third presenter, 37 s take), in Abik's manual-edit look (§22).
No numbered list in this script, so no number cards; one plain cover card on "AI engineering".

    python3 tools/gen_reel13.py          # renders "Fanout Reel 13/Fanout_Reel_13_preview.mp4"
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manual_look as ML, manual_reel as MR
from gen_reel12 import phrase, key_metrics, small_w, P, MAN, COV, COVERS, cover, CLICK

ROOT = "/Users/abiknewar/Work/Claude Editing 2"
REEL = os.path.join(ROOT, "Fanout Reel 13")
SCRATCH = "/private/tmp/claude-501/-Users-abiknewar-Work-Claude-Editing-2/50ae89ed-a5e9-41ec-bd82-530f1b1ca78b/scratchpad/r13"
M = os.path.join(REEL, "Media") + "/"
SVMID = os.path.join(ROOT, "B-roll library", "movies", "Silicon Valley - middle out whiteboard.mp4")

hook_a = phrase([("If", 3), ("you're", 6), ("an", 10)], "engineer", 12, 21, 0.266) + \
         phrase([("scrolling", 21), ("reels", 33)], "before bed", 42, 60, 0.262, justify=True, tall=True)
hook_b = [{"text": w, "style": "small", "x": 0.70, "y": 0.632 + 0.043 * i, "start": sf, "end": 88}
          for i, (w, sf) in enumerate([("this", 71), ("is", 75), ("for", 78), ("you", 82)])]
sz_ai, _, _ = key_metrics("AI products", 175, 0.73, ML.FONT_SEMI.replace('Semibold', 'Medium'))
broll_words = [{"text": "production-grade", "style": "med", "x": 0.145, "y": 0.655, "start": 478, "end": 516},
               {"text": "AI products", "style": "keymed", "x": 0.5, "align": "c", "y": 0.745, "start": 494, "end": 516, "size": sz_ai}]
CUT = lambda x, scale=95: {"cut_scale": scale, "cut_pos": [x, 0.76]}

BEATS = [
    # ---------------- hook: If you're an ENGINEER / scrolling reels BEFORE BED / this is for you
    {"type": "pres", "src": [2, 60], "scale": {"kf": [[0, 100], [14, 114]]}, "pos": {"kf": [[0, [0.5, 0.5]], [14, [0.5, 0.54]]]}, "words": hook_a},
    {"type": "pres", "src": [70, 88], **P(168), "words": hook_b, "whoosh": True},
    # ---------------- I started doing one or two modules on Fanout every day before I hit the bed,
    {"type": "rec", "src": [105, 167], "file": M + "r13_modules.mov", **CUT(0.38), "click": True,
     "pills": [("I started doing", 106, 120), ("one or two modules", 120, 147), ("on Fanout", 147, 167)]},
    {"type": "pres", "src": [168, 214], **P(146), "pills": [("every day", 169, 180), ("before I hit the bed,", 180, 214)]},
    # ---------------- and I'm actually starting to get AI engineering.
    {"type": "pres", "src": [214, 237], **P(159), "pills": [("and I'm actually", 215, 226), ("starting to get", 226, 237)]},
    {"type": "card", "src": [237, 264], "n": None, "col": 5, "cover": cover("75"), "lines": [("AI", "big", 239), ("ENGINEERING", "big", 247)], "click": True},
    # ---------------- A few weeks ago, I couldn't have told you how a chatbot answers from your company's own documents.
    {"type": "pres", "src": [277, 328], **P(130), "pills": [("A few weeks ago,", 278, 300), ("I couldn't have", 300, 314), ("told you", 314, 328)]},
    {"type": "rec", "src": [333, 408], "file": M + "r13_rag.mov", "rec_scale": 98, "rec_pos": [0.5, 0.584], **CUT(0.6, 85), "pill_y": 0.50, "click": True,
     "pills": [("how a chatbot", 334, 351), ("answers from", 351, 369), ("your company's", 369, 385), ("own documents.", 385, 408)]},
    {"type": "pres", "src": [415, 438], **P(166), "pills": [("Now I can", 416, 426), ("explain it.", 426, 438)]},
    # ---------------- And also actually build production-grade AI products all by myself.
    {"type": "broll", "src": [445, 516], "file": SVMID, "in_s": 187.0, "frame_w": 1920, "scale": 182,
     "pos": {"kf": [[6, [0.6, 0.5]], [30, [1.15, 0.5]]]}, "pills": [("And also", 446, 456), ("actually build", 456, 478)], "words": broll_words},
    {"type": "pres", "src": [516, 536], **P(128), "pills": [("all by myself.", 516, 536)]},
    # ---------------- I feel like an AI engineer already, and like I can build on top of this technology very comfortably.
    {"type": "pres", "src": [538, 591], **P(150), "pills": [("I feel like", 539, 552), ("an AI engineer", 552, 570), ("already,", 570, 591)]},
    {"type": "rec", "src": [591, 676], "file": M + "r13_build.mov", **CUT(0.62), "click": True,
     "pills": [("and like I can build", 592, 617), ("on top of", 617, 631), ("this technology", 631, 648), ("very comfortably.", 648, 676)]},
    # ---------------- So tonight, try swapping doomscrolling for one module on Fanout.
    {"type": "pres", "src": [682, 724], **P(128), "pills": [("So tonight,", 683, 698), ("try swapping", 698, 710), ("doomscrolling", 710, 724)]},
    {"type": "pres", "src": [724, 770], **P(166), "pills": [("for one module", 724, 747)], "logo_chest": {"start": 747}, "click": True},
    # ---------------- And you'll feel the difference yourself.
    {"type": "pres", "src": [780, 817], **P(139), "pills": [("And you'll feel", 781, 792), ("the difference", 792, 802), ("yourself.", 802, 817)]},
    # ---------------- Curated, mapped & complete, then the loader
    {"type": "end", "src": [822, 874], "words": [("{ curated }", 822, 840), ("{ mapped }", 840, 860), ("{ complete }", 860, 874)]},
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


PLAN = {"aroll": M + "before bed aroll.mp4", "matte_dir": os.path.join(SCRATCH, "frames"), "covers": COVERS,
        "man": MAN, "loader": MAN + "fanout-loader-alpha-prores4444 (1).mov", "beats": BEATS, "audio": audio}

if __name__ == '__main__':
    json.dump({k: v for k, v in PLAN.items() if k != 'audio'}, open(os.path.join(ROOT, "Fanout Reel 13 look-plan.json"), 'w'), indent=1)
    out = os.path.join(REEL, "Fanout_Reel_13_preview.mp4")
    n, starts = MR.render(PLAN, out, os.path.join(REEL, "preview_work"))
    print(out, n, 'frames', round(n / 24, 2), 's; beat starts', starts)
