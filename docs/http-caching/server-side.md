# Server-Side Caching

!!! tip "In a nutshell"
    Symfony ships a reverse proxy written in PHP, `HttpCache`, that **wraps** your
    kernel and serves shared-cache hits before the app runs. Enable it with
    `framework.http_cache: true`; it honours `s-maxage`, keeps a filesystem
    `Store`, and reports each hit/miss in the `X-Symfony-Cache` trace header.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain what the Symfony reverse proxy (`HttpCache`) is and where it sits.
    - [ ] Enable it via `framework.http_cache` or by wrapping the kernel.
    - [ ] Describe `Store`, the lookup/write flow and the `X-Symfony-Cache` trace.
    - [ ] Decide when to use the PHP reverse proxy vs Varnish.

    **Syllabus:** `HTTP Caching → Server-side (reverse proxy)` ·
    **Level:** Expert ·
    **Est. time:** 25 min ·
    **Prerequisites:** [Cache Types](cache-types.md), [Expiration](expiration.md)

---

## Theory

A **reverse proxy** (gateway cache) is a shared cache you own, placed **in front
of** the application. It answers cache hits itself and only forwards misses to
the backend. Symfony ships one written in PHP:
`Symfony\Component\HttpKernel\HttpCache\HttpCache`. It is a drop-in
`HttpKernelInterface` that **wraps** your real kernel, so a request hits the
cache kernel first.

It obeys the standard headers you already know — `Cache-Control` (especially
`s-maxage`, since it is a *shared* cache), `Expires`, `ETag`, `Last-Modified`,
`Vary` — no bespoke config language. It also understands [ESI](esi.md).

!!! info "Development convenience, not always production"
    The PHP reverse proxy is a real, correct HTTP/1.1 cache — handy in dev and
    fine for small sites. High-traffic production usually fronts the app with a
    dedicated cache (Varnish, an HTTP-caching CDN); the same response headers
    drive both.

## Deep Dive — how it works internally

### The wrapping model

```mermaid
flowchart LR
    C[Client] --> HC[HttpCache kernel]
    HC -->|lookup| ST[(Store)]
    ST -->|fresh hit| C
    HC -->|miss / stale| K[App Kernel]
    K --> HC
    HC -->|write| ST
```

`HttpCache` implements `HttpKernelInterface` **and** `TerminableInterface`. Its
constructor is:

```php
public function __construct(
    HttpKernelInterface $kernel,
    StoreInterface $store,
    ?SurrogateInterface $surrogate = null,
    array $options = [],
)
```

- `$kernel` — your application kernel (the backend it protects).
- `$store` — where entries live; the default is
  `Symfony\Component\HttpKernel\HttpCache\Store`, a filesystem store keyed by URL
  + `Vary`, using digest files and lock files.
- `$surrogate` — an `Esi` or `Ssi` instance for [fragment](esi.md) processing.
- `$options` — behavioural knobs (below).

!!! note "Source reference"
    `Symfony\Component\HttpKernel\HttpCache\HttpCache`,
    `...\HttpCache\Store` and `...\HttpCache\StoreInterface` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php).

### The lookup → validate → store flow

1. **Only `GET`/`HEAD`** are cache candidates; unsafe methods pass through and
   invalidate matching entries.
2. **Private guard:** if the request carries a header in `private_headers`
   (default `Authorization`, `Cookie`), it is treated as private — not served
   from nor stored in the shared cache.
3. **Lookup** in the `Store` by URL + `Vary` headers.
4. **Fresh hit** → return the stored response, adding an `Age` header.
5. **Stale/miss** → forward to the backend; if the entry is *validateable*
   (`ETag`/`Last-Modified`), send a conditional request and turn a backend `304`
   into a refreshed store entry.
6. **Store** the backend response if it is cacheable, then serve it.

### Options that shape behaviour

| Option | Default | Effect |
|---|---|---|
| `debug` | `false` | Throw on errors; verbose trace |
| `default_ttl` | `0` | TTL when the response gives no freshness info |
| `private_headers` | `Authorization, Cookie` | Headers that mark a request private |
| `allow_reload` | `false` | Honour client `Cache-Control: no-cache` (force reload) |
| `allow_revalidate` | `false` | Honour client `max-age=0` (force revalidate) |
| `stale_while_revalidate` | `2` | Default background-revalidation window |
| `stale_if_error` | `60` | Default serve-stale-on-error window |
| `trace_header` | `X-Symfony-Cache` | Header carrying the hit/miss trace |
| `trace_level` | `full`/`none` | Verbosity of the trace |

