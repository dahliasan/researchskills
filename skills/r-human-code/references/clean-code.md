# Clean-code reasoning adapted to R

Read only when a design choice is ambiguous.

The aim is to preserve durable clean-code values without copying application-oriented
Java habits into scientific R.

## Meaningful extraction

"Do one thing" is a test of conceptual coherence, not a demand for tiny functions.
A multi-expression dplyr pipeline can still be one analytical operation. Extract a
function when the extracted block has a meaningful domain name or creates a useful
abstraction boundary. Do not create function confetti.

## One level of abstraction

A calculation function should not casually alternate between domain decisions,
filename construction, directory creation, model fitting, plotting, and export. When
those concerns truly belong together, make the orchestration role explicit.

## Single responsibility

Group things that change for the same reason and separate things that change for
different reasons. Scientific model settings change for scientific reasons; CLI
parsing changes because execution infrastructure changes. Do not tangle them without a
real need.

## Conditions

Branches are normal. Complexity comes from decisions the reader cannot name, deeply
nested pathways, or the same decision repeated throughout the codebase. Prefer named
scientific predicates. Repeated category logic may be data rather than polymorphism.
When nesting obscures the main path, an early return or guard clause can expose that path
more clearly. This is an option, not a mandatory rewrite pattern.

## R return style

Ordinary R functions usually read cleanly when the final expression is returned
implicitly. Reserve explicit `return()` mainly for early exits or cases where it makes
control flow clearer. Do not rewrite existing functions solely to remove harmless
`return()` calls.

## Match structure to context

An analysis script, reusable helper/package code, and a pipeline entry point solve
different problems. Interactive top-level code and inspectable intermediates are normal
in analysis scripts. Reusable package/helper code should expose stable interfaces and
minimise hidden state. Pipeline files should make orchestration obvious and delegate
substantial reusable computation when that improves dependency clarity or testing.

## Human values, agent mechanics

Do not force agents to imitate every human coding discipline. Enforce what can be
checked deterministically with project tooling, and use this skill for values that
need judgment: intent, cohesion, useful abstraction, scientific meaning, and readable
interfaces.

R differs from typical application languages because analysis scripts are commonly
read and executed interactively. Preserve that mode while requiring clean fresh-session
execution where practical. Automation should adapt to the analysis unless the project
genuinely needs an external interface.
