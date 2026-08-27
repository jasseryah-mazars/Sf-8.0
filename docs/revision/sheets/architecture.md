# Revision Sheet — Symfony Architecture

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Symfony Architecture](../../architecture/index.md).

## Backward Compatibility Promise
- Public, non-`@internal`, non-experimental API is stable within a major.
- BC breaks only in majors, only after deprecation.
- `@internal`, `final`/`@final`, `@experimental` carve exceptions out of the promise.
- Extend via events/decoration/DI, not inheritance of framework classes.

**Cheat:** Covered: stable public API within a major. Not covered: `@internal`, `@experimental`; don't subclass `final`. Breaks: major only, post-deprecation. Users vs extenders: extenders have fewer guarantees.

## Official Best Practices
- Thin controllers; business logic in private, autowired services.
- Attributes for routing/validation; env vars/secrets for config.
- Practices exist to keep the compiled container lean and the app testable.
- They're recommendations for apps — bundles have their own conventions.

**Cheat:** Logic → services (private, autowired). Routing/validation → attributes. Infra → env vars · secrets → vault · behaviour → parameters. Smoke-test every public URL.

## Bridges
- A bridge is glue between a component and one specific third-party library.
- It keeps components free of external dependencies.
- Bridges live in `src/Symfony/Bridge/` and are typically wired by a bundle.

**Cheat:** Bridge = component + specific 3rd-party lib. Package name: `symfony/<name>-bridge`; dir `src/Symfony/Bridge/`. Classes come from the bridge, services from a bundle.

## Code Organization
- Skeleton: `bin/ config/ public/ src/ templates/ var/ vendor/ tests/`.
- `public/index.php` is the only front controller; web root is `public/`.
- `App\Kernel` uses `MicroKernelTrait` to load bundles + config.
- Modern bundles use the new layout; `getParent()` inheritance is removed.

**Cheat:** Web root = `public/`; caches/logs = `var/`; deps = `vendor/`. Bundles → `config/bundles.php`; services → `config/services.yaml`. Env overrides → `config/packages/<env>/`. Kernel = `MicroKernelTrait`.

## Components
- Symfony = decoupled components + a framework that wires them.
- Contracts hold interfaces; components hold implementations; bundles integrate.
- Each component is its own SemVer Composer package, usable standalone.

**Cheat:** Component = library · Contract = interfaces · Bridge = 3rd-party glue · Bundle = framework wiring. Type-hint contracts/interfaces for swap-ability. `composer require symfony/<name>` — no full framework needed.

## Deprecations Best Practices
- Use `trigger_deprecation(package, version, message, ...args)` from the contracts package.
- Deprecations are `E_USER_DEPRECATED` notices, removed only in the next major.
- Detect via the profiler and the `deprecation` log channel.

**Cheat:** `trigger_deprecation('pkg', 'X.Y', 'msg %s', $arg)` — package, version, msg, args. Level: `E_USER_DEPRECATED`. Removed: next major. Detect: toolbar/profiler, `deprecation` log channel. DI: `deprecated:` key / `Definition::setDeprecated()`.

## Event Dispatcher & Kernel Events
- Dispatcher sorts by priority (desc), memoises, and invokes lazily-built listeners.
- Listener = one event; subscriber = many events in `getSubscribedEvents()`.
- `dispatch(object, ?name)` — PSR-14 order.
- `stopPropagation()` halts only the current event's remaining listeners.

**Cheat:** Register: `#[AsEventListener]`, tag `kernel.event_listener`, or subscriber. `getSubscribedEvents(): array` → `[EventName => 'method' | ['method', prio] | [['m',prio],…]]`. Default priority `0`; higher first. Compiled by `RegisterListenersPass`.

## Exception Handling
- `handle(catch: true)` catches, then dispatches `kernel.exception`.
- `ErrorListener` (priority `-128`) forwards to the error controller as a sub-request.
- `HttpExceptionInterface::getStatusCode()` decides the status; default `500`.
- Override error templates under `templates/bundles/TwigBundle/Exception/`.

**Cheat:** `ExceptionEvent::getThrowable()` / `setResponse()`. `NotFoundHttpException` 404 · `AccessDeniedHttpException` 403 · `HttpException` any. `ErrorListener` priority **-128**; `error_controller` = `ErrorController`. No response set → re-thrown → 500.

## Symfony Flex
- Flex is a Composer plugin: aliases + recipes automate setup.
- Recipes run configurators (bundles, config, env) via `manifest.json`.
- `symfony.lock` records installed recipes and is committed.
- Bundles register through `config/bundles.php`, read by the kernel at boot.

