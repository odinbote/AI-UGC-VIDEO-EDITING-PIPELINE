---
name: tab-windows-overlays
description: "\"Tab windows\" b-roll asset: 25 full Chrome/Terminal windows cut out on transparency (approved 2026-10-30); what \"tabs without background\" means to Abik and where the generator lives"
metadata:
  node_type: memory
  type: project
  originSessionId: 12e16190-fb11-4583-9ff8-f1b26ac30b3c
  modified: 2026-10-30T12:16:20.262Z
---

On 2026-10-30 Abik asked for "25 chrome tabs and mac tabs, without background". After a first round of small tab chips, they clarified with a reference image: they want **full browser windows** (macOS Chrome: tab strip, address bar, page) cut out on transparency, no desktop, no shadow, no mockup. Approved "Looks good".

**Why:** the windows are b-roll for the "400 tabs / scattered" beat in the fanout scripts (Out of order, Mapped). They need to read as real sites about system design, inference engineering, Claude Code, Codex.

**How to apply:**
- "Tabs without background" = window cutouts, not chips. Chrome windows for everything; Terminal windows only for CLI tools (Claude Code, Codex).
- Generator: `tools/render_tab_windows.py` (Playwright, 1700x880 at 2x, `omit_background`), pages in `tools/tabwin/pages.py`, frame in `tools/tabwin/frame.py`, hand-drawn favicons in `tools/tabwin/icons.py`. Output in `Tab windows/` with README and `_contact_sheet.png`. Older chips in `Tab overlays/` (`tools/render_tabs.py`).
- Favicons/logos are drawn approximations, nothing downloaded. Real pages (arXiv PagedAttention, Lil'Log, system-design-primer, Llama 3.1 card) use my own wording.

See [[hard-rules-no-slop]], [[fanout-reel-editing-system]].
