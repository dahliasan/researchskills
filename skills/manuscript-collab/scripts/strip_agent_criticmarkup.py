#!/usr/bin/env python3
"""Strip agent-authored CriticMarkup comments from Manuscript Markdown."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

DEFAULT_AGENT_AUTHORS = frozenset(
    {
        "claude",
        "cursor",
        "codex",
        "chatgpt",
        "composer",
        "gpt",
        "chat gpt",
    }
)

_COMMENT_RE = re.compile(r"\{>>((?:(?!\{>>).)*?)<<\}", re.DOTALL)

# Highlight immediately before cursor: {==text==} or ==text==
_HIGHLIGHT_BEFORE_RE = re.compile(
    r"(?:\{==([^=]+?)==\}|==([^=]+?)==)\s*\Z",
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
    """Return author if body looks attributed; else None."""
    s = body.strip()
    m = re.match(r"^@([^|(]+?)(?:\s*\([^)]*\))?\s*\|\s*", s)
    if m:
        return m.group(1).strip()
    m = re.match(r"^([A-Za-z][A-Za-z0-9 ._-]*?)(?:\s*\([^)]*\))?\s*\|\s*", s)
    if m:
        return m.group(1).strip()
    return None


def _is_agent_author(author: str | None, agents: frozenset[str]) -> bool:
    if not author:
        return False
    key = author.strip().lstrip("@").lower()
    if key in agents:
        return True
    first = key.split()[0] if key else ""
    return first in agents


def strip_agent_comments(
    text: str,
    *,
    authors: frozenset[str] | None = None,
) -> tuple[str, dict[str, int]]:
    agents = authors if authors is not None else DEFAULT_AGENT_AUTHORS
    stats: Counter[str] = Counter()
    out: list[str] = []
    pos = 0

    for match in _COMMENT_RE.finditer(text):
        start, end = match.span()
        body = match.group(1)
        author = _parse_comment_author(body)
        out.append(text[pos:start])
        if _is_agent_author(author, agents):
            stats[_canonical_author(author or "agent")] += 1
            buf = "".join(out)
            hm = _HIGHLIGHT_BEFORE_RE.search(buf)
            if hm is not None:
                inner = hm.group(1) if hm.group(1) is not None else hm.group(2)
                out = [buf[: hm.start()], inner or ""]
            # drop comment
        else:
            out.append(match.group(0))
        pos = end

    out.append(text[pos:])
    result = "".join(out)
    result = re.sub(r"[ \t]{2,}", " ", result)
    return result, dict(stats)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--in", dest="infile", required=True)
    p.add_argument("--out", dest="outfile", required=True)
    p.add_argument("--stats", action="store_true")
    args = p.parse_args(argv)
    text = Path(args.infile).read_text(encoding="utf-8")
    stripped, stats = strip_agent_comments(text)
    Path(args.outfile).write_text(stripped, encoding="utf-8")
    if args.stats:
        for k, v in sorted(stats.items()):
            print(f"{k}: {v}", file=sys.stderr)
        print(f"total: {sum(stats.values())}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
