"""Page bodies for the 25 tab windows. Each SPEC: kind, theme, icon, title, host, path, body, css."""
from .icons import icon

AV = '<span class="av" style="width:{s}px;height:{s}px"></span>'
HAND = "font-family:'Chalkboard SE','Comic Sans MS',cursive;"


def av(s=32, grad=None):
    g = f"background:{grad};" if grad else ""
    return f'<span class="av" style="width:{s}px;height:{s}px;{g}"></span>'


# ------------------------------------------------------------------ YouTube (dark, like the reference)

YT_CSS = """
.yt{background:#0f0f0f;color:#f1f1f1;height:100%;display:flex;flex-direction:column}
.yt-h{height:56px;display:flex;align-items:center;padding:0 24px;gap:22px}
.yt-logo{display:flex;align-items:center;gap:6px;font-weight:700;font-size:20px;letter-spacing:-.6px}
.yt-logo i{width:30px;height:21px;background:#ff0000;border-radius:6px;display:inline-block;position:relative}
.yt-logo i:after{content:"";position:absolute;left:11px;top:5px;border-left:9px solid #fff;border-top:5.5px solid transparent;border-bottom:5.5px solid transparent}
.yt-logo sup{font-size:9px;font-weight:400;opacity:.7;margin-left:2px;vertical-align:top}
.yt-s{margin-left:auto;margin-right:auto;display:flex;align-items:center}
.yt-s .in{width:540px;height:40px;border:1px solid #303030;border-radius:20px 0 0 20px;background:#121212;display:flex;align-items:center;padding-left:16px;color:#888;font-size:16px}
.yt-s .b{width:64px;height:40px;border:1px solid #303030;border-left:0;border-radius:0 20px 20px 0;background:#222;display:flex;align-items:center;justify-content:center}
.yt-s .mic{width:40px;height:40px;border-radius:50%;background:#181818;margin-left:12px;display:flex;align-items:center;justify-content:center}
.yt-r{display:flex;align-items:center;gap:22px}
.yt-bell{position:relative}.yt-bell b{position:absolute;top:-6px;right:-8px;background:#f00;color:#fff;font-size:10px;border-radius:9px;padding:1px 5px;font-weight:500}
.yt-m{display:flex;gap:24px;padding:0 24px;flex:1}
.yt-l{width:1070px}
.yt-p{width:1070px;height:602px;border-radius:12px;overflow:hidden;position:relative;background:#0b0b0b}
.yt-ctl{position:absolute;left:0;right:0;bottom:0;height:52px;display:flex;align-items:center;padding:0 16px;gap:18px;font-size:13px;background:linear-gradient(transparent,rgba(0,0,0,.55))}
.yt-prog{position:absolute;left:12px;right:12px;bottom:50px;height:3px;background:rgba(255,255,255,.3)}
.yt-prog i{position:absolute;left:0;top:0;bottom:0;background:#f00}.yt-prog i:after{content:"";position:absolute;right:-6px;top:-5px;width:13px;height:13px;border-radius:50%;background:#f00}
.yt-ctl .sp{flex:1}.yt-ctl .cc{border:1.5px solid #fff;border-radius:2px;font-size:10px;padding:0 3px;font-weight:700}
.yt-t{font-size:20px;font-weight:600;margin:14px 0 10px}
.yt-ch{display:flex;align-items:center;gap:12px}
.yt-ch .n{font-weight:600;font-size:16px}.yt-ch .n small{font-size:12px;color:#aaa;display:block;font-weight:400;margin-top:2px}
.yt-sub{background:#f1f1f1;color:#0f0f0f;border-radius:18px;padding:9px 16px;font-weight:600;font-size:14px;margin-left:12px}
.yt-act{margin-left:auto;display:flex;gap:8px}
.yt-act span{background:#272727;border-radius:18px;padding:9px 16px;font-size:14px;font-weight:600;display:flex;align-items:center;gap:8px}
.yt-side{flex:1}
.chips{display:flex;gap:8px;margin:0 0 14px;overflow:hidden;white-space:nowrap}
.chips span{background:#272727;border-radius:8px;padding:7px 12px;font-size:14px;font-weight:500}.chips span.on{background:#f1f1f1;color:#0f0f0f}
.vid{display:flex;gap:8px;margin-bottom:8px;padding:4px;border-radius:8px}.vid.on{background:#262626}
.vid .th{width:168px;height:94px;border-radius:8px;position:relative;flex:none;overflow:hidden;background:#1a1a1a}
.vid .th b{position:absolute;right:6px;bottom:6px;background:rgba(0,0,0,.8);font-size:11px;padding:2px 4px;border-radius:4px;font-weight:500}
.vid .i{font-size:14px;font-weight:500;line-height:1.35}.vid .i small{display:block;color:#aaa;font-size:12px;margin-top:6px;font-weight:400}
.vid .num{width:18px;color:#aaa;font-size:13px;display:flex;align-items:center;justify-content:center}
.th .tt{position:absolute;left:8px;top:8px;right:8px;font-size:12px;font-weight:700;line-height:1.1}
.th .dg{position:absolute;left:10px;right:10px;bottom:12px;display:flex;gap:6px}
.th .dg i{flex:1;height:22px;border:1px solid rgba(255,255,255,.5);border-radius:3px}
"""


def yt_thumb(title, sub, accent, kind):
    # chalkboard-style drawn thumbnails
    if kind == "ring":
        dia = """<svg width="470" height="300" viewBox="0 0 470 300" style="position:absolute;right:40px;top:250px"><circle cx="235" cy="150" r="118" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="8 7"/>
        <g font-family="Chalkboard SE" font-size="20" fill="#fff">%s</g></svg>""" % "".join(
            f'<circle cx="{235+118*__import__("math").cos(a):.0f}" cy="{150+118*__import__("math").sin(a):.0f}" r="18" fill="{c}"/><text x="{235+150*__import__("math").cos(a):.0f}" y="{156+150*__import__("math").sin(a):.0f}" text-anchor="middle">{l}</text>'
            for a, c, l in [(-1.2, "#4f9cff", "node A"), (0.3, "#ff6b6b", "node B"), (1.9, "#ffd34f", "node C"), (3.4, "#6be67c", "node D"), (4.6, "#c58cff", "key 42")])
    elif kind == "kv":
        cells = "".join(f'<div style="width:46px;height:46px;border:2px solid #fff;border-radius:6px;background:{"#2d7cf6" if (i%7)<4 else "transparent"}"></div>' for i in range(28))
        dia = f'<div style="position:absolute;right:60px;top:150px;width:420px;display:grid;grid-template-columns:repeat(7,46px);gap:10px">{cells}</div><div style="position:absolute;right:60px;top:450px;{HAND}font-size:26px;color:#9ad0ff">cached keys / values per layer</div>'
    elif kind == "msgs":
        dia = '<div style="position:absolute;right:70px;top:140px;display:flex;flex-direction:column;gap:14px">' + "".join(
            f'<div style="display:flex;gap:14px;align-items:center"><div style="width:110px;height:54px;border:2.5px solid #fff;border-radius:8px;display:flex;align-items:center;justify-content:center;{HAND}font-size:18px">{a}</div><div style="color:#ffd34f;font-size:28px">→</div><div style="width:150px;height:54px;border:2.5px solid #6be67c;border-radius:8px;display:flex;align-items:center;justify-content:center;{HAND}font-size:18px;color:#6be67c">{b}</div></div>'
            for a, b in [("client", "gateway"), ("gateway", "shard 1..512"), ("shard", "storage"), ("fanout", "1T+ rows")]) + "</div>"
    else:  # bucket
        dia = f"""<svg width="420" height="320" viewBox="0 0 420 320" style="position:absolute;right:70px;top:150px"><path d="M120 40v200q0 30 30 30h120q30 0 30-30V40" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
        {"".join(f'<circle cx="{150+ (i%4)*34}" cy="{240-(i//4)*34}" r="14" fill="#ffd34f"/>' for i in range(10))}
        <path d="M40 60q40-40 70-10" fill="none" stroke="#6be67c" stroke-width="5"/><text x="20" y="110" font-family="Chalkboard SE" font-size="22" fill="#6be67c">tokens in</text>
        <path d="M300 290q40 20 80-10" fill="none" stroke="#ff6b6b" stroke-width="5"/><text x="290" y="250" font-family="Chalkboard SE" font-size="22" fill="#ff6b6b">requests out</text></svg>"""
    return f"""<div style="position:absolute;inset:0;background:radial-gradient(1200px 700px at 30% 20%,#17181c,#0b0b0d)">
      <div style="position:absolute;left:52px;top:46px;{HAND}font-size:86px;font-weight:700;letter-spacing:-1px;line-height:1">{title}</div>
      <div style="position:absolute;left:56px;top:150px;{HAND}font-size:40px;color:#fff">{sub}</div>
      <div style="position:absolute;left:56px;top:206px;width:420px;height:6px;background:{accent};border-radius:3px;transform:rotate(-.6deg)"></div>
      {dia}</div>"""


def yt_page(title, channel, subs, time_, total, chapter, thumb, sidebar, active=0, chips=("All", "From {ch}", "Related")):
    vids = ""
    for k, (t, ch, dur, c1, c2) in enumerate(sidebar):
        on = " on" if k == active else ""
        vids += f'''<div class="vid{on}"><div class="num">{"▸" if k == active else k + 1}</div><div class="th" style="background:linear-gradient(135deg,{c1},{c2})"><span class="tt" style="{HAND}">{t.split(" - ")[0][:34]}</span><span class="dg"><i></i><i></i><i></i></span><b>{dur}</b></div><div class="i">{t}<small>{ch}</small></div></div>'''
    chipsh = "".join(f'<span class="{"on" if k == 0 else ""}">{c.format(ch=channel)}</span>' for k, c in enumerate(chips))
    return f"""<div class="yt">
<div class="yt-h"><svg width="22" height="22" viewBox="0 0 24 24" fill="#fff"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>
 <div class="yt-logo"><i></i>YouTube<sup>IN</sup></div>
 <div class="yt-s"><div class="in">Search</div><div class="b"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg></div><div class="mic"><svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0" fill="none" stroke="#fff" stroke-width="2"/><path d="M12 18v3" stroke="#fff" stroke-width="2"/></svg></div></div>
 <div class="yt-r"><span class="yt-bell"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8"><path d="M18 16v-5a6 6 0 0 0-12 0v5l-2 2h16zM10 20a2 2 0 0 0 4 0"/></svg><b>9+</b></span>{av(32)}</div></div>
<div class="yt-m"><div class="yt-l">
 <div class="yt-p">{thumb}
  <div class="yt-prog"><i style="width:{int(100*time_/total)}%"></i></div>
  <div class="yt-ctl"><svg width="26" height="26" viewBox="0 0 24 24" fill="#fff"><path d="M6 4l14 8-14 8z"/></svg><svg width="24" height="24" viewBox="0 0 24 24" fill="#fff"><path d="M5 4l10 8-10 8zM17 4h2v16h-2z"/></svg><svg width="24" height="24" viewBox="0 0 24 24" fill="#fff"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16 8a5 5 0 0 1 0 8" fill="none" stroke="#fff" stroke-width="2"/></svg><span>{fmt(time_)} / {fmt(total)} &nbsp;·&nbsp; {chapter} ›</span><span class="sp"></span><span class="cc">CC</span><svg width="22" height="22" viewBox="0 0 24 24" fill="#fff"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" fill="none" stroke="#fff" stroke-width="1.6"/></svg><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><rect x="11" y="11" width="7" height="5" fill="#fff"/></svg><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/></svg><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></div>
 </div>
 <div class="yt-t">{title}</div>
 <div class="yt-ch">{av(40, "linear-gradient(135deg,#f6d365,#fda085)")}<div class="n">{channel} <span style="color:#aaa;font-size:13px">✓</span><small>{subs} subscribers</small></div><span class="yt-sub">Subscribe</span>
  <div class="yt-act"><span>👍&nbsp; 28K &nbsp;|&nbsp; 👎</span><span>↗ Share</span><span>···</span></div></div>
</div>
<div class="yt-side"><div class="chips">{chipsh}</div>{vids}</div></div></div>"""


def fmt(s):
    return f"{s // 60}:{s % 60:02d}"


# ------------------------------------------------------------------ builders for the other sites

