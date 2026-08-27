# Contributing

Thank you for helping build the best Symfony 8 Certification resource.

## Ground rules

- **English only.** Clear, progressive, expert-level, concise. No filler.
- **Symfony 8 / PHP 8.4+ only.** No deprecated APIs, no legacy syntax. Every
  snippet must compile.
- **Stay inside the syllabus.** See the
  [official topics](https://certification.symfony.com/exams/symfony.html) and the
  [Traceability Matrix](specs/TraceabilityMatrix.md). Do **not** add content for
  excluded subjects (Symfony UX/AI, Doctrine, Monolog, AssetMapper, Encore,
  third-party bundles/bridges) or expand the three chapters already relocated to
  [`docs/appendices/out-of-syllabus/`](docs/appendices/out-of-syllabus/index.md)
  as if they were in-scope again — see the Traceability Matrix's "Out-of-scope /
  Additional Learning" section for the complete, current exclusion list.
- **Every claim is verifiable** against official documentation or the Symfony
  source. Link the official docs for each major concept.

## Adding or editing a chapter

1. Copy [`docs/_meta/CHAPTER_TEMPLATE.md`](docs/_meta/CHAPTER_TEMPLATE.md).
2. Follow [`docs/_meta/CONVENTIONS.md`](docs/_meta/CONVENTIONS.md) for headings,
   admonitions, diagrams, and code style.
3. Add the page to the `nav:` tree in `mkdocs.yml`.
4. Run `mkdocs build --strict` — it must pass with zero warnings.
5. Update the [Traceability Matrix](specs/TraceabilityMatrix.md) if you added a
   syllabus mapping.

## Adding practice questions

- Add questions to the matching file in [`quiz/`](quiz/).
- Format is compatible with
  [certificationy-cli](https://github.com/certificationy/certificationy-cli).
- Every question needs an explanation and at least one official-docs reference.

## Definition of Done

See [`specs/DefinitionOfDone.md`](specs/DefinitionOfDone.md). A chapter is not
done until it passes the [Review Checklist](specs/ReviewChecklist.md).
