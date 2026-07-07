# The Service Container

!!! tip "In a nutshell"
    The container builds your objects, injects their dependencies, and hands them
    back — you describe *how* to build a service, it does the rest. Remember the
    split: a `ContainerBuilder` compiles everything once into a dumped PHP class
    that serves instances at runtime. Highest-yield fact: services are **private
    and shared by default**.

!!! example "Real-world analogy"
    The container is a restaurant kitchen. You order a dish (ask for a service);
    the kitchen gathers and assembles the ingredients (its dependencies) and plates
    it — you never touch the pans (`new`). **Compiling** the container is prepping
    the kitchen *once* before service (mise en place), so every order during the
    night is fast. Asking for a dish that is not on the menu (a private or removed
    id) gets a polite refusal, not a plate.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Define what a *service* is and distinguish **compilation** from **runtime**.
    - [ ] Trace the container compilation lifecycle and explain the **compiled
          container cache** in `var/cache/`.
    - [ ] Explain `ContainerInterface::get()` semantics and why services are
          **private by default**.

    **Syllabus:** `Dependency Injection → Service Container` ·
    **Level:** Advanced / Expert ·
    **Est. time:** 40 min ·
    **Prerequisites:** [Symfony Architecture](../architecture/index.md)

---

## Theory

A **service** is any object that performs a job and is managed by the container:
a mailer, a logger, a repository, your own `InvoiceGenerator`. Value objects
(an `Order`, a `Money`) are *not* services — they carry data, they are not wired.

```php
// A service: does a job, has dependencies, is wired by the container
final class InvoiceGenerator { /* logger injected, registered once */ }

// Value objects: carry data, built with `new`, NOT services
$order = new Order(42);
$price = new Money(1999, 'EUR');
```

The **service container** (also *DI container*) is the object that instantiates
services, injects their dependencies, and hands them out on demand. In Symfony it
is defined by `Symfony\Component\DependencyInjection\ContainerInterface`. You
almost never build services with `new`; you describe *how* they are built and let
the container do it — lazily, once, and shared by default.

```php
use Symfony\Component\DependencyInjection\ContainerInterface;

// Manual wiring with `new` — what you almost never do:
$generator = new InvoiceGenerator(new Logger());

// The container (ContainerInterface) builds it for you — lazily, once, shared:
$generator = $container->get(InvoiceGenerator::class);
```

The crucial idea: there are **two containers**.

| | Build time | Runtime |
|---|---|---|
| Class | `ContainerBuilder` | dumped `App\..\Container*` |
| Holds | `Definition` objects | real service instances |
| When | cache warmup / first request | every request |
| Mutable? | yes (until frozen) | no |

!!! question "Predict first"
    A service is registered `public: false`. At runtime you call
    `$container->get(App\Invoice\InvoiceGenerator::class)`. What happens?

??? note "Reveal"
    It throws `ServiceNotFoundException`. Private services are not fetchable by id
    from the runtime container — the compiler may even have inlined or removed them.
    Inject the service via autowiring instead of pulling it from the container.

## Deep Dive — how it works internally

### Definitions, not instances (build time)

During compilation nothing is instantiated. Each service is a
`Symfony\Component\DependencyInjection\Definition`: a recipe holding the class,
arguments, method calls, tags, `public`/`shared`/`lazy` flags and factory. A
`Symfony\Component\DependencyInjection\Reference` points to another service by id;
a `Symfony\Component\DependencyInjection\Alias` makes one id resolve to another;
a `Symfony\Component\DependencyInjection\Parameter` references a container
parameter. All of these are pure metadata objects.

