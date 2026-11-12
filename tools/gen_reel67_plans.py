#!/usr/bin/env python3
"""
Plans for multi-clip A-rolls with hook variants (Fanout Reel 6 "learning AI the hard way",
Fanout Reel 7 "stop winging your system design").

Each video is one stitched A-roll file: hook A, hook B, hook C, then the body clips, untrimmed.
Every clip becomes its own timeline item (video + linked audio) trimmed to speech, so the edit
stays adjustable. One plan per hook: <hook X> + body. Beats are written in clip-local frames.

    python3 tools/gen_reel67_plans.py <stitch.json>      # writes "Fanout Reel N - hook X plan.json"
"""
import json, sys, os

ROOT = "/Users/abiknewar/Work/Claude Editing 2"
TEMPLATE = json.load(open(os.path.join(ROOT, "Fanout Reel 4 v2 plan.json")))
L_X, R_X = 0.3037036955356598, 0.6101852059364319
LOADER = 50


class Builder:
    def __init__(self, reel, cfg, stitch, hook):
        self.reel, self.cfg, self.hook = reel, cfg, hook
        self.src = {s['name']: s['start_f'] for s in stitch['segs']}       # clip -> first source frame
        order = [f"hook {hook}"] + cfg['body']
        self.tl = {}                                                       # (clip, part) -> (tl_start, a, b)
        t = 0; self.parts = []
        for clip in order:
            for pi, (a, b) in enumerate(cfg['trims'][clip]):
                self.tl[(clip, pi)] = (t, a, b); self.parts.append((clip, pi, t, a, b)); t += b - a
        self.end = t
        self.total = t + LOADER
        self.items = []; self.cuts = []; self.ui_cuts = []

    # clip-local frame -> timeline frame
    def T(self, clip, lf):
        for (c, pi), (t, a, b) in self.tl.items():
            if c == clip and a <= lf <= b:
                return t + lf - a
        raise ValueError(f"{clip} local frame {lf} is trimmed out")

    def S(self, clip, lf):          # clip-local -> source frame in the stitched file
        return self.src[clip] + lf

    def V(self, track, ex, s, e, **kw):
        self.items.append({"kind": "video", "track": track, "exemplar": ex, "start_f": s, "end_f": e, **kw})

    # ---- layouts (clip, l0, l1 in clip-local frames) ----
    def full(self, clip, l0, l1, motion=None, cut=True):
        c = self.cfg
        s, e = self.T(clip, l0), self.T(clip, l1)
        self.V("Aroll Full Screen", "aroll", s, e, in_f=self.S(clip, l0), motion=motion or {"Scale": c['full_scale'], "Position": c['full_pos']})
        if cut: self.cuts.append(s)

    def cutout(self, clip, l0, l1, where='c'):
        c = self.cfg
        x, rot = c['cut_pos'][where]
        self.V("Aroll Cutout", "aroll", self.T(clip, l0), self.T(clip, l1), media_key="cutout", in_f=self.S(clip, l0),
               motion={"Scale": c['cut_scale'], "Position": [x, c['cut_y']], "Rotation": rot})

    def rec(self, clip, l0, l1, key, where='c', motion=None, in_s=0):
        s, e = self.T(clip, l0), self.T(clip, l1)
        self.V("Screen Recording 1", "rec", s, e, media_key=key, file=self.cfg['recs'][key][0], in_s=in_s,
               motion=motion or {"Scale": 70.8, "Position": [0.5, 0.5]})
        self.cutout(clip, l0, l1, where); self.cuts.append(s)

    def slides(self, clip, l0, l1, top, bottom, where='c'):
        s, e = self.T(clip, l0), self.T(clip, l1)
        self.V("Screen Recording 2", "shot_slide2", s, e, still=top, motion={"Scale": 70, "Position": {"keyframes": [[0, [0.5, 0.215]], [27, [0.5, 0.175]]]}})
        self.V("Screen Recording 1", "shot_slide", s, e, still=bottom, motion={"Scale": 70, "Position": {"keyframes": [[0, [0.5, 0.585]], [27, [0.5, 0.545]]]}})
        self.cutout(clip, l0, l1, where); self.cuts.append(s)

    def listscroll(self, clip, l0, l1, still, where='c'):
        s, e = self.T(clip, l0), self.T(clip, l1)
        self.V("Screen Recording 1", "shot_scroll", s, e, still=still, motion={"Scale": 165, "Position": {"keyframes": [[0, [0.5, 1.0]], [50, [0.5, 0.55]]]}})
        self.cutout(clip, l0, l1, where); self.cuts.append(s)

    def zoom(self, clip, l0, l1, still, where='c', s0=62, s1=68, y=0.36):
        s, e = self.T(clip, l0), self.T(clip, l1)
        self.V("Screen Recording 1", "shot_zoom", s, e, still=still, motion={"Scale": {"keyframes": [[0, s0], [e - s, s1]]}, "Position": [0.5, y]})
        self.cutout(clip, l0, l1, where); self.cuts.append(s)

    def broll(self, clip, l0, l1, which, in_s, where='c', track="Broll 1", first=True):
        s, e = self.T(clip, l0), self.T(clip, l1)
        # Silicon Valley: punched in and raised so the actor's face clears the title stack;
        # Social Network: punched in past its letterbox bars
        ex, scale, pos = ("broll1", 215, [0.5, 0.40]) if which == 'sv' else ("broll2", 365, [0.5, 0.5])
        self.V(track, ex, s, e, in_s=in_s, motion={"Scale": scale, "Position": pos})
        self.cutout(clip, l0, l1, where)
        (self.cuts if first else self.ui_cuts).append(s)

    # ---- text ----
    def G(self, clip, l0, l1, track, ex, text, style, size, x, y):
        self.items.append({"kind": "graphic", "track": f"Text Graphics {track}", "exemplar": ex, "title": {"text": text, "style": style, "size": size},
                           "start_f": self.T(clip, l0), "end_f": self.T(clip, l1), "motion": {"Position": [x, y]}})

    def stack(self, clip, end, lines, above_head=False):
        """lines: [(l0, text, kind)], kind 's' serif or 'b' box; 2 or 3 lines; all end at `end`."""
        ys = self.cfg['title_y_head'] if above_head else self.cfg['title_y']
        kinds = ''.join(k for _, _, k in lines)
        ex = {'sb': ['g_instead', 'g_random'], 'ssb': ['g_instead', 'g_memorizing', 'g_senior'], 'sbs': ['g_thisfeels', 'g_cheating', 'g_but'],
              'ss': ['g_instead', 'g_memorizing'], 'sss': ['g_instead', 'g_memorizing', 'g_but']}[kinds]
        xs = [0.45, 0.5, 0.57] if len(lines) == 3 else [0.45, 0.5]
        for i, (l0, text, k) in enumerate(lines):
            if k == 'b':
                n = len(text); size = 121 if n <= 15 else 110 if n <= 17 else 100 if n <= 20 else 92
                style = 'box-semibold'; x = 0.5
            else:
                n = len(text); size = 85 if n <= 26 else 74 if n <= 30 else 64
                style = 'serif'; x = xs[i] if n <= 22 else 0.5
            self.G(clip, l0, end, i + 1, ex[i], text, style, size, x, ys[i])

    def caps(self, clip, rows, ex="cap_layout"):
        for l0, l1, text in rows:
            self.items.append({"kind": "caption", "track": "Subtitle 1", "exemplar": ex, "text": text, "start_f": self.T(clip, l0), "end_f": self.T(clip, l1)})

    def A(self, track, ex, gain, s, e, in_s, **kw):
        self.items.append({"kind": "audio", "track": track, "exemplar": ex, "gain_db": gain, "start_f": s, "end_f": e, "in_s": in_s, **kw})

    def whoosh(self, clip, lf):
        t = self.T(clip, lf)
        self.A("SFX 3", "sfx_whoosh", -15, t - 6, t + 13, 2.875)
        self.A("SFX 4", "sfx_button", -25, t, t + 6, 1.875); self.A("SFX 5", "sfx_button", -25, t, t + 6, 1.875)

    def logo(self, clip, l0, l1, which):
        s, e = self.T(clip, l0), self.T(clip, l1)
        if which == 'netflix':
            self.V("Logos", "logo_netflix", s, e, still="Netflix_2015_logo", motion={"Scale": {"keyframes": [[0, 0], [3, 18]]}, "Position": [0.5, 0.2875]})
        else:
            self.V("Logos", "logo_uber", s, e, still="5ij5qdSHFzJ2piPRuoTL5F", motion={"Scale": {"keyframes": [[0, 0], [2, 33]]}, "Position": [0.5, 0.283]})
        self.A("SFX 3" if which == 'netflix' else "SFX 4", "sfx_ting", -10, s - 2, s + 13, 0.0)

    # ---- assemble ----
    def finish(self):
        c = self.cfg
        base = []
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
        name = f"{self.reel} - hook {self.hook}"
        M = os.path.join(ROOT, self.reel, "Media") + "/"
        p = {k: TEMPLATE[k] for k in ['reference', 'media_copy_dirs', 'exemplars', 'old_sequence_name', 'media_flat', 'preview_grade']}
        p['media_skip'] = ["Sequence 02_12.mp4"] + ([] if c.get('broll') else [
            "vidssave.com Silicon Valley _ Season 1-5 _ Dinesh and Gilfoyle 1080P.mp4", "vidssave.com _We're Ranking Girls_ _ THE SOCIAL NETWORK (2010) Movie CLIP 4K 720P.mp4"])
        p['output_dir'] = os.path.join(ROOT, self.reel, f"Copied_{self.reel}")
        p['project_name'] = p['sequence_name'] = name
        p['total_frames'] = self.total
        p['media'] = {"aroll": c['aroll'], "cutout": c['cutout'], "aroll_frames": c['aroll_frames']}
        p['media_copy'] = [M + c['aroll'], M + c['cutout']] + [M + f for f, _ in c['recs'].values()] + [M + s for s in c['stills'].values()]
        dur = c['aroll_frames'] / 24
        p['retarget'] = [{"old_title": "Sequence 02_12.mp4", "new_file": c['aroll'], "duration_s": round(dur, 3), "audio_rate": 48000, "frame_rect": "0,0,1080,1920"}]
        rects = {"Screenshot 2026-10-24 at 1.10.17 AM.png": "0,0,1526,1100", "Screenshot 2026-10-24 at 1.12.30 AM.png": "0,0,1526,1000",
                 "Screenshot 2026-10-24 at 1.25.04 AM.png": "0,0,1526,1400", "Screenshot 2026-10-24 at 1.25.39 AM.png": "0,0,500,2200"}
        for old, new in c['stills'].items():
            p['retarget'].append({"old_title": old, "new_file": new, "frame_rect": rects[old]})
        p['new_media'] = [{"key": "cutout", "exemplar_title": "fanout-loader-alpha-prores4444 (1).mov", "new_file": c['cutout'], "duration_s": round(dur, 3), "frame_rect": "0,0,1080,1920"}] + [
            {"key": k, "exemplar_title": "Screen Recording 2026-10-24 at 1.08.06 AM.mov", "new_file": f, "duration_s": round(n / 24, 3), "frame_rect": "0,0,1526,2712"} for k, (f, n) in c['recs'].items()]
        p['items'] = base + self.items
        out = os.path.join(ROOT, f"{name} plan.json")
        json.dump(p, open(out, 'w'), indent=1, ensure_ascii=False)
        return out, self.total


