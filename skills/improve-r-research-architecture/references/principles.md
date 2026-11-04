# Principles and evidence

This skill adapts Matt Pocock's architectural-review method; it is an original R-specific workflow, not a reproduction of his skill.

## Architecture review method

- Matt Pocock, *improve-codebase-architecture*. Emphasises recent hotspots, architectural friction, deep rather than shallow modules, the deletion test, concrete before/after candidates, and user selection before redesign. https://github.com/mattpocock/skills ; https://deska.dev/skills/mattpocock/skills/improve-codebase-architecture
- The choice to demand scientific-result baselines, preservation of analysis decisions, and incremental verification is this skill's adaptation, not a claim from Pocock.

## Scientific reproducibility and organisation

- The Turing Way, *Research Compendia* and *Reproducible Research*: project organisation, data/code/documentation, reproducible environments, version control. https://book.the-turing-way.org/reproducible-research/compendia/ ; https://book.the-turing-way.org/reproducible-research/reproducible-research/
- Marwick, Boettiger & Mullen (2018). *Packaging Data Analytical Work Reproducibly Using R (and Friends)*. The American Statistician 72:80–88. https://doi.org/10.1080/00031305.2017.1375986
- Posit, *RStudio Projects*: working with RStudio project directories. https://docs.posit.co/ide/user/ide/guide/code/projects.html
- `here`: robust project-relative paths. https://here.r-lib.org/
- `renv`: project-local library state and lockfile. https://rstudio.github.io/renv/

## Modularity, pipelines, and testing

- Wickham & Bryan, *R Packages (2e)*: `R/` directory convention for package functions. It is an inspiration, **not** a rule that ordinary analysis projects should become packages. https://r-pkgs.org/
- Landau, *The targets R package user manual*: dependency-tracked workflows, rerun only invalidated work, target design and side-effect guidance. https://books.ropensci.org/targets/ ; https://books.ropensci.org/targets/targets.html
- Wickham, *testthat*: testing infrastructure for R functions. https://testthat.r-lib.org/

## Explicitly non-universal conventions

- `data/raw`, `data/processed`, `R`, `scripts`, `outputs`, `reports` are practical naming conventions, not an official R standard.
- `targets`, `renv`, `testthat`, and R packages have maintenance costs. Introduce each only for a concrete benefit.
- Reproducibility includes code, data, computational environment, randomness, provenance, and traceable outputs; folder layout alone does not establish it.

## Companion skill

- `r-human-code` (in the local skills folder): line-level readability for R scientists,
  including error-handling rules and function extraction. Used together with this skill.
  This skill covers structure, data flow, provenance and verification.