### The `X-Symfony-Cache` trace

Every response carries a trace header (default `X-Symfony-Cache`) describing what
happened: `fresh`, `stale`, `miss`, `store`, `invalid`, e.g.
`X-Symfony-Cache: GET /: fresh`. It is your primary debugging tool — inspect it
to confirm hits.

!!! danger "`allow_reload`/`allow_revalidate` are off by default"
    Because letting any client force a cache bypass invites abuse, `allow_reload`
    and `allow_revalidate` default to **false**. A visitor's hard-reload does
    **not** blow past the shared cache unless you opt in.

## Configuration & code

=== "framework.http_cache (recommended)"

    ```yaml
    # config/packages/framework.yaml
    framework:
        # Boolean, or a map of the options above.
        http_cache:
            enabled: true
            trace_header: X-Symfony-Cache
            default_ttl: 0
    ```

    Symfony wraps the kernel with `HttpCache` automatically — no `public/index.php`
    changes needed. Enable it per-environment (typically prod).

=== "Wrap the kernel (index.php)"

    ```php
    <?php
    // public/index.php
    declare(strict_types=1);

    use App\Kernel;
    use Symfony\Bundle\FrameworkBundle\HttpCache\HttpCache;
    use Symfony\Component\HttpKernel\HttpKernelInterface;

    require_once dirname(__DIR__).'/vendor/autoload_runtime.php';

    return function (array $context): HttpKernelInterface {
        $kernel = new Kernel($context['APP_ENV'], (bool) $context['APP_DEBUG']);

        // Only wrap in prod; the FrameworkBundle subclass wires Store + options.
        if ('prod' === $context['APP_ENV']) {
            return new HttpCache($kernel);
        }

        return $kernel;
    };
    ```

=== "Console (debug)"

    ```console
    $ curl -sI https://localhost/articles | grep -i x-symfony-cache
    X-Symfony-Cache: GET /articles: fresh
    ```

!!! info "Which HttpCache class?"
    `Symfony\Bundle\FrameworkBundle\HttpCache\HttpCache` is a convenience
    **subclass** of the component's `HttpCache`. It reads the `Store` path from
    the kernel's cache dir and exposes `getOptions()`, `createStore()` and
    `createSurrogate()` to override. Use it when wrapping manually; the
    `framework.http_cache` flag uses the component class under the hood.

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Drive it with standard headers (`s-maxage`, `ETag`) | Expecting custom config to force caching |
| Enable it in **prod** only | Wrapping the kernel in dev (masks changes) |
| Read `X-Symfony-Cache` to verify hits | Guessing whether a response was cached |
| Front real traffic with Varnish/CDN at scale | Relying on the PHP proxy for very high load |

## When (not) to use it / alternatives

Use the PHP reverse proxy for local development, small/medium sites, and when you
want caching without extra infrastructure. Reach for **Varnish** or a caching
**CDN** at high traffic or when you need edge distribution — they speak the same
HTTP headers, so your Symfony code is unchanged. For per-fragment freshness on a
mostly-cacheable page, add [ESI](esi.md) (supported by both the PHP proxy and
Varnish).

!!! danger "Certification traps"
    - `HttpCache` is a **shared** cache, so it obeys `s-maxage` over `max-age`.
    - It implements `HttpKernelInterface` **and** `TerminableInterface` and
      **wraps** your kernel — it is not a bundle you enable with services alone.
    - A request with a **session cookie/`Authorization`** is treated as
      **private** by default (`private_headers`) and skips the shared cache.
    - `allow_reload`/`allow_revalidate` default to **false** — clients cannot
      force a bypass unless enabled.
    - The default `Store` is a **filesystem** store; there is no built-in shared
      distributed store.

!!! warning "Common mistakes"
    - Enabling the proxy in `dev` and then wondering why edits don't show up.
    - Assuming the reverse proxy needs Varnish — the PHP `HttpCache` works out of
      the box.

## Exercises

1. **(Advanced)** Enable the Symfony reverse proxy in prod only and confirm a
   route is being served from cache.
