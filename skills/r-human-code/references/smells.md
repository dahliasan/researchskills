# Recognition examples

Use these as review prompts, not automatic violations.

| Pattern | Inspect for |
|---|---|
| `main <- function() ...; main()` in an analysis script | Application structure added without a real need |
| `commandArgs()` or a CLI with no documented Bash/HPC caller | Unnecessary execution plumbing |
| One-use wrappers around clear package calls | Function confetti |
| Many tiny helpers that force file-jumping | Abstraction making the workflow harder to read |
| Dense or deeply nested Boolean branches | A scientific decision that should be named or simplified |
| The same category `if/else` repeated in several places | Lookup/data representation or dedicated decision function |
| S3/R6 introduced only to remove branching | Java-style architecture imported without R benefit |
| Calculation function writes files unexpectedly | Hidden side effect / mixed responsibility |
| `setwd()`, `rm(list = ls())`, restored `.RData` assumptions | Hidden session state |
| Blanket `tryCatch()` | Failures being hidden instead of understood |
| `stopifnot(file.exists(...))` / `stop()` before `read_*` / `st_read` / `rast` | Redundant: the reader already fails on a missing path |
| `if (!nrow(x)) stop(...)` or `if (nrow(x) > 0)` around required layers | Premature guard; let the next step fail or plot |
| `if ("col" %in% names(d))` for required columns | Use the column; missing names error naturally |
| `map()` nested several levels deep | Functional style obscuring control flow |
| Repeated `rbind()` in growing loops | Readability and performance problem |

## Audit smells

The audit itself can become a smell. Do not manufacture work.

| Pattern | Default classification | Reason |
|---|---|---|
| Clear code with an alternative style available | PASS | Preference alone is not a defect |
| High cyclomatic complexity warning | REVIEW | Inspect whether the branching reflects real domain logic before splitting |
| `docopt` selecting a config file for a documented shell, SLURM, or pipeline caller | PASS | It serves a real interface |
| `commandArgs()` or a CLI with no evident external caller | REVIEW | It may be generated execution plumbing |
| Parse error or deterministic checker failure | FAIL | Objective defect |
| Refactor that expands the diff beyond the identified problem | REVIEW | Adjacent cleanup increases risk without proving value |

Prefer the smallest justified change. A successful audit may result in no code changes.
