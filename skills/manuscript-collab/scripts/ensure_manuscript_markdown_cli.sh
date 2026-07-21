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
export PATH="$DEST_DIR:$PATH"
if ! command -v manuscript-markdown >/dev/null 2>&1; then
  echo "Installed to $out but not on PATH. Add $DEST_DIR to PATH." >&2
  exit 1
fi
manuscript-markdown --version
