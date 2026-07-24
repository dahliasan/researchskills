#!/usr/bin/env python3
"""Render the paper-card extraction prompt from PROTOCOL.md YAML + prose.

Stdlib only. PROTOCOL YAML is a small indentation subset (scalars, maps, lists).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)
SECTION = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

DEFAULT_TEMPLATE = (
    Path(__file__).resolve().parents[1] / "references" / "extraction-prompt.md"
)


def _parse_scalar(raw: str) -> Any:
    text = raw.strip()
    if text == "" or text == "~" or text.lower() == "null":
        return None
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part) for part in inner.split(",")]
    try:
        if re.fullmatch(r"-?\d+", text):
            return int(text)
    except ValueError:
        pass
    return text


def parse_simple_yaml(text: str) -> Any:
    """Parse indentation-based YAML maps/lists used in PROTOCOL front matter."""
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.lstrip(" ")))

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(lines):
            return None, index
        if lines[index][1].startswith("- "):
            return parse_list(index, indent)
        return parse_map(index, indent)

    def parse_map(index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(lines):
            line_indent, content = lines[index]
            if line_indent < indent:
                break
            if line_indent > indent:
                raise ValueError(f"Unexpected indent at: {content}")
            if content.startswith("- "):
                break
            if ":" not in content:
                raise ValueError(f"Expected key: value at: {content}")
            key, _, rest = content.partition(":")
            key = key.strip()
            rest = rest.strip()
            index += 1
            if rest:
                result[key] = _parse_scalar(rest)
                continue
            if index >= len(lines) or lines[index][0] <= indent:
                result[key] = None
                continue
            child_indent = lines[index][0]
            if child_indent <= indent:
                result[key] = None
                continue
            value, index = parse_block(index, child_indent)
            result[key] = value
        return result, index

    def parse_list(index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(lines):
            line_indent, content = lines[index]
            if line_indent < indent:
                break
            if line_indent > indent:
                raise ValueError(f"Unexpected indent in list at: {content}")
            if not content.startswith("- "):
                break
            item = content[2:].strip()
            index += 1
            if item == "" or (":" in item and not item.startswith("{")):
                # `-` alone → nested map, or `- key: value` start of map item
                if item == "":
                    if index >= len(lines) or lines[index][0] <= indent:
                        result.append(None)
                        continue
                    value, index = parse_block(index, lines[index][0])
                    result.append(value)
                    continue
                # Inline map start: "- name: foo"
                key, _, rest = item.partition(":")
                mapping: dict[str, Any] = {key.strip(): _parse_scalar(rest.strip())}
                while index < len(lines) and lines[index][0] > indent:
                    child_indent, child = lines[index]
                    if child.startswith("- "):
                        break
                    if child_indent <= indent:
                        break
                    if ":" not in child:
                        break
                    # Same map continues at greater indent
                    if child_indent == indent + 2 or child_indent > indent:
                        ck, _, cv = child.partition(":")
                        cv = cv.strip()
                        index += 1
                        if cv:
                            mapping[ck.strip()] = _parse_scalar(cv)
                        else:
                            if index < len(lines) and lines[index][0] > child_indent:
                                nested, index = parse_block(index, lines[index][0])
                                mapping[ck.strip()] = nested
                            else:
                                mapping[ck.strip()] = None
                        continue
                    break
                result.append(mapping)
            else:
                result.append(_parse_scalar(item))
        return result, index

    if not lines:
        return {}
    value, index = parse_block(0, lines[0][0])
    if index != len(lines):
        raise ValueError(f"Unconsumed YAML near: {lines[index][1]}")
    return value


def parse_protocol(text: str) -> tuple[dict[str, Any], dict[str, str]]:
    match = FRONT_MATTER.match(text)
    if not match:
        raise ValueError("PROTOCOL.md must start with YAML front matter (--- ... ---)")
    data = parse_simple_yaml(match.group(1)) or {}
    if not isinstance(data, dict):
        raise ValueError("PROTOCOL YAML front matter must be a mapping")
    body = match.group(2) or ""
    sections: dict[str, str] = {}
    parts = SECTION.split(body)
    if len(parts) >= 3:
        for i in range(1, len(parts), 2):
            heading = parts[i].strip().lower()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            sections[heading] = content
    return data, sections


def _bullets(items: Any) -> str:
    if not items:
        return "  (none)"
    if isinstance(items, str):
        return f"- {items}"
    lines = []
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines) if lines else "  (none)"


def _question_block(question: Any, framework: str) -> str:
    if not isinstance(question, dict) or not question:
        return "  (not set)"
    lines = []
    for key, value in question.items():
        lines.append(f"  - {key}: {value if value not in (None, '') else '(empty)'}")
    return "\n".join(lines) + f"\n  (framework: {framework or 'unspecified'})"


def _date_range(dr: Any) -> str:
    if not isinstance(dr, dict):
        return "(not set)"
    return f"{dr.get('from', '?')} → {dr.get('to', '?')}"


def _extra_fields_block(extra: Any) -> str:
    if not extra:
        return (
            "(none declared — omit `protocol_extra` or use `{}`)\n"
            "Declare fields in PROTOCOL YAML under extraction.extra_fields, e.g.:\n"
            "  extra_fields:\n"
            "    - name: weather_exposure\n"
            "      type: string\n"
            "      description: How weather/climate exposure was measured or discussed."
        )
    lines = []
    if isinstance(extra, list):
        for item in extra:
            if isinstance(item, str):
                lines.append(f"- `{item}` (string or null; meaning from field name)")
            elif isinstance(item, dict):
                name = item.get("name") or item.get("key") or "field"
                typ = item.get("type") or "string"
                desc = item.get("description") or item.get("prompt") or ""
                lines.append(f"- `{name}` ({typ}): {desc}".rstrip())
            else:
                lines.append(f"- {item}")
    elif isinstance(extra, dict):
        for name, spec in extra.items():
            if isinstance(spec, dict):
                typ = spec.get("type") or "string"
                desc = spec.get("description") or ""
                lines.append(f"- `{name}` ({typ}): {desc}".rstrip())
            else:
                lines.append(f"- `{name}`: {spec}")
    else:
        lines.append(str(extra))
    return "\n".join(lines)


def render(template: str, protocol: dict[str, Any], sections: dict[str, str]) -> str:
    question = protocol.get("question") or {}
    eligibility = protocol.get("eligibility") or {}
    extraction = protocol.get("extraction") or {}
    extra = extraction.get("extra_fields") if isinstance(extraction, dict) else None

    mapping = {
        "review_name": str(protocol.get("name") or "(unnamed)"),
        "review_type": str(protocol.get("review_type") or "(unspecified)"),
        "question_framework": str(protocol.get("question_framework") or ""),
        "question_block": _question_block(
            question, str(protocol.get("question_framework") or "")
        ),
        "date_range": _date_range(protocol.get("date_range")),
        "languages": ", ".join(protocol.get("languages") or []) or "(not set)",
        "include_block": _bullets(
            eligibility.get("include") if isinstance(eligibility, dict) else None
        ),
        "exclude_block": _bullets(
            eligibility.get("exclude") if isinstance(eligibility, dict) else None
        ),
        "overview_block": sections.get("overview") or "(none)",
        "question_prose_block": sections.get("question") or "(none)",
        "extra_fields_block": _extra_fields_block(extra),
    }

    marker = re.search(r"^##\s+System prompt[^\n]*\n+", template, re.MULTILINE)
    if marker:
        template = template[marker.end() :].strip() + "\n"
        if template.startswith("---"):
            template = template.split("\n", 1)[1].lstrip() if "\n" in template else ""

    out = template
    for key, value in mapping.items():
        out = out.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{[a-z_]+\}\}", out)
    if leftover:
        raise ValueError(f"Unreplaced template placeholders: {sorted(set(leftover))}")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", "-p", type=Path, required=True)
    parser.add_argument(
        "--template",
        "-t",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Prompt template markdown (default: literature-review references)",
    )
    parser.add_argument("-o", "--output", type=Path, help="Write prompt to file")
    args = parser.parse_args(argv)

    protocol_text = args.protocol.read_text(encoding="utf-8")
    data, sections = parse_protocol(protocol_text)
    template = args.template.read_text(encoding="utf-8")
    prompt = render(template, data, sections)

    if args.output:
        args.output.write_text(prompt, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
