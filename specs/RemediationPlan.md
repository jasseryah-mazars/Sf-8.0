# Remediation Plan

Tracks every subject from the mission brief ("Mise en conformité vérifiable avec
le syllabus officiel Symfony 8"), in the mandated order, most-critical first.
Status is updated as each subject is analyzed → planned → modified → tested →
corrected → documented. See `specs/RemediationLog.md` for the executed result of
each subject and `specs/FinalComplianceAudit.md` for the end-state audit.

**Status legend:** `not started` · `in progress` · `done this run` · `deferred`
(deferred = analyzed and scoped, but not executed this run — reason given).

## P0 — Blocking

| # | Subject | Status | Notes |
|---|---|---|---|
| P0-01 | Symfony 8.0 doc/source references | **done this run** | 5,773 unversioned-`doc`-tree link replacements (pinned to `/doc/8.0/`) across 456 files; `specs/*.md` policy language updated; new blocking check `tools/check_doc_version_refs.py` (wired into CI); one documented exception (`specs/GapAnalysis.md`, describes an unrelated ancestor project, not a live reference). See RemediationLog. |
| P0-02 | Official taxonomy alignment | **in progress** | Taxonomy extracted into `specs/OfficialSyllabusBaseline.md` from `specs/TraceabilityMatrix.md` (already cross-referenced against the syllabus in prior sessions). Live re-fetch of `certification.symfony.com` blocked this run — flagged, not silently assumed correct. Comparison against mkdocs.yml/docs/quiz/exams/revision/labs/tasks not yet executed this run. |
| P0-03 | Excluded topics re-audit + relocation | **in progress** | Prior session's P0-06 out-of-scope audit already removed evaluated content on excluded subjects; this run's job is to re-verify that holds AND physically relocate the 3 full excluded chapters to `docs/appendices/out-of-syllabus/` with the mandated banner and an anti-regression check — not yet executed. |
| P0-04 | Traceability matrix rebuild (6-status schema) | **in progress** | New per-subtopic status columns (absent/structure/partiel/validé techniquement/validé éditorialement/conforme) require a schema change to `tools/gen_traceability_matrix.py` and a re-derivation of every one of 175 rows — large, mechanical, done incrementally; see RemediationLog for what's landed vs pending at end of this run. |

## P1 — High priority

| # | Subject | Status | Notes |
|---|---|---|---|
| P1-01 | Strengthen `tools/audit.py` / `tools/final_audit.py` | in progress | `final_audit.py`'s hardcoded `/154` fixed this run (P0-04 spirit). Full structured-Markdown-AST checks (vs. today's regex-based section detection) not yet done — deferred, scoped in RemediationLog. |
| P1-02 | Code/config fragment testing (PHP 8.4, YAML, XML, Twig) | deferred this run | PHP fragments already pass `tools/lint_php.py` (382 snippets, 0 failures) against PHP 8.4.19 — that part is real and current. YAML fragments inside quiz/config examples and Twig-fragment syntax checking via a real Twig lexer are **not yet wired** — scoped as a follow-up, not fabricated as done. |
| P1-03 | Full quiz audit (every question) | deferred this run | `specs/QuizAuditReport.md` created with the schema/method and the automated checks that *are* running (`validate_quiz.py`) but a full per-question manual audit of 1,292 questions against syllabus/accuracy/ambiguity/duplication is out of reach in one run — see the report for what was and wasn't checked. |
| P1-04 | Reproducible reports | **done this run** | Every report this run's tooling writes now states date, branch, commit, and tool versions (see RemediationLog). |
| P1-05 | CI hardening | **partial this run** | Added the P0-01 blocking check to `.github/workflows/deploy.yml`. Full permission/version pinning review of the workflow deferred. |

## P2 — Medium priority

| # | Subject | Status |
|---|---|---|
| P2-01 | Editorial structure normalization | not started this run |
| P2-02 | README/documentation corrections | not started this run |
| P2-03 | Site quality (accessibility, mobile, etc.) | not started this run |

## P3 — Improvements

Not started — P0/P1/P2 are not closed, so P3 has not begun per the mandated order.

## Method applied per subject (mission brief, verbatim intent)

1. Record the action here before starting.
2. Identify affected files, blast radius, and references.
3. Apply the fix.
4. Run the relevant automated check(s).
5. Fix any failure, re-run.
6. Update the matrix and reports.
7. Log the result in `specs/RemediationLog.md`.
8. Commit locally (never push — explicit instruction this run).
9. Move to the next subject immediately.
