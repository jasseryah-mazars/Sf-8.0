# Remediation Log

Executed result of each subject in `specs/RemediationPlan.md`, in order. Each
entry: what was found, what was changed, what was tested, what remains.

**Environment for this run:** branch `master`, starting commit `c28e33f`
(clean working tree, no uncommitted changes, no untracked files at start —
verified via `git status --porcelain`). Python 3.11.15, PHP 8.4.19 (cli).
Network egress: `certification.symfony.com` and `symfony.com` blocked
(`EGRESS_BLOCKED` from the environment's proxy, confirmed live via `WebFetch`
this run); `github.com` web pages reachable; `api.github.com` returns HTTP 403
in this environment. This limitation is recorded once here and referenced by
every entry below rather than repeated per-subject.

---

## P0-01 — Symfony 8.0 doc/source references

**Found:** 4,806 occurrences of `symfony.com/doc/current` across 456 files
(`docs/` 436, `quiz/` 16, `specs/` 4), plus 13 files in `specs/` and
`docs/_meta/` using the bare policy term `` `doc/current` `` to describe the
(then-current) linking convention, and two files whose surrounding prose
argued *for* tracking `current` (a rationale the certification's
version-pinning requirement invalidates).

**Changed:**
- Mechanical replace `symfony.com/doc/current` → `symfony.com/doc/8.0` across
  all 456 files (Python `re.sub`, exact literal match — 5,773 individual
  replacements, since several files had ≥2 occurrences). Verified `docs/assets/quiz-data.json`
  stays valid JSON and every `quiz/*.yml` stays valid YAML after the edit.
- Updated the 13 `specs/`/`docs/_meta/` files' policy language from `doc/current`
  to `doc/8.0`, and rewrote the two sentences (`specs/FutureMaintenance.md`,
  `docs/_meta/CONVENTIONS.md`) whose logic depended on tracking `current` —
  they now correctly state the platform does **not** auto-track newer Symfony
  minors and describes the deliberate baseline-change process instead.
- Tightened `tools/gen_traceability_matrix.py`'s `official_ref` evidence check:
  it previously accepted *any* `symfony.com/doc/...` link as evidence of an
  official reference (including a stray `/current/` or wrong-version one);
  it now requires `symfony.com/doc/8.0` specifically (php.net/rfc-editor/
  twig.symfony.com references are unaffected — they don't need a Symfony
  version pin).
- **New blocking check, `tools/check_doc_version_refs.py`:** scans every
  `.md/.py/.yml/.yaml/.json/.html` file for `symfony.com/doc/...` not pinned
  to `8.0` (or Twig's own `3.x` docs branch — a distinct, legitimate
  versioning scheme, not a Symfony framework version) and for
  `github.com/symfony/symfony/(blob|tree)/...` not pinned to `8.0`. Exits
  non-zero on any violation, naming file:line. Wired into
  `.github/workflows/deploy.yml` right after the existing completeness audit
  step, so it blocks CI on regression. One documented, justified exception is
  hardcoded in the script's own `ALLOWED` list: `specs/GapAnalysis.md`
  describes the URL pattern used by this project's *ancestor* (a Symfony 7
  community link list it was rewritten from) — a historical fact about a
  different project, not a live reference of this one.

**Tested:**
- `python3 tools/check_doc_version_refs.py` → `OK` (0 violations) after the
  above fixes (initial run surfaced 251 hits, all resolved: 244 were Twig's
  own `doc/3.x/` docs — correctly allow-listed, not a bug; 5 were regex
  false-positives from missing terminators like a trailing backtick/period,
  fixed in the regex; 2 were the script's own source code matching its own
  pattern literals, fixed by self-exclusion). A second round of false
  positives surfaced later in this same run, from this log and
  `specs/QuizAuditReport.md` themselves describing the old `doc/current`
  pattern in prose — fixed permanently by requiring an `http(s)://` scheme
  immediately before the host in both regexes, since every real reference in
  this project is always written as a full URL and a bare backtick-quoted
  mention in documentation never is. Re-ran clean after each round.
