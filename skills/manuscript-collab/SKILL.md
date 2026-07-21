---
name: manuscript-collab
description: >-
  CriticMarkup collaboration for research Markdown: teach agents to attribute
  comments (@Claude/@Cursor/@Codex/@ChatGPT), address human review comments,
  and export Word for coauthors after snapshotting and stripping agent notes.
  Use when the user says "/manuscript-collab", asks to leave agent comments,
  address CriticMarkup review feedback, or share DOCX without Claude/Cursor
  comments. Convert engine is upstream manuscript-markdown CLI (required for
  export); extension optional. Does not draft scientific prose
  (use manuscript-writing).
metadata:
  version: 0.1.0
---

# /manuscript-collab — CriticMarkup collab router

Router for **comment / address / export**. Storage is CriticMarkup in the `.md`
file (not Markdown Collab `<!--mc:-->`). DOCX conversion stays in
`manuscript-markdown` + upstream CLI.

Details: [reference.md](reference.md)

## Step 0 — Detect mode

| Signal | Mode |
|--------|------|
| “leave a note”, “review this md”, `/manuscript-collab review` | **comment / review** |
| “address comments”, “fix review feedback” | **address** |
| “export for coauthors”, “share Word without agent comments”, `/manuscript-collab export` | **export** |
| “install CLI” / doctor for share-export | **export** install gate |

## Mode: comment / review

Agents **must** attribute CriticMarkup comments with an allowlisted name:

```markdown
{>>@Claude | note<<}
{>>@Cursor | note<<}
{>>@Codex | note<<}
{>>@ChatGPT | note<<}
```

Prefer `@Name`. Optional timestamp: `{>>@Claude (2026-07-21 14:00) | note<<}`.

Review Mode: open agent comments on passages; do **not** edit prose unless asked.

Never-visible agent-only notes may use HTML `<!-- … -->` (invisible in Word).

## Mode: address

1. Find CriticMarkup `{>>…<<}` whose author is **not** on the agent allowlist
   (human comments such as `@Dahlia Foo`).
2. Edit surrounding prose as requested.
3. Append a reply: `{>>@Claude | …<<}` (or your acting agent name) after the
   human comment. Do **not** delete or edit the human comment body. Do **not**
   claim the thread is resolved (humans resolve).

## Mode: export

**Requires** `manuscript-markdown` on `PATH`. Extension is optional.

From the researchskills repo root (or with absolute script paths):

```bash
bash skills/manuscript-collab/scripts/export_for_collaborators.sh \
  path/to/paper.md path/to/share.docx --force
```

Optional: `--archive-dir DIR`, `--ensure-cli` (download official binary to `~/bin`).

Pipeline:

1. Snapshot full `.md` (agent comments kept) → archive
2. Strip agent comments (+ paired `{==…==}` wrappers → bare text)
3. `manuscript-markdown` → DOCX

**Do not** fall back to pandoc. If CLI missing, stop and point to
`skills/manuscript-markdown/references/install.md` or `--ensure-cli`.

## Composes with

- `manuscript-markdown` — raw MD↔DOCX / install doctor
- `manuscript-writing` — prose draft/revise (not this skill)
