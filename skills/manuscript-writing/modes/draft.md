# Mode: draft

## Steps

1. Apply evidence, readiness, and conflict gates (`SKILL.md`). Stop if
   `NOT READY`.
2. Verify or state the central contribution for the section in scope.
3. If planning gate applies (new manuscript, new complete section, major
   structural revision, or Intro/Discussion with several linked claims),
   load [outline.md](outline.md) artifacts or build them first.
4. Load the target section contract from [reference.md](../reference.md)
   (Introduction, Methods, Results, Discussion, Abstract, or Captions). For a
   separate Conclusion section or concluding Discussion paragraph, also load
   [conclusion.md](../conclusion.md).
5. Load [scaffolding.md](../scaffolding.md) and scan draft for scaffolding
   leaks.
6. Draft in the section role only — no Discussion mechanisms in Results; no
   result reporting in Introduction.
7. Run deterministic validator when a full section draft is returned.

**Done when** finished prose exists for the requested scope, every material
number or citation is gated, scaffolding is absent from prose, and `[TBC]` /
conflicts are listed separately (not buried in the section).

## Output

1. Finished text
2. Material `[TBC]` items or scientific conflicts separately
3. No long explanation of routine choices