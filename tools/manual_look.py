#!/usr/bin/env python3
"""
Building blocks for Abik's manual-edit look (EDITING_SYSTEM.md §22, reference/abik manual edit 2026-11-13):
word-by-word hook text with one yellow keyword, the ring of fanout course covers behind the presenter's head,
and a small compositor that renders a preview from a "look plan" (a Python dict, see gen_reel10_hook.py).

All frame numbers are timeline frames at 24 fps; positions are normalised to the 1080x1920 frame.
"""
import os, math, subprocess, glob, shutil
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H, FPS = 1080, 1920, 24
YELLOW = (250, 222, 78)
WHITE = (255, 255, 255)
FONT_SEMI = os.path.expanduser('~/Library/Fonts/SF-Pro-Display-Semibold.otf')
FONT_BOLD = os.path.expanduser('~/Library/Fonts/SF-Pro-Display-Bold.otf')
SMALL_PX = 68          # small white words (SF Pro Semibold, tracking -49)
KEY_MAX_PX = 270       # keyword (SF Pro Bold, yellow); also fitted to KEY_W of the frame width
KEY_W = 0.75
TRACK = -49            # 1/1000 em

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = 'ffmpeg'


# ---------------------------------------------------------------- text
def text_width(text, font, track=TRACK):
    return sum(font.getlength(c) for c in text) + font.size * track / 1000 * (len(text) - 1)


def fit_size(text, path, max_px, width_px, track=TRACK):
    size = max_px
    while size > 20 and text_width(text, ImageFont.truetype(path, size), track) > width_px:
        size -= 2
    return size


