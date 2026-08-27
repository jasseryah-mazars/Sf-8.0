# Final Compliance Audit — Validation finale

_This IS the mission's "Validation finale": every subject in
`specs/RemediationPlan.md` (P0-01 through P3) is closed as of this file's
generation. Generated 2026-08-27, branch `claude/sf-8-certification-quality-iimd4l`,
commit `e400ce4`, from a clean working tree (verified via `git status
--porcelain` immediately before this run's final validation pass)._

## 1. State at generation time

- **Branch:** `claude/sf-8-certification-quality-iimd4l`
- **Commit:** `e400ce4` (HEAD at generation time)
- **Commits this compliance run** (`c28e33f..HEAD`, oldest first):
  1. `4c484da` — P0-01: pin every Symfony doc/source reference to 8.0
  2. `f1d3482` — P0-03: relocate the 3 fully-excluded chapters to `docs/appendices/out-of-syllabus/`
  3. `774d9f7` — P0-02: align `tasks/` with the current 15-domain syllabus taxonomy
  4. `8180906` — docs(mission): initialize compliance remediation tracking + quiz answer-count check
  5. `445ecec` — P0-04 + P1-01: rebuild traceability matrix on the six-status schema, new structural checks
  6. `aeb3748` — P1-02: YAML/XML/Twig fragment testing, wired into CI
  7. `0f04266` — P1-03: quiz near-duplicate detection + fix one genuine duplicate
  8. `294b27d` — P1-04: reproducible-report provenance stamps + staleness checker
  9. `55766ad` — P1-05: CI hardening — exclusions consistency check + branch/scope fixes
  10. `a0d7bb7` — P2-01: editorial structure checks + fix revision-sheet duplication bug
  11. `e312c97` — P2-02: README/CONTRIBUTING corrections
  12. `df6c005` — P2-03: real browser-based site quality audit + 3 verified fixes
  13. `61a9f4e` — P3: error-handling hardening + future syllabus-update process docs
  14. `e400ce4` — chore: regenerate provenance-stamped reports for validation finale

  (starting point: `c28e33f`, clean working tree, verified via
  `git status --porcelain` at the start of this run)
- **Branch correction made mid-run:** the working checkout had drifted onto
  `master` partway through this multi-session mission. Verified via
  `git merge-base --is-ancestor` that this was a pure fast-forward
  continuation of the harness-designated branch's already-pushed tip (no
  divergent history discarded), moved the branch pointer forward, and
  continued all subsequent work on the correct branch — see P1-05 in
  `specs/RemediationLog.md`.
- **Pushed to a remote:** **Yes, as of this run's completion** — the
  mission's final instruction ("fait pusher et deployer en githu pages")
  explicitly supersedes the earlier general no-push instruction in the
  same message. Push happens after this report is committed; see the
  final chat message for the actual push/deploy confirmation, since it
  necessarily happens after this file is written.
- **Destructive Git operations used:** None, across the entire run. No
  `--force`, no history rewrite of any already-pushed commit, no branch
  deletion. `git mv` was used for the P0-03 relocation (history-preserving
  rename). The one branch-pointer move (above) was a fast-forward onto the
  branch's own already-pushed tip, not a rewrite.

## 2. Validation commands run and their results (final state, this commit)

