# Exception Handling

!!! tip "In a nutshell"
    When an uncaught exception escapes, the kernel catches it and dispatches
    `kernel.exception` so a listener can turn it into a `Response`. Highest-yield:
    `ErrorListener` runs at priority **-128** (yours run first), and only
    `HttpExceptionInterface` carries a status code — everything else becomes **500**.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Trace how an uncaught exception becomes an HTTP `Response`.
    - [ ] Explain the role of `ErrorListener`, `kernel.exception` and the error controller.
    - [ ] Map an exception's class to a status code via `HttpExceptionInterface`.
    - [ ] Customise error pages and behaviour safely.

    **Syllabus:** `Symfony Architecture → Exception Handling` ·
    **Level:** Expert ·
    **Est. time:** 30 min ·
    **Prerequisites:** [Request Handling](request-handling.md), [Events](events.md)

---

## Theory

When any code in the request cycle throws and the exception is not caught, the
kernel must still produce a `Response`. It does this by dispatching the
**`kernel.exception`** event; a listener converts the exception into a response.
The candidate response otherwise defaults to `500`, unless the exception carries
its own status code.

## Deep Dive — how it works internally

### The catch in `handleRaw()`

`HttpKernel::handle(..., catch: true)` wraps `handleRaw()` in a `try/catch`. On an
exception it calls `handleThrowable()`, which dispatches an
`Symfony\Component\HttpKernel\Event\ExceptionEvent`. If a listener sets a response
via `$event->setResponse()`, that response is returned (still passing through
`kernel.response`); otherwise the exception is re-thrown. With `catch: false`
(often used in sub-requests and tests) the exception simply propagates.

### ErrorListener — the default converter

`Symfony\Component\HttpKernel\EventListener\ErrorListener` is registered on
`kernel.exception`. It:

1. logs the exception,
2. forwards to the **error controller** as a *sub-request*, and
3. sets the resulting response on the event.

It also runs at a **low priority (`-128`)** so your own `kernel.exception`
listeners get first chance to handle or transform the exception.

```mermaid
sequenceDiagram
    participant K as HttpKernel
    participant D as Dispatcher
    participant EL as ErrorListener (-128)
    participant EC as ErrorController
    Note over K: throwable escapes handleRaw()
    K->>K: catch in handle(catch: true)
    K->>D: dispatch kernel.exception (ExceptionEvent)
    Note over D: your listeners run first…
    D->>EL: __invoke(event)
    EL->>EC: forward as sub-request
    EC-->>EL: Response (status/headers via HttpExceptionInterface)
    EL-->>D: event->setResponse(...)
    D-->>K: Response → passes through kernel.response
```

If one of your higher-priority listeners sets a response first, `ErrorListener`
sees a response already set and does nothing; if none does, `ErrorListener`
produces the fallback error page (or re-throw path when `catch` is `false`).

### HttpExceptionInterface → status code

`Symfony\Component\HttpKernel\Exception\HttpExceptionInterface` exposes
`getStatusCode(): int` and `getHeaders(): array`. When the exception implements it,
`ErrorListener`/the error controller use that status code and headers; otherwise
the response is `500`. Common built-ins:

| Exception | Status |
|---|---|
| `NotFoundHttpException` | 404 |
| `AccessDeniedHttpException` | 403 |
| `BadRequestHttpException` | 400 |
| `MethodNotAllowedHttpException` | 405 |
| `HttpException` (generic) | any (constructor arg) |

Security's `AccessDeniedException` (a *different* class,
`Symfony\Component\Security\Core\Exception\AccessDeniedException`) is translated by
the firewall into a `403` (or a redirect to login for anonymous users) — it is not
itself an `HttpExceptionInterface`.

### The error controller

The default `error_controller` service is
`Symfony\Component\HttpKernel\Controller\ErrorController`. It renders an exception
via the configured error renderer. In `dev` you get the rich exception page; in
`prod` you get a clean status-code page. TwigBundle lets you override templates by
path: `templates/bundles/TwigBundle/Exception/error404.html.twig` (fallback:
`error.html.twig`).

```mermaid
flowchart TD
    A[Throw in handleRaw] --> B[catch in handle]
    B --> C[dispatch kernel.exception]
    C --> D{listener set response?}
    D -- yes --> E[ErrorListener/your listener → Response]
    D -- no --> F[re-throw]
    E --> G[kernel.response] --> H[Response]
```

!!! note "Source reference"
    `Symfony\Component\HttpKernel\EventListener\ErrorListener` and
    `HttpException` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/ErrorListener.php).

### Compilation vs runtime

