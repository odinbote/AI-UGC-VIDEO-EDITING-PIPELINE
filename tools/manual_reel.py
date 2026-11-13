#!/usr/bin/env python3
"""
Full-reel compositor for Abik's manual-edit look (EDITING_SYSTEM.md §22). Builds on manual_look.py
(tracked text, yellow keyword, cover ring) and adds the rest of his edit: peach caption pills, recordings with the
presenter cut-out, full-screen b-roll with a pan, number cards from the course covers, logos, the logo on the chest,
the { curated } end card and the loader.

A reel is a list of beats. Every beat (except the loader) names the A-roll source frames whose sound plays under it,
so cutting pauses and letting the voice run under graphics both fall out of the beat list. All text times inside a
beat are A-roll source frames. See gen_reel12.py for a complete plan.
"""
import os, glob, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageOps
import manual_look as ML

W, H, FPS = ML.W, ML.H, ML.FPS
FONT_MED = '/Library/Fonts/SF-Pro-Display-Medium.otf'
FONT_SEMI = '/Library/Fonts/SF-Pro-Display-Semibold.otf'
FONT_BOLD = '/Library/Fonts/SF-Pro-Display-Bold.otf'
PEACH, PILL_TEXT = (239, 177, 118), (38, 27, 20)
BG = (246, 246, 249)
INK = (30, 30, 32)
FFMPEG = ML.FFMPEG


# ------------------------------------------------------------------ media cache
class Media:
    def __init__(self, work):
        self.work = work; self.cache = {}

    def seq(self, key, path, start_s=0.0, n=None, vf=None, alpha=False):
        d = os.path.join(self.work, key)
        ext = 'png' if alpha else 'jpg'
        if not glob.glob(os.path.join(d, '*.' + ext)):
            os.makedirs(d, exist_ok=True)
            cmd = [FFMPEG, '-v', 'error', '-y', '-ss', str(start_s), '-i', path]
            if n: cmd += ['-frames:v', str(n)]
            cmd += ['-vf', f'fps={FPS}' + (',' + vf if vf else '')]
            cmd += (['-pix_fmt', 'rgba'] if alpha else ['-q:v', '2']) + ['-start_number', '0', os.path.join(d, 'f_%04d.' + ext)]
            subprocess.run(cmd, check=True)
        files = sorted(glob.glob(os.path.join(d, '*.' + ext)))
        return lambda i: Image.open(files[max(0, min(len(files) - 1, i))])


# ------------------------------------------------------------------ drawing helpers
def text_im(text, path, size, fill, track):
    return ML.draw_text(text, path, size, fill, track)


def paste(canvas, im, x, y):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.paste(im, (round(x), round(y)), im if im.mode == 'RGBA' else None)
    canvas.alpha_composite(layer)


def fade(im, a):
    if a >= 1: return im
    out = im.copy(); out.putalpha(im.split()[3].point(lambda v: int(v * a))); return out


_pill_cache = {}


def pill(text):
    if text not in _pill_cache:
        t, asc = text_im(text, FONT_MED, 58, PILL_TEXT, -40)
        cap = round(0.72 * 58)
        w, h = t.width + 2 * 22, cap + 2 * 19
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=18, fill=PEACH + (255,))
        im.alpha_composite(t, (22, 19 + cap - asc))
        _pill_cache[text] = im
    return _pill_cache[text]


def draw_pills(canvas, pills, sf, default_y):
    for p in pills or []:
        text, s0, s1 = p[0], p[1], p[2]; y = p[3] if len(p) > 3 else default_y
        if s0 <= sf < s1:
            im = pill(text); paste(canvas, im, W / 2 - im.width / 2, y * H - im.height / 2)


