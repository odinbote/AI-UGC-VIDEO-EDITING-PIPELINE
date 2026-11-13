#!/usr/bin/env python3
"""
Fanout Reel 9 — "The sauce for engineers: five things to learn" (one continuous take, 1080x1920).

Built in the look of Abik's own Reel 7 edit (2026-11-12):
  * reference project = his "Fanout Reel 7 - hook A_1.prproj" (no-background titles: SF Pro Bold key
    phrase, Instrument Serif Regular lead/tail lines)
  * b-roll literal to the words, 2 short shots per line, in the hook too (full screen, no cutout),
    taken from "B-roll library/" and never a shot another reel has used (B-roll library/used.json)
  * hard punch-ins between phrases on full-frame beats

  * this presenter wears a white T-shirt in a bright office, so the no-background titles sit ABOVE the head
    (between the exit sign and the hair), never on the chest; the frame is pushed down to make that band

    python3 tools/gen_reel9_plan.py                   # writes "Fanout Reel 9 plan.json"
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_reel67_plans import Builder, ROOT, LOADER

REEL = "Fanout Reel 9"
REF = os.path.join(ROOT, "reference", "abik edits 2026-11-12", "Fanout Reel 7 - hook A_1.prproj")
R7 = os.path.join(ROOT, "Fanout Reel 7", "Copied_Fanout Reel 7")
LIB = os.path.join(ROOT, "B-roll library", "movies")
SV = "vidssave.com Silicon Valley _ Season 1-5 _ Dinesh and Gilfoyle 1080P.mp4"

# template items in Abik's project: kind, track, start seconds
f = lambda n: n / 24
EXEMPLARS = {
    "aroll": ("video", "Aroll", 0.0), "matte": ("video", "Color mate Background", f(55)),
    "rec": ("video", "Screen Recording 1", f(241)), "shot_slide": ("video", "Screen Recording 1", f(610)),
    "shot_slide2": ("video", "Screen Recording 2", f(610)), "broll1": ("video", "Broll 1", f(55)), "broll2": ("video", "Broll 2", f(89)),
    "adj": ("video", "Adjustment effects Grains & Fades", f(55)), "outro": ("video", "Outro Animation", f(843)),
    "g_lead": ("video", "Text Graphics 1", f(147)), "g_key": ("video", "Text Graphics 2", f(165)), "g_tail": ("video", "Text Graphics 3", f(86)),
    "g_lead2": ("video", "Text Graphics 2", f(330)), "g_key3": ("video", "Text Graphics 3", f(347)),
    "logo_netflix": ("video", "Logos", f(570)), "logo_uber": ("video", "Logos", f(583)),
    "cap_layout": ("caption", "Subtitle 1", f(241)), "cap_youll": ("caption", "Subtitle 1", f(189)), "cap_low": ("caption", "Subtitle 1", f(781)),
    "dialog": ("audio", "Aroll Sound", 0.0), "sfx_click": ("audio", "SFX 1", f(51)), "sfx_ui_b": ("audio", "SFX 5", f(85)),
    "sfx_whoosh": ("audio", "SFX 3", f(15)), "sfx_button": ("audio", "SFX 4", f(21)), "sfx_ting": ("audio", "SFX 3", f(568)),
    "music": ("audio", "Background music", 0.0),
}

# b-roll sources: key -> (file, folder, duration s, frame rect, scale that fills 9:16)
BROLL = {
    "sv": (SV, R7, 1292.4, "0,0,1920,1080", 180),
    "mrrobot": ("Mr Robot - Elliot hacking compilation.mp4", LIB, 1897.3, "0,0,1920,1080", 180),
    "gwh": ("Good Will Hunting - Will solves the math challenge.mp4", LIB, 255.7, "0,0,1920,1080", 180),
}

CFG = dict(
    aroll="senior aroll.mp4", cutout="senior_cutout_alpha.mov", aroll_frames=1009,
    body=[],
    trims={"take": [(3, 82), (87, 1005)]},
    # full frame is pushed down so the band between the exit sign and the hair is free for titles
    full_scale=114, full_pos=[0.5, 0.57], punch_scale=140, punch_pos=[0.5, 0.62],
    cut_scale=88, cut_y=0.717, cut_pos={'c': (0.5, 0), 'l': (0.34, 12), 'r': (0.62, -10)},
    recs={"youtube": ("r9_youtube.mov", 40), "blogs": ("r9_blogs.mov", 40), "guides": ("r9_company_guides.mov", 60),
          "sys_overview": ("r9_system_overview.mov", 44), "ml_math": ("r9_ml_math.mov", 60), "papers": ("r9_papers.mov", 40),
          "attention": ("r9_attention.mov", 46), "inference": ("r9_inference.mov", 50), "ai_eng": ("r9_ai_engineering.mov", 72),
          "home": ("r9_home.mov", 64)},
    stills={},
)


class B9(Builder):
    def __init__(self, stitch):
        self.reel, self.cfg, self.hook = REEL, CFG, 'A'
        self.src = {s['name']: s['start_f'] for s in stitch['segs']}
        self.tl = {}; self.parts = []; t = 0
        for clip in ["take"] + CFG['body']:
            for pi, (a, b) in enumerate(CFG['trims'][clip]):
                self.tl[(clip, pi)] = (t, a, b); self.parts.append((clip, pi, t, a, b)); t += b - a
        self.end, self.total = t, t + LOADER
        self.items = []; self.cuts = []; self.ui_cuts = []; self.used = {}

    def punch(self, clip, l0, l1):                       # hard punch-in between phrases
        self.full(clip, l0, l1, {"Scale": CFG['punch_scale'], "Position": CFG['punch_pos']}, cut=False)

    def shot(self, clip, l0, l1, src, in_s, where=None, pos=(0.5, 0.5), zoom=1.0, track="Broll 1", first=True):
        """library b-roll; where=None -> full screen with no presenter, else behind the cutout"""
        fn, _, _, _, fill = BROLL[src]
        s, e = self.T(clip, l0), self.T(clip, l1)
        it = {"in_s": in_s, "file": fn, "motion": {"Scale": round(fill * zoom), "Position": list(pos)}}
        if src != 'sv': it["media_key"] = src
        self.V(track, "broll1", s, e, **it)
        if where: self.cutout(clip, l0, l1, where)
        (self.cuts if first else self.ui_cuts).append(s)
        self.used.setdefault(src, []).append(in_s)

    def titles(self, clip, end, lines, y=0.415, align='l'):
        """no-background stack. lines: [(l0, text, kind)] kind: 'l' lead, 'k' key, 't' tail. Lines end together at `end`."""
        kinds = ''.join(k for _, _, k in lines)
        ex = {'lk': ['g_lead', 'g_key'], 'k': ['g_key'], 'lkt': ['g_lead', 'g_key', 'g_tail'], 'llk': ['g_lead', 'g_lead2', 'g_key3']}[kinds]
        tr = {'g_lead': 1, 'g_key': 2, 'g_tail': 3, 'g_lead2': 2, 'g_key3': 3}
        key = next(t for _, t, k in lines if k == 'k'); n = len(key)
        ksize = 154 if n <= 8 else 140 if n <= 11 else 125 if n <= 14 else 112 if n <= 17 else 100 if n <= 20 else 90
        kw = 0.00037 * ksize * n
        yy = y
        for i, (l0, text, k) in enumerate(lines):
            if k == 'k':
                yk = yy if i == 0 else yy + 0.058
                self.G(clip, l0, end, tr[ex[i]], ex[i], text, 'plain-bold', ksize, 0.5, round(yk, 3)); yy = yk
            else:
                lw = 0.0208 * len(text)
                if k == 'l' and align == 'r':      # lead flush with the key's right edge: keeps it off the ceiling light on presenter beats
                    x = max(0.5, min(0.86, 0.5 + kw / 2 - lw / 2)); yl = yy if i == 0 else yy + 0.045
                elif k == 'l':
                    x = min(0.5, max(0.3, 0.5 - kw / 2 + lw / 2)); yl = yy if i == 0 else yy + 0.045
                else:
                    x = max(0.5, min(0.72, 0.5 + kw / 2 - lw / 2)); yl = yy + 0.05
                self.G(clip, l0, end, tr[ex[i]], ex[i], text, 'serif-regular', 68, round(x, 3), round(yl, 3)); yy = yl

    def finish(self):
        c = self.cfg; base = []
        for i, (clip, pi, t, a, b) in enumerate(self.parts):
            base.append({"kind": "video", "track": "Aroll", "exemplar": "aroll", "start_f": t, "end_f": t + b - a, "in_f": self.S(clip, a), "link": f"a{i}",
                         "motion": {"Scale": c['full_scale'], "Position": c['full_pos']}})
            self.items.append({"kind": "audio", "track": "Aroll Sound", "exemplar": "dialog", "gain_db": 0, "start_f": t, "end_f": t + b - a, "in_f": self.S(clip, a), "link": f"a{i}"})
        base.append({"kind": "video", "track": "Color mate Background", "exemplar": "matte", "start_f": 0, "end_f": self.total})
        self.V("Adjustment effects Grains & Fades", "adj", 0, self.end)
        self.V("Outro Animation", "outro", self.end, self.total, in_s=0, motion={"Scale": 48, "Position": [0.5, 0.5]})
        for i, cf in enumerate(sorted(set(x for x in self.cuts if x > 0))):
            self.A("SFX 1" if i % 2 == 0 else "SFX 2", "sfx_click", -10, cf - 4, cf + 12, 2.417)
        for cf in sorted(set(self.ui_cuts)):
            self.A("SFX 5", "sfx_ui_b", -15, cf - 4, cf, 0.0)
        self.A("SFX 2", "sfx_ui_b", -15, self.end, self.end + 4, 0.0)
        self.A("Background music", "music", -30, 0, self.total, 14.875, fade_out_f=7)
        M = os.path.join(ROOT, REEL, "Media") + "/"
        shared = ["ES_Electronica the Witch - Andreas Dahlback.mp3", "ES_Mechanical, Click, Buttons, Switches, Mixed, Antique, Special, Clicks - Epidemic Sound.mp3",
                  "ES_Mechanical, Click, Miniature Button, Multiple Pushes - Epidemic Sound.mp3", "ES_Swooshes, Whoosh, Airy, Light 03 - Epidemic Sound.mp3",
                  "ES_User Interface, Click, On & Off, Small, Short 02 - Epidemic Sound.mp3", "ES_User Interface, Misc, Pings, Tings, Generic, High, Tings - Epidemic Sound.mp3",
                  "fanout-loader-alpha-prores4444 (1).mov", "Netflix_2015_logo.svg.webp", "5ij5qdSHFzJ2piPRuoTL5F.jpg", "Transition_Woosh.mp3"]
        p = {"reference": REF, "media_copy_dirs": [], "media_skip": [], "old_sequence_name": "Fanout Reel 7 - hook A", "media_flat": True, "preview_grade": True,
             "caption_font": "regular",
             "exemplars": {k: {"kind": v[0], "track": v[1], "start": v[2]} for k, v in EXEMPLARS.items()},
             "output_dir": os.path.join(ROOT, REEL, f"Copied_{REEL}"), "project_name": REEL, "sequence_name": REEL, "total_frames": self.total,
             "media": {"aroll": c['aroll'], "cutout": c['cutout'], "aroll_frames": c['aroll_frames']}}
        p['media_copy'] = ([M + c['aroll'], M + c['cutout']] + [M + fn for fn, _ in c['recs'].values()] + [M + s for s, _ in c['stills'].values()]
                           + [os.path.join(R7, s) for s in shared] + [os.path.join(BROLL[k][1], BROLL[k][0]) for k in sorted(set(self.used))])
        dur = c['aroll_frames'] / 24
        p['retarget'] = [{"old_title": "sysdesign aroll.mp4", "new_file": c['aroll'], "duration_s": dur, "audio_rate": 48000, "frame_rect": "0,0,1080,1920"}] + [
            {"old_title": old, "new_file": new, "frame_rect": rect} for old, (new, rect) in c['stills'].items()]
        p['new_media'] = ([{"key": "cutout", "exemplar_title": "fanout-loader-alpha-prores4444 (1).mov", "new_file": c['cutout'], "duration_s": dur, "frame_rect": "0,0,1080,1920"}]
                          + [{"key": k, "exemplar_title": "r7_home.mov", "new_file": fn, "duration_s": round(n / 24, 3), "frame_rect": "0,0,1526,2712"} for k, (fn, n) in c['recs'].items()]
                          + [{"key": k, "exemplar_title": SV, "new_file": BROLL[k][0], "duration_s": BROLL[k][2], "frame_rect": BROLL[k][3]} for k in sorted(set(self.used)) if k != 'sv'])
        p['items'] = base + self.items
        out = os.path.join(ROOT, f"{REEL} plan.json")
        json.dump(p, open(out, 'w'), indent=1, ensure_ascii=False)
        return out, self.total


T = "take"


def edit(b):
    Y = 0.165          # first title line on presenter beats: renders at ~0.26, under the ceiling light and clear of the hair (two lines only)
    # ---- HOOK: I'm about to reveal some sauce for engineers that's not out there.
    b.full(T, 3, 24, cut=False)
    b.shot(T, 24, 40, "sv", 1235.85, pos=(0.8, 0.5), track="Broll 1")               # engineers gathered behind their screens
    b.shot(T, 40, 55, "sv", 1153.8, track="Broll 2", first=False)
    b.punch(T, 55, 82); b.whoosh(T, 55)
    b.titles(T, 55, [(3, "I'm about to", 'l'), (13, "reveal some sauce", 'k'), (37, "for engineers", 't')], y=Y, align='r')
    b.titles(T, 82, [(55, "that's", 'l'), (63, "not out there.", 'k')], y=Y, align='r')

    # ---- This is all you need to know to actually become a senior engineer.
    b.full(T, 87, 119)
    b.punch(T, 119, 163); b.whoosh(T, 119)
    b.titles(T, 119, [(90, "This is all", 'l'), (101, "you need to know", 'k')], y=Y, align='r')
    b.titles(T, 160, [(119, "to actually", 'l'), (128, "become a senior engineer.", 'k')], y=Y, align='r')

    # ---- I searched YouTube, I read a bunch of blogs, I even asked a few senior engineers.
    b.rec(T, 163, 194, "youtube", 'c');  b.caps(T, [(167, 180, "I searched"), (180, 194, "YouTube,")])
    b.rec(T, 194, 224, "blogs", 'l');    b.caps(T, [(196, 209, "I read a bunch"), (209, 224, "of blogs,")])
    # title sits on the actor's chest, between his face and the presenter's head (as in Abik's Reel 7 edit)
    b.shot(T, 224, 250, "sv", 498.45, 'r', pos=(0.62, 0.47), zoom=1.1, track="Broll 1")    # the senior engineer, arms crossed at his desk
    b.shot(T, 250, 276, "sv", 801.9, 'r', pos=(0.1, 0.47), zoom=1.1, track="Broll 2", first=False)
    b.titles(T, 276, [(226, "I even asked", 'l'), (242, "a few senior engineers.", 'k')], y=0.345)

    # ---- And I found out what you actually need to learn.
    b.full(T, 276, 340)
    b.titles(T, 321, [(279, "And I found out", 'l'), (299, "what you actually", 'k')], y=Y, align='r')
    b.titles(T, 338, [(321, "need to learn.", 'k')], y=Y + 0.058)

    # ---- One, system design. That's how apps like Netflix and Uber handle millions of people.
    b.punch(T, 340, 377); b.whoosh(T, 340)
    b.titles(T, 377, [(343, "One,", 'l'), (354, "System design.", 'k')], y=Y, align='r')
    b.rec(T, 377, 421, "guides", 'l')
    b.caps(T, [(380, 397, "That's how apps like"), (397, 409, "Netflix"), (409, 421, "and Uber")])
    b.logo(T, 397, 409, 'netflix'); b.logo(T, 409, 421, 'uber')
    b.rec(T, 421, 461, "sys_overview", 'r'); b.caps(T, [(421, 443, "handle millions"), (443, 458, "of people.")])

    # ---- Two, the math behind machine learning, starting from the very basics.
    b.rec(T, 461, 517, "ml_math", 'c'); b.caps(T, [(465, 474, "Two,"), (482, 497, "the math behind"), (497, 515, "machine learning,")])
    b.shot(T, 517, 537, "gwh", 64.8, 'l', pos=(0.12, 0.5), track="Broll 1")             # working a problem on the board
    b.shot(T, 537, 556, "gwh", 101.4, 'l', track="Broll 2", first=False)                # the matrix on the board
    b.titles(T, 556, [(517, "starting from", 'l'), (532, "the very basics.", 'k')], y=0.15)

    # ---- Three, the famous AI research papers. For example, Attention Is All You Need.
    b.full(T, 556, 590)
    b.punch(T, 590, 626); b.whoosh(T, 590)
    b.titles(T, 590, [(561, "Three,", 'l'), (580, "the famous", 'k')], y=Y, align='r')
    b.titles(T, 624, [(590, "AI research papers.", 'k')], y=Y + 0.058)
    b.rec(T, 626, 649, "papers", 'r');   b.caps(T, [(628, 645, "For example,")])
    b.rec(T, 649, 686, "attention", 'c', {"Scale": 90, "Position": [0.5, 0.636]})        # top-aligned, paywall card out of frame
    b.caps(T, [(649, 665, "Attention Is"), (665, 683, "All You Need.")])

    # ---- Four, inference engineering, which is how AI models actually run.
    b.rec(T, 686, 730, "inference", 'l'); b.caps(T, [(689, 698, "Four,"), (706, 730, "inference engineering,")])
    b.shot(T, 730, 757, "sv", 1244.0, 'r', pos=(0.34, 0.5), track="Broll 1")            # inside the server racks
    b.shot(T, 757, 783, "sv", 420.4, 'r', pos=(0.66, 0.40), zoom=1.2, track="Broll 2", first=False)
    b.titles(T, 783, [(730, "which is how AI models", 'l'), (757, "actually run.", 'k')], y=0.345)

    # ---- Five, AI engineering, which is building real products with those models.
    b.punch(T, 783, 825); b.whoosh(T, 783)
    b.titles(T, 825, [(786, "Five,", 'l'), (804, "AI engineering,", 'k')], y=Y, align='r')
    b.rec(T, 825, 889, "ai_eng", 'l')
    b.caps(T, [(825, 839, "which is building"), (839, 858, "real products"), (858, 885, "with those models.")])

    # ---- And you can find all of these only on Fanout,
    b.rec(T, 889, 948, "home", 'c')
    b.caps(T, [(893, 911, "And you can find"), (911, 927, "all of these"), (927, 946, "only on Fanout,")])
    # ---- curated, mapped, and complete.
    b.punch(T, 948, 1005)
    b.titles(T, 1005, [(952, "Curated,", 'l'), (974, "mapped & complete.", 'k')], y=Y, align='r')


if __name__ == '__main__':
    stitch = {"segs": [{"name": "take", "start_f": 0, "frames": CFG['aroll_frames']}]}
    b = B9(stitch); edit(b)
    out, total = b.finish()
    json.dump(b.used, open(os.path.join(ROOT, REEL, "broll_used.json"), 'w'), indent=1)
    print(os.path.basename(out), total, 'frames', round(total / 24, 1), 's', len(b.items), 'items; b-roll used:', b.used)
