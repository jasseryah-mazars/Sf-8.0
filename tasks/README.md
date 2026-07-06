# Tasks

Granular, independently-executable work items for building and maintaining the
platform. Each task has an ID, dependencies, acceptance criteria, deliverables,
complexity, and a review checklist reference.

## Conventions

- **ID:** `T-<AREA>-<n>` (e.g. `T-DI-09`). Foundation tasks use `T-FND-*`.
- **Complexity:** S (≤1h) · M (½ day) · L (1–2 days).
- **Acceptance:** a chapter passes only if it satisfies
  [`specs/DefinitionOfDone.md`](../specs/DefinitionOfDone.md) and the
  [`specs/ReviewChecklist.md`](../specs/ReviewChecklist.md).
- **Deliverables** for a chapter task: the Markdown file + its `nav` entry +
  3–6 questions in the area's `quiz/*.yml` + Traceability Matrix row set to ✅.

## Task groups

| File | Scope |
|---|---|
| [foundation.md](foundation.md) | Scaffold, specs, template, CI, quiz schema |
| [php-web-security.md](php-web-security.md) | 11 chapters |
| [http.md](http.md) | 10 chapters |
| [architecture.md](architecture.md) | 16 chapters |
| [controllers.md](controllers.md) | 13 chapters |
| [routing.md](routing.md) | 11 chapters |
| [twig.md](twig.md) | 13 chapters |
| [forms.md](forms.md) | 11 chapters |
| [validation.md](validation.md) | 8 chapters |
| [dependency-injection.md](dependency-injection.md) | 11 chapters |
| [security.md](security.md) | 11 chapters |
| [http-caching.md](http-caching.md) | 6 chapters |
| [console.md](console.md) | 8 chapters |
| [testing.md](testing.md) | 10 chapters |
| [miscellaneous.md](miscellaneous.md) | 15 chapters |
| [quality-gate.md](quality-gate.md) | Cross-cutting QA, build, coverage |

## Dependency overview

Foundation → area indexes → chapters → quality gate. Chapters within an area are
independent of each other. Cross-area prerequisites follow
[`specs/Roadmap.md`](../specs/Roadmap.md) (e.g. Forms depends on Twig + Validation).