**Cheat:** Alias → real package; recipe → automation. Recipe sources: `symfony/recipes` (main), `symfony/recipes-contrib` (opt-in). `symfony.lock` = recipes; `composer.lock` = versions. `composer recipes` / `recipes:update`.

## License & Trademark
- Symfony is MIT-licensed: use/modify/sell freely, even closed-source.
- The sole condition is keeping the copyright + permission notice.
- "Symfony" name/logo is a trademark, governed separately from the code.

**Cheat:** License = **MIT** (permissive, non-copyleft). Obligation = keep the notice. Trademark ≠ license — name/logo need the trademark policy.

## Naming Conventions
- Classes PascalCase; `Interface`/`Trait` suffixes; `Abstract` prefix; `Exception` suffix.
- Service id = FQCN; parameters/config keys snake_case; tags dotted lowercase.
- Routes snake_case (`entity_action`); env vars UPPER_SNAKE, `APP_`-prefixed.
- Naming feeds autoconfiguration and the router — it is functional, not cosmetic.

**Cheat:** Interface→`Interface`, Trait→`Trait`, Abstract→`Abstract…`, Exception→`Exception`. Constants UPPER_SNAKE; enum cases PascalCase. Service id = FQCN; params snake_case; routes snake_case. Env vars: `APP_*` UPPER_SNAKE; read via `%env(...)%`.

## Framework Overloading
- Services: redefine, decorate, or use a compiler pass.
- Templates: `templates/bundles/<BundleName>/`; translations: app `translations/` win.
- Config: `config/packages/<alias>.yaml` (+ `<env>/`).
- Bundle inheritance (`getParent()`) is removed — use per-resource overriding.

**Cheat:** Template override path: `templates/bundles/<BundleName>/…`. Decorate: `#[AsDecorator(decorates: id)]` + `#[AutowireDecorated]` → `.inner`. Config override: `config/packages/<alias>.yaml`. No `getParent()` in Symfony 8.

## Interoperability & PSRs
- Symfony implements PSR-6, PSR-11, PSR-14, PSR-16, PSR-20; consumes PSR-3; follows PSR-4/12.
- HttpFoundation ≠ PSR-7; the psr-http-message bridge converts (PSR-7/15/17).
- Type-hint PSR interfaces for cross-library portability.

**Cheat:** Implements: PSR-6 (Cache), PSR-11 (Container), PSR-14 (EventDispatcher), PSR-16, PSR-20 (Clock). Consumes: PSR-3 (Logger). Autoload: PSR-4. PSR-7/15/17 → via psr-http-message **bridge**.

## Release Management
- SemVer + time-based: minors in May/Nov, majors every 2 years.
- Standard: 8 months bug / 14 months security. LTS (`X.4`): 3 years / 4 years.
- `8.4` is the Symfony 8 LTS and ships with `9.0`.
- Minors add features + deprecations; only majors break BC.

**Cheat:** Minor = May & Nov · Major = every 2 yr. LTS = `X.4` (3 yr bug + 4 yr sec) · Standard = 8 mo bug + 14 mo sec. Patch: bugs only · Minor: features+deprecations, BC-safe · Major: removals.

## Request Handling (HttpKernel)
- One entry point: `HttpKernel::handle()`; the logic is in `handleRaw()`.
- Eight events: request, controller, controller_arguments, view, response,
  finish_request, terminate (+ exception on error).
- `kernel.view` only for non-`Response` returns; `kernel.terminate` after send.
- Controller and argument resolution use `ControllerResolverInterface` /
  `ArgumentResolverInterface`.

**Cheat:** `handle(Request, MAIN_REQUEST|SUB_REQUEST, catch=true): Response` Order: **REQUEST → CONTROLLER → CONTROLLER_ARGUMENTS → VIEW → RESPONSE → FINISH_REQUEST → TERMINATE**; EXCEPTION on error. `MAIN_REQUEST=1`, `SUB_REQUEST=2`; no `MASTER_REQUEST`. `KernelEvents` constants = event-name strings (`kernel.request`, …).

## Roadmap & Schedule
- Minors: May & November; majors + LTS: every 2 years.
- 8.x: 8.0 → 8.4, with 8.4 the LTS shipping alongside 9.0 (Nov 2027).
- Combine dates with maintenance windows to plan upgrades.

**Cheat:** 8.0 Nov'25 · 8.1 May'26 · 8.2 Nov'26 · 8.3 May'27 · 8.4 LTS Nov'27 (+9.0). LTS = `X.4`, ships with `(X+1).0`. `php bin/console about` shows EOL dates.