# ======================================================================================
# Reel 6 — "learning AI the hard way"
# ======================================================================================
R6 = dict(
    aroll="learnai aroll.mp4", cutout="learnai_cutout_alpha.mov", aroll_frames=1200,
    body=["body 02", "body 03", "body 04", "body 05", "body 06", "body 07"],
    trims={"hook A": [(4, 93)], "hook B": [(0, 93)], "hook C": [(4, 129)], "body 02": [(2, 140)], "body 03": [(0, 184)],
           "body 04": [(0, 81), (101, 139)], "body 05": [(1, 131)], "body 06": [(8, 96)], "body 07": [(2, 110)]},
    full_scale=140, full_pos=[0.5, 0.5], title_y=[0.404, 0.467, 0.530], title_y_head=[0.164, 0.227, 0.29],
    cut_scale=155, cut_y=0.882, cut_pos={'c': (0.5, 0), 'l': (L_X, 18), 'r': (R_X, -11)},
    recs={"youtube": ("r6_youtube.mov", 56), "youtube_more": ("r6_youtube_more.mov", 52), "arxiv_abs": ("r6_arxiv_abs.mov", 42),
          "arxiv_paper": ("r6_arxiv_paper.mov", 42), "home": ("r6_home.mov", 42), "papers": ("r6_papers.mov", 45),
          "explainer": ("r6_explainer.mov", 58), "math": ("r6_math.mov", 32), "math_formulas": ("r6_math_formulas.mov", 62)},
    stills={"Screenshot 2026-10-24 at 1.25.39 AM.png": "r6_arxiv_list.png", "Screenshot 2026-10-24 at 1.25.04 AM.png": "r6_equation.png",
            "Screenshot 2026-10-24 at 1.10.17 AM.png": "r6_attn_b.png", "Screenshot 2026-10-24 at 1.12.30 AM.png": "r6_attn_a.png"},
)


