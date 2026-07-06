# Request Handling (HttpKernel)

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Trace a request from `public/index.php` to a `Response` through `HttpKernel::handle()`.
    - [ ] Name the **eight** `KernelEvents` and place them in the correct order.
    - [ ] Explain the roles of `ControllerResolverInterface` and `ArgumentResolverInterface`.
    - [ ] Distinguish main requests from sub-requests and know how `terminate()` fits in.

    **Syllabus:** `Symfony Architecture → Request Handling` ·
    **Level:** Expert ·
    **Est. time:** 40 min ·
    **Prerequisites:** [HTTP Request/Response](../http/request.md), [Events](events.md)

---

## Theory

Every Symfony HTTP request is turned into a response by a single contract:

```php
Symfony\Component\HttpKernel\HttpKernelInterface::handle(
    Request $request,
    int $type = self::MAIN_REQUEST,
    bool $catch = true
): Response
```

The front controller (`public/index.php`) boots the `Kernel`, builds a `Request`
from PHP superglobals, calls `handle()`, sends the returned `Response`, then calls
`terminate()`. Between `handle()` and `terminate()`, `HttpKernel` orchestrates a
sequence of **events** that let listeners observe or short-circuit the flow. This
event-driven core is what makes Symfony extensible without patching.

`self::MAIN_REQUEST` (value `1`) and `self::SUB_REQUEST` (value `2`) are the two
request types; the old `MASTER_REQUEST` constant was removed.

## Deep Dive — how it works internally

### The front controller and Runtime

`public/index.php` is intentionally tiny. The `symfony/runtime` component wraps it:
the returned callable receives autowired arguments (like `array $context` from the
server environment) and the `Runtime` handles `Request::createFromGlobals()`,
`$response->send()` and `$kernel->terminate()` for you.

```php
<?php
// public/index.php
use App\Kernel;

require_once dirname(__DIR__).'/vendor/autoload_runtime.php';

return function (array $context): Kernel {
    return new Kernel($context['APP_ENV'], (bool) $context['APP_DEBUG']);
};
```

### The classes in play

| Role | FQCN |
|---|---|
| Kernel | `Symfony\Component\HttpKernel\Kernel` (app: `App\Kernel`) |
| Kernel contract | `Symfony\Component\HttpKernel\HttpKernelInterface` |
| Engine | `Symfony\Component\HttpKernel\HttpKernel` |
| Controller resolution | `Symfony\Component\HttpKernel\Controller\ControllerResolverInterface` |
| Argument resolution | `Symfony\Component\HttpKernel\Controller\ArgumentResolverInterface` |
| Dispatcher | `Symfony\Contracts\EventDispatcher\EventDispatcherInterface` |
| Event names | `Symfony\Component\HttpKernel\KernelEvents` |

`Kernel::handle()` boots the container (once) and delegates to the
`http_kernel` service — an instance of `HttpKernel`. The real work lives in the
private `HttpKernel::handleRaw()`.

### The eight kernel events, in execution order

```mermaid
sequenceDiagram
    participant FC as index.php
    participant K as HttpKernel
    participant D as Dispatcher
    participant C as Controller
    FC->>K: handle(request)
    K->>D: kernel.request (RequestEvent)
    Note over D: routing, firewall, locale…
    D-->>K: response set? → skip to kernel.response
    K->>D: kernel.controller (ControllerEvent)
    K->>D: kernel.controller_arguments (ControllerArgumentsEvent)
    K->>C: call controller(...$args)
    C-->>K: Response OR any value
    K->>D: kernel.view (ViewEvent) — only if not a Response
    K->>D: kernel.response (ResponseEvent)
    K->>D: kernel.finish_request (FinishRequestEvent)
    K-->>FC: Response
    FC->>K: terminate() → kernel.terminate (TerminateEvent)
```

1. **`kernel.request`** — `RequestEvent`. Runs *before* routing decides anything
   the controller needs. `RouterListener` matches the route here (priority `32`);
   the security firewall authenticates here too. **If a listener calls
   `$event->setResponse()`, the kernel jumps straight to `kernel.response`** —
   the controller is never invoked.
2. **`kernel.controller`** — `ControllerEvent`. The `ControllerResolverInterface`
   has resolved the `_controller`; listeners may swap it with
   `$event->setController()`.
3. **`kernel.controller_arguments`** — `ControllerArgumentsEvent`. After
   `ArgumentResolverInterface::getArguments()` has built the argument array,
   listeners may alter it (`$event->setArguments()`).
4. *(controller is called)* — the controller returns a `Response` **or any other
   value**.
5. **`kernel.view`** — `ViewEvent`. **Only dispatched when the controller did not
   return a `Response`.** A listener must turn the returned value into a `Response`
   (e.g. serialize to JSON). If none does, an exception is thrown.
