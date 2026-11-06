# Tab overlays (25)

Single tab chips on transparency. No window, no toolbar, no mockup: the only
opaque pixels are the tab itself. Rendered at 4x (1 CSS px = 4 px), so a Chrome
tab is ~1000 px wide and 152 px tall; scale down freely in Premiere.

Styles
- `chrome_light` / `chrome_dark`: Chrome (2023 refresh) active tab, macOS, with the bottom flares.
- `safari_light` / `safari_dark`: Safari (macOS 14/15) active tab chip, favicon + centred title.
- `terminal_light` / `terminal_dark`: native macOS window tab (Terminal.app), close cross on the left.

Favicons are drawn by hand in `tools/render_tabs.py` (nothing downloaded), so they
are close approximations, not the real brand files.

Regenerate: `python3 tools/render_tabs.py` (all) or `python3 tools/render_tabs.py 12` (one).
Edit the `TABS` list in that file to change titles, widths or styles.

| # | Style | Tab |
|---|---|---|
| 01 | Chrome light | YouTube: Consistent Hashing explained |
| 02 | Chrome light | arXiv: PagedAttention / vLLM paper |
| 03 | Safari light | GitHub: system-design-primer |
| 04 | Chrome dark | Claude Code overview, Claude Docs |
| 05 | Terminal dark | `claude` running in ~/inference-demo |
| 06 | Chrome light | YouTube: KV cache explained |
| 07 | Safari light | Wikipedia: CAP theorem |
| 08 | Chrome dark | localhost:3000 token stream demo |
| 09 | Chrome light | Codex, OpenAI |
| 10 | Chrome light | Medium: speculative decoding |
| 11 | Safari dark | YouTube: chat app scaling |
| 12 | Chrome light | Lil'Log: transformer inference optimization |
| 13 | Chrome light | Hacker News: p99 latency |
| 14 | Terminal light | `codex` running in ~/queue-sim |
| 15 | Chrome dark | Hugging Face: Llama-3.1-8B-Instruct |
| 16 | Safari light | Colab: inference_benchmark.ipynb |
| 17 | Chrome light | FastAPI Swagger UI (local demo API) |
| 18 | Chrome light | Stack Overflow: CUDA out of memory |
| 19 | Safari dark | fanout Roadmap |
| 20 | Chrome light | GitHub pull request: load shedding for the queue |
| 21 | Chrome dark | YouTube: designing a rate limiter |
| 22 | Chrome light | Google Docs: system design notes |
| 23 | Safari light | Excalidraw: inference topology |
| 24 | Chrome light | Claude chat: tensor parallelism |
| 25 | Chrome dark | VS Code: serve.py |
