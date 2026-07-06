# The Service Container

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

The **service container** (also *DI container*) is the object that instantiates
services, injects their dependencies, and hands them out on demand. In Symfony it
is defined by `Symfony\Component\DependencyInjection\ContainerInterface`. You
almost never build services with `new`; you describe *how* they are built and let
the container do it — lazily, once, and shared by default.

The crucial idea: there are **two containers**.

| | Build time | Runtime |
|---|---|---|
| Class | `ContainerBuilder` | dumped `App\..\Container*` |
| Holds | `Definition` objects | real service instances |
| When | cache warmup / first request | every request |
| Mutable? | yes (until frozen) | no |

## Deep Dive — how it works internally

### Definitions, not instances (build time)

During compilation nothing is instantiated. Each service is a
`Symfony\Component\DependencyInjection\Definition`: a recipe holding the class,
arguments, method calls, tags, `public`/`shared`/`lazy` flags and factory. A
`Symfony\Component\DependencyInjection\Reference` points to another service by id;
a `Symfony\Component\DependencyInjection\Alias` makes one id resolve to another;
a `Symfony\Component\DependencyInjection\Parameter` references a container
parameter. All of these are pure metadata objects.

`ContainerBuilder` extends `Container` and additionally stores these definitions,
aliases, extensions and compiler passes.

### The compilation pipeline

`ContainerBuilder::compile()` runs the passes registered in
`Symfony\Component\DependencyInjection\Compiler\PassConfig`, then **freezes**
parameters and marks the container compiled. Passes resolve autowiring, inline
private services, remove unused (private, unreferenced) definitions, and validate
references. See [Compiler Passes](compiler-passes.md) for the phase order.

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

## References

- [Official Symfony docs — Service Container](https://symfony.com/doc/current/service_container.html)
- [Official Symfony docs — Compiling the Container](https://symfony.com/doc/current/components/dependency_injection/compilation.html)
- [Symfony source — ContainerBuilder](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/ContainerBuilder.php)

---

<small>Related: [Registration](registration.md) · [Autowiring](autowiring.md) ·
[Compiler Passes](compiler-passes.md)</small>