def arxiv():
    css = """.ax{background:#fff;color:#000;height:100%;font-family:'Lucida Grande',Helvetica,Arial,sans-serif}
.ax-h{background:#b31b1b;height:50px;display:flex;align-items:center;padding:0 40px;color:#fff;font-size:17px;gap:24px}
.ax-h b{font-size:24px;font-weight:700;letter-spacing:-.5px}.ax-h .s{margin-left:auto;background:#fff;color:#999;width:300px;height:30px;border-radius:3px;padding:6px 10px;font-size:14px}
.ax-m{display:flex;gap:40px;padding:22px 40px}
.ax-a{flex:1}.ax-a .lbl{font-size:13px;color:#333;margin-bottom:6px}
.ax-a h1{font-size:30px;font-weight:700;line-height:1.15;margin:4px 0 14px;font-family:Georgia,serif}
.ax-a .au{color:#0a5bbd;font-size:15px;line-height:1.7;margin-bottom:14px}
.ax-a p{font-size:16px;line-height:1.65;margin:0 0 16px}
.ax-a .meta{font-size:14px;line-height:1.7;color:#333}.ax-a .meta b{display:inline-block;width:140px;font-weight:700}
.ax-b{width:290px}.ax-b h3{font-size:14px;margin:0 0 8px;font-weight:700}.ax-b a{display:block;color:#0a5bbd;font-size:15px;line-height:1.9}
.ax-b .box{border:1px solid #ddd;border-radius:3px;padding:14px;margin-bottom:16px;background:#f7f7f7}
.ax-b .pdf{background:#b31b1b;color:#fff;padding:8px 12px;border-radius:3px;display:inline-block;font-size:14px;font-weight:700}
"""
    body = """<div class="ax"><div class="ax-h"><b>arXiv</b><span>&gt; cs &gt; arXiv:2309.06180</span><span class="s">Search...</span></div>
<div class="ax-m"><div class="ax-a">
<div class="lbl">Computer Science &gt; Machine Learning</div><div class="lbl" style="color:#888">[Submitted on 12 Sep 2023]</div>
<h1>Efficient Memory Management for Large Language Model Serving with PagedAttention</h1>
<div class="au">Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, Ion Stoica</div>
<p>Serving a large language model means keeping a key-value cache for every request in flight. Existing systems allocate that cache as one contiguous block per request and waste most of it to fragmentation and over-reservation, which caps the batch size and therefore the throughput. The paper borrows virtual memory and paging from operating systems: the KV cache is split into fixed-size blocks that do not need to be contiguous, so memory is allocated as tokens are generated and shared across requests that have a common prefix.</p>
<p>Built into a serving system called vLLM, the approach keeps KV-cache waste near zero and lets many more requests share a GPU. The evaluation reports several times the throughput of earlier systems at the same latency, with the biggest gains on long sequences, large models and complex decoding such as parallel sampling and beam search.</p>
<div class="meta"><div><b>Comments:</b> SOSP 2023</div><div><b>Subjects:</b> Machine Learning (cs.LG); Distributed, Parallel, and Cluster Computing (cs.DC)</div><div><b>Cite as:</b> <span style="color:#0a5bbd">arXiv:2309.06180</span> [cs.LG]</div></div>
</div>
<div class="ax-b"><div class="box"><h3>Access Paper:</h3><span class="pdf">View PDF</span><a>TeX Source</a><a>Other Formats</a></div>
<div class="box" style="background:#fff"><h3>References &amp; Citations</h3><a>NASA ADS</a><a>Google Scholar</a><a>Semantic Scholar</a></div>
<div class="box" style="background:#fff"><h3>Bookmark</h3><a>BibSonomy</a><a>Reddit</a></div></div></div></div>"""
    return dict(theme="light", icon="arxiv", title="[2309.06180] Efficient Memory Management for Large Language Model Serving with PagedAttention", host="arxiv.org", path="/abs/2309.06180", body=body, css=css)


GH_CSS = """
.gh{height:100%;background:var(--gbg);color:var(--gfg);font-size:14px}
.gh-top{height:62px;display:flex;align-items:center;padding:0 18px;gap:14px;border-bottom:1px solid var(--gbd)}
.gh-top .path{font-size:16px}.gh-top .path b{font-weight:600}.gh-top .s{margin-left:auto;border:1px solid var(--gbd);border-radius:6px;padding:5px 12px;width:320px;color:#777;font-size:14px}
.gh-tabs{display:flex;gap:4px;padding:0 18px;border-bottom:1px solid var(--gbd);height:46px;align-items:flex-end}
.gh-tabs span{padding:10px 8px 12px;font-size:14px;display:flex;gap:6px;align-items:center}.gh-tabs span.on{border-bottom:2px solid #fd8c73;font-weight:600}
.gh-tabs b{background:var(--gpill);border-radius:10px;padding:0 7px;font-size:12px;font-weight:500}
.gh-m{display:flex;gap:26px;padding:22px 26px}
.gh-f{flex:1;border:1px solid var(--gbd);border-radius:6px;overflow:hidden}
.gh-f .r{display:flex;gap:12px;padding:9px 16px;border-top:1px solid var(--gbd);align-items:center}.gh-f .r.h{background:var(--gpill2);border-top:0}
.gh-f .r .fn{width:300px;color:var(--glink)}.gh-f .r .msg{flex:1;color:#8b949e;white-space:nowrap;overflow:hidden}.gh-f .r .ago{color:#8b949e;width:120px;text-align:right}
.gh-s{width:300px}.gh-s h3{font-size:16px;margin:0 0 8px}.gh-s p{color:#8b949e;line-height:1.5;margin:0 0 12px}.gh-s .st{display:flex;gap:16px;color:#8b949e;margin:0 0 20px}.gh-s .st b{color:var(--gfg)}
.gh-s .tg{display:inline-block;background:var(--gtag);color:var(--glink);border-radius:12px;padding:3px 10px;font-size:12px;margin:0 4px 6px 0}
.btn{border:1px solid var(--gbd);background:var(--gpill2);border-radius:6px;padding:5px 12px;font-weight:500;font-size:13px;display:inline-flex;gap:6px;align-items:center}
.btn.g{background:#1f883d;color:#fff;border-color:#1f883d}
"""
GH_LIGHT = "--gbg:#fff;--gfg:#1f2328;--gbd:#d0d7de;--gpill:#e8ebef;--gpill2:#f6f8fa;--glink:#0969da;--gtag:#ddf4ff"
GH_DARK = "--gbg:#0d1117;--gfg:#e6edf3;--gbd:#30363d;--gpill:#30363d;--gpill2:#161b22;--glink:#58a6ff;--gtag:#121d2f"


def gh_top(path_html, theme):
    mark = icon("github_dark" if theme == "dark" else "github", 32)
    return f'<div class="gh-top">{mark}<span class="path">{path_html}</span><span class="s">Type <span style="border:1px solid #777;border-radius:4px;padding:0 4px;font-size:11px">/</span> to search</span><span class="btn">+ ▾</span><span class="av" style="width:32px;height:32px"></span></div>'


def github_repo():
    rows = [("📁", ".github", "Update workflows", "2 years ago"), ("📁", "resources", "Add links to additional learning resources", "1 year ago"),
            ("📁", "solutions", "Add Pastebin and Twitter timeline solutions", "2 years ago"), ("📄", ".gitignore", "Initial commit", "8 years ago"),
            ("📄", "CONTRIBUTING.md", "Add contributing guidelines", "7 years ago"), ("📄", "LICENSE.txt", "Update license", "6 years ago"),
            ("📄", "README.md", "Fix typo in CAP section", "3 months ago"), ("📄", "README-zh-Hans.md", "Update Chinese translation", "7 months ago")]
    rh = "".join(f'<div class="r"><span>{a}</span><span class="fn">{b}</span><span class="msg">{c}</span><span class="ago">{d}</span></div>' for a, b, c, d in rows)
    body = f"""<div class="gh" style="{GH_LIGHT}">{gh_top("donnemartin / <b>system-design-primer</b>", "light")}
<div class="gh-tabs"><span class="on">&lt;&gt; Code</span><span>◎ Issues <b>246</b></span><span>⑂ Pull requests <b>171</b></span><span>▷ Actions</span><span>⊞ Projects</span><span>⛉ Security</span><span>⩪ Insights</span></div>
<div class="gh-m"><div style="flex:1"><div style="display:flex;gap:8px;margin-bottom:14px;align-items:center"><span class="btn">⑂ master ▾</span><span style="color:#8b949e">59 Branches · 0 Tags</span><span style="margin-left:auto" class="btn">Go to file</span><span class="btn">+</span><span class="btn g">&lt;&gt; Code ▾</span></div>
<div class="gh-f"><div class="r h">{av(22)}<span style="font-weight:600">donnemartin</span><span class="msg">Fix typo in CAP section</span><span class="ago">3 months ago · 2,146 commits</span></div>{rh}</div>
<div style="margin-top:22px;border:1px solid #d0d7de;border-radius:6px;padding:18px 24px"><div style="font-size:24px;font-weight:600;border-bottom:1px solid #d0d7de;padding-bottom:8px;margin-bottom:12px">The System Design Primer</div><p style="line-height:1.6;color:#1f2328">Learn how to design large-scale systems. Prep for the system design interview. Index of topics: scalability, latency vs throughput, availability vs consistency, CAP theorem, consistency patterns, DNS, CDN, load balancer, reverse proxy, microservices, database, cache, asynchronism, communication.</p></div></div>
<div class="gh-s"><h3>About</h3><p>Learn how to design large-scale systems. Prep for the system design interview. Includes Anki flashcards.</p>
<div class="st"><span>☆ <b>281k</b> stars</span><span>👁 <b>6.9k</b> watching</span><span>⑂ <b>46.6k</b> forks</span></div>
<span class="tg">system</span><span class="tg">design</span><span class="tg">interview</span><span class="tg">scalability</span><span class="tg">web</span><span class="tg">programming</span><span class="tg">development</span><span class="tg">interview-questions</span><span class="tg">interview-practice</span>
<h3 style="margin-top:22px">Readme</h3><h3>Releases</h3><p>No releases published</p></div></div></div>"""
    return dict(theme="light", icon="github", title="donnemartin/system-design-primer: Learn how to design large-scale systems. Prep for the system design interview.", host="github.com", path="/donnemartin/system-design-primer", body=body, css=GH_CSS)


def github_pr():
    diff = [("+", "    if queue.depth() > SHED_THRESHOLD:"), ("+", "        metrics.inc('shed_total')"), ("+", "        raise HTTPException(503, 'overloaded, retry later')"),
            (" ", "    item = Request(prompt=body.prompt, max_tokens=body.max_tokens)"), ("-", "    await queue.put(item)"), ("+", "    await queue.put(item, timeout=QUEUE_TIMEOUT_S)")]
    dh = "".join(f'<div style="display:flex;background:{ {"+": "#12261e", "-": "#2a1518", " ": "transparent"}[s]};padding:2px 10px"><span style="width:60px;color:#6e7681">{40 + k}</span><span style="width:18px;color:{"#3fb950" if s == "+" else "#f85149" if s == "-" else "#8b949e"}">{s}</span><span>{t}</span></div>' for k, (s, t) in enumerate(diff))
    body = f"""<div class="gh" style="{GH_DARK}">{gh_top("abik / <b>queue-demo</b>", "dark")}
<div style="padding:18px 26px 0"><div style="font-size:28px;font-weight:400">Load shedding for the request queue <span style="color:#8b949e">#4</span></div>
<div style="display:flex;align-items:center;gap:10px;margin:10px 0 14px;color:#8b949e"><span style="background:#238636;color:#fff;border-radius:16px;padding:5px 12px;font-weight:500">⑂ Open</span><b style="color:#e6edf3">abik</b> wants to merge 3 commits into <span style="background:#121d2f;color:#58a6ff;padding:1px 6px;border-radius:4px">main</span> from <span style="background:#121d2f;color:#58a6ff;padding:1px 6px;border-radius:4px">load-shedding</span></div></div>
<div class="gh-tabs"><span class="on">💬 Conversation <b>2</b></span><span>⊙ Commits <b>3</b></span><span>✓ Checks <b>4</b></span><span>± Files changed <b>5</b></span></div>
<div class="gh-m"><div style="flex:1">
<div style="border:1px solid #30363d;border-radius:6px;overflow:hidden"><div style="background:#161b22;padding:10px 16px;border-bottom:1px solid #30363d;color:#8b949e"><b style="color:#e6edf3">abik</b> commented 2 hours ago</div><div style="padding:16px;line-height:1.6">When the queue goes past 18k requests/sec the p99 climbs to 9 s and the GPU workers never catch up. This PR sheds load at the gateway once queue depth crosses a threshold, returns 503 with Retry-After, and adds a timeout on enqueue so a stuck worker cannot pin memory forever.<br><br>Before: p99 9.1 s under 18k rps. After: p99 410 ms with 6% of requests shed.</div></div>
<div class="mono" style="margin-top:16px;border:1px solid #30363d;border-radius:6px;font-size:12.5px;overflow:hidden"><div style="background:#161b22;padding:8px 12px;color:#8b949e;border-bottom:1px solid #30363d">gateway/app.py</div>{dh}</div>
<div style="margin-top:16px;border:1px solid #30363d;border-radius:6px;padding:14px 16px;display:flex;align-items:center;gap:12px"><span style="color:#3fb950;font-size:20px">✓</span><div><b>All checks have passed</b><div style="color:#8b949e">4 successful checks · lint, unit, load-test (18k rps), build</div></div><span class="btn g" style="margin-left:auto">Merge pull request ▾</span></div>
</div><div class="gh-s"><h3 style="font-size:12px;color:#8b949e">Reviewers</h3><p>{av(20)} maya-k · ✓ approved</p><h3 style="font-size:12px;color:#8b949e">Labels</h3><span class="tg">performance</span><span class="tg">backend</span><h3 style="font-size:12px;color:#8b949e;margin-top:14px">Milestone</h3><p>v0.3 · production readiness</p></div></div></div>"""
    return dict(theme="dark", icon="github_dark", title="Load shedding for the request queue by abik · Pull Request #4 · abik/queue-demo", host="github.com", path="/abik/queue-demo/pull/4", body=body, css=GH_CSS)


