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
        documentation: "https://symfony.com/doc/current/service_container/compiler_passes.html"
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
