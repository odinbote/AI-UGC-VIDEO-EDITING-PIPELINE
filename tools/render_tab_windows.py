#!/usr/bin/env python3
"""Render 25 full browser / terminal windows as transparent PNGs (window only, no desktop).

Each window is an HTML page that mimics the real site, screenshotted with Playwright at 2x
with a transparent background and rounded window corners.

Usage: python3 tools/render_tab_windows.py            # all 25 + contact sheet
       python3 tools/render_tab_windows.py 7          # one window
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tabwin import pages  # noqa: E402
from tabwin.frame import chrome_window, terminal_window  # noqa: E402
from tabwin.icons import icon  # noqa: E402

W, H, DPR = 1700, 880, 2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "Tab windows")
TMP = os.path.join(ROOT, "tools", "tabwin", "_build")


def build_html(i):
    spec = pages.SPECS[i - 1]
    kind = spec.get("kind", "chrome")
    if kind == "terminal":
        return terminal_window(W, H, spec["theme"], spec["title"], spec.get("sub", ""), spec["body"], spec.get("css", "")), spec
    fav = icon(spec["icon"]) if spec.get("icon") else ""
    return chrome_window(W, H, spec["theme"], fav, spec["title"], spec["host"], spec.get("path", ""), spec["body"], spec.get("css", "")), spec


def slug(s):
    out = "".join(c.lower() if c.isalnum() else "_" for c in s)
    while "__" in out:
        out = out.replace("__", "_")
    return out.strip("_")[:34].rstrip("_")


def render(indices):
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    outs = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=DPR)
        page = ctx.new_page()
        for i in indices:
            html, spec = build_html(i)
            hp = os.path.join(TMP, f"win_{i:02d}.html")
            with open(hp, "w") as f:
                f.write(html)
            page.goto("file://" + hp)
            page.wait_for_timeout(150)
            name = f"win_{i:02d}_{spec.get('kind','chrome')}_{spec['theme']}_{slug(spec['title'])}.png"
            out = os.path.join(OUT_DIR, name)
            page.locator(".win").screenshot(path=out, omit_background=True)
            print(out)
            outs.append(out)
        browser.close()
    return outs


def contact_sheet(paths):
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert("RGBA") for p in paths]
    cols = 3
    tw = 760
    th = int(tw * H / W)
    gap = 28
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * tw + (cols + 1) * gap, rows * (th + 30) + (rows + 1) * gap), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    cs = 20
    for yy in range(0, sheet.height, cs):
        for xx in range(0, sheet.width, cs):
            c = (118, 118, 118, 255) if ((xx // cs + yy // cs) % 2 == 0) else (138, 138, 138, 255)
            d.rectangle((xx, yy, xx + cs, yy + cs), fill=c)
    for k, im in enumerate(ims):
        r, c = divmod(k, cols)
        x = gap + c * (tw + gap)
        y = gap + r * (th + 30 + gap)
        sheet.alpha_composite(im.resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 8), f"{k + 1:02d}  {os.path.basename(paths[k])[7:-4]}", fill=(255, 255, 255, 255))
    return sheet


if __name__ == "__main__":
    if len(sys.argv) > 1:
        render([int(a) for a in sys.argv[1:]])
    else:
        outs = render(range(1, len(pages.SPECS) + 1))
        contact_sheet(outs).save(os.path.join(OUT_DIR, "_contact_sheet.png"))
