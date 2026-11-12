#!/usr/bin/env python3
"""
Fanout Reel 8 — "How Discord stores a trillion messages" (hook A, six generated clips).

Built in the look of Abik's own Reel 7 edit (2026-11-12):
  * reference project = his "Fanout Reel 7 - hook A_1.prproj" (no-background titles: SF Pro Bold key
    phrase, Instrument Serif Regular lead/tail lines)
  * b-roll literal to the words, 2 short shots per line, in the hook too (full screen, no cutout),
    taken from "B-roll library/" and never a shot another reel has used (B-roll library/used.json)
  * hard punch-ins between phrases on full-frame beats

    python3 tools/gen_reel8_plan.py <stitch.json>     # writes "Fanout Reel 8 plan.json"
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_reel67_plans import Builder, ROOT, LOADER

REEL = "Fanout Reel 8"
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
    "snowden": ("Snowden - aptitude test.mp4", LIB, 176.0, "0,0,1280,536", 360),
}

CFG = dict(
    aroll="discord aroll.mp4", cutout="discord_cutout_alpha.mov", aroll_frames=960,
    body=["clip 02", "clip 03", "clip 04", "clip 05", "clip 06"],
    trims={"clip 01": [(3, 134)], "clip 02": [(1, 183)], "clip 03": [(1, 137)], "clip 04": [(2, 137)], "clip 05": [(0, 137)], "clip 06": [(3, 189)]},
    full_scale=140, full_pos=[0.5, 0.5], punch_scale=190, punch_pos=[0.5, 0.56],
    cut_scale=135, cut_y=0.888, cut_pos={'c': (0.5, 0), 'l': (0.33, 14), 'r': (0.61, -11)},
    recs={"discord_2017": ("r8_discord_2017.mov", 40), "cassandra": ("r8_cassandra.mov", 36), "scylladb": ("r8_scylladb.mov", 40),
          "data_model": ("r8_data_model.mov", 32), "cpp": ("r8_cpp_source.mov", 32), "rust": ("r8_rust.mov", 55),
          "data_services": ("r8_data_services.mov", 50), "fanout_case": ("r8_fanout_case.mov", 58), "guides": ("r8_company_guides.mov", 76)},
    stills={"r7_video_b.png": ("r8_case_b.png", "0,0,1526,1100"), "r7_video_a.png": ("r8_case_a.png", "0,0,1526,1000")},
)


class B8(Builder):
    def __init__(self, stitch):
        self.reel, self.cfg, self.hook = REEL, CFG, 'A'
        self.src = {s['name']: s['start_f'] for s in stitch['segs']}
        self.tl = {}; self.parts = []; t = 0
        for clip in ["clip 01"] + CFG['body']:
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

    def titles(self, clip, end, lines, y=0.415):
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
                if k == 'l':
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


def edit(b):
    # ---- clip 01 (hook): Discord stores over a trillion messages, and the database behind it nearly buckled.
    b.full("clip 01", 3, 23, cut=False)
    b.shot("clip 01", 23, 43, "mrrobot", 1237.8, pos=(0.5, 0.44), zoom=1.12, track="Broll 1")   # typing a message on a phone
    b.shot("clip 01", 43, 62, "mrrobot", 466.0, track="Broll 2", first=False)           # chat scrolling in a terminal
    b.full("clip 01", 62, 100)
    b.punch("clip 01", 100, 134); b.whoosh("clip 01", 100)
    b.titles("clip 01", 62, [(3, "Discord stores over", 'l'), (31, "a trillion messages,", 'k')])
    b.titles("clip 01", 134, [(65, "and the database behind it", 'l'), (103, "nearly buckled.", 'k')], y=0.455)

    # ---- clip 02: Back in 2017 they moved everything to Cassandra.
    b.rec("clip 02", 1, 36, "discord_2017", 'c');  b.caps("clip 02", [(1, 23, "Back in 2017,"), (23, 36, "they moved")])
    b.rec("clip 02", 36, 68, "cassandra", 'l');    b.caps("clip 02", [(36, 48, "everything"), (48, 68, "to Cassandra.")])
    # But one viral channel could pin a single node
    b.shot("clip 02", 68, 104, "sv", 415.0, 'r', zoom=1.15, track="Broll 1")            # hands inside one server rack
    b.shot("clip 02", 104, 136, "sv", 409.8, 'r', zoom=1.15, track="Broll 2", first=False)
    b.titles("clip 02", 136, [(70, "But one viral channel could pin", 'l'), (118, "a single node", 'k')], y=0.17)
    # and slow down everyone else on it.
    b.full("clip 02", 136, 183)
    b.titles("clip 02", 183, [(136, "and slow down", 'l'), (155, "everyone else", 'k'), (173, "on it.", 't')])

    # ---- clip 03: So they swapped in ScyllaDB. Same data model, written in C++,
    b.rec("clip 03", 1, 36, "scylladb", 'c');      b.caps("clip 03", [(1, 21, "So they swapped in"), (21, 36, "ScyllaDB.")])
    b.rec("clip 03", 36, 63, "data_model", 'l');   b.caps("clip 03", [(38, 63, "Same data model,")])
    b.rec("clip 03", 63, 90, "cpp", 'r');          b.caps("clip 03", [(65, 90, "written in C++,")])
    # so no garbage-collection pauses.
    b.full("clip 03", 90, 137, {"Scale": CFG['punch_scale'], "Position": CFG['punch_pos']})
    b.titles("clip 03", 137, [(93, "so no", 'l'), (105, "garbage collection", 'k'), (123, "pauses.", 't')], y=0.455)

    # ---- clip 04: Then they put a Rust service in front that merges duplicate requests
    b.rec("clip 04", 2, 52, "rust", 'c');          b.caps("clip 04", [(2, 19, "Then they put"), (19, 38, "a Rust service"), (38, 52, "in front")])
    b.rec("clip 04", 52, 96, "data_services", 'l'); b.caps("clip 04", [(52, 68, "that merges"), (68, 96, "duplicate requests")])
    # before they hit the database.
    b.shot("clip 04", 96, 137, "sv", 1257.4, 'r', pos=(0.3, 0.5), zoom=1.1)              # the server room, darker side so the title reads
    b.titles("clip 04", 137, [(96, "before they hit", 'l'), (116, "the database.", 'k')], y=0.17)

    # ---- clip 05: Reads went from as slow as 125 milliseconds... to 15.
    b.full("clip 05", 0, 58)
    b.titles("clip 05", 58, [(0, "Reads went from as slow as", 'l'), (29, "125 ms", 'k')])
    b.punch("clip 05", 58, 84)
    b.titles("clip 05", 84, [(64, "15 ms.", 'k')], y=0.51)
    # Stories like this are why I use Fanout.
    b.rec("clip 05", 84, 137, "fanout_case", 'c', {"Scale": 74, "Position": [0.5, 0.523]});   # top-aligned so the paywall card stays out of frame
    b.caps("clip 05", [(86, 113, "Stories like this"), (113, 137, "are why I use Fanout.")])

    # ---- clip 06: It animates how systems like Netflix and Uber actually work, request by request.
    b.rec("clip 06", 3, 75, "guides", 'l')
    b.caps("clip 06", [(3, 21, "It animates how"), (21, 34, "systems like"), (34, 42, "Netflix"), (42, 54, "and Uber"), (54, 75, "actually work,")])
    b.logo("clip 06", 34, 47, 'netflix'); b.logo("clip 06", 48, 62, 'uber')
    b.slides("clip 06", 75, 103, "r8_case_a.png", "r8_case_b.png", 'r'); b.caps("clip 06", [(77, 103, "request by request.")])
    # Before your next system design round,
    b.shot("clip 06", 103, 147, "snowden", 24.2, 'c', pos=(0.42, 0.5))                  # examiner in front of the test wall
    b.titles("clip 06", 147, [(105, "Before your next", 'l'), (121, "system design round,", 'k')], y=0.17)
    # check out Fanout.sh.
    b.full("clip 06", 147, 189)
    b.caps("clip 06", [(149, 156, "check out"), (156, 189, "fanout.sh")], "cap_low")


if __name__ == '__main__':
    stitch = json.load(open(sys.argv[1]))[REEL]
    b = B8(stitch); edit(b)
    out, total = b.finish()
    json.dump(b.used, open(os.path.join(ROOT, REEL, "broll_used.json"), 'w'), indent=1)
    print(os.path.basename(out), total, 'frames', round(total / 24, 1), 's', len(b.items), 'items; b-roll used:', b.used)
