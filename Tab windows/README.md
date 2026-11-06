# Tab windows (25)

Full browser windows like the reference: macOS Chrome window (tab strip, address bar,
page) cut out on transparency. No desktop, no shadow, no mockup. The only opaque pixels
are the window itself, with 11 px rounded corners.

- 23 Chrome windows (dark frame on YouTube, Claude Docs, localhost, Hugging Face, fanout,
  GitHub PR, VS Code; light frame on the rest).
- 2 native macOS Terminal windows: Claude Code (dark) and Codex CLI (light).
- 1700 x 880 CSS px rendered at 2x = 3400 x 1760 px PNG, RGBA.

Every page is hand-built HTML that mimics the real site (YouTube, arXiv, GitHub, Claude
Docs, Wikipedia, Medium, Lil'Log, Hacker News, Hugging Face, Colab, Swagger, Stack
Overflow, fanout, Google Docs, Excalidraw, claude.ai, vscode.dev). Favicons and logos are
drawn approximations. Video titles, channels and article authors are invented except the
real arXiv paper, the real Lil'Log post, the real system-design-primer repo and the real
Llama 3.1 model card.

Regenerate: `python3 tools/render_tab_windows.py` (all + contact sheet) or
`python3 tools/render_tab_windows.py 7 12` (some). Pages live in `tools/tabwin/pages.py`,
the window frame in `tools/tabwin/frame.py`, favicons in `tools/tabwin/icons.py`.

| # | Window | Site |
|---|---|---|
| 01 | Chrome dark | YouTube: Consistent Hashing explained |
| 02 | Chrome light | arXiv: PagedAttention / vLLM paper |
| 03 | Chrome light | GitHub: system-design-primer |
| 04 | Chrome dark | Claude Docs: Claude Code overview |
| 05 | Terminal dark | Claude Code session in ~/inference-demo |
| 06 | Chrome dark | YouTube: KV cache explained |
| 07 | Chrome light | Wikipedia: CAP theorem |
| 08 | Chrome dark | localhost:3000 token-stream demo |
| 09 | Chrome light | OpenAI: Codex product page |
| 10 | Chrome light | Medium: speculative decoding |
| 11 | Chrome dark | YouTube: chat app at trillions of messages |
| 12 | Chrome light | Lil'Log: transformer inference optimization |
| 13 | Chrome light | Hacker News front page |
| 14 | Terminal light | Codex CLI in ~/queue-sim |
| 15 | Chrome dark | Hugging Face: Llama-3.1-8B-Instruct |
| 16 | Chrome light | Colab: inference_benchmark.ipynb |
| 17 | Chrome light | FastAPI Swagger UI on localhost:8000 |
| 18 | Chrome light | Stack Overflow: CUDA out of memory |
| 19 | Chrome dark | fanout.sh Roadmap |
| 20 | Chrome dark | GitHub PR: load shedding for the queue |
| 21 | Chrome dark | YouTube: designing a rate limiter |
| 22 | Chrome light | Google Docs: system design notes |
| 23 | Chrome light | Excalidraw: inference topology |
| 24 | Chrome light | claude.ai: tensor parallelism chat |
| 25 | Chrome dark | vscode.dev: serve.py |
