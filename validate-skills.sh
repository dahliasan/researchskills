#!/usr/bin/env bash
# Validate researchskills pack structure.
set -euo pipefail
root="$(cd "$(dirname "$0")" && pwd)"
cd "$root"
fail=0

required_skills=(
  researchskills
  manuscript-writing
  scientific-writing
  literature-review
  discover-papers
  protocol
  find-pdf
  zotero
  zotseek
  zotero-local-library
  research-project-ops
)

echo "== frontmatter + required skills =="
for name in "${required_skills[@]}"; do
  skill="skills/$name/SKILL.md"
  if [[ ! -f "$skill" ]]; then
    echo "FAIL: missing $skill"
    fail=1
    continue
  fi
  if ! grep -qE '^name:' "$skill"; then
    echo "FAIL: $name missing name:"
    fail=1
  fi
  if ! grep -qE '^description:' "$skill"; then
    echo "FAIL: $name missing description:"
    fail=1
  fi
  declared=$(grep -E '^name:' "$skill" | head -1 | sed 's/^name:[[:space:]]*//' | tr -d '"' | tr '[:upper:]' '[:lower:]')
  if [[ "$declared" != "$name" ]]; then
    echo "FAIL: $name folder vs frontmatter name='$declared'"
    fail=1
  fi
done

echo "== required scripts =="
for path in \
  skills/discover-papers/scripts/openalex_search.py \
  skills/manuscript-writing/validator.py \
  skills/zotero/scripts/zotero.py \
  skills/zotero-local-library/query_collection.py \
  skills/zotseek/scripts/zotseek_stdio_mcp.py
do
  if [[ ! -f "$path" ]]; then
    echo "FAIL: missing $path"
    fail=1
  fi
done

echo "== plugin JSON =="
python3 - <<'PY'
import json
from pathlib import Path
for rel in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
    json.loads(Path(rel).read_text())
    print(f"OK JSON {rel}")
PY

echo "== scrub: no personal machine paths in skill runtime files =="
hits=$(grep -RInE 'Dennis|Dahlia|/Users/dennis|dahlias-skills|dahlia-zotseek' \
  skills/*/SKILL.md \
  skills/*/reference.md \
  skills/*/*.py \
  skills/*/scripts/*.py \
  2>/dev/null || true)
if [[ -n "$hits" ]]; then
  echo "$hits"
  echo "FAIL: personal/private path markers found"
  fail=1
else
  echo "OK scrub"
fi

echo "== offline tests =="
python3 tests/test_openalex_offline.py
python3 tests/test_validator_fixture.py

if [[ "$fail" -ne 0 ]]; then
  echo "FAILED"
  exit 1
fi
echo "ALL OK"
