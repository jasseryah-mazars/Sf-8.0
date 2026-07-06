# Error Handling

!!! tip "In a nutshell"
    The ErrorHandler component turns PHP errors into catchable exceptions and
    renders uncaught throwables (via a serializable `FlattenException`), while
    HttpKernel's `kernel.exception` flow turns an exception into a `Response`.
    Exam gold: only `HttpExceptionInterface` carries a custom status; everything
    else becomes a 500.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain how the ErrorHandler component turns PHP errors into exceptions.
    - [ ] Trace how an exception becomes an HTTP `Response` via the error controller.
    - [ ] Distinguish prod vs dev error output and customise error pages.

    **Syllabus:** `Miscellaneous → Error Handling` ·
    **Level:** Advanced ·
    **Est. time:** 30 min ·
    **Prerequisites:** [Request Handling](../architecture/request-handling.md)

---

## Theory

Two layers cooperate. The low-level **ErrorHandler** component converts PHP
**errors** (warnings, notices, fatals) into catchable exceptions and formats
uncaught throwables. The high-level **HttpKernel** layer catches exceptions
escaping a request and dispatches `kernel.exception` so a listener can build a
`Response`. This chapter focuses on the component; the kernel event flow is
covered in [Exception Handling](../architecture/exception-handling.md).

## Deep Dive — how it works internally

### The ErrorHandler component

`Symfony\Component\ErrorHandler\ErrorHandler` is registered early (via the
Runtime / `Debug::enable()` in debug mode). It:

- sets `set_error_handler()` to throw `\ErrorException` for PHP errors,
- sets `set_exception_handler()` to render uncaught throwables,
- registers a shutdown function to catch fatal errors.

Rendering is delegated to **error renderers** implementing
`Symfony\Component\ErrorHandler\ErrorRenderer\ErrorRendererInterface`:
`HtmlErrorRenderer` (the rich dev page with stack traces), `SerializerErrorRenderer`
(content-negotiated JSON/XML). Throwables are first normalised into a
`Symfony\Component\ErrorHandler\Exception\FlattenException`, a serializable
snapshot (class, message, status code, trace) safe to render or log.

```mermaid
flowchart LR
    E[PHP error] --> H[ErrorHandler]
    H -->|throw| Ex[\ErrorException]
    T[Uncaught throwable] --> FE[FlattenException]
    FE --> R[ErrorRendererInterface]
    R --> O[HTML / JSON / XML]
```

!!! note "Source reference"
    `Symfony\Component\ErrorHandler\ErrorHandler` and `FlattenException` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/ErrorHandler/ErrorHandler.php).

### In the framework: the error controller

When an exception escapes a request (`$catch = true`), HttpKernel dispatches
`kernel.exception`; the framework's `ErrorListener` calls the **error
controller** (`error_controller`, default
`Symfony\Component\HttpKernel\Controller\ErrorController`). It uses the
`ErrorRenderer` to produce the body and maps the throwable to a status code:
`HttpExceptionInterface::getStatusCode()` if it is an
`Symfony\Component\HttpKernel\Exception\HttpException` (e.g.
`NotFoundHttpException` → 404), otherwise **500**.

### Prod vs dev

| | dev (`APP_DEBUG=1`) | prod |
|---|---|---|
| Page | Rich exception page + trace | Clean error template |
| Detail | Full message/trace exposed | Generic, no internals |
| Renderer | `HtmlErrorRenderer` (debug) | template `error.html.twig` / status pages |

