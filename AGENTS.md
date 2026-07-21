# AGENTS.md

Operating notes for agents working in **researchskills**.

## Non-negotiables

1. Skills are documentation-first; do not vendor UsefulPapers, anulib, or scihub into this repo.
2. Do not add overlapping prose twins. `manuscript-writing` is the manuscript prose and audit source of truth.
3. `discover-papers` must support quick mode without PROTOCOL.md.
4. `protocol` is soft-hidden but must remain a real, independently invocable skill.
5. Scrub personal paths, credentials, project data, and private conventions before committing skill text.
6. Treat validators as guardrails. Do not encode context-dependent style preferences as universal scientific blockers.

## Layout

```text
skills/<name>/SKILL.md
docs/superpowers/specs/
docs/superpowers/plans/
.claude-plugin/
```

## Checks

```bash
./validate-skills.sh
python3 -m unittest tests/test_validator_fixture.py
```