def claude_docs():
    css = """.cd{height:100%;background:#0e0e0f;color:#e8e8e6;display:flex;flex-direction:column}
.cd-h{height:60px;border-bottom:1px solid #26262a;display:flex;align-items:center;padding:0 28px;gap:28px;font-size:14.5px}
.cd-h .lg{font-weight:600;font-size:17px;display:flex;align-items:center;gap:10px}.cd-h .s{border:1px solid #2e2e33;border-radius:8px;padding:7px 14px;width:360px;color:#8a8a8e;margin-left:30px}
.cd-m{display:flex;flex:1}
.cd-n{width:270px;border-right:1px solid #26262a;padding:22px 18px;font-size:14px;line-height:2.05;color:#b3b3b6}.cd-n b{display:block;color:#fff;font-weight:600;margin-top:10px}.cd-n .on{color:#e7b091;background:#1d1a19;border-radius:6px;padding:0 10px;margin:0 -10px;display:block}
.cd-a{flex:1;padding:30px 60px;max-width:960px}.cd-a .crumb{color:#e7b091;font-size:13px;margin-bottom:10px}
.cd-a h1{font-size:38px;font-weight:600;letter-spacing:-.5px;margin-bottom:10px}.cd-a .sub{color:#9a9a9e;font-size:18px;margin-bottom:26px}
.cd-a p{font-size:16px;line-height:1.7;margin-bottom:18px;color:#d4d4d2}.cd-a h2{font-size:24px;margin:26px 0 12px;font-weight:600}
.code{background:#151517;border:1px solid #2a2a2e;border-radius:10px;padding:16px 18px;font-size:14px;line-height:1.7;color:#e8e8e6}.code .c{color:#7fb37f}
.cd-t{width:250px;padding:30px 24px;font-size:13.5px;color:#9a9a9e;line-height:2}.cd-t b{color:#fff;display:block;font-weight:600}
"""
    body = f"""<div class="cd"><div class="cd-h"><span class="lg">{icon('claude', 26)} Claude Docs</span><span class="s">Search or ask...  ⌘K</span><span style="margin-left:auto">Developer Platform</span><span>Claude Code</span><span>Agent SDK</span><span>API Reference</span><span style="background:#e7b091;color:#1a1a1a;padding:7px 14px;border-radius:8px;font-weight:600">Console</span></div>
<div class="cd-m"><div class="cd-n"><b>Getting started</b><span class="on">Overview</span>Quickstart<span style="display:block">Common workflows</span><b>Build with Claude Code</b>Subagents<br>Output styles<br>Hooks<br>GitHub Actions<br>Model Context Protocol<br><b>Configuration</b>Settings<br>Memory<br>Permissions<br>Terminal config<br><b>Reference</b>CLI reference<br>Interactive mode<br>Slash commands</div>
<div class="cd-a"><div class="crumb">Getting started</div><h1>Claude Code overview</h1><div class="sub">Learn about Claude Code, the agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.</div>
<h2>Get started in 30 seconds</h2><p>Prerequisites: Node.js 18 or newer. Install the CLI, open any project in your terminal, and start a session.</p>
<div class="code mono"><span class="c"># Install Claude Code</span><br>npm install -g @anthropic-ai/claude-code<br><br><span class="c"># Navigate to your project</span><br>cd inference-demo<br><br><span class="c"># Start Claude Code</span><br>claude</div>
<h2>What Claude Code does for you</h2><p><b>Build features from descriptions.</b> Tell Claude what you want to build in plain English. It will make a plan, write the code, and verify it works.</p><p><b>Debug and fix issues.</b> Describe a bug or paste an error message. Claude Code analyzes your codebase, identifies the problem, and implements a fix.</p></div>
<div class="cd-t"><b>On this page</b>Get started in 30 seconds<br>What Claude Code does for you<br>Why developers love Claude Code<br>Next steps<br>Additional resources</div></div></div>"""
    return dict(theme="dark", icon="claude", title="Claude Code overview - Claude Docs", host="docs.claude.com", path="/en/docs/claude-code/overview", body=body, css=css)


TERM_CSS = """.term{height:100%;padding:12px 16px;font-size:13.5px;line-height:1.5;white-space:pre;color:var(--tc);background:var(--tbg);overflow:hidden}
.term .d{color:#8a8a8a}.term .o{color:#d97757}.term .g{color:#4fc26b}.term .b{color:#5aa0ff}.term .y{color:#e3b341}.term .w{color:#fff;font-weight:600}
.term .box{display:inline-block;border:1px solid var(--tc);border-radius:4px;padding:4px 10px;margin:2px 0}
.term .in{border:1px solid #666;border-radius:4px;padding:6px 10px;margin-top:10px;display:block;white-space:pre}
"""


def term_claude():
    body = """<div class="term mono" style="--tc:#dcdcdc;--tbg:#1a1a1a"><div class="box" style="border-color:#d97757;padding:8px 14px;line-height:1.6"><span class="o">✻</span> <span class="w">Welcome to Claude Code!</span>

  /help for help, /status for your current setup

  cwd: /Users/abik/inference-demo
</div>

<span class="d">Tips for getting started:</span>
<span class="d">  Run /init to create a CLAUDE.md file with instructions for Claude</span>

<span class="w">&gt;</span> make /generate batch waiting requests every 8 ms and stream tokens back as SSE

<span class="o">⏺</span> I'll look at how the endpoint is wired first, then add a small batching loop.

<span class="g">⏺</span> <span class="w">Read</span>(server/serve.py)
  <span class="d">⎿  Read 142 lines</span>

<span class="g">⏺</span> <span class="w">Read</span>(server/engine.py)
  <span class="d">⎿  Read 88 lines</span>

<span class="g">⏺</span> <span class="w">Update</span>(server/serve.py)
  <span class="d">⎿  Added 31 lines, removed 6 lines</span>
     <span class="g">+ class Batcher:</span>
     <span class="g">+     def __init__(self, engine, window_ms=8, max_batch=16):</span>
     <span class="g">+         self.queue = asyncio.Queue()</span>
     <span class="g">+     async def run(self):</span>
     <span class="g">+         while True:</span>
     <span class="g">+             batch = await self._collect(self.window_ms)</span>
     <span class="g">+             async for tok in self.engine.generate(batch): ...</span>

<span class="g">⏺</span> <span class="w">Bash</span>(python -m pytest tests/test_batch.py -q)
  <span class="d">⎿  5 passed in 1.84s</span>

<span class="o">⏺</span> Done. Requests now wait up to 8 ms, get batched (max 16) and stream over SSE.
  TTFT in the local benchmark went from 184 ms to 92 ms at 40 concurrent clients.

<span class="in"><span class="w">&gt;</span> <span class="d">Try "add a load test for 18k rps"</span></span>
<span class="d">  ? for shortcuts                                              claude-fable-5-1 · ⏵⏵ accept edits on</span></div>"""
    return dict(kind="terminal", theme="dark", title="claude", sub="— ~/inference-demo — zsh — 120×36", body=body, css=TERM_CSS)


def term_codex():
    body = """<div class="term mono" style="--tc:#2a2a2a;--tbg:#ffffff"><span class="d">OpenAI Codex (research preview) v0.42</span>
<span class="d">model: gpt-5-codex · approval: on-request · directory: ~/queue-sim</span>

<span class="w">user</span>
simulate the request queue at 18,000 rps with 4 workers and show where it breaks

<span class="w">codex</span>
I'll run the simulator with the production config and sweep the arrival rate.

<span class="b">$ python sim.py --workers 4 --rps 6000,12000,18000,24000 --duration 30</span>

  rps     depth(max)   p50      p99      shed    gpu util
  6000         41      38 ms    120 ms   0.0%    61%
 12000        118      55 ms    310 ms   0.0%    88%
 18000       2947     640 ms    9.1 s    0.0%    97%   <span class="y">← breakpoint</span>
 24000      11860     2.8 s     31 s     0.0%    97%

At 18k the arrival rate passes the service rate (4 workers × ~4,300 rps). Queue depth
grows without bound, so latency is the queue, not the model. Two fixes:
  1. shed load above a depth threshold (fast, protects p99 for everyone else)
  2. add a 5th worker (raises the breakpoint to ~21.5k, costs a GPU)

<span class="w">codex</span> wants to run: <span class="b">python sim.py --workers 4 --rps 18000 --shed-depth 400</span>
  <span class="g">▸ Yes (y)</span>   Yes, don't ask again for this command   No (n)

<span class="d">⏎ send  ⌃J newline  ⌃T transcript  ⌃C quit                                         92% context left</span></div>"""
    return dict(kind="terminal", theme="light", title="codex", sub="— ~/queue-sim — zsh — 120×36", body=body, css=TERM_CSS)


def wikipedia():
    css = """.wk{height:100%;background:#fff;color:#202122;font-family:sans-serif;display:flex;flex-direction:column}
.wk-h{height:60px;display:flex;align-items:center;padding:0 30px;gap:20px;border-bottom:1px solid #eaecf0}
.wk-h .lg{font-family:'Linux Libertine',Georgia,serif;font-size:21px;line-height:1}.wk-h .lg small{display:block;font-size:11px;font-family:sans-serif;letter-spacing:1px}
.wk-h .s{border:1px solid #a2a9b1;border-radius:2px;width:520px;padding:7px 10px;color:#72777d;font-size:14px;margin-left:40px}
.wk-m{display:flex;flex:1}
.wk-toc{width:240px;padding:24px 20px;font-size:14px;line-height:1.9;color:#36c}.wk-toc b{color:#202122;display:block}.wk-toc .on{color:#202122;border-left:3px solid #36c;padding-left:8px;margin-left:-11px}
.wk-a{flex:1;padding:20px 40px 0 20px;max-width:1150px}
.wk-a h1{font-family:'Linux Libertine',Georgia,serif;font-size:28.8px;font-weight:400;border-bottom:1px solid #a2a9b1;padding-bottom:4px;margin-bottom:6px}
.wk-a .f{font-size:13px;color:#54595d;margin-bottom:14px}
.wk-a p{font-size:14.5px;line-height:1.6;margin-bottom:12px}.wk-a a{color:#36c}
.wk-a h2{font-family:'Linux Libertine',Georgia,serif;font-size:22px;font-weight:400;border-bottom:1px solid #a2a9b1;margin:18px 0 10px}
.wk-ib{float:right;border:1px solid #a2a9b1;background:#f8f9fa;padding:12px;margin:0 0 14px 20px;width:300px;font-size:12.5px;text-align:center}
.wk-tabs{display:flex;gap:18px;font-size:14px;color:#36c;border-bottom:1px solid #a2a9b1;margin-bottom:12px}.wk-tabs span{padding:6px 0}.wk-tabs .on{color:#202122;border-bottom:2px solid #36c}
"""
    tri = """<svg width="260" height="230" viewBox="0 0 260 230"><polygon points="130,20 20,210 240,210" fill="none" stroke="#333" stroke-width="2"/><circle cx="130" cy="20" r="26" fill="#eaf3ff" stroke="#36c"/><circle cx="20" cy="210" r="26" fill="#fff4e5" stroke="#e67e22"/><circle cx="240" cy="210" r="26" fill="#eafaea" stroke="#2e8b57"/><text x="130" y="25" text-anchor="middle" font-size="13" font-weight="700">C</text><text x="20" y="215" text-anchor="middle" font-size="13" font-weight="700">A</text><text x="240" y="215" text-anchor="middle" font-size="13" font-weight="700">P</text><text x="130" y="128" text-anchor="middle" font-size="12" fill="#555">pick two</text></svg>"""
    body = f"""<div class="wk"><div class="wk-h"><span style="font-size:20px">☰</span><div class="lg">WIKIPEDIA<small>The Free Encyclopedia</small></div><span class="s">🔍 Search Wikipedia</span><span style="margin-left:auto;color:#36c;font-size:14px">Donate</span><span style="color:#36c;font-size:14px">Create account</span><span style="color:#36c;font-size:14px">Log in</span></div>
<div class="wk-m"><div class="wk-toc"><b>Contents</b><span class="on">(Top)</span><br>Explanation<br>Database PACELC<br>History<br>See also<br>References<br>External links</div>
<div class="wk-a"><h1>CAP theorem</h1><div class="wk-tabs"><span class="on">Article</span><span>Talk</span><span style="margin-left:auto">Read</span><span>Edit</span><span>View history</span><span>Tools ▾</span></div><div class="f">From Wikipedia, the free encyclopedia</div>
<div class="wk-ib">{tri}<div style="margin-top:6px">The three properties of the CAP theorem. A distributed data store can guarantee only two of them at the same time.</div></div>
<p>In <a>database theory</a>, the <b>CAP theorem</b>, also named <b>Brewer's theorem</b> after computer scientist <a>Eric Brewer</a>, states that any <a>distributed data store</a> can provide at most two of the following three guarantees:</p>
<p><b>Consistency</b> — every read receives the most recent write or an error.<br><b>Availability</b> — every request receives a non-error response, without the guarantee that it contains the most recent write.<br><b>Partition tolerance</b> — the system continues to operate despite an arbitrary number of messages being dropped or delayed by the network between nodes.</p>
<p>When a network partition happens, a system has to choose between cancelling the operation, which lowers availability but keeps consistency, or proceeding with the operation, which keeps availability but risks inconsistency. Since partitions cannot be ruled out in a real network, the practical choice is between consistency and availability only while a partition is in progress.</p>
<h2>Explanation</h2><p>No distributed system is safe from network failures, so partition tolerance has to be assumed. The theorem is therefore often summarised as a trade-off between consistency and availability under partition, and the <a>PACELC</a> extension adds the latency trade-off that exists even when the network is healthy.</p></div></div></div>"""
    return dict(theme="light", icon="wikipedia", title="CAP theorem - Wikipedia", host="en.wikipedia.org", path="/wiki/CAP_theorem", body=body, css=css)