6. **`kernel.response`** — `ResponseEvent`. Every response passes through here;
   listeners tweak headers, inject the web-debug-toolbar, set cookies, etc.
7. **`kernel.finish_request`** — `FinishRequestEvent`. Fired after each request
   (main **and** every sub-request) so listeners can reset request-scoped state,
   e.g. restore the parent request's locale in the `RequestStack`.
8. **`kernel.terminate`** — `TerminateEvent`. Fired by `terminate()` *after* the
   response has been sent to the client. Ideal for heavy work you don't want the
   user to wait on (sending emails, dispatching messages via `kernel.terminate`).

The eighth `KernelEvents` constant, **`kernel.exception`** (`ExceptionEvent`), is
dispatched *out of band* — it is not part of the linear flow above but fires
whenever any exception escapes during `handleRaw()` (and `$catch` is `true`).
It is covered in [Exception Handling](exception-handling.md).

!!! note "Source reference"
    `Symfony\Component\HttpKernel\HttpKernel::handleRaw()` and
    `Symfony\Component\HttpKernel\KernelEvents` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpKernel.php).

### Controller and argument resolution

`ControllerResolverInterface::getController(Request): callable|false` reads the
`_controller` request attribute (set by the router) and returns a PHP callable.
`ArgumentResolverInterface::getArguments(Request, callable, ?ReflectionFunctionAbstract): array`
then builds the ordered argument list by running a chain of
`ValueResolverInterface` resolvers (request attributes, the `Request` object,
`#[MapRequestPayload]`, `#[MapQueryString]`, services, variadics, defaults…). See
[Argument Value Resolvers](../controllers/value-resolvers.md).

### Sub-requests

A controller (or listener) can render a fragment by calling `handle()` again with
`HttpKernelInterface::SUB_REQUEST`. Sub-requests run the **same** event flow
(`kernel.request` … `kernel.finish_request`) but **not** `kernel.terminate`.
`RequestStack` tracks the nesting so `getCurrentRequest()` and
`getMainRequest()` stay correct; `kernel.finish_request` restores parent state.

### Compilation vs runtime

`Kernel::boot()` loads the **compiled** container from
`var/cache/<env>/…Container.php`. The dispatcher, resolvers and listeners are all
services wired at **compile time** (see [Dependency Injection](../dependency-injection/index.md)).
At **runtime** `handle()` only *reads* that container — no configuration parsing —
which is why the hot path is fast. In `debug` mode the `ConfigCache` checks
freshness and rebuilds when source config changes.

### Performance & memory

- The event dispatch loop is the main per-request overhead; keep listeners cheap
  and use **priorities** rather than re-ordering registration.