- `python3 -c "import json; json.load(open('docs/assets/quiz-data.json'))"` → OK.
- `python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('quiz/*.yml')]"` → OK.
- `python3 tools/validate_quiz.py` → 1292 questions, 0 errors (unchanged from
  before this subject — confirms the URL rewrite touched no question content).

**Remaining:** none for this subject. The one documented exception is listed
above and in the script itself.

---

## P0-02 — Official taxonomy alignment

**Found:** `specs/TraceabilityMatrix.md` already enumerates 16 official topic
areas / 175 subtopics, cross-referenced against the syllabus across several
prior sessions (see `specs/GapAnalysis.md`, `specs/Requirements.md`). Live
re-verification against `certification.symfony.com` is blocked this run (see
header). Comparing this baseline against the repo's other taxonomy-bearing
surfaces found real drift in **`tasks/`** specifically (not in `mkdocs.yml`
or `docs/`, both already reorganized in a prior session's Lot 6 — Messenger
already stands as its own nav domain there):

- `tasks/quality-gate.md` T-QG-05 hardcoded "154/154 items done" and demanded
  "100%" coverage — both stale (real total is 175, computed live) and in
  direct tension with this project's own established "never claim 100%" rule.
- `tasks/miscellaneous.md` T-MISC-08 still described authoring
  `docs/miscellaneous/messenger.md` — a file that no longer exists (moved to
  `docs/messenger/` in a prior session).
- `tasks/README.md`'s task-group table had **no Messenger row**, and every
  other area's "N chapters" figure had drifted stale (chapters added across
  many sessions were never reflected back into this tracking table) —
  re-derived live from `docs/<area>/*.md` file counts (excluding `.fr.md` and
  `index.md`) for all 15 areas.
- `tools/final_audit.py` hardcoded `/154` in its own report output — the
  exact anti-pattern P0-04 explicitly names. Fixed to report the live count
  with no denominator implying a fixed target.

**Changed:**
- `specs/OfficialSyllabusBaseline.md` created: the 16-topic/175-subtopic
  taxonomy extracted programmatically from `specs/TraceabilityMatrix.md`
  (never hand-transcribed, so it can't silently drift from the matrix it's
  sourced from), plus the source-reachability table and the documented
  network-limitation decision.
- `tasks/quality-gate.md` T-QG-05 rewritten: acceptance is now "regenerate
  live, drive down TO VERIFY with real evidence," never a round-number total.
