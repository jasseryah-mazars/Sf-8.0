# Review Checklist

Used by the QA / Fact-Checker / Code-Reviewer pass before a chapter is accepted.
Reviewer records pass/fail per item.

## Technical accuracy

- [ ] Every factual claim is correct for **Symfony 8.0 / PHP 8.4**.
- [ ] Class/interface/method names exist and are spelled with correct FQCN.
- [ ] Execution-order / lifecycle claims match the actual framework behaviour.
- [ ] No deprecated or removed APIs; replacements are current.
- [ ] Config keys, attribute names, and console commands are real and current.

## Code quality

- [ ] Snippets parse and would run (imports present, types valid).
- [ ] `declare(strict_types=1)`, promotion, `readonly`, attributes used idiomatically.
- [ ] Examples are minimal but realistic; no dead placeholders that break parsing.

## Pedagogy

- [ ] Concepts introduced before use; difficulty progresses.
- [ ] Deep dive genuinely explains internals, not a restatement of "how".
- [ ] Exercises match the objectives; solutions are correct and complete.
- [ ] Certification traps are real exam-relevant subtleties, not padding.

## Structure & consistency

- [ ] Template section order followed; admonition types used per conventions.
- [ ] Diagrams render and are legible on mobile.
- [ ] Tables ≤4 columns; paragraphs short.
- [ ] Cross-links and doc links resolve (checked by `--strict` build + spot check).

## Scope

- [ ] Nothing from the excluded list is taught.
- [ ] Sub-topic maps to a real syllabus item (Traceability Matrix updated).

## Sign-off

- [ ] Author agent · [ ] Peer reviewer agent · [ ] `mkdocs build --strict` green.
