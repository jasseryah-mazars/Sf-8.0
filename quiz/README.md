# Practice Quiz Bank

Machine-readable question bank, one YAML file per syllabus topic area. The schema
is compatible with
[certificationy-cli](https://github.com/certificationy/certificationy-cli) so you
can self-test in the terminal, and it is also rendered in the
[Revision Hub → Quiz](../docs/revision/quiz.md).

## Run it locally

```console
$ composer global require certificationy/certificationy-cli
$ certificationy start   # point it at this quiz/ directory via its config
```

## Schema

```yaml
categories:
  - name: "Dependency Injection"
    questions:
      - question: "Which attribute registers a compiler pass? (choose one)"
        answers:
          - value: "There is no attribute; you register it in the Kernel/bundle build() method"
            correct: true
          - value: "#[CompilerPass]"
            correct: false
          - value: "#[AsCompilerPass]"
            correct: false
        # Optional but REQUIRED in this project:
        explanation: >-
          Compiler passes are registered programmatically via
          ContainerBuilder::addCompilerPass(), typically in Kernel::build()
          or a bundle's build() method. There is no core attribute for this.
        documentation: "https://symfony.com/doc/8.0/service_container/compiler_passes.html"
```

## Rules

- `correct: true` on **one or more** answers (multiple-choice supported).
- Every question **must** include `explanation` and `documentation`.
- True/false questions use two answers (`"True"` / `"False"`).
- Symfony 8 / PHP 8.4 only. No deprecated APIs in stems or options.
- 3–6 questions per chapter; group them under the topic-area `name`.

## Files

`php-web-security.yml`, `http.yml`, `architecture.yml`, `controllers.yml`,
`routing.yml`, `twig.yml`, `forms.yml`, `validation.yml`, `dependency-injection.yml`,
`security.yml`, `http-caching.yml`, `console.yml`, `testing.yml`, `miscellaneous.yml`.

---

## Rich metadata (v2) — the Global Question Bank

Questions may carry metadata that powers the Chapter Exams and the
coverage/difficulty/type-aware mock generator. Base fields stay required;
metadata fields are strongly recommended on new/updated questions.

```yaml
categories:
  - name: "Security — Voters"
    questions:
      - id: "SEC-VOTERS-01"          # unique, stable: <AREA>-<SUBTOPIC>-<n>
        question: "…"
        type: "single"                # see types below
        difficulty: "medium"          # easy | medium | hard
        subchapter: "security/voters" # docs path without .md (maps to the chapter)
        concepts: ["voter", "access-decision", "strategy"]
        syllabus: "Security → Voters & voting strategies"
        answers:
          - { value: "…", correct: true }
          - { value: "…", correct: false }
        explanation: >-
          Why the correct answer is correct, why the others are wrong, the
          Symfony-internal behaviour that justifies it, and the common misconception.
        documentation: "https://symfony.com/doc/8.0/security/voters.html"
```

**`type` enum:** `single` · `multiple` · `true-false` · `code` (code-reading) ·
`config` (configuration analysis) · `debug` (debugging scenario) · `internals`
(internal Symfony behaviour) · `scenario` (real-world) · `trap` (certification trick).

**Rules for v2 questions**
- `id` unique across the whole bank; `subchapter` matches a `docs/<area>/<file>` (no `.md`).
- Balance types across each area; don't make everything `single`.
- `explanation` must justify correct **and** wrong answers where applicable.
- Every question maps to a syllabus objective via `syllabus`.
- Coverage goal: **every subchapter has at least one question** (checked by
  `tools/validate_quiz.py`).