def reel6(b, hook):
    FS = b.cfg['full_scale']
    push = lambda k0, k1: {"Scale": {"keyframes": [[k0, FS], [k1, FS + 10]]}, "Position": b.cfg['full_pos']}
    if hook == 'A':     # Most software engineers are learning AI the hard way.
        b.full("hook A", 4, 93, push(50, 82)); b.whoosh("hook A", 56)
        b.stack("hook A", 93, [(4, "Most software engineers", 's'), (30, "are learning AI", 's'), (58, "the hard way.", 'b')])
    elif hook == 'B':   # Watching more AI tutorials is exactly why you still don't get transformers.
        b.full("hook B", 0, 93, push(54, 82)); b.whoosh("hook B", 56)
        b.stack("hook B", 54, [(0, "Watching more", 's'), (13, "AI tutorials", 'b'), (32, "is exactly why", 's')])
        b.caps("hook B", [(54, 68, "you still don't"), (68, 93, "get transformers.")], "cap_youll")
    else:               # Most engineers learn AI top-down. The ones who get it start from the paper.
        b.full("hook C", 4, 129, push(62, 92)); b.whoosh("hook C", 66)
        b.stack("hook C", 66, [(4, "Most engineers", 's'), (24, "learn AI top-down.", 'b')])
        b.stack("hook C", 129, [(66, "The ones who get it", 's'), (95, "start from the paper.", 'b')])

    # A YouTube video on transformers, a paper you save for later, and forty tabs you never close.
    b.rec("body 02", 2, 54, "youtube", 'c');        b.caps("body 02", [(4, 25, "A YouTube video"), (25, 54, "on transformers,")])
    b.rec("body 02", 54, 92, "arxiv_abs", 'l');     b.caps("body 02", [(56, 68, "a paper"), (68, 92, "you save for later,")])
    b.rec("body 02", 92, 140, "youtube_more", 'r'); b.caps("body 02", [(94, 115, "and forty tabs"), (115, 138, "you never close.")])
    # But the video skips the part the paper assumes you already know, so you open the paper anyway.
    b.full("body 03", 0, 67)
    b.stack("body 03", 67, [(0, "But the video", 's'), (14, "skips the part", 'b'), (30, "the paper assumes you already know,", 's')])
    b.rec("body 03", 67, 105, "arxiv_paper", 'c');  b.caps("body 03", [(69, 83, "so you open"), (83, 105, "the paper anyway.")])
    # Page three. First equation. Laptop closed.
    b.listscroll("body 03", 105, 127, "r6_arxiv_list.png", 'l'); b.caps("body 03", [(107, 127, "Page three.")])
    b.zoom("body 03", 127, 184, "r6_equation.png", 'r', s0=95, s1=108, y=0.385);         b.caps("body 03", [(129, 154, "First equation."), (156, 184, "Laptop closed.")])
    # The problem isn't you. It's the order you're learning it in.
    b.full("body 04", 0, 81)
    b.stack("body 04", 34, [(0, "The problem", 's'), (14, "isn't you.", 'b')])
    b.stack("body 04", 81, [(34, "It's the order", 's'), (53, "you're learning it in.", 'b')])
    # Fanout flips the order.
    b.rec("body 04", 101, 139, "home", 'c');        b.caps("body 04", [(101, 120, "Fanout flips"), (120, 139, "the order.")])
    # Its AI Research archive walks you through the ideas behind a paper before you read it.
    b.rec("body 05", 1, 42, "papers", 'l');         b.caps("body 05", [(1, 28, "Its AI Research"), (28, 42, "archive")])
    # explainer shown larger and top-aligned so the page's paywall card stays out of frame
    b.rec("body 05", 42, 97, "explainer", 'r', {"Scale": 90, "Position": [0.5, 0.636]});     b.caps("body 05", [(42, 61, "walks you through"), (61, 76, "the ideas"), (76, 97, "behind a paper")])
    b.slides("body 05", 97, 131, "r6_attn_a.png", "r6_attn_b.png", 'c'); b.caps("body 05", [(97, 116, "before you"), (116, 131, "read it.")])
    # So by page three, you already know what the equation is doing.
    b.rec("body 06", 8, 37, "math", 'l');           b.caps("body 06", [(8, 37, "So by page three,")])
    b.rec("body 06", 37, 96, "math_formulas", 'r', {"Scale": {"keyframes": [[0, 70.8], [59, 76]]}, "Position": [0.5, 0.5]})
    b.caps("body 06", [(37, 53, "you already know"), (53, 72, "what the equation"), (72, 96, "is doing.")])
    # Next time a paper lands in your team chat, open it on Fanout.sh first.
    b.full("body 07", 2, 110)
    b.stack("body 07", 52, [(2, "Next time a paper lands", 's'), (30, "in your team chat,", 'b')])
    b.caps("body 07", [(53, 71, "open it on"), (71, 92, "fanout.sh"), (92, 110, "first.")], "cap_low")


