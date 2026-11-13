#!/usr/bin/env python3
"""
Premiere project for a reel in Abik's manual-edit look (EDITING_SYSTEM.md §22).

Takes the same beat list the preview renderer uses (tools/gen_reelNN.py -> BEATS) and clones every clip, text graphic,
caption and sound from Abik's own manual project (reference/abik manual edit 2026-11-13/AI UGC Manual Edits.prproj),
so fonts, colours, caption style, the keyword text animator and effect stacks are his, and everything stays editable.

His sequence is 23.976 fps, so the A-roll and the presenter cut-out are delivered as frame-for-frame 23.976 copies and
every time here is a frame count on that grid.

    python3 tools/build_manual_prproj.py 13
"""
import os, sys, json, importlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_prproj as BP, manual_look as ML, manual_reel as MR
from PIL import ImageFont

BP.FT = 10595108966                          # ticks per frame of his sequence (23.9748 fps, the rate Premiere read from his A-roll)
ROOT = "/Users/abiknewar/Work/Claude Editing 2"
REF = os.path.join(ROOT, "reference", "abik manual edit 2026-11-13", "AI UGC Manual Edits.prproj")
MAN = "/Users/abiknewar/Work/Fanout/AI Trianing UGC Prject Filea/Copied_AI UGC Manual Edits/"
SV_OLD = "vidssave.com Silicon Valley _ Season 1-5 _ Dinesh and Gilfoyle 1080P.mp4"
LOADER = "fanout-loader-alpha-prores4444 (1).mov"
AE_EXEMPLAR = "AI UGC Manual Edits Linked Comp 03/AI UGC manual Edits.aep"

# template items in his project: kind, track (by position), start seconds
EXEMPLARS = {
    "aroll": ("video", "V1", 2.377), "aroll_kf": ("video", "V1", 0.0), "ae_comp": ("video", "V1", 17.518), "rec": ("video", "V3", 6.298), "broll": ("video", "V2", 8.676),
    "matte": ("video", "V2", 36.455), "loader": ("video", "V3", 38.666), "logo_chest": ("video", "V10", 35.662),
    "netflix": ("video", "V7", 15.099), "uber": ("video", "V7", 15.600),
    "g_small": ("video", "V4", 0.209), "g_key": ("video", "V6", 0.542), "g_med": ("video", "V9", 9.301), "g_keymed": ("video", "V11", 9.593),
    "g_end1": ("video", "V3", 36.455), "g_end2": ("video", "V4", 37.164), "g_end3": ("video", "V5", 37.873),
    "cap_pres": ("caption", "C1", 10.636), "cap_rec": ("caption", "C1", 6.298), "cap_rec_low": ("caption", "C1", 24.484),
    "dialog": ("audio", "A1", 0.0), "music": ("audio", "A4", 0.0), "sfx_click": ("audio", "A3", 6.131),
    "sfx_whoosh": ("audio", "A5", 2.044), "sfx_button": ("audio", "A6", 2.294), "sfx_ting": ("audio", "A7", 15.099),
    "sfx_ratchet": ("audio", "A8", 3.462), "sfx_clock": ("audio", "A9", 3.379),
}
# text graphics: where the text origin (left end of the baseline) sits in the graphic's own frame, and the font size of the template
G = {"small": ("g_small", (0.25558, 0.12151), 68, ML.FONT_SEMI), "key": ("g_key", (0.12048, 0.16250), 270, ML.FONT_BOLD),
     "med": ("g_med", (0.125, 0.37135), 68, MR.FONT_MED), "keymed": ("g_keymed", (0.125, 0.37135), 150, MR.FONT_MED)}


def word_item(wd, st, a, track):
    ex, (tx, ty), ex_size, font = G[wd['style']]
    size = wd.get('size') or ML.SMALL_PX
    width = ML.text_width(wd['text'], ImageFont.truetype(font, size)) / ML.W
    left = wd['x'] - (width if wd.get('align') == 'r' else width / 2 if wd.get('align') == 'c' else 0)
    s = size / ex_size
    motion = {"Position": [round(left - s * (tx - 0.5), 5), round(wd['y'] - s * (ty - 0.5), 5)]}
    if abs(s - 1) > 0.005:
        motion["Scale"] = round(100 * s, 2)
    it = {"kind": "graphic", "track": track, "exemplar": ex, "title": {"text": wd['text']}, "start_f": st + wd['start'] - a, "end_f": st + wd['end'] - a, "motion": motion}
    if wd['style'] in ('key', 'keymed'):
        it["anim_in_f"] = 5
    return it