def localhost_demo():
    css = """.ld{height:100%;background:#0b0d12;color:#e6e8ee;padding:34px 56px;font-size:15px}
.ld-h{display:flex;align-items:center;gap:14px;margin-bottom:26px}.ld-h b{font-size:20px;font-weight:600}.ld-h .pill{background:#17331f;color:#5ee38a;border-radius:12px;padding:3px 10px;font-size:12px}
.ld-g{display:grid;grid-template-columns:1fr 420px;gap:26px}
.card{background:#12151c;border:1px solid #232733;border-radius:12px;padding:20px 22px}
.card h3{font-size:13px;font-weight:500;color:#8b92a5;margin-bottom:10px;text-transform:uppercase;letter-spacing:.6px}
.prompt{background:#0f1218;border:1px solid #2a2f3d;border-radius:10px;padding:14px 16px;font-size:15px;color:#c9cdd8;display:flex;align-items:center}.prompt b{margin-left:auto;background:#4f7cff;color:#fff;padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600}
.out{font-size:16.5px;line-height:1.75;margin-top:16px}.out span{background:#1a2238;border-radius:4px;padding:0 3px;margin:0 1px;display:inline-block}.out span.n{background:#223e2a}
.stat{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.stat div{background:#0f1218;border-radius:10px;padding:12px 14px}.stat b{font-size:26px;font-weight:600;display:block}.stat small{color:#8b92a5}
.bars{display:flex;align-items:flex-end;gap:5px;height:120px;margin-top:10px}.bars i{flex:1;background:#4f7cff;border-radius:3px 3px 0 0;display:block}
"""
    toks = "Quantum computing uses qubits , which can hold a blend of 0 and 1 at the same time . Where a classical bit answers one question per step , a qubit register explores many at once , and interference cancels the wrong answers before you measure .".split(" ")
    out = "".join(f'<span class="{"n" if k >= len(toks) - 6 else ""}">{t}</span> ' for k, t in enumerate(toks))
    bars = "".join(f'<i style="height:{h}%"></i>' for h in [40, 55, 48, 70, 62, 85, 78, 92, 66, 74, 88, 95, 71, 60, 83, 90, 76, 64, 58, 80, 69, 91, 73, 86])
    body = f"""<div class="ld"><div class="ld-h"><b>token-stream demo</b><span class="pill">● engine connected</span><span style="color:#8b92a5">Llama-3.1-8B-Instruct · fp8 · 1×H100</span><span style="margin-left:auto;color:#8b92a5">localhost:3000 → :8000/generate</span></div>
<div class="ld-g"><div><div class="card"><h3>Prompt</h3><div class="prompt">Explain quantum computing in simple terms<b>Generate</b></div><h3 style="margin-top:22px">Streaming output <span style="color:#5ee38a;text-transform:none;letter-spacing:0">● live · 61 tok/s</span></h3><div class="out">{out}<span style="background:#4f7cff;width:9px;height:20px;vertical-align:-4px"></span></div></div></div>
<div><div class="card"><h3>Request stats</h3><div class="stat"><div><b>84 ms</b><small>time to first token</small></div><div><b>61</b><small>tokens / s</small></div><div><b>8</b><small>batch size</small></div></div></div>
<div class="card" style="margin-top:16px"><h3>Inter-token latency (ms, last 24 tokens)</h3><div class="bars">{bars}</div><div style="display:flex;justify-content:space-between;color:#8b92a5;font-size:12px;margin-top:6px"><span>p50 14 ms</span><span>p99 23 ms</span></div></div>
<div class="card" style="margin-top:16px"><h3>KV cache</h3><div style="height:10px;background:#1a1f2b;border-radius:5px;overflow:hidden"><div style="width:63%;height:100%;background:linear-gradient(90deg,#4f7cff,#8a5cff)"></div></div><div style="color:#8b92a5;font-size:13px;margin-top:8px">63% of 80 GB · 1,412 blocks in use · 0 preempted</div></div></div></div></div>"""
    return dict(theme="dark", icon="globe", title="token-stream demo", host="localhost:3000", path="/playground?model=llama-3.1-8b", body=body, css=css)


def codex_openai():
    css = """.oa{height:100%;background:#fff;color:#000;display:flex;flex-direction:column}
.oa-h{height:64px;display:flex;align-items:center;padding:0 40px;gap:30px;font-size:15px}.oa-h .lg{font-weight:700;font-size:20px;display:flex;align-items:center;gap:8px}
.oa-h .r{margin-left:auto;display:flex;gap:22px;align-items:center}.oa-h .r b{background:#000;color:#fff;padding:9px 18px;border-radius:22px;font-weight:500}
.oa-b{display:flex;flex:1;padding:40px 60px 0 60px;gap:50px}
.oa-b h1{font-size:72px;font-weight:500;letter-spacing:-2.5px;line-height:1;margin:34px 0 20px}.oa-b p{font-size:22px;line-height:1.4;color:#333;max-width:560px}
.oa-b .cta{display:flex;gap:14px;margin-top:30px}.oa-b .cta span{border-radius:24px;padding:12px 22px;font-size:15px;font-weight:500;border:1px solid #000}.oa-b .cta span.d{background:#000;color:#fff}
.shot{flex:1;background:linear-gradient(160deg,#e9eef5,#f7f3ec);border-radius:18px;position:relative;overflow:hidden}
.shot .w{position:absolute;left:46px;top:40px;right:-60px;bottom:-40px;background:#fff;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.12);padding:22px 26px;font-size:14px;color:#333;line-height:1.7}
.shot .w b{display:block;font-size:16px;margin-bottom:8px}.shot .task{border:1px solid #e3e3e3;border-radius:10px;padding:10px 14px;margin:8px 0;display:flex;gap:10px;align-items:center}.shot .task i{width:8px;height:8px;border-radius:50%;background:#10a37f;display:inline-block}
"""
    body = """<div class="oa"><div class="oa-h"><span class="lg"><svg width="26" height="26" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" fill="#000"/><polygon points="12,5.7 12,10.3 8,12.6 4,10.3 4,5.7 8,3.4" fill="none" stroke="#fff" stroke-width="1.4"/></svg>OpenAI</span><span>Research</span><span>Product</span><span>Safety</span><span>Company</span><span class="r"><span>Log in</span><b>Try Codex</b></span></div>
<div class="oa-b"><div><div style="font-size:15px;color:#666">Product</div><h1>Codex</h1><p>A cloud-based software engineering agent that works on many tasks in parallel, in its own sandbox, and opens a pull request when it's done.</p>
<div class="cta"><span class="d">Try in ChatGPT</span><span>Read the docs</span><span>Install the CLI</span></div>
<div style="margin-top:50px;color:#666;font-size:14px">Available in ChatGPT Pro, Enterprise, Team and Plus.</div></div>
<div class="shot"><div class="w"><b>Tasks</b><div class="task"><i></i>Add load shedding to the request queue <span style="margin-left:auto;color:#10a37f">Open PR</span></div><div class="task"><i></i>Write tests for the batching loop <span style="margin-left:auto;color:#10a37f">Open PR</span></div><div class="task"><i style="background:#f5a623"></i>Profile serve.py under 18k rps <span style="margin-left:auto;color:#999">Running · 4 min</span></div><div class="task"><i style="background:#ccc"></i>Explain why p99 climbs after 12k rps <span style="margin-left:auto;color:#999">Queued</span></div><div style="margin-top:14px;color:#999">Ask Codex to do something… </div></div></div></div></div>"""
    return dict(theme="light", icon="openai", title="Codex | OpenAI", host="openai.com", path="/codex/", body=body, css=css)


def medium():
    css = """.md{height:100%;background:#fff;color:#242424}
.md-h{height:58px;border-bottom:1px solid #f2f2f2;display:flex;align-items:center;padding:0 24px;gap:16px}.md-h .lg{font-family:Georgia,serif;font-weight:700;font-size:28px;letter-spacing:-1px}
.md-h .s{background:#f9f9f9;border-radius:20px;padding:9px 16px;width:240px;color:#6b6b6b;font-size:14px}.md-h .r{margin-left:auto;display:flex;gap:20px;align-items:center;font-size:14px;color:#6b6b6b}.md-h .r b{background:#1a8917;color:#fff;border-radius:20px;padding:8px 16px;font-weight:400}
.md-a{max-width:680px;margin:0 auto;padding:40px 0 0}
.md-a h1{font-family:'Charter',Georgia,serif;font-size:42px;letter-spacing:-.6px;line-height:1.15;margin-bottom:10px;font-weight:700}.md-a .sub{font-family:Georgia,serif;font-size:22px;color:#6b6b6b;margin-bottom:28px}
.md-a .au{display:flex;align-items:center;gap:12px;font-size:14px;margin-bottom:18px}.md-a .au small{color:#6b6b6b;display:block}.md-a .au .f{color:#1a8917}
.md-a .bar{border-top:1px solid #f2f2f2;border-bottom:1px solid #f2f2f2;padding:10px 0;display:flex;gap:28px;color:#6b6b6b;font-size:14px;margin-bottom:30px}
.md-a p{font-family:'Charter',Georgia,serif;font-size:20px;line-height:1.6;margin-bottom:26px}
"""
    body = f"""<div class="md"><div class="md-h"><span class="lg">Medium</span><span class="s">🔍 Search</span><span class="r"><span>✎ Write</span><span>🔔</span>{av(32)}</span></div>
<div class="md-a"><h1>Speculative decoding, explained simply</h1><div class="sub">A small model guesses, a big model checks. Why that makes LLM inference two to three times faster without changing a single output.</div>
<div class="au">{av(44)}<div>Priya Natarajan <span class="f">· Follow</span><small>11 min read · Oct 18, 2026</small></div></div>
<div class="bar"><span>👏 2.4K</span><span>💬 41</span><span style="margin-left:auto">🔖</span><span>↗</span><span>···</span></div>
<p>Generating text with a large language model is slow for a boring reason: every token needs a full pass through the model, and that pass is limited by memory bandwidth, not compute. The GPU spends most of its time moving weights, and the arithmetic units sit idle.</p>
<p>Speculative decoding attacks exactly that waste. A small <b>draft model</b> proposes several tokens cheaply. The large <b>target model</b> then scores all of them in a single forward pass, which costs about the same as scoring one. Every draft token the target agrees with is accepted; the first disagreement is replaced with the target's own choice, and the process repeats.</p>
<p>The trick is that the accept-or-reject rule is designed so the final text has exactly the distribution the big model would have produced on its own. You are not trading quality for speed, you are trading idle compute for speed.</p></div></div>"""
    return dict(theme="light", icon="medium", title="Speculative decoding, explained simply | by Priya Natarajan | Medium", host="medium.com", path="/@priyanat/speculative-decoding-explained-simply-7c1e2a", body=body, css=css)