| Command | Result |
|---|---|
| `python3 tools/gen_traceability_matrix.py` | 175 subtopics regenerated under the six-status schema |
| `python3 tools/audit.py` | **conforme: 161 · validé éditorialement: 9 · validé techniquement: 0 · partiel: 4 · structure: 1 · absent: 0.** `170/175` reach *validé éditorialement or conforme* — **this is not "170 fully compliant"; full completion (conforme, all 175) is not reached.** Exit 0 (no genuinely `absent` mapped chapter). |
| `python3 tools/check_exclusions.py` | 0 inconsistencies — all 3 relocated chapters + in-chapter exclusions consistently marked across files, nav, quiz tags, and the matrix |
| `python3 tools/check_doc_version_refs.py` | `OK` — 0 non-8.0-pinned Symfony doc/source references |
| `python3 tools/validate_quiz.py` | **Structural validity: 1292 questions, 0 schema errors.** 1268 official / 24 out-of-scope; subchapter coverage 157/157. **This proves the bank is well-formed, not that all 1,292 questions are individually fact-checked against Symfony 8.0** — see `specs/QuizAuditReport.md`. |
| `python3 tools/check_quiz_duplicates.py` | 16 candidate near-duplicate pairs (lexical heuristic); all reviewed by hand — legitimate shared template phrasing across different topics, not real duplicates (the one real duplicate found this run was already fixed in P1-03) |
| `python3 tools/check_section_order.py` | 176/176 chapters compliant |
| `python3 tools/lint_php.py` | **382 blocs PHP testés, 0 erreur** (PHP 8.4.19) — proves the extracted snippets parse/lint cleanly, not that each is independently confirmed accurate against Symfony 8.0's current API |
| `python3 tools/lint_yaml.py` | 373 blocs YAML testés, 0 erreur (syntax only) |
| `python3 tools/lint_twig.py` | 222 blocs Twig testés, 0 erreur (block-tag pairing only — no real Twig lexer available in this environment, documented as such in the tool itself) |
| `python3 tools/lint_xml.py` | 2 documents complets testés + 2 fragments correctement ignorés, 0 erreur |
| `python3 tools/check_placeholders.py` | OK — every `## Official References` section has a link, no placeholder markers, no broken internal links, across 497 files |
| `python3 tools/check_editorial_structure.py` | 0 violations — nav/docs consistency, code-fence balance, empty-heading detection |
| `python3 tools/check_links.py --offline` | 700 URLs inventoried, offline only (no network used) |
| `python3 tools/check_report_freshness.py` | All 4 stamped reports FRESH (stamped commit == this file's own generation commit's parent, as expected) |
| `mkdocs build --strict` | **Exit code 0.** Promotes MkDocs' own structural warnings (broken link, missing nav target, orphan page) to failures. **Does not silence the recurring third-party `DeprecationWarning` below**, which is documented regardless of the exit code. |

