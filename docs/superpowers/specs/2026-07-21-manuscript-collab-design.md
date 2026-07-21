# Manuscript Collab — Design

**Date:** 2026-07-21  
**Status:** approved / implemented on `feat/manuscript-collab`  
**Repo:** researchskills  
**Related:** `skills/manuscript-markdown/` (convert-only), vs-markdown-collab (inspiration only; CriticMarkup storage, not `<!--mc:-->`)

## Problem

Research manuscripts live in Markdown with CriticMarkup for coauthor review and agent provenance. Manuscript Markdown roundtrips MD ↔ DOCX and preserves comments as Word comments. Agent notes (Claude, Cursor, Codex, ChatGPT) should stay in the git-tracked `.md` for internal record, but must not appear in Word exports shared with collaborators.

There is no upstream flag to omit comments by author. Markdown Collab’s sidecar-style HTML markers are not the storage format we use (extension removed; CriticMarkup + Manuscript Markdown is canonical).

## Goals

1. Teach agents to leave CriticMarkup comments with a stable **author name**.
2. Support **address** and **review/comment** workflows on CriticMarkup (router skill).
3. Support **export for collaborators**: snapshot full MD → strip agent comments → DOCX via upstream CLI.
4. Keep convert engine **upstream** (do not vendor or reimplement Manuscript Markdown).

## Non-goals (v1)

- Forking or vendoring `jbearak/manuscript-markdown` (GPLv3; large surface).
- Reimplementing CriticMarkup ↔ Word conversion.
- Evidence-graph / citekey hover.
- Any Markdown WYSIWYG integration.
- Auto-resolving human review threads.
- Requiring the VS Code/Cursor extension for export.

## Decisions

| ID | Decision |
|----|----------|
| D1 | New router skill `manuscript-collab`; do **not** absorb into `manuscript-markdown`. |
| D2 | Storage = CriticMarkup in the `.md` file (not Markdown Collab `<!--mc:-->` JSON). |
| D3 | Agent authors allowlist: `Claude`, `Cursor`, `Codex`, `ChatGPT` (+ case/alias matching). |
| D4 | Preferred comment form: `{>>@Claude \| note<<}` (stripper also accepts `Claude (date) \|` without `@`). |
| D5 | Strip rule for paired highlight+agent comment: remove `{>>…<<}` **and** adjacent `{==…==}` / CriticMarkup highlight wrapper; keep bare text. |
| D6 | Leave human comments and unrelated `{++}` / `{--}` / `{~~}` alone on export. |
| D7 | Export requires upstream `manuscript-markdown` **CLI**; extension optional for humans. |
| D8 | researchskills may ship an **ensure/download** helper for the official CLI binary; not a fork. |
| D9 | Before strip/export, write a dated snapshot of the full `.md` under the project’s manuscript `_archive/` (or configurable archive dir). |

## Architecture

```text
User / agent
    │
    ▼
skills/manuscript-collab/          # router: comment | address | export
    │
    ├─ comment/review  → CriticMarkup authoring rules (reference.md)
    ├─ address         → edit prose; reply; do not resolve for humans
    └─ export          → scripts/export_for_collaborators.sh
                            │
                            ├─ 1. snapshot full .md → _archive/
                            ├─ 2. strip_agent_criticmarkup.py → temp .md
                            └─ 3. manuscript-markdown CLI → dest.docx

skills/manuscript-markdown/        # unchanged role: doctor + convert playbook
upstream manuscript-markdown CLI   # required for step 3
```

## Package layout

```text
skills/manuscript-collab/
  SKILL.md
  reference.md                         # author names, CriticMarkup patterns, modes
  scripts/
    strip_agent_criticmarkup.py        # stdin/file → stripped markdown
    export_for_collaborators.sh        # snapshot → strip → CLI
    ensure_manuscript_markdown_cli.sh  # optional: fetch official binary to ~/bin
```

No binary of Manuscript Markdown is committed to researchskills.

## Agent commenting contract

- Agents **must** attribute comments with an allowlisted name, preferably `@Name`:
  - `{>>@Claude | …<<}`
  - `{>>@Cursor | …<<}`
  - `{>>@Codex | …<<}`
  - `{>>@ChatGPT | …<<}`
- Humans use their own names (e.g. `{>>@Dahlia Foo (2025-09-09 22:21) | …<<}`) — never stripped.
- Agent-only notes that should never become Word comments may use HTML `<!-- … -->` (Manuscript Markdown keeps these invisible in DOCX). Prefer CriticMarkup when the note should be visible in-editor as a review affordance for the authoring team.

