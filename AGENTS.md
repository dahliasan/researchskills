# AGENTS.md

Operating notes for agents working in **researchskills**.

## Non-negotiables

1. Skills are documentation-first; do not vendor external literature-pipeline engines, anulib, or scihub **engines** into this repo. The in-repo paper-card schema under `schemas/` is owned here (`researchskills.extraction.v1`).
2. Do not add overlapping prose twins. `manuscript-writing` is the manuscript prose and audit source of truth.
3. Default MD↔DOCX converter is `manuscript-markdown` (CLI/extension). Do not use pandoc for manuscript Word roundtrip unless the user opts in after an install/compare flag. `manuscript-markdown` does not draft prose.
4. `discover-papers` must support quick mode without PROTOCOL.md.
5. `protocol` is soft-hidden but must remain a real, independently invocable skill.
6. Scrub personal paths, credentials, project data, and private conventions before committing skill text.
7. Treat validators as guardrails. Do not encode context-dependent style preferences as universal scientific blockers.
8. Do not import demoted Research Harness generics (`academic-writing`, `citation-management`, stats dumps, community `peer-review`) from dahlias `research-harness-optional.txt`. Those stay out of this pack.

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