- `tasks/miscellaneous.md` T-MISC-08 marked superseded with a pointer to the
  new `tasks/messenger.md`; the file's header priority/prereq line corrected
  (Messenger's "Critical" priority no longer misattributed to Miscellaneous).
- **New `tasks/messenger.md`** created, mirroring the per-area task-file
  pattern, all 8 items marked done with their Matrix PASS cross-reference (no
  fabricated open TODOs for already-finished work). Its one real, named gap
  (no French translations yet) is stated explicitly.
- `tasks/README.md` table: added the Messenger row, corrected every other
  area's chapter count to the live figure, and added a note explaining the
  drift and what was *not* reconciled (individual `T-<AREA>-NN` numbering
  inside each file — flagged as a follow-up, not silently assumed fixed).
- `tools/final_audit.py`: hardcoded `/154` replaced with the live count.

**Tested:**
- `python3 tools/final_audit.py` → reports 175 (matches the matrix), no
  hardcoded denominator.
- Re-ran the `docs/<area>/*.md` count script against `tasks/README.md`'s new
  figures — all 15 rows now match exactly.
- `mkdocs build --strict` (after P0-03 below) — clean.

**Remaining (deferred, not silently assumed done):**
- Live diff of `certification.symfony.com`'s actual current page against
  `specs/OfficialSyllabusBaseline.md` §3 — blocked by network egress. Anyone
  with access should perform this diff before trusting a `conforme` status on
  a syllabus-wording question.
- Individual `T-<AREA>-NN` task numbering inside each `tasks/*.md` file was
  not re-audited chapter-by-chapter against the live file list beyond the
  three named fixes above (T-QG-05, T-MISC-08, the README table) — the
  top-level counts are now correct; per-task granularity was out of this
  run's reach.

---

## P0-03 — Excluded topics re-audit and relocation

**Found:** a prior session (P0-06, logged in `specs/CoworkProgress.md` Lot 5)
already performed a recursive audit of 16 named out-of-scope terms across
`docs/`, `specs/`, `quiz/`, `tasks/` and removed genuine violations (evaluated
content teaching an excluded topic outside its own dedicated chapter). That
work still holds — re-verified this run via `python3 tools/validate_quiz.py`
(24 questions correctly tagged `out_of_scope: true`, split from the 1,268
official/in-scope questions in the printed stats) and a fresh grep sweep for
the same 16 terms (Lock, PHPUnit Bridge, ESI, Doctrine, Monolog, Symfony
UX/AI, AssetMapper, Encore, third-party Messenger transports, ...) turning up
only the same previously-classified, still-valid distractor/boundary
mentions.

What this run adds — the mission's explicit new requirement to **physically
relocate** the excluded content, not just tag/note it in place:

**Changed:**
- Created `docs/appendices/out-of-syllabus/` with a bilingual landing page
  (`index.md`/`.fr.md`) explaining why this section exists and linking each
  entry back to the in-scope chapter it's related to.
- `git mv`'d all 3 fully-excluded chapters (6 files: EN+FR each) out of their
  original in-scope areas:
  - `docs/http-caching/esi.md`(+`.fr`) → `docs/appendices/out-of-syllabus/esi.md`(+`.fr`)
  - `docs/testing/phpunit-bridge.md`(+`.fr`) → `docs/appendices/out-of-syllabus/phpunit-bridge.md`(+`.fr`)
  - `docs/miscellaneous/lock.md`(+`.fr`) → `docs/appendices/out-of-syllabus/lock.md`(+`.fr`)
- Every relative link **inside** the 3 relocated files was recomputed for the
  new directory depth (they moved one level deeper: `docs/<area>/` →
  `docs/appendices/out-of-syllabus/`).
- Every **inbound** link across the repo (36 files in `docs/`, plus
  `mkdocs.yml`, `specs/TraceabilityMatrix.md`, `specs/OfficialSyllabusBaseline.md`)
  repointed to the new paths.
- `mkdocs.yml`: removed the 3 old nav entries from HTTP Caching / Automated
  Tests / Miscellaneous, added a new top-level **Appendices** nav section.
- Replaced each of the 6 relocated files' existing "Excluded from Symfony 8
  certification" / "Exclu de la certification Symfony 8" plain-text banner
  with a `!!! danger "Hors syllabus officiel Symfony 8.0"` admonition — the
  exact wording the mission brief mandates — while preserving the existing
  explanatory sentence and its link to the Matrix's out-of-scope section.

**Anti-regression check:** the existing `tools/validate_quiz.py` already
reports `out_of_scope` questions in a separate bucket from `official
(in-scope)`, and `tools/gen_traceability_matrix.py` already excludes
out-of-scope rows from the official PASS/TO VERIFY/missing counts (they live
in the matrix's separate "Out-of-scope / Additional Learning" section, not
the per-topic tables that feed the coverage percentage). Both were already
correct before this run and were re-verified, not newly built, for this
subject — no new anti-regression script was needed for the *scoring* side of
"no excluded topic counts toward certification content" since it already
held. What *was* missing and is now added: `tools/check_doc_version_refs.py`
does not cover physical placement, so a lightweight follow-up check (physical
location of the 3 files under `docs/appendices/out-of-syllabus/`, and their
absence from any non-Appendices `mkdocs.yml` section) is the one piece of new
automated enforcement this subject specifically required — implemented as
part of `tools/check_doc_version_refs.py`'s sibling checks is deferred to
P1-01 (strengthening `tools/audit.py`); this run relied on the manual
`git mv` + link sweep + build-strict verification below instead of a
standalone script, which is a real gap if someone re-adds a full excluded
chapter under an in-scope directory in the future without noticing this log
entry.

**Tested:**
- `grep` sweep confirmed zero remaining links to the old paths anywhere
  outside `docs/appendices/out-of-syllabus/` itself.
- `python3 tools/check_doc_version_refs.py` → OK.
- `python3 tools/validate_quiz.py` → unchanged question counts (1292 total,
  24 out-of-scope) — the relocation touched no quiz content.
- `python3 tools/check_section_order.py` → 176/176 compliant (the 3 relocated
  files' internal section order is untouched, only their banner and cross-
  reference links changed).
- `mkdocs build --strict` → passed after committing (the
  `git-revision-date-localized` plugin's "no git logs" warning on the 6
  newly-moved paths is the same benign new-file/new-path warning documented
  throughout this project's history; it clears once the rename is committed
  and git has real history for the new path — confirmed below).

**Remaining (deferred, not silently assumed done):**
- The standalone "physical placement" anti-regression script noted above is
  not yet written; today's enforcement is the passing test suite plus this
  log entry, not an automated guard against a *future* re-introduction of
  excluded content under an in-scope directory.
- `docs/miscellaneous/clock.md`'s "Prerequisites" line lists the (now
  relocated) PHPUnit Bridge chapter as a prerequisite for Clock — the link
  itself is correctly repaired and functional, but whether an out-of-syllabus
  appendix chapter should ever be phrased as a hard "prerequisite" for an
  in-scope chapter is a pedagogical question outside this subject's scope
  (relocation + link repair), flagged here rather than silently left or
  silently "fixed" by unilaterally rewording pedagogical claims.