```php
use Symfony\Component\DependencyInjection\Alias;
use Symfony\Component\DependencyInjection\Definition;
use Symfony\Component\DependencyInjection\Parameter;
use Symfony\Component\DependencyInjection\Reference;

// Definition: the recipe — nothing is instantiated here
$def = new Definition(App\Invoice\InvoiceGenerator::class);
$def->setArgument(0, new Reference('logger'));       // Reference: points to another service id
$def->setArgument(1, new Parameter('kernel.debug')); // Parameter: references a container parameter
$def->setPublic(false);  // public flag
$def->setShared(true);   // shared flag
$def->setLazy(false);    // lazy flag

// Alias: makes one id resolve to another
$containerBuilder->setAlias('app.invoices', new Alias(App\Invoice\InvoiceGenerator::class));
```

`ContainerBuilder` extends `Container` and additionally stores these definitions,
aliases, extensions and compiler passes.

```mermaid
classDiagram
    class ContainerBuilder
    class Definition {
      +class
      +arguments
      +tags
      +public/shared/lazy
    }
    class Reference
    class Alias
    class Parameter
    class CompilerPassInterface {
      +process(ContainerBuilder)
    }
    ContainerBuilder "1" o-- "*" Definition : holds
    ContainerBuilder "1" o-- "*" Alias : holds
    ContainerBuilder ..> CompilerPassInterface : runs
    Definition "1" o-- "*" Reference : argument
    Definition ..> Parameter : argument
    Alias ..> Definition : resolves to
```

### The compilation pipeline

`ContainerBuilder::compile()` runs the passes registered in
`Symfony\Component\DependencyInjection\Compiler\PassConfig`, then **freezes**
parameters and marks the container compiled. Passes resolve autowiring, inline
private services, remove unused (private, unreferenced) definitions, and validate
references. See [Compiler Passes](compiler-passes.md) for the phase order.

```php
use Symfony\Component\DependencyInjection\Compiler\PassConfig;

// Passes are registered into a PassConfig phase…
$containerBuilder->addCompilerPass(new AppPass(), PassConfig::TYPE_BEFORE_OPTIMIZATION);

// …then ContainerBuilder::compile() runs them all, freezes parameters
// and marks the container compiled
$containerBuilder->compile();
```

```mermaid
flowchart LR
    Y["YAML / PHP / attributes"] --> B[ContainerBuilder]
    B --> E["Extensions: load()"]
    E --> C["compile(): PassConfig"]
    C --> R["resolve autowiring<br/>+ remove private"]
    R --> D["PhpDumper → cache class"]
    D --> RT["runtime: compiled Container"]
```

### The compiled container cache

After compilation, `Symfony\Component\DependencyInjection\Dumper\PhpDumper` writes
an optimised PHP class (e.g. `App_KernelDevContainer`) to
`var/cache/<env>/`. This class has a hard-coded method per public service and
`getXxxService()` factories — no reflection, no YAML parsing at runtime. On the
next request the kernel loads that class directly; the `ContainerBuilder` is never
touched again. In `dev`, the `ConfigCache` checks the tracked resources (config
files) and rebuilds only when they change; in `prod` you warm it once during
deploy.

```php
use Symfony\Component\Config\ConfigCache;
use Symfony\Component\DependencyInjection\Dumper\PhpDumper;

$file = 'var/cache/dev/App_KernelDevContainer.php';
$cache = new ConfigCache($file, true); // dev: tracks the config resources

if (!$cache->isFresh()) {              // rebuild only when tracked config changed
    $containerBuilder->compile();
    $dumper = new PhpDumper($containerBuilder); // dumps the optimised PHP class
    $code = $dumper->dump(['class' => 'App_KernelDevContainer']);
    $cache->write($code, $containerBuilder->getResources());
}

require_once $file;
$container = new \App_KernelDevContainer(); // hard-coded getXxxService() factories inside
```

```mermaid
flowchart TB
    subgraph compile["Compile — once (warmup / config change)"]
        direction TB
        CFG["config: YAML / PHP / #[attributes]"] --> BLD["ContainerBuilder<br/>(Definition objects)"]
        BLD --> OPT["passes: optimize<br/>(autowire, resolve refs)"]
        OPT --> REM["passes: remove<br/>(prune private / unused)"]
        REM --> DMP["PhpDumper"]
        DMP --> CACHE[("var/cache · *Container.php")]
    end
    subgraph runtime["Runtime — every request"]
        direction TB
        LOAD["kernel loads compiled class"] --> GET["get(id): build once, share instance"]
    end
    CACHE -.->|"loaded, not rebuilt<br/>unless config changes"| LOAD
```

