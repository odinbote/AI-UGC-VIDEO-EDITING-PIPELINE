"""Inline 16x16 SVG favicons (hand-drawn approximations, nothing downloaded)."""


def _svg(inner, bg=None, r=3):
    bgrect = f'<rect width="16" height="16" rx="{r}" fill="{bg}"/>' if bg else ""
    return f'<svg class="ico" viewBox="0 0 16 16" width="16" height="16">{bgrect}{inner}</svg>'


ICONS = {
    "youtube": _svg('<rect y="2.5" width="16" height="11" rx="3.4" fill="#FF0000"/><path d="M6.4 5.3v5.4L11 8z" fill="#fff"/>'),
    "arxiv": _svg('<text x="8" y="12.2" text-anchor="middle" font-family="Helvetica" font-weight="700" font-size="11" fill="#fff">X</text>', "#B31B1B", 2),
    "github": _svg('<circle cx="8" cy="8" r="8" fill="#24292f"/><ellipse cx="8" cy="8.8" rx="4.4" ry="3.5" fill="#fff"/><path d="M3.8 6.6l-.2-3.8 2.9 2.5zM12.2 6.6l.2-3.8-2.9 2.5z" fill="#fff"/><rect x="6.9" y="11" width="2.2" height="3.8" rx=".6" fill="#fff"/>'),
    "github_dark": _svg('<circle cx="8" cy="8" r="8" fill="#fff"/><ellipse cx="8" cy="8.8" rx="4.4" ry="3.5" fill="#24292f"/><path d="M3.8 6.6l-.2-3.8 2.9 2.5zM12.2 6.6l.2-3.8-2.9 2.5z" fill="#24292f"/><rect x="6.9" y="11" width="2.2" height="3.8" rx=".6" fill="#24292f"/>'),
    "claude": _svg('<g stroke="#fff" stroke-width="1.7" stroke-linecap="round">' + "".join(
        f'<line x1="8" y1="8" x2="{8 + 5.2 * __import__("math").cos(a):.2f}" y2="{8 + 5.2 * __import__("math").sin(a):.2f}"/>'
        for a in [__import__("math").pi / 8 + k * __import__("math").pi / 4 for k in range(8)]) + '</g>', "#D97757", 3.5),
    "openai": _svg('<circle cx="8" cy="8" r="8" fill="#000"/><polygon points="12,5.7 12,10.3 8,12.6 4,10.3 4,5.7 8,3.4" fill="none" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/><path d="M8 8L12 5.7M8 8L4 5.7M8 8v4.6" stroke="#fff" stroke-width="1.1"/>'),
    "globe": _svg('<g fill="none" stroke="#9aa0a6" stroke-width="1.2"><circle cx="8" cy="8" r="6.6"/><ellipse cx="8" cy="8" rx="2.8" ry="6.6"/><path d="M1.6 8h12.8M8 1.4v13.2"/></g>'),
    "medium": _svg('<circle cx="8" cy="8" r="8" fill="#000"/><text x="8" y="11.6" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="10" fill="#fff">M</text>'),
    "hn": _svg('<text x="8" y="12.4" text-anchor="middle" font-family="Helvetica" font-weight="700" font-size="12" fill="#fff">Y</text>', "#FF6600", 0),
    "wikipedia": _svg('<text x="8" y="13" text-anchor="middle" font-family="Times New Roman,serif" font-size="14" fill="#000">W</text>', "#fff", 0),
    "lillog": _svg('<text x="8" y="12" text-anchor="middle" font-family="Helvetica" font-weight="600" font-size="11" fill="#fff">L</text>', "#2e2e2e", 2),
    "gdocs": _svg('<rect x="2.6" y=".6" width="10.8" height="14.8" rx="1.3" fill="#4285F4"/><g fill="#fff"><rect x="5" y="7" width="6" height=".9"/><rect x="5" y="9" width="6" height=".9"/><rect x="5" y="11" width="6" height=".9"/><rect x="5" y="13" width="4" height=".9"/></g>'),
    "hf": _svg('<circle cx="8" cy="8" r="7.5" fill="#FFD21E"/><ellipse cx="5.2" cy="6.3" rx="1" ry="1.2" fill="#3c2814"/><ellipse cx="10.8" cy="6.3" rx="1" ry="1.2" fill="#3c2814"/><path d="M4.6 8.8q3.4 4.2 6.8 0" fill="none" stroke="#3c2814" stroke-width="1.3" stroke-linecap="round"/>'),
    "colab": _svg('<g fill="none" stroke-width="2.4"><path d="M6.6 5.1A3.4 3.4 0 1 0 6.6 10.9" stroke="#F9AB00"/><path d="M9.4 5.1A3.4 3.4 0 1 1 9.4 10.9" stroke="#E8710A"/></g>'),
    "swagger": _svg('<circle cx="8" cy="8" r="8" fill="#85EA2D"/><text x="8" y="11" text-anchor="middle" font-family="Helvetica" font-weight="700" font-size="8" fill="#1e1e1e">{ }</text>'),
    "so": _svg('<path d="M3 9v5.5h10V9" fill="none" stroke="#BCBBBB" stroke-width="1.6"/><rect x="5" y="11" width="6" height="1.3" fill="#F48024"/><g stroke="#F48024" stroke-width="1.3"><path d="M5 8.4l6 .6M5.4 5.5l5.6 2M6.6 2.6l4.6 3.5"/></g>'),
    "fanout": _svg('<g stroke="#fff" stroke-width="1.3"><path d="M4 8L12 4.2M4 8L12 8M4 8L12 11.8"/></g><circle cx="4" cy="8" r="1.3" fill="#fff"/><circle cx="12" cy="4.2" r="1" fill="#fff"/><circle cx="12" cy="8" r="1" fill="#fff"/><circle cx="12" cy="11.8" r="1" fill="#fff"/>', "#141414", 3.5),
    "excalidraw": _svg('<text x="8" y="12.2" text-anchor="middle" font-family="Helvetica" font-weight="700" font-size="11" fill="#fff">E</text>', "#6965DB", 2.5),
    "vscode": _svg('<g stroke="#fff" stroke-width="2.2" stroke-linecap="round"><path d="M3 5.5l9.5 7M3 10.5l9.5-7"/></g><rect x="11.3" y="3" width="2" height="10" fill="#fff"/>', "#0078D4", 2.5),
}


def icon(name, size=16):
    s = ICONS[name]
    if size != 16:
        s = s.replace('width="16" height="16"', f'width="{size}" height="{size}"', 1)
    return s
