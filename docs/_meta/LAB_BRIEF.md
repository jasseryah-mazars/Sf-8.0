# Lab Author Brief (shared)

You write **one flagship Practical Lab** for a topic area. Goal: turn theory into
applied, exam-ready skill.

## Read first
- `docs/_meta/LAB_TEMPLATE.md` — the exact section order and modes.
- `docs/_meta/CONVENTIONS.md` — versions, code style, admonitions.
- The theory chapters in your area (link the lab back to them).

## Choose the mode (Rule 1 eligibility)
- **TDD lab** when the concept is *code behaviour* (a class/service/component you
  can instantiate and assert on): DI, Forms, Validator, EventDispatcher, Console,
  Voters, Serializer, value resolvers, data transformers, custom constraints,
  Messenger handlers, HttpClient with `MockHttpClient`, SPL structures, Twig
  extensions. Write the **PHPUnit test first**, then the code (red/green/refactor).
- **Manual-verification lab** when the concept is *config/infra* (security.yaml,
  HTTP cache headers, routing config, deployment): replace the TDD block with
  Validation Steps (CLI `bin/console`, profiler, `curl -I`).
- **Conceptual Simulation** when the concept is *pure theory* (kernel event order,
  BC promise, licensing): replace Task+TDD with predict-output / order-the-steps /
  debug-the-scenario questions with hidden answers.

## Hard rules
- **Symfony 8 / PHP 8.4 only.** No deps outside the certification scope (Symfony
  components + PHPUnit are fine; NO Doctrine/UX/AI/Encore/third-party).
- Every complete `<?php` snippet must compile (`php -l`): `<?php` +
  `declare(strict_types=1)` on the first lines, real `use` imports, valid types.
  Method-only excerpts are fine (they won't be linted). Mark any intentional
  error demo with `// lint-skip`.
- **Progressive difficulty**: state Easy/Medium/Advanced; you may include a short
  "level up" note toward an exam-trick variant.
- Follow the LAB_TEMPLATE section order and the OUTPUT FORMAT exactly.
- Stay mapped to your area's theory; introduce **no** unrelated concepts.
- Additive only — do not edit theory chapters, `mkdocs.yml`, quiz, specs, or other
  areas.

## Deliverable
Exactly one file: `docs/labs/<area>.md` (filename given to you), following the
template, ending with a `Related` line linking the theory chapter and `index.md`.

## Report back
The lab's concept + mode + difficulty, the FQCNs used, and confirmation that the
reference solution + test skeleton are valid Symfony 8 / PHP 8.4 that would compile.
