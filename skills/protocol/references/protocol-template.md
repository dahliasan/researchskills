---
version: "0.1"
name: example-review
review_type: scoping
question_framework: PCC
question:
  population: ""
  concept: ""
  context: ""
date_range:
  from: "2000-01-01"
  to: "2026-12-31"
languages: ["en"]
search:
  queries:
    - "replace with OpenAlex query strings"
sources:
  primary:
    - id: openalex
      role: primary
      method: api
  additional:
    - id: citation_snowball
    - id: seed_inject
seeds: []
eligibility:
  include:
    - "Draft include criteria"
  exclude:
    - "Draft exclude criteria"
screening:
  stages: ["title_abstract"]
  ai:
    enabled: true
    role: triage
extraction:
  schema: usefulpapers.extraction.v3
synthesis:
  method: narrative
reporting:
  checklist: PRISMA-ScR
---

## Overview

One paragraph: what this review is for.

## Question

State the research question in prose.

## Eligibility

Include / exclude in plain language (mirrors YAML).

## Search

**Primary:** OpenAlex using `search.queries` above.  
**Additional:** snowball / seeds as listed.

## Screening

How title/abstract (and optional full text) decisions are made.