Override prod pages with Twig templates under `templates/bundles/TwigBundle/Exception/`
(`error404.html.twig`, `error500.html.twig`, or generic `error.html.twig`).

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    final class ProductController
    {
        public function show(?Product $product): never
        {
            // 404 status derived from HttpExceptionInterface
            throw new NotFoundHttpException('Product not found');
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/packages/framework.yaml
    framework:
        error_controller: App\Controller\CustomErrorController::show
    ```

=== "Console"

    ```console
    $ php bin/console debug:container error_controller
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Throw `HttpException` subclasses for HTTP status | Returning `new Response('', 404)` everywhere |
| Customise prod templates per status code | Leaking stack traces in prod |
| Log via `kernel.exception` listener | Swallowing exceptions silently |

## When (not) to use it / alternatives

You rarely instantiate `ErrorHandler` yourself — the Runtime wires it. Hook
`kernel.exception` to translate domain exceptions to responses, or register a
custom `error_controller` for full control over rendering.

!!! danger "Certification traps"
    - Non-`HttpException` throwables become **500**; only `HttpExceptionInterface`
      carries a custom status code.
    - `FlattenException` is the serializable form used for rendering/logging.
    - Dev exposes traces; prod must not — controlled by `APP_DEBUG`.

!!! warning "Common mistakes"
    - Expecting a custom 404 template to apply in `dev` (the debug page shows instead).
    - Confusing the ErrorHandler component with the `kernel.exception` event flow.

## Exercises

1. **(Advanced)** Return a 404 from a controller so the framework renders the
   correct error page.
2. **(Advanced)** Explain why an uncaught `\RuntimeException` yields a 500.

??? success "Solutions"

    **1.** Throw `NotFoundHttpException` (see code above); `ErrorController` maps it
    to 404 via `HttpExceptionInterface::getStatusCode()`.

    **2.** `\RuntimeException` does not implement `HttpExceptionInterface`, so the
    error controller defaults its status code to 500.

## Certification questions

??? question "Q1. An uncaught exception that is NOT an HttpException produces which status?"
    - [ ] A. 404
    - [x] B. 500 ✅
    - [ ] C. 400

    **Why:** Only `HttpExceptionInterface` carries a status; otherwise 500.
    **Ref:** [Errors & exceptions](https://symfony.com/doc/current/controller/error_pages.html).

??? question "Q2. What does the ErrorHandler do with a PHP warning?"
    - [x] A. Converts it into an `\ErrorException` ✅
    - [ ] B. Ignores it
    - [ ] C. Writes it to the response body

    **Why:** `set_error_handler()` throws `\ErrorException` so PHP errors are catchable.
    **Ref:** [ErrorHandler](https://symfony.com/doc/current/components/error_handler.html).

??? question "Q3. Which serializable object represents a throwable for rendering?"
    - [x] A. `FlattenException` ✅
    - [ ] B. `HttpException`
    - [ ] C. `ErrorEvent`

    **Why:** `FlattenException` snapshots the throwable for renderers/loggers.
    **Ref:** [ErrorHandler](https://symfony.com/doc/current/components/error_handler.html).

## Key takeaways

- ErrorHandler converts PHP errors to exceptions and renders uncaught throwables.
- `FlattenException` + `ErrorRendererInterface` produce HTML/JSON/XML output.
- `error_controller` maps throwables to responses; non-HTTP exceptions → 500.
- Prod hides internals; dev shows the trace — driven by `APP_DEBUG`.

## Last-minute revision

!!! tip "Cheat sheet"
    - `ErrorHandler` = `set_error_handler` + `set_exception_handler` + shutdown fn.
    - Renderers: `HtmlErrorRenderer`, `SerializerErrorRenderer`.
    - Status: `HttpExceptionInterface::getStatusCode()` else 500.
    - Prod templates: `templates/bundles/TwigBundle/Exception/error{404,500}.html.twig`.

## Official References
- [Official docs — Error pages](https://symfony.com/doc/current/controller/error_pages.html)
- [Official docs — ErrorHandler component](https://symfony.com/doc/current/components/error_handler.html)
- [Symfony source — ErrorHandler](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/ErrorHandler/ErrorHandler.php)

---

<small>Related: [Exception Handling](../architecture/exception-handling.md) · [Debugging](debugging.md) · [Profiler](profiler.md)</small>
