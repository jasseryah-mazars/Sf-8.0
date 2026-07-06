# Enhancement-Pass Brief (fact-check + "In a nutshell")

You are performing a **review-and-enrich pass** on one topic area. Two goals:

## Goal 1 — Add an "In a nutshell" TL;DR to every chapter

At the **very top of each chapter, immediately after the `# H1` title and before
the `!!! abstract "Learning objectives"` block**, insert:

```
!!! tip "In a nutshell"
    <1–3 short sentences in plain, candidate-first language: what this is, why it
    exists, and the single highest-yield fact to remember for the exam.>
```

Rules:
- Plain language first (candidate view), then the exam hook. No jargon dump.
- Mobile-friendly: max ~3 short lines. One idea.
- Do **not** duplicate the objectives; complement them.
- Skip the area `index.md` landing page (it is already a summary).

## Goal 2 — Fact-check and fix (Symfony 8 / PHP 8.4)

Read each chapter critically and **fix inaccuracies in place**:
- Wrong or misspelled FQCNs, class/interface/method names, config keys, attributes.
- Incorrect execution order / lifecycle claims.
- Any deprecated/removed API presented as current (must be framed as "removed, use X").
- Broken or non-`current` doc links; source links should target `blob/8.0`.

## Hard rules

- **NEVER delete or shorten existing content.** Add, extend, correct only
  (`specs/AuditPolicy.md`). Fixing a factual error is allowed; removing a section
  is not.
- Keep every chapter's template section order intact.
- Do **not** edit `mkdocs.yml`, `specs/TraceabilityMatrix.md`, `quiz/*`, or other
  areas' files.
- Symfony 8.0 / PHP 8.4 only. Attributes-first. Snippets must still compile
  (`php -l`), so keep `<?php`+`declare(strict_types=1)` on complete-file snippets.

## Report back

List: chapters given a TL;DR; every factual fix made (file + what was wrong → the
correction); anything you were unsure about for a human fact-checker.
