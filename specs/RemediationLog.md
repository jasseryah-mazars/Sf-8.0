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

**Tested (combined):** `lint_yaml.py` → 373 blocs YAML testés, 0 erreur;
`lint_twig.py` → 222 blocs Twig testés, 0 erreur (appariement des balises
uniquement); `lint_xml.py` → 2 documents complets testés + 2 fragments
ignorés (non des erreurs), 0 erreur; `lint_php.py` → 382 blocs PHP testés,
0 erreur (inchangé, re-vérifié — ce chiffre mesure le nombre de blocs
passés au linter, pas le nombre total de blocs de code du site, et ne
prouve que l'absence d'erreur de syntaxe PHP détectée par ce script, pas
l'exactitude fonctionnelle du contenu); `mkdocs build --strict` → code de
sortie 0 (le `DeprecationWarning` tiers documenté ci-dessus reste présent
dans les logs de build malgré le code 0 — voir `specs/FinalComplianceAudit.md`).

Wired all three new tools into `.github/workflows/deploy.yml` alongside the
existing `lint_php.py` step so CI blocks on regression.

---

## P1-03 — Full quiz audit: near-duplicate detection

**Source added:** `tools/check_quiz_duplicates.py` (new). **Method, stated
honestly:** normalizes each of the 1 292 questions' stem text (lowercase,
strip punctuation, tokenize, drop a small stopword list), then computes
pairwise **Jaccard token-set similarity** between every pair of questions
(with a cheap size-ratio pre-filter to keep the O(n²) comparison tractable).
This is a **lexical-overlap heuristic, not semantic understanding** — it
cannot recognize two differently-worded questions that test the same fact,
and it can flag two questions that are legitimately different but share a
lot of template phrasing. The script does not fail CI; every reported pair
is explicitly labeled a *candidate* requiring human review, never asserted
as a confirmed duplicate by the tool itself.

**Run (threshold 0.75):** `checked 1292 questions, 833986 pairs,
threshold=0.75: 17 candidate near-duplicate pair(s)`.

**Human review of all 17 candidates:**
- **16 pairs were legitimate, not duplicates.** Nearly all shared the same
  template stem across different topics — e.g. "Which of the following
  statements are true about the Symfony `X` component?" repeated for
  different values of `X` (Routing, Validator, Messenger, …) — same
  sentence shape, entirely different tested content and answer options.
  These were read individually and confirmed as distinct questions, not
  batch-dismissed on the pattern alone.
- **1 pair was a genuine near-duplicate:** `MISC-DEPLOY-03`
  (`quiz/miscellaneous.yml`) and `PHP-EXT-09` (`quiz/php-web-security.yml`)
  both tested `opcache.validate_timestamps=0` with near-identical wording
  and the same "why set it" framing, differing mainly in which chapter they
  sat in.

