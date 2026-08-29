# Question-Bank Author Brief (shared)

You upgrade and expand **one area's** `quiz/<area>.yml` into part of the metadata-rich
Global Question Bank. Read `quiz/README.md` (the **v2 schema**) and
`docs/_meta/CONVENTIONS.md` first.

## Two jobs

**1. Tag every existing question** in your file with v2 metadata:
`id`, `type`, `difficulty`, `subchapter`, `concepts`, `syllabus`. Keep the
existing `question`/`answers`/`explanation`/`documentation` intact.

**2. Expand to full coverage.** Ensure **every subchapter** of your area (each
`docs/<area>/*.md` except `index.md`) has questions. Add new questions until each
subchapter is well covered and the **type mix is balanced** across the area.

## v2 field rules

- `id`: unique, stable, `<AREA>-<SUBTOPIC>-<n>` (e.g. `SEC-VOTERS-03`).
- `subchapter`: the docs path without `.md` (e.g. `security/voters`).
- `type` ∈ `single｜multiple｜true-false｜code｜config｜debug｜internals｜scenario｜trap`.
  **Balance them** — roughly ≥1 of `internals`, `trap`, and one of
  code/config/debug per subchapter where it makes sense. Don't make everything `single`.
- `difficulty` ∈ `easy｜medium｜hard`. Aim ~30% easy / ~45% medium / ~25% hard per area.
- `concepts`: 2–4 short tags. `syllabus`: the official objective string.

## Question quality (exam-realistic)

Write like the real Symfony 8 exam — reward **reasoning, not recall of trivia**:

- Test **internals**: kernel-event order, DI compilation, security passport flow,
  form/validation lifecycles, Messenger middleware, cache headers.
- Use **precise** class names, method signatures, config keys, and **default values**.
- **code** questions: a short snippet → "what happens / what's the output / which line
  is wrong". **config** questions: a YAML/attributes block → what it does.
  **debug** questions: a symptom → the cause. **trap** questions: exploit a common
  confusion (see each chapter's "Certification traps"/"Easily confused").
- `multiple` questions: say "(choose N)"; mark all correct answers.
- Symfony 8 / PHP 8.4 only. No deprecated APIs in stems/options (unless the question
  is *about* a removal, framed correctly).

## Answer explanations (mandatory, rich)

Each `explanation` must state: **why the correct answer is correct**, **why the
wrong ones are wrong** (when applicable), the **Symfony-internal behaviour** that
justifies it, and the **common misconception**. Keep `documentation` as a real
`symfony.com/doc/8.0/...` (or php.net for pure-PHP) link.

## Hard rules

- Edit **only** `quiz/<your-area>.yml`. Additive/enriching — don't delete questions.
- YAML must parse; run a mental check against `quiz/README.md`.
- No duplicate `id`s within your file (coordinator checks globally).

## Report
Counts: existing tagged, new added, per-type and per-difficulty tallies, and confirm
every subchapter of your area now has ≥1 question.
