# Cowork Progress — Sf-8.0 Certification Quality

_Compact, durable log. Update after every lot instead of rescanning the repo._
_Branch: `claude/sf-8-certification-quality-iimd4l`. Both Lot 1 (`60c0814`) and
Lot 2 (`15d1f4c`) are committed AND pushed to origin. No PR opened (not asked)._

## Lot 2 — Official syllabus realignment (2026-08-26, second mission)

**Mission:** align the repo to the official Symfony 8 syllabus structure per an
explicit brief (13-column TraceabilityMatrix rebuild, PHP Attributes/Enums,
HTTP RFC 9110, missing component rows, dedicated Messenger topic, out-of-scope
purge, version-lock, overclaiming-language purge, final validations). Full
detail was given to the user as a structured final report at the end of this
lot — read that report (in the conversation, not duplicated here) before
resuming. This section is the durable summary for a future session.

**Network limitation (important, applies to everything below):**
`symfony.com`, `certification.symfony.com`, `www.php.net`, and
`www.rfc-editor.org` are all egress-blocked from this environment this
session. Only `github.com` (raw source + API, API sometimes 403s) was
reachable. Every fact in this lot that needed live verification was checked
against `symfony/symfony` source on the `8.0` branch (or `php/php-src` for
PHP-level facts) instead — never against the actual live syllabus/doc pages.
**A future session with web access to those domains should re-verify the
"Official Topic/Subtopic" wording in TraceabilityMatrix.md against the real
`certification.symfony.com/exams/symfony.html` page** — this lot could not.

**What changed (see the full Priority|File|Modification|Evidence|Result table
given to the user for the complete list):**
- `specs/TraceabilityMatrix.md` fully rebuilt: 13 mandated columns, 175
  official subtopics (was 154), each with real automated evidence
  (`tools/gen_traceability_matrix.py`, new) — 140 PASS (80.0%), 35 TO VERIFY
  including named gaps. A "Coverage summary" and "Out-of-scope / Additional
  Learning" section were added. `tools/audit.py` was rewritten to import from
  the same generator so `specs/CoverageReport.md` can never report a
  different number than the matrix again.
- New chapters (EN, + FR for the first two): `php-web-security/attributes.md`,
  `php-web-security/enums.md` (replacing a duplicated subsection in
  `php-api.md`, now a cross-reference), `http/rfc-9110.md` (**no FR yet**).
  Each verified against real source (PHP attribute stub files, Symfony's
  `Route` attribute flags, `BackedEnumValueResolver`, `EnumType`) and given
  2 new quiz questions each so they score PASS on real evidence, not just
  existing.
- Out-of-scope purge (bounded to what mission named explicitly): ESI,
  PHPUnit Bridge, Lock component chapters (EN+FR) now carry an explicit
  "Excluded from Symfony 8 certification" notice; their 24 quiz questions
  tagged `out_of_scope: true` (schema addition, `validate_quiz.py` updated
  to report official vs. out-of-scope counts separately). Intl's ICU-utility
  subsection (`Countries`/`Languages`/`Locales`/`Currencies`/`Timezones`)
  similarly marked excluded, and its mismatched source-reference link fixed
  (was citing `Translator::trans()`, now cites `Intl\Countries`).
- Version-lock: "current Twig 3.x" → "Twig up to 3.22" fixed in 6 real
  locations (source chapter EN+FR, quiz source, 3 generated echoes,
  hand-patched — no full `gen_*.py` regeneration, same caution as Lot 1).
  Swept for Symfony 8.1+/Twig 3.23+/PHP 8.5+ claims: none found.
- Overclaiming-language purge: "definitive", "100% syllabus coverage",
  "every official topic", "no deprecated APIs" replaced with the mandated
  sentence (or a softened equivalent) in `README.md`, `docs/index.md`,
  `mkdocs.yml` (site_description, EN+FR).
- Internationalization renamed to "Internationalization and localization" in
  nav + index pages (EN+FR).

