# Quality Requirements

Non-functional requirements the platform must meet. Verified per chapter (Review
Checklist) and globally (CI `mkdocs build --strict`).

## Q1 — Correctness

All content is technically accurate for Symfony 8.0 / PHP 8.4. Claims are backed
by official docs or Symfony source. No deprecated/removed APIs anywhere.

## Q2 — Depth (Expert bar)

Every major concept answers: *What happens internally? Which classes/interfaces?
Execution order? Lifecycle? Extension points? Performance/memory impact? Common
mistakes? When not to use it? Alternatives?* Surface-level "how-to" is insufficient.

## Q3 — Consistency

One template, one voice, one set of conventions. Terminology, admonition usage,
tab labels, and file naming are uniform across all chapters.

## Q4 — Completeness

100% of official syllabus items are covered (Traceability Matrix). Each chapter
includes objectives, theory, deep dive, code, traps, exercises+solutions,
questions, revision, and references.

## Q5 — Readability (mobile-first)

Micro-chapters (target 150–450 lines). Short paragraphs, narrow tables, small
diagrams. Navigation reachable in ≤2 taps via tabbed nav + client-side search.

## Q6 — Maintainability

Small independent files; content decoupled from build config. Doc links use
`doc/current`; source links pin `8.0`. Clear contribution path and templates.
See [FutureMaintenance.md](FutureMaintenance.md).

## Q7 — Buildability

`mkdocs build --strict` passes with zero warnings on every push (CI). No broken
internal links, no missing nav targets, no orphan pages.

## Q8 — Learnability

Content is ordered by an optimized [Roadmap](Roadmap.md), not raw syllabus order,
to maximize understanding for an Expert-level candidate.

## Q9 — Language

Clear, concise, progressive, technically precise English. No filler, no
duplicated explanations — cross-reference instead.

## Q10 — Legal / scope

MIT-licensed, upstream attribution preserved, Symfony trademark disclaimer present,
excluded topics not taught.
