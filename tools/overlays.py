#!/usr/bin/env python3
"""
Overlay devices learned from the UGC reference study, for render_preview.py.

Plan entries live in plan["overlays"], each {type, start_f, end_f, ...}:
  caption_kw   text with one keyword in brand colour (bold sans, stroke)   {text, kw, y}
  topcard      white rounded headline card at the top, brand highlight     {lines:[...], hl:"word"}
  counter      dark stat card: label + number counting up                  {label, n, suffix, sub, x, y}
  stamp        verdict pill popping in (red/green)                         {text, color, x, y}
  emoji        emoji popping in next to a position                         {char, x, y}
  freeze       blurred, darkened freeze of the presenter + giant text      {text, sub}   (replaces frame)
  diagram      dark-navy animated system diagram                           {kind:"request_path"} (replaces frame)
  split        presenter bottom half + card/recording top half             {src_dir}     (replaces frame)
  flash        white flash                                                 {}
  endcard      brand end card                                              {url, cta}    (replaces frame)
"""
import math, os, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 24
BRAND = (255, 122, 26)        # orange keyword / highlight
GREEN = (46, 204, 113)
RED = (235, 64, 52)
NAVY = (11, 20, 48)
CARD = (16, 21, 34)
HOME = os.path.expanduser('~')
F_BOLD = f'{HOME}/Library/Fonts/SF-Pro-Display-Bold.otf'
F_HEAVY = f'{HOME}/Library/Fonts/SF-Pro-Display-Heavy.otf'
F_SEMI = f'{HOME}/Library/Fonts/SF-Pro-Display-Semibold.otf'
F_MONO = '/System/Library/Fonts/Menlo.ttc'
F_EMOJI = '/System/Library/Fonts/Apple Color Emoji.ttc'
HERE = os.path.dirname(os.path.abspath(__file__))
F_SERIF = os.path.join(HERE, '..', 'reference', 'fonts', 'InstrumentSerif-Italic.ttf')


def font(path, size):
    return ImageFont.truetype(path, size)


def ease_out(p, k=2.4):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** k


def pop(p):
    """overshoot pop: 0.6 -> 1.06 -> 1.0"""
    p = max(0.0, min(1.0, p))
    if p < 0.6:
        return 0.6 + 0.46 * ease_out(p / 0.6)
    return 1.06 - 0.06 * ((p - 0.6) / 0.4)


def paste_center(canvas, im, cx, cy, scale=1.0):
    if scale != 1.0:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    x = round(cx * W - im.width / 2); y = round(cy * H - im.height / 2)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.paste(im, (x, y)); canvas.alpha_composite(layer)


