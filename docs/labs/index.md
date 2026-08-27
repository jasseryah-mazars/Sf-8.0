# Practical Labs

Theory tells you *how it works*; labs make you *able to build and debug it under
exam conditions*. Each lab is a university-style TD: an objective, step-by-step
instructions, a **test-first (TDD)** cycle where code behaviour allows it, and a
hidden reference solution to compare against.

!!! abstract "How to use a lab"
    1. Read the linked **theory** chapter first.
    2. Do the **TD instructions** yourself — resist opening the solution.
    3. For TDD labs: write the **failing test**, then make it pass, then refactor.
    4. Run the **validation steps**; review the **common mistakes**.
    5. Only then open the **ideal solution** and compare.

## Lab modes

- :material-flask: **TDD lab** — code behaviour: write the PHPUnit test first.
- :material-console: **Manual verification** — config/infra: verify via CLI,
  profiler, or `curl`.
- :material-thought-bubble: **Conceptual simulation** — pure theory: predict
  output, order the steps, debug the scenario.

## Flagship labs (one per topic area)

| Area | Lab | Mode | Difficulty |
|---|---|---|---|
| [PHP & Web Security](php-web-security.md) | A typed collection with SPL (`IteratorAggregate`, `Countable`, `ArrayAccess`) | TDD | Medium |
| [HTTP](http.md) | An API client tested with `MockHttpClient` | TDD | Medium |
| [Architecture](architecture.md) | A custom event + prioritised subscribers on the `EventDispatcher` | TDD | Medium |
| [Controllers](controllers.md) | A custom `ValueResolverInterface` argument resolver | TDD | Advanced |
| [Routing](routing.md) | Predict & verify route matching (`debug:router` / `router:match`) | Manual | Medium |
| [Templating (Twig)](twig.md) | A custom Twig extension filter/function | TDD | Easy |
| [Forms](forms.md) | A custom form type with a `DataTransformer` | TDD | Advanced |
| [Data Validation](validation.md) | A custom `Constraint` + `ConstraintValidator` | TDD | Medium |
| [Dependency Injection](dependency-injection.md) | A tag-driven registry built by a compiler pass | TDD | Advanced |
| [Security](security.md) | A `Voter` for fine-grained authorization | TDD | Medium |
| [HTTP Caching](http-caching.md) | Expiration & validation headers, verified with `curl` | Manual | Medium |
| [Console](console.md) | A command tested with `CommandTester` | TDD | Easy |
| [Automated Tests](testing.md) | Service + functional tests (`KernelTestCase`/`WebTestCase`) | TDD | Medium |
| [Miscellaneous](miscellaneous.md) | A Messenger handler + custom middleware | TDD | Advanced |

!!! tip "Where labs fit in the study loop"
    Do a lab right after finishing an area's theory and flashcards, before the
    mock exam. Applying a concept once beats re-reading it three times.

---

<small>Related: [Roadmap](../roadmap.md) · [Revision Hub](../revision/index.md)</small>

## Official References

- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Testing](https://symfony.com/doc/8.0/testing.html)
