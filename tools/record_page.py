#!/usr/bin/env python3
"""
Record a real browser session of a fanout.sh page as a frame sequence → ProRes mov,
in the same narrow portrait window Abik's reference recordings use (763 css px wide, 2x).

  scroll mode:    python3 record_page.py URL out.mov --mode scroll --frames 60 --speed 60 [--start 0] [--lead 8]
  drag mode:      python3 record_page.py URL out.mov --mode drag --frames 40 --selector "input[type=range]" --index 2

- 24 fps, one screenshot per frame, constant scroll speed (css px/frame) with a 4-frame ease-in,
  `--lead` extra frames rendered before frame 0 so the clip is already moving at its first frame.
- The mouse moves along a gentle path so hover states render; a macOS-style cursor is composited.
- The "BEST EXPERIENCED ON DESKTOP" banner and the coupon popup are removed every frame.
"""
import argparse, os, subprocess, tempfile, shutil, math, io, time
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = 'ffmpeg'
FPS = 24
VW, VH, DPR = 763, 950, 2   # overridden by --vh

CLEAN_JS = """
() => {
  const kill = (needle) => { for (const el of document.querySelectorAll('div,section,aside,button')) {
      if (el.innerText && el.innerText.trim().toUpperCase().startsWith(needle)) { el.remove(); return true; } } return false; };
  kill('BEST EXPERIENCED ON DESKTOP');
  for (const el of document.querySelectorAll('div')) {
    const t = el.innerText || '';
    if (t.includes('LAUNCH30') && el.getBoundingClientRect().width < 500) { el.closest('[role=dialog]') ? el.closest('[role=dialog]').remove() : el.remove(); break; }
  }
  document.querySelectorAll('[role=dialog]').forEach(d => { if ((d.innerText||'').includes('% off')) d.remove(); });
}
"""


def cursor_image(scale=2):
    s = 22 * scale
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(0, 0), (0, 16), (4, 12), (7, 19), (10, 18), (7, 11), (12, 11)]
    pts = [(x * scale, y * scale) for x, y in pts]
    d.polygon(pts, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    d.line(pts + [pts[0]], fill=(0, 0, 0, 255), width=scale)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url'); ap.add_argument('out')
    ap.add_argument('--mode', default='scroll', choices=['scroll', 'drag'])
    ap.add_argument('--frames', type=int, default=60); ap.add_argument('--lead', type=int, default=8)
    ap.add_argument('--speed', type=float, default=60, help='css px per frame (scroll mode)')
    ap.add_argument('--start', type=int, default=0, help='initial scroll offset (css px)')
    ap.add_argument('--selector', default='input[type=range]'); ap.add_argument('--index', type=int, default=0)
    ap.add_argument('--drag-to', type=float, default=0.85, help='drag mode: target fraction of the slider width')
    ap.add_argument('--settle', type=int, default=6, help='drag mode: frames to hold before the drag starts')
    ap.add_argument('--vh', type=int, default=950, help='viewport height in css px (1356 = 9:16 at 763 wide)')
    a = ap.parse_args()
    global VH
    VH = a.vh
    tmp = tempfile.mkdtemp(); cur = cursor_image(DPR)
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        ctx = br.new_context(viewport={'width': VW, 'height': VH}, device_scale_factor=DPR)
        page = ctx.new_page()
        page.goto(a.url, wait_until='load', timeout=90000)
        page.wait_for_timeout(2500)
        # force lazy content to load, then return
        total = page.evaluate('document.documentElement.scrollHeight')
        for y in range(0, int(total), 600):
            page.evaluate(f'window.scrollTo(0,{y})'); page.wait_for_timeout(40)
        page.evaluate(f'window.scrollTo(0,{a.start})'); page.wait_for_timeout(300)
        page.evaluate(CLEAN_JS)
        n = a.frames + a.lead
        frames = []
        if a.mode == 'scroll':
            y = float(a.start); mx, my = VW * 0.55, VH * 0.45
            for i in range(n):
                ease = min(1.0, (i + 1) / 4.0)
                y += a.speed * ease
                page.evaluate(f'window.scrollTo(0,{int(y)})')
                mx = VW * (0.55 + 0.06 * math.sin(i / 9.0)); my = VH * (0.45 + 0.05 * math.cos(i / 7.0))
                page.mouse.move(mx, my)
                page.evaluate(CLEAN_JS)
                page.wait_for_timeout(30)
                frames.append((page.screenshot(type='png'), mx, my))
        else:
            el = page.locator(a.selector).nth(a.index)
            el.scroll_into_view_if_needed(); page.wait_for_timeout(200)
            page.evaluate('window.scrollBy(0,-220)'); page.wait_for_timeout(200)
            box = el.bounding_box()
            x0 = box['x'] + box['width'] * 0.12; x1 = box['x'] + box['width'] * a.drag_to; yy = box['y'] + box['height'] / 2
            # current thumb position: read value/min/max
            vals = el.evaluate('e => [parseFloat(e.value), parseFloat(e.min||0), parseFloat(e.max||100)]')
            frac = (vals[0] - vals[1]) / max(1e-9, (vals[2] - vals[1]))
            xs = box['x'] + box['width'] * frac
            mx, my = xs, yy + 60
            for i in range(n):
                if i < a.lead + a.settle:
                    t = (i + 1) / (a.lead + a.settle)
                    mx = xs + (0 - 0) ; my = yy + 60 * (1 - t)
                    page.mouse.move(mx, my)
                    if i == a.lead + a.settle - 1:
                        page.mouse.down()
                else:
                    t = min(1.0, (i - a.lead - a.settle + 1) / max(1, n - a.lead - a.settle - 4))
                    te = 0.5 - 0.5 * math.cos(math.pi * t)
                    mx = xs + (x1 - xs) * te; my = yy
                    page.mouse.move(mx, my)
                page.evaluate(CLEAN_JS)
                page.wait_for_timeout(30)
                frames.append((page.screenshot(type='png'), mx, my))
            page.mouse.up()
        br.close()
    for i, (png, mx, my) in enumerate(frames[a.lead:]):
        im = Image.open(io.BytesIO(png)).convert('RGBA')
        im.alpha_composite(cur, (int(mx * DPR), int(my * DPR)))
        im.convert('RGB').save(os.path.join(tmp, f'f_{i:04d}.png'))
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, 'f_%04d.png'),
                    '-c:v', 'prores_ks', '-profile:v', '2', '-pix_fmt', 'yuv422p10le', a.out], check=True)
    shutil.rmtree(tmp)
    print(a.out, f'{len(frames) - a.lead} frames', f'{VW * DPR}x{VH * DPR}')


if __name__ == '__main__':
    main()