def lillog():
    css = """.ll{height:100%;background:#fff;color:#333;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif}
.ll-h{max-width:1000px;margin:0 auto;padding:26px 0 10px;display:flex;align-items:baseline;gap:30px;border-bottom:1px solid #eee}.ll-h b{font-size:26px;font-weight:700}.ll-h span{color:#555;font-size:15px}
.ll-a{max-width:1000px;margin:0 auto;padding-top:30px;display:flex;gap:50px}
.ll-a h1{font-size:34px;font-weight:700;line-height:1.2;margin-bottom:8px}.ll-a .m{color:#777;font-size:14px;margin-bottom:26px}
.ll-a p{font-size:17px;line-height:1.75;margin-bottom:20px}.ll-a a{color:#0074d9}
.ll-t{width:300px;font-size:14px;line-height:1.9;color:#0074d9;border-left:2px solid #eee;padding-left:16px;margin-top:70px;flex:none}.ll-t b{color:#333;display:block;font-size:15px}
"""
    body = """<div class="ll"><div class="ll-h"><b>Lil'Log</b><span>Posts</span><span>Archive</span><span>Search</span><span>Tags</span><span>FAQ</span></div>
<div class="ll-a"><div><h1>Large Transformer Model Inference Optimization</h1><div class="m">Date: January 10, 2023 &nbsp;|&nbsp; Estimated Reading Time: 10 min &nbsp;|&nbsp; Author: Lilian Weng</div>
<p>Large transformer models are mainstream nowadays, creating SoTA results for a variety of tasks. They are powerful but very expensive to train and use. The extremely high inference cost, in both time and memory, is a big bottleneck for adopting a powerful transformer for solving real-world tasks at scale.</p>
<p><b>Why is it hard to run inference for large transformer models?</b> Besides the increasing size of SoTA models, there are two main factors contributing to the inference challenge: the large memory footprint (model parameters and intermediate states need to be kept in memory at inference time) and the low parallelizability of autoregressive decoding, since each token depends on the ones before it.</p>
<p>This post looks at several methods that make inference cheaper: distillation, quantization, pruning, sparsity and mixture-of-experts, as well as architecture changes that reduce the size of the KV cache.</p></div>
<div class="ll-t"><b>Table of contents</b>Methods Overview<br>Distillation<br>Quantization<br>&nbsp;&nbsp;Challenges for Transformer Quantization<br>&nbsp;&nbsp;Post-training quantization (PTQ)<br>&nbsp;&nbsp;Quantization-aware training (QAT)<br>Pruning<br>&nbsp;&nbsp;How to prune?<br>Sparsity<br>&nbsp;&nbsp;Mixture-of-Experts<br>Architectural Optimization<br>Citation<br>References</div></div></div>"""
    return dict(theme="light", icon="lillog", title="Large Transformer Model Inference Optimization | Lil'Log", host="lilianweng.github.io", path="/posts/2023-01-10-inference-optimization/", body=body, css=css)


def hn():
    items = [("Why your p99 latency is lying to you", "latencyfield.dev", 412, 188, "4 hours ago"),
             ("vLLM 0.9 adds disaggregated prefill and decode", "github.com/vllm-project", 265, 71, "6 hours ago"),
             ("Ask HN: How do you learn system design without a big-company job?", "", 331, 240, "7 hours ago"),
             ("Show HN: A simulator for request queues that shows where they break", "queue-sim.dev", 148, 39, "9 hours ago"),
             ("The KV cache is the new working set", "lmsys.org", 201, 64, "10 hours ago"),
             ("Speculative decoding in production: what actually worked", "fireworks.ai", 177, 52, "12 hours ago"),
             ("Consistent hashing, 28 years later", "akamai.com", 93, 21, "13 hours ago"),
             ("Claude Code hooks and headless mode (docs)", "docs.claude.com", 244, 119, "15 hours ago"),
             ("Codex CLI now runs tasks in parallel sandboxes", "openai.com", 203, 97, "16 hours ago"),
             ("Amdahl's law and the limits of faster coding", "ibm.com", 167, 141, "18 hours ago"),
             ("How Discord indexes trillions of messages", "discord.com", 389, 95, "20 hours ago")]
    css = """.hn{height:100%;background:#f6f6ef;font-family:Verdana,Geneva,sans-serif;font-size:13.5px;color:#000;padding:8px 0 0 0}
.hn-in{width:1550px;margin:0 auto}.hn-h{background:#ff6600;padding:3px 6px;display:flex;align-items:center;gap:10px}.hn-h .y{border:1px solid #fff;color:#fff;font-weight:700;padding:0 4px;font-size:12px}.hn-h b{font-weight:700}.hn-h span{color:#000}
.hn-r{display:flex;gap:6px;padding:5px 6px 0}.hn-r .n{width:28px;text-align:right;color:#828282}.hn-r .t a{color:#000}.hn-r .d{color:#828282;font-size:11px}.hn-r .s{color:#828282;font-size:11px;padding-left:34px;margin-bottom:4px}
"""
    rows = "".join(f'<div class="hn-r"><span class="n">{k + 1}.</span><span style="color:#828282">▲</span><span class="t">{t} <span class="d">({d})</span></span></div><div class="s">{p} points by {"mkarpov" if k % 2 else "jlee"} {ago} | hide | {c} comments</div>' for k, (t, d, p, c, ago) in enumerate(items))
    body = f"""<div class="hn"><div class="hn-in"><div class="hn-h"><span class="y">Y</span><b>Hacker News</b><span>new | past | comments | ask | show | jobs | submit</span><span style="margin-left:auto">abik (412) | logout</span></div>{rows}</div></div>"""
    return dict(theme="light", icon="hn", title="Why your p99 latency is lying to you | Hacker News", host="news.ycombinator.com", path="/item?id=42118834", body=body, css=css)


def huggingface():
    css = """.hf{height:100%;background:#fff;color:#111827;font-size:14px}
.hf-h{height:56px;display:flex;align-items:center;padding:0 24px;gap:22px;border-bottom:1px solid #e5e7eb}.hf-h .s{background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:7px 12px;width:280px;color:#6b7280}
.hf-h .n{display:flex;gap:18px;margin-left:auto;color:#374151}
.hf-m{padding:22px 40px}
.hf-m h1{font-size:22px;font-weight:600;display:flex;gap:8px;align-items:center}.hf-m h1 small{font-size:13px;color:#6b7280;font-weight:400}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 18px}.tags span{border:1px solid #e5e7eb;border-radius:6px;padding:3px 8px;font-size:12.5px;color:#374151;display:flex;gap:5px;align-items:center}
.hf-t{display:flex;gap:18px;border-bottom:1px solid #e5e7eb;font-size:14px}.hf-t span{padding:10px 4px}.hf-t .on{border-bottom:2px solid #111827;font-weight:600}
.hf-c{display:flex;gap:40px;margin-top:22px}.hf-c .l{flex:1;max-width:980px}.hf-c .l h2{font-size:20px;margin:0 0 10px}.hf-c .l p{line-height:1.6;color:#374151;margin-bottom:12px}
.hf-c .r{width:360px}.hf-c .r .b{border:1px solid #e5e7eb;border-radius:10px;padding:14px;margin-bottom:12px}.hf-c .r b{display:block;margin-bottom:6px}
.hf-c .r .btn{background:#111827;color:#fff;border-radius:8px;padding:9px 14px;text-align:center;font-weight:600}
.hf-c table{width:100%;border-collapse:collapse;font-size:13px}.hf-c td{padding:5px 0;border-top:1px solid #f3f4f6}
"""
    tags = "".join(f"<span>{t}</span>" for t in ["📝 Text Generation", "🤗 Transformers", "🔒 Safetensors", "🔥 PyTorch", "🌐 8 languages", "llama", "facebook", "meta", "llama-3", "conversational", "text-generation-inference", "📄 arxiv:2204.05149", "📜 License: llama3.1"])
    body = f"""<div class="hf"><div class="hf-h">{icon('hf', 30)}<span class="s">🔍 Search models, datasets, users...</span><span class="n"><span>Models</span><span>Datasets</span><span>Spaces</span><span>Docs</span><span>Pricing</span>{av(28)}</span></div>
<div class="hf-m"><h1>{icon('hf', 22)} meta-llama<span style="color:#9ca3af">/</span>Llama-3.1-8B-Instruct <small>♡ like 4.98k · ⤓ 6.1M downloads last month</small></h1>
<div class="tags">{tags}</div>
<div class="hf-t"><span class="on">📄 Model card</span><span>📁 Files and versions</span><span>💬 Community <span style="background:#f3f4f6;border-radius:8px;padding:0 6px">312</span></span><span style="margin-left:auto;background:#f3f4f6;border-radius:8px;padding:6px 12px;font-weight:500">⬢ Train ▾</span><span style="background:#f3f4f6;border-radius:8px;padding:6px 12px;font-weight:500">▶ Deploy ▾</span><span style="background:#111827;color:#fff;border-radius:8px;padding:6px 12px;font-weight:500">Use this model ▾</span></div>
<div class="hf-c"><div class="l"><h2>Model Information</h2><p>The Meta Llama 3.1 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction tuned generative models in 8B, 70B and 405B sizes (text in/text out). The Llama 3.1 instruction tuned text only models are optimized for multilingual dialogue use cases.</p>
<p><b>Model Architecture:</b> Llama 3.1 is an auto-regressive language model that uses an optimized transformer architecture. The tuned versions use supervised fine-tuning (SFT) and reinforcement learning with human feedback (RLHF) to align with human preferences for helpfulness and safety.</p>
<h2>How to use</h2><p>This repository contains two versions of Meta-Llama-3.1-8B-Instruct, for use with transformers and with the original llama codebase.</p></div>
<div class="r"><div class="btn">Use this model ▾</div><div class="b" style="margin-top:12px"><b>Model size</b>8.03B params · <b style="display:inline">Tensor type</b> BF16</div><div class="b"><b>Inference Providers</b><table><tr><td>Together AI</td><td style="text-align:right;color:#16a34a">● live</td></tr><tr><td>Fireworks</td><td style="text-align:right;color:#16a34a">● live</td></tr><tr><td>Groq</td><td style="text-align:right;color:#16a34a">● live</td></tr></table></div><div class="b"><b>Collections including this model</b>Llama 3.1 · 12 items</div></div></div></div></div>"""
    return dict(theme="dark", icon="hf", title="meta-llama/Llama-3.1-8B-Instruct · Hugging Face", host="huggingface.co", path="/meta-llama/Llama-3.1-8B-Instruct", body=body, css=css)


def colab():
    css = """.co{height:100%;background:#fff;color:#202124;font-size:14px;display:flex;flex-direction:column}
.co-h{height:52px;display:flex;align-items:center;padding:0 16px;gap:12px}.co-h .t{font-size:18px}.co-h .menu{display:flex;gap:16px;color:#5f6368;font-size:13.5px;margin-left:14px}.co-h .r{margin-left:auto;display:flex;gap:14px;align-items:center}
.co-h .cn{border:1px solid #dadce0;border-radius:4px;padding:5px 12px;color:#1a73e8;font-weight:500;font-size:13px}
.co-tb{height:40px;border-bottom:1px solid #e8eaed;display:flex;align-items:center;gap:14px;padding:0 16px;color:#5f6368;font-size:13px}.co-tb b{color:#1a73e8;font-weight:500}
.co-m{display:flex;flex:1}.co-s{width:54px;border-right:1px solid #e8eaed;padding-top:10px;display:flex;flex-direction:column;align-items:center;gap:22px;color:#5f6368;font-size:18px}
.co-c{flex:1;padding:14px 60px 0 30px}
.cell{display:flex;gap:10px;margin-bottom:12px}.cell .run{width:28px;height:28px;border-radius:50%;border:1.5px solid #5f6368;display:flex;align-items:center;justify-content:center;font-size:11px;color:#5f6368;flex:none;margin-top:6px}
.cell pre{flex:1;background:#f7f7f7;border-radius:4px;padding:10px 14px;font-size:13px;line-height:1.55;white-space:pre;border-left:3px solid #e8eaed}
.cell.on pre{border-left-color:#1a73e8}
.cell .out{flex:1;padding:4px 14px;font-size:13px;line-height:1.55;white-space:pre}
.k{color:#8e2eb3}.s{color:#188038}.c{color:#9aa0a6}.f{color:#1967d2}
"""
    body = f"""<div class="co"><div class="co-h">{icon('colab', 36)}<span class="t">inference_benchmark.ipynb ☆</span><span class="menu"><span>File</span><span>Edit</span><span>View</span><span>Insert</span><span>Runtime</span><span>Tools</span><span>Help</span></span><span class="r"><span style="color:#5f6368">All changes saved</span><span class="cn">Comment</span><span class="cn" style="background:#1a73e8;color:#fff;border-color:#1a73e8">Share</span>{av(30)}</span></div>
<div class="co-tb">+ Code &nbsp; + Text &nbsp;<span style="margin-left:auto">RAM ▮▮▮▯ Disk ▮▯▯▯ &nbsp; <b>● A100</b> ▾</span></div>
<div class="co-m"><div class="co-s"><span>≡</span><span>🔍</span><span>{{x}}</span><span>📁</span></div><div class="co-c">
<div class="cell"><span class="run">▶</span><pre><span class="c"># Compare batch sizes on one GPU: throughput vs time-to-first-token</span>
!pip -q install vllm==0.9.2 matplotlib
<span class="k">from</span> vllm <span class="k">import</span> LLM, SamplingParams
llm = LLM(<span class="s">"meta-llama/Llama-3.1-8B-Instruct"</span>, dtype=<span class="s">"bfloat16"</span>, gpu_memory_utilization=<span class="f">0.9</span>)</pre></div>
<div class="cell on"><span class="run">▶</span><pre><span class="k">import</span> time, matplotlib.pyplot <span class="k">as</span> plt
results = []
<span class="k">for</span> bs <span class="k">in</span> [<span class="f">1</span>, <span class="f">4</span>, <span class="f">8</span>, <span class="f">16</span>, <span class="f">32</span>, <span class="f">64</span>]:
    t0 = time.perf_counter()
    out = llm.generate(prompts[:bs], SamplingParams(max_tokens=<span class="f">256</span>))
    dt = time.perf_counter() - t0
    results.append((bs, bs*<span class="f">256</span>/dt, out[<span class="f">0</span>].metrics.first_token_time))
    print(<span class="s">f"bs={{bs:&gt;3}}  {{bs*256/dt:7.0f}} tok/s  ttft={{out[0].metrics.first_token_time*1e3:5.0f}} ms"</span>)</pre></div>
<div class="cell"><span class="run" style="border:0"></span><div class="out">bs=  1      71 tok/s  ttft=   38 ms
bs=  4     268 tok/s  ttft=   41 ms
bs=  8     512 tok/s  ttft=   46 ms
bs= 16     948 tok/s  ttft=   58 ms
bs= 32    1689 tok/s  ttft=   84 ms
bs= 64    2731 tok/s  ttft=  141 ms
<svg width="520" height="150" viewBox="0 0 520 150"><g stroke="#ddd"><line x1="50" y1="10" x2="50" y2="130"/><line x1="50" y1="130" x2="500" y2="130"/></g><polyline points="60,127 130,118 200,106 270,86 340,53 410,8" fill="none" stroke="#1a73e8" stroke-width="2.5"/>{"".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#1a73e8"/>' for x, y in [(60,127),(130,118),(200,106),(270,86),(340,53),(410,8)])}<text x="270" y="147" font-size="11" text-anchor="middle" fill="#5f6368">batch size</text><text x="12" y="70" font-size="11" fill="#5f6368">tok/s</text></svg></div></div>
</div></div></div>"""
    return dict(theme="light", icon="colab", title="inference_benchmark.ipynb - Colab", host="colab.research.google.com", path="/drive/1xK9vQ…", body=body, css=css)