def draw_words(canvas, words, sf, behind):
    for wd in words or []:
        if bool(wd.get('behind')) != behind or not (wd['start'] <= sf < wd['end']):
            continue
        st = wd['style']
        path = {'small': FONT_SEMI, 'key': FONT_BOLD, 'med': FONT_MED, 'keymed': FONT_MED}[st]
        yellow = st in ('key', 'keymed')
        size = wd.get('size') or (ML.fit_size(wd['text'], path, wd.get('max_px', ML.KEY_MAX_PX), wd.get('fit_w', ML.KEY_W) * W) if yellow else ML.SMALL_PX)
        im, asc = text_im(wd['text'], path, size, ML.YELLOW if yellow else ML.WHITE, ML.TRACK)
        a, dy = 1.0, 0
        if yellow:                                       # Impact Text Animator in: fade + push up
            p = ML.ease((sf - wd['start'] + 1) / 5); a, dy = p, round((1 - p) * 0.07 * size)
        x = wd['x'] * W - (im.width if wd.get('align') == 'r' else im.width / 2 if wd.get('align') == 'c' else 0)
        paste(canvas, fade(im, a), x, wd['y'] * H - asc + dy)


def placed(im, scale, pos):
    """image scaled (percent) with its centre at normalised pos, as a full-frame RGBA layer"""
    s = scale / 100
    im2 = im if s == 1 else im.resize((round(im.width * s), round(im.height * s)), Image.BICUBIC)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    layer.paste(im2, (round(pos[0] * W - im2.width / 2), round(pos[1] * H - im2.height / 2)))
    return layer


# ------------------------------------------------------------------ number card
CARD_COL = {1: ((226, 226, 220), (62, 68, 54)), 2: ((243, 236, 218), (62, 68, 54)), 3: ((247, 226, 226), (122, 42, 58)),
            4: ((218, 227, 240), (31, 111, 184)), 5: ((216, 226, 240), (44, 140, 131))}
_card_cache = {}


def card_static(n, cover_path, col=None):
    """n: the numeral, or None for a plain card (cover + title only); col: which CARD_COL entry to use for a plain card"""
    key = (n, cover_path)
    if key not in _card_cache:
        num_col, ink = CARD_COL[n or col]
        base = Image.new('RGBA', (W, H), BG + (255,))
        if n:
            t, asc = text_im(str(n), FONT_BOLD, 2650, num_col, 0)
            # numeral: cap height ~1.0 H, centred a little right of the middle so it bleeds off the frame
            cap = round(0.705 * 2650)
            paste(base, t, 0.56 * W - t.width / 2, 0.5 * H + cap / 2 - asc)
        cov = Image.open(cover_path).convert('RGBA')
        ch = 450; cov = cov.resize((round(cov.width * ch / cov.height), ch), Image.LANCZOS)
        _card_cache[key] = (base, cov, ink)
    return _card_cache[key]


def render_card(b, lf, sf):
    base, cov, ink = card_static(b.get('n'), b['cover'], b.get('col'))
    canvas = base.copy()
    p = 1 - (1 - min(1.0, (lf + 1) / 9)) ** 3            # cover slides in from the left, easing out
    cx = -0.25 + (0.5 + 0.25) * p
    rot = (1 - p) * 14
    c = cov.rotate(rot, resample=Image.BICUBIC, expand=True) if rot > 0.3 else cov
    paste(canvas, c, cx * W - c.width / 2, 0.40 * H - c.height / 2)
    y = 0.545
    for text, kind, s0 in b['lines']:
        if kind == 'lead':
            size = 62; im, asc = text_im(text, FONT_BOLD, size, ink, -20); base_y = y + 0.705 * size / H; y = base_y + 0.012
        else:
            size = ML.fit_size(text, FONT_BOLD, 230, 0.79 * W, -30); im, asc = text_im(text, FONT_BOLD, size, ink, -30)
            base_y = y + 0.705 * size / H; y = base_y + 0.013
        if sf >= s0:
            paste(canvas, fade(im, min(1.0, (sf - s0 + 1) / 4)), W / 2 - im.width / 2, base_y * H - asc)
    return canvas


