# Install

## CLI

```bash
npx skills add dahliasan/researchskills
npx skills add dahliasan/researchskills --skill manuscript-writing discover-papers
npx skills add dahliasan/researchskills --list
```

Inside an agent session, pass the agent explicitly if needed:

```bash
npx skills add dahliasan/researchskills -a claude-code
```

## Maintainer install (live edits)

Clone once, then symlink into every harness. **Edits in the clone update immediately** (no reinstall):

```bash
git clone https://github.com/dahliasan/researchskills.git ~/Developer/researchskills
cd ~/Developer/researchskills
./scripts/link-global.sh
```

Set list: `skills/sets/global.txt`. After `git pull`, re-run `./scripts/link-global.sh` only if new skills were added (existing symlinks already track file edits).

Consumer copy install (snapshot, not live):

```bash
npx skills add dahliasan/researchskills -g -y
npx skills update
```

## Claude Code plugin

```text
/plugin marketplace add dahliasan/researchskills
/plugin install researchskills@researchskills
```

## Environment

| Variable | Purpose |
|----------|---------|
| `RESEARCHSKILLS_MAILTO` | OpenAlex polite pool identity (fallback: `OPENALEX_MAILTO`) |
| Zotero local API | Default `http://127.0.0.1:23119` — Zotero Desktop must be running |

## Optional backends

| Capability | Optional install |
|------------|------------------|
| Batch literature pipeline | [usefulpapers](https://github.com/dahliasan/usefulpapers) engine |
| Institutional PDF | `anulib` CLI (if your institution supports it) |
| Sci-Hub fallback | `scihub` CLI |
| Semantic Zotero | [introfini/ZotSeek](https://github.com/introfini/ZotSeek) plugin (`.xpi` from [Releases](https://github.com/introfini/ZotSeek/releases)) + MCP; see skill `zotseek` |
| Richer Zotero MCP (Python) | [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) — skill `zotero-mcp` for install/config; skill `zotero` prefers it when connected. **Not** a Zotero `.xpi` |

Skills degrade: HTTP OpenAlex and documented waterfall steps still work without UsefulPapers.

## Optional companion skills (external)

Keep these **upstream**; do not fork into this pack unless you need lasting
pack-specific changes (then use `references/attribution.md`).

| Capability | Install |
|------------|---------|
| Quarto authoring (`.qmd`, projects, callouts, …) | `npx skills add posit-dev/skills@quarto-authoring -g` |

`r-editor-setup` installs/checks Quarto **CLI + editor extension** only; it
does not vendor the Quarto authoring skill. After env setup, install the
companion when you write Quarto docs.

## Clone for contributors

```bash
git clone https://github.com/dahliasan/researchskills.git
cd researchskills
./validate-skills.sh
```
