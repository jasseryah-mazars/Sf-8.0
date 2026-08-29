# Specification

## 1. Vision

Build the definitive, open-source, self-contained preparation platform for the
**Symfony 8 Certification** (Advanced & Expert). An experienced developer should
be able to prepare **without any other learning material** except official
documentation references.

## 2. Problem

The only well-known community resource
([ThomasBerends list](https://github.com/ThomasBerends/symfony-certification-preparation-list))
is a link index with no teaching content. Candidates must assemble knowledge from
dozens of scattered pages, with no depth, exercises, traps, or revision aids, and
it targets Symfony 7.

## 3. Goals

- **G1** Cover 100% of the official syllabus, verified by a Traceability Matrix.
- **G2** Teach at Expert depth — internals, lifecycle, trade-offs — not summaries.
- **G3** Modern only — Symfony 8, PHP 8.4+, attributes, no deprecated APIs.
- **G4** Optimize for smartphone reading and minimal-click navigation.
- **G5** Provide practice: exercises + solutions, inline questions, and a
  machine-readable quiz bank.
- **G6** Be maintainable across future Symfony minor releases.

## 4. Non-goals

- Not a Doctrine/Monolog/UX/AI/AssetMapper/Encore tutorial (out of syllabus scope).
- Not a replacement for the official documentation — it complements and references it.
- Not an exam brain-dump; questions are educational, not leaked exam items.

## 5. Audience & personas

- **P1 "The Practitioner"** — 2–5 yrs Symfony, targets Advanced. Needs structured
  coverage and confidence on edge cases.
- **P2 "The Expert candidate"** — senior, targets Expert. Needs internals,
  trade-offs, and trap-spotting.
- **P3 "The Contributor"** — maintains/extends content after new Symfony releases.

## 6. Scope

- **In:** the 14 official topic areas and all their sub-topics; an Exam Guide; a
  Revision Hub; a quiz bank.
- **Out:** the excluded list in [GapAnalysis §5](GapAnalysis.md).

## 7. Deliverables

1. `docs/` — MkDocs Material site of micro-chapters (one folder per topic area).
2. `quiz/` — certificationy-compatible YAML question bank.
3. `specs/` — this SpecKit set (started at 13 documents, now 25 as later
   audit/remediation rounds added their own report and log documents).
4. `tasks/` — granular, independently-executable task definitions.
5. Build/deploy tooling (`mkdocs.yml`, `requirements.txt`, GitHub Actions).

## 8. Success criteria

- Traceability Matrix at 100%.
- `mkdocs build --strict` green in CI.
- Every chapter passes the [Definition of Done](DefinitionOfDone.md).
- Content usable end-to-end on a phone.

## 9. Exam facts (drivers)

75 questions / 90 min; single, multiple, true/false; Advanced & Expert by score;
PHP 8.4+ baseline; HTTP Caching down-weighted, Messenger up-weighted vs SF7.

## 10. Related specs

[Requirements](Requirements.md) · [Architecture](Architecture.md) ·
[LearningStrategy](LearningStrategy.md) · [ContentStructure](ContentStructure.md) ·
[Roadmap](Roadmap.md) · [GapAnalysis](GapAnalysis.md) · [MigrationPlan](MigrationPlan.md) ·
[QualityRequirements](QualityRequirements.md) · [DefinitionOfDone](DefinitionOfDone.md) ·
[TraceabilityMatrix](TraceabilityMatrix.md) · [ReviewChecklist](ReviewChecklist.md) ·
[FutureMaintenance](FutureMaintenance.md).
