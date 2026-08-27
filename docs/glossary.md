# Glossary

Fast lookup of the terms the Symfony 8 certification uses. Each entry is one line;
follow the link for the full chapter.

!!! tip "How to use"
    Skim before the exam to lock in vocabulary. If a definition feels fuzzy, open
    the linked chapter and do its lab.

## A

- **AbstractController** — Base controller with helper shortcuts (`render`, `json`,
  `redirectToRoute`, `denyAccessUnlessGranted`…); a service subscriber. → [chapter](controllers/abstract-controller.md)
- **Access decision** — How authorization resolves a decision from voters via a
  strategy (affirmative/unanimous/consensus/priority). → [voters](security/voters.md)
- **`access_control`** — Firewall rules matched **top-to-bottom, first match wins**. → [chapter](security/access-control.md)
- **Argument value resolver** — Turns request data into typed controller arguments
  (`ValueResolverInterface`). → [chapter](controllers/value-resolvers.md)
- **Attribute** — PHP 8 `#[...]` metadata (e.g. `#[Route]`, `#[AsCommand]`). Preferred over annotations.
- **Autoconfiguration** — Auto-applies tags/calls to services by interface/attribute. → [registration](dependency-injection/registration.md)
- **Autowiring** — Injects service arguments by type-hint. → [chapter](dependency-injection/autowiring.md)

## B

- **Badge** — A piece of a `Passport` resolved on `CheckPassportEvent` (`UserBadge`,
  `CsrfTokenBadge`, `RememberMeBadge`…). → [authenticators](security/authenticators.md)
- **BC promise** — Backward-compatibility contract: breaking changes only in majors,
  after deprecation. → [chapter](architecture/bc-promise.md)
- **Bus (message bus)** — `MessageBusInterface`; runs a message through middleware to its handler. → [messenger](messenger/messages-handlers.md)

## C

- **Cache-Control** — HTTP header driving freshness (`max-age`, `s-maxage`, `public`,
  `private`, `no-cache`, `no-store`). → [expiration](http-caching/expiration.md)
- **CompiledContainer** — The dumped PHP container built once at compile time. → [container](dependency-injection/container.md)
- **Compiler pass** — `CompilerPassInterface`; mutates the container at build time
  (registered in `Kernel::build()` — **no `#[CompilerPass]` attribute**). → [chapter](dependency-injection/compiler-passes.md)
- **Constraint / Validator** — A rule (`Constraint`) + the class that enforces it
  (`ConstraintValidator`). → [custom constraints](validation/custom-constraints.md)
- **Content negotiation** — Choosing a response format from `Accept*` headers. → [chapter](http/content-negotiation.md)
- **CSRF token** — Anti-forgery token; stateless in Symfony 7.2+/8. → [chapter](forms/csrf.md)

## D

- **Data collector** — Feeds the Web Profiler (`DataCollectorInterface`). → [profiler](miscellaneous/profiler.md)
- **Data transformer** — Converts form model↔norm↔view data
  (`transform`/`reverseTransform`). → [chapter](forms/data-transformers.md)
- **Decoration** — Wrapping a service; higher `decoration_priority` = outermost; `.inner` = decorated. → [chapter](dependency-injection/decoration.md)
- **Deprecation** — `trigger_deprecation()`; a soft warning before a future removal. → [chapter](architecture/deprecations.md)

## E

- **Envelope** — Wraps a Messenger message with **stamps** (metadata). → [messenger](messenger/middleware.md)
- **ESI (Edge Side Includes)** — Cache fragments independently at a gateway. → [chapter](appendices/out-of-syllabus/esi.md)
- **ETag** — Validation cache header (content fingerprint); wins over `Last-Modified`. → [validation](http-caching/validation.md)
- **EventDispatcher** — Dispatches events to listeners/subscribers by priority. → [chapter](architecture/events.md)
- **`empty_data`** — Form value used when nothing is submitted. → [creation](forms/creation.md)

## F

- **Factory** — A callable that builds a service (static/instance/invokable). → [chapter](dependency-injection/factories.md)
- **Firewall** — The security context for a set of URLs; picks how identity is proven. → [chapter](security/firewalls.md)
- **Flash message** — One-shot session message read on the next request. → [chapter](controllers/flash-messages.md)
- **Flex** — Composer plugin that auto-configures packages via recipes. → [chapter](architecture/flex.md)

