#!/usr/bin/env python3
"""Render single browser / macOS tab chips as transparent PNGs (no window, no mockup).

Styles: chrome_light, chrome_dark, safari_light, safari_dark, terminal.
Everything is drawn in 1x "CSS pixel" units, rendered at SCALE x (default 4) with
supersampling for clean anti-aliased edges. Favicons are drawn by hand (no downloads).

Usage:  python3 tools/render_tabs.py [index]      # one tab (1-based), or all when omitted
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

SCALE = 4          # output pixels per 1x unit
SS = 3             # supersampling factor
U = SCALE * SS     # drawing units per 1x pixel

SF = "/System/Library/Fonts/SFNS.ttf"
HELV = "/System/Library/Fonts/Helvetica.ttc"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Tab overlays")


def font(size_1x, weight="Regular", path=SF):
    f = ImageFont.truetype(path, int(round(size_1x * U)))
    if path == SF:
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
    return f


def hx(c, a=255):
    c = c.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), a)


# ---------------------------------------------------------------- favicons (16x16 at 1x)

def _icon_canvas():
    n = 16 * U
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im), n


def _rounded(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def _letter(d, n, txt, color, size=11, weight="Bold", dy=0):
    f = font(size, weight)
    bb = d.textbbox((0, 0), txt, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((n - w) / 2 - bb[0], (n - h) / 2 - bb[1] + dy * U), txt, font=f, fill=color)


def icon_youtube():
    im, d, n = _icon_canvas()
    _rounded(d, (0, 2.5 * U, n, n - 2.5 * U), 3.5 * U, hx("FF0000"))
    cx, cy = n / 2 + 0.4 * U, n / 2
    d.polygon([(cx - 2.2 * U, cy - 2.8 * U), (cx - 2.2 * U, cy + 2.8 * U), (cx + 2.8 * U, cy)], fill=(255, 255, 255, 255))
    return im


def icon_arxiv():
    im, d, n = _icon_canvas()
    _rounded(d, (0, 0, n, n), 2 * U, hx("B31B1B"))
    _letter(d, n, "X", (255, 255, 255, 255), size=12, weight="Semibold", dy=-0.3)
    return im


def icon_github(dark=False):
    im, d, n = _icon_canvas()
    bg = (255, 255, 255, 255) if dark else (36, 41, 47, 255)
    fg = (36, 41, 47, 255) if dark else (255, 255, 255, 255)
    d.ellipse((0, 0, n, n), fill=bg)
    # simple cat head
    cx, cy = n / 2, n / 2 + 0.6 * U
    d.ellipse((cx - 4.6 * U, cy - 3.6 * U, cx + 4.6 * U, cy + 3.6 * U), fill=fg)
    d.polygon([(cx - 4.4 * U, cy - 2.4 * U), (cx - 4.2 * U, cy - 6.2 * U), (cx - 1.2 * U, cy - 3.6 * U)], fill=fg)
    d.polygon([(cx + 4.4 * U, cy - 2.4 * U), (cx + 4.2 * U, cy - 6.2 * U), (cx + 1.2 * U, cy - 3.6 * U)], fill=fg)
    d.rounded_rectangle((cx - 1.2 * U, cy + 2.6 * U, cx + 1.2 * U, cy + 6.6 * U), radius=0.6 * U, fill=fg)
    return im


def icon_claude():
    im, d, n = _icon_canvas()
    _rounded(d, (0, 0, n, n), 3.5 * U, hx("D97757"))
    cx, cy = n / 2, n / 2
    for k in range(8):
        a = math.pi / 8 + k * math.pi / 4
        x2, y2 = cx + 5.2 * U * math.cos(a), cy + 5.2 * U * math.sin(a)
        d.line([(cx, cy), (x2, y2)], fill=(255, 255, 255, 255), width=int(1.7 * U))
    return im


def icon_openai():
    im, d, n = _icon_canvas()
    d.ellipse((0, 0, n, n), fill=(0, 0, 0, 255))
    cx, cy, r = n / 2, n / 2, 4.6 * U
    pts = [(cx + r * math.cos(math.pi / 6 + k * math.pi / 3), cy + r * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
    for k in range(6):
        d.line([pts[k], pts[(k + 1) % 6]], fill=(255, 255, 255, 255), width=int(1.5 * U), joint="curve")
        d.line([pts[k], (cx, cy)], fill=(255, 255, 255, 255), width=int(1.2 * U))
    return im


def icon_globe(dark=False):
    im, d, n = _icon_canvas()
    c = (160, 160, 160, 255) if dark else (95, 99, 104, 255)
    w = int(1.2 * U)
    d.ellipse((1 * U, 1 * U, n - 1 * U, n - 1 * U), outline=c, width=w)
    d.ellipse((4.6 * U, 1 * U, n - 4.6 * U, n - 1 * U), outline=c, width=w)
    d.line([(1.2 * U, n / 2), (n - 1.2 * U, n / 2)], fill=c, width=w)
    d.line([(n / 2, 1 * U), (n / 2, n - 1 * U)], fill=c, width=w)
    return im


def icon_medium():
    im, d, n = _icon_canvas()
    d.ellipse((0, 0, n, n), fill=(0, 0, 0, 255))
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if os.path.exists("/System/Library/Fonts/Supplemental/Georgia Bold.ttf") else HELV, int(10 * U))
    bb = d.textbbox((0, 0), "M", font=f)
    d.text(((n - (bb[2] - bb[0])) / 2 - bb[0], (n - (bb[3] - bb[1])) / 2 - bb[1]), "M", font=f, fill=(255, 255, 255, 255))
    return im


def icon_hn():
    im, d, n = _icon_canvas()
    d.rectangle((0, 0, n, n), fill=hx("FF6600"))
    _letter(d, n, "Y", (255, 255, 255, 255), size=12, weight="Bold")
    return im


def icon_wikipedia():
    im, d, n = _icon_canvas()
    d.rectangle((0, 0, n, n), fill=(255, 255, 255, 255))
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman.ttf" if os.path.exists("/System/Library/Fonts/Supplemental/Times New Roman.ttf") else HELV, int(14 * U))
    bb = d.textbbox((0, 0), "W", font=f)
    d.text(((n - (bb[2] - bb[0])) / 2 - bb[0], (n - (bb[3] - bb[1])) / 2 - bb[1]), "W", font=f, fill=(0, 0, 0, 255))
    return im


def icon_lillog():
    im, d, n = _icon_canvas()
    _rounded(d, (0, 0, n, n), 2 * U, hx("2E2E2E"))
    _letter(d, n, "L", (255, 255, 255, 255), size=11, weight="Semibold")
    return im


def icon_gdocs():
    im, d, n = _icon_canvas()
    d.rounded_rectangle((2.5 * U, 0.5 * U, n - 2.5 * U, n - 0.5 * U), radius=1.2 * U, fill=hx("4285F4"))
    for i, w in enumerate((6, 6, 6, 4)):
        y = 7 * U + i * 2 * U
        d.rectangle((5 * U, y, (5 + w) * U, y + 0.9 * U), fill=(255, 255, 255, 255))
    return im


def icon_hf():
    im, d, n = _icon_canvas()
    d.ellipse((0.5 * U, 0.5 * U, n - 0.5 * U, n - 0.5 * U), fill=hx("FFD21E"))
    d.ellipse((4.2 * U, 5 * U, 6.2 * U, 7.4 * U), fill=(60, 40, 20, 255))
    d.ellipse((n - 6.2 * U, 5 * U, n - 4.2 * U, 7.4 * U), fill=(60, 40, 20, 255))
    d.arc((4 * U, 5 * U, n - 4 * U, n - 3.5 * U), 15, 165, fill=(60, 40, 20, 255), width=int(1.3 * U))
    return im


def icon_colab():
    im, d, n = _icon_canvas()
    w = int(2.4 * U)
    d.arc((0.8 * U, 4 * U, 9 * U, 12 * U), 40, 320, fill=hx("F9AB00"), width=w)
    d.arc((7 * U, 4 * U, n - 0.8 * U, 12 * U), 220, 140, fill=hx("E8710A"), width=w)
    return im


def icon_swagger():
    im, d, n = _icon_canvas()
    d.ellipse((0, 0, n, n), fill=hx("85EA2D"))
    _letter(d, n, "{ }", (30, 30, 30, 255), size=8, weight="Bold", dy=-0.2)
    return im


def icon_so():
    im, d, n = _icon_canvas()
    g = hx("BCBBBB")
    d.line([(3 * U, 9 * U), (3 * U, 14.5 * U), (13 * U, 14.5 * U), (13 * U, 9 * U)], fill=g, width=int(1.6 * U))
    d.rectangle((5 * U, 11 * U, 11 * U, 12.3 * U), fill=hx("F48024"))
    for k, ang in enumerate((-12, -30, -55)):
        cx, cy = 8 * U, (9 - k * 1.9) * U
        a = math.radians(ang)
        dx, dy = 3 * U * math.cos(a), 3 * U * math.sin(a)
        d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=hx("F48024"), width=int(1.3 * U))
    return im


def icon_fanout():
    im, d, n = _icon_canvas()
    _rounded(d, (0, 0, n, n), 3.5 * U, (20, 20, 20, 255))
    w = int(1.3 * U)
    x0, y0 = 4 * U, n / 2
    d.ellipse((x0 - 1.2 * U, y0 - 1.2 * U, x0 + 1.2 * U, y0 + 1.2 * U), fill=(255, 255, 255, 255))
    for yy in (4.2, 8, 11.8):
        d.line([(x0, y0), (12 * U, yy * U)], fill=(255, 255, 255, 255), width=w)
        d.ellipse((12 * U - 1 * U, yy * U - 1 * U, 12 * U + 1 * U, yy * U + 1 * U), fill=(255, 255, 255, 255))
    return im


def icon_excalidraw():
    im, d, n = _icon_canvas()
    _rounded(d, (0, 0, n, n), 2.5 * U, hx("6965DB"))
    _letter(d, n, "E", (255, 255, 255, 255), size=11, weight="Bold")
    return im


def icon_vscode():
    im, d, n = _icon_canvas()
    _rounded(d, (0.5 * U, 0.5 * U, n - 0.5 * U, n - 0.5 * U), 2.5 * U, hx("0078D4"))
    w = int(2.2 * U)
    d.line([(3 * U, 5.5 * U), (12.5 * U, 12.5 * U)], fill=(255, 255, 255, 255), width=w)
    d.line([(3 * U, 10.5 * U), (12.5 * U, 3.5 * U)], fill=(255, 255, 255, 255), width=w)
    d.rectangle((11.3 * U, 3 * U, 13.3 * U, 13 * U), fill=(255, 255, 255, 255))
    return im


def icon_substack():
    im, d, n = _icon_canvas()
    o = hx("FF6719")
    d.rectangle((2 * U, 2 * U, n - 2 * U, 3.6 * U), fill=o)
    d.rectangle((2 * U, 5.4 * U, n - 2 * U, 7 * U), fill=o)
    d.polygon([(2 * U, 8.8 * U), (n - 2 * U, 8.8 * U), (n - 2 * U, 14.5 * U), (n / 2, 11.8 * U), (2 * U, 14.5 * U)], fill=o)
    return im


def icon_grafana():
    im, d, n = _icon_canvas()
    d.ellipse((0.5 * U, 0.5 * U, n - 0.5 * U, n - 0.5 * U), fill=hx("F46800"))
    d.ellipse((5 * U, 5 * U, n - 5 * U, n - 5 * U), fill=(255, 255, 255, 255))
    d.ellipse((6.6 * U, 6.6 * U, n - 6.6 * U, n - 6.6 * U), fill=hx("F46800"))
    return im


ICONS = {
    "youtube": icon_youtube, "arxiv": icon_arxiv, "github": icon_github, "claude": icon_claude,
    "openai": icon_openai, "globe": icon_globe, "medium": icon_medium, "hn": icon_hn,
    "wikipedia": icon_wikipedia, "lillog": icon_lillog, "gdocs": icon_gdocs, "hf": icon_hf,
    "colab": icon_colab, "swagger": icon_swagger, "so": icon_so, "fanout": icon_fanout,
    "excalidraw": icon_excalidraw, "vscode": icon_vscode, "substack": icon_substack, "grafana": icon_grafana,
}


def make_icon(name, dark):
    fn = ICONS[name]
    try:
        return fn(dark)
    except TypeError:
        return fn()


# ---------------------------------------------------------------- shared text helpers

def draw_title(canvas, text, x, y_center, max_w, color, size=12, weight="Regular", fade=18, align="left"):
    """Draw a single-line title clipped to max_w with Chrome-style alpha fade at the end."""
    f = font(size, weight)
    bb = f.getbbox(text)
    tw = bb[2] - bb[0]
    th_asc, th_desc = f.getmetrics()
    layer_w = int(max_w * U)
    layer = Image.new("RGBA", (max(layer_w, 1), int((th_asc + th_desc) * 1.2)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    x0 = 0
    if align == "center" and tw < layer_w:
        x0 = (layer_w - tw) / 2
    ld.text((x0 - bb[0], 0), text, font=f, fill=color)
    if tw > layer_w and fade:
        fw = int(fade * U)
        mask = Image.new("L", layer.size, 255)
        md = ImageDraw.Draw(mask)
        for i in range(fw):
            v = int(255 * (1 - i / fw))
            xx = layer_w - fw + i
            md.line([(xx, 0), (xx, layer.size[1])], fill=v)
        a = layer.getchannel("A")
        a = Image.composite(a, Image.new("L", layer.size, 0), mask)
        layer.putalpha(a)
    # vertical centre on cap-height-ish box
    ty = int(y_center * U - (th_asc + th_desc) / 2 + 0.12 * size * U)
    canvas.alpha_composite(layer, (int(x * U), ty))
    return min(tw, layer_w) / U


def draw_close(d, cx, cy, color, size=8, width=1.3):
    h = size / 2 * U
    d.line([(cx * U - h, cy * U - h), (cx * U + h, cy * U + h)], fill=color, width=int(width * U))
    d.line([(cx * U - h, cy * U + h), (cx * U + h, cy * U - h)], fill=color, width=int(width * U))


def arc_pts(cx, cy, r, a0, a1, steps=24):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / steps)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / steps))) for i in range(steps + 1)]


# ---------------------------------------------------------------- tab styles

def render_chrome(spec, dark):
    """Chrome (2023 refresh) active tab on macOS: 34px tall, 10px top radius, bottom flares."""
    body_w = spec.get("width", 240)
    h, r, rt = 34, 10, 10
    W = body_w + 2 * r
    pad = 2  # transparent margin
    img = Image.new("RGBA", (int((W + 2 * pad) * U), int((h + 2 * pad) * U)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill = hx("35363A") if dark else hx("FFFFFF")
    ox, oy = pad, pad
    pts = []
    pts += arc_pts(ox + 0, oy + h - r, r, 90, 0)                 # left flare
    pts += arc_pts(ox + r + rt, oy + rt, rt, 180, 270)           # top-left
    pts += arc_pts(ox + W - r - rt, oy + rt, rt, 270, 360)       # top-right
    pts += arc_pts(ox + W, oy + h - r, r, 180, 90)               # right flare
    pts += [(ox + W, oy + h), (ox + 0, oy + h)]
    d.polygon([(x * U, y * U) for x, y in pts], fill=fill)

    text_col = hx("E8EAED") if dark else hx("1F1F1F")
    close_col = hx("C4C7C5") if dark else hx("444746")
    x = ox + r + 10
    cy = oy + h / 2
    if spec.get("icon"):
        ic = make_icon(spec["icon"], dark)
        img.alpha_composite(ic, (int(x * U), int((cy - 8) * U)))
        x += 16 + 8
    close_cx = ox + W - r - 8 - 8
    max_w = close_cx - 8 - 6 - x
    draw_title(img, spec["title"], x, cy, max_w, text_col, size=12)
    draw_close(d, close_cx, cy, close_col, size=7.5, width=1.05)
    return img


def render_safari(spec, dark):
    """Safari (macOS 14/15, separate tab bar) active tab: rounded 6px chip, centred favicon+title."""
    w = spec.get("width", 200)
    h = 28
    pad = 2
    img = Image.new("RGBA", (int((w + 2 * pad) * U), int((h + 2 * pad) * U)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill = hx("4B4B4B") if dark else hx("F6F6F6")
    border = hx("5C5C5C") if dark else hx("D6D6D6")
    d.rounded_rectangle((pad * U, pad * U, (pad + w) * U, (pad + h) * U), radius=6 * U, fill=fill,
                        outline=border, width=int(0.8 * U))
    text_col = hx("F2F2F2") if dark else hx("222222")
    cy = pad + h / 2
    f = font(12, "Regular")
    bb = f.getbbox(spec["title"])
    tw = (bb[2] - bb[0]) / U
    has_icon = bool(spec.get("icon"))
    inner = w - 2 * 22  # room kept for the (hover) close button zone on the left and symmetry
    content = (16 + 7 if has_icon else 0) + tw
    content = min(content, inner)
    x = pad + (w - content) / 2
    if has_icon:
        ic = make_icon(spec["icon"], dark)
        img.alpha_composite(ic, (int(x * U), int((cy - 8) * U)))
        x += 16 + 7
    draw_title(img, spec["title"], x, cy, content - ((16 + 7) if has_icon else 0), text_col, size=12, fade=14)
    if spec.get("close", False):
        draw_close(d, pad + 12, cy, hx("B0B0B0") if dark else hx("7A7A7A"), size=7, width=1.2)
    return img


def render_terminal(spec, dark):
    """Native macOS window tab (Terminal.app): flat segment, 28px, title centred, close on the left."""
    w = spec.get("width", 260)
    h = 28
    pad = 2
    img = Image.new("RGBA", (int((w + 2 * pad) * U), int((h + 2 * pad) * U)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill = hx("2B2B2B") if dark else hx("E6E6E6")
    divider = hx("1A1A1A") if dark else hx("C9C9C9")
    d.rectangle((pad * U, pad * U, (pad + w) * U, (pad + h) * U), fill=fill)
    d.rectangle((pad * U, pad * U, (pad + 0.8) * U, (pad + h) * U), fill=divider)
    d.rectangle(((pad + w - 0.8) * U, pad * U, (pad + w) * U, (pad + h) * U), fill=divider)
    text_col = hx("E8E8E8") if dark else hx("2B2B2B")
    cy = pad + h / 2
    draw_title(img, spec["title"], pad + 24, cy, w - 48, text_col, size=12, weight="Regular", align="center", fade=14)
    draw_close(d, pad + 12, cy, hx("9A9A9A") if dark else hx("6E6E6E"), size=7, width=1.2)
    return img


RENDERERS = {
    "chrome_light": lambda s: render_chrome(s, False),
    "chrome_dark": lambda s: render_chrome(s, True),
    "safari_light": lambda s: render_safari(s, False),
    "safari_dark": lambda s: render_safari(s, True),
    "terminal_light": lambda s: render_terminal(s, False),
    "terminal_dark": lambda s: render_terminal(s, True),
}


# ---------------------------------------------------------------- the 25 tabs

TABS = [
    # system design / inference via YouTube + articles
    dict(style="chrome_light", icon="youtube", title="Consistent Hashing explained in 10 minutes - YouTube", width=240),
    dict(style="chrome_light", icon="arxiv", title="[2309.06180] Efficient Memory Management for Large Language Model Serving with PagedAttention", width=240),
    dict(style="safari_light", icon="github", title="donnemartin/system-design-primer: Learn how to design large-scale systems", width=220),
    dict(style="chrome_dark", icon="claude", title="Claude Code overview - Claude Docs", width=220),
    dict(style="terminal_dark", title="claude — ~/inference-demo — zsh — 120×36", width=280),
    dict(style="chrome_light", icon="youtube", title="KV cache explained: why LLM inference eats your GPU memory - YouTube", width=200),
    dict(style="safari_light", icon="wikipedia", title="CAP theorem - Wikipedia", width=200),
    dict(style="chrome_dark", icon="globe", title="localhost:3000 — token stream demo", width=220),
    dict(style="chrome_light", icon="openai", title="Codex | OpenAI", width=160),
    dict(style="chrome_light", icon="medium", title="Speculative decoding, explained simply | Medium", width=240),
    dict(style="safari_dark", icon="youtube", title="How a chat app scales to trillions of messages - YouTube", width=230),
    dict(style="chrome_light", icon="lillog", title="Large Transformer Model Inference Optimization | Lil'Log", width=240),
    dict(style="chrome_light", icon="hn", title="Why your p99 latency is lying to you | Hacker News", width=210),
    dict(style="terminal_light", title="codex — ~/queue-sim — zsh — 120×36", width=260),
    dict(style="chrome_dark", icon="hf", title="meta-llama/Llama-3.1-8B-Instruct · Hugging Face", width=240),
    dict(style="safari_light", icon="colab", title="inference_benchmark.ipynb - Colab", width=210),
    dict(style="chrome_light", icon="swagger", title="FastAPI - Swagger UI", width=180),
    dict(style="chrome_light", icon="so", title="python - torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 GiB - Stack Overflow", width=240),
    dict(style="safari_dark", icon="fanout", title="Roadmap — fanout", width=180, close=True),
    dict(style="chrome_light", icon="github", title="Load shedding for the request queue by abik · Pull Request #4 · queue-demo", width=240),
    dict(style="chrome_dark", icon="youtube", title="Designing a rate limiter (system design interview) - YouTube", width=190),
    dict(style="chrome_light", icon="gdocs", title="System design notes — Google Docs", width=220),
    dict(style="safari_light", icon="excalidraw", title="inference topology — Excalidraw", width=200),
    dict(style="chrome_light", icon="claude", title="Explain tensor parallelism like I'm new to GPUs - Claude", width=240),
    dict(style="chrome_dark", icon="vscode", title="serve.py — inference-demo — Visual Studio Code", width=230),
]


def slug(s):
    out = "".join(c.lower() if c.isalnum() else "_" for c in s)
    while "__" in out:
        out = out.replace("__", "_")
    return out.strip("_")[:40]


def render_one(i):
    spec = TABS[i - 1]
    big = RENDERERS[spec["style"]](spec)
    small = big.resize((big.width // SS, big.height // SS), Image.LANCZOS)
    name = f"tab_{i:02d}_{spec['style']}_{slug(spec.get('icon') or 'terminal')}_{slug(spec['title'])[:28].rstrip('_')}.png"
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, name)
    small.save(path, optimize=True)
    return path, small


def contact_sheet(paths):
    ims = [Image.open(p).convert("RGBA") for p in paths]
    cols = 1
    gap = 16 * SCALE
    w = max(i.width for i in ims) + 2 * gap + 60 * SCALE
    h = sum(i.height for i in ims) + gap * (len(ims) + 1)
    sheet = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # checker + mid grey so both light and dark chips can be judged
    d = ImageDraw.Draw(sheet)
    cs = 12 * SCALE
    for yy in range(0, h, cs):
        for xx in range(0, w, cs):
            c = (120, 120, 120, 255) if ((xx // cs + yy // cs) % 2 == 0) else (140, 140, 140, 255)
            d.rectangle((xx, yy, xx + cs, yy + cs), fill=c)
    y = gap
    f = ImageFont.truetype(SF, 11 * SCALE)
    for k, im in enumerate(ims, 1):
        d.text((gap, y + im.height / 2 - 6 * SCALE), f"{k:02d}", font=f, fill=(255, 255, 255, 255))
        sheet.alpha_composite(im, (gap + 40 * SCALE, y))
        y += im.height + gap
    return sheet


if __name__ == "__main__":
    if len(sys.argv) > 1:
        p, _ = render_one(int(sys.argv[1]))
        print(p)
    else:
        paths = [render_one(i)[0] for i in range(1, len(TABS) + 1)]
        for p in paths:
            print(p)
        contact_sheet(paths).save(os.path.join(OUT_DIR, "_contact_sheet.png"))
