#!/usr/bin/env bash
# Symlink researchskills into all harness skill dirs.
# Edits in this clone are live for every harness that follows the symlink.
#
# Usage:
#   ./scripts/link-global.sh
#   DRY_RUN=1 ./scripts/link-global.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${REPO_ROOT}/skills"
SET_FILE="${SKILLS_DIR}/sets/global.txt"
DRY_RUN="${DRY_RUN:-0}"

DESTS=(
  "${HOME}/.agents/skills"
  "${HOME}/.cursor/skills"
  "${HOME}/.claude/skills"
  "${HOME}/.codex/skills"
)

[[ -f "$SET_FILE" ]] || { echo "error: missing ${SET_FILE}" >&2; exit 1; }

skills=()
while IFS= read -r line; do
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  skills+=("$line")
done <"$SET_FILE"

[[ "${#skills[@]}" -gt 0 ]] || { echo "error: no skills in ${SET_FILE}" >&2; exit 1; }

for skill in "${skills[@]}"; do
  [[ -f "${SKILLS_DIR}/${skill}/SKILL.md" ]] || {
    echo "error: missing ${SKILLS_DIR}/${skill}/SKILL.md" >&2
    exit 1
  }
done

link_skill() {
  local skill="$1"
  local dest_root="$2"
  local src="${SKILLS_DIR}/${skill}"
  local dest="${dest_root}/${skill}"

  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[DRY_RUN] ln -sfn ${src} -> ${dest}"
    return
  fi
  mkdir -p "$dest_root"
  # Replace copied dirs / stale links with a live symlink to this clone
  if [[ -e "$dest" || -L "$dest" ]]; then
    rm -rf "$dest"
  fi
  ln -sfn "$src" "$dest"
}

for dest_root in "${DESTS[@]}"; do
  for skill in "${skills[@]}"; do
    link_skill "$skill" "$dest_root"
  done
  # Drop stale researchskills links no longer in global.txt (e.g. removed skills)
  if [[ "$DRY_RUN" != "1" && -d "$dest_root" ]]; then
    for link in "$dest_root"/*; do
      [[ -L "$link" ]] || continue
      target="$(readlink "$link" || true)"
      case "$target" in
        "${SKILLS_DIR}/"*)
          base="$(basename "$link")"
          keep=0
          for skill in "${skills[@]}"; do
            [[ "$base" == "$skill" ]] && keep=1 && break
          done
          if [[ "$keep" -eq 0 ]]; then
            rm -f "$link"
            echo "removed stale ${link}"
          fi
          ;;
      esac
    done
  fi
done

if [[ "$DRY_RUN" == "1" ]]; then
  echo "[DRY_RUN] would link ${#skills[@]} skills → ${DESTS[*]}"
else
  echo "Linked ${#skills[@]} researchskills → ${DESTS[*]}"
  echo "Edit files under ${SKILLS_DIR}/; harnesses pick up changes immediately."
fi
