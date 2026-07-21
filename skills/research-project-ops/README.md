# research-project-ops

An Agent Skill for scaffolding, auditing, reorganizing, maintaining, handing off, and preparing empirical research projects for manuscript writing.

## Install

Copy this directory into a skills-compatible location, for example:

```bash
.agents/skills/research-project-ops/
```

The required entry point is `SKILL.md`.

## Design

This is a router skill. It determines the project operation needed, then creates or updates only the artifacts required for that phase.

Modes:

- scaffold
- audit
- reorganize
- update
- handoff
- results-package
- manuscript-ready
- closeout

Detailed artifact templates live in `references/artifact-contracts.md`.

## Scope

The skill manages durable research-project context and traceability. It does not replace:

- domain literature review
- statistical analysis
- visualization
- manuscript drafting
- peer-review response