- Prefer `kernel.terminate` for post-response work to shorten time-to-first-byte.
- Sub-requests are full request cycles — cache fragments (ESI/`render_esi`) rather
  than rendering many synchronous sub-requests.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventListener;

    use Symfony\Component\HttpKernel\Event\ResponseEvent;
    use Symfony\Component\EventDispatcher\Attribute\AsEventListener;
    use Symfony\Component\HttpKernel\KernelEvents;

    #[AsEventListener(event: KernelEvents::RESPONSE, priority: -10)]
    final class SecurityHeadersListener
    {
        public function __invoke(ResponseEvent $event): void
        {
            // Runs for every response passing through kernel.response.
            $event->getResponse()->headers->set('X-Frame-Options', 'DENY');
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/services.yaml
    services:
        App\EventListener\SecurityHeadersListener:
            tags:
                - { name: kernel.event_listener, event: kernel.response, priority: -10 }
    ```

=== "Console"

    ```console
    $ php bin/console debug:event-dispatcher kernel.request
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Short-circuit with `setResponse()` on `kernel.request` for maintenance/redirects | Doing routing work in the controller |
| Use `kernel.terminate` for slow after-response tasks | Blocking `kernel.response` with heavy I/O |
| Convert non-Response return values in a `kernel.view` listener | Returning arrays and hoping "it works" without a view listener |
| Use `debug:event-dispatcher` to inspect real order | Guessing listener priorities |

## When (not) to use it / alternatives

You almost never call `HttpKernel::handle()` yourself in application code — the
Runtime does it. You *do* hook the events. Reach for a **kernel event listener**
when behaviour must apply across many controllers (headers, auth, locale). For
per-controller concerns, prefer a controller argument resolver or the controller
itself.

!!! danger "Certification traps"
    - The order is **request → controller → controller_arguments → view →
      response → finish_request → terminate**, with **exception** injected on error.
      Memorise it.
    - `kernel.view` fires **only** when the controller returns a non-`Response`.
    - `kernel.terminate` fires **after** the response is sent, and **not** for sub-requests.
    - `MASTER_REQUEST` no longer exists — it is `MAIN_REQUEST`.
    - Setting a response on `kernel.request` skips the controller **and**
      `kernel.controller`/`kernel.view`, but still reaches `kernel.response`.

!!! warning "Common mistakes"
    - Confusing `kernel.finish_request` (per request, before returning) with
      `kernel.terminate` (once, after sending).
    - Assuming `kernel.controller_arguments` runs before argument resolution — it
      runs *after*, so you edit an already-built array.

## Exercises

1. **(Expert)** Write a listener that returns a `503` maintenance response for all
   requests when an env flag is set, without invoking any controller.
2. **(Expert)** Explain, in order, which events fire when a controller returns a
   plain array and a `kernel.view` listener serializes it to JSON.

??? success "Solutions"

    **1.** Listen on `KernelEvents::REQUEST` with a **positive** priority (so it
    runs before the router) and call `$event->setResponse(new Response('...', 503))`.
    The kernel skips straight to `kernel.response`.

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventListener;

    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\EventDispatcher\Attribute\AsEventListener;
    use Symfony\Component\HttpKernel\Event\RequestEvent;
    use Symfony\Component\HttpKernel\KernelEvents;

    #[AsEventListener(event: KernelEvents::REQUEST, priority: 100)]
    final class MaintenanceListener
    {
        public function __construct(private readonly bool $maintenance) {}

        public function __invoke(RequestEvent $event): void
        {
            if ($this->maintenance && $event->isMainRequest()) {
                $event->setResponse(new Response('Down for maintenance', 503));
            }
        }
    }
    ```

    **2.** `kernel.request` → `kernel.controller` → `kernel.controller_arguments`
    → controller returns `array` → `kernel.view` (listener builds a `JsonResponse`)
    → `kernel.response` → `kernel.finish_request`; then after send, `kernel.terminate`.

## Certification questions

??? question "Q1. In what order do these fire for a controller returning a Response?"
    - [ ] A. request → view → controller → response
    - [x] B. request → controller → controller_arguments → response ✅
    - [ ] C. controller → request → response → terminate

    **Why:** `kernel.view` is skipped because a `Response` was returned; the rest
    follow the canonical order. **Ref:** [HttpKernel component](https://symfony.com/doc/current/components/http_kernel.html#the-workflow-of-a-request).

??? question "Q2. When is `kernel.terminate` dispatched?"
    - [x] A. After the response is sent to the client, for the main request only ✅
    - [ ] B. Before `kernel.response`
    - [ ] C. Once per sub-request

    **Why:** `terminate()` runs post-send and is not called for sub-requests.
    **Ref:** [kernel.terminate](https://symfony.com/doc/current/reference/events.html#kernel-terminate).

??? question "Q3. A listener calls `setResponse()` on `kernel.request`. What happens?"
    - [ ] A. The controller still runs
    - [x] B. The controller is skipped; flow continues at `kernel.response` ✅
    - [ ] C. A `kernel.view` event is required

    **Why:** A response on `kernel.request` short-circuits controller resolution.
    **Ref:** [kernel.request](https://symfony.com/doc/current/reference/events.html#kernel-request).

## Key takeaways

- One entry point: `HttpKernel::handle()`; the logic is in `handleRaw()`.
- Eight events: request, controller, controller_arguments, view, response,
  finish_request, terminate (+ exception on error).
- `kernel.view` only for non-`Response` returns; `kernel.terminate` after send.
- Controller and argument resolution use `ControllerResolverInterface` /
  `ArgumentResolverInterface`.

## Last-minute revision

!!! tip "Cheat sheet"
    - `handle(Request, MAIN_REQUEST|SUB_REQUEST, catch=true): Response`
    - Order: **REQUEST → CONTROLLER → CONTROLLER_ARGUMENTS → VIEW → RESPONSE →
      FINISH_REQUEST → TERMINATE**; EXCEPTION on error.
    - `MAIN_REQUEST=1`, `SUB_REQUEST=2`; no `MASTER_REQUEST`.
    - `KernelEvents` constants = event-name strings (`kernel.request`, …).

## Official References
- [Official docs — HttpKernel workflow](https://symfony.com/doc/current/components/http_kernel.html)
- [Official docs — Built-in events](https://symfony.com/doc/current/reference/events.html)
- [Symfony source — HttpKernel](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpKernel.php)
- [Symfony source — KernelEvents](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/KernelEvents.php)

---

<small>Related: [Events](events.md) · [Exception Handling](exception-handling.md) · [Components](components.md) · [Value Resolvers](../controllers/value-resolvers.md)</small>
