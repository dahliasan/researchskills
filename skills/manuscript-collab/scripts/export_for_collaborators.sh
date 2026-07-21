#!/usr/bin/env bash
# Snapshot full markdown, strip agent CriticMarkup, convert to DOCX.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
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
    --archive-dir)
      ARCHIVE_DIR="$2"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --ensure-cli)
      ENSURE_CLI=1
      shift
      ;;
    *)
      usage
      ;;
  esac
done

[[ -f "$SOURCE" ]] || { echo "Missing source: $SOURCE" >&2; exit 1; }
[[ "$SOURCE" == *.md ]] || { echo "Source must be .md" >&2; exit 1; }

if ! command -v manuscript-markdown >/dev/null 2>&1; then
  if [[ "$ENSURE_CLI" -eq 1 ]]; then
    bash "$ENSURE"
    # ensure may install to ~/bin; refresh PATH for this process
    export PATH="${MANUSCRIPT_MARKDOWN_BIN_DIR:-$HOME/bin}:$PATH"
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
  probe="$src_dir"
  ARCHIVE_DIR=""
  for _ in 1 2 3 4 5 6 7 8; do
    if [[ -d "$probe/docs/manuscript/_archive" ]]; then
      ARCHIVE_DIR="$probe/docs/manuscript/_archive"
      break
    fi
    parent="$(dirname "$probe")"
    [[ "$parent" == "$probe" ]] && break
    probe="$parent"
  done
  if [[ -z "$ARCHIVE_DIR" ]]; then
    ARCHIVE_DIR="$src_dir/_archive"
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
