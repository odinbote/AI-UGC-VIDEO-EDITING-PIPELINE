#!/usr/bin/env python3
"""
Approximate preview render of a plan built by build_prproj.py, so the edit can be
checked without opening Premiere.  Composites with PIL, mixes audio with ffmpeg.

    python3 render_preview.py plan.json out.mp4
"""
import json, sys, os, math, subprocess, glob, shutil, gzip
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageOps

FPS = 24
W, H = 1080, 1920
TICKS = 254016000000
FFMPEG = None
try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = 'ffmpeg'

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_SERIF = os.path.join(HERE, '..', 'reference', 'fonts', 'InstrumentSerif-Italic.ttf')
FONT_SANS_SEMI = os.path.expanduser('~/Library/Fonts/SF-Pro-Display-Semibold.otf')
FONT_SANS_BOLD = os.path.expanduser('~/Library/Fonts/SF-Pro-Display-Bold.otf')

# title copy per exemplar key: (text, style)   style: serif | box-semibold | box-bold
TITLES = {   # text, style, font size (read from the reference text blobs)
    'g_instead': ('Instead of', 'serif', 85), 'g_memorizing': ('memorizing', 'serif', 85),
    'g_random': ('random concepts', 'box-semibold', 106), 'g_why': ('Why', 'serif', 85),
    'g_systems': ('Systems', 'box-bold', 147), 'g_designed': ('are designed', 'serif', 85),
    'g_theway': ('the way', 'serif', 85), 'g_theyare': ('they are?', 'box-bold', 127),
}
CAPTION_Y = {'cap_layout': 0.385, 'cap_youll': 0.61, 'cap_understand': 0.61, 'cap_low': 0.70}
FONT_SCALE = 0.92   # Premiere renders these graphics at ~0.92x the nominal font size (measured on the reference)
# on-screen centre = Vector Motion position + offset (measured per exemplar on the reference render)
TITLE_OFFSET = {'g_instead': (0.0, 0.096), 'g_memorizing': (0.0, 0.097), 'g_random': (0.0, 0.097),
                'g_why': (0.0, -0.269), 'g_systems': (0.0, -0.279), 'g_designed': (0.0, -0.269),
                'g_theway': (0.0, -0.268), 'g_theyare': (0.0, -0.275)}
SFX_FILE = {'sfx_click': 'Mechanical, Click, Buttons', 'sfx_ui_a': 'User Interface, Click', 'sfx_ui_b': 'User Interface, Click',
            'sfx_whoosh': 'Swooshes, Whoosh', 'sfx_woosh2': 'Transition_Woosh', 'sfx_button': 'Miniature Button', 'sfx_ting': 'Pings, Tings'}
GAIN_DB = {'music': -30.0, 'sfx_whoosh': -15.0, 'sfx_woosh2': -17.0, 'sfx_button': -25.0, 'sfx_ting': -10.0, 'sfx_click': -10.0, 'sfx_ui_a': -15.0, 'sfx_ui_b': -15.0, 'dialog': 0.0}
ROSE = (176, 85, 90)
GREEN = (24, 48, 32)
MATTE = (245, 245, 245)


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def extract_frames(src, out_dir, start_s, n_frames, alpha=False):
    os.makedirs(out_dir, exist_ok=True)
    if len(glob.glob(os.path.join(out_dir, '*.png'))) >= n_frames:
        return
    cmd = [FFMPEG, '-v', 'error', '-y', '-ss', str(start_s), '-i', src, '-frames:v', str(n_frames), '-vf', f'fps={FPS}']
    if alpha:
        cmd += ['-pix_fmt', 'rgba']
    cmd += [os.path.join(out_dir, 'f_%04d.png')]
    run(cmd)


def frame_path(d, i):
    p = os.path.join(d, f'f_{i + 1:04d}.png')
    if not os.path.exists(p):   # clamp to the last decoded frame
        files = sorted(glob.glob(os.path.join(d, 'f_*.png')))
        p = files[-1]
    return p


def place(canvas, im, cx, cy, scale, rotation=0.0):
    """scale in percent, (cx, cy) normalised centre"""
    if scale != 100:
        im = im.resize((max(1, round(im.width * scale / 100)), max(1, round(im.height * scale / 100))), Image.LANCZOS)
    if rotation:
        im = im.rotate(-rotation, resample=Image.BICUBIC, expand=True)
    x = round(cx * W - im.width / 2)
    y = round(cy * H - im.height / 2)
    if im.mode == 'RGBA':
        canvas.alpha_composite(im, (x, y)) if 0 <= x and 0 <= y and x + im.width <= W and y + im.height <= H else _paste_clip(canvas, im, x, y)
    else:
        canvas.paste(im, (x, y))


