# Instruction set

The rules the pipeline works under, in the order to read them. `memory/` is a verbatim copy of the assistant's persistent notes (one fact per file, dated); the other documents live at the repo root.

1. `memory/hard-rules-no-slop.md` — everything the editor does not want. Check every cut against it.
2. `memory/session-2026-10-24-index.md` — where things live and how the reel pipeline runs end to end.
3. `../NORMAL_UGC_1_CONTEXT.md` — the approved style "Normal UGC 1" in one file (also packaged as a Claude Code skill in `../.claude/skills/normal-ugc-1/SKILL.md`).
4. `../EDITING_SYSTEM.md` — the full spec: layout grammar, title and caption styles, in/out animation, SFX, Premiere project format, FCP7 XML dialect.
5. `memory/reel-feedback-first-build.md`, `memory/fanout-reel-editing-system.md`, `memory/style-normal-ugc-1.md`, `memory/abik-editor-profile.md` — the feedback rounds and the working agreement (preview first, package after approval).
6. `../UGC_REFERENCE_STUDY.md`, `memory/ugc-reference-styles.md` — the 21-ad study (taste reference, not a licence to copy devices).
7. Script side: `../AD_SCRIPT_PLAYBOOK.md`, `memory/avb-ad-playbook.md`, `memory/script-trigger-workflow.md`, `memory/script-delivery-in-chat.md`, and the scripts at the repo root (`Fanout … script.md`).
8. Later reference formats: `memory/tab-windows-overlays.md`, `memory/devmonk-explainer-reference.md`, `memory/metro-media-house-reference.md`.

`memory/MEMORY.md` is the index the assistant loads at the start of every session.

Paths inside the notes point at the editor's machine (`/Users/abiknewar/…`); the same files are in this repo under the same names.
