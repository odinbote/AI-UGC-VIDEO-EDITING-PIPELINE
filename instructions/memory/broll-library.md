---
name: broll-library
description: Where the movie/TV/stock b-roll library, its shot catalogue, theme index and used-shots ledger live; how to pick and add shots
metadata:
  type: reference
---

`/Users/abiknewar/Work/Claude Editing 2/B-roll library/` (local only, excluded from git; never publish, the clips are copyrighted):
- `movies/` — 12 clips downloaded 2026-11-12 with Abik's go-ahead ("yes download and also keep it for later"): Mr Robot hacking compilation, Hackers (1995), Halt and Catch Fire, The Imitation Game, Good Will Hunting, A Beautiful Mind, The Internship, Snowden, Blackhat, WarGames, two Silicon Valley scenes. Video only.
- Abik's own two files stay in `~/Downloads` (Silicon Valley compilation `sv`, Social Network clip `sn`), plus his Artlist stock there.
- `catalog/<key>_shots.json` + `<key>_pN.jpg` — every shot with in/out seconds and a thumbnail sheet (about 1,750 shots in all).
- `README.md` — per-source notes (letterbox, watermarks, subtitles, scale needed) and **shot picks by theme**: code on screen, hands typing, engineer at a desk, team stuck at screens, open office, servers and hardware, whiteboards, equations, interview/being tested, success.
- `used.json` — shots each reel has used. Read before picking, append after cutting. Abik's rule: a shot used in one video must not appear in another.
- Add a source: download, then `python3 tools/catalog_shots.py <video> <key> "B-roll library/catalog"`, view the sheets, add picks to the README.

yt-dlp is installed (`/Library/Frameworks/Python.framework/Versions/3.14/bin/yt-dlp`); video-only format `bv*[height<=1080][vcodec^=avc1]` needs no ffmpeg merge. Ask before downloading anything new (list titles, source, size).

See [[abik-edits-reel-6-7-broll-style]], [[ask-title-style-every-video]].