# ------------------------------------------------------------------ logos
def logo_images(man):
    net = Image.open(os.path.join(man, 'Netflix_2015_logo.svg.webp')).convert('RGBA')
    net = net.resize((round(net.width * 0.18), round(net.height * 0.18)), Image.LANCZOS)
    ub = Image.open(os.path.join(man, '5ij5qdSHFzJ2piPRuoTL5F.jpg')).convert('L')
    ub = ub.resize((round(ub.width * 0.33), round(ub.height * 0.33)), Image.LANCZOS)
    uber = Image.new('RGBA', ub.size, (0, 0, 0, 255)); uber.putalpha(ub.point(lambda v: 0 if v < 60 else min(255, int((v - 60) * 1.4))))   # invert + luma key: black wordmark only
    return {'netflix': (net, 0.2875, 3), 'uber': (uber, 0.283, 2)}


# ------------------------------------------------------------------ render
def render(plan, out, work):
    os.makedirs(work, exist_ok=True)
    M = Media(work)
    aroll = M.seq('src', plan['aroll'])
    matte_dir = plan['matte_dir']
    cut = lambda sf: Image.open(os.path.join(matte_dir, f'f_{sf:04d}.png'))
    covers = [Image.open(p).convert('RGBA') for p in plan['covers']]
    logos = logo_images(plan['man'])
    loader = M.seq('loader', plan['loader'], vf='scale=iw*0.44:-2', alpha=True)
    out_dir = os.path.join(work, 'out'); shutil.rmtree(out_dir, ignore_errors=True); os.makedirs(out_dir)
    t = 0; starts = []
    for bi, b in enumerate(plan['beats']):
        starts.append(t)
        n = b['n_frames'] if b['type'] == 'loader' else b['src'][1] - b['src'][0]
        if b['type'] == 'rec':
            rec = M.seq(f"rec_{bi}", b['file'], vf=f"scale={round(1526 * b.get('rec_scale', 70.8) / 100)}:-2")
        if b['type'] == 'broll':
            br = M.seq(f"broll_{bi}", b['file'], start_s=b['in_s'], n=n + 2, vf=f"scale={round(b['frame_w'] * b['scale'] / 100)}:-2")
        for lf in range(n):
            sf = (b['src'][0] + lf) if b['type'] != 'loader' else None
            ty = b['type']
            if ty == 'pres':
                scale, pos = ML.kf(b['scale'], lf), ML.kf(b['pos'], lf)
                canvas = Image.new('RGBA', (W, H), (0, 0, 0, 255))
                canvas.alpha_composite(placed(aroll(sf).convert('RGBA'), scale, pos))
                ring = b.get('ring'); has_behind = any(w.get('behind') and w['start'] <= sf < w['end'] for w in b.get('words', []))
                ring_on = ring and ring['start'] <= sf < ring['start'] + ring['frames']
                if ring_on:
                    p = (sf - ring['start']) / ring['frames']
                    canvas.alpha_composite(ML.render_ring(covers, 0.27 - 1.34 * p, cx=0.5, cy=0.205, radius=560, card_h=647))
                draw_words(canvas, b.get('words'), sf, True)
                if ring_on or has_behind:
                    canvas.alpha_composite(placed(cut(sf).convert('RGBA'), scale, pos))
                draw_words(canvas, b.get('words'), sf, False)
                draw_pills(canvas, b.get('pills'), sf, 0.66)
                lc = b.get('logo_chest')
                if lc and sf >= lc['start']:
                    im = loader((sf - lc['start']) * 2).convert('RGBA')          # 200% speed, tinted white
                    white = Image.new('RGBA', im.size, (255, 255, 255, 0)); white.putalpha(im.split()[3])
                    paste(canvas, white, 0.5 * W - im.width / 2, lc.get('y', 0.667) * H - im.height / 2)
            elif ty == 'rec':
                canvas = Image.new('RGBA', (W, H), (255, 255, 255, 255))
                fr = rec(min(b.get('in_f', 0) + lf, b.get('max_f', 10 ** 6))).convert('RGBA')      # max_f: hold the scroll there
                rp = b.get('rec_pos', [0.5, 0.5])
                paste(canvas, fr, rp[0] * W - fr.width / 2, rp[1] * H - fr.height / 2)
                for which, s0, s1 in b.get('logos', []):
                    if s0 <= sf < s1:
                        im, y, pop = logos[which]; k = min(1.0, (sf - s0 + 1) / pop)
                        im2 = im if k >= 1 else im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))))
                        paste(canvas, im2, 0.5 * W - im2.width / 2, y * H - im2.height / 2)
                canvas.alpha_composite(placed(cut(sf).convert('RGBA'), b['cut_scale'], b['cut_pos']))
                draw_pills(canvas, b.get('pills'), sf, b.get('pill_y', 0.47))
            elif ty == 'broll':
                canvas = Image.new('RGBA', (W, H), (0, 0, 0, 255))
                fr = br(lf).convert('RGBA'); pos = ML.kf(b['pos'], lf)
                paste(canvas, fr, pos[0] * W - fr.width / 2, pos[1] * H - fr.height / 2)
                draw_words(canvas, b.get('words'), sf, False)
                draw_pills(canvas, b.get('pills'), sf, 0.66)
            elif ty == 'card':
                canvas = render_card(b, lf, sf)
            elif ty == 'end':
                canvas = Image.new('RGBA', (W, H), BG + (255,))
                for text, s0, s1 in b['words']:
                    if s0 <= sf < s1:
                        im, asc = text_im(text, FONT_SEMI, 98, INK, -83)
                        paste(canvas, im, W / 2 - im.width / 2, 0.5 * H + 0.35 * 98 - asc)
            else:   # loader on the end-card white
                canvas = Image.new('RGBA', (W, H), BG + (255,))
                im = loader(lf).convert('RGBA'); paste(canvas, im, W / 2 - im.width / 2, H / 2 - im.height / 2)
            canvas.convert('RGB').save(os.path.join(out_dir, f'o_{t:04d}.jpg'), quality=95)
            t += 1
    total = t
    # ---- audio
    ins = ['-i', plan['aroll']]; fc = []; segs = []
    voiced = [b for b in plan['beats'] if b['type'] != 'loader']
    for i, b in enumerate(voiced):
        fc.append(f"[0:a]atrim={b['src'][0] / FPS}:{b['src'][1] / FPS},asetpts=PTS-STARTPTS[d{i}]"); segs.append(f'[d{i}]')
    fc.append(''.join(segs) + f"concat=n={len(segs)}:v=0:a=1,apad=whole_dur={total / FPS}[dlg]"); mix = ['[dlg]']; k = 1
    for s in plan['audio'](starts, total):
        ins += ['-i', s['file']]
        dur = (s['end'] - s['start']) / FPS; sp = s.get('speed', 1.0)
        ch = f"[{k}:a]atrim={s['in_s']}:{s['in_s'] + dur * sp},asetpts=PTS-STARTPTS"
        if sp != 1.0: ch += f",asetrate=48000*{sp}"
        ch += f",aresample=48000,volume={s.get('gain_db', 0)}dB"
        if s.get('fade_out'): ch += f",afade=t=out:st={max(0, dur - s['fade_out'] / FPS)}:d={s['fade_out'] / FPS}"
        ch += f",adelay={round(max(0, s['start']) / FPS * 1000)}:all=1[s{k}]"
        fc.append(ch); mix.append(f'[s{k}]'); k += 1
    fc.append(''.join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,alimiter=limit=0.89:level=false,atrim=0:{total / FPS}[a]")
    subprocess.run([FFMPEG, '-v', 'error', '-y'] + ins + ['-framerate', str(FPS), '-i', os.path.join(out_dir, 'o_%04d.jpg'),
                    '-filter_complex', ';'.join(fc), '-map', f'{k}:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', '-t', str(total / FPS), out], check=True)
    return total, starts