def text_img(text, fnt, fill, stroke=0, stroke_fill=(0, 0, 0)):
    d = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    l, t, r, b = d.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    im = Image.new('RGBA', (r - l + 2 * stroke + 4, b - t + 2 * stroke + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((stroke + 2 - l, stroke + 2 - t), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im


# ---------------------------------------------------------------- caption with keyword
def caption_kw(canvas, ov, fl):
    size = ov.get('size', 66); fnt = font(F_BOLD, size)
    words = ov['text'].split(' '); kw = ov.get('kw', '')
    gap = size * 0.2
    parts = [text_img(w, fnt, BRAND if w.strip('.,!?') == kw else (255, 255, 255), stroke=5) for w in words]
    total = sum(p.width for p in parts) + gap * (len(parts) - 1)
    line = Image.new('RGBA', (int(total) + 4, max(p.height for p in parts)), (0, 0, 0, 0)); x = 0
    for p in parts:
        line.paste(p, (int(x), 0)); x += p.width + gap
    if ov.get('pill', True):
        px, py = 28, 14
        pil = Image.new('RGBA', (line.width + 2 * px, line.height + 2 * py), (0, 0, 0, 0))
        ImageDraw.Draw(pil).rounded_rectangle((0, 0, pil.width - 1, pil.height - 1), radius=22, fill=(8, 8, 12, 200))
        pil.alpha_composite(line, (px, py)); line = pil
    a = ease_out(fl / 3.0)
    if a < 1:
        line.putalpha(line.split()[3].point(lambda v: int(v * a)))
    paste_center(canvas, line, 0.5, ov.get('y', 0.70) + (1 - a) * 0.01)


# ---------------------------------------------------------------- top headline card
def topcard(canvas, ov, fl, dur):
    lines = ov['lines']; hl = ov.get('hl'); fnt = font(F_HEAVY, ov.get('size', 54))
    pad = 34; lh = int(fnt.size * 1.25)
    rows = []
    for ln in lines:
        words = ln.split(' '); imgs = []
        for w in words:
            if hl and w.upper() == hl.upper():
                t = text_img(w, fnt, (255, 255, 255)); bg = Image.new('RGBA', (t.width + 18, t.height + 6), BRAND + (255,))
                bg.alpha_composite(t, (9, 3)); imgs.append(bg)
            else:
                imgs.append(text_img(w, fnt, NAVY))
        wgap = int(fnt.size * 0.3)
        row = Image.new('RGBA', (sum(i.width for i in imgs) + wgap * (len(imgs) - 1), lh), (0, 0, 0, 0)); x = 0
        for i in imgs:
            row.paste(i, (x, (lh - i.height) // 2)); x += i.width + wgap
        rows.append(row)
    cw = max(r.width for r in rows) + 2 * pad; ch = lh * len(rows) + 2 * pad - 8
    card = Image.new('RGBA', (cw + 12, ch + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle((6, 10, cw + 6, ch + 10), radius=18, fill=(0, 0, 0, 70))
    d.rounded_rectangle((6, 6, cw + 6, ch + 6), radius=18, fill=(255, 255, 255, 255), outline=NAVY + (255,), width=3)
    y = pad + 6
    for r in rows:
        card.alpha_composite(r, ((cw - r.width) // 2 + 6, y)); y += lh
    p = ease_out(fl / 8.0)
    paste_center(canvas, card, 0.5, ov.get('y', 0.14) - (1 - p) * 0.08)


# ---------------------------------------------------------------- counter card
def counter(canvas, ov, fl):
    n = ov['n']; p = ease_out(fl / 14.0, 3)
    val = int(round(n * p)); shown = f"{val:,}{ov.get('suffix', '')}"
    cw, ch = ov.get('w', 640), ov.get('h', 330)
    card = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=28, fill=CARD + (245,), outline=(60, 70, 95, 255), width=2)
    lab = text_img(ov['label'].upper(), font(F_SEMI, 30), (160, 170, 195)); card.alpha_composite(lab, ((cw - lab.width) // 2, 34))
    num = text_img(shown, font(F_HEAVY, ov.get('num_size', 150)), (255, 255, 255)); card.alpha_composite(num, ((cw - num.width) // 2, 78))
    if ov.get('sub'):
        sub = text_img(ov['sub'], font(F_SEMI, 32), BRAND); card.alpha_composite(sub, ((cw - sub.width) // 2, ch - 70))
    paste_center(canvas, card, ov.get('x', 0.5), ov.get('y', 0.22), pop(fl / 7.0))


# ---------------------------------------------------------------- stamp
def stamp(canvas, ov, fl):
    col = GREEN if ov.get('color', 'green') == 'green' else RED
    fnt = font(F_HEAVY, ov.get('size', 92)); t = text_img(ov['text'].upper(), fnt, col, stroke=3, stroke_fill=(0, 0, 0))
    pw, ph = t.width + 70, t.height + 36
    glow = Image.new('RGBA', (pw + 80, ph + 80), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle((40, 40, 40 + pw, 40 + ph), radius=22, fill=col + (110,)); glow = glow.filter(ImageFilter.GaussianBlur(18))
    pill = Image.new('RGBA', (pw + 80, ph + 80), (0, 0, 0, 0)); pill.alpha_composite(glow)
    d = ImageDraw.Draw(pill); d.rounded_rectangle((40, 40, 40 + pw, 40 + ph), radius=22, fill=(8, 10, 14, 235), outline=col + (255,), width=5)
    pill.alpha_composite(t, (40 + 35, 40 + 18))
    paste_center(canvas, pill, ov.get('x', 0.5), ov.get('y', 0.62), pop(fl / 6.0))


# ---------------------------------------------------------------- emoji pop
def emoji(canvas, ov, fl):
    try:
        fnt = ImageFont.truetype(F_EMOJI, 160)
        im = Image.new('RGBA', (240, 240), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((0, 0, 239, 239), fill=CARD + (235,), outline=(70, 80, 105, 255), width=4)
        d.text((40, 30), ov['char'], font=fnt, embedded_color=True)
    except Exception:
        return
    paste_center(canvas, im, ov.get('x', 0.5), ov.get('y', 0.5), pop(fl / 6.0) * ov.get('scale', 0.9))


# ---------------------------------------------------------------- freeze beat
def freeze(canvas, ov, fl, aroll_frame):
    base = aroll_frame.convert('RGB').resize((W, H)).filter(ImageFilter.GaussianBlur(22))
    base = Image.blend(base, Image.new('RGB', (W, H), (10, 10, 14)), 0.55).convert('RGBA')
    canvas.paste(base, (0, 0))
    big = text_img(ov['text'], font(F_HEAVY, ov.get('size', 230)), BRAND, stroke=0)
    paste_center(canvas, big, 0.5, 0.47, pop(fl / 5.0))
    if ov.get('sub'):
        sub = text_img(ov['sub'].upper(), font(F_BOLD, 54), (255, 255, 255)); paste_center(canvas, sub, 0.5, 0.36)


# ---------------------------------------------------------------- diagram insert
def diagram(canvas, ov, fl, dur):
    canvas.paste(Image.new('RGBA', (W, H), NAVY + (255,)), (0, 0))
    d = ImageDraw.Draw(canvas)
    # subtle grid
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(18, 30, 64, 255), width=1)
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(18, 30, 64, 255), width=1)
    line = (120, 190, 255); mono = font(F_MONO, 34); lab = font(F_SEMI, 40)
    nodes = ov.get('nodes', [('CLIENT', 0.5, 0.18), ('LOAD BALANCER', 0.5, 0.36), ('API', 0.5, 0.54), ('CACHE', 0.27, 0.74), ('DATABASE', 0.73, 0.74)])
    edges = ov.get('edges', [(0, 1), (1, 2), (2, 3), (2, 4)])
    total = len(nodes) + len(edges); per = max(1, (dur - 10) // total)
    def pt(i):
        return (nodes[i][1] * W, nodes[i][2] * H)
    step = 0
    for i, (name, nx, ny) in enumerate(nodes):
        p = ease_out((fl - step * per) / per); step += 1
        if p <= 0: continue
        bw, bh = 400 * p, 120 * p; cx, cy = nx * W, ny * H
        d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), radius=16, outline=line + (255,), width=4, fill=(14, 26, 60, 255))
        if p > 0.7:
            t = text_img(name, lab, (230, 240, 255)); canvas.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))
        # edges that end at this node draw right after it
        for (a, b) in edges:
            if b == i:
                q = ease_out((fl - step * per) / per); step += 1
                if q <= 0: continue
                ax, ay = pt(a); bx, by = pt(b); ay += 60; by -= 60
                ex, ey = ax + (bx - ax) * q, ay + (by - ay) * q
                d.line([(ax, ay), (ex, ey)], fill=GREEN + (255,), width=6)
                if q >= 1:
                    ang = math.atan2(by - ay, bx - ax)
                    d.polygon([(bx, by), (bx - 22 * math.cos(ang - 0.5), by - 22 * math.sin(ang - 0.5)), (bx - 22 * math.cos(ang + 0.5), by - 22 * math.sin(ang + 0.5))], fill=GREEN + (255,))
    if ov.get('title'):
        t = text_img(ov['title'].upper(), mono, (160, 180, 220)); canvas.alpha_composite(t, (int(W / 2 - t.width / 2), 90))


# ---------------------------------------------------------------- split frame
def split(canvas, ov, fl, top_img, aroll_frame):
    canvas.paste(Image.new('RGBA', (W, H), (20, 20, 22, 255)), (0, 0))
    m = 40; th = int(H * 0.47); bh = H - th - 3 * m
    def rounded(im, w, h, r=36):
        im = im.convert('RGB').resize((w, h)); mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255)
        out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); out.paste(im, (0, 0), mask); return out
    # top: crop the middle of the recording frame to the card aspect
    tw = W - 2 * m; src = top_img.convert('RGB'); ar = tw / th
    sw, sh = src.size
    if sw / sh > ar: nw = int(sh * ar); src = src.crop(((sw - nw) // 2, 0, (sw + nw) // 2, sh))
    else: nh = int(sw / ar); src = src.crop((0, int(sh * ov.get('top_focus', 0.08)), sw, int(sh * ov.get('top_focus', 0.08)) + nh))
    canvas.alpha_composite(rounded(src, tw, th), (m, m))
    # bottom: presenter crop (upper body)
    a = aroll_frame.convert('RGB'); aw, ah = a.size; ar2 = tw / bh
    nh = int(aw / ar2); a = a.crop((0, int(ah * 0.12), aw, int(ah * 0.12) + nh))
    canvas.alpha_composite(rounded(a, tw, bh), (m, th + 2 * m))


# ---------------------------------------------------------------- flash / end card
def flash(canvas, ov, fl, dur):
    a = int(255 * (1 - fl / max(1, dur)))
    canvas.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, max(0, a))))


def endcard(canvas, ov, fl, logo_img=None):
    canvas.paste(Image.new('RGBA', (W, H), (245, 245, 245, 255)), (0, 0))
    p = ease_out(fl / 8.0)
    if logo_img is not None:
        sc = min(1.0, (W * 0.62) / logo_img.width)
        paste_center(canvas, logo_img, 0.5, 0.40 - (1 - p) * 0.03, sc)
    t = text_img(ov.get('headline', 'Think like a senior engineer.'), font(F_SERIF, 92), (20, 20, 24)); paste_center(canvas, t, 0.5, 0.53)
    btn_t = text_img(ov.get('cta', 'Start learning free  →'), font(F_BOLD, 50), (255, 255, 255))
    bw, bh = btn_t.width + 90, btn_t.height + 50
    btn = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); ImageDraw.Draw(btn).rounded_rectangle((0, 0, bw - 1, bh - 1), radius=bh // 2, fill=BRAND + (255,)); btn.alpha_composite(btn_t, (45, 25))
    paste_center(canvas, btn, 0.5, 0.63, pop(fl / 7.0))
    u = text_img(ov.get('url', 'fanout.sh'), font(F_MONO, 44), (90, 90, 100)); paste_center(canvas, u, 0.5, 0.72)


REPLACERS = {'freeze', 'diagram', 'split', 'endcard'}


def draw_overlays(canvas, plan, f, ctx):
    """ctx: dict with aroll_frame(f)->Image, rec_frame(dir, i)->Image, logo_img"""
    active = [ov for ov in plan.get('overlays', []) if ov['start_f'] <= f < ov['end_f']]
    for ov in active:
        fl = f - ov['start_f']; dur = ov['end_f'] - ov['start_f']; t = ov['type']
        if t == 'freeze': freeze(canvas, ov, fl, ctx['aroll_frame'](ov.get('src_f', ov['start_f'])))
        elif t == 'diagram': diagram(canvas, ov, fl, dur)
        elif t == 'split': split(canvas, ov, fl, ctx['rec_frame'](ov['src_dir'], fl + ov.get('src_offset', 0)), ctx['aroll_frame'](f))
        elif t == 'endcard': endcard(canvas, ov, fl, ctx.get('logo_img'))
    for ov in active:
        fl = f - ov['start_f']; dur = ov['end_f'] - ov['start_f']; t = ov['type']
        if t == 'caption_kw': caption_kw(canvas, ov, fl)
        elif t == 'topcard': topcard(canvas, ov, fl, dur)
        elif t == 'counter': counter(canvas, ov, fl)
        elif t == 'stamp': stamp(canvas, ov, fl)
        elif t == 'emoji': emoji(canvas, ov, fl)
        elif t == 'flash': flash(canvas, ov, fl, dur)