2. **(Expert)** A page sets `s-maxage=60` but never gets a shared-cache hit for
   logged-in users. Explain why, and how to still cache the anonymous version.

??? success "Solutions"

    **1.** Set `framework.http_cache: true` in `config/packages/framework.yaml`
    (guard with `when@prod` if you keep it prod-only), then
    `curl -sI` the route and check `X-Symfony-Cache: ...: fresh` on the second
    request.

    **2.** Logged-in requests send a session `Cookie`, which is in the proxy's
    `private_headers`, so they are treated as private and bypass the shared cache.
    Anonymous requests (no session cookie) *are* cached. To also cache the
    logged-in shell, move the per-user parts into [ESI](esi.md) fragments so the
    outer page stays anonymous/cacheable.

## Certification questions

??? question "Q1. What is `Symfony\Component\HttpKernel\HttpCache\HttpCache`?"
    - [ ] A. A Twig extension for cache tags
    - [x] B. A reverse-proxy kernel that wraps your app kernel ✅
    - [ ] C. A PSR-6 cache pool
    - [ ] D. A compiler pass

    **Why:** It implements `HttpKernelInterface`/`TerminableInterface` and wraps
    the real kernel, acting as an in-PHP gateway cache.
    **Ref:** [Symfony reverse proxy](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy).

??? question "Q2. Which request header, by default, makes `HttpCache` treat a request as private?"
    - [x] A. `Cookie` (and `Authorization`) ✅
    - [ ] B. `Accept`
    - [ ] C. `User-Agent`
    - [ ] D. `Referer`

    **Why:** The `private_headers` option defaults to `Authorization, Cookie`;
    such requests skip the shared cache.
    **Ref:** [HttpCache options](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php).

??? question "Q3. How do you inspect whether the reverse proxy served a hit?"
    - [ ] A. `X-Cache-Status`
    - [x] B. The `X-Symfony-Cache` trace header ✅
    - [ ] C. The `Age` header must be 0
    - [ ] D. `X-Debug-Cache`

    **Why:** `HttpCache` writes a trace (default header `X-Symfony-Cache`) like
    `GET /: fresh`/`miss`/`store`.
    **Ref:** [Debugging HttpCache](https://symfony.com/doc/current/http_cache.html).

??? question "Q4. The easiest way to enable the reverse proxy in Symfony 8 is…"
    - [x] A. `framework.http_cache: true` in config ✅
    - [ ] B. Registering a compiler pass
    - [ ] C. Installing Varnish
    - [ ] D. Adding `#[AsHttpCache]` to the kernel

    **Why:** The framework config flag wraps the kernel automatically; manual
    wrapping in `public/index.php` is the alternative.
    **Ref:** [Symfony reverse proxy](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy).

## Key takeaways

- The Symfony reverse proxy is `HttpCache`, a PHP gateway cache that **wraps** the
  kernel and obeys standard HTTP headers (shared cache ⇒ `s-maxage`).
- Enable it with `framework.http_cache: true` or by wrapping in `public/index.php`.
- The default `Store` is filesystem; `private_headers` (Cookie/Authorization)
  keep authenticated requests out of the shared cache.
- `X-Symfony-Cache` is the trace header; `allow_reload`/`allow_revalidate` are off
  by default.
- Varnish/CDN are drop-in alternatives driven by the same headers.

## Last-minute revision

!!! tip "Cheat sheet"
    - Class: `Symfony\Component\HttpKernel\HttpCache\HttpCache` (impl.
      `HttpKernelInterface` + `TerminableInterface`).
    - Enable: `framework.http_cache: true` **or** wrap kernel with
      `Symfony\Bundle\FrameworkBundle\HttpCache\HttpCache`.
    - Ctor: `(kernel, store, ?surrogate, options)`; default `Store` = filesystem.
    - Trace header `X-Symfony-Cache`; `private_headers` = Cookie, Authorization.
    - Shared cache → honours `s-maxage`; supports [ESI](esi.md).

## Official References
- [Symfony docs — Symfony reverse proxy](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy)
- [Symfony source — HttpCache](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php)
- [Symfony source — Store](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/Store.php)

---

<small>Related: [Cache Types](cache-types.md) · [Expiration](expiration.md) ·
[Edge Side Includes](esi.md) · [Architecture](../architecture/index.md)</small>
