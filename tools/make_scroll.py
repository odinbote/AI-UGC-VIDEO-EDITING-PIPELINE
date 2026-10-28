#!/usr/bin/env python3
"""
Turn a tall full-page screenshot into a smooth "screen recording" that scrolls the page.

    python3 make_scroll.py page.png out.mov --vw 2560 --vh 1600 --start 0 --end 2400 --dur 3.0 [--hold 0.3]

The viewport (vw x vh) pans from scroll offset `start` to `end` (pixels of the capture) over
`dur` seconds with an ease-in-out, after holding `hold` seconds at the start. 24 fps, ProRes 422.
"""
import argparse, os, subprocess, math, tempfile, shutil
from PIL import Image

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = 'ffmpeg'
FPS = 24


def ease(p):
    return 0.5 - 0.5 * math.cos(math.pi * p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--vw', type=int, default=2560); ap.add_argument('--vh', type=int, default=1600)
    ap.add_argument('--start', type=int, default=0); ap.add_argument('--end', type=int, required=True)
    ap.add_argument('--dur', type=float, default=3.0); ap.add_argument('--hold', type=float, default=0.3)
    ap.add_argument('--tail', type=float, default=0.5, help='hold at the end')
    ap.add_argument('--x', type=int, default=0, help='left edge of the viewport in the capture')
    a = ap.parse_args()
    im = Image.open(a.src).convert('RGB')
    end = min(a.end, im.height - a.vh)
    tmp = tempfile.mkdtemp()
    n_hold, n_move, n_tail = round(a.hold * FPS), round(a.dur * FPS), round(a.tail * FPS)
    i = 0
    for k in range(n_hold + n_move + n_tail):
        if k < n_hold:
            off = a.start
        elif k < n_hold + n_move:
            off = a.start + (end - a.start) * ease((k - n_hold) / max(1, n_move - 1))
        else:
            off = end
        off = int(round(off))
        im.crop((a.x, off, a.x + a.vw, off + a.vh)).save(os.path.join(tmp, f'f_{i:04d}.png')); i += 1
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, 'f_%04d.png'),
                    '-c:v', 'prores_ks', '-profile:v', '2', '-pix_fmt', 'yuv422p10le', a.out], check=True)
    shutil.rmtree(tmp)
    print(a.out, f'{i} frames ({i / FPS:.2f} s)', f'{a.vw}x{a.vh}')


if __name__ == '__main__':
    main()