def swagger():
    css = """.sw{height:100%;background:#fafafa;color:#3b4151;font-family:sans-serif}
.sw-h{background:#1b1b1b;height:60px;display:flex;align-items:center;padding:0 40px;gap:14px}.sw-h b{color:#fff;font-size:22px;display:flex;align-items:center;gap:8px}.sw-h .u{margin-left:auto;background:#fff;border-radius:4px;padding:8px 14px;width:520px;font-size:14px;color:#333}.sw-h .e{background:#4990e2;color:#fff;padding:9px 24px;border-radius:4px;font-weight:700}
.sw-m{max-width:1460px;margin:0 auto;padding:26px 0}
.sw-m h1{font-size:36px;font-weight:700;display:flex;align-items:center;gap:12px}.sw-m h1 small{background:#7d8492;color:#fff;font-size:14px;border-radius:14px;padding:4px 10px;font-weight:400}
.sw-m .l{color:#4990e2;font-size:14px;margin:6px 0 20px;display:block}
.sw-m h2{font-size:24px;font-weight:700;border-bottom:1px solid rgba(59,65,81,.3);padding-bottom:8px;margin:10px 0 14px;display:flex;align-items:center}.sw-m h2 small{font-size:14px;font-weight:400;color:#888;margin-left:12px}
.op{border-radius:4px;border:1px solid;display:flex;align-items:center;gap:12px;padding:8px 10px;margin-bottom:10px;font-size:15px}
.op b{color:#fff;border-radius:3px;padding:6px 0;width:80px;text-align:center;font-size:14px;font-weight:700}.op .p{font-family:monospace;font-weight:700;font-size:16px}.op .d{color:#3b4151;flex:1;font-size:13px}.op .lk{opacity:.5}
.post{background:rgba(73,204,144,.1);border-color:#49cc90}.post b{background:#49cc90}
.get{background:rgba(97,175,254,.1);border-color:#61affe}.get b{background:#61affe}
.del{background:rgba(249,62,62,.1);border-color:#f93e3e}.del b{background:#f93e3e}
"""
    ops = [("post", "/generate", "Generate tokens for one prompt (streams SSE when stream=true)"), ("post", "/batch", "Generate for up to 64 prompts in one request"),
           ("get", "/health", "Engine health and loaded model"), ("get", "/metrics", "Prometheus metrics: ttft, tokens/s, queue depth, kv-cache usage"),
           ("get", "/v1/models", "List models available on this engine"), ("del", "/cache", "Drop the prefix cache")]
    body = f"""<div class="sw"><div class="sw-h"><b>{icon('swagger', 30)} swagger</b><span class="u">http://localhost:8000/openapi.json</span><span class="e">Explore</span></div>
<div class="sw-m"><h1>Inference demo API <small>0.3.1</small> <small style="background:#89bf04">OAS 3.1</small></h1><span class="l">/openapi.json</span>
<p style="font-size:14px;margin-bottom:20px">A small FastAPI front for the vLLM engine used in the token-stream demo. Requests are batched every 8 ms; see /metrics for queue depth.</p>
<h2>generate <small>Text generation</small></h2>{"".join(f'<div class="op {m}"><b>{"DELETE" if m == "del" else m.upper()}</b><span class="p">{p}</span><span class="d">{d}</span><span class="lk">🔓</span><span>⌄</span></div>' for m, p, d in ops[:2])}
<h2>system <small>Health and observability</small></h2>{"".join(f'<div class="op {m}"><b>{"DELETE" if m == "del" else m.upper()}</b><span class="p">{p}</span><span class="d">{d}</span><span class="lk">🔓</span><span>⌄</span></div>' for m, p, d in ops[2:])}
</div></div>"""
    return dict(theme="light", icon="swagger", title="FastAPI - Swagger UI", host="localhost:8000", path="/docs", body=body, css=css)


def stackoverflow():
    css = """.so{height:100%;background:#fff;color:#232629;font-size:14px}
.so-h{height:50px;border-top:3px solid #f48024;border-bottom:1px solid #d6d9dc;display:flex;align-items:center;padding:0 24px;gap:18px;background:#f8f9f9}.so-h b{font-size:20px;display:flex;align-items:center;gap:6px;font-weight:400}.so-h b i{font-style:normal;font-weight:700}
.so-h .s{flex:1;border:1px solid #babfc4;border-radius:3px;padding:7px 10px;color:#838c95;max-width:700px}.so-h .n{color:#525960}
.so-m{display:flex;gap:30px;padding:24px 40px}
.so-q{flex:1}.so-q h1{font-size:27px;font-weight:400;margin-bottom:8px;line-height:1.3}.so-q .meta{color:#6a737c;font-size:13px;border-bottom:1px solid #e3e6e8;padding-bottom:10px;margin-bottom:16px}.so-q .meta b{color:#232629;font-weight:400}
.post{display:flex;gap:16px}.vote{width:40px;display:flex;flex-direction:column;align-items:center;gap:4px;color:#6a737c;font-size:21px}.vote b{font-size:21px;color:#232629;font-weight:400}
.pb{flex:1}.pb p{font-size:15px;line-height:1.5;margin-bottom:12px}.pb pre{background:#f6f6f6;border-radius:5px;padding:12px;font-size:13px;line-height:1.5;margin-bottom:14px;white-space:pre;overflow:hidden}
.tg{background:#e1ecf4;color:#39739d;border-radius:4px;padding:3px 7px;font-size:12px;margin-right:4px}
.ans{border-top:1px solid #e3e6e8;margin-top:20px;padding-top:16px}.ans h2{font-size:19px;font-weight:400;margin-bottom:14px}
.so-s{width:300px}.so-s .box{border:1px solid #f1e5bc;background:#fdf7e2;padding:12px;font-size:13px;border-radius:3px}.so-s .box b{display:block;margin-bottom:6px}
"""
    body = f"""<div class="so"><div class="so-h"><b>{icon('so', 28)} stack <i>overflow</i></b><span class="n">About</span><span class="n">Products</span><span class="s">🔍 Search…</span>{av(26)}<span class="n">🏆 1,284</span></div>
<div class="so-m"><div class="so-q"><h1>python - torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 GiB while serving Llama 3.1 8B</h1>
<div class="meta">Asked <b>2 days ago</b> &nbsp; Modified <b>today</b> &nbsp; Viewed <b>4k times</b></div>
<div class="post"><div class="vote">▲<b>37</b>▼<span style="font-size:18px">🔖</span></div><div class="pb"><p>I'm serving <code>meta-llama/Llama-3.1-8B-Instruct</code> on a single 24 GB GPU with a batch size of 16 and 4k context. The first few requests work, then after a few minutes:</p>
<pre class="mono">torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 GiB.
GPU 0 has a total capacity of 23.68 GiB of which 1.12 GiB is free.
Including non-PyTorch memory, this process has 22.55 GiB memory in use.
Of the allocated memory 19.80 GiB is allocated by PyTorch, and 1.91 GiB is reserved
but unallocated. If reserved but unallocated memory is large try setting
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True</pre>
<p>The weights are 16 GB in bf16, so I expected 8 GB headroom. Why does memory keep growing with the number of concurrent requests, and how do I size the batch properly?</p>
<span class="tg">python</span><span class="tg">pytorch</span><span class="tg">cuda</span><span class="tg">llm</span><span class="tg">vllm</span></div></div>
<div class="ans"><h2>2 Answers</h2><div class="post"><div class="vote">▲<b>52</b>▼<span style="color:#2e8b57;font-size:24px">✓</span></div><div class="pb"><p>The weights are the fixed cost; the <b>KV cache</b> is the variable one, and it is what grows with concurrency. For Llama 3.1 8B every token in flight costs about 128 KB of cache in bf16 (32 layers × 8 KV heads × 128 dims × 2 × 2 bytes). 16 requests × 4,096 tokens is 8 GB on its own, which is exactly your headroom, before activations and the allocator's fragmentation.</p><p>Either cap the total tokens in flight (vLLM: <code>--max-num-batched-tokens</code> and <code>--gpu-memory-utilization</code>), quantize the cache to fp8, or move to paged attention so blocks are allocated as tokens arrive instead of reserved up front.</p></div></div></div></div>
<div class="so-s"><div class="box"><b>The Overflow Blog</b>Why inference, not training, is where most GPU hours go now</div><div class="box" style="background:#fff;border-color:#e3e6e8;margin-top:12px"><b>Related</b><span style="color:#0074cc">CUDA out of memory with a small batch size</span><br><span style="color:#0074cc">How is the KV cache size computed?</span><br><span style="color:#0074cc">vLLM: what does gpu_memory_utilization mean</span></div></div></div></div>"""
    return dict(theme="light", icon="so", title="python - torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 GiB while serving Llama 3.1 8B - Stack Overflow", host="stackoverflow.com", path="/questions/79318842/", body=body, css=css)


def fanout():
    css = """.fo{height:100%;background:#0a0a0a;color:#f2f0ea;display:flex;flex-direction:column}
.fo-h{height:64px;display:flex;align-items:center;padding:0 48px;gap:34px;font-size:15px;color:#c9c5bb}.fo-h b{color:#fff;font-size:19px;font-weight:600;display:flex;align-items:center;gap:10px}.fo-h .r{margin-left:auto;display:flex;gap:20px;align-items:center}.fo-h .r i{font-style:normal;background:#f2f0ea;color:#0a0a0a;padding:8px 16px;border-radius:8px;font-weight:600}
.fo-m{flex:1;display:flex;padding:30px 48px 0}
.fo-l{width:520px}.fo-l h1{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:54px;font-weight:400;line-height:1.05;letter-spacing:-.5px}.fo-l h1 b{font-style:normal;font-weight:400}
.fo-l p{color:#b4b0a6;font-size:17px;line-height:1.55;margin-top:18px;max-width:440px}
.fo-l .cta{margin-top:26px;display:flex;gap:12px}.fo-l .cta span{border-radius:8px;padding:11px 18px;font-weight:600;font-size:14px;border:1px solid #333}.fo-l .cta .p{background:#f2f0ea;color:#0a0a0a;border-color:#f2f0ea}
.fo-l .st{margin-top:40px;color:#8d897f;font-size:13px;line-height:1.9}
.fo-map{flex:1;position:relative}
.node{position:absolute;border:1px solid #2c2c2c;background:#121212;border-radius:10px;padding:10px 14px;font-size:14px;min-width:150px}.node small{display:block;color:#8d897f;font-size:12px;margin-top:3px}.node.on{border-color:#f2f0ea}.node.free:after{content:"free";position:absolute;right:10px;top:9px;color:#8fd19e;font-size:11px}
"""
    nodes = [(40, 300, "Start here", "the first branch", "on free"), (300, 90, "Research", "papers, a paper at a time", ""), (300, 230, "System design", "queues, caches, consistency", "on"),
             (300, 370, "The math", "attention, scaling, numerics", ""), (300, 510, "Inference", "KV cache, batching, serving", ""),
             (580, 170, "Consistent hashing", "", ""), (580, 250, "Load shedding", "lab · watch it break at 18k", "on"), (580, 330, "CAP in practice", "", ""),
             (580, 470, "Paged attention", "", ""), (580, 550, "Speculative decoding", "", "")]
    nh = "".join(f'<div class="node {c}" style="left:{x}px;top:{y}px">{t}<small>{s}</small></div>' for x, y, t, s, c in nodes)
    lines = "".join(f'<path d="M{x1} {y1} C {x1+120} {y1}, {x2-120} {y2}, {x2} {y2}" fill="none" stroke="#333" stroke-width="1.5"/>' for x1, y1, x2, y2 in [(200, 325, 300, 115), (200, 325, 300, 255), (200, 325, 300, 395), (200, 325, 300, 535), (470, 255, 580, 195), (470, 255, 580, 275), (470, 255, 580, 355), (470, 535, 580, 495), (470, 535, 580, 575)])
    body = f"""<div class="fo"><div class="fo-h"><b>{icon('fanout', 26)} fanout</b><span style="color:#fff">Roadmap</span><span>Labs</span><span>Papers</span><span>Archive</span><span class="r"><span>Log in</span><i>Start the first branch</i></span></div>
<div class="fo-m"><div class="fo-l"><h1>Everything an OpenAI L7 knows. <b>Mapped.</b></h1><p>Research, system design, the math underneath, inference. In the order a senior engineer learned it, with labs where you watch systems break.</p><div class="cta"><span class="p">Start the first branch</span><span>See the map</span></div><div class="st">20,000+ engineers reading it this way<br>Maintained every week as the field moves<br>Read by people at Amazon · Stanford · IIT Bombay</div></div>
<div class="fo-map"><svg width="900" height="640" style="position:absolute;left:0;top:0">{lines}</svg>{nh}</div></div></div>"""
    return dict(theme="dark", icon="fanout", title="Roadmap — fanout", host="fanout.sh", path="/roadmap", body=body, css=css)