# ======================================================================================
# Reel 7 — "stop winging your system design"
# ======================================================================================
R7 = dict(
    aroll="sysdesign aroll.mp4", cutout="sysdesign_cutout_alpha.mov", aroll_frames=1152, broll=True,
    body=["body 02", "body 03", "body 04", "body 05", "body 06"],
    trims={"hook A": [(2, 57)], "hook B": [(0, 87)], "hook C": [(0, 94)], "body 02": [(0, 186)], "body 03": [(0, 176)],
           "body 04": [(1, 144)], "body 05": [(1, 189)], "body 06": [(0, 111)]},
    full_scale=114, full_pos=[0.5, 0.436], title_y=[0.424, 0.487, 0.550], title_y_head=[0.164, 0.227, 0.29],
    cut_scale=108, cut_y=0.81, cut_pos={'c': (0.5, 0), 'l': (0.5, 4), 'r': (0.5, -4)},
    recs={"kafka": ("r7_kafka.mov", 28), "cache": ("r7_cache.mov", 20), "lb": ("r7_loadbalancers.mov", 24), "home": ("r7_home.mov", 58),
          "guides": ("r7_company_guides.mov", 70), "lab": ("r7_lab_latency.mov", 36), "roadmap": ("r7_roadmap.mov", 50)},
    stills={"Screenshot 2026-10-24 at 1.10.17 AM.png": "r7_video_b.png", "Screenshot 2026-10-24 at 1.12.30 AM.png": "r7_video_a.png"},
)


