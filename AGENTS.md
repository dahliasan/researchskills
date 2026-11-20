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
python3 -m unittest tests/test_validator_fixture.py tests/test_track_edit.py
```

## Corrected rules

When the user corrects the same manuscript mistake twice, fix it at the
highest level that works (tool, check, test) and add a row here. Validator
checks are warnings, not blockers (non-negotiable 7). Each check has a test
built from a sentence the user corrected in a real draft.

| Rule | Enforced by |
|------|-------------|
| Tracked changes come from one shared tool, word by word, never a new OOXML script | `manuscript-writing/scripts/track_edit.py`; `tests/test_track_edit.py` |
| Live citation fields are never silently turned into plain text | `track_edit.py` refuses unmatched citations; `tests/test_track_edit.py` |
| Rejecting an edit run restores the input exactly | `track_edit.py` self-check before writing |
| Paragraphs open with their point, not an announcement of the topic | validator `announcing_opener` |
| No invented gaps ("managers lack…") without a source | validator `unsupported_gap` |
| Say each point once: no repeated citation of the same claim, no restated thresholds | validator `repeated_citation`, `repeated_value` |
| Discussion in proportion to the Introduction | validator `discussion_length` |
| The author's avoided words stay out | validator `--avoid-words` reading the private voice profile |
| Verify facts with tools before guessing or asking | `manuscript-writing` rule only (judgment) |
| Limitations pass the materiality test; no minor caveats | `manuscript-writing` rule only (judgment) |
| Every detail serves the argument (relevance) | `manuscript-writing` rule only (judgment) |
| Neutral register at the paper's real size; no forced tension | `manuscript-writing` rule only (judgment) |
| A Claude model writes the Word file; other orchestrators delegate that step | `word-documents.md` (rule only) |