## Router modes

### comment / review

Triggers: “leave a note”, “review this md”, `/manuscript-collab review`.

- Instruct / apply CriticMarkup with required author attribution.
- Optional Review Mode: open agent comments on passages (do not edit prose unless asked).

### address

Triggers: “address comments”, “fix review feedback”.

- Actionable = CriticMarkup comments whose author is **not** on the agent allowlist (human comments).
- Edit surrounding prose; append a short agent reply as a new attributed comment when useful.
- Do not delete human comments unless explicitly asked.
- Do not mark threads “resolved” (humans resolve in Word or by deleting CriticMarkup).

### export / share

Triggers: “export for coauthors”, “share Word without agent comments”, `/manuscript-collab export`.

```text
export_for_collaborators.sh <source.md> <dest.docx> [--archive-dir DIR] [--force]
```

1. Doctor: `manuscript-markdown` on PATH (or run ensure helper if user opted in).
2. Snapshot: copy `source.md` → `<archive-dir>/<stem>-YYYY-MM-DD-HHMM.md` with a snapshot banner.
3. Strip: write temp stripped markdown (agent comments + paired highlights removed per D5).
4. Convert: `manuscript-markdown <temp.md> --output <dest.docx> [--force]`.
5. Report: snapshot path, counts stripped by author, DOCX path.

## Stripper behaviour (v1)

Input: Markdown string or file.  
Output: Markdown with agent CriticMarkup comments removed.

Match comment authors case-insensitively against allowlist and aliases, e.g.:

- `Claude`, `claude`, `@Claude`
- `Cursor`, `Composer` (alias → treat as Cursor if configured)
- `Codex`
- `ChatGPT`, `GPT`, `Chat GPT`

Patterns to remove when author matches:

1. Standalone `{>>…<<}` (including multiline bodies).
2. Immediately adjacent highlight wrappers tied to that comment:
   - `{==text==}{>>@Claude | …<<}` → `text`
   - CriticMarkup highlight forms used the same way in our corpus.

Do **not** remove:

- Human-authored `{>>…<<}`
- Standalone highlights with no agent comment
- `{++}` / `{--}` / `{~~}` regardless of author (v1)

Configurable allowlist via flag or small YAML next to the script (defaults baked in).

## Relationship to `manuscript-markdown` skill

| Concern | Owner |
|---------|--------|
| Install/doctor CLI or extension | `manuscript-markdown` |
| Raw MD↔DOCX conversion | `manuscript-markdown` + upstream CLI |
| Agent author names, address, strip, snapshot-export | `manuscript-collab` |

`manuscript-collab` export mode **invokes** the CLI; it does not duplicate convert docs. Cross-link both skills in descriptions so `/manuscript-collab export` and `/manuscript-markdown` do not conflict.

## Requirements matrix

| Capability | Required? |
|------------|-----------|
| `manuscript-markdown` CLI on PATH | **Yes** for export |
| Cursor/VS Code extension | Optional (human CriticMarkup UI) |
| Python 3 (stdlib) for stripper | Yes for export |
| Git archive dir writable | Yes for snapshot step |

## Success criteria

1. Agent following `manuscript-collab` leaves `@Claude`-style comments, not anonymous `{>>note<<}`.
2. Export of a file with mixed Dahlia + Claude comments produces DOCX with only human comments; Claude highlights wrappers unwrapped to bare text.
3. Full pre-strip `.md` exists under `_archive/` with timestamp.
4. Missing CLI fails with install/ensure instructions (no silent pandoc fallback).
5. No Manuscript Markdown source or binary vendored in researchskills.

## Open questions (non-blocking for v1)

- Exact reply syntax when addressing (append second `{>>@Claude | Re: …<<}` vs HTML note) — lock in implementation plan.
- Whether `Composer` maps to Cursor by default — default yes in allowlist aliases.
- Default archive path when project has no `docs/manuscript/_archive/` — fall back to `<source-dir>/_archive/`.

## Implementation order (preview)

1. Spec approval (this doc).
2. Plan: `docs/superpowers/plans/2026-07-21-manuscript-collab.md`.
3. `strip_agent_criticmarkup.py` + tests on fixtures (including MegaMove-style `Claude (date) |` and paired `{==}{>>}`).
4. `export_for_collaborators.sh` + `ensure_manuscript_markdown_cli.sh`.
5. `skills/manuscript-collab/SKILL.md` + `reference.md`.
6. Cross-links from `manuscript-markdown` skill description.
7. `./validate-skills.sh`.
