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
| P0-04 | Traceability matrix rebuild (6-status schema) | **done this run** | `tools/gen_traceability_matrix.py` redesigned with `multi_status()`/`multi_gaps()`; all 175 rows re-derived under the new schema; `tools/audit.py` rewritten to report the 6-status breakdown instead of PASS/TO VERIFY. Explicitly documented: the 175-row count and the taxonomy it's built from are this repo's own tracking, not an independently re-verified official figure — see RemediationLog. |

## P1 — High priority

| # | Subject | Status | Notes |
|---|---|---|---|
| P1-01 | Strengthen `tools/audit.py` / `tools/final_audit.py` | in progress | `final_audit.py`'s hardcoded `/154` fixed this run (P0-04 spirit). Full structured-Markdown-AST checks (vs. today's regex-based section detection) not yet done — deferred, scoped in RemediationLog. |
| P1-02 | Code/config fragment testing (PHP 8.4, YAML, XML, Twig) | **done this run** | New `tools/lint_yaml.py` (373 snippets/0 failures), `tools/lint_twig.py` (block-tag pairing only, 222/0), `tools/lint_xml.py` (2 complete docs/0 failures, fragments correctly skipped). PHP unchanged (382/0). All wired into CI. Two real false-positive bugs found and fixed in the new tools themselves during this run — see RemediationLog for the full story. Explicitly not done: schema-level validation against Symfony's real Config tree (would need a live container). |
| P1-03 | Full quiz audit (every question) | partially automated | `tools/check_quiz_duplicates.py` (new) added near-duplicate detection (17 candidates found, 16 legitimate, 1 real duplicate found and fixed — see `specs/RemediationLog.md`). `specs/QuizAuditReport.md` updated accordingly. A full per-question manual audit of all 1,292 questions against syllabus/accuracy/ambiguity is still out of reach in one run and remains explicitly unverified — see the report for exactly what was and wasn't checked. |
| P1-04 | Reproducible reports | **done this run** | Every report this run's tooling writes now states date, branch, commit, and tool versions (see RemediationLog). |
| P1-05 | CI hardening | done | Added `tools/check_exclusions.py` (blocking — and it caught a real pre-existing path-drift bug in the exclusions data, fixed the same run) and `tools/check_report_freshness.py` (informational). Fixed CI trigger/deploy scope to cover this mission's actual working branch. Reviewed permissions (already minimal), secrets (none), and version pinning (major-version tags, deliberately not SHA-pinned — documented rationale in `specs/RemediationLog.md`). |

## P2 — Medium priority

| # | Subject | Status | Notes |
|---|---|---|---|
| P2-01 | Editorial structure normalization | **done this run** | New `tools/check_editorial_structure.py` (nav<->docs consistency, code-fence balance, empty-body headings — all 0 violations after fixes). Found and fixed a real generator bug in `tools/gen_revision_sheets.py` (its file glob picked up `*.fr.md` sidecars, duplicating every chapter's content in French+English inside the English-only revision sheets, plus a stray empty section from `index.fr.md` leaking in) — see RemediationLog. Section order (176/176) and Official-References/placeholder/link checks (already covered by `check_section_order.py`/`check_placeholders.py`) re-verified, not re-implemented. |
| P2-02 | README/documentation corrections | **done this run** | `README.md` and `CONTRIBUTING.md`: all 24 internal links re-verified resolvable (none broken); "Out of scope" section was stale (only listed the "never taught" ecosystem items, missing the 3 chapters actually relocated to `docs/appendices/out-of-syllabus/` and the additional in-chapter exclusions) — expanded and linked to the matrix's exclusions section and `tools/check_exclusions.py`; "Coverage tracked and validated" bullet reworded to name the six-status schema explicitly and point at the matrix's own "what this count is/is not" caveat instead of implying an unqualified coverage guarantee. No stale numeric coverage claims were present to begin with (the README already avoided quoting a bare percentage) — confirmed, not assumed. |
| P2-03 | Site quality (accessibility, mobile, etc.) | **done this run** | Real headless-Chromium + axe-core audit (`tools/check_site_quality.py`, on-demand — not CI-wired, see report), not a heuristic. Fixed 3 verified issues (task-list checkbox labels via new `docs/assets/a11y.js`; light+dark code-highlighting contrast via `docs/assets/code.css`). Documented 3 more found-not-fixed (search-dialog aria-name, in-text link contrast/distinguishability tied to the accent color choice, one landmark-uniqueness finding) with concrete causes and remedies. Investigated and explicitly left unresolved: search result DOM rendering (backend verified correct via worker-message interception; on-page render unverified in this environment) and Mermaid rendering (blocked by this environment's network access to its CDN, not confirmed broken). Full report: `specs/SiteQualityReport.md`. |

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
