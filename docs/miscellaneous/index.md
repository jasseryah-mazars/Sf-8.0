# Miscellaneous Components

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[Messenger Middleware](../labs/miscellaneous.md)** — a step-by-step TD with test-first guidance and a reference solution.

The advanced components that round out an Expert-level Symfony toolkit:
Serializer, PropertyAccess, Mailer & Mime, Cache, Process, Lock,
Intl/Translation, Runtime, Clock, Config/DotEnv/ExpressionLanguage, plus
error handling, debugging and deployment practice. Each is a decoupled
component you can use standalone or through the framework's autowiring.
**Messenger** — previously part of this stage — is now its own dedicated
stage: see [Messenger](../messenger/index.md), the single most tested topic
in the syllabus.

!!! abstract "Stage at a glance"
    - **Prerequisites:** [Architecture](../architecture/index.md) (kernel, events),
      [Dependency Injection](../dependency-injection/index.md) (autowiring, tags)
    - **Level:** Advanced → Expert
    - **Difficulty:** ★★☆
    - **Est. time:** 5–6 h
    - **Dependencies:** builds on Architecture + DI
    - **Revision priority:** **High** overall.

## Chapters

- [Configuration (Config, DotEnv, ExpressionLanguage)](configuration.md) — TreeBuilder,
  Processor, `.env` cascade + `.env.local.php`, expression syntax.
- [Error Handling](error-handling.md) — the ErrorHandler component, error/exception
  conversion, the error controller, prod vs dev.
- [Code Debugging](debugging.md) — VarDumper (`dump`/`dd`, cloners/dumpers, `Data`),
  the Debug tooling, Stopwatch.
- [Deployment Best Practices](deployment.md) — prod env, cache warmup, `--no-dev`,
  opcache/preload, dotenv dump, checklist.
- [Cache Component](cache.md) — PSR-6 vs PSR-16 vs Symfony contracts, adapters,
  tags, stampede protection.
- [Process Component](process.md) — `Process`, `run` vs `start`/`wait`, timeouts,
  streaming, exit codes, `fromShellCommandline` pitfalls.
- [Serializer Component](serializer.md) — normalizers + encoders, groups,
  `#[SerializedName]`, `#[Ignore]`, context, circular refs.
- [PropertyAccess Component](property-access.md) — dynamic property paths,
  the getter lookup order, magic-method fallbacks.
- [Mime & Mailer Components](mailer.md) — `Email`/`TemplatedEmail`, transports,
  attachments/embedding, async sending via Messenger, the Mime part model.
- [Filesystem & Finder Components](filesystem-finder.md) — file operations and
  the fluent file iterator.
- [Lock Component](../appendices/out-of-syllabus/lock.md) — `LockFactory`, blocking vs non-blocking, stores,
  expiring/auto-refreshing and shared locks.
- [Web Profiler & Data Collectors](profiler.md) — the toolbar, custom
  `DataCollectorInterface`, when it runs, prod disabling.
- [Internationalization and localization](intl.md) — Translator, ICU MessageFormat,
  domains, locale fallback, the Intl data component.
- [Runtime Component](runtime.md) — the entry-point flow, `RuntimeInterface`,
  `SymfonyRuntime`, `autoload_runtime.php`.
- [Clock Component](clock.md) — `ClockInterface`, `now()`, mock/monotonic/native
  clocks, `DatePoint`, testing time.

## Suggested reading order

Start with the data-shaping components — [Serializer](serializer.md),
[PropertyAccess](property-access.md), and [Mailer](mailer.md) — followed by
the infrastructure set
([Cache](cache.md), [Lock](../appendices/out-of-syllabus/lock.md), [Process](process.md),
[Filesystem & Finder](filesystem-finder.md)). Fold in
[Config](configuration.md), [Runtime](runtime.md), [Clock](clock.md) and
[Intl](intl.md), and finish with the operational trio
[Error Handling](error-handling.md), [Debugging](debugging.md),
[Profiler](profiler.md) and [Deployment](deployment.md).

## Official References

- [Symfony documentation — Symfony Components](https://symfony.com/doc/8.0/components/index.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
