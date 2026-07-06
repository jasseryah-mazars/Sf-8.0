# Controllers

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[Value Resolver](../labs/controllers.md)** — a step-by-step TD with test-first guidance and a reference solution.

A **controller** is the PHP callable Symfony runs to turn a `Request` into a
`Response`. It is the first *feature layer* you write on top of the kernel and
the container: everything from the [request lifecycle](../architecture/index.md)
and [dependency injection](../dependency-injection/index.md) converges here.
This stage teaches how controllers are resolved, what conveniences
`AbstractController` gives you, how arguments are filled by **value resolvers**,
and how to speak fluent [HttpFoundation](../http/index.md) — requests, responses,
cookies, sessions, and flash messages.

!!! info "Stage at a glance"
    | Field | Value |
    |---|---|
    | **Prerequisites** | [Architecture](../architecture/index.md), [Dependency Injection](../dependency-injection/index.md), [HTTP](../http/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Stages 3 & 4 |
    | **Revision priority** | **High** |
    | **Est. time** | 3–4 h |

## Why this stage matters

A controller is deceptively simple — "return a `Response`" — but the exam probes
the machinery around it: how `ControllerResolverInterface` finds your callable,
how `ArgumentResolverInterface` fills its parameters, why `AbstractController`
is a *service subscriber* rather than a god-object base class, and the exact
lifecycle of a flash message or a sub-request. Master the mechanics here and
routing, forms, and security become straightforward.

## Micro-chapters

- [Naming Conventions](naming-conventions.md) — controller naming, single-action
  (invokable) controllers, `__invoke`, the `Action` suffix myth.
- [AbstractController](abstract-controller.md) — the helper methods it provides,
  how it obtains services via `getSubscribedServices()`, and why it is *not* a
  `ControllerBase`.
- [The Request](request.md) — type-hinting `Request`, the parameter bags, and how
  the `Request` reaches your action (cross-links [HTTP → Request](../http/request.md)).
- [The Response](response.md) — `Response`, `JsonResponse`, streamed and binary
  responses (cross-links [HTTP → Response](../http/response.md)).
- [Cookies](cookies.md) — reading and setting cookies from a controller.
- [The Session](session.md) — `RequestStack::getSession()`, `SessionInterface`,
  the attribute bag, storage, invalidation, and lazy sessions.
- [Flash Messages](flash-messages.md) — `addFlash()`, `FlashBagInterface`,
  rendering in Twig, and the one-shot lifecycle.
- [HTTP Redirects](http-redirects.md) — `redirectToRoute()`, `redirect()`,
  `RedirectResponse`, 301 vs 302, and other redirect status codes.
- [Internal Redirects (Forwarding)](internal-redirects.md) — `forward()`,
  sub-requests, and how they differ from an HTTP redirect.
- [404 & Error Pages](error-pages.md) — `createNotFoundException()`, throwing
  `HttpException`, and customizing error templates/controllers.
- [File Upload](file-upload.md) — `UploadedFile`, moving files, `#[MapUploadedFile]`
  (cross-links [Forms → File Upload](../forms/file-upload.md)).
- [Built-in Internal Controllers](built-in-controllers.md) — `TemplateController`
  and `RedirectController` driven purely from route config.
- [Argument Value Resolvers](value-resolvers.md) — `ValueResolverInterface`, the
  built-in resolvers, targeted resolvers, writing your own, and priorities.

## How to study this stage

1. Read [Naming](naming-conventions.md) and [AbstractController](abstract-controller.md)
   first — they frame everything else.
2. Do the [Value Resolvers](value-resolvers.md) deep dive hands-on; it is the most
   internals-heavy and most examined topic in this stage.
3. Treat [Session](session.md), [Flash](flash-messages.md), and
   [redirects](http-redirects.md) as a trio — they share the request/response cycle.

---

<small>Prev stage: [Dependency Injection](../dependency-injection/index.md) · Next stage: [Routing](../routing/index.md)</small>

## Official References

- [Symfony documentation — Controllers](https://symfony.com/doc/current/controller.html)
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