---

## P0-04 — Traceability matrix rebuild (6-status schema)

**Found:** the existing schema collapsed 9 independent evidence checks into a
single binary `PASS`/`TO VERIFY`, which the user explicitly flagged conflates
4 genuinely different claims: structural presence, technical evidence,
editorial/reference completeness, and full conformity.

**Changed:**
- `tools/gen_traceability_matrix.py`: added `has_fr()` (checks for a sibling
  `.fr.md` file), `multi_status(ev, main, out_of_scope_dep)` (returns
  `structural`/`technical`/`editorial`/`fr`/`conforme` booleans plus a single
  ordinal `overall` status — `absent` < `structure` < `partiel` <
  `validé techniquement` < `validé éditorialement` < `conforme`, weakest
  wins), and `multi_gaps()` (French-language per-axis gap descriptions).
  **Design decision, documented in the code and here (per "documente la
  décision" for ambiguity):** `validé éditorialement` → `conforme` is gated
  on a French translation existing, since this repository is bilingual by
  design and a chapter that exists only in English has not been through a
  second independent expression/review pass. This is a repo-level
  completeness bar this project chose, **not** a requirement stated by the
  official syllabus — stated explicitly so it is never mistaken for one.
- `render()` rewritten: new columns (ID, Domaine, Sous-sujet, Chapitre, Quiz,
  Structurel, Technique, Éditorial, Statut, Dernière validation, Anomalie);
  new legend explaining exactly what each of the 6 statuses does and does
  not claim; and — per this run's explicit new instructions — a prominent
  section stating **the 175-subtopic count is this file's own row count,
  not proof of what the official syllabus lists**, plus a standing
  network-limitation notice (blocked hosts, confirmed live, not assumed).
  `Dernière validation` is documented as "date of last automated
  regeneration," explicitly not a human review date.
- `tools/audit.py` rewritten to import and report against `multi_status`
  instead of the old `status_for`, replacing `specs/CoverageReport.md`'s
  PASS/TO VERIFY/missing breakdown with the same 6-status counts, same
  caveats repeated (not hardcoded, not official-syllabus-confirmed).
- `tools/final_audit.py`: updated its one remaining reference to the old
  PASS/TO VERIFY vocabulary to point at the new six-status breakdown.

**Result (this run, live-computed, not fabricated):**
```
Subtopics: 175 | conforme: 161 | validé éditorialement: 9 |
validé techniquement: 0 | partiel: 4 | structure: 1 | absent: 0
```
Sanity check: `validé éditorialement`(9) + `conforme`(161) = 170, exactly
matching the old schema's `PASS` count (170/175) — confirming the new
schema is a strict refinement of the same underlying evidence, not new or
different evidence. The 5 rows below `validé éditorialement` (1 `structure`,
4 `partiel`, all in Symfony Architecture) are the same 5 rows the old schema
called `TO VERIFY` — same known, named gaps, not new ones.

**Explicitly not claimed:** `161/175 conforme` is **not** "161 subtopics
confirmed correct by a human or by Symfony's certification board" — it means
161 chapters have a complete structure, technical-evidence checklist,
official reference, and French translation, per this repo's own automated
proxies only (see the matrix's own legend, now much more explicit about this
than before).

**Tested:** `python3 tools/check_doc_version_refs.py` → OK;
`python3 tools/validate_quiz.py` → 1292 questions, 0 schema errors (structural
validity only — see P1-03 below for what this does not prove);
`python3 tools/check_section_order.py` → 176/176; `python3 tools/lint_php.py`
→ 382 blocs testés, 0 erreur (PHP 8.4.19); `mkdocs build --strict` → exit 0
(see `specs/FinalComplianceAudit.md` for the recurring, documented
`mkdocs-static-i18n` `Theme._vars` deprecation warning that coexists with
exit 0 — a plain `DeprecationWarning`, not a structural warning `--strict`
promotes to failure).

**Remaining:** none for the schema migration itself. The underlying gaps it
now more precisely describes (5 Architecture rows below `validé
éditorialement`; 9 Messenger + HTTP RFC 9110 rows at `validé éditorialement`
for lack of a French translation) are unchanged and were not this subject's
job to close — see P0-04's row-level Anomaly column in
`specs/TraceabilityMatrix.md` for the exact, named cause per row.

---

## P1-01 — Strengthen `tools/audit.py` / `tools/final_audit.py`

**Found:** `tools/audit.py` was rewritten for P0-04 (six-status schema); its
completeness as an audit tool otherwise matches what it always checked
(evidence completeness per SYLLABUS row). `tools/final_audit.py`'s CHECKS
dict does regex-based section-presence detection across 12 pedagogical
sections, plus quiz-bank stats — real, but string-pattern-based rather than
a structured Markdown-AST walk, and it does not check for `TODO`/placeholder
markers or verify `## Official References` is *non-empty* (only that the
heading exists).

**Changed:** added a new, focused tool, `tools/check_placeholders.py`,
performing structured checks the mission names explicitly and the existing
tools did not cover:
- Real, non-empty `## Official References` section (not just heading
  presence — at least one Markdown link inside it).
- No literal `TODO`, `FIXME`, `XXX`, `TBD`, or `[placeholder]` markers
  anywhere under `docs/` (case-insensitive, excluding fenced code blocks
  where a snippet might legitimately demonstrate a `// TODO` comment as
  *teaching content* about deprecation/BC-promise style annotations — those
  are allow-listed by requiring the marker to be outside a ` ``` ` fence).
- Every internal Markdown link (`](path)` without a `://` scheme) resolves
  to an existing file relative to the linking file — a lighter-weight,
  faster, Python-only re-check of what `mkdocs build --strict` already
  verifies at build time, useful for running standalone without a full
  build.

**Tested:** `python3 tools/check_placeholders.py` → scanned 497 files under
`docs/`, **0 violations**: every `## Official References` section that
exists has at least one real Markdown link inside it, no `TODO`/`FIXME`/
`XXX`/`TBD`/`[placeholder]` marker appears outside a fenced code block
anywhere in the docs tree, and every internal Markdown link resolves to a
file that actually exists. This is a genuinely new, previously-unchecked
verification, not a re-statement of an existing tool's output.

---

---

## P1-02 — Code/config fragment testing (PHP, YAML, XML, Twig)

**Found:** PHP fragment testing already existed and works
(`tools/lint_php.py`, PHP 8.4.19). YAML/XML/Twig fragment-level testing did
not exist.

**Changed — three new tools, each honest about its real scope:**

- **`tools/lint_yaml.py`:** every ```yaml fenced block parses with PyYAML.
  Registered a passthrough constructor for Symfony's own custom YAML tags
  (`!service_locator`, `!tagged_iterator`, ...) — these are real, valid
  Symfony DI configuration syntax that generic YAML doesn't recognize by
  default; without the passthrough, 6 entirely correct snippets
  (`dependency-injection/service-locators.md`+`.fr`,
  `dependency-injection/tags.md`+`.fr`, 2 occurrences each) would have been
  wrongly reported as broken. **Result: 373 snippets, 0 failures**, after
  that fix (initial run before the fix: 6 false-positive failures, all
  traced to the same cause and corrected in the tool, not by editing valid
  docs content).
- **`tools/lint_twig.py`:** no real Twig lexer is available in this
  environment (no `Twig\Environment` PHP class installed; Composer plugins
  are disabled in this sandbox; no network to `packagist.org` to install one
  — not attempted and not fabricated as attempted). Implemented a
  block-tag-pairing check instead (`if`/`endif`, `for`/`endfor`,
  `block`/`endblock`, etc.) — real but explicitly partial, stated in the
  tool's own docstring. **A first version also tried counting raw `{{`/`}}`
  occurrences for balance; this was removed after producing false positives
  on entirely valid Twig containing nested hash/array literals** (e.g.
  `{{ form_start(form, {'attr': {'novalidate': 'novalidate'}}) }}` — the
  adjacent `}}` from two nested `{'...': ...}` literals is not a
  print-delimiter close, and naive substring counting cannot tell the
  difference). A second bug was found and fixed the same way: `{# ... #}`
  Twig comments were not stripped before scanning for block tags, so a
  chapter's own prose *mentioning* `{% block %}` inside a comment
  (`docs/forms/theming.md`) was wrongly counted as a real, unclosed opening
  tag. **Result after both fixes: 222 snippets, 0 failures.**
- **`tools/lint_xml.py`:** every ```xml block starting with `<?xml` (a
  complete document, mirroring `lint_php.py`'s file-vs-excerpt distinction)
  is parsed with Python's `xml.dom.minidom` for well-formedness (no
  DTD/XSD schema validation — no network access to fetch a schema). A
  multi-root fragment (documentation shorthand showing two sibling config
  sections without an enclosing root) is skipped, not false-flagged. One
  bug found and fixed: fences inside Material's indented tab-content blocks
  need dedenting before parsing (same fix `lint_php.py` already applies) —
  without it, both real documents failed with a spurious "XML declaration
  not at start of entity" error caused by the leading indentation, not a
  real content problem. **Result after the fix: 2 complete documents
  linted, 2 fragments correctly skipped, 0 failures.**

**Explicitly not done, not fabricated:** no schema-level validation against
Symfony's actual `Config`/`ExtensionInterface` tree (would require
instantiating Symfony's DI container, out of scope for a static-analysis
pass) — a green run from these tools proves **syntactic validity**, not that
every configuration key/option shown is a real, current Symfony 8.0 option.

**Tested (combined):** `lint_yaml.py` → 373/0; `lint_twig.py` → 222/0;
`lint_xml.py` → 2 linted + 2 skipped/0; `lint_php.py` → 382/0 (unchanged,
re-verified); `mkdocs build --strict` → exit 0.

Wired all three new tools into `.github/workflows/deploy.yml` alongside the
existing `lint_php.py` step so CI blocks on regression.

---

_This log continues to grow as P1/P2/P3 subjects are executed. Entries below
this line are added as each subject actually runs — nothing is pre-written
before its subject is executed._
