# Mode: prose-audit

Audit or surgically edit manuscript prose for formulaic, inflated, generic, or AI-shaped writing while preserving scientific meaning and disciplinary tone.

Use this mode when the user asks whether text reads as AI, asks to remove AI slop, or wants a final prose-polish pass after the scientific argument and evidence are stable.

Do not use this mode to plan, draft, or substantially restructure a manuscript. Route those tasks to `outline`, `draft`, or `revise`.

## Principle

Diagnose from first principles before applying stylistic rules. Determine what the passage is trying to do, what the evidence permits, and what conventions the section requires. Treat named patterns only as possible symptoms. Edit only when wording or structure interferes with meaning, argument, evidence alignment, section fit, disciplinary tone, or readability.

## Steps

1. Identify the manuscript section, passage purpose, audience, and local journal or project style.
2. Apply evidence and conflict gates to any claim whose meaning may change.
3. Read the full audited span before marking sentence-level issues.
4. Assess in this order:
   1. **Section function** — is the passage doing the correct job for its section?
   2. **Evidence alignment** — is each claim as strong, broad, and certain as the evidence allows?
   3. **Argument economy** — does each paragraph add a necessary claim, interpretation, boundary, or transition?
   4. **Disciplinary tone** — does the prose resemble credible writing in the field rather than conversational, promotional, bureaucratic, or generically polished prose?
   5. **Global rhythm** — do paragraphs or sentences repeat an artificial template even when each unit is acceptable alone?
   6. **Local patterns** — inspect the diagnostic prompts below.
5. For an audit request, name and quote each material issue without rewriting the full passage.
6. For an edit request, make the minimum effective changes. Preserve strong sentences, technical terms, qualifiers that carry scientific meaning, and legitimate section conventions.
7. Re-read the edited span as a whole. Check that the revision still sounds like the same manuscript and that no edit weakened precision.

## Diagnostic prompts, not bans

For each pattern, ask whether it serves the science before changing it.

- **Formulaic contrast:** Does “not X but Y” clarify a real distinction, or manufacture emphasis?
- **Colon reveal:** Does the colon express a clear logical relation, list, definition, or label, or create artificial suspense?
- **Polished synthesis:** Does the final sentence add a necessary inference, or merely restate and package the paragraph?
- **Importance language:** Does “important”, “novel”, “critical”, “robust”, or similar wording name a demonstrated property, or substitute for one?
- **Superficial interpretation:** Do words such as “highlighting”, “underscoring”, or “reflecting” explain a mechanism or consequence, or only claim significance?
- **Weasel attribution:** Is “studies show” or “research suggests” tied to verified sources and an exact claim?
- **Abstract compression:** Are concrete organisms, processes, results, and mechanisms replaced by broad umbrella nouns?
- **Synonym cycling:** Are technical terms rotated for style rather than used consistently?
- **Hedge stacking:** Does more than one qualifier add meaning?
- **Causal inflation:** Does the verb match the design and analysis?
- **Result repetition:** Does repeated result context enable interpretation, or duplicate the Results?
- **Citation accumulation:** Does each cited example change or support the argument, or merely make the paragraph look comprehensive?
- **Artificial symmetry:** Do paragraphs repeatedly follow the same claim → evidence → synthesis → recommendation pattern without a scientific reason?
- **Generic ending:** Does the conclusion state the clearest supported answer, or end with broad importance language or “more research is needed”?

## Preserve legitimate scientific prose

Do not mechanically remove:

- passive voice where the actor is unimportant or the method is the focus
- stable repetition of the correct technical term
- cautious qualifiers that define uncertainty or scope
- contrasts that distinguish hypotheses, mechanisms, models, or interpretations
- colons used for lists, definitions, labels, hypotheses, or clear explanatory relations
- section signposting that helps the reader follow a complex argument
- paragraph synthesis that adds a necessary inference
- citations required to support a claim

## Every edit must earn its place

Change text only when the revision improves at least one of:

- scientific accuracy
- evidence alignment
- logical progression
- section fit
- clarity
- concision
- disciplinary tone
- readability

Do not rewrite merely to make prose more uniform, direct, active, or polished.

## Output

### Audit

```markdown
## Overall assessment
[Brief judgment of tone and the main pattern across the passage.]

## Findings
- [SEVERITY] **Pattern** — “quoted text”
  - Why it matters: ...
  - Required action: ...

## What to preserve
- ...
```

Use `MAJOR`, `MINOR`, or `EDITORIAL`. Use `BLOCKER` only for a scientific conflict or unsupported claim, not for style.

### Edit

1. Revised passage
2. Material unresolved scientific or evidence issues only
3. A short summary of the main edit types when useful

## Done when

The passage fits its section, claims remain evidence-aligned, disciplinary tone is preserved, global rhythm has been checked, and every edit is defensible by a stated scientific or writing purpose.