def _paste_clip(canvas, im, x, y):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    layer.paste(im, (x, y))
    canvas.alpha_composite(layer)


def lerp_kf(kfs, t, ease):
    (t0, v0), (t1, v1) = kfs[0], kfs[-1]
    if t <= t0:
        return v0
    if t >= t1:
        return v1
    p = (t - t0) / (t1 - t0)
    if ease:
        p = 0.5 - 0.5 * math.cos(math.pi * p)
    if isinstance(v0, list):
        return [v0[i] + (v1[i] - v0[i]) * p for i in range(2)]
    return v0 + (v1 - v0) * p


def motion_at(mo, f_local, kind_ease):
    out = {}
    for k, v in mo.items():
        if isinstance(v, dict):
            out[k] = lerp_kf(v['keyframes'], f_local, kind_ease.get(k, True))
        else:
            out[k] = v
    return out


def render_title(text, style, alpha, dy, size=100):
    size = round(size * FONT_SCALE)
    if style == 'serif':
        font = ImageFont.truetype(FONT_SERIF, size)
        pad = (0, 0)
    else:
        font = ImageFont.truetype(FONT_SANS_BOLD if style == 'box-bold' else FONT_SANS_SEMI, size)
        pad = (26, 14)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), text, font=font)
    tw, th = r - l, b - t
    im = Image.new('RGBA', (tw + 2 * pad[0] + 4, th + 2 * pad[1] + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if style != 'serif':
        d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=18, fill=ROSE + (255,))
    d.text((pad[0] + 2 - l, pad[1] + 2 - t), text, font=font, fill=(255, 255, 255, 255))
    if alpha < 1:
        a = im.split()[3].point(lambda v: int(v * alpha))
        im.putalpha(a)
    return im, dy


def render_caption(text):
    font = ImageFont.truetype(FONT_SERIF, 70)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), text, font=font)
    tw, th = r - l, b - t
    padx, pady = 24, 14
    im = Image.new('RGBA', (tw + 2 * padx, th + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=14, fill=GREEN + (255,))
    d.text((padx - l, pady - t), text, font=font, fill=(255, 255, 255, 255))
    return im


def main(plan_path, out_path):
    plan = json.load(open(plan_path))
    media = plan['output_dir'] if plan.get('media_flat') else os.path.join(plan['output_dir'], 'Media')
    work = os.path.join(os.path.dirname(out_path), 'preview_work')
    os.makedirs(work, exist_ok=True)
    total = plan['total_frames']

    # graphic positions from the generated project
    xml = gzip.open(os.path.join(plan['output_dir'], plan['project_name'] + '.prproj')).read()
    root = ET.fromstring(xml)
    byid = {e.attrib['ObjectID']: e for e in root if 'ObjectID' in e.attrib}
    byuid = {e.attrib['ObjectUID']: e for e in root if 'ObjectUID' in e.attrib}
    gpos = {}
    gfam = {}
    vg = [e for e in root if e.tag == 'VideoTrackGroup'][0]
    for t in vg.find('TrackGroup/Tracks').findall('Track'):
        te = byuid[t.attrib['ObjectURef']]
        name = te.findtext('.//MZ.TrackName')
        if 'Text' not in name:
            continue
        for x in te.find('.//ClipItems/TrackItems').findall('TrackItem'):
            it = byid[x.attrib['ObjectRef']]
            st = int(it.find('.//TrackItem/Start').text or 0)
            comps = byid[it.find('.//ComponentOwner/Components').attrib['ObjectRef']]
            for c in comps.iter('Component'):
                ce = byid[c.attrib['ObjectRef']]
                if ce.findtext('MatchName') == 'AE.ADBE Graphic Group':
                    for pr in ce.find('.//Params').findall('Param'):
                        p = byid[pr.attrib['ObjectRef']]
                        if p.findtext('Name') == 'Position':
                            xy = p.findtext('StartKeyframe').split(',')[1].split(':')
                            gpos[(name, round(st / TICKS * FPS))] = (float(xy[0]), float(xy[1]))
                if ce.findtext('MatchName') == 'AE.ADBE Text':
                    for pr in ce.find('.//Params').findall('Param'):
                        p = byid[pr.attrib['ObjectRef']]
                        if p.findtext('Name') == 'Position':
                            ty = float(p.findtext('StartKeyframe').split(',')[1].split(':')[1])
                            gfam[(name, round(st / TICKS * FPS))] = (0.0, 0.096) if ty > 0.28 else (0.0, -0.272)
    # transitions (anim-in duration) per graphic
    gtrans = {}
    for t in vg.find('TrackGroup/Tracks').findall('Track'):
        te = byuid[t.attrib['ObjectURef']]
        name = te.findtext('.//MZ.TrackName')
        tr = te.find('.//TransitionItems/TrackItems')
        if tr is None:
            continue
        for x in tr.findall('TrackItem'):
            it = byid[x.attrib['ObjectRef']]
            ti = it.find('.//TrackItem')
            s = int(ti.findtext('Start') or 0)
            e = int(ti.findtext('End'))
            gtrans[(name, round(s / TICKS * FPS))] = round((e - s) / TICKS * FPS)

    def mpath(key):
        for f in os.listdir(media):
            if key in f:
                return os.path.join(media, f)
        raise KeyError(key)

    # pre-extract video frames
    pm = plan.get('media', {})
    aroll = mpath(pm.get('aroll', 'veo31_1080p_take3.mp4'))
    nfr = int(pm.get('aroll_frames', 192))
    extract_frames(aroll, os.path.join(work, 'aroll'), 0, nfr)
    extract_frames(mpath(pm.get('cutout', 'cutout_alpha.mov')), os.path.join(work, 'cutout'), 0, nfr, alpha=True)
    extract_frames(mpath('fanout-loader'), os.path.join(work, 'loader'), 0, 60, alpha=True)
    broll_dirs = {}
    for it in plan['items']:
        if it['kind'] == 'video' and it['track'].startswith('Broll'):
            key = f"{it['track'].replace(' ', '_')}_{it['start_f']}"
            src = mpath(it.get('file') or ('Silicon Valley' if it['exemplar'] == 'broll1' else 'SOCIAL NETWORK'))
            extract_frames(src, os.path.join(work, key), it['in_s'], it['end_f'] - it['start_f'])
            broll_dirs[(it['track'], it['start_f'])] = os.path.join(work, key)

    vid_dirs = {}
    for it in plan['items']:
        if it['kind'] == 'video' and it.get('file') and not it['track'].startswith('Broll'):
            key = f"vid_{it['track'].replace(' ', '_')}_{it['start_f']}"
            extract_frames(mpath(it['file']), os.path.join(work, key), it.get('in_s', 0), it['end_f'] - it['start_f'])
            vid_dirs[(it['track'], it['start_f'])] = os.path.join(work, key)
    stills = {}
    for it in plan['items']:
        if it.get('still') and it['still'] not in stills:
            stills[it['still']] = Image.open(mpath(it['still'])).convert('RGBA')
    captions_cache = {}
    frames_dir = os.path.join(work, 'out')
    os.makedirs(frames_dir, exist_ok=True)

    order = ['Aroll', 'Color mate Background', 'Screen Recording 1', 'Screen Recording 2', 'Broll 1', 'Broll 2', 'Aroll Cutout', 'Aroll Full Screen', 'Logos',
             'Text Graphics 1', 'Text Graphics 2', 'Text Graphics 3', 'Outro Animation']
    items = plan['items']
    for f in range(total):
        if os.path.exists(os.path.join(frames_dir, f'f_{f:04d}.png')) and os.environ.get('PREVIEW_REUSE'):
            continue
        canvas = Image.new('RGBA', (W, H), MATTE + (255,))
        for track in order:
            for it in items:
                if it['track'] != track or not (it['start_f'] <= f < it['end_f']):
                    continue
                fl = f - it['start_f']
                kind = it['kind']
                if kind == 'video':
                    mo = motion_at(it.get('motion', {}), fl, {'Position': it.get('exemplar') != 'shot_scroll'})
                    pos = mo.get('Position', [0.5, 0.5]); sc = mo.get('Scale', 100); rot = mo.get('Rotation', 0)
                    ex = it['exemplar']
                    if it.get('still'):
                        im = stills[it['still']]
                    elif (track, it['start_f']) in vid_dirs:
                        im = Image.open(frame_path(vid_dirs[(track, it['start_f'])], fl)).convert('RGBA')
                    elif track == 'Aroll Cutout':
                        im = Image.open(frame_path(os.path.join(work, 'cutout'), it['in_f'] + fl)).convert('RGBA')
                    elif track == 'Aroll Full Screen':
                        im = Image.open(frame_path(os.path.join(work, 'aroll'), it['in_f'] + fl)).convert('RGBA')
                    elif (track, it['start_f']) in broll_dirs:
                        im = Image.open(frame_path(broll_dirs[(track, it['start_f'])], fl)).convert('RGBA')
                    elif track == 'Aroll':
                        im = Image.open(frame_path(os.path.join(work, 'aroll'), it['in_f'] + fl)).convert('RGBA')
                    elif track == 'Outro Animation':
                        im = Image.open(frame_path(os.path.join(work, 'loader'), min(fl, 59))).convert('RGBA')
                    elif track == 'Color mate Background':
                        canvas.paste(MATTE + (255,), (0, 0, W, H))
                        continue
                    else:
                        continue
                    place(canvas, im, pos[0], pos[1], sc, rot)
                elif kind == 'graphic':
                    if 'title' in it:
                        text, style, size = it['title']['text'], it['title']['style'], it['title']['size']
                    else:
                        text, style, size = TITLES[it['exemplar']]
                    key = (track, it['start_f'])
                    cx, cy = gpos.get(key, (0.5, 0.5))
                    ox, oy = gfam.get(key, TITLE_OFFSET.get(it['exemplar'], (0, 0)))
                    cx, cy = cx + ox, cy + oy
                    D = gtrans.get(key, 12)
                    p = min(1.0, fl / max(1, D))
                    pe = 1 - (1 - p) ** 2.4
                    alpha = 0.25 + 0.75 * pe
                    dy = 95 * (1 - pe)
                    im, dy = render_title(text, style, alpha, dy, size)
                    place(canvas, im, cx, cy + dy / H, 100)
        # captions on top
        for it in items:
            if it['kind'] == 'caption' and it['start_f'] <= f < it['end_f']:
                im = captions_cache.get(it['text'])
                if im is None:
                    im = captions_cache[it['text']] = render_caption(it['text'])
                place(canvas, im, 0.5, it.get('y', CAPTION_Y[it['exemplar']]), 100)
        out = canvas.convert('RGB')
        if plan.get('preview_grade'):
            import numpy as np
            arr = np.asarray(out).astype(np.float32)
            arr = arr * 0.88 + 22                      # lift blacks, soften contrast (Faded Film ~28)
            arr += np.random.normal(0, 3.0, arr.shape)  # grain (~5 %)
            out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        out.save(os.path.join(frames_dir, f'f_{f:04d}.png'))
        if f % 24 == 0:
            print('frame', f, flush=True)

    # ---- audio mix ----
    aud = []
    for it in items:
        if it['kind'] != 'audio':
            continue
        if it['track'] == 'Aroll Sound':
            src = aroll; start = it['in_f'] / FPS
        elif it['exemplar'] == 'music':
            src = mpath('Electronica'); start = it['in_s']
        else:
            src = mpath(it.get('file') or SFX_FILE[it['exemplar']]); start = it['in_s']
        gain = it.get('gain_db', GAIN_DB.get(it['exemplar'], 0.0))
        fade = it.get('fade_out_f', 0) / FPS
        aud.append((src, start, (it['end_f'] - it['start_f']) / FPS, it['start_f'] / FPS, gain, fade))
    inputs, filt = [], []
    for i, (src, start, dur, at, gain, fade) in enumerate(aud):
        inputs += ['-ss', f'{start:.4f}', '-t', f'{dur:.4f}', '-i', src]
        chain = f'[{i+1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain}dB'
        if fade:
            chain += f',afade=t=out:st={max(0, dur - fade):.3f}:d={fade:.3f}'
        chain += f',adelay={int(at*1000)}|{int(at*1000)}[a{i}]'
        filt.append(chain)
    mix = ''.join(f'[a{i}]' for i in range(len(aud))) + f'amix=inputs={len(aud)}:normalize=0:dropout_transition=0[mix]'
    cmd = [FFMPEG, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(frames_dir, 'f_%04d.png')] + inputs + \
          ['-filter_complex', ';'.join(filt + [mix]), '-map', '0:v', '-map', '[mix]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20',
           '-c:a', 'aac', '-b:a', '192k', '-shortest', out_path]
    subprocess.run(cmd, check=True)
    print('wrote', out_path)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