class Tracks:
    """lowest free video track from V4 up for text and overlays"""
    def __init__(self):
        self.busy = {}

    def take(self, s, e, lo=4, hi=13):
        for t in range(lo, hi + 1):
            if all(e <= bs or s >= be for bs, be in self.busy.get(t, [])):
                self.busy.setdefault(t, []).append((s, e)); return f"V{t}"
        raise RuntimeError("no free video track")


def build(reel_no):
    gen = importlib.import_module(f"gen_reel{reel_no}")
    cfg = json.load(open(os.path.join(ROOT, "tools", f"reel{reel_no}_package.json")))
    reel = os.path.join(ROOT, f"Fanout Reel {reel_no}"); M = os.path.join(reel, "Media") + "/"
    out_dir = os.path.join(reel, f"Copied_Fanout Reel {reel_no}"); os.makedirs(out_dir, exist_ok=True)
    name = f"Fanout Reel {reel_no}"
    items, T = [], Tracks()
    t = 0; starts = []; rec_titles = {}; new_media = []; media_copy = set(); voiced = 0
    aroll_frames = cfg['aroll_frames']

    # ---- cards: linked After Effects comps once Abik has run the AE build script (ae_comp_ids.json), rendered clips until then
    cards = {}; linked = {}
    ae_dir = os.path.join(reel, name + " AE folder")               # where Abik runs the AE build script
    ids_path, aep = os.path.join(ae_dir, "ae_comp_ids.json"), os.path.join(out_dir, name + ".aep")
    if os.path.exists(ids_path) and os.path.exists(os.path.join(ae_dir, name + ".aep")):
        import shutil
        shutil.copy2(os.path.join(ae_dir, name + ".aep"), aep)     # like his package: the .aep also sits next to the .prproj (same comp ids)
        linked = {c['beat']: c for c in json.load(open(ids_path))}
    for bi, b in enumerate(gen.BEATS):
        if b['type'] == 'card' and bi in linked:
            n = b['src'][1] - b['src'][0]; media_copy.add(aep)
            new_media.append({"key": f"card{bi}", "exemplar_title": AE_EXEMPLAR, "new_file": name + ".aep", "duration_s": n * 1001 / 24000, "frame_rect": "0,0,1080,1920"})
        elif b['type'] == 'card':
            n = b['src'][1] - b['src'][0]; fn = f"r{reel_no}_card_{bi:02d}.mov"; path = M + fn
            if not os.path.exists(path):
                d = os.path.join(reel, "preview_work", f"card_{bi}"); os.makedirs(d, exist_ok=True)
                for lf in range(n):
                    MR.render_card(b, lf, b['src'][0] + lf).convert('RGB').save(os.path.join(d, f"c_{lf:04d}.png"))
                subprocess.run([ML.FFMPEG, '-v', 'error', '-y', '-framerate', '24000/1001', '-i', os.path.join(d, 'c_%04d.png'),
                                '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', path], check=True)
            cards[bi] = fn; media_copy.add(path)
            new_media.append({"key": f"card{bi}", "exemplar_title": "r9_attention.mov", "new_file": fn, "duration_s": n * 1001 / 24000, "frame_rect": "0,0,1080,1920"})

    for bi, b in enumerate(gen.BEATS):
        starts.append(t); ty = b['type']
        n = b['n_frames'] if ty == 'loader' else b['src'][1] - b['src'][0]
        a = b['src'][0] if ty != 'loader' else 0; st = t
        if ty != 'loader':            # the voice under this beat, checkerboarded on A1/A2
            items.append({"kind": "audio", "track": "A1" if voiced % 2 == 0 else "A2", "exemplar": "dialog", "start_f": st, "end_f": st + n, "in_f": a}); voiced += 1
        if b.get('click'):
            items.append({"kind": "audio", "track": "A3", "exemplar": "sfx_click", "start_f": st - 4, "end_f": st + 12, "in_s": 2.419})

        def motion_of(scale, pos):
            m = {}
            for nm, v in (("Scale", scale), ("Position", pos)):
                m[nm] = {"keyframes": [[f, val] for f, val in v['kf']]} if isinstance(v, dict) else v
            return m

        if ty == 'pres':
            kf = isinstance(b['scale'], dict) or isinstance(b['pos'], dict)
            items.append({"kind": "video", "track": "V1", "exemplar": "aroll_kf" if kf else "aroll", "start_f": st, "end_f": st + n, "in_f": a, "motion": motion_of(b['scale'], b['pos'])})
            if any(w.get('behind') for w in b.get('words', [])) or b.get('ring'):
                s0 = min([w['start'] for w in b.get('words', []) if w.get('behind')] + ([b['ring']['start']] if b.get('ring') else []))
                items.append({"kind": "video", "track": "V13", "exemplar": "rec", "media_key": "cutout", "start_f": st + s0 - a, "end_f": st + n, "in_f": s0,
                              "motion": motion_of(b['scale'], b['pos'])})
            for cap in b.get('pills', []):
                it = {"kind": "caption", "track": "C1", "exemplar": "cap_pres", "text": cap[0], "start_f": st + cap[1] - a, "end_f": st + min(cap[2], b['src'][1]) - a}
                if len(cap) > 3:                   # pill moved off his chest line (e.g. under something the presenter holds)
                    it["y"] = round(cap[3] - 0.007, 4)
                items.append(it)
            lc = b.get('logo_chest')
            if lc:
                s = st + lc['start'] - a
                items.append({"kind": "video", "track": T.take(s, st + n, lo=10), "exemplar": "logo_chest", "start_f": s, "end_f": st + n, "in_s": 0.0, "speed": 2,
                              "motion": {"Scale": 44, "Position": [0.5, lc.get('y', 0.667)]}})
        elif ty == 'rec':
            title = os.path.basename(b['file'])
            it = {"kind": "video", "track": "V2", "exemplar": "rec", "start_f": st, "end_f": st + n, "in_s": b.get('in_f', 0) / 24,
                  "motion": {"Scale": b.get('rec_scale', 70.8), "Position": b.get('rec_pos', [0.5, 0.5])}}
            if title in cfg.get('rec_new', {}):       # more recordings than his project has: extra ones are new media
                it["media_key"] = "rec_" + title
            elif title != cfg['rec_retarget']['r9_youtube.mov']:
                it["media_title"] = title
            items.append(it)
            items.append({"kind": "video", "track": "V3", "exemplar": "rec", "media_key": "cutout", "start_f": st, "end_f": st + n, "in_f": a,
                          "motion": {"Scale": b['cut_scale'], "Position": b['cut_pos']}})
            for which, s0, s1 in b.get('logos', []):
                items.append({"kind": "video", "track": T.take(st + s0 - a, st + s1 - a, lo=7), "exemplar": which, "start_f": st + s0 - a, "end_f": st + s1 - a})
                items.append({"kind": "audio", "track": "A7" if which == 'netflix' else "A8", "exemplar": "sfx_ting", "start_f": st + s0 - a, "end_f": st + s0 - a + 15, "in_s": 0.0})
            ex = "cap_rec_low" if b.get('pill_y', 0.47) >= 0.5 else "cap_rec"
            for cap in b.get('pills', []):
                it = {"kind": "caption", "track": "C1", "exemplar": ex, "text": cap[0], "start_f": st + cap[1] - a, "end_f": st + min(cap[2], b['src'][1]) - a}
                if 'pill_y' in b:
                    it["y"] = round(b['pill_y'] - 0.007, 4)
                items.append(it)
        elif ty == 'broll':
            pos = b['pos']
            items.append({"kind": "video", "track": "V2", "exemplar": "broll", "start_f": st, "end_f": st + n, "in_s": b['in_s'],
                          "motion": {"Scale": b['scale'], "Position": {"keyframes": [[f, v] for f, v in pos['kf']]} if isinstance(pos, dict) else pos}})
            for cap in b.get('pills', []):
                items.append({"kind": "caption", "track": "C1", "exemplar": "cap_pres", "text": cap[0], "start_f": st + cap[1] - a, "end_f": st + min(cap[2], b['src'][1]) - a})
        elif ty == 'card':
            if bi in linked:
                items.append({"kind": "video", "track": "V1", "exemplar": "ae_comp", "media_key": f"card{bi}", "start_f": st, "end_f": st + n, "in_f": 0})
            else:
                items.append({"kind": "video", "track": "V1", "exemplar": "rec", "media_key": f"card{bi}", "start_f": st, "end_f": st + n, "in_f": 0, "motion": {"Scale": 100, "Position": [0.5, 0.5]}})
        elif ty == 'end':
            total_after = st + n + sum(x['n_frames'] for x in gen.BEATS[bi + 1:] if x['type'] == 'loader')
            items.append({"kind": "video", "track": "V2", "exemplar": "matte", "start_f": st, "end_f": total_after})
            for (text, s0, s1), ex, trk in zip(b['words'], ("g_end1", "g_end2", "g_end3"), ("V3", "V4", "V5")):
                items.append({"kind": "graphic", "track": trk, "exemplar": ex, "start_f": st + s0 - a, "end_f": st + s1 - a, "anim_in_f": 0})
        elif ty == 'loader':
            items.append({"kind": "video", "track": "V3", "exemplar": "loader", "start_f": st, "end_f": st + n, "in_s": 0.0})
        for wd in b.get('words', []) if ty in ('pres', 'broll') else []:
            s, e = st + wd['start'] - a, st + wd['end'] - a
            items.append(word_item(wd, st, a, T.take(s, e, lo=4, hi=12)))
        t += n
    total = t
    # ---- music and the hook sounds
    items.append({"kind": "audio", "track": "A4", "exemplar": "music", "start_f": 0, "end_f": total - 14, "in_s": 19.854})
    punch = starts[1]
    items += [{"kind": "audio", "track": "A5", "exemplar": "sfx_whoosh", "start_f": punch - 8, "end_f": punch + 11, "in_s": 2.878},
              {"kind": "audio", "track": "A6", "exemplar": "sfx_button", "start_f": punch - 2, "end_f": punch + 4, "in_s": 1.877},
              {"kind": "audio", "track": "A7", "exemplar": "sfx_button", "start_f": punch - 2, "end_f": punch + 4, "in_s": 1.877}]
    for bi, b in enumerate(gen.BEATS):
        if b.get('ring'):
            r = starts[bi] + b['ring']['start'] - b['src'][0]
            items += [{"kind": "audio", "track": "A8", "exemplar": "sfx_ratchet", "start_f": r + 3, "end_f": r + 36, "in_s": 0.0, "speed": 0.6},
                      {"kind": "audio", "track": "A9", "exemplar": "sfx_clock", "start_f": r + 1, "end_f": r + 32, "in_s": 0.459}]

    dur = aroll_frames * 1001 / 24000
    retarget = [{"old_title": "IliiUD5WCcn_Eb6udsbzeg.mp4", "new_file": cfg['aroll'], "duration_s": dur, "audio_rate": 48000, "frame_rect": "0,0,1080,1920"}]
    for old, new in cfg['rec_retarget'].items():
        retarget.append({"old_title": old, "new_file": new, "duration_s": cfg['rec_frames'][new] / 24, "frame_rect": "0,0,1526,2712"})
    if cfg.get('broll'):
        retarget.append({"old_title": SV_OLD, "new_file": os.path.basename(cfg['broll']['file']), "duration_s": cfg['broll']['duration_s'], "frame_rect": cfg['broll']['frame_rect']})
        media_copy.add(cfg['broll']['file'])
    for f, frames in cfg.get('rec_new', {}).items():
        new_media.append({"key": "rec_" + f, "exemplar_title": "r9_attention.mov", "new_file": f, "duration_s": frames / 24, "frame_rect": "0,0,1526,2712"})
        media_copy.add(M + f)
    new_media.append({"key": "cutout", "exemplar_title": LOADER, "new_file": cfg['cutout'], "duration_s": dur, "frame_rect": "0,0,1080,1920"})
    media_copy |= {M + cfg['aroll'], M + cfg['cutout']} | {M + f for f in cfg['rec_retarget'].values()}
    media_copy |= {MAN + f for f in (LOADER, "Every Living Breathing Moment.mp3", "ES_Swooshes, Whoosh, Airy, Light 03 - Epidemic Sound.mp3",
                                       "ES_Mechanical, Click, Miniature Button, Multiple Pushes - Epidemic Sound.mp3",
                                       "ES_Mechanical, Click, Buttons, Switches, Mixed, Antique, Special, Clicks - Epidemic Sound.mp3",
                                       "ES_User Interface, Misc, Pings, Tings, Generic, High, Tings - Epidemic Sound.mp3",
                                       "Denis Liudkevich - Delicate Antiques - Adjusting Ratchet Mech.wav",
                                       "Unrealsfx - Dramatic Clocks Vol 2 - Rotating Dials Clock Mechanism Beat.wav",
                                       "Netflix_2015_logo.svg.webp", "5ij5qdSHFzJ2piPRuoTL5F.jpg")}
    used_ex = {it['exemplar'] for it in items}
    plan = {"reference": REF, "output_dir": out_dir, "media_flat": True, "media_copy": sorted(media_copy), "media_copy_dirs": [], "media_skip": [],
            "exemplars": {k: {"kind": v[0], "track": v[1], "start": v[2]} for k, v in EXEMPLARS.items() if k in used_ex},
            "retarget": retarget, "new_media": new_media, "items": sorted(items, key=lambda i: i['start_f']),
            "total_frames": total, "project_name": name, "sequence_name": name, "old_sequence_name": "IliiUD5WCcn_Eb6udsbzeg"}
    json.dump(plan, open(os.path.join(ROOT, f"{name} prproj-plan.json"), 'w'), indent=1)
    out = BP.build(plan)
    # his sequence carries preview renders of his own timeline; drop them so they never show over this edit
    P = BP.Project(out); n_prev = 0
    for e in P.root.iter('PreviewItems'):
        for x in list(e):
            e.remove(x); n_prev += 1
    # Dynamic Link: each linked comp is a Media entry on the .aep whose ImporterPrefs is the comp's item id
    order = [linked[bi] for bi, b in enumerate(gen.BEATS) if b['type'] == 'card' and bi in linked]
    if order:
        import base64
        aep_name = name + ".aep"
        meds = [e for e in P.root if e.tag == 'Media' and e.findtext('Title') == aep_name]
        mcs = [e for e in P.root if e.tag == 'MasterClip' and e.findtext('Name') == aep_name]
        pis = [e for e in P.root if e.tag == 'ClipProjectItem' and e.findtext('.//Name') == aep_name]
        subs = [e for e in P.root if e.tag == 'SubClip' and e.findtext('Name') == aep_name]
        assert len(meds) == len(order), (len(meds), len(order))
        for i, c in enumerate(order):
            title = f"{c['name']}/{aep_name}"
            P.set_child(meds[i], 'Title', title)
            ip = meds[i].find('ImporterPrefs')
            ip.text = base64.b64encode(("%08x-0000-0000-0000-000000000000" % c['id']).encode('utf-16-le')).decode()
            P.rehash(ip)
            P.set_child(mcs[i], 'Name', title); P.set_child(pis[i].find('ProjectItem'), 'Name', title)
            mcu = mcs[i].attrib['ObjectUID']
            for sc in subs:
                if sc.find('MasterClip') is not None and sc.find('MasterClip').attrib.get('ObjectURef') == mcu:
                    P.set_child(sc, 'Name', title)
        print('linked', len(order), 'After Effects comp(s)')
    P.save(out)
    print('dropped', n_prev, 'stale preview renders')
    return out, total, len(items), cards


if __name__ == '__main__':
    out, total, n, cards = build(int(sys.argv[1]))
    print(out, total, 'frames', n, 'items; card clips:', cards)
