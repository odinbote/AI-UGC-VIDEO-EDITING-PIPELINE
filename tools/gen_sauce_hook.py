#!/usr/bin/env python3
"""
"Sauce for engineers" hook, any presenter, in Abik's manual-edit look (EDITING_SYSTEM.md §22).
Same two lines every time, so one layout and a small config per clip: where the pauses are, when each word
is spoken (source frames), and the framing that puts the top of the head just under the text.

    python3 tools/gen_sauce_hook.py r11          # renders "Fanout Reel 11/Fanout_Reel_11_hook_preview.mp4"
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manual_look as ML
from PIL import ImageFont

ROOT = "/Users/abiknewar/Work/Claude Editing 2"
SCRATCH = "/private/tmp/claude-501/-Users-abiknewar-Work-Claude-Editing-2/50ae89ed-a5e9-41ec-bd82-530f1b1ca78b/scratchpad"
MAN = "/Users/abiknewar/Work/Fanout/AI Trianing UGC Prject Filea/Copied_AI UGC Manual Edits/"
COV = os.path.join(ROOT, "reference", "abik manual edit 2026-11-13", "covers")
COVERS = [os.path.join(COV, f"Group 13213167{n}.png") for n in ("66", "47", "48", "49", "75")]   # system design, math, AI research, inference, AI engineering

CONFIGS = {
    # pieces: (src_in, src_out, scale, pos). w: source frame each word starts. stack_x: left edge of the one-word-per-line stack.
    "r10": dict(reel="Fanout Reel 10", aroll="sauce hook aroll.mp4", matte="r10/frames",
                pieces=[(13, 78, {"kf": [[0, 108], [14, 122]]}, {"kf": [[0, [0.5, 0.54]], [14, [0.5, 0.61]]]}), (79, 101, 168, [0.5, 0.518]), (102, 180, 135, [0.5, 0.675])],
                w=dict(im=15, about=18, to=22, reveal=26, some=34, sauce=41, for_=52, engineers=58, thats=79, not_=84, out=88, there=95,
                       ring=102, to2=129, actually=138, become=146, a=154, senior=158, engineer=164), stack_x=0.15),
    "r11": dict(reel="Fanout Reel 11", aroll="sauce hook 3 aroll.mp4", matte="r11/frames",
                pieces=[(13, 67, {"kf": [[0, 100], [14, 114]]}, {"kf": [[0, [0.5, 0.5]], [14, [0.5, 0.522]]]}), (67, 95, 168, [0.5, 0.40]), (105, 183, 120, [0.5, 0.564])],
                w=dict(im=15, about=18, to=22, reveal=26, some=34, sauce=41, for_=51, engineers=57, thats=67, not_=76, out=80, there=85,
                       ring=105, to2=132, actually=140, become=148, a=156, senior=162, engineer=168), stack_x=0.70),
}


def small_w(text):
    return ML.text_width(text, ImageFont.truetype(ML.FONT_SEMI, ML.SMALL_PX))


def key_metrics(text, max_px=ML.KEY_MAX_PX, fit_w=ML.KEY_W):
    size = ML.fit_size(text, ML.FONT_BOLD, max_px, fit_w * ML.W)
    w = ML.text_width(text, ImageFont.truetype(ML.FONT_BOLD, size))
    return size, w / ML.W, 0.52 * size / ML.H        # size px, width (norm), x-height (norm)


def build(c):
    P = c['pieces']; w = c['w']; words = []
    pieces = [{"src_in": a, "src_out": b, "scale": s, "pos": p} for a, b, s, p in P]
    off, t = [], 0
    for a, b, _, _ in P:
        off.append(a - t); t += b - a
    N = t
    T = lambda piece, sf: sf - off[piece]

    def phrase(piece, smalls, key, key_sf, end_sf, base_y, justify=False):
        size, kw, xh = key_metrics(key)
        left, end = 0.5 - kw / 2, T(piece, end_sf)
        words.append({"text": key, "style": "key", "x": 0.5, "align": "c", "y": base_y, "start": T(piece, key_sf), "end": end, "size": size})
        sy = base_y - xh - 0.014
        if justify:           # first word flush left, the rest flush right (leaves room for the keyword's i-dots)
            words.append({"text": smalls[0][0], "style": "small", "x": left + 0.01, "y": sy, "start": T(piece, smalls[0][1]), "end": end})
            rest = ' '.join(x for x, _ in smalls[1:]); x = 0.5 + kw / 2 - 0.01 - small_w(rest) / ML.W
            for wd, sf in smalls[1:]:
                words.append({"text": wd, "style": "small", "x": x, "y": sy, "start": T(piece, sf), "end": end}); x += small_w(wd + ' ') / ML.W
        else:
            x = left
            for wd, sf in smalls:
                words.append({"text": wd, "style": "small", "x": x, "y": sy, "start": T(piece, sf), "end": end}); x += small_w(wd + ' ') / ML.W

    # piece 0: I'm about to REVEAL / some sauce for ENGINEERS
    phrase(0, [("I'm", w['im']), ("about", w['about']), ("to", w['to'])], "reveal", w['reveal'], w['some'], 0.266)
    phrase(0, [("some", w['some']), ("sauce", w['sauce']), ("for", w['for_'])], "engineers", w['engineers'], P[0][1], 0.248, justify=True)
    # piece 1: that's / not / out / there, one word per line beside the face
    for i, (wd, k) in enumerate([("that's", 'thats'), ("not", 'not_'), ("out", 'out'), ("there", 'there')]):
        words.append({"text": wd, "style": "small", "x": c['stack_x'], "y": 0.632 + 0.043 * i, "start": T(1, w[k]), "end": T(1, P[1][1])})
    # piece 2: covers sweep behind the head under "This is all you need to know", then the keyword block
    ring = {"start": T(2, w['ring']), "end": T(2, w['ring']) + 32, "phase0": 0.27, "turns": -1.34, "covers": COVERS,
            "geom": {"cx": 0.5, "cy": 0.205, "radius": 560, "card_h": 647}}
    x = 0.93 - small_w("to actually") / ML.W
    for wd, k in [("to", 'to2'), ("actually", 'actually')]:
        words.append({"text": wd, "style": "small", "x": x, "y": 0.222, "start": T(2, w[k]), "end": T(2, w['become'])}); x += small_w(wd + ' ') / ML.W
    size_s, kw_s, xh_s = key_metrics("senior", max_px=330, fit_w=0.76)
    size_e, _, _ = key_metrics("engineer", max_px=330, fit_w=0.76)
    end = T(2, P[2][1])
    words.append({"text": "senior", "style": "key", "x": 0.5, "align": "c", "y": 0.245, "start": T(2, w['senior']), "end": end, "size": size_s, "behind": True})
    words.append({"text": "engineer", "style": "key", "x": 0.5, "align": "c", "y": 0.318, "start": T(2, w['engineer']), "end": end, "size": size_e, "behind": True})
    x = 0.5 - kw_s / 2 + 0.11
    for wd, k in [("become", 'become'), ("a", 'a')]:
        words.append({"text": wd, "style": "small", "x": x, "y": 0.245 - xh_s - 0.014, "start": T(2, w[k]), "end": end, "behind": True}); x += small_w(wd + ' ') / ML.W

    cut1 = T(1, P[1][0])
    audio = {"layers": [
        {"file": MAN + "Every Living Breathing Moment.mp3", "in_s": 19.854, "start": 0, "end": N, "gain_db": -15, "fade_out": 6},
        {"file": MAN + "ES_Swooshes, Whoosh, Airy, Light 03 - Epidemic Sound.mp3", "in_s": 2.878, "start": cut1 - 8, "end": cut1 + 11, "gain_db": -15},
        {"file": MAN + "ES_Mechanical, Click, Miniature Button, Multiple Pushes - Epidemic Sound.mp3", "in_s": 1.877, "start": cut1 - 2, "end": cut1 + 4, "gain_db": -22},
        {"file": MAN + "Denis Liudkevich - Delicate Antiques - Adjusting Ratchet Mech.wav", "in_s": 0.0, "start": ring['start'] + 3, "end": ring['start'] + 36, "speed": 0.6, "gain_db": -12},
        {"file": MAN + "Unrealsfx - Dramatic Clocks Vol 2 - Rotating Dials Clock Mechanism Beat.wav", "in_s": 0.459, "start": ring['start'] + 1, "end": ring['start'] + 32, "gain_db": -12},
    ]}
    reel = os.path.join(ROOT, c['reel'])
    return {"aroll": os.path.join(reel, "Media", c['aroll']), "matte_dir": os.path.join(SCRATCH, c['matte']),
            "pieces": pieces, "words": words, "ring": ring, "audio": audio}


if __name__ == '__main__':
    key = sys.argv[1]; c = CONFIGS[key]
    plan = build(c)
    json.dump(plan, open(os.path.join(ROOT, f"{c['reel']} hook look-plan.json"), 'w'), indent=1)
    n_reel = c['reel'].split()[-1]
    out = os.path.join(ROOT, c['reel'], f"Fanout_Reel_{n_reel}_hook_preview.mp4")
    n = ML.render(plan, out, os.path.join(ROOT, c['reel'], "preview_work"))
    print(out, n, 'frames', round(n / 24, 2), 's', len(plan['words']), 'words')