**Recurring warning, documented as instructed (a 0 exit code does not make**
**it disappear from the record):** every `mkdocs build` in this environment
prints, twice (once per language build):
```
DeprecationWarning: Do not access Theme._vars, instead access the keys of Theme directly.
  File ".../mkdocs_static_i18n/reconfigure.py", line 304, in reconfigure_material_theme
```
This originates inside the third-party `mkdocs-static-i18n` plugin's own
code, not this repository's content or configuration. `mkdocs build
--strict` does not treat a plain Python `DeprecationWarning` as
build-breaking (only MkDocs' own structural warnings are promoted), which
is why exit 0 and this warning coexist. It has appeared on every build
this run and across prior sessions; fixing it requires an upstream
`mkdocs-static-i18n` release or pinning an older `mkdocs`/`mkdocs-material`
version — neither done this run.

None of the numeric results above are hardcoded anywhere in the reporting
tools — each command computes its figures live from the current repository
state, and `tools/repo_meta.py`-stamped reports name the exact commit they
were generated from (`tools/check_report_freshness.py` verifies this).

## 3. Per-subject final status (mirrors specs/RemediationPlan.md — all done)

| Subject | Status |
|---|---|
| P0-01 Symfony 8.0 doc/source references | **Done.** 0 violations, blocking CI check. |
| P0-02 Official taxonomy alignment | **Done, with one honestly-flagged gap:** a live re-diff against `certification.symfony.com` could not be performed this run — network egress confirmed blocked, not assumed. The taxonomy used is this repo's own working taxonomy, cross-referenced against official sources in prior sessions when reachable — see `specs/OfficialSyllabusBaseline.md`'s explicit "not itself official" banner. |
| P0-03 Excluded topics relocation | **Done.** 3 chapters relocated with banners, `tools/check_exclusions.py` (P1-05) now guards against future re-drift — and caught one real pre-existing path-drift bug in the matrix's own exclusions table during that same subject. |
| P0-04 Traceability matrix rebuild (6-status schema) | **Done.** `tools/gen_traceability_matrix.py` redesigned; all 175 rows re-derived; `170/175 PASS`-equivalent, explicitly not full conformance. |
| P1-01 Strengthen audit tooling | **Done.** New structural checks (`check_placeholders.py`). |
| P1-02 Code/config fragment testing | **Done.** YAML (373/0), Twig (222/0, block-tag-only, documented limit), XML (2+2/0) linters added and wired into CI; PHP unchanged (382/0, re-verified). |
| P1-03 Full quiz audit | **Partially automated, honestly scoped.** Near-duplicate detection added and one real duplicate fixed. A full per-question manual read against Symfony 8.0 for all 1,292 questions remains outside one run's reach — `specs/QuizAuditReport.md` states exactly what is and isn't covered. |
| P1-04 Reproducible reports | **Done.** Every machine-generated report now carries a commit/branch/date/tool-version stamp; a staleness checker exists. |
| P1-05 CI hardening | **Done.** New blocking exclusions check, informational freshness check, fixed CI branch/deploy scope, reviewed permissions/secrets/version-pinning. |
| P2-01 Editorial structure normalization | **Done.** New nav/fence/empty-heading checks; fixed a real generator bug that was duplicating French content into English revision sheets. |
| P2-02 README/documentation corrections | **Done.** Fixed a stale exclusion list and an overclaim-risk coverage bullet in README/CONTRIBUTING. |
| P2-03 Site quality | **Done, with 2 items explicitly left unresolved rather than guessed at** (search result DOM rendering, Mermaid CDN reachability) — see `specs/SiteQualityReport.md`. 3 real accessibility issues fixed (verified with axe-core), 3 more documented with concrete remedies. |
| P3 Improvements | **Done.** Error-handling hardened in 3 tools; future syllabus-update process documented in `specs/FutureMaintenance.md` §10-11. Duplication reduction and pedagogical-quality improvement addressed where found (P1-03, P2-01), not attempted as a separate sitewide sweep — documented as out of one-run reach rather than claimed complete. |

## 4. What "conforme" does and does not mean here

Per this project's standing rule (never declare a status just because a
file or title exists) and this run's explicit caveats: **"conforme" in
`specs/TraceabilityMatrix.md` is this project's own six-status schema's
top tier** (structural + technical validation + editorial validation + a
French translation present) — **it is not an assertion that Symfony's
certification body has confirmed the item**, nor that the content has been
re-verified against a live fetch of the official syllabus this run (that
fetch was blocked). 161/175 subtopics reach "conforme"; 9 more reach
"validé éditorialement" (same bar minus the French translation); 5 do not
reach either. None of this is "170/175 PASS = compliance achieved" — it is
this project's own tracked completeness against its own working taxonomy,
stated exactly that precisely, on purpose.

Similarly: `validate_quiz.py`'s 0 errors means **structural validity**
(every question has the required fields, a syllabus tag, a correct-answer
count matching its type), not that all 1,292 questions' content is
individually confirmed accurate. `lint_php.py`'s "382 blocs testés, 0
erreur" means 382 PHP snippets were extracted and parsed/linted without a
syntax error — not that each one was independently confirmed to reflect
Symfony 8.0's current API surface. `mkdocs build --strict`'s exit 0 means
no broken link/missing nav/orphan page — it coexists with, and does not
erase, the documented third-party `DeprecationWarning` in §2.

## 5. Known, real, unresolved gaps (not exhaustive — see RemediationLog.md
for the full list with reasoning per item)

- **Live syllabus/doc re-verification blocked by network egress** for
  every subject touching `certification.symfony.com` or `symfony.com` —
  confirmed blocked live via a failed fetch this run, not assumed from a
  prior session. `specs/OfficialSyllabusBaseline.md` §1 has the exact
  source-reachability table this decision rests on.
- **The full manual, per-question quiz audit (P1-03)** — automatable parts
  (schema validity, near-duplicate detection) are done; the human read of
  1,292 questions against primary sources is not, and is stated as such in
  `specs/QuizAuditReport.md` rather than rounded up.
- **9/175 subtopics at "validé éditorialement," 5/175 at "partiel" or
  below** — the exact rows are in `specs/TraceabilityMatrix.md`'s per-topic
  tables; not individually re-attempted this run (out of the mandated
  subject order, which prioritized building the six-status schema itself
  over closing every gap it now makes visible).
- **`docs/messenger/*.fr.md` French translations do not exist** (a
  pre-existing gap from a prior session, unrelated to this run's subjects,
  still real and unresolved — it is exactly why those chapters cap out at
  "validé éditorialement" rather than "conforme" under the new schema).
- **Two P2-03 findings investigated but left explicitly unresolved**:
  search result DOM rendering (backend verified correct; on-page render
  unverified in this sandboxed environment) and Mermaid diagram rendering
  (blocked by this environment's network access to its CDN, not confirmed
  broken) — both need a human check in a real browser on the live site.
- **Two P2-03 findings documented with a concrete remedy, not fixed**: the
  search dialog's missing ARIA name and one landmark-uniqueness finding
  are stock Material template internals (need a template-override
  mechanism this project doesn't currently use); the in-text link
  contrast/distinguishability issue traces to the site's own
  `primary: black` / `accent: indigo` palette choice, which is a visible
  sitewide design decision, not something to change unilaterally.
- **No sitewide prose-duplication sweep** beyond the two specific
  duplication bugs found and fixed this run (a quiz near-duplicate, a
  revision-sheet generator bug) — no tooling exists yet for that broader
  class of check.

## 6. Sources actually used this run

1. Mission brief (this conversation) — both the original "Mettre le projet
   en conformité..." mission and this message's "Reprends à P0-04..."
   follow-up, including its 8 explicit wording/honesty caveats, applied
   throughout.
2. `specs/TraceabilityMatrix.md` and its supporting `specs/*.md` history
   (previously cross-referenced against `certification.symfony.com` and
   `symfony.com/doc/8.0/` in prior sessions when reachable — **not**
   re-fetched live this run).
3. `github.com/symfony/symfony/tree/8.0` and its `blob/8.0/...` file pages
   (reachable via `WebFetch` in prior sessions this mission drew on;
   `api.github.com` returns 403 in this environment).
4. This repository's own content, read and cross-checked before every edit.
5. **Confirmed not reachable this run** (`EGRESS_BLOCKED`, tested live, not
   assumed): `certification.symfony.com/exams/symfony.html`,
   `symfony.com/doc/8.0/`. `squidfunk.github.io` (for the P2-03 search
   control test) was also confirmed blocked the same way.
6. PHP 8.4.19 (`php -v`, confirmed installed), Node.js 22 + Playwright +
   Chromium (pre-installed in this environment) + axe-core 4.13.0 (fetched
   via `npm install` through this environment's proxy, confirmed reachable)
   for the P2-03 real-browser audit.

## 7. Report paths generated or updated this run

- `specs/OfficialSyllabusBaseline.md` — explicit non-official banner
- `specs/RemediationPlan.md` — full P0–P3 status table
- `specs/RemediationLog.md` — full narrative log, every subject
- `specs/QuizAuditReport.md` — quiz audit scope/method/results
- `specs/SiteQualityReport.md` — P2-03 full findings
- `specs/FinalComplianceAudit.md` — this file
- `specs/TraceabilityMatrix.md` — regenerable via `python3 tools/gen_traceability_matrix.py`
- `specs/CoverageReport.md` — regenerable via `python3 tools/audit.py`
- `specs/FinalAudit.md` — regenerable via `python3 tools/final_audit.py`
- `specs/SectionOrderReport.md` — regenerable via `python3 tools/check_section_order.py`
- `specs/FutureMaintenance.md` — §10 (syllabus-update process), §11 (tool inventory) added
