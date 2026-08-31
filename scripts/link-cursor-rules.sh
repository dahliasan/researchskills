#!/usr/bin/env bash
# Symlink researchskills Cursor rules into ~/.cursor/rules/
#
# Usage:
#   ./scripts/link-cursor-rules.sh
#   DRY_RUN=1 ./scripts/link-cursor-rules.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RULES_DIR="${REPO_ROOT}/rules"
DEST="${HOME}/.cursor/rules"
DRY_RUN="${DRY_RUN:-0}"

[[ -d "$RULES_DIR" ]] || { echo "error: missing ${RULES_DIR}" >&2; exit 1; }

shopt -s nullglob
rules=("${RULES_DIR}"/*.mdc)
[[ "${#rules[@]}" -gt 0 ]] || { echo "no .mdc files in ${RULES_DIR}"; exit 0; }

mkdir -p "$DEST"

for src in "${rules[@]}"; do
  name="$(basename "$src")"
  target="${DEST}/${name}"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[DRY_RUN] ln -sfn ${src} -> ${target}"
  else
    ln -sfn "$src" "$target"
    echo "linked ${target}"
  fi
done
