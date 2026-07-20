# AGENTS.md

Operating notes for agents working in **researchskills**.

## Non-negotiables

1. Skills are documentation-first; do not vendor UsefulPapers, anulib, or scihub into this repo.
2. Do not add overlapping prose twins (`academic-writing`, etc.); `scientific-writing` is the SOT.
3. `discover-papers` must support quick mode without PROTOCOL.md.
4. `protocol` is soft-hidden but must remain a real, invocable skill.
5. Scrub personal paths before committing skill text.

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
```