## G–H

- **Group (validation)** — A named subset of constraints; `Default` vs `{ClassName}`. → [groups](validation/groups.md)
- **GroupSequence** — Ordered validation; stops at the first failing group. → [chapter](validation/group-sequence.md)
- **HttpKernel** — Turns a `Request` into a `Response`; dispatches the 8 kernel events. → [request handling](architecture/request-handling.md)
- **HttpClient** — `HttpClientInterface`; test with `MockHttpClient`. → [chapter](http/httpclient.md)

## I–K

- **`#[IsGranted]`** — Attribute enforcing authorization on a controller/action. → [authorization](security/authorization.md)
- **`IS_AUTHENTICATED_*` / `PUBLIC_ACCESS`** — Runtime access attributes (not roles);
  `IS_AUTHENTICATED_ANONYMOUSLY` was replaced by `PUBLIC_ACCESS`. → [roles](security/roles.md)
- **Kernel events** — `kernel.request` → `controller` → `controller_arguments` →
  `view` → `response` → `finish_request` → `terminate` (+ `exception` out-of-band). → [request handling](architecture/request-handling.md)

## L–M

- **Last-Modified** — Timestamp validation cache header. → [validation](http-caching/validation.md)
- **Middleware (Messenger)** — Layers wrapping handling; russian-doll via `stack->next()`. → [messenger](messenger/middleware.md)
- **MockHttpClient** — In-memory HttpClient for tests. → [chapter](http/httpclient.md)

## N–P

- **`NotBlank` vs `NotNull`** — `NotBlank` rejects `''`/`[]`/blank; `NotNull` only rejects `null`. → [built-in constraints](validation/built-in-constraints.md)
- **Passport** — The authentication payload of badges built by an authenticator. → [authenticators](security/authenticators.md)
- **Password hasher** — One-way hashing (`auto`/bcrypt/sodium); supports rehash. → [chapter](security/password-hashers.md)
- **Profiler** — Dev debugging + data collectors; also usable in tests. → [chapter](miscellaneous/profiler.md)
- **PSR** — Shared interfaces Symfony implements/consumes (PSR-3/4/6/7/11/14/16/20). → [chapter](architecture/psr.md)

## Q–R

- **Reference type** — URL generation mode: `ABSOLUTE_PATH` (default), `ABSOLUTE_URL`,
  `NETWORK_PATH`, `RELATIVE_PATH`. → [url generation](routing/url-generation.md)
- **Retry strategy / failure transport** — Messenger redelivery then dead-letter. → [messenger](messenger/retries-failures.md)
- **Role hierarchy** — `ROLE_*` inheritance (e.g. `ROLE_ADMIN` ⊃ `ROLE_USER`). → [roles](security/roles.md)
- **Runtime** — Bootstraps the app entry point (`SymfonyRuntime`). → [chapter](miscellaneous/runtime.md)

## S

- **Service locator** — Lazy, on-demand access to a fixed set of services. → [chapter](dependency-injection/service-locators.md)
- **Serializer** — normalizers + encoders; `#[Groups]` controls fields. → [chapter](miscellaneous/serializer.md)
- **Stamp** — Metadata on a Messenger `Envelope`. → [messenger](messenger/middleware.md)
- **Stateless CSRF** — Cookie/origin-based CSRF without session (7.2+/8). → [csrf](forms/csrf.md)

## T–V

- **Tag** — Marks services for collection (`tagged_iterator`, `#[AutowireLocator]`). → [chapter](dependency-injection/tags.md)
- **Token / TokenStorage** — The current authentication state. → [authentication](security/authentication.md)
- **Value object** — Immutable typed data holder (often `readonly`). → [OOP](php-web-security/oop.md)
- **Voter** — Votes GRANTED/DENIED/ABSTAIN on an access decision. → [chapter](security/voters.md)

## W

- **WebTestCase / KernelTestCase** — Functional (HTTP client) vs integration
  (container) test base classes. → [functional tests](testing/functional-tests.md)
- **Web Profiler** — The dev toolbar + profiler UI. → [chapter](miscellaneous/profiler.md)

---

<small>Related: [Roadmap](roadmap.md) · [Revision Hub](revision/index.md) · [Cheat Sheet](revision/cheat-sheet.md)</small>

## Official References

- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Certification syllabus](https://certification.symfony.com/exams/symfony.html)
