# Contributing

PRs welcome for skill clarity, safer defaults, and new non-overlapping skills.

## Rules

1. One job per skill. Prefer composition over mega-skills.
2. No personal machine paths, private emails, or lab-only secrets in skill bodies.
3. New skills need `name` + `description` frontmatter and a README table row.
4. Run `./validate-skills.sh` before opening a PR.
5. Soft-hidden skills (e.g. `protocol`) must still be agent-discoverable via description triggers.

## Skill format

```yaml
---
name: skill-name
description: When the user wants to… Triggers on "…"
metadata:
  version: 0.1.0
---
```

## Attribution

When adapting from another repo, add `references/attribution.md` with source URL, license, and what changed.