**Fix applied to `PHP-EXT-09`:** reworded from asking *why* the setting is
used (already `MISC-DEPLOY-03`'s question) to a complementary
consequence/trap angle — *what happens if you deploy code but forget to
reset OPcache* — testing a different, non-overlapping fact (that OPcache
silently keeps serving stale bytecode with no error) rather than repeating
the rationale for the setting. `type` changed from `internals` to `trap`
to match the new question shape (confirmed in `validate_quiz.py`'s
type-count breakdown: `trap` 216→217, `internals` 201→200).

**Propagated to every derived copy of this question** (hand-patched, not
regenerated — a full `gen_chapter_exams.py` run for this one change
resurfaced ~270 lines of pre-existing, unrelated historical drift between
the committed exam file and the current quiz source; that regeneration was
reverted with `git checkout --` and the specific block was hand-edited
instead, per this project's established practice):
- `quiz/php-web-security.yml` — source of truth, edited directly.
- `docs/exams/php-web-security.md` — Q106 block hand-patched to match.
- `docs/revision/flashcards/php-web-security.md` — card 89 hand-patched.
- `docs/assets/quiz-data.json` — fully regenerated via `tools/gen_quiz_json.py`
  (safe: single combined file, no historical-drift risk) and the new text
  verified present.
- `quiz/flashcards.csv` — this file is CRLF-encoded; edited via a
  byte-level script (never through a text editor, which would silently
  normalize ~100 unrelated lines' line endings) and re-verified after the
  edit by re-parsing the whole file with Python's `csv` module (1 293 rows:
  1 header + 1 292 questions, unchanged count) and spot-checking that the
  target row now carries the new question and explanation text.

**What this does and does not prove, stated explicitly per the mission's
caveat:** `validate_quiz.py` passing (1292 questions, 0 error(s)) after this
change demonstrates the quiz bank's **structural validity** — every
question has the required fields, a syllabus tag, correct-answer count,
etc. — it does **not** demonstrate that the other 1 291 questions are
individually fact-checked against the official Symfony 8.0 documentation;
that remains outside what any script in this repository can verify without
network access to the official sources, and outside what was re-verified in
this pass (only the one edited question was re-checked against
`php.net/manual/en/opcache.configuration.php`, which reachable per the
standing network-limitation notice in `specs/TraceabilityMatrix.md`).

**Tested:** `check_quiz_duplicates.py` → 17 candidats, 1 doublon réel
corrigé; `validate_quiz.py` → 1292 questions, 0 erreur (validité
structurelle uniquement); `mkdocs build --strict` → code de sortie 0.

Wired `check_quiz_duplicates.py` into `.github/workflows/deploy.yml` as a
non-blocking informational step (documented as such in the workflow step
name), consistent with the script's own stated scope.

---

## P1-05 — CI hardening

**Bug found and fixed first (via a new consistency check, not by manual
inspection):** `tools/gen_traceability_matrix.py`'s `OUT_OF_SCOPE` table
still referenced the *pre-P0-03* paths for the three excluded chapters
(`http-caching/esi.md`, `testing/phpunit-bridge.md`, `miscellaneous/lock.md`)
even though P0-03 physically moved those files to
`docs/appendices/out-of-syllabus/` several commits ago. `specs/
TraceabilityMatrix.md`'s "Out-of-scope / Additional Learning" section was
therefore pointing at paths that no longer exist. Fixed by updating the
three table entries to the current `appendices/out-of-syllabus/*.md` paths
(with a note on where they moved from), and regenerating the matrix.

**New source:** `tools/check_exclusions.py` — checks, for each of the 3
excluded chapters, that (1) its `.md`/`.fr.md` files exist under
`docs/appendices/out-of-syllabus/`, (2) both carry the explicit "Hors
syllabus officiel Symfony 8.0" admonition, (3) `mkdocs.yml`'s nav lists them
only inside the `Appendices` block, never earlier (i.e. not mixed into the
main syllabus nav), (4) every quiz question whose `subchapter` matches one
of the three is tagged `out_of_scope: true`, and (5)
`specs/TraceabilityMatrix.md`'s own exclusions section still names all
three at their current path. **Result after the path fix above: 0
inconsistencies.** Wired into CI as a **blocking** step (this is exactly
the kind of drift that should fail a build, not just get noticed by an
occasional human read).

**New source:** `tools/check_report_freshness.py` (also serves P1-04) —
wired into CI as an **informational, non-blocking** step. It is
deliberately not blocking: every report it checks necessarily names its
own *parent* commit (the commit that embeds the stamp doesn't exist until
after generation), so a freshly-committed report reads "stale" for exactly
one commit by construction — making it blocking would fail every push that
touches a report, which is not a real problem to catch.

**CI trigger/deploy scope fixed:** `.github/workflows/deploy.yml` only
triggered on `main`/`master`/`claude/symfony8-cert-platform-mgkdkr` — it did
not cover this mission's actual working branch,
`claude/sf-8-certification-quality-iimd4l`. Added that branch to the `push`
trigger and to both the artifact-upload and deploy `if` conditions, so a
push to this branch (as this mission's final step requires) actually runs
CI and deploys to Pages, instead of being silently skipped.

**Also discovered and corrected while reviewing this:** the working
checkout had drifted onto `master` at some point in this multi-session
mission instead of the harness-designated
`claude/sf-8-certification-quality-iimd4l` branch. Confirmed via
`git merge-base --is-ancestor` that `origin/claude/sf-8-certification-
quality-iimd4l`'s tip (`3d81b56`) is a strict ancestor of `master`'s current
HEAD — i.e. `master`'s history is a pure fast-forward continuation of that
branch's already-pushed tip, with no divergent/conflicting commits. Moved
the local `claude/sf-8-certification-quality-iimd4l` branch pointer forward
to `master`'s HEAD (a fast-forward, not a rewrite — nothing on the
already-pushed branch tip was discarded or altered) and switched the
working checkout to it. All work from this point in the mission onward
happens on the correctly-designated branch.

**Existing CI already covers, reviewed and kept as-is:**
- Blocking: `tools/audit.py` (fails only on a genuinely `absent` mapped
  chapter), `tools/check_doc_version_refs.py`, `tools/validate_quiz.py`,
  `tools/lint_php.py`/`lint_yaml.py`/`lint_twig.py`/`lint_xml.py`,
  `tools/check_placeholders.py`, `mkdocs build --strict`.
- Report-only/non-blocking, by design (each documented in its own
  docstring as a heuristic, not a ground-truth check): `tools/
  check_quiz_duplicates.py`, `tools/check_section_order.py`, `tools/
  check_links.py --offline`.
- **Permissions:** already minimal at the workflow level (`contents: read`,
  `pages: write`, `id-token: write` — no broader scope, no job-level
  overrides). **Secrets:** none referenced anywhere in the workflow.
- **Version pinning:** third-party Actions are pinned to major-version tags
  (`actions/checkout@v4`, `actions/setup-python@v5`, `shivammathur/
  setup-php@v2`, `actions/upload-pages-artifact@v3`, `actions/
  deploy-pages@v4`) and `python-version: "3.12"` / `php-version: "8.4"` are
  explicit, not floating `latest`. Full commit-SHA pinning (vs. major-version
  tags) was considered and not applied — it is stronger supply-chain
  hardening but wasn't asked for and adds real maintenance burden (every
  Action update needs a new SHA); documented here as a deliberate choice,
  not an oversight, should a future session want to tighten it further.

**Tested:** `check_exclusions.py` → 0 inconsistencies (after the path fix);
full suite re-run end to end (`audit.py`, `check_doc_version_refs.py`,
`validate_quiz.py`, `check_quiz_duplicates.py` → 16 pairs now, down from 17
— confirms the P1-03 fix removed exactly the one real duplicate,
`gen_quiz_json.py`, `check_section_order.py`, `check_links.py --offline`,
`lint_php.py`/`lint_yaml.py`/`lint_twig.py`/`lint_xml.py`,
`check_placeholders.py`, `check_report_freshness.py`) — all clean;
`mkdocs build --strict` → exit 0 (theme `DeprecationWarning` still present
in the log, still documented, still not a structural MkDocs failure).

---

## P2-01 — Editorial structure normalization

**New source:** `tools/check_editorial_structure.py` — three checks not
already covered elsewhere:
1. **Nav <-> docs consistency:** every `docs/**/*.md` file (excluding
   `mkdocs.yml`'s own `exclude_docs: _meta/` and the per-chapter generated
   `exams/`/`revision/` pages, which are reached via their own hub index,
   not individually nav-listed) must be reachable from `mkdocs.yml`'s
   `nav:` tree, and every nav entry must point at a file that exists.
2. **Balanced code fences:** every file's ` ``` ` markers must come in
   pairs (an unclosed fence breaks rendering for the rest of the page).
3. **No heading with an empty subtree:** a heading is flagged only if
   *nothing* — not even a deeper subheading and its content — appears
   before the next heading at the same or shallower level (so a `## Deep
   Dive` immediately followed by `### The wrapping model` and a Mermaid
   diagram is correctly NOT flagged; only a truly empty stub is).

**First run found 83 violations, 82 of which were the same class of bug,
traced to its actual source and fixed there (not patched in the output):**
`tools/gen_revision_sheets.py`'s file glob (`docs/<area>/*.md`) picked up
every chapter's `*.fr.md` sidecar in addition to its `.md` file, and its
`index.md`-only exclusion check missed `index.fr.md` (`"index.fr.md"
.endswith("index.md")` is `False`). Two consequences, both real, both
present in every one of the 15 generated revision sheets, not just the one
`check_editorial_structure.py` happened to flag as empty:
- Every chapter's content appeared **twice** in its area's revision sheet —
  once from the French file, once from the English file, under the same
  `## Heading` — silently doubling every "cheat sheet" with untranslated
  French prose mixed into what is meant to be the English page.
- `docs/miscellaneous/index.fr.md`'s H1 ("Miscellaneous Components") leaked
  in as a spurious heading with zero content (index pages have no "Key
  takeaways"/"Last-minute revision" sections to extract) — this is the one
  `check_editorial_structure.py`'s empty-section check actually caught;
  the French-duplication half of the bug required reading the diff, not
  just the automated check, to notice.

**Fix:** excluded both `*.fr.md` (all of them, not just the index) and
`index.fr.md` explicitly from the glob in `tools/gen_revision_sheets.py`,
then regenerated all 15 sheets. **Verified: every area's sheet now has
exactly one `## ` section per non-index, non-French chapter file** (counted
file-by-file, 15/15 areas match exactly — e.g. `dependency-injection`:
14 chapters, 14 sections; `security`: 16/16; full table checked, not
sampled). `check_editorial_structure.py` re-run: 0 violations across all
three checks.

**What this does not do:** rewrite or re-validate the *content* of the
now-deduplicated sheets against the source chapters beyond the count-match
above — the extracted text itself was already correct English prose before
this fix (the bug was inclusion of extra unwanted sections, not corruption
of the wanted ones), so a full content re-read was not required to close
this specific defect, but is not claimed here either.

Wired `tools/check_editorial_structure.py` into
`.github/workflows/deploy.yml` as a **blocking** step.

**Tested:** `check_editorial_structure.py` → 0/0/0 violations across all
three checks; `validate_quiz.py` → 1292/0 (unaffected — this fix touches
`docs/revision/sheets/` only, not `quiz/`); `check_placeholders.py` → OK;
`mkdocs build --strict` → exit 0.

---

## P2-02 — README and documentation corrections

**Verified, not assumed:** all 24 non-external links in `README.md` were
extracted and checked against the filesystem with a small script (not by
eye) — 0 broken. No stale hardcoded coverage percentage was found in
`README.md` to begin with (it already only linked to the matrix rather
than quoting a number) — checked, not taken on faith.

**Fixed — stale exclusion list:** `README.md`'s "Out of scope" section
only listed the "never taught" ecosystem items (Symfony UX/AI, Doctrine,
Monolog, AssetMapper, Encore, third-party bundles) inherited from the
project's original `GapAnalysis.md` scoping. It did not mention the three
chapters (ESI, PHPUnit Bridge, Lock component) that P0-03 physically moved
to `docs/appendices/out-of-syllabus/` earlier in this run, nor the
additional in-chapter exclusions (third-party Messenger transports, Intl
ICU utilities) already documented in `specs/TraceabilityMatrix.md`'s
"Out-of-scope / Additional Learning" section. Expanded the README section
to mention both, link to the appendices index and the matrix section, and
name `tools/check_exclusions.py` (P1-05) as the mechanism keeping them in
sync going forward. `CONTRIBUTING.md`'s equivalent scoping paragraph
updated the same way, so a contributor reading either file gets the
complete picture.

**Fixed — overclaim risk in the "Coverage tracked and validated" bullet:**
reworded to name the six-status schema explicitly (per this run's user
caveat: a bare "coverage tracked" claim invites reading it as officially
verified) and to point readers at the matrix's own "What the [N]-subtopic
count is, and is not" section before they quote a percentage anywhere,
rather than letting the README imply a stronger guarantee than the matrix
itself claims.

**Not changed, reviewed and found accurate:** the "Exam facts (Symfony 8)"
table (75 questions/90 minutes/Advanced-Expert split) is sourced and cited
inside `docs/exam-guide/index.md`'s own "Official References" section
(fetched in a prior session when `certification.symfony.com` was reachable
— this run's network access to that domain is confirmed blocked, so it was
not and could not be re-fetched this run; the existing citation was
checked for presence, not re-verified against a live fetch). The local-dev
command block (`python -m venv`, `pip install -r requirements.txt`,
`mkdocs serve`) matches `requirements.txt` and was exercised indirectly
all run via the repeated `mkdocs build --strict` calls in every other
subject's testing step.

**Tested:** README/CONTRIBUTING link check (script, 24/24 resolve);
`validate_quiz.py`, `check_placeholders.py`, `check_editorial_structure.py`
all clean; `mkdocs build --strict` → exit 0.

---

## P2-03 — Site quality (real browser testing, not a heuristic)

This environment has Chromium + Playwright pre-installed, so unlike the
YAML/Twig/XML linters earlier in this run (necessarily heuristic — no real
parser available), this subject was tested with an actual headless
browser and axe-core, not simulated. New tools: `tools/check_site_quality.py`
(Python orchestrator: serves `site/`, invokes the Node script, relays its
result) + `tools/_site_quality_check.js` (Playwright + axe-core, launches
real Chromium against 5 sampled pages) + `tools/package.json`
(axe-core@4.13.0 as the one dev dependency; `tools/node_modules/`
gitignored). Full narrative, every finding, every fix and every
deliberately-not-fixed item with its reasoning: `specs/SiteQualityReport.md`
— summarized here:

**Fixed (3, each verified before/after with a fresh axe-core run):**
1. Task-list checkbox labels (critical, 9 nodes on the sampled page) —
   `pymdownx.tasklist`'s `custom_checkbox: true` output wraps each checkbox
   in a `<label>` with no text of its own; these checkboxes are always
   `disabled` (decorative bullets, never interactive), so the WCAG-correct
   fix is `aria-hidden="true"`, not an invented label. New
   `docs/assets/a11y.js` applies it, using the same `document$`-subscribe
   pattern `quiz.js` already uses for instant-navigation compatibility.
2. Light-scheme code-highlighting contrast (serious, 34 nodes) —
   comment/variable/operator/punctuation tokens measured 4.48:1 (need
   4.5:1) against the code background. Scoped override in
   `docs/assets/code.css` darkens just those five tokens inside
   `.md-typeset .highlight`, leaving the shared theme variable untouched
   everywhere else it's used.
3. Dark-scheme code-highlighting contrast (serious, 10 nodes) — number and
   constant tokens measured 4.45:1/4.48:1 against the dark code background;
   same file, dark-scheme-scoped override.

**Found, documented, deliberately not fixed (3)** — each traces to either
a stock Material template internal (`aria-dialog-name` on the search
dialog; one `landmark-unique` finding) or the site's `primary: black` /
`accent: indigo` palette choice (`link-in-text-block` +the remaining
`color-contrast` findings, all on the same `<small>` in-text links) — fixing
the latter properly means a visible, sitewide link-color/underline change,
which is a design decision for whoever owns the project's branding, not
something to make unilaterally mid-run. Both categories get a concrete,
ready-to-implement recommended fix in the report.

**Investigated in depth, left explicitly unresolved (2)** — not rounded up
to "fixed" or down to "broken," per this run's explicit anti-fabrication
instruction:
- **Search result rendering.** Typing a query (and separately, navigating
  to Material's own `/?q=` URL entry point) left the results list empty in
  this headless environment. Not accepted at face value: intercepted the
  actual `postMessage` traffic to/from Material's search Web Worker, which
  showed the worker receives the query, initializes its index correctly,
  and **returns 23 correct matching documents** — the backend is
  provably correct. Only the on-page DOM update never happened, in every
  variant tried. No network path exists from this environment to a vanilla
  mkdocs-material install to run the same test as a control (confirmed via
  a failed fetch, not assumed), so there is no way here to tell "real
  front-end bug" apart from "headless-Chromium rendering-pipeline quirk."
  Reported exactly that way — a human should confirm with a real query in
  a real browser on the live site before this is called a defect.
- **Mermaid rendering.** This site loads Mermaid from
  `https://unpkg.com/mermaid@11` (a CDN, not bundled locally); this
  environment's network egress proxy blocks/fails TLS for `unpkg.com`
  (confirmed via a failed-request listener), so Mermaid.js never loads
  here and diagrams cannot be verified to render, one way or the other.
  Noted as a general resilience point regardless: an external-CDN
  dependency for a core rendering feature is one outage/firewall block
  away from failing for a real visitor too — bundling Mermaid locally is
  the fix, but is a build-pipeline change out of this pass's scope.

**Why not wired into CI:** needs a Chromium download + `npm install` (real
CI cost), and its two hardest findings need human judgment to interpret,
not a pass/fail gate — kept as an on-demand local tool. Documented as a
deliberate scoping decision in the report, not an oversight.

**Tested:** `check_site_quality.py` end-to-end run before the fixes (18
total flagged issues across 5 pages) and after (15; the drop is
concentrated in the fully-resolved `label` rule and the two contrast
fixes, not a page-count change — the theme-level findings are unaffected,
as expected); `validate_quiz.py`, `check_placeholders.py`,
`check_editorial_structure.py` all clean after the `docs/assets/a11y.js` +
`docs/assets/code.css` + `mkdocs.yml` changes; `mkdocs build --strict` →
exit 0.

---

_This log continues to grow as P1/P2/P3 subjects are executed. Entries below
this line are added as each subject actually runs — nothing is pre-written
before its subject is executed._
