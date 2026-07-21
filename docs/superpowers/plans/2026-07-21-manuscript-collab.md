# Manuscript Collab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `manuscript-collab` skill that teaches agents CriticMarkup authorship, addresses human comments, and exports Word docs after snapshotting and stripping agent comments via the upstream `manuscript-markdown` CLI.

**Architecture:** Python stripper (stdlib) is the core; a shell wrapper snapshots then strips then calls upstream CLI; a router skill documents comment/address/export modes. Convert engine stays upstream (not vendored).

**Tech Stack:** Python 3 unittest (stdlib), bash, Markdown skill docs, upstream `manuscript-markdown` CLI (external binary).

**Spec:** `docs/superpowers/specs/2026-07-21-manuscript-collab-design.md`

## Global Constraints

- Do not vendor or reimplement `jbearak/manuscript-markdown` (GPLv3).
- Do not silently fall back to pandoc.
- Scrub personal paths from skill runtime files (`AGENTS.md`).
- Prefer `@AgentName` CriticMarkup attribution; stripper must also accept `Name (date) |` without `@`.
- Strip rule D5: remove agent `{>>…<<}` and adjacent `{==…==}` wrapper; keep bare text.
- Leave human comments and `{++}` / `{--}` / `{~~}` alone.
- Agent allowlist: Claude, Cursor, Codex, ChatGPT; alias `Composer` → Cursor; case-insensitive.
- Address reply syntax (locked): append `{>>@Claude | …<<}` (or the acting agent name) after the human comment; never delete or edit the human comment body; never set a “resolved” flag.
- Archive default: `docs/manuscript/_archive/` if it exists under a parent of the source file; else `<source-dir>/_archive/`.
- Extension optional; CLI required for export.

## File map

| Path | Responsibility |
|------|----------------|
| `skills/manuscript-collab/scripts/strip_agent_criticmarkup.py` | Pure strip + CLI `--in` / `--out` / `--stats` |
| `skills/manuscript-collab/scripts/export_for_collaborators.sh` | Snapshot → strip → `manuscript-markdown` |
| `skills/manuscript-collab/scripts/ensure_manuscript_markdown_cli.sh` | Optional download of official CLI to `~/bin` |
| `skills/manuscript-collab/SKILL.md` | Router: comment / address / export |
| `skills/manuscript-collab/reference.md` | Author list, patterns, strip/export details |
| `tests/test_strip_agent_criticmarkup.py` | Unit tests for stripper |
| `tests/fixtures/criticmarkup_mixed.md` | Fixture with human + agent comments |
| `validate-skills.sh` | Register skill + script + offline test |
| `skills/manuscript-markdown/SKILL.md` | Cross-link export-for-share → collab |
| `skills/researchskills/SKILL.md` | Route table entry |
| `README.md` | Skill table row |

---

### Task 1: Stripper library + unit tests (TDD)

**Files:**
- Create: `skills/manuscript-collab/scripts/strip_agent_criticmarkup.py`
- Create: `tests/test_strip_agent_criticmarkup.py`
- Create: `tests/fixtures/criticmarkup_mixed.md`

**Interfaces:**
- Produces: `strip_agent_comments(text: str, *, authors: frozenset[str] | None = None) -> tuple[str, dict[str, int]]`
- Produces: `DEFAULT_AGENT_AUTHORS: frozenset[str]`
- Produces: CLI `python3 strip_agent_criticmarkup.py --in PATH --out PATH [--stats]`
- Consumes: nothing from later tasks

- [ ] **Step 1: Write the failing test file**

Create `tests/test_strip_agent_criticmarkup.py`:

