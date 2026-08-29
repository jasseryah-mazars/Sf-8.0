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
| [php-web-security.md](php-web-security.md) | 13 chapters |
| [http.md](http.md) | 11 chapters |
| [architecture.md](architecture.md) | 16 chapters |
| [controllers.md](controllers.md) | 13 chapters |
| [routing.md](routing.md) | 11 chapters |
| [twig.md](twig.md) | 13 chapters |
| [forms.md](forms.md) | 11 chapters |
| [validation.md](validation.md) | 8 chapters |
| [dependency-injection.md](dependency-injection.md) | 14 chapters |
| [security.md](security.md) | 16 chapters |
| [http-caching.md](http-caching.md) | 6 chapters |
| [console.md](console.md) | 8 chapters |
| [testing.md](testing.md) | 10 chapters |
| [messenger.md](messenger.md) | 7 chapters (split out of Miscellaneous — its own top-level syllabus domain) |
| [miscellaneous.md](miscellaneous.md) | 15 chapters (Messenger relocated out — see above) |
| [quality-gate.md](quality-gate.md) | Cross-cutting QA, build, coverage |

_Chapter counts above are the live count of non-index `.md` files under each
`docs/<area>/` directory (English source), re-derived this run — several had
drifted stale over many prior sessions as chapters were added (e.g.
`php-web-security` gained Attributes/Enums; `security` gained five Expert
chapters; `dependency-injection` gained Lazy Services/Resettable Services/
Container Dump). Not every individual `T-<AREA>-NN` task entry inside each file has been
re-numbered to match this live count — that finer-grained reconciliation is
tracked as a follow-up in `specs/RemediationLog.md` (P0-02), not silently
assumed done just because the top-level count above now matches reality._

## Dependency overview

Foundation → area indexes → chapters → quality gate. Chapters within an area are
independent of each other. Cross-area prerequisites follow
[`specs/Roadmap.md`](../specs/Roadmap.md) (e.g. Forms depends on Twig + Validation).
