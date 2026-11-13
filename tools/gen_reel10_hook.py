#!/usr/bin/env python3
"""
Fanout Reel 10 — hook only ("sauce for engineers", second presenter), in Abik's manual-edit look (§22).

    python3 tools/gen_reel10_hook.py            # renders "Fanout Reel 10/Fanout_Reel_10_hook_preview.mp4"
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manual_look as ML
from PIL import ImageFont

ROOT = "/Users/abiknewar/Work/Claude Editing 2"
REEL = os.path.join(ROOT, "Fanout Reel 10")
SCRATCH = "/private/tmp/claude-501/-Users-abiknewar-Work-Claude-Editing-2/50ae89ed-a5e9-41ec-bd82-530f1b1ca78b/scratchpad/r10"
MAN = "/Users/abiknewar/Work/Fanout/AI Trianing UGC Prject Filea/Copied_AI UGC Manual Edits/"
COV = os.path.join(ROOT, "reference", "abik manual edit 2026-11-13", "covers")
COVERS = [os.path.join(COV, f"Group 13213167{n}.png") for n in ("66", "47", "48", "49", "75")]   # system design, math, AI research, inference, AI engineering

# A-roll pieces (source frames, every pause cut) and their framing
PIECES = [
    {"src_in": 13, "src_out": 78, "scale": {"kf": [[0, 108], [14, 122]]}, "pos": {"kf": [[0, [0.5, 0.54]], [14, [0.5, 0.61]]]}},   # I'm about to reveal some sauce for engineers
    {"src_in": 79, "src_out": 101, "scale": 168, "pos": [0.5, 0.518]},                                                              # that's not out there.
    {"src_in": 102, "src_out": 180, "scale": 135, "pos": [0.5, 0.675]},                                                              # This is all ... a senior engineer.
]
OFF = [13, 14, 15]            # source frame -> timeline frame, per piece
T = lambda piece, src_f: src_f - OFF[piece]

words = []


def small_w(text):
    return ML.text_width(text, ImageFont.truetype(ML.FONT_SEMI, ML.SMALL_PX))


def key_metrics(text, max_px=ML.KEY_MAX_PX, fit_w=ML.KEY_W):
    size = ML.fit_size(text, ML.FONT_BOLD, max_px, fit_w * ML.W)
    w = ML.text_width(text, ImageFont.truetype(ML.FONT_BOLD, size))
    return size, w / ML.W, 0.52 * size / ML.H        # size px, width (norm), x-height (norm)


def phrase(smalls, key, key_start, end, base_y, justify=False, indent=0.0, max_px=ML.KEY_MAX_PX, behind=False):
    """smalls: [(word, start)] on one row above the keyword; key: keyword text"""
    size, kw, xh = key_metrics(key, max_px)
    left = 0.5 - kw / 2
    words.append({"text": key, "style": "key", "x": 0.5, "align": "c", "y": base_y, "start": key_start, "end": end, "size": size, "behind": behind})
    sy = base_y - xh - 0.014
    if justify:           # first word flush left, the rest flush right (leaves room for the keyword's i-dots)
        words.append({"text": smalls[0][0], "style": "small", "x": left + 0.01, "y": sy, "start": smalls[0][1], "end": end})
        rest = ' '.join(w for w, _ in smalls[1:]); x = 0.5 + kw / 2 - 0.01 - small_w(rest) / ML.W
        for w, st in smalls[1:]:
            words.append({"text": w, "style": "small", "x": x, "y": sy, "start": st, "end": end}); x += small_w(w + ' ') / ML.W
    else:
        x = left + indent
        for w, st in smalls:
            words.append({"text": w, "style": "small", "x": x, "y": sy, "start": st, "end": end}); x += small_w(w + ' ') / ML.W
    return base_y


# ---- piece 0
phrase([("I'm", T(0, 15)), ("about", T(0, 18)), ("to", T(0, 22))], "reveal", T(0, 26), T(0, 34), 0.266)
phrase([("some", T(0, 34)), ("sauce", T(0, 41)), ("for", T(0, 52))], "engineers", T(0, 58), T(0, 78), 0.248, justify=True)
# ---- piece 1: one word per line beside the face
for i, (w, sf) in enumerate([("that's", 79), ("not", 84), ("out", 88), ("there", 95)]):
    words.append({"text": w, "style": "small", "x": 0.15, "y": 0.632 + 0.043 * i, "start": T(1, sf), "end": T(1, 101)})
# ---- piece 2: ring under "This is all you need to know", then the keyword block behind the head
RING = {"start": T(2, 102), "end": T(2, 134), "phase0": 0.27, "turns": -1.34, "covers": COVERS,
        "geom": {"cx": 0.5, "cy": 0.205, "radius": 560, "card_h": 647}}
x = 0.93 - small_w("to actually") / ML.W
for w, sf in [("to", 129), ("actually", 138)]:
    words.append({"text": w, "style": "small", "x": x, "y": 0.222, "start": T(2, sf), "end": T(2, 146)}); x += small_w(w + ' ') / ML.W
size_s, kw_s, xh_s = key_metrics("senior", max_px=330, fit_w=0.76)
words.append({"text": "senior", "style": "key", "x": 0.5, "align": "c", "y": 0.245, "start": T(2, 158), "end": T(2, 180), "size": size_s, "behind": True})
size_e, kw_e, xh_e = key_metrics("engineer", max_px=330, fit_w=0.76)
words.append({"text": "engineer", "style": "key", "x": 0.5, "align": "c", "y": 0.318, "start": T(2, 164), "end": T(2, 180), "size": size_e, "behind": True})
x = 0.5 - kw_s / 2 + 0.11
for w, sf in [("become", 146), ("a", 154)]:
    words.append({"text": w, "style": "small", "x": x, "y": 0.245 - xh_s - 0.014, "start": T(2, sf), "end": T(2, 180), "behind": True}); x += small_w(w + ' ') / ML.W

N = sum(p['src_out'] - p['src_in'] for p in PIECES)
cut1 = T(1, 79)
AUDIO = {"layers": [
    {"file": MAN + "Every Living Breathing Moment.mp3", "in_s": 19.854, "start": 0, "end": N, "gain_db": -15, "fade_out": 6},
    {"file": MAN + "ES_Swooshes, Whoosh, Airy, Light 03 - Epidemic Sound.mp3", "in_s": 2.878, "start": cut1 - 8, "end": cut1 + 11, "gain_db": -15},
    {"file": MAN + "ES_Mechanical, Click, Miniature Button, Multiple Pushes - Epidemic Sound.mp3", "in_s": 1.877, "start": cut1 - 2, "end": cut1 + 4, "gain_db": -22},
    {"file": MAN + "Denis Liudkevich - Delicate Antiques - Adjusting Ratchet Mech.wav", "in_s": 0.0, "start": RING['start'] + 3, "end": RING['start'] + 36, "speed": 0.6, "gain_db": -12},
    {"file": MAN + "Unrealsfx - Dramatic Clocks Vol 2 - Rotating Dials Clock Mechanism Beat.wav", "in_s": 0.459, "start": RING['start'] + 1, "end": RING['start'] + 32, "gain_db": -12},
]}

PLAN = {"aroll": os.path.join(REEL, "Media", "sauce hook aroll.mp4"), "matte_dir": os.path.join(SCRATCH, "frames"),
        "pieces": PIECES, "words": words, "ring": RING, "audio": AUDIO}

if __name__ == '__main__':
    json.dump(PLAN, open(os.path.join(ROOT, "Fanout Reel 10 hook look-plan.json"), 'w'), indent=1)
    out = os.path.join(REEL, "Fanout_Reel_10_hook_preview.mp4")
    n = ML.render(PLAN, out, os.path.join(REEL, "preview_work"))
    print(out, n, 'frames', round(n / 24, 2), 's', len(words), 'words')