def draw_text(text, path, size, fill, track=TRACK):
    """RGBA image of tracked text; returns (image, ascent) with the baseline at y = ascent."""
    font = ImageFont.truetype(path, size)
    asc, desc = font.getmetrics()
    w = int(math.ceil(text_width(text, font, track))) + 8
    im = Image.new('RGBA', (w, asc + desc + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); x = 2.0
    for c in text:
        d.text((x, 0), c, font=font, fill=fill + (255,))
        x += font.getlength(c) + size * track / 1000
    return im, asc


# ---------------------------------------------------------------- ring of covers
def _persp_coeffs(dst, src):
    """coefficients for Image.transform(PERSPECTIVE): maps output (dst) points to source points"""
    A = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    B = np.array(src).reshape(8)
    return np.linalg.solve(np.array(A, dtype=float), B)


def render_ring(covers, phase, cx=0.5, cy=0.21, radius=560, card_h=560, zoom=1800, dist=2200, tilt=0.0):
    """Five covers on a horizontal ring (after 3D_Horizontal_Image_Ring.jsx), camera in front.
    phase: rotation in turns (decreasing = covers travel right to left). Covers fade at the sides."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cards = []
    for i, im in enumerate(covers):
        turn = i / len(covers) + phase                  # unwrapped: each cover makes one pass across the front,
        if abs(turn) >= 0.25:                           # entering at +0.25 turn (right) and leaving at -0.25 (left)
            continue
        ang = 2 * math.pi * turn
        z = -math.cos(ang) * radius                     # negative = towards the camera
        if z > -0.05 * radius:
            continue
        cards.append((z, ang, im))
    for z, ang, im in sorted(cards, key=lambda c: -c[0]):   # far to near
        ch = card_h; cw = ch * im.width / im.height
        x0 = math.sin(ang) * radius
        dx, dz = math.cos(ang) * cw / 2, math.sin(ang) * cw / 2    # card faces outward from the ring centre
        pts3 = [(x0 - dx, -ch / 2, z - dz), (x0 + dx, -ch / 2, z + dz), (x0 + dx, ch / 2, z + dz), (x0 - dx, ch / 2, z - dz)]
        dst = []
        for (X, Y, Z) in pts3:
            m = zoom / (dist + Z)
            dst.append((cx * W + X * m, cy * H + Y * m))
        if dst[1][0] - dst[0][0] < 8:
            continue
        src = [(0, 0), (im.width, 0), (im.width, im.height), (0, im.height)]
        warped = im.transform((W, H), Image.PERSPECTIVE, _persp_coeffs(dst, src), Image.BICUBIC)
        face = -z / radius                               # 1 = dead centre front, 0 = side
        if face < 0.35:
            a = warped.split()[3].point(lambda v, f=face / 0.35: int(v * f)); warped.putalpha(a)
        layer.alpha_composite(warped)
    return layer


# ---------------------------------------------------------------- compositor
def ease(p):
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, p)))


def kf(v, f):
    """v: number/list, or {"kf": [[frame, value], [frame, value]]} with frames local to the piece"""
    if not isinstance(v, dict):
        return v
    (f0, a), (f1, b) = v['kf']
    p = ease((f - f0) / max(1, f1 - f0))
    return [a[i] + (b[i] - a[i]) * p for i in range(len(a))] if isinstance(a, list) else a + (b - a) * p


def place(canvas, im, scale, pos):
    s = scale / 100
    im2 = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS if s < 1 else Image.BICUBIC)
    x, y = round(pos[0] * W - im2.width / 2), round(pos[1] * H - im2.height / 2)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.paste(im2, (x, y))
    canvas.alpha_composite(layer)


def render(plan, out, work):
    """plan keys: aroll, matte_dir, pieces[{src_in, src_out, scale, pos}], words[...], ring{start,end,turns,phase0,covers}, audio{...}"""
    os.makedirs(work, exist_ok=True)
    src_dir = os.path.join(work, 'src')
    if not glob.glob(os.path.join(src_dir, '*.png')):
        os.makedirs(src_dir, exist_ok=True)
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', plan['aroll'], '-vf', f'fps={FPS}', '-start_number', '0', os.path.join(src_dir, 'f_%04d.png')], check=True)
    covers = [Image.open(p).convert('RGBA') for p in plan.get('ring', {}).get('covers', [])]
    out_dir = os.path.join(work, 'out'); shutil.rmtree(out_dir, ignore_errors=True); os.makedirs(out_dir)
    # timeline map
    tl = []
    for pc in plan['pieces']:
        for sf in range(pc['src_in'], pc['src_out']):
            tl.append((pc, sf - pc['src_in'], sf))
    words = []
    for wd in plan['words']:
        key = wd['style'] == 'key'
        path = FONT_BOLD if key else FONT_SEMI
        size = wd.get('size') or (fit_size(wd['text'], path, wd.get('max_px', KEY_MAX_PX), wd.get('fit_w', KEY_W) * W) if key else SMALL_PX)
        im, asc = draw_text(wd['text'], path, size, YELLOW if key else WHITE)
        words.append((wd, im, asc, size))
    ring = plan.get('ring')
    for t, (pc, lf, sf) in enumerate(tl):
        fr = Image.open(os.path.join(src_dir, f'f_{sf:04d}.png')).convert('RGBA')
        scale, pos = kf(pc['scale'], lf), kf(pc['pos'], lf)
        canvas = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        place(canvas, fr, scale, pos)
        behind = []
        if ring and ring['start'] <= t < ring['end']:
            p = (t - ring['start']) / (ring['end'] - ring['start'])
            behind.append(render_ring(covers, ring['phase0'] + ring['turns'] * p, **ring.get('geom', {})))
        front = []
        for wd, im, asc, size in words:
            if not (wd['start'] <= t < wd['end']):
                continue
            a, dy = 1.0, 0
            if wd['style'] == 'key':                     # Impact Text Animator in: fade + push up
                p = ease((t - wd['start'] + 1) / 5); a, dy = p, round((1 - p) * 0.35 * size * 0.2)
            x = wd['x'] * W - (im.width if wd.get('align') == 'r' else im.width / 2 if wd.get('align') == 'c' else 0)
            y = wd['y'] * H - asc + dy                    # wd['y'] is the baseline
            wim = im
            if a < 1:
                wim = im.copy(); wim.putalpha(im.split()[3].point(lambda v: int(v * a)))
            (behind if wd.get('behind') else front).append((wim, round(x), round(y)))
        if behind:
            for b in behind:
                if isinstance(b, tuple):
                    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.paste(b[0], (b[1], b[2])); canvas.alpha_composite(layer)
                else:
                    canvas.alpha_composite(b)
            cut = Image.open(os.path.join(plan['matte_dir'], f'f_{sf:04d}.png')).convert('RGBA')
            place(canvas, cut, scale, pos)
        for wim, x, y in front:
            layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.paste(wim, (x, y)); canvas.alpha_composite(layer)
        canvas.convert('RGB').save(os.path.join(out_dir, f'o_{t:04d}.png'))
    n = len(tl)
    # ---- audio: dialogue pieces, music, sfx
    A = plan['audio']; ins = ['-i', plan['aroll']]; fc = []; mix = []
    for i, pc in enumerate(plan['pieces']):
        fc.append(f"[0:a]atrim={pc['src_in'] / FPS}:{pc['src_out'] / FPS},asetpts=PTS-STARTPTS[d{i}]")
    fc.append(''.join(f'[d{i}]' for i in range(len(plan['pieces']))) + f"concat=n={len(plan['pieces'])}:v=0:a=1[dlg]"); mix.append('[dlg]')
    k = 1
    for s in A.get('layers', []):
        ins += ['-i', s['file']]
        dur = (s['end'] - s['start']) / FPS; sp = s.get('speed', 1.0)
        chain = f"[{k}:a]atrim={s['in_s']}:{s['in_s'] + dur * sp},asetpts=PTS-STARTPTS"
        if sp != 1.0:
            chain += f",asetrate=48000*{sp},aresample=48000"
        chain += f",aresample=48000,volume={s.get('gain_db', 0)}dB"
        if s.get('fade_out'):
            chain += f",afade=t=out:st={max(0, dur - s['fade_out'] / FPS)}:d={s['fade_out'] / FPS}"
        chain += f",adelay={round(max(0, s['start']) / FPS * 1000)}:all=1[s{k}]"
        fc.append(chain); mix.append(f'[s{k}]'); k += 1
    fc.append(''.join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{n / FPS}[a]")
    subprocess.run([FFMPEG, '-v', 'error', '-y'] + ins + ['-framerate', str(FPS), '-i', os.path.join(out_dir, 'o_%04d.png')] +
                   ['-filter_complex', ';'.join(fc), '-map', f'{k}:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', '-t', str(n / FPS), out], check=True)
    return n
