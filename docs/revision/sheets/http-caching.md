# Revision Sheet — HTTP Caching

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [HTTP Caching](../../http-caching/index.md).

## Cache Types
- Three cache types: **private** (browser), **shared** (network), **reverse
  proxy** (yours).
- `public` opts a response into shared caching; `private` restricts it to the
  browser; the Symfony default is `no-cache, private`.
- `max-age` is for all caches; `s-maxage` is shared-only.
- `Vary` adds request headers to the cache key — use it precisely, never `*` or
  `Cookie`.

**Cheat:** Default `Cache-Control` = `no-cache, private`. Opt into sharing with `public`. `public`/`private` are mutually exclusive; last setter wins. `max-age` = everyone; `s-maxage` = shared caches only (browser ignores). `Vary` = extra cache-key headers. `Vary: *`/`Cookie` ≈ no shared caching. Reverse proxy = gateway cache = `HttpCache`/Varnish (a shared cache).

## Client-Side Caching
- The browser is a **private** cache: honours `max-age`/`Expires`, ignores
  `s-maxage`, may store `private`.
- `Cache-Control` request directives (`no-cache`, `max-age=0`, `only-if-cached`)
  let the client steer caches.
- Reload ≈ revalidate; hard reload ≈ full refetch; bfcache restores instantly.
- Only safe methods are cached; version asset URLs to bust the cache.

**Cheat:** Browser cache = private: `max-age`/`Expires`/`ETag`; ignores `s-maxage`. Reload → `max-age=0` (304 possible). Hard reload → `no-cache` (refetch). Fingerprinted asset → `public, max-age=31536000, immutable`. Cache busting = new URL, not "clearing" the browser cache.

## Expiration (Expires, Cache-Control)
- Freshness lets a cache answer without hitting the origin; precedence is
  `s-maxage` > `max-age` > `Expires` for shared caches.
- `setSharedMaxAge()` implies `public`; `must-revalidate` has no setter.
- `no-cache` = revalidate before reuse; `no-store` = never store.
- `stale-while-revalidate`/`stale-if-error` trade freshness for availability.
- `#[Cache]` is applied late on RESPONSE and never overrides explicit headers.

**Cheat:** `setMaxAge()` browser+shared · `setSharedMaxAge()` shared-only **+ public**. `setCache([...])` validates keys; unknown key → `InvalidArgumentException`. `no-cache` ≠ `no-store`. `must-revalidate` via `setCache`/attribute only. Shared freshness: `s-maxage` > `max-age` > `Expires`. `Age` counts elapsed. `#[Cache]` listener: CONTROLLER_ARGUMENTS (304 short-circuit) + RESPONSE −10.

## Server-Side Caching
- The Symfony reverse proxy is `HttpCache`, a PHP gateway cache that **wraps** the
  kernel and obeys standard HTTP headers (shared cache ⇒ `s-maxage`).
- Enable it with `framework.http_cache: true` or by wrapping in `public/index.php`.
- The default `Store` is filesystem; `private_headers` (Cookie/Authorization)
  keep authenticated requests out of the shared cache.
- `X-Symfony-Cache` is the trace header; `allow_reload`/`allow_revalidate` are off
  by default.
- Varnish/CDN are drop-in alternatives driven by the same headers.

**Cheat:** Class: `Symfony\Component\HttpKernel\HttpCache\HttpCache` (impl. `HttpKernelInterface` + `TerminableInterface`). Enable: `framework.http_cache: true` **or** wrap kernel with `Symfony\Bundle\FrameworkBundle\HttpCache\HttpCache`. Ctor: `(kernel, store, ?surrogate, options)`; default `Store` = filesystem. Trace header `X-Symfony-Cache`; `private_headers` = Cookie, Authorization. Shared cache → honours `s-maxage`; supports ESI.

## Validation (ETag, Last-Modified)
- Validation carries a fingerprint (`ETag`/`Last-Modified`) so caches ask "changed?"
  and get a bodyless `304` when not.
- `isNotModified()` mutates the response to 304 and strips the body; you return it.
- ETag beats Last-Modified when both conditional headers are present.
- `#[Cache]` expressions run pre-controller and SHA-256-hash the ETag.
- Combine a short TTL with a validator for cheap revalidation.

**Cheat:** `setEtag($v, weak?)` → `ETag`/`W/"..."`; `setLastModified(\DateTimeInterface)`. `isNotModified(Request)` → 304 + strips body; **still `return`** it. Conditional headers: `If-None-Match` (ETag) · `If-Modified-Since` (date). ETag wins over Last-Modified when both present. `#[Cache(etag:, lastModified:)]` → 304 before controller; ETag is SHA-256'd.
