"""Window frames (Chrome macOS light/dark, macOS Terminal) rendered as HTML on a transparent body."""

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:transparent;width:%(W)dpx;height:%(H)dpx;overflow:hidden}
body{font-family:-apple-system,"SF Pro Text","Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
.win{position:relative;width:%(W)dpx;height:%(H)dpx;border-radius:11px;overflow:hidden;display:flex;flex-direction:column}
.page{flex:1;position:relative;overflow:hidden}
.mono{font-family:"SF Mono",Menlo,Monaco,monospace}
.av{border-radius:50%%;background:linear-gradient(135deg,#7bb0ff,#f7c59f 55%%,#4f6d7a);display:inline-block}
svg{display:block}
.ico{width:16px;height:16px;border-radius:3px;display:inline-block;vertical-align:middle;flex:none}
"""

CHROME_CSS = """
.strip{height:42px;display:flex;align-items:flex-end;padding-left:80px;position:relative;background:var(--strip)}
.lights{position:absolute;left:13px;top:14px;display:flex;gap:8px}
.lights i{width:12px;height:12px;border-radius:50%;display:block}
.tab{height:34px;background:var(--tb);border-radius:10px 10px 0 0;display:flex;align-items:center;gap:8px;padding:0 10px 0 12px;width:260px;color:var(--fg);font-size:12.5px;position:relative}
.tab .t{flex:1;white-space:nowrap;overflow:hidden;-webkit-mask-image:linear-gradient(90deg,#000 84%,transparent)}
.tab .x{width:16px;height:16px;display:flex;align-items:center;justify-content:center;color:var(--fg);opacity:.85}
.tab:before,.tab:after{content:"";position:absolute;bottom:0;width:10px;height:10px;background:var(--tb)}
.tab:before{left:-10px;-webkit-mask:radial-gradient(circle at 0 0,transparent 10px,#000 10.5px)}
.tab:after{right:-10px;-webkit-mask:radial-gradient(circle at 100% 0,transparent 10px,#000 10.5px)}
.newtab{width:28px;height:28px;margin:0 0 3px 18px;display:flex;align-items:center;justify-content:center;color:var(--fg)}
.bar{height:48px;background:var(--tb);display:flex;align-items:center;padding:0 10px 0 14px;gap:6px;color:var(--fg)}
.bar .nav{width:28px;height:28px;display:flex;align-items:center;justify-content:center;opacity:.9}
.bar .nav.dim{opacity:.35}
.omni{flex:1;height:34px;border-radius:17px;background:var(--omni);display:flex;align-items:center;padding:0 14px 0 14px;gap:10px;margin:0 8px 0 10px;font-size:14.5px;color:var(--fg)}
.omni .host{color:var(--fg)}.omni .path{opacity:.6}
.omni .star{margin-left:auto;opacity:.85}
.bar .right{display:flex;align-items:center;gap:12px;margin-left:4px}
.bar .sep{width:1px;height:18px;background:var(--fg);opacity:.25}
"""

CHROME_THEMES = {
    "dark": "--strip:#1f1f1f;--tb:#2b2b2b;--omni:#1b1b1b;--fg:#e3e3e3",
    "light": "--strip:#dfe3e8;--tb:#ffffff;--omni:#eef1f5;--fg:#1f1f1f",
}

TERMINAL_CSS = """
.ttl{height:28px;background:var(--tt);display:flex;align-items:center;justify-content:center;position:relative;color:var(--tfg);font-size:13px}
.ttl .lights{top:8px}
.ttl .sub{opacity:.6;margin-left:6px}
.ttl .tabs{position:absolute;left:0;right:0;top:28px;height:26px;background:var(--tt2);display:flex}
"""

LIGHTS = '<div class="lights"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></div>'

SVG = {
    "back": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>',
    "fwd": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
    "reload": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg>',
    "lock": '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M17 9V7a5 5 0 0 0-10 0v2a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2zm-8-2a3 3 0 0 1 6 0v2H9z"/></svg>',
    "star": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3l2.8 5.9 6.4.8-4.7 4.5 1.2 6.4L12 17.5 6.3 20.6l1.2-6.4L2.8 9.7l6.4-.8z"/></svg>',
    "side": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M15 4v16"/></svg>',
    "kebab": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>',
    "plus": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
    "x": '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
}


def chrome_window(W, H, theme, favicon_html, title, host, path, body_html, extra_css=""):
    t = CHROME_THEMES[theme]
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{BASE_CSS % dict(W=W, H=H)}{CHROME_CSS}{extra_css}
.win{{{t}}}
</style></head><body><div class="win">
<div class="strip">{LIGHTS}
 <div class="tab">{favicon_html}<span class="t">{title}</span><span class="x">{SVG['x']}</span></div>
 <div class="newtab">{SVG['plus']}</div>
</div>
<div class="bar">
 <div class="nav">{SVG['back']}</div><div class="nav dim">{SVG['fwd']}</div><div class="nav">{SVG['reload']}</div>
 <div class="omni">{SVG['lock']}<span><span class="host">{host}</span><span class="path">{path}</span></span><span class="star">{SVG['star']}</span></div>
 <div class="right">{SVG['side']}<span class="sep"></span><span class="av" style="width:26px;height:26px"></span>{SVG['kebab']}</div>
</div>
<div class="page">{body_html}</div>
</div></body></html>"""


def terminal_window(W, H, theme, title, sub, body_html, extra_css=""):
    if theme == "dark":
        t = "--tt:#2a2a2a;--tt2:#242424;--tfg:#e6e6e6"
    else:
        t = "--tt:#e8e8e8;--tt2:#dedede;--tfg:#2a2a2a"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{BASE_CSS % dict(W=W, H=H)}{TERMINAL_CSS}{extra_css}
.win{{{t}}}
</style></head><body><div class="win">
<div class="ttl">{LIGHTS}<span>{title}</span><span class="sub">{sub}</span></div>
<div class="page">{body_html}</div>
</div></body></html>"""
