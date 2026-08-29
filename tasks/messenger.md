# Tasks — Messenger

**Area dir:** `docs/messenger/` · **Quiz:** `quiz/messenger.yml` · **Revision priority:** Critical (up-weighted on the Symfony 8 exam) · **Prerequisites:** Dependency Injection, Console, Events

> Acceptance for every task below = passes [DefinitionOfDone](../specs/DefinitionOfDone.md) + [ReviewChecklist](../specs/ReviewChecklist.md). Deliverables = chapter file + nav entry + quiz questions + Matrix row.

Split out of `docs/miscellaneous/` into its own top-level domain because the
official syllabus presents Messenger as an autonomous topic area with its own
7 sub-topics, not a Miscellaneous subsection (see `tasks/miscellaneous.md`
T-MISC-08 for the superseded original entry). All 8 items below are **done** —
`specs/TraceabilityMatrix.md` reports 7/7 Messenger subtopics PASS on automated
evidence as of the matrix's last regeneration.

## T-MSG-00 — Area landing page
- **Deliverable:** `docs/messenger/index.md` (intro, prereqs/level/difficulty/dependencies/revision priority, links to all sub-chapters).
- **Status:** done.

## T-MSG-01 — Messenger component
- **Deliverable:** `docs/messenger/component.md`.
- **Status:** done. Matrix: PASS.

## T-MSG-02 — Messages and handlers
- **Deliverable:** `docs/messenger/messages-handlers.md`.
- **Status:** done. Matrix: PASS.

## T-MSG-03 — Middleware
- **Deliverable:** `docs/messenger/middleware.md`.
- **Status:** done. Matrix: PASS.

## T-MSG-04 — Transports
- **Deliverable:** `docs/messenger/transports.md`. Third-party transports
  (Doctrine, Redis, Amazon SQS) are explicitly out of scope — the chapter says
  so.
- **Status:** done. Matrix: PASS.

## T-MSG-05 — Workers
- **Deliverable:** `docs/messenger/workers.md`.
- **Status:** done. Matrix: PASS.

## T-MSG-06 — Retries and failures
- **Deliverable:** `docs/messenger/retries-failures.md`.
- **Status:** done. Matrix: PASS.

## T-MSG-07 — Events
- **Deliverable:** `docs/messenger/events.md`.
- **Status:** done. Matrix: PASS.

## Remaining, real gap (not a placeholder — logged for a future lot)

- **French translations** for all 8 files above do not exist yet
  (`docs/messenger/*.fr.md`) — the area currently falls back to English under
  `mkdocs-static-i18n`'s `fallback_to_default`. This is a genuine, named
  content gap, tracked here and in `specs/CoworkProgress.md`, not silently
  hidden.
