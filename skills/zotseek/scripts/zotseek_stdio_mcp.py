#!/usr/bin/env python3
"""Stdio MCP bridge for ZotSeek (Cursor-compatible).

ZotSeek's HTTP MCP is Streamable HTTP + POST-only / stateless. Cursor then
opens a GET SSE stream on the same URL, Zotero returns 400 "Endpoint does not
support method", and Cursor marks the server failed.

This process speaks MCP over stdio and calls ZotSeek's REST API on localhost
(or an SSH tunnel to Dahlia): GET /zotseek/search|similar|stats.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE = "http://127.0.0.1:23119"
TIMEOUT = 120


def _http_get(path: str, params: dict[str, Any] | None = None) -> Any:
    qs = urllib.parse.urlencode({k: v for k, v in (params or {}).items() if v is not None})
    url = f"{BASE}{path}" + (f"?{qs}" if qs else "")
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            err = json.loads(body)
            msg = err.get("error") or body
        except json.JSONDecodeError:
            msg = body or str(e)
        raise RuntimeError(f"ZotSeek HTTP {e.code}: {msg}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Cannot reach ZotSeek at {BASE} ({e.reason}). "
            "Is Zotero running with AI Agent Access on? "
            "If Zotero is on Dahlia: ssh -fN dahlia-zotseek"
        ) from e


def _tool_result(payload: Any) -> dict[str, Any]:
    text = payload if isinstance(payload, str) else json.dumps(payload, indent=2)
    return {"content": [{"type": "text", "text": text}]}


TOOLS = [
    {
        "name": "search",
        "description": (
            "Semantic search over the user's Zotero library using ZotSeek's local "
            "embeddings. Returns papers ranked by relevance, with matched text "
            "excerpts and page numbers where available. Each result carries "
            "zotero:// deep links (and *Http variants)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural-language search query"},
                "max_results": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 10,
                },
                "mode": {
                    "type": "string",
                    "enum": ["hybrid", "semantic", "keyword"],
                    "default": "hybrid",
                },
                "min_similarity": {"type": "number", "minimum": 0, "maximum": 1},
                "granularity": {
                    "type": "string",
                    "enum": ["papers", "passages"],
                    "default": "papers",
                },
                "library_key": {
                    "type": "string",
                    "description": "'user', 'group:<id>', or omit for all indexed libraries",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "find_similar",
        "description": (
            "Find papers similar to a known library item by Zotero item key "
            "(8 characters)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "item_key": {"type": "string"},
                "library_key": {"type": "string", "default": "user"},
                "max_results": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 10,
                },
            },
            "required": ["item_key"],
        },
    },
    {
        "name": "index_status",
        "description": (
            "Report ZotSeek index status: indexed papers, chunks, model, lastIndexed."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def call_tool(name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
    args = arguments or {}
    if name == "index_status":
        return _tool_result(_http_get("/zotseek/stats"))
    if name == "search":
        params = {
            "q": args["query"],
            "topK": args.get("max_results", 10),
            "mode": args.get("mode", "hybrid"),
            "granularity": args.get("granularity", "papers"),
        }
        if "min_similarity" in args:
            params["minSimilarity"] = args["min_similarity"]
        if args.get("library_key"):
            params["libraryKey"] = args["library_key"]
        return _tool_result(_http_get("/zotseek/search", params))
    if name == "find_similar":
        params = {
            "itemKey": args["item_key"],
            "libraryKey": args.get("library_key", "user"),
            "topK": args.get("max_results", 10),
        }
        return _tool_result(_http_get("/zotseek/similar", params))
    raise RuntimeError(f"Unknown tool: {name}")


def handle(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method")
    msg_id = msg.get("id")
    params = msg.get("params") or {}

    # Notifications have no id and no response
    if msg_id is None and method and method.startswith("notifications/"):
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "zotseek-stdio", "version": "1.0.0"},
            },
        }

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        name = params.get("name")
        try:
            result = call_tool(name, params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": msg_id, "result": result}
        except Exception as e:  # noqa: BLE001 — surface to MCP client
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": str(e)}],
                    "isError": True,
                },
            }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    # Ignore unknown notifications; error on unknown requests
    if msg_id is None:
        return None
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
