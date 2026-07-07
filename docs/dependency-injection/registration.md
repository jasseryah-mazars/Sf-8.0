# Service Registration

!!! tip "In a nutshell"
    Registration tells the container which classes are services; the `App\:`
    resource glob plus `autowire`/`autoconfigure` covers ~95% of it. Highest-yield
    fact: an auto-registered service's **id is its FQCN**, and `autowire` (args by
    type) and `autoconfigure` (tags by interface) are **independent** flags.

!!! example "Real-world analogy"
    Registration is writing the kitchen's station list: which classes are cooks on
    duty (services) and which are just pantry stock (value objects, entities). The
    `App\:` glob is a blanket "everyone in this room is on shift", `autowire` hands
    each cook their ingredients by type, and a named block is a sticky note amending
    one cook's setup.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain `services.yaml` `_defaults` (`autowire`, `autoconfigure`,
          `public`) and `resource`/`exclude` auto-registration.
    - [ ] Write manual `Definition`s with `arguments`, method `calls`, and
          `aliases`.
    - [ ] Configure a single service with `#[Autoconfigure]`.

    **Syllabus:** `Dependency Injection → Service Registration` ·
    **Level:** Advanced / Expert ·
    **Est. time:** 40 min ·
    **Prerequisites:** [The Service Container](container.md)

---

## Theory

Registration is telling the container which classes are services and how to build
them. Modern Symfony favours **convention over configuration**: one `resource`
glob registers a whole directory, `autowire` supplies constructor arguments by
type, and `autoconfigure` applies tags by implemented interface. You drop to
manual definitions only when the conventions cannot express something.

```yaml
# config/services.yaml
services:
    _defaults:
        autowire: true        # fill constructor args by type
        autoconfigure: true   # apply tags based on implemented interfaces
    App\:
        resource: '../src/'   # one resource glob registers the whole directory
```

!!! question "Predict first"
    Using the `App\:` resource glob, what is a service's id — a short name or
    something else? And are `autowire` and `autoconfigure` the same switch?

??? note "Reveal"
    The id **is the FQCN**. `autowire` (fill arguments by type) and `autoconfigure`
    (apply tags by interface/attribute) are **independent** flags — you can enable
    either without the other.

## Deep Dive — how it works internally

### `_defaults` and PSR-4 resource loading

`services.yaml` `_defaults` sets baseline flags for every service defined in that
file. The `App\:` block with `resource: '../src/'` walks the directory, and for
every class creates a `Definition` whose id **is the FQCN**. `exclude` skips
paths that are not services (Entities, DTOs, the Kernel).

```yaml
services:
    _defaults:
        autowire: true
        autoconfigure: true
        public: false

    App\:
        resource: '../src/'
        exclude: '../src/{DependencyInjection,Entity,Kernel.php}'
```

Registration order matters: a later, more specific entry **overrides** the glob for
the same id. So the `App\:` glob first registers everything, then a named block
tweaks one service.

### Arguments, calls, aliases

- **arguments** — positional or by name (`$logger:`). With autowiring you only
  list the ones the container cannot guess (scalars, ambiguous types).
- **calls** — setter injection: methods invoked after construction. Use
  constructor injection first; `calls` for optional/late deps.
- **aliases** — a second id (or an interface) pointing at a service, so it can be
  fetched/autowired under another name.

```yaml
services:
    App\Report\PdfReporter:
        arguments:
            $logger: '@monolog.logger'    # argument by name
        calls:
            - setLogger: ['@logger']      # setter injection after construction

    # Alias: the interface id points at the concrete service.
    App\Report\ReporterInterface: '@App\Report\PdfReporter'
```

```mermaid
flowchart TD
    G["App\\: resource glob"] --> D["Definition per class (id = FQCN)"]
    D --> O["named block overrides"]
    O --> A["autowire fills args"]
    A --> AC["autoconfigure adds tags"]
```

### `#[Autoconfigure]` — per-class defaults from the class

Instead of a YAML block, `#[Autoconfigure]` on the class sets its flags —
`public`, `shared`, `lazy`, `tags`, `bind`, `calls`, `properties`,
`constructor`. It is applied by the attribute-autoconfiguration pass at compile
time and is handy for library classes that carry their own wiring.