def gdocs():
    css = """.gd{height:100%;background:#f9fbfd;color:#1f1f1f;display:flex;flex-direction:column;font-size:14px}
.gd-h{height:64px;display:flex;align-items:center;padding:0 16px;gap:12px}.gd-h .t{font-size:18px}.gd-h .menu{display:flex;gap:14px;color:#444;font-size:14px;margin-left:10px}.gd-h .r{margin-left:auto;display:flex;align-items:center;gap:14px}.gd-h .sh{background:#c2e7ff;border-radius:20px;padding:9px 18px;font-weight:500}
.gd-tb{height:40px;background:#edf2fa;border-radius:24px;margin:0 16px 10px;display:flex;align-items:center;padding:0 16px;gap:16px;color:#444;font-size:13.5px}.gd-tb span.b{border-left:1px solid #c7c7c7;height:20px}
.gd-p{flex:1;display:flex;justify-content:center;overflow:hidden}.gd-pg{width:816px;background:#fff;border:1px solid #e0e0e0;padding:60px 72px;font-family:Arial,sans-serif;font-size:11pt;line-height:1.5}
.gd-pg h1{font-size:20pt;font-weight:400;margin-bottom:12pt;font-family:Arial}.gd-pg h2{font-size:16pt;font-weight:400;color:#434343;margin:14pt 0 6pt}.gd-pg li{margin-left:28px;margin-bottom:3pt}.gd-pg p{margin-bottom:8pt}
.gd-ol{width:190px;padding:10px 16px;font-size:13px;color:#444;line-height:2}.gd-ol b{display:block;color:#1f1f1f}
"""
    body = f"""<div class="gd"><div class="gd-h">{icon('gdocs', 40)}<div><div class="t">System design notes</div><div class="menu"><span>File</span><span>Edit</span><span>View</span><span>Insert</span><span>Format</span><span>Tools</span><span>Extensions</span><span>Help</span></div></div><span class="r"><span style="color:#444">🕓</span><span style="color:#444">💬</span><span class="sh">🔒 Share ▾</span>{av(32)}</span></div>
<div class="gd-tb"><span>↶ ↷ 🖨 ✎</span><span class="b"></span><span>100% ▾</span><span class="b"></span><span>Normal text ▾</span><span class="b"></span><span>Arial ▾</span><span class="b"></span><span>− 11 +</span><span class="b"></span><span><b>B</b> <i>I</i> <u>U</u> A</span><span class="b"></span><span>≡ ≡ ≡</span></div>
<div class="gd-p"><div class="gd-ol"><b>Outline</b>1. Load balancing<br>2. Caching<br>3. Queues<br>4. CAP in practice<br>5. Inference serving<br>6. Questions for Thursday</div><div class="gd-pg"><h1>System design notes</h1><p><i>Week 3 · what a senior engineer actually checks first</i></p>
<h2>1. Load balancing</h2><ul><li>Round robin vs least-connections: least-connections wins once request cost varies (LLM calls vary a lot).</li><li>Consistent hashing keeps a prefix cache warm on the same worker. Virtual nodes smooth the ring.</li><li>Health checks must be cheaper than the request they protect.</li></ul>
<h2>2. Caching</h2><ul><li>Cache the thing that is expensive to compute, not the thing that is easy to store.</li><li>KV cache is a cache too: paged allocation, eviction by LRU on blocks, prefix sharing.</li></ul>
<h2>3. Queues</h2><ul><li>A queue does not add capacity. Once arrival rate &gt; service rate, depth grows without bound (the 18k rps lab).</li><li>Shed load early at the gateway; a 503 in 5 ms beats a 200 in 9 s.</li></ul>
<h2>4. CAP in practice</h2><ul><li>Partition tolerance is not optional, so the real choice is C vs A during a partition.</li></ul></div></div></div>"""
    return dict(theme="light", icon="gdocs", title="System design notes - Google Docs", host="docs.google.com", path="/document/d/1rQ8…/edit", body=body, css=css)


def excalidraw():
    css = """.ex{height:100%;background:#fff;position:relative;overflow:hidden;color:#1e1e1e}
.ex-tb{position:absolute;left:50%;top:14px;transform:translateX(-50%);background:#fff;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.12);display:flex;gap:6px;padding:6px}.ex-tb span{width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;color:#333}.ex-tb span.on{background:#e0dfff}
.ex-m{position:absolute;left:14px;top:14px;background:#fff;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.12);width:44px;height:44px;display:flex;align-items:center;justify-content:center;font-size:18px}
.ex-r{position:absolute;right:14px;top:14px;display:flex;gap:10px}.ex-r span{background:#a8a5ff;color:#fff;border-radius:10px;padding:12px 16px;font-weight:600;font-size:14px}.ex-r span.l{background:#ececec;color:#333}
.ex-z{position:absolute;left:14px;bottom:14px;background:#ececec;border-radius:10px;padding:10px 14px;font-size:14px}
"""
    def box(x, y, w, h, t, c="#1e1e1e", bg="transparent"):
        return f'<path d="M{x} {y} q{w/2} -2 {w} 0 q2 {h/2} 0 {h} q-{w/2} 2 -{w} 0 q-2 -{h/2} 0 -{h}" fill="{bg}" stroke="{c}" stroke-width="2"/><text x="{x+w/2}" y="{y+h/2+7}" text-anchor="middle" font-family="Chalkboard SE" font-size="20" fill="{c}">{t}</text>'
    def arrow(x1, y1, x2, y2, c="#1e1e1e", lbl=""):
        return f'<path d="M{x1} {y1} Q{(x1+x2)/2} {(y1+y2)/2 - 6} {x2} {y2}" fill="none" stroke="{c}" stroke-width="2"/><path d="M{x2} {y2} l-14 -7 M{x2} {y2} l-13 8" fill="none" stroke="{c}" stroke-width="2"/>' + (f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 12}" text-anchor="middle" font-family="Chalkboard SE" font-size="15" fill="{c}">{lbl}</text>' if lbl else "")
    svg = f"""<svg width="1700" height="790" style="position:absolute;inset:0" viewBox="0 0 1700 790">
<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#e5e5e5"/></pattern></defs><rect width="1700" height="790" fill="url(#g)"/>
<text x="380" y="130" font-family="Chalkboard SE" font-size="34" fill="#1e1e1e">inference topology — one GPU box</text>
{box(300, 320, 170, 80, "clients", "#1e1e1e")}{arrow(470, 360, 560, 360, lbl="18k rps")}
{box(560, 300, 190, 120, "gateway", "#e03131", "#ffe3e3")}<text x="655" y="395" text-anchor="middle" font-family="Chalkboard SE" font-size="14" fill="#e03131">shed above depth 400</text>
{arrow(750, 360, 850, 360)}{box(850, 320, 180, 80, "queue", "#f08c00", "#fff4e6")}{arrow(1030, 360, 1130, 300)}{arrow(1030, 360, 1130, 420)}
{box(1130, 240, 200, 70, "batcher · 8 ms", "#1971c2", "#e7f5ff")}{box(1130, 400, 200, 70, "batcher · 8 ms", "#1971c2", "#e7f5ff")}
{arrow(1330, 275, 1420, 275)}{arrow(1330, 435, 1420, 435)}{box(1420, 220, 200, 110, "GPU 0 · engine", "#2f9e44", "#ebfbee")}{box(1420, 380, 200, 110, "GPU 1 · engine", "#2f9e44", "#ebfbee")}
{box(1420, 560, 200, 70, "KV cache · paged", "#6741d9", "#f3f0ff")}<path d="M1520 490 L1520 560" stroke="#6741d9" stroke-width="2" stroke-dasharray="6 5"/>
<text x="860" y="470" font-family="Chalkboard SE" font-size="15" fill="#f08c00">depth grows without bound once arrivals &gt; service</text>
<text x="330" y="620" font-family="Chalkboard SE" font-size="18" fill="#868e96">TODO: where does p99 come from? → the queue, not the model</text></svg>"""
    body = f"""<div class="ex">{svg}<div class="ex-m">☰</div><div class="ex-tb"><span>🔒</span><span>✋</span><span class="on">↖</span><span>▭</span><span>◇</span><span>○</span><span>→</span><span>—</span><span>✎</span><span>A</span><span>🖼</span><span>⌫</span></div><div class="ex-r"><span class="l">Library</span><span>Share</span></div><div class="ex-z">− &nbsp;100% &nbsp;+</div></div>"""
    return dict(theme="light", icon="excalidraw", title="inference topology — Excalidraw", host="excalidraw.com", path="/#room=a8f2…", body=body, css=css)


def claude_chat():
    css = """.cc{height:100%;background:#f5f3ee;color:#2b2a27;display:flex}
.cc-s{width:270px;background:#ece9e2;padding:18px 14px;font-size:14px}.cc-s .lg{font-weight:600;font-size:18px;display:flex;align-items:center;gap:8px;margin-bottom:18px}.cc-s .nw{background:#d97757;color:#fff;border-radius:10px;padding:9px 12px;font-weight:600;margin-bottom:18px}
.cc-s .h{color:#7a7772;font-size:12px;margin:10px 0 6px}.cc-s div.i{padding:7px 10px;border-radius:8px;white-space:nowrap;overflow:hidden;color:#3d3b37}.cc-s div.on{background:#e0dcd3}
.cc-m{flex:1;display:flex;flex-direction:column;align-items:center;padding:30px 0 0}
.cc-c{width:780px}
.u{background:#e8e4da;border-radius:16px;padding:14px 18px;font-size:16px;margin-left:200px;margin-bottom:26px}
.a{font-size:16px;line-height:1.65}.a p{margin-bottom:14px}.a li{margin:0 0 8px 22px}.a code{background:#eae6dd;border-radius:4px;padding:1px 5px;font-size:14px}
.cc-in{width:780px;margin-top:auto;margin-bottom:22px;background:#fff;border:1px solid #d9d5cc;border-radius:16px;padding:16px 18px;color:#8a877f;font-size:15px;display:flex;align-items:center}.cc-in b{margin-left:auto;background:#d97757;color:#fff;border-radius:8px;width:30px;height:30px;display:flex;align-items:center;justify-content:center}
"""
    body = f"""<div class="cc"><div class="cc-s"><div class="lg">{icon('claude', 24)} Claude</div><div class="nw">+ New chat</div><div class="h">Recents</div><div class="i on">Explain tensor parallelism like I'm new…</div><div class="i">KV cache size for Llama 3.1 8B</div><div class="i">Review serve.py batching loop</div><div class="i">Consistent hashing vs rendezvous</div><div class="i">What breaks first at 18k rps</div><div class="i">CAP theorem in one paragraph</div></div>
<div class="cc-m"><div class="cc-c"><div class="u">Explain tensor parallelism like I'm new to GPUs</div>
<div class="a"><p>Think of one layer of the model as a big multiplication: your input vector times a huge weight matrix. When the matrix is too big for one GPU, or you want the answer faster, you <b>cut the matrix into slices</b> and give each GPU a slice.</p>
<ul><li><b>Each GPU multiplies the same input by its slice.</b> Four GPUs, four slices, four partial answers, all at the same time.</li><li><b>Then they combine.</b> An <code>all-reduce</code> adds the partial answers together so every GPU ends up with the full result before the next layer.</li><li><b>The cost is the talking.</b> Every layer needs that exchange, so tensor parallelism only pays off when the GPUs are connected by something fast like NVLink inside one box.</li></ul>
<p>That is the whole idea: split the <i>weights</i> within a layer, not the batch. Pipeline parallelism, by contrast, gives each GPU whole layers and passes activations down a line.</p><p>Want me to show the same thing with the attention heads, where the split is even more natural?</p></div></div>
<div class="cc-in">Reply to Claude…<b>↑</b></div></div></div>"""
    return dict(theme="light", icon="claude", title="Explain tensor parallelism like I'm new to GPUs - Claude", host="claude.ai", path="/chat/7f3a9c2e", body=body, css=css)


