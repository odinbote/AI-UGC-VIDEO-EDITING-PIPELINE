#!/usr/bin/env python3
"""
Shot catalogue for a b-roll source: detects cuts, writes <key>_shots.json (in/out seconds per shot)
and thumbnail sheets <key>_pN.jpg labelled "#shot in-seconds +duration".

    python3 tools/catalog_shots.py <video> <key> <out_dir>
"""
import av, sys, json, numpy as np, os
from PIL import Image, ImageDraw
src, key, out = sys.argv[1], sys.argv[2], sys.argv[3]
c = av.open(src); v = c.streams.video[0]; v.thread_type = 'AUTO'
fps = float(v.average_rate); prev = None; shots = []; start = 0.0; thumbs = {}; frames = []
i = 0
for fr in c.decode(video=0):
    t = float(fr.pts * v.time_base)
    if i % 2 == 0:
        small = fr.reformat(width=96, height=54).to_ndarray(format='gray').astype(np.float32)
        if prev is not None:
            d = float(np.abs(small - prev).mean())
            if d > 16:
                shots.append((start, t)); start = t
        prev = small
    i += 1
shots.append((start, t))
shots = [(a, b) for a, b in shots if b - a >= 0.75]
# thumbnails at 40 % into each shot
want = sorted((a + (b - a) * 0.4, k) for k, (a, b) in enumerate(shots))
c = av.open(src); v = c.streams.video[0]; v.thread_type = 'AUTO'; wi = 0; got = {}
for fr in c.decode(video=0):
    t = float(fr.pts * v.time_base)
    while wi < len(want) and t >= want[wi][0]:
        got[want[wi][1]] = fr.reformat(width=240, height=135).to_image(); wi += 1
    if wi >= len(want): break
json.dump([{"k": k, "in": round(a, 2), "out": round(b, 2)} for k, (a, b) in enumerate(shots)], open(f"{out}/{key}_shots.json", "w"))
W, PER = 10, 70
for page in range(0, len(shots), PER):
    sub = list(range(page, min(page + PER, len(shots)))); rows = (len(sub) + W - 1) // W
    sh = Image.new('RGB', (240 * W, 150 * rows), 'black'); d = ImageDraw.Draw(sh)
    for j, k in enumerate(sub):
        x, y = (j % W) * 240, (j // W) * 150
        if k in got: sh.paste(got[k], (x, y + 15))
        a, b = shots[k]; d.text((x + 3, y + 2), f"#{k} {a:.1f}s +{b - a:.1f}", fill='yellow')
    sh.save(f"{out}/{key}_p{page // PER}.jpg", quality=72)
print(key, 'shots', len(shots), 'duration', round(t, 1))
