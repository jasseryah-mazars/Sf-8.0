# PHP & Web Security

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[SPL Collection](../labs/php-web-security.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Le **socle langage** de toute la certification, plus le **modèle de menaces**
contre lequel chaque fonctionnalité de sécurité de Symfony est conçue pour se
défendre. Symfony 8 exige **PHP 8.4+**, et l'examen attend une maîtrise du PHP
moderne — enums, classes readonly, property hooks, la SPL, la hiérarchie des
exceptions — ainsi que du vocabulaire des attaques web (XSS, CSRF, injection
SQL, fixation de session) que les étapes suivantes supposent déjà acquis.

!!! info "Stage at a glance"
    | Field | Value |
    |---|---|
    | **Prerequisites** | À l'aise avec le PHP procédural + OOP |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Aucune — c'est l'étape 1 |
    | **Revision priority** | **High** |
    | **Est. time** | 4–6 h |

## Why this stage is first

Symfony est du *PHP moderne idiomatique*. Vous ne pouvez pas raisonner sur le
container de services sans comprendre la promotion de constructeur et readonly,
ni sur le système d'events sans les closures et les interfaces, ni sur le
composant de sécurité sans savoir ce qu'est réellement une attaque XSS ou CSRF.
Maîtrisez ici le langage et le modèle de menaces, et chaque étape suivante
devient de la lecture plutôt que de la découverte.

## Micro-chapters

- [PHP API (up to 8.4)](php-api.md) — les fonctionnalités du langage utiles à
  la certification : enums, classes readonly, first-class callables, arguments
  nommés, `match`, nullsafe, constantes typées, `#[\Override]`, `json_validate()`,
  new-in-initializer, **property hooks & visibilité asymétrique (8.4)**, types DNF.
- [Object-Oriented Programming](oop.md) — classes, visibilité, `static`, late
  static binding, promotion de constructeur, `clone`, méthodes magiques.
- [Namespaces & Autoloading](namespaces.md) — PSR-4, `use`, alias, règles de
  résolution des noms.
- [Interfaces & Type Declarations](interfaces.md) — covariance/contravariance,
  `instanceof`, types union/intersection/DNF.
- [Anonymous Functions & Closures](closures.md) — arrow functions, `bindTo`,
  `Closure::fromCallable`, syntaxe first-class callable.
- [Abstract Classes](abstract-classes.md) — classe abstraite vs interface, le
  pattern template method.
- [Traits](traits.md) — résolution de conflits (`insteadof`/`as`), membres
  abstraits/statiques, précédence.
- [Exception & Error Handling](exceptions.md) — la hiérarchie `Throwable`,
  `try`/`catch`/`finally`, exceptions personnalisées, niveaux d'erreur,
  `set_error_handler`.
- [PHP Extensions](extensions.md) — `mbstring`, `intl`, `ctype`, `iconv`,
  `pdo`, `opcache` et comment les détecter/exiger.
- [SPL](spl.md) — `ArrayAccess`, `Iterator`/`IteratorAggregate`, `Countable`,
  `SplStack`/`Queue`/`Heap`/`PriorityQueue`, `SplObjectStorage`, générateurs.
- [Web Security Fundamentals](web-security.md) — XSS, CSRF, injection SQL,
  détournement/fixation de session, clickjacking, HTTPS/HSTS, en-têtes de
  sécurité, stockage des mots de passe — présentés sous l'angle de ce contre
  quoi Symfony protège.

## How to study this stage

1. Lisez [PHP API](php-api.md) de bout en bout — il ancre tous les pièges liés
   aux versions.
2. Parcourez les chapitres OOP ([OOP](oop.md), [interfaces](interfaces.md),
   [traits](traits.md), [abstract classes](abstract-classes.md)) — vous en
   connaissez probablement l'essentiel, concentrez-vous donc sur les
   **certification traps**.
3. Faites les exercices de [SPL](spl.md) et de [closures](closures.md) en
   pratique.
4. Considérez [Web Security Fundamentals](web-security.md) comme la passerelle
   vers l'[étape Security](../security/index.md).

---

<small>Next stage: [HTTP](../http/index.md) · Related: [Security](../security/index.md)</small>

## Official References

- [Symfony documentation — PHP Manual](https://www.php.net/manual/en/)
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
