#!/usr/bin/env python3
"""OpenAlex works search for researchskills discover-papers.

Uses only the Python standard library. Prefer RESEARCHSKILLS_MAILTO or
OPENALEX_MAILTO for the polite pool.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

OPENALEX_BASE = "https://api.openalex.org/works"
DEFAULT_MAILTO = os.environ.get("RESEARCHSKILLS_MAILTO") or os.environ.get(
    "OPENALEX_MAILTO", ""
)


def _parse_yaml_frontmatter(text: str) -> dict[str, Any]:
    """Minimal YAML subset for PROTOCOL.md front matter (no PyYAML required)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end].strip()
    # Prefer PyYAML when available
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(block)
        return data if isinstance(data, dict) else {}
    except Exception:
        pass
    # Fallback: extract search.queries list items and simple date_range
    data: dict[str, Any] = {"search": {"queries": []}, "question": {}, "date_range": {}}
    in_queries = False
    for line in block.splitlines():
        if re.match(r"^search:\s*$", line):
            in_queries = False
            continue
        if re.match(r"^\s+queries:\s*$", line):
            in_queries = True
            continue
        if in_queries:
            m = re.match(r'^\s+-\s+["\']?(.*?)["\']?\s*$', line)
            if m:
                data["search"]["queries"].append(m.group(1))
                continue
            if re.match(r"^\S", line) or re.match(r"^\s+[a-zA-Z_]+:", line):
                in_queries = False
        for key in ("population", "concept", "context"):
            m = re.match(rf'^\s+{key}:\s+["\']?(.*?)["\']?\s*$', line)
            if m:
                data["question"][key] = m.group(1)
        m = re.match(r'^name:\s+["\']?(.*?)["\']?\s*$', line)
        if m:
            data["name"] = m.group(1)
        m = re.match(r'^\s+from:\s+["\']?(\d{4}-\d{2}-\d{2})["\']?\s*$', line)
        if m:
            data["date_range"]["from"] = m.group(1)
        m = re.match(r'^\s+to:\s+["\']?(\d{4}-\d{2}-\d{2})["\']?\s*$', line)
        if m:
            data["date_range"]["to"] = m.group(1)
    return data


def search_queries_from_snapshot(snapshot: dict[str, Any]) -> list[str]:
    search = snapshot.get("search") or {}
    queries = search.get("queries")
    if isinstance(queries, list):
        cleaned = [str(q).strip() for q in queries if str(q).strip()]
        if cleaned:
            return cleaned
    question = snapshot.get("question") or {}
    parts = [
        str(question[k])
        for k in ("population", "concept", "context")
        if question.get(k)
    ]
    if parts:
        return [" ".join(parts)]
    return [str(snapshot.get("name", "literature review"))]


def _user_agent(mailto: str) -> str:
    identity = mailto or "researchskills@users.noreply.github.com"
    return f"researchskills/0.1 (mailto:{identity})"


def openalex_search(
    query: str,
    *,
    mailto: str,
    per_page: int = 25,
    max_pages: int = 1,
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    filters: list[str] = []
    if from_date:
        filters.append(f"from_publication_date:{from_date}")
    if to_date:
        filters.append(f"to_publication_date:{to_date}")
    for page in range(1, max_pages + 1):
        params: dict[str, str] = {
            "search": query,
            "per-page": str(per_page),
            "page": str(page),
        }
        if mailto:
            params["mailto"] = mailto
        if filters:
            params["filter"] = ",".join(filters)
        url = OPENALEX_BASE + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(
            url,
            headers={"User-Agent": _user_agent(mailto), "Accept": "application/json"},
        )
        payload = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                if exc.code == 429 and attempt < 2:
                    retry_after = exc.headers.get("Retry-After")
                    if retry_after and str(retry_after).isdigit():
                        delay = min(float(retry_after), 30.0)
                    else:
                        delay = float(2**attempt)
                    time.sleep(max(delay, 1.0))
                    continue
                raise
        if payload is None:
            raise RuntimeError(f"OpenAlex failed for query={query!r}")
        for work in payload.get("results") or []:
            doi = work.get("doi") or ""
            if isinstance(doi, str) and doi.startswith("https://doi.org/"):
                doi = doi.removeprefix("https://doi.org/")
            oa = (work.get("open_access") or {}).get("oa_url")
            primary = (work.get("primary_location") or {}).get("landing_page_url")
            year = work.get("publication_year")
            results.append(
                {
                    "title": work.get("display_name"),
                    "doi": doi or None,
                    "year": year,
                    "oa_url": oa or primary,
                    "openalex_id": work.get("id"),
                    "cited_by_count": work.get("cited_by_count"),
                    "query": query,
                }
            )
        time.sleep(0.1)
        if not payload.get("results"):
            break
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenAlex search for researchskills")
    parser.add_argument("--query", action="append", default=[], help="Search string (repeatable)")
    parser.add_argument("--protocol", type=Path, help="PROTOCOL.md path")
    parser.add_argument("--mailto", default=DEFAULT_MAILTO)
    parser.add_argument("--per-page", type=int, default=25)
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    queries: list[str] = list(args.query)
    from_date = to_date = None
    if args.protocol:
        snap = _parse_yaml_frontmatter(args.protocol.read_text(encoding="utf-8"))
        queries = search_queries_from_snapshot(snap)
        dr = snap.get("date_range") or {}
        from_date = dr.get("from")
        to_date = dr.get("to")
    if not queries:
        parser.error("provide --query or --protocol")

    seen: set[str] = set()
    all_rows: list[dict[str, Any]] = []
    for q in queries:
        for row in openalex_search(
            q,
            mailto=args.mailto or "",
            per_page=args.per_page,
            max_pages=args.max_pages,
            from_date=from_date,
            to_date=to_date,
        ):
            key = (row.get("doi") or row.get("openalex_id") or row.get("title") or "").lower()
            if key in seen:
                continue
            seen.add(key)
            all_rows.append(row)

    if args.json:
        json.dump(all_rows, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        for row in all_rows:
            print(f"{row.get('year')}\t{row.get('doi')}\t{row.get('title')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
