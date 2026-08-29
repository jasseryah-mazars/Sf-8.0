# PHP & Web Security

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[SPL Collection](../labs/php-web-security.md)** — a step-by-step TD with test-first guidance and a reference solution.

The **language baseline** for the whole certification plus the **threat model**
that every Symfony security feature is built to defend. Symfony 8 requires
**PHP 8.4+**, and the exam expects fluency in modern PHP — enums, readonly
classes, property hooks, the SPL, the exception hierarchy — as well as the
web-attack vocabulary (XSS, CSRF, SQL injection, session fixation) that later
stages assume you already know.

!!! info "Stage at a glance"
    | Field | Value |
    |---|---|
    | **Prerequisites** | Comfortable procedural + OOP PHP |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | None — this is stage 1 |
    | **Revision priority** | **High** |
    | **Est. time** | 4–6 h |

## 🧠 Pour les nuls

**C'est quoi cette étape ?** Le socle de langage PHP moderne (enums, closures, attributs...) plus le vocabulaire des attaques web courantes (XSS, CSRF...) — les deux bases sur lesquelles tout le reste de Symfony est construit.

**Pourquoi ça existe ?** Symfony est du PHP moderne idiomatique : sans maîtriser les enums, les closures ou la promotion de constructeur, une bonne partie du code Symfony reste illisible. Et sans connaître les attaques qu'il défend, les fonctionnalités de sécurité paraissent arbitraires.

**🏠 Analogie de la vraie vie :** Apprendre l'alphabet et la grammaire avant de lire un roman. Tu ne peux pas comprendre une phrase complexe (un service Symfony) si tu ne reconnais pas encore les mots de base (enums, interfaces, closures) qui la composent.

**Symfony dans la vraie vie :** Le service container utilise massivement les interfaces et l'injection par constructeur — deux concepts purement PHP enseignés ici, avant même de parler de Symfony.

**⚠️ Erreur fréquente :** vouloir sauter cette étape parce qu'elle "n'est que du PHP" — plusieurs pièges de l'examen portent précisément sur des subtilités PHP (ex. `NotBlank` vs `NotNull`, `===` sur les enums) que Symfony réutilise partout ensuite.

**🧠 Comment le mémoriser :** "Maîtrise la langue avant de lire le livre — chaque chapitre Symfony suivant suppose que celui-ci est déjà acquis."

## Why this stage is first

Symfony is *idiomatic modern PHP*. You cannot reason about the service
container without understanding constructor promotion and readonly, nor about
the event system without closures and interfaces, nor about the security
component without knowing what an XSS or CSRF attack actually is. Master the
language and the threat model here, and every later stage becomes reading
comprehension rather than discovery.

## Micro-chapters

- [PHP API (up to 8.4)](php-api.md) — cert-relevant language features:
  enums, readonly classes, first-class callables, named args, `match`,
  nullsafe, typed constants, `#[\Override]`, `json_validate()`,
  new-in-initializer, **property hooks & asymmetric visibility (8.4)**, DNF types.
  Full journey: [exercises](php-api-exercises.md) · [exam](php-api-exam.md) · [flashcards](php-api-flashcards.md).
- [Object-Oriented Programming](oop.md) — classes, visibility, `static`, late
  static binding, constructor promotion, `clone`, magic methods.
  Full journey: [exercises](oop-exercises.md) · [exam](oop-exam.md) · [flashcards](oop-flashcards.md).
- [Attributes](attributes.md) — declaring `#[\Attribute]` classes, `TARGET_*`
  flags, `IS_REPEATABLE`, and reading them back via Reflection.
  Full journey: [exercises](attributes-exercises.md) · [exam](attributes-exam.md) · [flashcards](attributes-flashcards.md).
- [Interfaces & Type Declarations](interfaces.md) — covariance/contravariance,
  `instanceof`, union/intersection/DNF types, interface properties (8.4).
  Full journey: [exercises](interfaces-exercises.md) ·
  [exam](interfaces-exam.md) · [flashcards](interfaces-flashcards.md).
- [Anonymous Functions & Closures](closures.md) — arrow functions, `bindTo`,
  `Closure::fromCallable`, first-class callable syntax.
  Full journey: [exercises](closures-exercises.md) · [exam](closures-exam.md) ·
  [flashcards](closures-flashcards.md).
- [Abstract Classes](abstract-classes.md) — abstract vs interface, the template
  method pattern.
  Full journey: [exercises](abstract-classes-exercises.md) ·
  [exam](abstract-classes-exam.md) · [flashcards](abstract-classes-flashcards.md).
- [Exception & Error Handling](exceptions.md) — the `Throwable` hierarchy,
  `try`/`catch`/`finally`, custom exceptions, error levels, `set_error_handler`.
  Full journey: [exercises](exceptions-exercises.md) · [exam](exceptions-exam.md) ·
  [flashcards](exceptions-flashcards.md).
- [Traits](traits.md) — precedence (class > trait > parent), conflict resolution
  (`insteadof`/`as`), abstract & static members, trait properties and constants
  (8.2), `as final` (8.3), and `__CLASS__` vs `__METHOD__` inside a trait.
  Full journey: [exercises](traits-exercises.md) · [exam](traits-exam.md) ·
  [flashcards](traits-flashcards.md).
- [Enums](enums.md) — pure vs. backed enums, `UnitEnum`/`BackedEnum`,
  `from()`/`tryFrom()`, and how routing/Forms consume them.
  Full journey: [exercises](enums-exercises.md) · [exam](enums-exam.md) ·
  [flashcards](enums-flashcards.md).

**Additional / depth chapters** (not on the official syllabus list, kept as
enrichment — see the repository's `specs/TraceabilityMatrix.md`):

- [Namespaces & Autoloading](namespaces.md) — PSR-4, `use`, aliasing, name
  resolution rules.
  Full journey: [exercises](namespaces-exercises.md) · [exam](namespaces-exam.md) ·
  [flashcards](namespaces-flashcards.md).
- [PHP Extensions](extensions.md) — `mbstring`, `intl`, `ctype`, `iconv`,
  `pdo`, `opcache` and how to detect/require them.
- [SPL](spl.md) — `ArrayAccess`, `Iterator`/`IteratorAggregate`, `Countable`,
  `SplStack`/`Queue`/`Heap`/`PriorityQueue`, `SplObjectStorage`, generators.
- [Web Security Fundamentals](web-security.md) — XSS, CSRF, SQL injection,
  session hijacking/fixation, clickjacking, HTTPS/HSTS, security headers,
  password storage — framed as what Symfony protects against.

## How to study this stage

1. Read [PHP API](php-api.md) end-to-end — it anchors every version-specific trap.
2. Skim the OOP chapters ([OOP](oop.md), [interfaces](interfaces.md),
   [traits](traits.md), [abstract classes](abstract-classes.md)) — you likely
   know most, so focus on the **certification traps**.
3. Do the [SPL](spl.md) and [closures](closures.md) exercises hands-on.
4. Treat [Web Security Fundamentals](web-security.md) as the bridge to the
   [Security stage](../security/index.md).

---

<small>Next stage: [HTTP](../http/index.md) · Related: [Security](../security/index.md)</small>

## Official References

- [Symfony documentation — PHP Manual](https://www.php.net/manual/en/)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