**Lot 2 continued (same session, user asked "is it finished, if not continue"):**
Picked up the two remaining named gaps plus two real bugs found in
`gen_traceability_matrix.py` itself:
- **Bug fix:** `sf8_ref` evidence check only recognized `blob/8.0`, missing
  the equally legitimate `tree/8.0` (directory-level source links) and Twig's
  own `twigphp/Twig/blob/3.x` (Twig isn't part of symfony/symfony). Also
  `example` only checked ```php/yaml/console fences, missing ```twig/```http.
  Fixing both moved PASS from 140→168/175 **on re-measurement of already-
  correct content**, not by loosening the actual PASS criteria.
- **Correction, not new work:** the "Messenger → Events" gap claimed earlier
  was **wrong** — `miscellaneous/messenger.md` already covers
  WorkerMessageReceivedEvent/Handled/Failed/Running/Stopped/RateLimited with
  a diagram, listener example, and source ref. Only `SendMessageToTransportsEvent`
  (the dispatch-side event) was genuinely missing — added (EN+FR, verified
  against source) plus one quiz question. Matrix corrected to PASS.
- **New chapter:** `miscellaneous/property-access.md` (EN only, no FR yet) —
  `PropertyAccessor`/`PropertyAccessorBuilder`, getter order
  (`get`/`is`/`has`/`can`), magic-method opt-in defaults (`__get`/`__set` on,
  `__call` off), `NoSuchPropertyException`/`UninitializedPropertyException` —
  verified against source, 2 quiz questions added, wired into mkdocs nav.
- **Re-mapping, not fabrication:** `Controllers → FrameworkBundle` and
  `Routing → FrameworkBundle` were wrongly marked "no chapter" — a real,
  substantive subsection already exists in `architecture/components.md`
  ("How the framework composes them": extension pattern, config tree,
  compiler-pass pipeline, real cert question). Re-mapped there instead of
  authoring a duplicate chapter. Also re-mapped 4 newly-added "component"
  rows (TwigBundle, Form component, Console component, Misc HTTP-Caching
  cross-ref) from bare `index.md` landing pages to the chapter that actually
  carries their pedagogical anatomy.
- Added a missing `Source reference` note to `http-caching/client-side.md`
  (EN+FR) citing `ResponseHeaderBag::addCacheControlDirective()` — it
  discussed `Response` without ever citing where the behavior lives.

**Result: 170/175 (97.1%) PASS, 0 missing, 5 legitimately-unforced TO VERIFY**
(Architecture's Flex/License/Best-practices/Release-management/Roadmap —
meta/policy topics with no natural class to cite or code to show; deliberately
**not** padded with a fake citation just to flip the checkbox). Full validation
clean: `mkdocs build --strict` (0 real warnings), `lint_php.py` (378/0
failures), `check_section_order.py` (170/170), `validate_quiz.py` (1295
questions, 0 errors).

## Lot 3 — Messenger split into docs/messenger/ (same session, deploy branch)

Per user instruction, this and all following work landed directly on
`claude/symfony8-cert-platform-mgkdkr` (the repo's real default/deploy
branch — **there is no `master` branch in this repo**; the deploy workflow
(`deploy.yml`) triggers on `main` or `claude/symfony8-cert-platform-mgkdkr`,
and only the latter exists). Lot 1+2's branch
(`claude/sf-8-certification-quality-iimd4l`) was fast-forward-merged in
first, then all Lot 3 work committed straight to the deploy branch so each
push triggers a live-site rebuild.

**What changed:**
- Split `miscellaneous/messenger.md` (707 lines, one monolithic chapter) into
  `docs/messenger/{index,component,messages-handlers,middleware,transports,
  workers,retries-failures,events}.md` — 8 files, EN only (no FR yet), each
  with full chapter anatomy (own exercises/traps/cheat-sheet/certification
  questions), redistributing the original's already-verified content rather
  than re-deriving it. Old `miscellaneous/messenger.md`/`.fr.md` deleted.
- **Caught a real accuracy bug while writing `retries-failures.md`:**
  initially wrote an exact "1000/2000/4000 ms" retry-delay example, then
  verified against `FrameworkBundle/DependencyInjection/Configuration.php`
  and found the framework's default `retry_strategy.jitter` is **0.1** (±10%
  randomization) — not 0. Fixed the chapter and its quiz question to state
  the delays are only exact when `jitter: 0`, with jitter itself now taught
  as its own certification trap.
- Migrated 28 quiz questions from `quiz/miscellaneous.yml` into a new
  `quiz/messenger.yml`, re-tagged to the 7 new subchapters (re-classified 2
  questions' `type` from `internals`→`trap` where that was the more honest
  label, to get situational coverage on `component`/`middleware`).
- Fixed ~30 cross-reference links across ~15 files (EN+FR) that pointed at
  the old `miscellaneous/messenger.md` path — dependency-injection chapters,
  `http/httpclient.md`, `docs/glossary.md`, `docs/labs/miscellaneous.md`,
  `docs/miscellaneous/{clock,lock,mailer,process,serializer,index}.md`.
  Glossary entries were pointed at the *specific* new chapter (e.g. "Stamp"
  → `middleware.md`), not just the index.
- Reworded `miscellaneous/index.md` (EN+FR): removed the "Messenger is the
  flagship of this stage" framing, added the missing `PropertyAccess`
  chapter-list entry (existed in nav but not in the index's own bullet list
  — a gap from Lot 2), adjusted difficulty/time estimates now that Messenger
  left this stage.
- Regenerated exam/flashcard/sheet artifacts for `miscellaneous` + new
  `messenger`, plus the three `index.md` files, via the `gen_*.py` tools —
  then **reverted the other 13 areas'** regenerated exam/flashcard/sheet
  files back to their committed versions (same historical-drift risk as
  Lot 1/2: a full regen resurfaces pre-existing staleness unrelated to this
  lot) and hand-corrected the two index pages' question counts to match the
  reverted (not regenerated) per-area files. `docs/assets/quiz-data.json`
  and `quiz/flashcards.csv` were kept fully regenerated (global,
  machine-read artifacts — no realistic partial-patch path for those).
- `tools/gen_traceability_matrix.py`: fixed two more real measurement bugs
  found while re-checking Messenger rows — `sf8_ref` only recognized
  `blob/8.0`/`tree/8.0`, not Twig's own `twigphp/Twig/blob/3.x` (Twig isn't
  in symfony/symfony); `example` only recognized ```php/yaml/console fences,
  not ```twig/```http. Also re-mapped 4 rows to a more suitable Main Chapter
  than a bare `index.md` landing page (TwigBundle → `controller-rendering.md`,
  Form component → `creation.md`, Console component → `built-in-commands.md`,
  Misc HTTP-Caching cross-ref → `cache-types.md`) since those already carry
  full anatomy and the index pages don't.
- Added a missing `Source reference` note to `http-caching/client-side.md`
  (EN+FR), citing `ResponseHeaderBag::addCacheControlDirective()` — spotted
  while re-checking why that row scored TO VERIFY.

**Result: 170/175 (97.1%) PASS, 0 missing.** Same 5 legitimately-unforced
Architecture meta-chapter rows remain TO VERIFY (Flex/License/Best-practices/
Release-management/Roadmap — no natural source-code citation to add without
padding). Full validation clean: `mkdocs build --strict` (0 real warnings,
only expected "no git logs yet" noise on new files), `lint_php.py` (382/0
failures), `check_section_order.py` (176/176), `validate_quiz.py` (1295
questions, 0 errors, 15 quiz files now).

**Known new inconsistency from this lot (logged, not fixed):** the 13
untouched areas' printed exam/flashcard page counts (e.g. "PHP & Web
Security — 112 questions") now lag behind `docs/assets/quiz-data.json`'s
live count for the same areas, because the JSON was fully regenerated but
the printed pages were deliberately reverted to avoid absorbing unrelated
historical drift. This is the same historical-drift issue flagged in Lot 1
and Lot 2 — not new, just newly visible in one more place. Fixing it means
doing the "full quiz-bank reformat" item below, area by area, with review.

## Lot 4 — "Not an official exam" banner (same session, deploy branch)

Added `!!! danger "Not an official exam" / Practice question, not an
official exam question...` to all 15 `docs/exams/*.md`, all 15
`docs/revision/flashcards/*.md`, all 3 `docs/revision/mock-exam*.md`, and
`docs/exam-simulator.md`/`.fr.md` (hand-patched the already-generated files
directly — no regeneration, no drift risk). Baked the same block into the
generator templates (`gen_chapter_exams.py`, `gen_flashcards.py`,
`mock_exam.py`) so future regenerations keep it. `docs/revision/quiz.md`
already had an equivalent disclaimer ("Isn't: leaked or brain-dumped exam
items") — left as-is, not duplicated. Also fixed a stale "14 areas" ->
"15 areas" count in `exam-simulator.md`/`.fr.md` (Messenger is now its own
area). Validated clean: `check_section_order.py` (176/176),
`mkdocs build --strict` (0 warnings, no new-file noise this time — all
edits to already-committed files).

**Still NOT done (explicitly deferred — see matrix Anomaly column for
each):**
- Full quiz-bank reformat to the mission's mandated per-question fields
  (Official Topic/Subtopic, Scenario, Explanation-per-option, Pitfall,
  Symfony 8.0 Reference) across all ~1295 questions — not attempted; only
  the ~16 new/reclassified questions across all passes use that
  scenario-forward style. This is the single largest undone item in the
  brief, and now also the fix for the historical-drift inconsistency above.
- Recursive ecosystem term audit (Symfony UX/AI, Doctrine, Monolog,
  AssetMapper, Encore, third-party bundles) — counted only, not individually
  triaged file-by-file.
- Every pre-existing row marked PASS was checked by **automated evidence
  only** — no fresh line-by-line technical re-read beyond Lot 1's DI
  chapters and this pass's spot-checks. A PASS is not a blanket claim of
  verified factual accuracy.
- `http/rfc-9110.md`, `miscellaneous/property-access.md`, and all 8 new
  `docs/messenger/*.md` chapters still have no French translation.
- A live (non-`--offline`) `check_links.py` run has still never been done.

**Next task:** pick ONE of the "Still NOT done" items above per future lot.
Before starting, re-read `specs/TraceabilityMatrix.md`'s Anomaly column for
that row instead of rescanning the repo.

## Session baseline (2026-08-26)

Automated structural checks were run first and are **clean** (0 errors) —
do NOT re-run these unless the underlying files change:

- `tools/lint_php.py` → 372 PHP snippets, 0 failures.
- `tools/validate_quiz.py` → 14 files, 1284 questions, 0 schema errors, 100% subchapter coverage.
- `tools/audit.py` → 154/154 syllabus items fully covered.
- `tools/check_section_order.py` → 166/166 chapters compliant.
- `tools/check_links.py --offline` → 670 unique external URLs catalogued (not yet network-checked this session — no network check run; see "Next task").

**Design decisions confirmed intentional (do NOT "fix"):**
- Doc links use `symfony.com/doc/current/...` on purpose (tracks latest stable; documented in
  specs/Architecture.md, FutureMaintenance.md, MigrationPlan.md, Requirements.md FR-12). Source
  links correctly pin `github.com/symfony/symfony/blob/8.0/...` — verified the `8.0` branch is
  real and has releases through 8.0.16 (current actual stable is 8.1.5, per GitHub as of
  2026-08-26). This is a real, deliberate versioning policy, not a bug.

## Lot 1 — Technical accuracy pass: DI chapters explicitly named in the task's sources-of-vérité list

**Scope:** `controllers/value-resolvers.md`, `dependency-injection/{tags,service-locators,compiler-passes}.md`
(+ `.fr.md`), and every generated artifact that echoes their quiz questions
(`quiz/dependency-injection.yml`, `quiz/flashcards.csv`, `docs/assets/quiz-data.json`,
`docs/exams/dependency-injection.md`, `docs/revision/flashcards/dependency-injection.md`,
`docs/revision/mock-exam.md`).

**Verified accurate (cross-checked against symfony/symfony `8.0` branch source on GitHub):**
- `value-resolvers.md` — all 9 built-in resolver priorities (120/120/100×4/-50/-100/-150) and the
  2 targeted-resolver tags match `FrameworkBundle/Resources/config/web.php` exactly. ✅ No changes.
- `tags.md` — `#[AutowireLocator]` and `#[AsTaggedItem]` constructor signatures verified against
  source. ✅ No changes.

**Bugs found and fixed (technically incorrect information — priority #1):**

1. **`ServiceSubscriberTrait` deprecation version was wrong everywhere.** Docs/quiz said
   "deprecated in 6.4"; verified via the actual `@deprecated` docblock in
   `symfony/service-contracts` (`since symfony/contracts v3.5`) cross-referenced against tag
   dates (v3.5.0 tagged 2024-05-03, matching Symfony **7.1** released 2024-05-31, not 6.4/7.0
   which shipped with contracts v3.4). Fixed to "deprecated in 7.1 (symfony/contracts v3.5)" in:
   `dependency-injection/service-locators.md` + `.fr.md`, `quiz/dependency-injection.yml`
   (DI-LOCATOR-05), `quiz/flashcards.csv`, `docs/assets/quiz-data.json`,
   `docs/exams/dependency-injection.md`, `docs/revision/flashcards/dependency-injection.md`.

2. **Wrong `PassConfig` constant names in `compiler-passes.md`.** Doc/quiz used
   `TYPE_OPTIMIZATION` and `TYPE_REMOVING`; verified against `PassConfig.php` on the `8.0`
   branch — the real constants are `TYPE_OPTIMIZE` and `TYPE_REMOVE` (values `'optimization'`/
   `'removing'`, but the constant *names* differ from what was written — a real exam trap if
   memorized wrong). One quiz question (DI-PASS-05) even had this wrong name inside its
   **correct answer text**, not just a distractor. Fixed in: `compiler-passes.md` + `.fr.md`,
   `quiz/dependency-injection.yml` (DI-PASS-02, DI-PASS-05), `docs/exams/dependency-injection.md`,
   `docs/revision/flashcards/dependency-injection.md`, `docs/revision/mock-exam.md`,
   `docs/assets/quiz-data.json`. (`TYPE_BEFORE_REMOVING`/`TYPE_AFTER_REMOVING`, which are
   correct as written, were left untouched — confirmed no accidental substring collision.)

**Not yet checked this lot:** `service-locators.md` internals beyond the trait-version bug (rest
looked correct on read-through but wasn't independently source-verified line by line), and
`miscellaneous/runtime.md` / `testing/phpunit-bridge.md` (both named in the task's
sources-of-vérité list) — not opened yet.

**Process note (important for future lots):** `tools/gen_quiz_json.py`, `gen_flashcards.py`,
`gen_chapter_exams.py`, `gen_revision_sheets.py` regenerate **all 14 areas** in one run — there
is no per-area flag. Running them after a single-file quiz edit touched 49 files, because the
already-committed generated docs are **stale relative to `quiz/*.yml`** (e.g. `docs/exams/architecture.md`
jumped from 116 to 123 questions on a full regen — untouched by this lot). Do NOT run these
generators broadly to propagate a small fix; hand-patch the same string into the specific
generated files that echo it instead (as done above), and revert the rest with
`git checkout -- <paths>`. `quiz/flashcards.csv` is CRLF-encoded (Python `csv` module default) —
editing it with a text-editing tool that normalizes line endings corrupts ~100 unrelated lines
(diff noise on every embedded-newline CSV field); use a byte-level `open(path,"rb")` replace
instead, never Edit/Write on that file.

## Known issue logged, not yet fixed (do not re-discover, plan for it)

- **Generated artifacts are stale vs. the quiz bank.** `docs/exams/*.md`, `docs/revision/flashcards/*.md`,
  `docs/revision/sheets/*.md`, `docs/assets/quiz-data.json`, `quiz/flashcards.csv` were generated
  from an older state of `quiz/*.yml` — full regeneration adds/reorders hundreds of questions
  across all 14 areas at once (confirmed on `architecture`: +7 questions). This is a large,
  separate undertaking (every newly-surfaced question needs a technical-accuracy read before
  being allowed to stand) — do NOT run the 4 `gen_*.py` generators repo-wide to "fix" this in one
  shot. Treat as its own future lot, one area at a time, with review of the diff before keeping it.
- **FR translation gap, not just desync:** `docs/revision/flashcards/dependency-injection.fr.md`
  has no card at all for the ServiceSubscriberTrait question that exists in the EN deck — i.e.
  the FR flashcard deck is missing content, not just carrying a stale copy. Worth a dedicated
  translation-completeness lot (priority #6/#7 in the task's list) — likely repo-wide, not just
  this one card.
- `check_links.py` has not been run with real network access this session (only `--offline`
  catalogued 670 URLs). A live link-rot sweep is still owed (priority #3-adjacent maintenance).

## Lot 5 — P0-06 recursive out-of-scope audit

**Mission:** full recursive audit of `docs/`, `specs/`, `quiz/`, `tasks/` for 16 named
out-of-scope terms (Symfony UX, Symfony AI, Doctrine, Monolog, AssetMapper, Webpack Encore,
PHP Polyfills, String/Uid/TypeInfo components, Lock component, Doctrine/Redis transports,
Amazon SQS, ESI, PHPUnit Bridge). Per occurrence: authorized/unauthorized verdict +
justification. Remove all evaluated ("évalué") content on these subjects; keep only the
literal phrase "Excluded from Symfony 8 certification." as a residual mention.

**Method:** grep every term (precise patterns to avoid substring false-positives like
"design"/"ESI" inside "design"), classify each hit, fix violations, re-validate.

**Verdict pattern that held across ~180 occurrences checked:** the overwhelming majority
are AUTHORIZED — wrong-answer distractors naming an excluded technology (e.g. "D. Doctrine",
"RedisAdapter" as one of 4 cache-adapter options), explicit boundary-testing questions whose
correct answer confirms exclusion, brief factual naming (e.g. `render_esi` named alongside
`render`/`render_hinclude` as one of three `FragmentHandler` strategies, with no behavior/config
taught), and spec/task-tracker documentation whose entire purpose is declaring the exclusion
(`specs/Requirements.md` FR-5, `specs/GapAnalysis.md` §5, `specs/DefinitionOfDone.md`, etc.).

**Confirmed violations found and fixed (evaluated content leaking an excluded topic into an
in-scope subchapter/chapter):**

| # | File | What | Fix |
|---|---|---|---|
| 1 | `quiz/twig.yml` `TWIG-RENDER-02` | Tested ESI fallback behavior under `twig/controller-rendering` (in-scope subchapter, not the dedicated excluded ESI chapter) | Deleted the question |
| 2 | `quiz/twig.yml` `TWIG-RENDER-07` | Tested `framework.esi.enabled` config under the same in-scope subchapter | Deleted the question |
| 3 | `quiz/architecture.yml` `ARCH-DEP-03` | Tested "which tool fails the suite on deprecations" (PHPUnit bridge/`SYMFONY_DEPRECATIONS_HELPER`) under `architecture/deprecations` (in-scope) | Deleted the question |
| 4 | `docs/twig/controller-rendering.md`+`.fr.md` | Whole "Predict first/Reveal" block, YAML `esi: {enabled: true}` config, an exercise, and Certification-questions Q2 taught/tested ESI fallback + config as core chapter content | Trimmed to one factual line ("`render_esi` also exists… **Excluded from Symfony 8 certification**") + removed the ESI exercise/question, replaced with `render_hinclude` (in-scope) equivalents |
| 5 | `docs/architecture/deprecations.md`+`.fr.md` | A "Fail tests on deprecations" config tab, an Expert exercise, and Certification-questions Q3 taught/tested `SYMFONY_DEPRECATIONS_HELPER`/PHPUnit-bridge CI gating as Architecture content | Removed the tab/exercise/question/cheat-sheet & takeaway bullets; left one cross-reference line to the excluded PHPUnit-bridge chapter |
| 6 | `docs/http-caching/index.md`+`.fr.md` | Said "the exam probes… Edge Side Includes" (false — ESI is excluded) | Reworded to name only the in-scope tooling as exam-probed; added exclusion notice on the ESI micro-chapter bullet |
| 7 | `docs/testing/index.md`+`.fr.md` | Same overclaiming pattern ("the exam cares about… the PHPUnit bridge") | Reworded; added exclusion notice on the PHPUnit-bridge micro-chapter bullet |
| 8 | `docs/revision/cheat-sheet.md`+`.fr.md` | "ESI = `<esi:include>` fragments. *(Down-weighted in the Symfony 8 exam.)*" — implies ESI is tested, just less | Reworded: ESI is out of scope, excluded |
| 9 | `docs/revision/edge-cases.md`+`.fr.md` | Two `??? question` self-checks evaluated ESI fallback behavior and ESI-as-the-fix for fragment TTL capping | Both removed (kept the general TTL-capping fact only in `execution-order-codex.md`, which doesn't hinge on ESI specifically) |

All propagated to every generated echo that carried the deleted quiz questions:
`docs/exams/{architecture,twig}.md`, `docs/exams/index.md`, `docs/revision/flashcards/{architecture,twig}.md`,
`docs/revision/flashcards/index.md`, `docs/assets/quiz-data.json`, `quiz/flashcards.csv` (byte-level,
CRLF-safe), `docs/revision/mock-exam.md` (hand-patched, not regenerated — full regen would have
reshuffled the whole paper via the shared `random.Random` sequence, see the generator note above).
Only the touched areas' `*.md`/index lines were regenerated/hand-fixed; every other area's exam,
flashcard and sheet page was reverted with `git checkout --` to avoid resurfacing the pre-existing,
unrelated drift documented above. New counts: Architecture 122 (was 123), Twig 109 (was 111 before
this lot's 2 deletions, 104 in the already-stale generated echo before that).

**Notable finding flagged, not acted on unilaterally:** `docs/testing/deprecations.md`
("Automated Tests → Handling legacy deprecated code", `TraceabilityMatrix.md` row PASS, its
own quiz subchapter `testing/deprecations`, not tagged `out_of_scope`) is substantively built
on PHPUnit-bridge mechanics (`SYMFONY_DEPRECATIONS_HELPER` threshold buckets, baseline files,
`#[IgnoreDeprecations]`). This reads as a deliberate prior-session decision to treat
"deprecation-handling in tests" as its own legitimate Automated-Tests syllabus item, distinct
from "PHPUnit Bridge" (`SymfonyExtension` registration, clock/DNS mocking, `simple-phpunit`) —
but it is in tension with the blanket "PHPUnit Bridge excluded" instruction taken literally.
Left untouched (mature, matrix-tracked, PASS-status chapter with its own quiz bank) pending an
explicit decision from the user rather than unilaterally dismantling it.

**Residual mentions after this lot** (all AUTHORIZED — verified none teach/test the excluded
subject): distractor-only mentions of Doctrine/Monolog/Redis/AssetMapper/Webpack Encore/Lock
across `quiz/*.yml` and `docs/*.md`; boundary-declaration mentions in `specs/*.md` and
`tasks/*.md`; cross-reference links from in-scope chapters to the dedicated excluded chapters
(`http-caching/esi.md`, `testing/phpunit-bridge.md`, `miscellaneous/lock.md`), each of which
itself still carries its own "**Excluded from Symfony 8 certification.**" notice from Lot 2.
`specs/TraceabilityMatrix.md`'s Out-of-scope section note updated to record that this line-by-line
re-audit happened (previously said "not re-audited line-by-line this lot").

Validation after this lot: `validate_quiz.py` (1292 q, 0 errors, 157/157 subchapter coverage),
`lint_php.py` (382 snippets, 0 failures), `check_section_order.py` (176/176 compliant),
`mkdocs build --strict` (clean, both `en`/`fr`).

## Lot 6 — Pedagogical reorg + Learning Dashboard

**Mission:** rebuild navigation/order around a *real* dependency graph (not the syllabus order),
create a mandatory homepage "Learning Dashboard", keep chapter-template restructuring
conditional (not a blanket rewrite of all 176 chapters — too large/risky to apply blind).

**Real dependency graph, built from evidence already in the repo** (each area's own `index.md`
`Prerequisites:`/`Dependencies:` metadata — not guessed): extracted, tabulated, and found two
genuine defects where `mkdocs.yml`'s top-level nav had drifted out of sync with what the
chapters themselves declare:

- `Dependency Injection` sat *after* Controllers/Twig/Forms/Validation in the nav, even though
  Controllers/Routing/Twig's own `index.md` files list DI as a prerequisite. `docs/roadmap.md`'s
  own stage table already had this right (DI = stage 4, before Controllers = stage 5) — only the
  site nav had drifted.
- `Forms` sat *before* `Data Validation`, even though `forms/index.md` lists Validation as a
  prerequisite (Forms composes Twig + Validation).
- `Messenger` (split into its own area in Lot 3) was never re-sequenced: its real prereqs (DI,
  Console, Events) are met right after Console, but nav/roadmap still had it lumped at the very
  end via the old pre-split "Miscellaneous (Messenger up-weighted)" line.

Fixed all three in `mkdocs.yml` (pure nav reorder — no file moves, no URL/anchor changes; only
sidebar order and the Material `navigation.footer` Previous/Next links change) and in
`docs/roadmap.md`+`.fr.md` (renumbered 14→15 stages, gave Messenger its own stage 13, updated the
Mermaid dependency graph with real prereq arrows and an explanatory note, fixed stale counts:
"14 topic areas"→15, "1,284-question bank / 154 sub-topics"→1,292/157 matching
`validate_quiz.py`'s live output, "~55–75h"→"~57–78h" for the added Messenger stage).

**Learning Dashboard:** rebuilt `docs/index.md`+`.fr.md` (root URL preserved) around a big table,
grouped into the mandated five buckets (Fondations / Cœur Symfony / Composants applicatifs /
Révision Certification / Hors programme), one row per official topic area (15 + the
Traceability-Matrix-tracked "Internationalization and localization" sub-topic, honestly shown
with empty cells rather than fabricated links since it has no dedicated lab/flashcard/exam file).
Columns: # (from the graph), Status (live PASS/TO-VERIFY counts from
`specs/TraceabilityMatrix.md`), Prerequisites, then links to Cours (chapter index — exercises
live inside chapters, no separate exercises-only page exists per area, noted explicitly),
TP (`labs/<area>.md`), Quiz (`exam-simulator.md`, same interactive tool for every row, filterable
client-side), Flashcards, Exams, Révision (`revision/sheets/<area>.md`). Kept all pre-existing
"What this is / Who it's for / How to use / Exam facts / Scope" content, folded the old "Scope"
in/out lists into cross-references to the new Dashboard sections instead of duplicating them.

**Self-caught regression, fixed before commit:** trimming the PHPUnit-bridge tangent out of
`docs/architecture/deprecations.md` in Lot 5 (P0-06 audit) had removed the chapter's *only*
Symfony-8.0-pinned source-reference link (the PHPUnit bridge one) without replacing it, dropping
`architecture/deprecations.md` from PASS to TO VERIFY in `tools/audit.py`'s automated evidence
count (170→169). Fixed by citing `Definition::setDeprecated()` — a class the chapter's own
compile-time code example already uses — pinned to `symfony/symfony` `8.0`, in both EN/FR.
Restored to 170/175 PASS after regenerating `specs/TraceabilityMatrix.md` (single-file, always-
regenerate-in-full generator — not an echo file, so no historical-drift risk from running it).

**Also fixed while sweeping for consistency:** stale "14 areas/topics" wording in
`exam-guide/index.md`+`.fr.md`, `exam-guide/format.md`+`.fr.md`, `revision/cheat-sheet.md`+`.fr.md`
→ 15. `revision/cheat-sheet.md`'s own numbered sections were still 1–14 with Messenger's facts
folded as a bullet inside the Miscellaneous section (pre-split leftover) — split it into its own
`## 13. Messenger` section (renumbering Automated Tests→14, Miscellaneous→15) in both languages.

**Left alone, flagged rather than silently patched:** `revision/edge-cases.fr.md` (and its EN
twin) says its 79-question drill deck covers "14 syllabus areas" — checked, and this is true: the
deck has zero Messenger questions (predates the Lot 3 split). Bumping the number to 15 without
adding Messenger content would overclaim coverage that doesn't exist; left as an honest, named
gap for a future content-authoring lot rather than "fixed" cosmetically.

**Explicitly out of scope for this lot (too large/risky to blanket-apply):** rewriting all 176
chapters into the newly-specified 17-section template. `check_section_order.py` already enforces
a consistent section order across 100% of chapters under the *existing* template; migrating to a
different template repo-wide is a large, separate content-authoring undertaking that needs
per-chapter review, not a mechanical nav/metadata change — flagged for the user rather than
attempted blind.

Validation: `check_section_order.py` (176/176), `validate_quiz.py` (1292 q, 0 errors, 157/157),
`lint_php.py` (382/0), `tools/audit.py` (170/175 PASS, 5 TO VERIFY, 0 missing — restored, see
regression note above), `mkdocs build --strict` (clean, en+fr, including the two broken-anchor
warnings on the new Dashboard page that were caught and fixed — emoji headings strip to no
leading hyphen in the generated slug).

## Next task

Pick up with: open `miscellaneous/runtime.md` (still on the task's explicit sources-of-vérité
list, not yet read this session), verify against `symfony/symfony` `8.0` branch source, fix any
confirmed errors the same way (source file + every generated echo, hand-patched, never a full
`gen_*.py` rerun). Then continue down the priority list per-lot: next bad-quiz-answer sweep on
another area's `quiz/*.yml`, a real (non-`--offline`) `check_links.py` run, the
`docs/testing/deprecations.md` scope question flagged in Lot 5, and the `revision/edge-cases.md`
Messenger-drill-questions gap flagged in Lot 6.
