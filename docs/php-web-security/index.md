# PHP & Web Security

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
- [Object-Oriented Programming](oop.md) — classes, visibility, `static`, late
  static binding, constructor promotion, `clone`, magic methods.
- [Namespaces & Autoloading](namespaces.md) — PSR-4, `use`, aliasing, name
  resolution rules.
- [Interfaces & Type Declarations](interfaces.md) — covariance/contravariance,
  `instanceof`, union/intersection/DNF types.
- [Anonymous Functions & Closures](closures.md) — arrow functions, `bindTo`,
  `Closure::fromCallable`, first-class callable syntax.
- [Abstract Classes](abstract-classes.md) — abstract vs interface, the template
  method pattern.
- [Traits](traits.md) — conflict resolution (`insteadof`/`as`), abstract/static
  members, precedence.
- [Exception & Error Handling](exceptions.md) — the `Throwable` hierarchy,
  `try`/`catch`/`finally`, custom exceptions, error levels, `set_error_handler`.
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
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