!!! note "Source reference"
    `Symfony\Component\DependencyInjection\ContainerBuilder` &
    `Container` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/ContainerBuilder.php).

### `get()` at runtime

`ContainerInterface::get($id, $invalidBehavior)` returns a service. By default
services are **shared**: the first `get()` builds and caches the instance, later
calls return the same object. A `shared: false` service is rebuilt each time.
The second argument controls what happens for a missing id
(`EXCEPTION_ON_INVALID_REFERENCE`, `NULL_ON_INVALID_REFERENCE`, etc.).

```php
use Symfony\Component\DependencyInjection\ContainerInterface;

// Shared (default): first get() builds, later calls return the SAME object
$a = $container->get('logger');
$b = $container->get('logger'); // $a === $b — unless defined with `shared: false`

// Second argument: EXCEPTION_ON_INVALID_REFERENCE (default) throws on a missing id
$container->get('missing.id', ContainerInterface::EXCEPTION_ON_INVALID_REFERENCE);

// NULL_ON_INVALID_REFERENCE returns null instead
$maybe = $container->get('missing.id', ContainerInterface::NULL_ON_INVALID_REFERENCE);
```

### Public vs private — and why private is the default

A **public** service can be fetched with `$container->get('id')`. A **private**
service cannot; it may only be *injected* into other services. Since Symfony 4,
**services are private by default**, because:

- The compiler can **inline** a private service directly into its single consumer,
  and **remove** private services that nothing references — smaller, faster
  container.
- It enforces proper dependency injection instead of the service-locator
  anti-pattern of pulling from the container everywhere.

Fetching a private (or removed) service by id throws
`ServiceNotFoundException`. That is why controllers use autowiring or the
`ServiceSubscriberInterface`, not `$container->get()`.

```php
use Symfony\Contracts\Service\ServiceSubscriberInterface;

// Private (or removed) id: $container->get() throws ServiceNotFoundException
$container->get(App\Invoice\InvoiceGenerator::class); // ServiceNotFoundException!

// Sanctioned alternative: declare the needed services explicitly
final class InvoiceController implements ServiceSubscriberInterface
{
    public static function getSubscribedServices(): array
    {
        return ['generator' => App\Invoice\InvoiceGenerator::class];
    }
}
```

### Null behavior

`ContainerInterface::get($id, $invalidBehavior)` decides what a *missing* id does.
The default `EXCEPTION_ON_INVALID_REFERENCE` throws `ServiceNotFoundException`; pass
`ContainerInterface::NULL_ON_INVALID_REFERENCE` and `get()` returns `null` instead
— the sanctioned way to model an *optional* dependency. A **private** or
compiler-**removed** service is "missing" from the public container even though it
exists, so `get()` on it also throws. Guard with `has($id)` before `get()`, or type
the injected dependency as nullable (`?LoggerInterface $logger = null`) so a
`null`-resolved reference is legal. The common bug: letting a
`ServiceNotFoundException` bubble up because you assumed an optional service was
always present.

!!! note "Null in real life"
    A missing service id is the waiter saying "we're out of that tonight" — with
    `NULL_ON_INVALID_REFERENCE` you get an empty plate (null) instead of an argument.

!!! info "Expert note"
    `debug:container` reads the *dumped* container, so it shows the world after
    compilation — inlined and removed private services simply are not there. When a
    service "disappears", check whether it was private and unreferenced: the removal
    pass pruned it. Add `--show-private` to see the private ids the compiler kept.

