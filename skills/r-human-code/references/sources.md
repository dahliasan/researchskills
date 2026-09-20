# Source context

This file records provenance and interpretation; it is not a second rulebook.

## Clean Code / Robert C. Martin

Retained ideas: reveal intent, small/cohesive responsibilities, one level of
abstraction, meaningful names, explicit decisions, controlled complexity, testing, and
deterministic quality feedback. Adapt these values to R rather than copying Java-style
object architecture or enforcing tiny functions mechanically.

For agentic coding, prefer deterministic checks for properties that can be measured.
Keep prompting/skills focused on judgment that tools cannot reliably decide.

## R4DS

Use descriptive function/argument names and treat repetition as a signal to reconsider
structure. Tidy-evaluation syntax is justified only when the abstraction itself is
justified.

## Scientific R

Interactive inspection is a legitimate execution mode. Whole-script fresh-session
execution remains valuable for reproducibility. Neither requirement implies that every
analysis should become a CLI or package.
