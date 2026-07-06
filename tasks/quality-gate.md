# Tasks — Quality Gate (cross-cutting)

Run after content tasks; some are recurring.

## T-QG-01 — Strict build passes
- **Description:** `mkdocs build --strict` completes with zero warnings (no broken
  links, no missing nav targets, no orphan pages).
- **Acceptance:** CI job green on the branch. **Complexity:** M · **recurring.**

## T-QG-02 — Fact-check / technical review
- **Description:** Verify Symfony 8 / PHP 8.4 accuracy across chapters: class/FQCN
  correctness, no deprecated APIs, kernel-event order, security flow, cache headers.
- **Acceptance:** [ReviewChecklist](../specs/ReviewChecklist.md) passes per chapter.
- **Complexity:** L.

## T-QG-03 — Consistency pass
- **Description:** Uniform template section order, admonition usage, tab labels,
  cross-link style; dedupe overlapping explanations (cross-link instead).
- **Complexity:** M.

## T-QG-04 — Quiz validation
- **Description:** All `quiz/*.yml` parse; every question has correct answer(s),
  `explanation`, and `documentation`; no deprecated APIs. **Complexity:** M.

## T-QG-05 — Traceability closure
- **Description:** Set every [Traceability Matrix](../specs/TraceabilityMatrix.md)
  row to ✅ and update the coverage summary to 100%.
- **Acceptance:** 154/154 items done. **Complexity:** S.

## T-QG-06 — Mobile readability spot-check
- **Description:** Verify chapters render on a narrow viewport (tables ≤4 cols,
  diagrams legible, no horizontal scroll). **Complexity:** S.

## T-QG-07 — Revision Hub aggregation
- **Description:** Ensure `docs/revision/*` reflects the finished chapters
  (cheat sheet, trap index, memory aids, quiz). **Complexity:** M.