```python
#!/usr/bin/env python3
"""Unit tests for manuscript-collab agent CriticMarkup stripper."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/manuscript-collab/scripts/strip_agent_criticmarkup.py"
FIXTURE = ROOT / "tests/fixtures/criticmarkup_mixed.md"


def load_mod():
    spec = importlib.util.spec_from_file_location("strip_agent_criticmarkup", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestStripAgentCriticmarkup(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_mod()

    def test_keeps_human_comment(self) -> None:
        src = "Hello.{>>@Dahlia Foo (2025-09-09 22:21) | Please expand.<<}"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, src)
        self.assertEqual(sum(stats.values()), 0)

    def test_strips_at_claude(self) -> None:
        src = "Hello.{>>@Claude | provenance note<<} World"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, "Hello. World")
        self.assertGreaterEqual(stats.get("Claude", 0), 1)

    def test_strips_claude_date_without_at(self) -> None:
        src = "X.{>>Claude (2026-07-21) | Provenance: seed=42.<<}Y"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, "X.Y")
        self.assertGreaterEqual(stats.get("Claude", 0), 1)

    def test_unwraps_paired_highlight(self) -> None:
        src = "{==Introduction==}{>>@Claude | fix heading<<}"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, "Introduction")
        self.assertGreaterEqual(sum(stats.values()), 1)

    def test_keeps_standalone_highlight(self) -> None:
        src = "See {==important==} claim."
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, src)
        self.assertEqual(sum(stats.values()), 0)

    def test_keeps_track_changes(self) -> None:
        src = "A {++added++} B {--deleted--} C {~~old~>new~~}"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, src)

    def test_composer_alias_as_cursor(self) -> None:
        src = "Note.{>>@Composer | agent note<<}"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, "Note.")
        self.assertTrue(sum(stats.values()) >= 1)

    def test_fixture_mixed(self) -> None:
        text = FIXTURE.read_text(encoding="utf-8")
        out, stats = self.mod.strip_agent_comments(text)
        self.assertIn("@Dahlia Foo", out)
        self.assertNotIn("@Claude", out)
        self.assertNotIn("Claude (2026-07-21)", out)
        self.assertIn("Keep this human comment", out)
        self.assertIn("Bare after unwrap", out)
        self.assertGreaterEqual(sum(stats.values()), 2)


if __name__ == "__main__":
    unittest.main()
```

Create `tests/fixtures/criticmarkup_mixed.md`:

```markdown
# Sample

{#1}Keep this human comment{/1}{#1>>@Dahlia Foo (2025-09-09 22:21) | Keep this human comment<<}

Normal prose with agent note.{>>@Claude | remove me<<}

{==Bare after unwrap==}{>>Claude (2026-07-21) | unwrap this highlight<<}

Leave {++addition++} and {--deletion--} alone.
```

Note: if ID-based comment syntax is awkward for v1 parser, simplify the fixture human line to:

```markdown
Keep this human comment.{>>@Dahlia Foo (2025-09-09 22:21) | Keep this human comment<<}
```