The error controller, renderers and `ErrorListener` are wired at compile time by
FrameworkBundle. At runtime only the dispatch + sub-request happen. The `dev`
exception page depends on `kernel.debug = true`, resolved at boot.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventListener;

    use App\Exception\QuotaExceededException;
    use Symfony\Component\HttpFoundation\JsonResponse;
    use Symfony\Component\EventDispatcher\Attribute\AsEventListener;
    use Symfony\Component\HttpKernel\Event\ExceptionEvent;
    use Symfony\Component\HttpKernel\KernelEvents;

    #[AsEventListener(event: KernelEvents::EXCEPTION, priority: 0)]
    final class ApiExceptionListener
    {
        public function __invoke(ExceptionEvent $event): void
        {
            $e = $event->getThrowable();
            if ($e instanceof QuotaExceededException) {
                $event->setResponse(new JsonResponse(['error' => 'quota'], 429));
            }
        }
    }
    ```

=== "Throwing an HTTP exception"

    ```php
    <?php
    declare(strict_types=1);

    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    throw new NotFoundHttpException('Article not found.');
    // → ErrorListener produces a 404 response
    ```

=== "Twig error template"

    ```twig
    {# templates/bundles/TwigBundle/Exception/error404.html.twig #}
    <h1>Not found</h1>
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Throw `HttpExceptionInterface` subclasses for HTTP semantics | Returning `new Response('...', 500)` from deep code |
| Handle domain exceptions in a `kernel.exception` listener | Catching everything in each controller |
| Keep listener priority above `-128` to pre-empt `ErrorListener` | Depending on `ErrorListener` for API JSON |
| Override templates via `templates/bundles/TwigBundle/Exception/` | Editing vendor files |

## When (not) to use it / alternatives

Use `kernel.exception` for **global** exception-to-response policy (API error
envelopes, logging enrichment). For a single controller's expected failure,
throwing the right `HttpException` is enough. Do not use exceptions for normal
control flow.

!!! danger "Certification traps"
    - `kernel.exception` is **not** in the numbered main sequence; it fires only on error.
    - `ErrorListener` runs at priority **-128**, so custom listeners run first.
    - If no listener sets a response, the exception is **re-thrown** (and becomes a 500).
    - `AccessDeniedException` (Security) ≠ `AccessDeniedHttpException` (HttpKernel).

!!! warning "Common mistakes"
    - Forgetting that setting a response in `kernel.exception` still routes through
      `kernel.response`.
    - Assuming a plain `\RuntimeException` yields anything but `500`.

## Exercises

1. **(Advanced)** Make all `/api` exceptions return JSON `{ "error": ... }` with the
   correct status code.
2. **(Expert)** Explain why a `kernel.exception` listener at priority `-200` would
   never see the exception in practice.

??? success "Solutions"

    **1.** Register a `kernel.exception` listener; read `getThrowable()`, derive the
    status from `HttpExceptionInterface::getStatusCode()` (default `500`), and set a
    `JsonResponse`. Guard on `str_starts_with($request->getPathInfo(), '/api')`.

    **2.** `ErrorListener` at `-128` will already have set a response and (in older
    flows) may stop further handling; a `-200` listener runs after it and its
    changes are effectively moot for the produced response.

## Certification questions

??? question "Q1. Which event turns an exception into a response?"
    - [x] A. `kernel.exception` ✅
    - [ ] B. `kernel.view`
    - [ ] C. `kernel.terminate`

    **Why:** `ExceptionEvent` listeners set the response. **Ref:**
    [kernel.exception](https://symfony.com/doc/current/reference/events.html#kernel-exception).

??? question "Q2. What status code does a bare `\LogicException` produce?"
    - [ ] A. 404
    - [x] B. 500 ✅
    - [ ] C. 400

    **Why:** Only `HttpExceptionInterface` exceptions carry a status; others → 500.
    **Ref:** [Error pages](https://symfony.com/doc/current/controller/error_pages.html).

??? question "Q3. Where do you override the 404 template?"
    - [x] A. `templates/bundles/TwigBundle/Exception/error404.html.twig` ✅
    - [ ] B. `templates/error/404.twig` (no effect)
    - [ ] C. In `vendor/`

    **Why:** TwigBundle resolves overrides under `templates/bundles/<Bundle>/`.
    **Ref:** [Customizing error pages](https://symfony.com/doc/current/controller/error_pages.html).

## Key takeaways

- `handle(catch: true)` catches, then dispatches `kernel.exception`.
- `ErrorListener` (priority `-128`) forwards to the error controller as a sub-request.
- `HttpExceptionInterface::getStatusCode()` decides the status; default `500`.
- Override error templates under `templates/bundles/TwigBundle/Exception/`.

## Last-minute revision

!!! tip "Cheat sheet"
    - `ExceptionEvent::getThrowable()` / `setResponse()`.
    - `NotFoundHttpException` 404 · `AccessDeniedHttpException` 403 · `HttpException` any.
    - `ErrorListener` priority **-128**; `error_controller` = `ErrorController`.
    - No response set → re-thrown → 500.

## Official References
- [Official docs — Error pages](https://symfony.com/doc/current/controller/error_pages.html)
- [Official docs — kernel.exception](https://symfony.com/doc/current/reference/events.html#kernel-exception)
- [Symfony source — ErrorListener](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/ErrorListener.php)

---

<small>Related: [Request Handling](request-handling.md) · [Events](events.md) · [Error Pages](../controllers/error-pages.md)</small>
