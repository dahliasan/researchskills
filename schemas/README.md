# Extraction schemas

Owned by **researchskills**. Do not require an external batch engine to extract papers.

| File | `schema_version` |
|------|------------------|
| [paper-extraction.v1.schema.json](paper-extraction.v1.schema.json) | `researchskills.extraction.v1` |
| [examples/paper-extraction.v1.example.json](examples/paper-extraction.v1.example.json) | example record |

PROTOCOL.md sets:

```yaml
extraction:
  schema: researchskills.extraction.v1
```

Field shape matches the former external `*.extraction.v3` paper card so old JSON
can be migrated by renaming `schema_version` (and `file.extractor_version` if
desired). New extracts must use `researchskills.extraction.v1`.

**Prompt:** render from PROTOCOL with

```bash
python skills/literature-review/scripts/render_extraction_prompt.py --protocol PROTOCOL.md
```

**Validate:**

```bash
python skills/literature-review/scripts/validate_extraction.py card.json
```
