#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
fail=0
shopt -s nullglob
for skill in "$root"/skills/*/SKILL.md; do
  dir=$(dirname "$skill")
  name=$(basename "$dir")
  if ! grep -qE '^name:' "$skill"; then
    echo "FAIL: $name missing name: frontmatter"
    fail=1
  fi
  if ! grep -qE '^description:' "$skill"; then
    echo "FAIL: $name missing description: frontmatter"
    fail=1
  fi
done
count=$(find "$root/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
if [[ "$count" -lt 1 ]]; then
  echo "FAIL: no skills directories"
  fail=1
fi
if [[ "$fail" -ne 0 ]]; then
  exit 1
fi
echo "OK: $count skills pass frontmatter checks"
