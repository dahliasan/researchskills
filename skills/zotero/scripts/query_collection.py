#!/usr/bin/env python3
"""
List Zotero items in a collection by name.

Default: Zotero 7+ local HTTP API (Web API v3 on localhost). Requires Zotero
running with local API access enabled.

Fallback: --backend sqlite reads zotero.sqlite (+ storage/) for offline / Zotero 6.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_API_BASE = "http://127.0.0.1:23119"
API_USER_PREFIX = "/api/users/0"


def default_zotero_data_dir() -> Path:
    env = os.environ.get("ZOTERO_DATA_DIR")
    if env:
        return Path(env).expanduser()
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Zotero"
    if sys.platform == "win32":
        return Path(os.environ.get("USERPROFILE", str(home))) / "Zotero"
    return home / "Zotero"


def api_root_url(api_base: str) -> str:
    base = api_base.rstrip("/")
    return base + API_USER_PREFIX


def parse_next_link(link_header: str | None) -> str | None:
    if not link_header:
        return None
    for segment in link_header.split(","):
        segment = segment.strip()
        if 'rel="next"' not in segment and "rel='next'" not in segment and "rel=next" not in segment:
            continue
        m = re.search(r"<([^>]+)>", segment)
        if m:
            return m.group(1).strip()
    return None


def api_headers() -> dict[str, str]:
    return {
        "Zotero-API-Version": "3",
        "Accept": "application/json",
        "User-Agent": "zotero-query-collection/2 (stdlib urllib)",
    }


def api_get_json(url: str, timeout: float = 60.0) -> tuple[list | dict, str | None]:
    req = urllib.request.Request(url, headers=api_headers())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            link = resp.headers.get("Link")
            if not raw.strip():
                return [], link
            data = json.loads(raw)
            return data, link
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {e.code} from Zotero local API ({url}). "
            f"Ensure Zotero is running and local app access is enabled (Settings → Advanced). "
            f"Body: {detail[:500]}"
        ) from e
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Could not reach Zotero at {url!r}: {e.reason!r}. "
            "Start Zotero 7+ and enable local API access, or use --backend sqlite."
        ) from e


def api_fetch_all_pages(first_url: str, timeout: float = 60.0) -> list:
    out: list = []
    url: str | None = first_url
    while url:
        chunk, link_header = api_get_json(url, timeout=timeout)
        if isinstance(chunk, list):
            out.extend(chunk)
        else:
            out.append(chunk)
        url = parse_next_link(link_header)
    return out


def normalize_link_mode(link_mode: str | int | None) -> tuple[str | None, bool, bool]:
    """Returns (label, is_linked_file, use_zotero_storage_dir).

    ``use_zotero_storage_dir`` is True for imported_file and imported_url. URL-imported
    attachments often still have a PDF (or snapshot) under ``storage/{attachmentKey}/``;
    Zotero opens those like normal files even when ``linkMode`` is not imported_file.
    """
    if link_mode is None:
        return None, False, False
    if isinstance(link_mode, int):
        # Zotero DB: 0 imported_file, 1 imported_url, 2 linked_file, 3 linked_url
        if link_mode == 2:
            return "linked_file", True, False
        if link_mode == 0:
            return "imported_file", False, True
        if link_mode == 1:
            return "imported_url", False, True
        return None, False, False
    s = str(link_mode).strip()
    if s == "linked_file":
        return s, True, False
    if s in ("imported_file", "imported_url"):
        return s, False, True
    return s, False, False


def resolve_attachment_path(
    zotero_dir: Path,
    attachment_key: str,
    path: str | None,
    link_mode: str | int | None,
) -> str | None:
    if not path:
        path = None
    p = (path or "").strip()
    if not p:
        p = None
    _, is_linked, use_storage = normalize_link_mode(link_mode)

    if is_linked and p:
        cand = Path(p)
        if cand.is_file():
            return str(cand.resolve())
        alt = zotero_dir / p
        if alt.is_file():
            return str(alt.resolve())
        return None

    if p and os.path.isabs(p) and Path(p).is_file():
        return str(Path(p).resolve())

    if use_storage:
        storage = zotero_dir / "storage" / attachment_key
        if storage.is_dir() and p:
            f = storage / p
            if f.is_file():
                return str(f.resolve())
        if storage.is_dir():
            pdfs = sorted(storage.glob("*.pdf"))
            if len(pdfs) == 1:
                return str(pdfs[0].resolve())
    return None


def collection_name_from_api(obj: dict) -> str:
    data = obj.get("data") or {}
    return str(data.get("name") or "")


def collection_key_from_api(obj: dict) -> str:
    return str(obj.get("key") or "")


def match_collections_by_name(collections: list, query: str) -> list[dict]:
    q = query.strip()
    if not q:
        return []
    exact = [c for c in collections if collection_name_from_api(c).lower() == q.lower()]
    if exact:
        return exact
    qlow = q.lower()
    return [c for c in collections if qlow in collection_name_from_api(c).lower()]


def item_data_title(item: dict) -> str:
    data = item.get("data") or {}
    return str(data.get("title") or "(no title)")


def item_data_type(item: dict) -> str:
    data = item.get("data") or {}
    return str(data.get("itemType") or "")


def attachments_from_api_children(
    zotero_dir: Path,
    children: list,
) -> list[dict]:
    out: list[dict] = []
    for ch in children:
        if item_data_type(ch) != "attachment":
            continue
        data = ch.get("data") or {}
        key = str(ch.get("key") or "")
        path_str = data.get("path")
        path_in_db = str(path_str) if path_str is not None else None
        lm = data.get("linkMode")
        ct = data.get("contentType")
        ct_str = str(ct) if ct is not None else None
        resolved = resolve_attachment_path(zotero_dir, key, path_in_db, lm)
        out.append(
            {
                "attachmentKey": key,
                "contentType": ct_str,
                "pathInDb": path_in_db,
                "linkMode": lm,
                "resolvedPath": resolved,
            }
        )
    return out


def run_backend_api(
    collection_query: str,
    zotero_dir: Path,
    api_base: str,
    timeout: float,
) -> dict:
    root = api_root_url(api_base)
    enc = urllib.parse.quote

    collections_url = f"{root}/collections?limit=100"
    try:
        all_collections = api_fetch_all_pages(collections_url, timeout=timeout)
    except RuntimeError:
        raise

    matched = match_collections_by_name(all_collections, collection_query)
    if not matched:
        raise LookupError(f"No collection matching: {collection_query!r}")

    matched_meta = [
        {"key": collection_key_from_api(c), "name": collection_name_from_api(c)} for c in matched
    ]
    matched_keys = {collection_key_from_api(c) for c in matched}

    items_out: list[dict] = []
    seen_keys: set[str] = set()

    for col in matched:
        ckey = collection_key_from_api(col)
        cname = collection_name_from_api(col)
        first = f"{root}/collections/{enc(ckey)}/items/top?limit=100"
        top_items = api_fetch_all_pages(first, timeout=timeout)

        for item in top_items:
            if not isinstance(item, dict):
                continue
            ikey = str(item.get("key") or "")
            if not ikey or ikey in seen_keys:
                continue
            itype = item_data_type(item)
            if itype == "attachment":
                continue

            seen_keys.add(ikey)
            title = item_data_title(item)
            version = item.get("version")

            kids_url = f"{root}/items/{enc(ikey)}/children?limit=100"
            children = api_fetch_all_pages(kids_url, timeout=timeout)
            atts = attachments_from_api_children(zotero_dir, children)
            pdfs = [a for a in atts if a.get("contentType") == "application/pdf"]

            items_out.append(
                {
                    "collectionKey": ckey,
                    "collectionName": cname,
                    "itemKey": ikey,
                    "itemVersion": int(version) if version is not None else None,
                    "itemType": itype,
                    "title": title,
                    "attachments": atts,
                    "pdfPaths": [a["resolvedPath"] for a in pdfs if a.get("resolvedPath")],
                }
            )

    return {
        "backend": "api",
        "zoteroApiBase": api_base.rstrip("/"),
        "zoteroApiRoot": root,
        "zoteroDir": str(zotero_dir.resolve()),
        "query": collection_query,
        "matchedCollections": matched_meta,
        "matchedCollectionKeys": sorted(matched_keys),
        "items": items_out,
    }


# --- SQLite backend (legacy) -------------------------------------------------

def open_zotero_db(zotero_dir: Path, use_copy: bool) -> tuple[sqlite3.Connection, Path | None]:
    db_path = zotero_dir / "zotero.sqlite"
    if not db_path.is_file():
        raise FileNotFoundError(f"Missing database: {db_path}")

    tmp: Path | None = None
    if use_copy:
        tmp = Path(tempfile.mkstemp(suffix=".sqlite", prefix="zotero_ro_")[1])
        shutil.copy2(db_path, tmp)
        conn = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
    else:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn, tmp


def cleanup_tmp(tmp: Path | None) -> None:
    if tmp and tmp.is_file():
        try:
            tmp.unlink()
        except OSError:
            pass


def get_field_id(conn: sqlite3.Connection, field_name: str) -> int | None:
    row = conn.execute(
        "SELECT fieldID FROM fields WHERE fieldName = ? COLLATE NOCASE",
        (field_name,),
    ).fetchone()
    return int(row["fieldID"]) if row else None


def resolve_collection_ids_sqlite(conn: sqlite3.Connection, name: str) -> list[int]:
    rows = conn.execute(
        """
        SELECT collectionID, collectionName
        FROM collections
        WHERE collectionName = ? COLLATE NOCASE
        ORDER BY collectionID
        """,
        (name,),
    ).fetchall()
    if rows:
        return [int(r["collectionID"]) for r in rows]
    like = f"%{name}%"
    rows = conn.execute(
        """
        SELECT collectionID, collectionName
        FROM collections
        WHERE collectionName LIKE ? COLLATE NOCASE
        ORDER BY collectionID
        """,
        (like,),
    ).fetchall()
    return [int(r["collectionID"]) for r in rows]


def item_title_sqlite(conn: sqlite3.Connection, item_id: int, title_field_id: int) -> str | None:
    row = conn.execute(
        """
        SELECT v.value
        FROM itemData d
        JOIN itemDataValues v ON d.valueID = v.valueID
        WHERE d.itemID = ? AND d.fieldID = ?
        """,
        (item_id, title_field_id),
    ).fetchone()
    return str(row["value"]) if row and row["value"] is not None else None


def item_type_name_sqlite(conn: sqlite3.Connection, item_id: int) -> str | None:
    row = conn.execute(
        """
        SELECT t.typeName
        FROM items i
        JOIN itemTypes t ON i.itemTypeID = t.itemTypeID
        WHERE i.itemID = ?
        """,
        (item_id,),
    ).fetchone()
    return str(row["typeName"]) if row else None


def attachment_columns(conn: sqlite3.Connection) -> set[str]:
    info = conn.execute("PRAGMA table_info(itemAttachments)").fetchall()
    return {str(r[1]) for r in info}


def attachments_for_parent_sqlite(
    conn: sqlite3.Connection,
    zotero_dir: Path,
    parent_item_id: int,
    cols: set[str],
) -> list[dict]:
    select = """
        SELECT ia.itemID AS attachmentItemID, ia.parentItemID, ia.path, ia.contentType,
               i.key AS attachmentKey
    """
    if "linkMode" in cols:
        select += ", ia.linkMode AS linkMode"
    select += """
        FROM itemAttachments ia
        JOIN items i ON i.itemID = ia.itemID
        WHERE ia.parentItemID = ?
    """
    rows = conn.execute(select, (parent_item_id,)).fetchall()

    out: list[dict] = []
    for r in rows:
        lm = None
        if "linkMode" in r.keys() and r["linkMode"] is not None:
            lm = int(r["linkMode"])
        key = str(r["attachmentKey"])
        raw_path = r["path"]
        path_str = str(raw_path) if raw_path is not None else None
        resolved = resolve_attachment_path(zotero_dir, key, path_str, lm)
        ct = r["contentType"]
        out.append(
            {
                "attachmentItemID": int(r["attachmentItemID"]),
                "attachmentKey": key,
                "contentType": str(ct) if ct else None,
                "pathInDb": path_str,
                "linkMode": lm,
                "resolvedPath": resolved,
            }
        )
    return out


def run_backend_sqlite(
    collection_query: str,
    zotero_dir: Path,
    use_copy: bool,
) -> dict:
    conn, tmp = open_zotero_db(zotero_dir, use_copy=use_copy)
    try:
        title_fid = get_field_id(conn, "title")
        if title_fid is None:
            raise RuntimeError("Could not find field 'title' in Zotero schema.")

        col_ids = resolve_collection_ids_sqlite(conn, collection_query.strip())
        if not col_ids:
            raise LookupError(f"No collection matching: {collection_query!r}")

        ia_cols = attachment_columns(conn)
        items_out: list[dict] = []
        seen_item: set[int] = set()

        for cid in col_ids:
            crow = conn.execute(
                "SELECT collectionName FROM collections WHERE collectionID = ?",
                (cid,),
            ).fetchone()
            cname = str(crow["collectionName"]) if crow else str(cid)

            rows = conn.execute(
                """
                SELECT ci.itemID
                FROM collectionItems ci
                WHERE ci.collectionID = ?
                ORDER BY ci.orderIndex, ci.itemID
                """,
                (cid,),
            ).fetchall()

            for r in rows:
                iid = int(r["itemID"])
                if iid in seen_item:
                    continue
                seen_item.add(iid)

                itype = item_type_name_sqlite(conn, iid) or ""
                if itype == "attachment":
                    continue

                title = item_title_sqlite(conn, iid, title_fid) or "(no title)"
                ikey_row = conn.execute("SELECT key FROM items WHERE itemID = ?", (iid,)).fetchone()
                ikey = str(ikey_row["key"]) if ikey_row else ""

                atts = attachments_for_parent_sqlite(conn, zotero_dir, iid, ia_cols)
                pdfs = [a for a in atts if a.get("contentType") == "application/pdf"]

                items_out.append(
                    {
                        "collectionID": cid,
                        "collectionName": cname,
                        "itemID": iid,
                        "itemKey": ikey,
                        "itemType": itype,
                        "title": title,
                        "attachments": atts,
                        "pdfPaths": [a["resolvedPath"] for a in pdfs if a.get("resolvedPath")],
                    }
                )

        return {
            "backend": "sqlite",
            "zoteroDir": str(zotero_dir.resolve()),
            "query": collection_query,
            "matchedCollectionIDs": col_ids,
            "items": items_out,
        }
    finally:
        conn.close()
        cleanup_tmp(tmp)


def print_text_report(payload: dict) -> None:
    backend = payload.get("backend")
    print(f"Backend: {backend}")
    if backend == "api":
        print(f"Zotero API: {payload.get('zoteroApiRoot')}")
    print(f"Zotero data dir: {payload.get('zoteroDir')}")
    if backend == "api":
        print(f"Matched collections: {payload.get('matchedCollectionKeys')}")
    else:
        print(f"Matched collection IDs: {payload.get('matchedCollectionIDs')}")

    for it in payload.get("items") or []:
        print(f"\n- {it.get('title')}")
        ik = it.get("itemKey")
        iid = it.get("itemID")
        line = f"  itemKey={ik}"
        if iid is not None:
            line += f" itemID={iid}"
        line += f" type={it.get('itemType')}"
        print(line)
        if it.get("pdfPaths"):
            for pp in it["pdfPaths"]:
                print(f"  PDF: {pp}")
        elif it.get("attachments"):
            for a in it["attachments"]:
                if a.get("resolvedPath"):
                    print(f"  file: {a['resolvedPath']}")


def main() -> int:
    p = argparse.ArgumentParser(
        description="List Zotero items in a collection by name (local API or SQLite)."
    )
    p.add_argument("collection", help='Collection name, e.g. "nz sea lion"')
    p.add_argument(
        "--backend",
        choices=("api", "sqlite"),
        default="api",
        help="api: Zotero 7+ local HTTP API (default). sqlite: read zotero.sqlite offline.",
    )
    p.add_argument(
        "--api-base",
        default=os.environ.get("ZOTERO_LOCAL_API_BASE", DEFAULT_API_BASE),
        help=f"Local Zotero base URL (default: {DEFAULT_API_BASE} or ZOTERO_LOCAL_API_BASE)",
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="HTTP timeout seconds for API backend (default: 60)",
    )
    p.add_argument(
        "--zotero-dir",
        type=Path,
        default=None,
        help="Zotero data directory for resolving files / sqlite (default: ~/Zotero or ZOTERO_DATA_DIR)",
    )
    p.add_argument(
        "--no-copy",
        action="store_true",
        help="SQLite only: open zotero.sqlite in place (fails if locked)",
    )
    p.add_argument("--json", action="store_true", help="Print JSON instead of text")
    args = p.parse_args()

    zdir = args.zotero_dir or default_zotero_data_dir()

    try:
        if args.backend == "api":
            payload = run_backend_api(args.collection, zdir, args.api_base, args.timeout)
        else:
            payload = run_backend_sqlite(args.collection, zdir, use_copy=not args.no_copy)
    except LookupError as e:
        print(str(e), file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 2
    except sqlite3.OperationalError as e:
        print(
            "Could not open database (often locked while Zotero is running). "
            "Omit --no-copy to use a temp copy, or use --backend api.\n"
            f"Error: {e}",
            file=sys.stderr,
        )
        return 2
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print_text_report(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