Use the simplified human line in the fixture (inline CriticMarkup only for v1). Update `test_fixture_mixed` expectations accordingly (still require `@Dahlia Foo` present).

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /path/to/researchskills && python3 tests/test_strip_agent_criticmarkup.py -v`

Expected: FAIL (module / file not found)

- [ ] **Step 3: Implement stripper**

Create `skills/manuscript-collab/scripts/strip_agent_criticmarkup.py` with at least:

```python
#!/usr/bin/env python3
"""Strip agent-authored CriticMarkup comments from Manuscript Markdown."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from typing import Iterable

DEFAULT_AGENT_AUTHORS = frozenset(
    {
        "claude",
        "cursor",
        "codex",
        "chatgpt",
        "composer",  # alias → counted under Cursor in stats if desired
        "gpt",
        "chat gpt",
    }
)

# CriticMarkup comment: {>> ... <<} non-greedy, DOTALL
_COMMENT_RE = re.compile(r"\{>>((?:(?!\{>>).)*?)<<\}", re.DOTALL)

# Optional immediately preceding ==highlight== (not CriticMarkup {==...==} only —
# support both ==text== and {==text==} used in corpus)
_HIGHLIGHT_BEFORE_RE = re.compile(
    r"(?:\{==([^=]+?)==\}|==([^=]+?)==)\s*$",
    re.DOTALL,
)


def _canonical_author(raw: str) -> str:
    key = raw.strip().lstrip("@").lower()
    if key in {"composer"}:
        return "Cursor"
    if key in {"gpt", "chat gpt", "chatgpt"}:
        return "ChatGPT"
    if key == "claude":
        return "Claude"
    if key == "cursor":
        return "Cursor"
    if key == "codex":
        return "Codex"
    return raw.strip().lstrip("@")


def _parse_comment_author(body: str) -> str | None:
    """Return author if body looks attributed; else None (anonymous / human-unattributed)."""
    s = body.strip()
    # @Author | text   OR   @Author (date) | text
    m = re.match(
        r"^@([^|(]+?)(?:\s*\([^)]*\))?\s*\|\s*",
        s,
    )
    if m:
        return m.group(1).strip()
    # Author (date) | text   OR   Author | text  (no @)
    m = re.match(
        r"^([A-Za-z][A-Za-z0-9 ._-]*?)(?:\s*\([^)]*\))?\s*\|\s*",
        s,
    )
    if m:
        return m.group(1).strip()
    return None


def _is_agent_author(author: str | None, agents: frozenset[str]) -> bool:
    if not author:
        return False
    key = author.strip().lstrip("@").lower()
    if key in agents:
        return True
    # first token only (e.g. "Claude Opus" → claude)
    first = key.split()[0] if key else ""
    return first in agents


def strip_agent_comments(
    text: str,
    *,
    authors: frozenset[str] | None = None,
) -> tuple[str, dict[str, int]]:
    agents = authors if authors is not None else DEFAULT_AGENT_AUTHORS
    stats: Counter[str] = Counter()

    def repl(match: re.Match[str]) -> str:
        body = match.group(1)
        author = _parse_comment_author(body)
        if not _is_agent_author(author, agents):
            return match.group(0)
        label = _canonical_author(author or "agent")
        stats[label] += 1
        return ""  # remove comment; highlight unwrap handled in pass 2

    # Pass 1: remove agent comments
    without_comments = _COMMENT_RE.sub(repl, text)

    # Pass 2: unwrap highlights that now sit immediately before removed-comment holes
    # Simpler approach: while scanning original, when removing an agent comment,
    # also peel a highlight that immediately precedes it.
    # Re-implement as single-pass for correctness:

    stats = Counter()
    out: list[str] = []
    pos = 0
    for match in _COMMENT_RE.finditer(text):
        start, end = match.span()
        body = match.group(1)
        author = _parse_comment_author(body)
        out.append(text[pos:start])
        if _is_agent_author(author, agents):
            stats[_canonical_author(author or "agent")] += 1
            # Peel trailing highlight from out buffer end
            buf = "".join(out)
            hm = _HIGHLIGHT_BEFORE_RE.search(buf)
            if hm and hm.end() == len(buf):
                inner = hm.group(1) if hm.group(1) is not None else hm.group(2)
                out = [buf[: hm.start()], inner]
            # drop comment (append nothing)
        else:
            out.append(match.group(0))
        pos = end
    out.append(text[pos:])
    result = "".join(out)
    # Collapse awkward double spaces left by removals (preserve newlines)
    result = re.sub(r"[ \t]{2,}", " ", result)
    return result, dict(stats)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--in", dest="infile", required=True)
    p.add_argument("--out", dest="outfile", required=True)
    p.add_argument("--stats", action="store_true")
    args = p.parse_args(argv)
    text = Path_read(args.infile)
    stripped, stats = strip_agent_comments(text)
    Path_write(args.outfile, stripped)
    if args.stats:
        for k, v in sorted(stats.items()):
            print(f"{k}: {v}", file=sys.stderr)
        print(f"total: {sum(stats.values())}", file=sys.stderr)
    return 0


def Path_read(path: str) -> str:
    from pathlib import Path

    return Path(path).read_text(encoding="utf-8")


def Path_write(path: str, text: str) -> None:
    from pathlib import Path

    Path(path).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
```

Implement the single-pass version cleanly (fix the draft’s dual-pass leftovers). Prefer `pathlib.Path` imports at top. Ensure `test_unwraps_paired_highlight` passes for `{==Introduction==}{>>@Claude | fix heading<<}` → `Introduction`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tests/test_strip_agent_criticmarkup.py -v`

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add skills/manuscript-collab/scripts/strip_agent_criticmarkup.py \
  tests/test_strip_agent_criticmarkup.py \
  tests/fixtures/criticmarkup_mixed.md
git commit -m "$(cat <<'EOF'
✨ feat: add CriticMarkup agent-comment stripper

EOF
)"
```

---

### Task 2: Export + ensure shell scripts

**Files:**
- Create: `skills/manuscript-collab/scripts/export_for_collaborators.sh`
- Create: `skills/manuscript-collab/scripts/ensure_manuscript_markdown_cli.sh`

**Interfaces:**
- Consumes: `strip_agent_criticmarkup.py --in --out --stats`
- Consumes: `manuscript-markdown` on PATH
- Produces: `export_for_collaborators.sh <source.md> <dest.docx> [--archive-dir DIR] [--force] [--ensure-cli]`

- [ ] **Step 1: Write `ensure_manuscript_markdown_cli.sh`**

```bash
#!/usr/bin/env bash
# Download official manuscript-markdown CLI to ~/bin if missing.
set -euo pipefail

if command -v manuscript-markdown >/dev/null 2>&1; then
  manuscript-markdown --version
  exit 0
fi

VERSION="${MANUSCRIPT_MARKDOWN_VERSION:-1.2.0}"
DEST_DIR="${MANUSCRIPT_MARKDOWN_BIN_DIR:-$HOME/bin}"
mkdir -p "$DEST_DIR"

uname_s="$(uname -s)"
uname_m="$(uname -m)"
case "$uname_s-$uname_m" in
  Darwin-arm64) asset="manuscript-markdown-darwin-arm64" ;;
  Darwin-x86_64) asset="manuscript-markdown-darwin-x64" ;;
  Linux-aarch64) asset="manuscript-markdown-linux-arm64" ;;
  Linux-x86_64) asset="manuscript-markdown-linux-x64" ;;
  *)
    echo "Unsupported platform: $uname_s $uname_m" >&2
    echo "Download manually from https://github.com/jbearak/manuscript-markdown/releases" >&2
    exit 1
    ;;
esac

url="https://github.com/jbearak/manuscript-markdown/releases/download/v${VERSION}/${asset}"
out="$DEST_DIR/manuscript-markdown"
echo "Downloading $url → $out" >&2
curl -fsSL -o "$out" "$url"
chmod +x "$out"
if ! command -v manuscript-markdown >/dev/null 2>&1; then
  echo "Installed to $out but not on PATH. Add $DEST_DIR to PATH." >&2
  exit 1
fi
manuscript-markdown --version
```

- [ ] **Step 2: Write `export_for_collaborators.sh`**

```bash
#!/usr/bin/env bash
# Snapshot full markdown, strip agent CriticMarkup, convert to DOCX.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
STRIP="$ROOT/skills/manuscript-collab/scripts/strip_agent_criticmarkup.py"
ENSURE="$ROOT/skills/manuscript-collab/scripts/ensure_manuscript_markdown_cli.sh"

usage() {
  echo "Usage: $0 <source.md> <dest.docx> [--archive-dir DIR] [--force] [--ensure-cli]" >&2
  exit 2
}

[[ $# -ge 2 ]] || usage
SOURCE="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
DEST="$2"
shift 2
ARCHIVE_DIR=""
FORCE=0
ENSURE_CLI=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --archive-dir) ARCHIVE_DIR="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --ensure-cli) ENSURE_CLI=1; shift ;;
    *) usage ;;
  esac
done

[[ -f "$SOURCE" ]] || { echo "Missing source: $SOURCE" >&2; exit 1; }
[[ "$SOURCE" == *.md ]] || { echo "Source must be .md" >&2; exit 1; }

if ! command -v manuscript-markdown >/dev/null 2>&1; then
  if [[ "$ENSURE_CLI" -eq 1 ]]; then
    bash "$ENSURE"
  else
    echo "manuscript-markdown CLI not on PATH." >&2
    echo "Install from GitHub Releases or re-run with --ensure-cli." >&2
    echo "See skills/manuscript-markdown/references/install.md" >&2
    exit 1
  fi
fi

stem="$(basename "$SOURCE" .md)"
src_dir="$(dirname "$SOURCE")"
if [[ -z "$ARCHIVE_DIR" ]]; then
  if [[ -d "$src_dir/../_archive" ]]; then
    ARCHIVE_DIR="$(cd "$src_dir/../_archive" && pwd)"
  elif [[ -d "$src_dir/../../manuscript/_archive" ]]; then
    ARCHIVE_DIR="$(cd "$src_dir/../../manuscript/_archive" && pwd)"
  elif [[ -d "$(dirname "$src_dir")/_archive" ]]; then
    ARCHIVE_DIR="$(cd "$(dirname "$src_dir")/_archive" && pwd)"
  else
    # Prefer docs/manuscript/_archive when walking up
    probe="$src_dir"
    ARCHIVE_DIR=""
    for _ in 1 2 3 4 5 6; do
      if [[ -d "$probe/docs/manuscript/_archive" ]]; then
        ARCHIVE_DIR="$probe/docs/manuscript/_archive"
        break
      fi
      probe="$(dirname "$probe")"
    done
    if [[ -z "$ARCHIVE_DIR" ]]; then
      ARCHIVE_DIR="$src_dir/_archive"
    fi
  fi
fi
mkdir -p "$ARCHIVE_DIR"

stamp="$(date +%Y-%m-%d-%H%M)"
snap="$ARCHIVE_DIR/${stem}-${stamp}.md"
{
  echo "<!-- SNAPSHOT backup of $(basename "$SOURCE")"
  echo "Taken: $stamp (local). Full file including agent CriticMarkup. Do not edit as canonical."
  echo "Canonical: $SOURCE"
  echo "-->"
  echo
  cat "$SOURCE"
} >"$snap"
echo "Snapshot: $snap"

tmp="$(mktemp -t "${stem}.stripped.XXXXXX.md")"
trap 'rm -f "$tmp"' EXIT
python3 "$STRIP" --in "$SOURCE" --out "$tmp" --stats

mm_args=("$tmp" --output "$DEST")
if [[ "$FORCE" -eq 1 ]]; then
  mm_args+=(--force)
fi
manuscript-markdown "${mm_args[@]}"
echo "DOCX: $DEST"
```

Simplify archive discovery in the real script to this rule only (match spec):

1. If `--archive-dir` set, use it.
2. Else walk parents for `docs/manuscript/_archive`.
3. Else use `<source-dir>/_archive`.

- [ ] **Step 3: chmod + dry-run strip path**

```bash
chmod +x skills/manuscript-collab/scripts/*.sh
python3 skills/manuscript-collab/scripts/strip_agent_criticmarkup.py \
  --in tests/fixtures/criticmarkup_mixed.md \
  --out /tmp/stripped-test.md --stats
```

Expected: stderr stats; `/tmp/stripped-test.md` keeps Dahlia comment, drops Claude.

- [ ] **Step 4: Commit**

```bash
git add skills/manuscript-collab/scripts/export_for_collaborators.sh \
  skills/manuscript-collab/scripts/ensure_manuscript_markdown_cli.sh
git commit -m "$(cat <<'EOF'
✨ feat: add collaborator export and CLI ensure scripts

EOF
)"
```

---

### Task 3: Skill docs (`SKILL.md` + `reference.md`)

**Files:**
- Create: `skills/manuscript-collab/SKILL.md`
- Create: `skills/manuscript-collab/reference.md`

**Interfaces:**
- Consumes: scripts from Tasks 1–2
- Produces: agent-facing router documentation

- [ ] **Step 1: Write `SKILL.md`**

Frontmatter `name: manuscript-collab`. Description must mention: CriticMarkup agent comments, address human review, export for coauthors (strip agents + snapshot + DOCX), `/manuscript-collab`. Modes: comment/review, address, export. Point convert details to `manuscript-markdown`. Include install gate for export (CLI). Include exact export command:

```bash
bash skills/manuscript-collab/scripts/export_for_collaborators.sh \
  path/to/paper.md path/to/share.docx --force
```

Address rules: actionable = non-allowlist authors; append `{>>@Claude | …<<}` reply; do not delete human comments; do not claim resolved.

- [ ] **Step 2: Write `reference.md`**

Include: allowlist + aliases, preferred `@Name` form, strip D5 examples, snapshot location rules, HTML `<!-- -->` for never-visible notes, link to Manuscript Markdown CriticMarkup docs.

- [ ] **Step 3: Commit**

```bash
git add skills/manuscript-collab/SKILL.md skills/manuscript-collab/reference.md
git commit -m "$(cat <<'EOF'
📝 docs: add manuscript-collab router skill

EOF
)"
```

---

### Task 4: Wire pack (validate, router, README, cross-links)

**Files:**
- Modify: `validate-skills.sh`
- Modify: `skills/researchskills/SKILL.md`
- Modify: `skills/manuscript-markdown/SKILL.md`
- Modify: `README.md`
- Modify: `tests` hook in `validate-skills.sh` to run the new unittest

- [ ] **Step 1: Update `validate-skills.sh`**

Add `manuscript-collab` to `required_skills`.  
Add to required scripts:

```bash
skills/manuscript-collab/scripts/strip_agent_criticmarkup.py
skills/manuscript-collab/scripts/export_for_collaborators.sh
skills/manuscript-collab/scripts/ensure_manuscript_markdown_cli.sh
```

Under offline tests, add:

```bash
python3 tests/test_strip_agent_criticmarkup.py
```

- [ ] **Step 2: Update `skills/researchskills/SKILL.md`**

Add route row:

| CriticMarkup collab, address review comments, or export Word without agent comments | `manuscript-collab` |

Mention in description list. Bump metadata version patch.

- [ ] **Step 3: Cross-link `manuscript-markdown`**

In `skills/manuscript-markdown/SKILL.md`, add a short “Share with coauthors” note: for stripping agent CriticMarkup before DOCX, use `manuscript-collab` export (do not expand convert skill into collab policy).

- [ ] **Step 4: Update `README.md` skill table**

Add row for manuscript-collab.

- [ ] **Step 5: Run validation**

```bash
./validate-skills.sh
```

Expected: `ALL OK`

- [ ] **Step 6: Commit**

```bash
git add validate-skills.sh skills/researchskills/SKILL.md \
  skills/manuscript-markdown/SKILL.md README.md
git commit -m "$(cat <<'EOF'
🔧 chore: register manuscript-collab in pack validation and routers

EOF
)"
```

---

### Task 5: Spec status + smoke note

**Files:**
- Modify: `docs/superpowers/specs/2026-07-21-manuscript-collab-design.md` (status → approved/implemented-ready)

- [ ] **Step 1: Mark spec status**

Set `**Status:** approved` (or `implemented` after code lands).

- [ ] **Step 2: Optional smoke (if CLI present)**

```bash
bash skills/manuscript-collab/scripts/export_for_collaborators.sh \
  tests/fixtures/criticmarkup_mixed.md /tmp/collab-smoke.docx --force --archive-dir /tmp/collab-archive
```

Expected: snapshot under `/tmp/collab-archive`, DOCX written, no Claude comments in a roundtrip check if desired.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-07-21-manuscript-collab-design.md
git commit -m "$(cat <<'EOF'
📝 docs: mark manuscript-collab spec approved

EOF
)"
```

---

## Spec coverage checklist

| Spec item | Task |
|-----------|------|
| D1 new router skill | 3 |
| D2 CriticMarkup storage | 3 |
| D3–D4 author allowlist / `@Name` | 1, 3 |
| D5 unwrap highlight | 1 |
| D6 keep human + track changes | 1 |
| D7 CLI required / extension optional | 2, 3 |
| D8 ensure helper | 2 |
| D9 snapshot | 2 |
| Address / comment / export modes | 3 |
| Pack registration | 4 |
| No vendor binary | all |

## Placeholder / consistency self-review

- Locked reply syntax: append `{>>@Agent | …<<}`.
- Locked Composer → Cursor.
- Locked archive fallback.
- Function name stable: `strip_agent_comments`.
- No pandoc fallback steps.

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-21-manuscript-collab.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — run tasks in this session with checkpoints  

Which approach?
