# Automated Tests

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[Kernel/Web Tests](../labs/testing.md)** — a step-by-step TD with test-first guidance and a reference solution.

Symfony ships a complete testing stack on top of **PHPUnit**: unit tests for
services in isolation, and *functional* (HTTP-level) tests that boot the real
kernel, send requests through a synthetic browser, and assert on the response,
the DOM, and the internal state of the framework. This stage teaches the tooling
the exam cares about — `KernelTestCase`, `WebTestCase`, the test **Client**, the
**Crawler**, the **Profiler**, and the response assertions. The PHPUnit bridge
is covered here for completeness but is **excluded from Symfony 8
certification**.

!!! abstract "Stage at a glance"
    - **Prerequisites:** [Controllers](../controllers/index.md),
      [Routing](../routing/index.md), [Forms](../forms/index.md),
      [Dependency Injection](../dependency-injection/index.md)
    - **Level:** Advanced → Expert
    - **Difficulty:** ★★☆
    - **Est. time:** 3–4 h
    - **Dependencies:** you test what the earlier stages let you build;
      the Profiler chapter leans on
      [HTTP](../http/index.md) and the deprecation chapter cross-links
      [Architecture → Deprecations](../architecture/deprecations.md)
    - **Revision priority:** **Medium** — steady exam weight; the reliable points
      are `self::getContainer()` privacy, the `assertResponse*` helpers, and the
      deprecation-helper modes.

## Why this stage matters

Testing is where the whole framework comes together: a functional test exercises
routing, the controller, Twig, security and the event system in one shot. The
certification does not ask you to write large suites — it asks whether you know
*which class does what*, *which service is available in a test*, and *which
assertion to reach for*. Those are precise, memorisable facts, so this stage is
high value per minute of study.

## Chapters

- [Unit Tests with PHPUnit](unit-tests.md) — `TestCase`, assertions, `#[DataProvider]`,
  mocks vs stubs, PHPUnit 11/12 attributes, testing a service in isolation.
- [Functional Tests](functional-tests.md) — `WebTestCase` vs `KernelTestCase`,
  `createClient()`, the `test` environment, `self::getContainer()`.
- [The Client Object](client.md) — `request()`, `submitForm()`, `clickLink()`,
  redirects, `disableReboot()`, cookies and history.
- [The Crawler Object](crawler.md) — `filter()`/`filterXPath()`, `selectLink()`/
  `selectButton()`, extracting text/attributes, `form()`/`link()`.
- [The Profiler Object](profiler.md) — `enableProfiler()`, `getProfile()`, reading
  data collectors, asserting emails and events.
- [Framework Objects Access](framework-objects.md) — the test container, booting
  the kernel, replacing/mocking services in tests.
- [Client Configuration](client-configuration.md) — server parameters, HTTP auth,
  headers, environment/debug, insulated requests.
- [Request/Response Introspection](introspection.md) — `getRequest()`/`getResponse()`
  and the `assertResponse*` / `assertSelector*` helpers.
- [PHPUnit Bridge](../appendices/out-of-syllabus/phpunit-bridge.md) — deprecation collection, clock/DNS mocking,
  `SYMFONY_DEPRECATIONS_HELPER`, the Symfony PHPUnit extension. **Excluded from
  Symfony 8 certification.**
- [Handling Deprecated Code](deprecations.md) — `#[IgnoreDeprecations]`, helper
  modes (`max`, `disabled`, `weak`), baselines.

## Suggested reading order

Start with [Unit Tests](unit-tests.md) for the PHPUnit baseline, then
[Functional Tests](functional-tests.md) for the kernel-booting layer. Learn the
[Client](client.md), [Crawler](crawler.md) and
[Introspection](introspection.md) trio together — they are how a functional test
actually drives and asserts. Finish with the framework-integration and
diagnostics cluster: [Framework Objects](framework-objects.md),
[Client Configuration](client-configuration.md), [Profiler](profiler.md),
[PHPUnit Bridge](../appendices/out-of-syllabus/phpunit-bridge.md) and [Deprecations](deprecations.md).

## Official References

- [Symfony documentation — Testing](https://symfony.com/doc/8.0/testing.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