def reel7(b, hook):
    FS = b.cfg['full_scale']
    push = lambda k0, k1: {"Scale": {"keyframes": [[k0, FS], [k1, FS + 8]]}, "Position": b.cfg['full_pos']}
    if hook == 'A':     # Stop winging your system design.
        b.full("hook A", 2, 57, push(19, 45)); b.whoosh("hook A", 23)
        b.stack("hook A", 57, [(2, "Stop winging", 's'), (23, "your system design.", 'b')])
    elif hook == 'B':   # You don't fail system design rounds because you don't know Kafka.
        b.full("hook B", 0, 87, push(44, 72)); b.whoosh("hook B", 46)
        b.stack("hook B", 87, [(0, "You don't fail", 's'), (15, "system design rounds", 'b'), (46, "because you don't know Kafka.", 's')])
    else:               # Junior engineers draw boxes. Senior engineers explain why the boxes break.
        b.full("hook C", 0, 94, push(38, 66)); b.whoosh("hook C", 40)
        b.stack("hook C", 40, [(0, "Junior engineers", 's'), (21, "draw boxes.", 'b')])
        b.stack("hook C", 94, [(40, "Senior engineers", 's'), (58, "explain why", 's'), (71, "the boxes break.", 'b')])

    # You've shipped real systems for years.
    b.broll("body 02", 0, 34, 'sv', 582.5, 'c', "Broll 1"); b.broll("body 02", 34, 49, 'sn', 93.0, 'c', "Broll 2", first=False)
    b.stack("body 02", 49, [(0, "You've shipped", 's'), (13, "real systems", 's'), (31, "for years.", 'b')], above_head=True)
    # Then someone says "design YouTube"
    b.broll("body 02", 49, 92, 'sn', 298.0, 'l', "Broll 1", first=False)
    b.stack("body 02", 92, [(49, "Then someone says", 's'), (72, "design YouTube", 'b')], above_head=True)
    # and your mind goes blank. But it's not that you don't know the parts.
    b.full("body 02", 92, 186)
    b.stack("body 02", 129, [(92, "and your mind", 's'), (110, "goes blank.", 'b')])
    b.caps("body 02", [(132, 152, "But it's not"), (152, 166, "that you don't know"), (166, 186, "the parts.")], "cap_youll")
    # You know Kafka, caches, load balancers.
    b.rec("body 03", 0, 25, "kafka", 'c');  b.caps("body 03", [(0, 25, "You know Kafka,")])
    b.rec("body 03", 25, 42, "cache", 'l'); b.caps("body 03", [(27, 42, "caches,")])
    b.rec("body 03", 42, 63, "lb", 'r');    b.caps("body 03", [(44, 63, "load balancers.")])
    # You've just never watched them work together under load. So you draw boxes and hope.
    b.full("body 03", 63, 176)
    b.stack("body 03", 124, [(65, "You've just never", 's'), (81, "watched them work together", 's'), (106, "under load.", 'b')])
    b.stack("body 03", 176, [(124, "So you draw boxes", 's'), (153, "and hope.", 'b')])
    # And the interviewer can tell the second they ask,
    b.broll("body 04", 1, 27, 'sv', 583.98, 'c', "Broll 1"); b.broll("body 04", 27, 51, 'sv', 586.66, 'c', "Broll 2", first=False)
    b.stack("body 04", 51, [(1, "And the interviewer", 's'), (20, "can tell the second", 's'), (36, "they ask,", 'b')], above_head=True)
    # "what happens when this fails?"
    b.full("body 04", 51, 90)
    b.stack("body 04", 90, [(52, "what happens", 's'), (66, "when this fails?", 'b')])
    # That's the part Fanout shows.
    b.rec("body 04", 90, 144, "home", 'c'); b.caps("body 04", [(94, 115, "That's the part"), (115, 144, "Fanout shows.")])
    # You watch how systems at Netflix and Uber actually work,
    b.rec("body 05", 1, 67, "guides", 'r')
    b.caps("body 05", [(1, 14, "You watch how"), (14, 27, "systems at"), (27, 35, "Netflix"), (35, 46, "and Uber"), (46, 67, "actually work,")])
    b.logo("body 05", 27, 40, 'netflix'); b.logo("body 05", 40, 56, 'uber')
    # piece by piece, in interactive animations.
    b.slides("body 05", 67, 88, "r7_video_a.png", "r7_video_b.png", 'l'); b.caps("body 05", [(67, 88, "piece by piece,")])
    b.rec("body 05", 88, 120, "lab", 'c');  b.caps("body 05", [(88, 101, "in interactive"), (101, 120, "animations.")])
    # You've built systems. Now you can explain them.
    b.full("body 05", 120, 189)
    b.stack("body 05", 189, [(124, "You've built systems.", 's'), (158, "Now you can", 's'), (171, "explain them.", 'b')])
    # If your design round is this month, check out Fanout.sh before it.
    b.rec("body 06", 0, 47, "roadmap", 'c'); b.caps("body 06", [(0, 21, "If your design round"), (21, 47, "is this month,")])
    b.full("body 06", 47, 111)
    b.caps("body 06", [(49, 59, "check out"), (59, 85, "Fanout.sh"), (85, 111, "before it.")], "cap_low")


if __name__ == '__main__':
    stitch = json.load(open(sys.argv[1]))
    for reel, cfg, fn in (("Fanout Reel 6", R6, reel6), ("Fanout Reel 7", R7, reel7)):
        for hook in "ABC":
            b = Builder(reel, cfg, stitch[reel], hook); fn(b, hook)
            out, total = b.finish()
            print(os.path.basename(out), total, 'frames', round(total / 24, 1), 's', len(b.items), 'items')
