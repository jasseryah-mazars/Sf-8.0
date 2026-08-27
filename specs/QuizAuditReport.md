# Quiz Audit Report

_Generated 2026-08-27. Branch `master`, commit at generation time: see
`specs/RemediationLog.md`'s P0 entries for the commit this run started from —
this report predates that run's final commit; regenerate/re-date if the quiz
bank changes after it._

## What this report is, and is not

The mission (P1-03) asks for a **full manual audit of every question**:
syllabus membership, Symfony 8.0 technical accuracy, correctness of the
marked answer, explanation quality, an official reference, absence of
ambiguity, absence of duplicates, and single/multiple answer-type
consistency. That audit — read all 1,292 questions individually against
Symfony 8.0 source/docs — was **not completed this run**. Auditing ~1,300
questions individually against primary sources is a multi-session
undertaking on its own; claiming it finished in one pass would violate this
project's own "never declare conforme without checked evidence" rule.

What follows is exactly what **is** automated and verifiable today, plus a
concrete, runnable method for the parts that still need a human (or a future
session with more budget) to actually read each question.

## 1. Automated schema/structure audit (ran this run)

Command: `python3 tools/validate_quiz.py`

```
validated 15 quiz files, 1292 questions; 0 error(s)
  official (in-scope): 1268 · out-of-scope/additional (excluded from certification): 24
  with v2 metadata: 1292/1292
  by type: {'single': 403, 'trap': 217, 'internals': 200, 'true-false': 49, 'scenario': 54, 'code': 102, 'config': 78, 'debug': 69, 'multiple': 120}
  by difficulty: {'easy': 332, 'medium': 661, 'hard': 299}
  subchapter coverage: 157/157 (100%)
```

**What this proves:** every question has ≥2 answers, ≥1 marked correct, a
non-empty `explanation`, and a `documentation` URL starting with `http`; every
`id` is unique across the bank; every `type`/`difficulty` value is a valid
enum member; every officially-tracked subchapter has at least one tagged
question.

**What this does NOT prove** (the gap this report is honest about):

| Mission requirement | Automated today? | How it would be checked |
|---|---|---|
| Question belongs to the official syllabus | Partial — `out_of_scope: true` questions are excluded from official stats (24 of them), but nothing verifies an *untagged* question is actually in-scope beyond the `subchapter` field matching a matrix row | Cross-reference every `subchapter` value against `specs/OfficialSyllabusBaseline.md` §3 (not yet scripted) |
| Symfony 8.0 technical accuracy of the *content* | No | Manual read against `github.com/symfony/symfony/tree/8.0` source or `symfony.com/doc/8.0/` (network-blocked this run for the latter) |
| The marked answer is actually correct | No | Manual verification per question |
| Explanation quality / no ambiguity | No | Manual read |
| `documentation` URL is relevant (not just present) | Partial — `tools/check_doc_version_refs.py` (new this run) verifies every `symfony.com/doc/...` URL in the bank is pinned to `8.0`, but not that it's the *right* page for the question | Manual spot-check |
| No duplicate questions (near-identical stems) | **Partial — implemented and run this session** | `tools/check_quiz_duplicates.py` (Jaccard token-overlap, lexical not semantic — see §1b) found 17 candidate pairs; all 17 were read by hand, 16 were legitimate distinct questions and 1 genuine near-duplicate was reworded (see `specs/RemediationLog.md` P1-03) |
| Single-vs-multiple type matches the actual count of `correct: true` answers | **Yes — implemented and run this session** | `tools/validate_quiz.py` now checks `single`/`true-false` have exactly 1 `correct: true` and `multiple` has ≥2; result: **0 errors** across all 1,292 questions |

## 1b. Near-duplicate detection (ran this run, P1-03)

Command: `python3 tools/check_quiz_duplicates.py --threshold 0.75`

```
checked 1292 questions, 833986 pairs, threshold=0.75: 17 candidate near-duplicate pair(s)
```

**Method, stated honestly:** Jaccard similarity of each question's
normalized token set (lowercase, punctuation stripped, stopwords removed).
This is a **lexical-overlap heuristic, not semantic understanding** — it
would miss two differently-worded questions testing the same fact, and it
can flag two questions sharing template phrasing (e.g. "Which of the
following statements are true about the Symfony `X` component?" repeated
per component) as candidates even when they are legitimately different.
The script never asserts a confirmed duplicate itself; it does not fail CI.

**Human review result:** all 17 candidate pairs were read individually.
16 were confirmed legitimate (shared template stem, different tested
content). 1 was a genuine near-duplicate — `MISC-DEPLOY-03` vs `PHP-EXT-09`,
both testing `opcache.validate_timestamps=0` with near-identical "why set
it" wording. `PHP-EXT-09` was reworded to a complementary consequence/trap
angle and propagated to every derived copy (exam page, flashcard,
`quiz-data.json`, `flashcards.csv`). Full before/after in
`specs/RemediationLog.md`'s P1-03 entry.

**What this does not prove:** that no *semantic* duplicate exists among
question pairs whose wording differs enough to fall under the lexical
threshold — that class of duplicate is not detectable by this script and
would require the manual per-question read described in §3.

## 2. Doc-reference version compliance (ran this run, P0-01)

`tools/check_doc_version_refs.py` scanned every `quiz/*.yml` file (they were
included in the P0-01 sweep) — 0 violations after fixing 5,773 unversioned
`symfony.com/doc/current` references bank-wide (see `specs/RemediationLog.md`
P0-01). Every quiz question's `documentation` field pointing at
`symfony.com/doc/` is now pinned to `/doc/8.0/`, or is a `twig.symfony.com`/
`symfony.com/doc/3.x/` Twig reference, or a `github.com/symfony/symfony/
blob|tree/8.0/...` source link, or a `php.net`/`rfc-editor.org` reference.

## 3. Proposed method for the remaining manual audit (not executed)

For a future run with the budget to do this properly, per question:

1. Read the `question` + all `answers` + `explanation`.
2. ~~Confirm `type` matches reality~~ — done: this check is now in
   `tools/validate_quiz.py` (see §1) and passes with 0 errors bank-wide.
3. Open the `documentation` link (or the equivalent GitHub source) and
   confirm the claimed behavior/API/config still matches Symfony 8.0 /
   PHP 8.4 / the syllabus's Twig version.
4. Check `subchapter` against `specs/OfficialSyllabusBaseline.md` — flag any
   question whose subchapter doesn't map to an official subtopic and isn't
   tagged `out_of_scope: true`.
5. ~~Fuzzy-match `question` text bank-wide for near-duplicates~~ — done:
   `tools/check_quiz_duplicates.py` (§1b) implements the token-overlap pass
   and the resulting 17 candidates were all reviewed this run. This
   surfaces *lexical* near-duplicates only; a true embedding/semantic pass
   across all 1,292 stems remains unimplemented (no ML/embedding library
   available in this environment) and would still be needed to catch
   differently-worded duplicates.

## 4. Honest summary

- **Structurally sound:** yes, per `validate_quiz.py`, with 0 errors.
- **Version-reference compliant:** yes, per `check_doc_version_refs.py`, with
  0 violations, after this run's P0-01 fix.
- **Individually fact-checked against Symfony 8.0 for all 1,292 questions:**
  **not verified this run.** Do not report this bank as "conforme" on
  technical-accuracy grounds without doing the §3 pass, or without pointing
  at the specific prior-session spot-checks already logged in
  `specs/CoworkProgress.md` (which covered a meaningful but partial subset,
  not the full bank).
