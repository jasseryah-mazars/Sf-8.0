# Cowork Progress — Sf-8.0 Certification Quality

_Compact, durable log. Update after every lot instead of rescanning the repo._
_Branch: `claude/sf-8-certification-quality-iimd4l`. No commits/pushes made (per task INTERDICTIONS)._

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
