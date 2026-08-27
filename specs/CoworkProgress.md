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

**Still NOT done (explicitly deferred — see matrix Anomaly column for
each):**
- Full quiz-bank reformat to the mission's mandated per-question fields
  (Official Topic/Subtopic, Scenario, Explanation-per-option, Pitfall,
  Symfony 8.0 Reference) across all ~1295 questions — not attempted; only
  the ~16 new/reclassified questions across all passes use that
  scenario-forward style. This is the single largest undone item in the
  brief, and now also the fix for the historical-drift inconsistency above.
- The "Practice question, not an official exam question" banner — still not
  added anywhere.
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

## Next task

Pick up with: open `miscellaneous/runtime.md` and `testing/phpunit-bridge.md` (still on the
task's explicit sources-of-vérité list, not yet read this session), verify against
`symfony/symfony` `8.0` branch source + `symfony/doc/8.0/components/phpunit_bridge.html` /
`runtime.html`, fix any confirmed errors the same way (source file + every generated echo,
hand-patched, never a full `gen_*.py` rerun). Then continue down the priority list per-lot:
next bad-quiz-answer sweep on another area's `quiz/*.yml`, then a real (non-`--offline`)
`check_links.py` run.