```php
use Symfony\Component\DependencyInjection\Attribute\Autoconfigure;

#[Autoconfigure(
    public: false,                                 // visibility flag
    shared: true,                                  // one instance per container
    lazy: true,                                    // proxy until first use
    tags: ['app.report'],                          // extra tags
    bind: ['$dir' => '%kernel.project_dir%/var'],  // named-argument binding
    calls: [['setLogger', ['@logger']]],           // setter calls
    properties: ['timeout' => 30],                 // property injection
    constructor: 'create',                         // static factory method
)]
final class PdfReporter { /* ... */ }
```

!!! note "Source reference"
    Attribute autoconfiguration is handled during compilation via
    `Symfony\Component\DependencyInjection\Attribute\Autoconfigure` and
    `ContainerBuilder::registerAttributeForAutoconfiguration()` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/Attribute/Autoconfigure.php).

### Null behavior

Required dependencies belong in the constructor; **optional** ones are where null
lives. Setter/`calls` injection of an absent service, or a `@?service.id` optional
reference, leaves the property at its declared default — so type it
`private ?LoggerInterface $logger = null` and null-guard every use. An **alias**
pointing at a non-existent target is a *compile error*, not a null. The example's
`setLogger()` pattern only stays safe because the property defaults to `null` and
the class checks before calling. The common bug is a nullable-defaulted property
that a required code path assumes is always set — inject it through the constructor
instead, so the container proves it exists at build time.

```php
// services.yaml: calls: [ setLogger: ['@?logger'] ]  — '@?' = optional reference
final class ReportRunner
{
    private ?LoggerInterface $logger = null;   // stays null if 'logger' is absent

    public function setLogger(LoggerInterface $logger): void
    {
        $this->logger = $logger;
    }

    public function run(): void
    {
        $this->logger?->info('running');       // null-guard every use
    }
}
```

