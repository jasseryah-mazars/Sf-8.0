# Symfony Architecture

The kernel, the event-driven request lifecycle, the service container, and the
release/BC machinery that keeps it all stable. This is the **mental model** the
rest of the certification builds on: once you can trace a request from
`public/index.php` to a `Response` and back, every other component slots into
place.

!!! abstract "Stage at a glance"
    - **Prerequisites:** [HTTP](../http/index.md) (request/response model)
    - **Level:** Advanced → Expert
    - **Difficulty:** ★★★
    - **Est. time:** 5–7 h
    - **Dependencies:** builds on HTTP; feeds
      [Dependency Injection](../dependency-injection/index.md) and
      [Controllers](../controllers/index.md)
    - **Revision priority:** **Critical** — the most heavily tested stage;
      kernel-event order and the BC/deprecation policy appear on nearly every exam.

## Why this stage is Critical

Symfony is not a monolith you configure — it is a set of **decoupled components**
wired together by a **service container** and driven by an **event dispatcher**
around one class: `HttpKernel`. Understanding that flow explains *where* to hook
in (events, resolvers, compiler passes) and *why* the framework behaves as it
does. The exam probes the details relentlessly: the exact order of the eight
kernel events, what the Backward Compatibility promise does and does not cover,
and how deprecations are signalled and removed.

## Chapters

- [Symfony Flex](flex.md) — recipes, aliases, `symfony.lock`, automatic bundle wiring.
- [License](license.md) — the MIT licence, the Symfony trademark, what MIT allows.
- [Components](components.md) — the decoupled-component philosophy and the key ones.
- [Bridges](bridges.md) — what an integration bridge is and where it lives.
- [Code Organization](code-organization.md) — the app skeleton and bundle structure.
- [Request Handling (HttpKernel)](request-handling.md) — **the core**: the full
  `handle()` flow and the eight kernel events in order.
- [Exception Handling](exception-handling.md) — how exceptions become responses.
- [Event Dispatcher & Kernel Events](events.md) — listeners, subscribers,
  priorities, `#[AsEventListener]`, propagation.
- [Official Best Practices](best-practices.md) — the canonical do/don't list.
- [Release Management](release-management.md) — SemVer, standard vs LTS, maintenance.
- [Backward Compatibility Promise](bc-promise.md) — `@internal`, `@final`, experimental.
- [Deprecations Best Practices](deprecations.md) — `trigger_deprecation()`, detection, fixing.
- [Framework Overloading](overloading.md) — overriding services, templates, translations, config.
- [Roadmap & Schedule](roadmap-schedule.md) — the May/November cadence and the 8.x timeline.
- [Interoperability & PSRs](psr.md) — which PSRs Symfony implements or consumes.
- [Naming Conventions](naming-conventions.md) — classes, services, parameters, routes, env vars.

## Suggested reading order

Start with [Request Handling](request-handling.md) and [Events](events.md) to
build the runtime mental model, then [Exception Handling](exception-handling.md).
Cover [Components](components.md), [Bridges](bridges.md),
[Code Organization](code-organization.md) and [Flex](flex.md) for the ecosystem
picture. Finish with the policy cluster —
[Release Management](release-management.md),
[BC Promise](bc-promise.md), [Deprecations](deprecations.md),
[Roadmap](roadmap-schedule.md) — which is pure exam scoring.