??? example "Debugging story"
    **Symptom:** an edit to `services.yaml` had no effect in `prod`.
    **Diagnosis:** the compiled container in `var/cache/prod/` was never rebuilt —
    the deploy skipped `cache:clear`, so the dumped `*Container.php` still held the
    old resolved arguments. **Fix:** run `cache:warmup` in the release step.
    **Avoid:** treat the compiled container as a build artifact; never edit
    `var/cache/` by hand, and always warm the cache on deploy.

??? abstract "Source-code tour"
    - `Symfony\Component\DependencyInjection\ContainerBuilder` — the build-time
      container; holds `Definition`s and runs `compile()`.
    - `Symfony\Component\DependencyInjection\Definition` &
      `Symfony\Component\DependencyInjection\Reference` — the recipe and the
      "wire me to that id" pointer.
    - `Symfony\Component\DependencyInjection\Compiler\PassConfig` — the ordered list
      of passes `compile()` executes.
    - `Symfony\Component\DependencyInjection\Dumper\PhpDumper` — turns the frozen
      builder into the optimised `*Container.php` served at runtime.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Invoice;

    use Psr\Log\LoggerInterface;

    // Autowired + registered by services.yaml resource loading.
    final class InvoiceGenerator
    {
        public function __construct(
            private readonly LoggerInterface $logger,
        ) {}

        public function generate(int $orderId): string
        {
            $this->logger->info('Generating invoice', ['order' => $orderId]);

            return \sprintf('INV-%06d', $orderId);
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/services.yaml
    services:
        _defaults:
            autowire: true      # inject by type-hint
            autoconfigure: true # apply tags by interface
            public: false       # private by default

        App\:
            resource: '../src/'
            exclude: '../src/{Entity,Kernel.php}'
    ```

=== "Console"

    ```console
    $ php bin/console debug:container App\\Invoice\\InvoiceGenerator
    $ php bin/console cache:clear   # rebuilds the compiled container
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Inject dependencies via the constructor | `$container->get('id')` in business code |
| Keep services private | Making services public "to be safe" |
| Let the compiler remove unused services | Manually `new`-ing wired services |
| Treat the compiled container as a build artifact | Editing `var/cache/` by hand |

## When (not) to use it / alternatives

Everything with behaviour and dependencies belongs in the container. Do **not**
register value objects, entities, or DTOs — build those with `new`. When you need
*many* services on demand without instantiating all of them, use a
[service locator](service-locators.md) instead of injecting the whole container.

!!! danger "Certification traps"
    - Services are **private by default** since Symfony 4; `$container->get()` on a
      private id throws `ServiceNotFoundException`.
    - `Definition`/`Reference`/`Alias` exist **only at build time**; the runtime
      container holds instances, not definitions.
    - The compiled container is a **dumped PHP class** in `var/cache/`, not the
      `ContainerBuilder`.
    - Services are **shared** by default — same instance on repeated `get()`.

!!! warning "Common mistakes"
    - Expecting config changes to take effect without a cache rebuild in `prod`.
    - Confusing *public* (fetchable by id) with *shared* (single instance) — they
      are independent flags.
    - Assuming autowiring or removal happens at runtime; it is all compile time.

## Exercises

1. **(Advanced)** Explain, in one sentence each, the difference between a
   `Definition` and the object it eventually produces.
2. **(Expert)** A teammate calls `$this->container->get(MailerInterface::class)`
   in a service and gets `ServiceNotFoundException`. Why, and what is the fix?
3. **(Expert)** Where on disk is the compiled container for the `prod` env, and
   what triggers its regeneration?

??? success "Solutions"

    **1.** A `Definition` is build-time metadata (class, arguments, flags) held by
    `ContainerBuilder`; the produced object is the runtime instance the dumped
    container creates from that recipe.

    **2.** `MailerInterface` resolves to a **private** service, so it is not
    fetchable by id. Inject it via the constructor (autowiring) instead of pulling
    it from the container.

    **3.** `var/cache/prod/` (a dumped `*Container.php` class). It is regenerated
    by `cache:clear` / `cache:warmup` — typically during deployment; in `dev` the
    `ConfigCache` rebuilds it automatically when a tracked config file changes.

## Certification questions

??? question "Q1. Why are Symfony services private by default?"
    - [ ] A. To make them read-only
    - [x] B. So the compiler can inline/remove them and enforce proper DI ✅
    - [ ] C. Because public services are deprecated
    - [ ] D. To make `get()` faster

    **Why:** Private services can be inlined into their sole consumer and pruned if
    unused, and it discourages the service-locator anti-pattern.
    **Ref:** [Service container](https://symfony.com/doc/current/service_container.html).

??? question "Q2. When does autowiring resolution happen?"
    - [x] A. At container **compilation** (build time) ✅
    - [ ] B. On every `get()` call at runtime
    - [ ] C. When the class file is autoloaded
    - [ ] D. During HTTP kernel termination

    **Why:** Autowiring is a compiler pass; the dumped container has arguments
    already resolved. **Ref:** [Autowiring](https://symfony.com/doc/current/service_container/autowiring.html).

??? question "Q3. `$container->get('some.private.service')` returns…"
    - [ ] A. The service instance
    - [x] B. Throws `ServiceNotFoundException` ✅
    - [ ] C. `null`
    - [ ] D. A new instance each call

    **Why:** Private services are not fetchable by id from the public container.
    **Ref:** [Service container](https://symfony.com/doc/current/service_container.html).

??? question "Q4. What is stored in `var/cache/prod/`?"
    - [ ] A. The `ContainerBuilder`
    - [ ] B. YAML definitions
    - [x] C. A dumped, compiled PHP container class ✅
    - [ ] D. Serialized service instances

    **Why:** `PhpDumper` writes an optimised PHP class with a method per service.
    **Ref:** [Compiling the container](https://symfony.com/doc/current/components/dependency_injection/compilation.html).

## Key takeaways

- A service is a container-managed object; value objects are not services.
- Build time = `ContainerBuilder` + `Definition`s; runtime = dumped container +
  instances.
- Compilation runs passes, resolves autowiring, removes private/unused services,
  then dumps a PHP class to `var/cache/`.
- Services are **private** and **shared** by default.

## Last-minute revision

!!! tip "Cheat sheet"
    - `ContainerBuilder.compile()` → `PassConfig` → freeze → `PhpDumper` → cache.
    - Private ≠ shared: independent flags. Both default to a "hidden, one instance"
      state.
    - `get()` on private id → `ServiceNotFoundException`.
    - `Definition`/`Reference`/`Alias`/`Parameter` = build-time metadata only.

## Connections

- **Depends on:** [Symfony Architecture](../architecture/index.md) — the kernel
  builds and boots the container.
- **Reused in:** [Controllers](../controllers/abstract-controller.md),
  [Console](../console/custom-commands.md),
  [Messenger](../miscellaneous/messenger.md) — every entry point pulls its
  collaborators from this container.
- **Confused with:** [Service Locators](service-locators.md) — a locator is a small
  PSR-11 subset, not the whole container.

## Official References
- [Official Symfony docs — Service Container](https://symfony.com/doc/current/service_container.html)
- [Official Symfony docs — Compiling the Container](https://symfony.com/doc/current/components/dependency_injection/compilation.html)
- [Symfony source — ContainerBuilder](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/ContainerBuilder.php)

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

- [ ] explain **why** the container exists and what problem DI solves
- [ ] build and wire a service in Symfony 8 (`autowire` + the `App\:` glob)
- [ ] debug a `ServiceNotFoundException` thrown on a private id
- [ ] spot the trick that services are private **and** shared by default
- [ ] explain compile-time (`ContainerBuilder`) vs runtime (dumped container)

---

<small>Related: [Registration](registration.md) · [Autowiring](autowiring.md) ·
[Compiler Passes](compiler-passes.md)</small>