!!! note "Null in real life"
    An optional cook who may not show up (optional setter dep): leave the station
    marked empty (`= null`) and check before assigning work — don't build the menu
    assuming they're there.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Report;

    use Psr\Log\LoggerInterface;
    use Symfony\Component\DependencyInjection\Attribute\Autoconfigure;
    use Symfony\Component\DependencyInjection\Attribute\Autowire;

    #[Autoconfigure(lazy: true, tags: ['app.report'])]
    final class PdfReporter
    {
        private ?LoggerInterface $logger = null;

        public function __construct(
            #[Autowire('%kernel.project_dir%/var/reports')]
            private readonly string $dir,
        ) {}

        // Optional setter injection.
        public function setLogger(LoggerInterface $logger): void
        {
            $this->logger = $logger;
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/services.yaml
    services:
        _defaults:
            autowire: true
            autoconfigure: true
            public: false

        App\:
            resource: '../src/'
            exclude: '../src/{Entity,Kernel.php}'

        # Manual definition overriding the glob for one class.
        App\Report\PdfReporter:
            arguments:
                $dir: '%kernel.project_dir%/var/reports'
            calls:
                - setLogger: ['@logger']
            lazy: true

        # Alias: fetch/autowire the interface as this service.
        App\Report\ReporterInterface: '@App\Report\PdfReporter'
    ```

=== "Console"

    ```console
    $ php bin/console debug:container --show-arguments App\\Report\\PdfReporter
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Rely on the `App\:` glob + autowire | Registering each class by hand |
| Constructor injection | Setter injection for required deps |
| `exclude` non-services | Letting Entities become services |
| Alias interface → impl | Duplicating full definitions |

## When (not) to use it / alternatives

Auto-registration covers ~95% of cases. Write a manual definition when you need a
non-autowirable argument, setter injection, a [factory](factories.md), or
different flags. Use `#[Autoconfigure]` when the wiring belongs *with* the class
(shared library code); use YAML when it is app-specific config.

!!! danger "Certification traps"
    - The auto-registered service **id is the FQCN**, not a short name.
    - `autoconfigure` (tags by interface) ≠ `autowire` (arguments by type) — two
      independent flags.
    - A later, more specific YAML entry overrides the glob for that id.
    - `exclude` does not delete files, it just skips registration.

!!! warning "Common mistakes"
    - Autowiring a **scalar** argument — it must come from `bind`/`#[Autowire]`.
    - Making everything `public: true` unnecessarily.
    - Forgetting an alias, then wondering why an interface type-hint fails.

## Exercises

1. **(Advanced)** Auto-register everything under `src/` except `Entity/` and
   `Kernel.php`, private and autowired.
2. **(Expert)** Register `PdfReporter` with a scalar `$dir` argument and an
   interface alias, keeping the rest autowired.

??? success "Solutions"

    **1.**
    ```yaml
    services:
        _defaults: { autowire: true, autoconfigure: true, public: false }
        App\:
            resource: '../src/'
            exclude: '../src/{Entity,Kernel.php}'
    ```

    **2.**
    ```yaml
    services:
        App\Report\PdfReporter:
            arguments:
                $dir: '%kernel.project_dir%/var/reports'
        App\Report\ReporterInterface: '@App\Report\PdfReporter'
    ```
    Only `$dir` is specified; other args stay autowired. The alias lets the
    interface be injected.

## Certification questions

??? question "Q1. Using the `App\:` resource glob, what is a service's id?"
    - [ ] A. A short snake_case name
    - [x] B. Its fully-qualified class name ✅
    - [ ] C. The file path
    - [ ] D. A random hash

    **Why:** PSR-4 auto-registration uses the FQCN as the id.
    **Ref:** [Service container](https://symfony.com/doc/current/service_container.html).

??? question "Q2. What does `autoconfigure: true` do?"
    - [ ] A. Fills constructor arguments by type
    - [x] B. Applies tags/flags based on implemented interfaces & attributes ✅
    - [ ] C. Makes services public
    - [ ] D. Clears the cache

    **Why:** Autoconfigure adds tags (e.g. event subscriber) automatically;
    autowire is what fills arguments. **Ref:** [Autoconfigure](https://symfony.com/doc/current/service_container.html#the-autoconfigure-option).

??? question "Q3. How do you make an interface type-hint resolve to a class?"
    - [x] A. Define an alias `Interface: '@Class'` ✅
    - [ ] B. Type-hint the class instead
    - [ ] C. Make the class public
    - [ ] D. Tag the class

    **Why:** An alias from the interface id to the concrete service lets autowiring
    resolve the type-hint. **Ref:** [Aliasing](https://symfony.com/doc/current/service_container/alias_private.html).

## Key takeaways

- `_defaults` + `App\:` glob + `autowire`/`autoconfigure` covers most services.
- Service id = FQCN; a specific block overrides the glob.
- Manual `arguments`/`calls`/`aliases` for what conventions cannot express.
- `#[Autoconfigure]` puts per-class wiring on the class itself.

## Last-minute revision

!!! tip "Cheat sheet"
    - `resource` = register glob; `exclude` = skip non-services.
    - `autowire` args-by-type; `autoconfigure` tags-by-interface — independent.
    - `arguments`, `calls` (setters), `aliases` (`Interface: '@Class'`).
    - `#[Autoconfigure(lazy:, public:, tags:, bind:)]`.

## Connections

- **Depends on:** [The Service Container](container.md) — registration produces the
  `Definition`s the container compiles.
- **Reused in:** [Autowiring](autowiring.md), [Tags](tags.md),
  [Factories](factories.md) — all build on registered definitions.
- **Confused with:** [Semantic Configuration](semantic-config.md) — app-level
  `services.yaml` vs a reusable bundle's typed config.

## Official References
- [Official Symfony docs — Service Container](https://symfony.com/doc/current/service_container.html)
- [Official Symfony docs — Aliasing & private services](https://symfony.com/doc/current/service_container/alias_private.html)
- [Symfony source — Autoconfigure attribute](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/Attribute/Autoconfigure.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "dependency injection" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/service_container.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** convention-over-configuration (`App\:` glob) covers most cases
- [ ] register services with `_defaults`, `resource`/`exclude` and an alias
- [ ] debug an interface type-hint that fails for lack of an alias
- [ ] spot that the id is the FQCN and `autowire` ≠ `autoconfigure`
- [ ] explain how a later, more specific block overrides the glob for one id

---

<small>Related: [Autowiring](autowiring.md) · [Factories](factories.md) ·
[Tags](tags.md)</small>
