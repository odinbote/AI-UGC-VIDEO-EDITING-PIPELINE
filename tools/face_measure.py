#!/usr/bin/env python3
"""
Measure the talking head in a vertical A-roll so layouts and titles can be placed
without covering the face.  Uses OpenCV's YuNet detector (model file next to this script).

    python3 face_measure.py aroll.mp4 [t0 t1 ...]      # seconds to sample (default: every 0.5 s)

Prints, per sample and averaged: face box (normalised), chin line, and the suggested
full-screen punch-in (scale / position) that puts the eyes at ~0.26 and the chin at ~0.46,
plus the first safe title line (chin + 0.02).
"""
import sys, os, subprocess, json
import cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, 'face_detection_yunet_2023mar.onnx')
try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = 'ffmpeg'


def frame_at(path, t):
    out = subprocess.run([FFMPEG, '-v', 'error', '-ss', str(t), '-i', path, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                         capture_output=True).stdout
    arr = np.frombuffer(out, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def measure(path, times):
    det = cv2.FaceDetectorYN.create(MODEL, '', (320, 320), 0.6, 0.3, 5000)
    rows = []
    for t in times:
        im = frame_at(path, t)
        if im is None:
            continue
        h, w = im.shape[:2]
        det.setInputSize((w, h))
        _, faces = det.detect(im)
        if faces is None or not len(faces):
            rows.append(dict(t=t, face=None))
            continue
        f = max(faces, key=lambda f: f[2] * f[3])
        x, y, fw, fh = f[:4]
        rows.append(dict(t=t, face=dict(x0=float(x / w), x1=float((x + fw) / w), y0=float(y / h), y1=float((y + fh) / h)),
                         eyes=float((y + 0.35 * fh) / h), chin=float((y + fh) / h)))
    good = [r for r in rows if r['face']]
    if not good:
        return rows, None
    eyes = float(np.median([r['eyes'] for r in good]))
    chin = float(np.median([r['chin'] for r in good]))
    top = float(np.median([r['face']['y0'] for r in good]))
    # full-screen punch-in: map eyes->0.26, chin->0.46 ; keep the frame top covered (y0 <= S/2)
    S = (0.46 - 0.26) / (chin - eyes)
    S = min(max(S, 1.05), 1.6)
    y0 = 0.46 - (chin - 0.5) * S
    y0 = min(y0, S / 2)
    chin_on_screen = y0 + (chin - 0.5) * S
    # cutout at scale 1.02: head top should land at ~0.49
    cut_y = 0.49 - (top - 0.5) * 1.02
    summary = dict(eyes_raw=round(eyes, 3), chin_raw=round(chin, 3), head_top_raw=round(top, 3),
                   fullscreen_scale=round(S * 100), fullscreen_y=round(y0, 3), chin_on_screen=round(chin_on_screen, 3),
                   first_title_line_y=round(chin_on_screen + 0.02, 3), cutout_y=round(cut_y, 3))
    return rows, summary


if __name__ == '__main__':
    path = sys.argv[1]
    if len(sys.argv) > 2:
        times = [float(x) for x in sys.argv[2:]]
    else:
        dur = float(subprocess.run([FFMPEG, '-i', path], capture_output=True, text=True).stderr.split('Duration: ')[1].split(',')[0].split(':')[-1]) \
            if 'Duration' in subprocess.run([FFMPEG, '-i', path], capture_output=True, text=True).stderr else 8
        times = [i * 0.5 for i in range(int(dur / 0.5))]
    rows, summary = measure(path, times)
    for r in rows:
        print(json.dumps({k: (round(v, 3) if isinstance(v, float) else ({kk: round(vv, 3) for kk, vv in v.items()} if isinstance(v, dict) else v)) for k, v in r.items()}))
    print('SUMMARY', json.dumps(summary))
