#!/usr/bin/env python3
"""
Fanout Reel 12 — "sauce for engineers", full script, third presenter, in Abik's manual-edit look (§22).
Beat for beat after his own edit (reference/abik manual edit 2026-11-13/timeline_dump.txt), with this take's timings.

    python3 tools/gen_reel12.py          # renders "Fanout Reel 12/Fanout_Reel_12_preview.mp4"
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manual_look as ML, manual_reel as MR
from PIL import ImageFont

ROOT = "/Users/abiknewar/Work/Claude Editing 2"
REEL = os.path.join(ROOT, "Fanout Reel 12")
SCRATCH = "/private/tmp/claude-501/-Users-abiknewar-Work-Claude-Editing-2/50ae89ed-a5e9-41ec-bd82-530f1b1ca78b/scratchpad/r12"
MAN = "/Users/abiknewar/Work/Fanout/AI Trianing UGC Prject Filea/Copied_AI UGC Manual Edits/"
R9 = os.path.join(ROOT, "Fanout Reel 9", "Media") + "/"
COV = os.path.join(ROOT, "reference", "abik manual edit 2026-11-13", "covers")
cover = lambda n: os.path.join(COV, f"Group 13213167{n}.png")
COVERS = [cover(n) for n in ("66", "47", "48", "49", "75")]   # system design, math, AI research, inference, AI engineering
SV = os.path.join(ROOT, "Fanout Reel 7", "Copied_Fanout Reel 7", "vidssave.com Silicon Valley _ Season 1-5 _ Dinesh and Gilfoyle 1080P.mp4")

# presenter framing: eyes land about 0.36 down the frame at any scale (raw eyes at 0.446)
P = lambda scale: {"scale": scale, "pos": [0.5, round(0.36 + 0.054 * scale / 100, 3)]}


def small_w(text, path=ML.FONT_SEMI):
    return ML.text_width(text, ImageFont.truetype(path, ML.SMALL_PX))


def key_metrics(text, max_px=ML.KEY_MAX_PX, fit_w=ML.KEY_W, path=ML.FONT_BOLD):
    size = ML.fit_size(text, path, max_px, fit_w * ML.W)
    return size, ML.text_width(text, ImageFont.truetype(path, size)) / ML.W, 0.52 * size / ML.H


def phrase(smalls, key, key_sf, end_sf, base_y, justify=False, tall=False):
    """tall: the keyword has ascenders (b, d, f, h, k, l, t) under the small words, so the small row sits above them"""
    out = []; size, kw, xh = key_metrics(key); left = 0.5 - kw / 2
    out.append({"text": key, "style": "key", "x": 0.5, "align": "c", "y": base_y, "start": key_sf, "end": end_sf, "size": size})
    sy = base_y - (0.75 * size / ML.H + 0.006 if tall else xh + 0.014)
    if justify:
        out.append({"text": smalls[0][0], "style": "small", "x": left + 0.01, "y": sy, "start": smalls[0][1], "end": end_sf})
        rest = ' '.join(w for w, _ in smalls[1:]); x = 0.5 + kw / 2 - 0.01 - small_w(rest) / ML.W
        for w, sf in smalls[1:]:
            out.append({"text": w, "style": "small", "x": x, "y": sy, "start": sf, "end": end_sf}); x += small_w(w + ' ') / ML.W
    else:
        x = left
        for w, sf in smalls:
            out.append({"text": w, "style": "small", "x": x, "y": sy, "start": sf, "end": end_sf}); x += small_w(w + ' ') / ML.W
    return out


# ---- hook words
hook_a = phrase([("I'm", 3), ("about", 6), ("to", 10)], "reveal", 14, 22, 0.266) + \
         phrase([("some", 22), ("sauce", 29), ("for", 39)], "engineers", 45, 55, 0.248, justify=True)
hook_b = [{"text": w, "style": "small", "x": 0.70, "y": 0.632 + 0.043 * i, "start": sf, "end": 82}
          for i, (w, sf) in enumerate([("that's", 55), ("not", 65), ("out", 69), ("there", 73)])]
ring_words = []
x = 0.93 - small_w("to actually") / ML.W
for w, sf in [("to", 121), ("actually", 129)]:
    ring_words.append({"text": w, "style": "small", "x": x, "y": 0.222, "start": sf, "end": 136}); x += small_w(w + ' ') / ML.W
size_s, kw_s, xh_s = key_metrics("senior", 330, 0.76); size_e, _, _ = key_metrics("engineer", 330, 0.76)
ring_words += [{"text": "senior", "style": "key", "x": 0.5, "align": "c", "y": 0.245, "start": 150, "end": 169, "size": size_s, "behind": True},
               {"text": "engineer", "style": "key", "x": 0.5, "align": "c", "y": 0.318, "start": 156, "end": 169, "size": size_e, "behind": True}]
x = 0.5 - kw_s / 2 + 0.11
for w, sf in [("become", 136), ("a", 144)]:
    ring_words.append({"text": w, "style": "small", "x": x, "y": 0.245 - xh_s - 0.014, "start": sf, "end": 169, "behind": True}); x += small_w(w + ' ') / ML.W
# ---- b-roll words (SF Pro Medium): "a few" white, "senior / engineers" yellow
sz_eng, _, _ = key_metrics("engineers", 175, 0.73, ML.FONT_SEMI.replace('Semibold', 'Medium'))
broll_words = [{"text": "a few", "style": "med", "x": 0.145, "y": 0.645, "start": 258, "end": 288},
               {"text": "senior", "style": "keymed", "x": 0.865, "align": "r", "y": 0.655, "start": 263, "end": 288, "size": 150},
               {"text": "engineers", "style": "keymed", "x": 0.5, "align": "c", "y": 0.735, "start": 271, "end": 288, "size": sz_eng}]

CUT = lambda x, scale=95: {"cut_scale": scale, "cut_pos": [x, 0.76]}
BEATS = [
    # ---------------- hook
    {"type": "pres", "src": [2, 55], "scale": {"kf": [[0, 100], [14, 114]]}, "pos": {"kf": [[0, [0.5, 0.5]], [14, [0.5, 0.54]]]}, "words": hook_a},
    {"type": "pres", "src": [55, 82], **P(168), "words": hook_b},
    {"type": "pres", "src": [95, 169], "scale": 120, "pos": [0.5, 0.582], "ring": {"start": 95, "frames": 32}, "words": ring_words},
    # ---------------- I searched YouTube, I read a bunch of blogs, I even asked a few senior engineers
    {"type": "rec", "src": [177, 201], "file": R9 + "r9_youtube.mov", **CUT(0.38), "pills": [("I searched", 178, 187), ("YouTube,", 187, 201)], "click": True},
    {"type": "rec", "src": [210, 239], "file": R9 + "r9_blogs.mov", **CUT(0.62), "pills": [("I read a bunch", 211, 225), ("of blogs.", 225, 239)]},
    {"type": "broll", "src": [243, 288], "file": SV, "in_s": 1220.4, "frame_w": 1920, "scale": 182,
     "pos": {"kf": [[13, [-0.35, 0.5]], [35, [0.75, 0.5]]]}, "pills": [("I even asked", 244, 258)], "words": broll_words},
    # ---------------- and I found out what you actually need to learn
    {"type": "pres", "src": [297, 344], **P(159), "pills": [("and I found out", 298, 311), ("what you", 311, 317), ("actually need", 317, 332), ("to learn", 332, 344)]},
    # ---------------- 1 system design
    {"type": "card", "src": [350, 373], "n": 1, "cover": cover("66"), "lines": [("SYSTEM", "big", 351), ("DESIGN", "big", 360)], "click": True},
    {"type": "pres", "src": [380, 400], **P(139), "pills": [("That's how", 381, 388), ("apps like", 388, 400)]},
    {"type": "rec", "src": [400, 462], "file": R9 + "r9_company_guides.mov", **CUT(0.5), "click": True,
     "pills": [("Netflix", 400, 409), ("and Uber", 409, 423), ("handle millions", 423, 446), ("of people.", 446, 462)],
     "logos": [("netflix", 400, 412), ("uber", 412, 424)]},
    # ---------------- 2 math behind machine learning
    {"type": "card", "src": [469, 518], "n": 2, "cover": cover("47"), "lines": [("MATH BEHIND", "lead", 485), ("MACHINE", "big", 499), ("LEARNING", "big", 506)], "click": True},
    {"type": "pres", "src": [519, 557], **P(144), "pills": [("starting from", 520, 529), ("the very basics.", 529, 557)]},
    # ---------------- 3 the famous AI research papers
    {"type": "card", "src": [566, 631], "n": 3, "cover": cover("48"), "lines": [("THE FAMOUS", "lead", 587), ("AI RESEARCH", "big", 596), ("PAPERS", "big", 614)], "click": True},
    {"type": "pres", "src": [634, 653], **P(146), "pills": [("for example.", 635, 653)]},
    {"type": "rec", "src": [658, 690], "file": R9 + "r9_attention.mov", "rec_scale": 98, "rec_pos": [0.5, 0.584], **CUT(0.6, 85), "pill_y": 0.50, "click": True,
     "pills": [("Attention is all", 659, 677), ("you need", 677, 690)]},
    # ---------------- 4 inference engineering
    {"type": "card", "src": [697, 725], "n": 4, "cover": cover("49"), "lines": [("INFERENCE", "big", 698), ("ENGINEERING", "big", 707)], "click": True},
    {"type": "pres", "src": [731, 786], **P(130), "pills": [("which is how", 732, 743), ("AI models", 743, 760), ("actually run.", 760, 786)]},
    # ---------------- 5 AI engineering
    {"type": "card", "src": [793, 830], "n": 5, "cover": cover("75"), "lines": [("ARTIFICIAL", "big", 811), ("INTELLIGENCE", "big", 813), ("ENGINEERING", "big", 816)], "click": True},
    {"type": "rec", "src": [830, 892], "file": R9 + "r9_ai_engineering.mov", **CUT(0.61), "click": True,
     "pills": [("which is building", 831, 844), ("real products", 844, 863), ("with those models.", 863, 892)]},
    # ---------------- and you can find all of these only on fanout
    {"type": "pres", "src": [898, 935], **P(128), "pills": [("And you can find", 899, 912), ("all of these", 912, 935)]},
    {"type": "pres", "src": [941, 967], **P(166), "pills": [("only on", 942, 955)], "logo_chest": {"start": 955}, "click": True},
    # ---------------- curated, mapped & complete, then the loader
    {"type": "end", "src": [968, 1015], "words": [("{ curated }", 968, 985), ("{ mapped }", 985, 1000), ("{ complete }", 1000, 1015)]},
    {"type": "loader", "n_frames": 72},
]

CLICK = MAN + "ES_Mechanical, Click, Buttons, Switches, Mixed, Antique, Special, Clicks - Epidemic Sound.mp3"
TING = MAN + "ES_User Interface, Misc, Pings, Tings, Generic, High, Tings - Epidemic Sound.mp3"


def audio(starts, total):
    L = [{"file": MAN + "Every Living Breathing Moment.mp3", "in_s": 19.854, "start": 0, "end": total - 14, "gain_db": -15, "fade_out": 10}]
    punch = starts[1]; ring = starts[2]
    L += [{"file": MAN + "ES_Swooshes, Whoosh, Airy, Light 03 - Epidemic Sound.mp3", "in_s": 2.878, "start": punch - 8, "end": punch + 11, "gain_db": -15},
          {"file": MAN + "ES_Mechanical, Click, Miniature Button, Multiple Pushes - Epidemic Sound.mp3", "in_s": 1.877, "start": punch - 2, "end": punch + 4, "gain_db": -22},
          {"file": MAN + "Denis Liudkevich - Delicate Antiques - Adjusting Ratchet Mech.wav", "in_s": 0.0, "start": ring + 3, "end": ring + 36, "speed": 0.6, "gain_db": -12},
          {"file": MAN + "Unrealsfx - Dramatic Clocks Vol 2 - Rotating Dials Clock Mechanism Beat.wav", "in_s": 0.459, "start": ring + 1, "end": ring + 32, "gain_db": -12}]
    for b, st in zip(BEATS, starts):
        if b.get("click"):
            L.append({"file": CLICK, "in_s": 2.419, "start": st - 4, "end": st + 12, "gain_db": -10})
        for which, s0, s1 in b.get("logos", []):
            t = st + s0 - b['src'][0]
            L.append({"file": TING, "in_s": 0.0, "start": t, "end": t + 15, "gain_db": -10})
    return L


PLAN = {"aroll": os.path.join(REEL, "Media", "sauce full aroll.mp4"), "matte_dir": os.path.join(SCRATCH, "frames"), "covers": COVERS,
        "man": MAN, "loader": MAN + "fanout-loader-alpha-prores4444 (1).mov", "beats": BEATS, "audio": audio}

if __name__ == '__main__':
    json.dump({k: v for k, v in PLAN.items() if k != 'audio'}, open(os.path.join(ROOT, "Fanout Reel 12 look-plan.json"), 'w'), indent=1)
    out = os.path.join(REEL, "Fanout_Reel_12_preview.mp4")
    n, starts = MR.render(PLAN, out, os.path.join(REEL, "preview_work"))
    print(out, n, 'frames', round(n / 24, 2), 's; beat starts', starts)
