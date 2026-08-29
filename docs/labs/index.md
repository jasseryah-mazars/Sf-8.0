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

## 🧠 Pour les nuls

**C'est quoi cette page ?** Le point d'entrée vers les exercices pratiques (labs) — un par domaine — où tu construis réellement du code au lieu de juste lire de la théorie.

**Pourquoi ça existe ?** Lire "comment fonctionne un Voter" et être capable d'en écrire un soi-même sous pression sont deux compétences différentes — les labs entraînent la seconde, indispensable le jour de l'examen (et en vrai travail).

**🏠 Analogie de la vraie vie :** Les travaux pratiques (TD) à l'université, en complément du cours magistral : le cours explique la théorie, le TD te fait manipuler toi-même, avec un corrigé caché à consulter seulement après avoir essayé.

**Symfony dans la vraie vie :** Le lab Security te fait écrire un vrai `Voter` testé unitairement — pas juste lire sa définition, mais le construire, le tester, et le comparer à une solution de référence.

**⚠️ Erreur fréquente :** ouvrir la solution cachée avant d'avoir vraiment essayé — ça donne l'illusion de comprendre sans avoir consolidé la compétence pratique.

**🧠 Comment le mémoriser :** "Essaie d'abord, compare ensuite — jamais l'inverse."

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