def vscode():
    css = """.vs{height:100%;background:#1e1e1e;color:#d4d4d4;display:flex;flex-direction:column;font-size:13px}
.vs-t{height:34px;background:#323233;display:flex;align-items:center;padding:0 12px;gap:14px;color:#ccc;font-size:12.5px}.vs-t .s{margin-left:auto;margin-right:auto;background:#252526;border:1px solid #444;border-radius:6px;width:520px;text-align:center;padding:3px 0;color:#999}
.vs-b{flex:1;display:flex}.vs-ab{width:48px;background:#333;display:flex;flex-direction:column;align-items:center;padding-top:10px;gap:22px;font-size:20px;color:#858585}.vs-ab span.on{color:#fff;border-left:2px solid #fff;padding-left:12px;margin-left:-14px}
.vs-ex{width:240px;background:#252526;padding:8px 0;color:#ccc}.vs-ex .h{font-size:11px;font-weight:700;padding:4px 20px;color:#bbb}.vs-ex div.f{padding:3px 0 3px 36px;white-space:nowrap}.vs-ex div.d{padding:3px 0 3px 20px;font-weight:600}.vs-ex div.on{background:#37373d}
.vs-e{flex:1;display:flex;flex-direction:column}.vs-tabs{height:35px;background:#252526;display:flex}.vs-tabs span{padding:0 14px;display:flex;align-items:center;gap:6px;color:#999;border-right:1px solid #1e1e1e}.vs-tabs span.on{background:#1e1e1e;color:#fff;border-top:1px solid #0078d4}
.vs-bc{height:22px;padding:0 16px;display:flex;align-items:center;color:#999;font-size:12px}
.vs-code{flex:1;display:flex;font-size:13.5px;line-height:19px;white-space:pre;padding-top:6px}.vs-code .ln{width:56px;text-align:right;padding-right:22px;color:#6e7681}.vs-code .ln span{display:block}
.k{color:#c586c0}.d{color:#569cd6}.fn{color:#dcdcaa}.s{color:#ce9178}.c{color:#6a9955}.n{color:#b5cea8}.t{color:#4ec9b0}.v{color:#9cdcfe}
.vs-term{height:170px;border-top:1px solid #3c3c3c;padding:6px 16px;white-space:pre;line-height:19px;font-size:12.5px}.vs-term .h{color:#999;display:flex;gap:18px;margin-bottom:4px}.vs-term .h b{color:#fff;border-bottom:1px solid #fff;font-weight:400}
.vs-st{height:22px;background:#0078d4;display:flex;align-items:center;padding:0 12px;gap:16px;font-size:12px;color:#fff}
"""
    code = """<span class="k">from</span> fastapi <span class="k">import</span> FastAPI, Request
<span class="k">from</span> fastapi.responses <span class="k">import</span> StreamingResponse
<span class="k">from</span> engine <span class="k">import</span> Engine, Batcher

app = <span class="fn">FastAPI</span>(title=<span class="s">"Inference demo API"</span>, version=<span class="s">"0.3.1"</span>)
engine = <span class="fn">Engine</span>(<span class="s">"meta-llama/Llama-3.1-8B-Instruct"</span>, dtype=<span class="s">"fp8"</span>)
batcher = <span class="fn">Batcher</span>(engine, window_ms=<span class="n">8</span>, max_batch=<span class="n">16</span>)
SHED_DEPTH = <span class="n">400</span>


<span class="d">@app.post</span>(<span class="s">"/generate"</span>)
<span class="k">async def</span> <span class="fn">generate</span>(req: Request):
    body = <span class="k">await</span> req.<span class="fn">json</span>()
    <span class="k">if</span> batcher.<span class="fn">depth</span>() &gt; SHED_DEPTH:            <span class="c"># protect p99 for everyone else</span>
        <span class="k">return</span> <span class="fn">JSONResponse</span>({<span class="s">"error"</span>: <span class="s">"overloaded"</span>}, status_code=<span class="n">503</span>,
                            headers={<span class="s">"Retry-After"</span>: <span class="s">"1"</span>})

    <span class="k">async def</span> <span class="fn">stream</span>():
        <span class="k">async for</span> tok <span class="k">in</span> batcher.<span class="fn">submit</span>(body[<span class="s">"prompt"</span>], body.<span class="fn">get</span>(<span class="s">"max_tokens"</span>, <span class="n">256</span>)):
            <span class="k">yield</span> <span class="s">f"data: </span>{tok.<span class="fn">json</span>()}<span class="s">\\n\\n"</span>
        <span class="k">yield</span> <span class="s">"data: [DONE]\\n\\n"</span>

    <span class="k">return</span> <span class="fn">StreamingResponse</span>(<span class="fn">stream</span>(), media_type=<span class="s">"text/event-stream"</span>)


<span class="d">@app.get</span>(<span class="s">"/metrics"</span>)
<span class="k">def</span> <span class="fn">metrics</span>():
    <span class="k">return</span> {<span class="s">"queue_depth"</span>: batcher.<span class="fn">depth</span>(), <span class="s">"kv_blocks_used"</span>: engine.<span class="fn">kv_usage</span>(),
            <span class="s">"ttft_p50_ms"</span>: batcher.stats.<span class="fn">p50</span>(), <span class="s">"ttft_p99_ms"</span>: batcher.stats.<span class="fn">p99</span>()}"""
    n = code.count("\n") + 1
    lns = "".join(f"<span>{i}</span>" for i in range(1, n + 1))
    body = f"""<div class="vs"><div class="vs-t"><span>⋮⋮</span><span>File  Edit  Selection  View  Go  Run  Terminal  Help</span><span class="s">🔍 inference-demo</span><span>⧉</span></div>
<div class="vs-b"><div class="vs-ab"><span class="on">⧉</span><span>🔍</span><span>⑂</span><span>▷</span><span>⊞</span></div>
<div class="vs-ex"><div class="h">EXPLORER</div><div class="d">▾ INFERENCE-DEMO</div><div class="d" style="padding-left:28px">▾ server</div><div class="f">🐍 engine.py</div><div class="f">🐍 batcher.py</div><div class="f on">🐍 serve.py</div><div class="d" style="padding-left:28px">▸ tests</div><div class="d" style="padding-left:28px">▸ web</div><div class="f" style="padding-left:28px">⚙ .env</div><div class="f" style="padding-left:28px">📄 README.md</div><div class="f" style="padding-left:28px">📦 requirements.txt</div></div>
<div class="vs-e"><div class="vs-tabs"><span>🐍 batcher.py</span><span class="on">🐍 serve.py ●</span><span>🐍 engine.py</span></div><div class="vs-bc">server &rsaquo; 🐍 serve.py &rsaquo; ⨍ generate</div>
<div class="vs-code mono"><div class="ln">{lns}</div><div>{code}</div></div>
<div class="vs-term mono"><div class="h"><span>PROBLEMS</span><span>OUTPUT</span><b>TERMINAL</b><span>PORTS</span></div><span style="color:#4ec9b0">abik@mbp</span> inference-demo % uvicorn server.serve:app --port 8000 --reload
<span style="color:#4ec9b0">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color:#4ec9b0">INFO</span>:     Loaded meta-llama/Llama-3.1-8B-Instruct in 11.4s · fp8 · 1×H100
<span style="color:#4ec9b0">INFO</span>:     127.0.0.1:52231 - "POST /generate HTTP/1.1" 200 OK   ttft=84ms  tok/s=61
<span style="color:#4ec9b0">INFO</span>:     127.0.0.1:52240 - "GET /metrics HTTP/1.1" 200 OK</div></div></div>
<div class="vs-st"><span>⑂ main*</span><span>⊗ 0 ⚠ 0</span><span style="margin-left:auto">Ln 15, Col 42</span><span>Spaces: 4</span><span>UTF-8</span><span>Python 3.12.4</span></div></div>"""
    return dict(theme="dark", icon="vscode", title="serve.py — inference-demo — Visual Studio Code", host="vscode.dev", path="/github/abik/inference-demo", body=body, css=css)


# ------------------------------------------------------------------ the YouTube four

def yt1():
    side = [("Consistent Hashing explained in 10 minutes", "ByteByteGo", "10:14", "#1d2b53", "#3b6fd6"), ("Load balancers: round robin vs least connections", "ByteByteGo", "8:51", "#3a1d53", "#9b4fd6"),
            ("How a CDN actually works", "ByteByteGo", "7:33", "#1d4f53", "#4fc5d6"), ("Rate limiting: token bucket vs sliding window", "ByteByteGo", "9:02", "#532f1d", "#d6864f"),
            ("Designing a URL shortener from scratch", "ByteByteGo", "15:40", "#1d532c", "#4fd68a"), ("Why your p99 latency is lying to you", "latencyfield", "12:08", "#53201d", "#d64f4f")]
    return dict(theme="dark", icon="youtube", title="Consistent Hashing explained in 10 minutes - YouTube", host="youtube.com", path="/watch?v=UF9Iqmg94tk", css=YT_CSS,
                body=yt_page("Consistent Hashing explained in 10 minutes (System Design)", "ByteByteGo", "1.2M", 191, 614, "Virtual nodes", yt_thumb("Consistent Hashing", "why adding a server moves only 1/N keys", "#4f9cff", "ring"), side))


def yt2():
    side = [("KV cache explained: why LLM inference eats your GPU memory", "Umar Jamil", "24:10", "#1d2b53", "#3b6fd6"), ("Attention is all you need, paper walkthrough", "Umar Jamil", "58:04", "#3a1d53", "#9b4fd6"),
            ("Paged attention and vLLM in 12 minutes", "Umar Jamil", "12:36", "#1d4f53", "#4fc5d6"), ("Quantization: int8, fp8 and what you lose", "Umar Jamil", "31:22", "#532f1d", "#d6864f"),
            ("Speculative decoding from scratch", "Umar Jamil", "27:45", "#1d532c", "#4fd68a"), ("Batching strategies for serving", "Umar Jamil", "19:17", "#53201d", "#d64f4f")]
    return dict(theme="dark", icon="youtube", title="KV cache explained: why LLM inference eats your GPU memory - YouTube", host="youtube.com", path="/watch?v=80bIUggRJf4", css=YT_CSS,
                body=yt_page("KV cache explained: why LLM inference eats your GPU memory", "Umar Jamil", "412K", 437, 1450, "Memory per token", yt_thumb("KV Cache", "128 KB per token · 32 layers · 8 KV heads", "#9ad0ff", "kv"), side, chips=("All", "From {ch}", "Large language models")))


def yt3():
    side = [("How a chat app scales to trillions of messages", "InfoQ", "41:02", "#1d2b53", "#3b6fd6"), ("Sharding: when, how and what breaks", "InfoQ", "35:18", "#3a1d53", "#9b4fd6"),
            ("Cassandra vs ScyllaDB at scale", "InfoQ", "48:50", "#1d4f53", "#4fc5d6"), ("Fan-out on write vs fan-out on read", "Gaurav Sen", "14:02", "#532f1d", "#d6864f"),
            ("Designing WhatsApp (system design)", "Gaurav Sen", "26:31", "#1d532c", "#4fd68a"), ("Hot partitions and how to avoid them", "InfoQ", "22:09", "#53201d", "#d64f4f")]
    return dict(theme="dark", icon="youtube", title="How a chat app scales to trillions of messages - YouTube", host="youtube.com", path="/watch?v=2sZ3V7pLXNU", css=YT_CSS,
                body=yt_page("How a chat app scales to trillions of messages (QCon talk)", "InfoQ", "392K", 1024, 2462, "Hot partitions", yt_thumb("Trillions of messages", "shards, hot partitions and the read path", "#6be67c", "msgs"), side, chips=("All", "From {ch}", "System design")))


def yt4():
    side = [("Designing a rate limiter (system design interview)", "Exponent", "18:44", "#1d2b53", "#3b6fd6"), ("Token bucket vs leaky bucket", "Exponent", "9:20", "#3a1d53", "#9b4fd6"),
            ("Distributed rate limiting with Redis", "Exponent", "16:05", "#1d4f53", "#4fc5d6"), ("Load shedding vs rate limiting: not the same thing", "latencyfield", "11:12", "#532f1d", "#d6864f"),
            ("Backpressure in async systems", "Exponent", "21:40", "#1d532c", "#4fd68a"), ("Mock interview: design an API gateway", "Exponent", "44:16", "#53201d", "#d64f4f")]
    return dict(theme="dark", icon="youtube", title="Designing a rate limiter (system design interview) - YouTube", host="youtube.com", path="/watch?v=mhUQe4BKZXs", css=YT_CSS,
                body=yt_page("Designing a rate limiter (system design interview)", "Exponent", "540K", 356, 1124, "Token bucket", yt_thumb("Rate Limiter", "token bucket · sliding window · where to put it", "#ffd34f", "bucket"), side, chips=("All", "From {ch}", "Interviews")))


SPECS = [
    yt1(), arxiv(), github_repo(), claude_docs(), term_claude(),
    yt2(), wikipedia(), localhost_demo(), codex_openai(), medium(),
    yt3(), lillog(), hn(), term_codex(), huggingface(),
    colab(), swagger(), stackoverflow(), fanout(), github_pr(),
    yt4(), gdocs(), excalidraw(), claude_chat(), vscode(),
]
