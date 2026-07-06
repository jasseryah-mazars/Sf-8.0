# Flashcards — HTTP Caching

26 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

??? question "1. Which Cache-Control value does a Symfony Response emit when you set no caching information at all?"
    **✅ no-cache, private**

    ResponseHeaderBag::computeCacheControlValue() defaults to "no-cache, private" when nothing is configured. It is safe (shared caches will not store it) but gives no caching benefit — you must opt in with public/max-age.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

??? question "2. Which caches honour the s-maxage directive?"
    **✅ Shared caches only (proxies and the reverse proxy)**

    s-maxage sets freshness for shared caches. Browsers (private caches) ignore it and fall back to max-age / Expires.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/expiration.html)

??? question "3. You call $response->setPublic() and then $response->setPrivate(). What is emitted?"
    **✅ Cache-Control: private (public is removed)**

    public and private are mutually exclusive; setPrivate() removes the public flag, so the later call wins. You can never emit "public, private".

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

??? question "4. What does the response header 'Vary: Accept-Language' instruct a cache to do?"
    **✅ Store a separate copy keyed by each distinct Accept-Language value**

    Vary adds the named request header(s) to the cache key, so each variant is stored and served independently. Vary:* or Vary:Cookie effectively disables shared caching.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

??? question "5. What does the Cache-Control directive 'no-cache' mean?"
    **✅ The response may be stored but must be revalidated before every reuse**

    no-cache permits storage but forces revalidation on each reuse. The directive that forbids storing at all is no-store.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

??? question "6. Besides setting s-maxage, what side effect does $response->setSharedMaxAge(600) have?"
    **✅ It marks the response public**

    A shared TTL is meaningless on a private response, so setSharedMaxAge() sets the public flag as well.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "7. For a shared cache, which freshness source takes precedence?"
    **✅ s-maxage, then max-age, then Expires**

    Shared caches resolve freshness as s-maxage > max-age > Expires. A private cache starts at max-age since it ignores s-maxage.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/expiration.html)

??? question "8. How do you emit a must-revalidate directive from a Response object?"
    **✅ $response->setCache(['must_revalidate' => true])**

    There is no dedicated setter; Response::mustRevalidate() is a getter returning bool. Use setCache(['must_revalidate' => true]) or #[Cache(mustRevalidate: true)].

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

??? question "9. Which #[Cache] options accept a relative date string like '1 hour' as well as an integer?"
    **✅ maxage, smaxage, staleWhileRevalidate, staleIfError**

    Those numeric-duration options accept an int (seconds) or a relative date string parsed via DateTimeImmutable. expires is a date string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#the-cache-attribute)

??? question "10. When Response::isNotModified() returns true, what has it done to the response?"
    **✅ Set the status to 304 and removed the body and content headers**

    isNotModified() mutates the response in place (status 304, strips the body and content-related headers). You still return the response yourself.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/validation.html)

??? question "11. A request carries both If-None-Match and If-Modified-Since. Which one decides the 304?"
    **✅ The ETag (If-None-Match) takes precedence**

    When an ETag is supplied it governs the comparison; Last-Modified alone only decides when no ETag is present.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "12. Using #[Cache(etag: 'post.getContent()')], what value is actually sent as the ETag?"
    **✅ The SHA-256 hash of the evaluated expression**

    CacheAttributeListener evaluates the expression on kernel.controller_arguments and SHA-256-hashes the result before using it as the ETag, so it can point at large content safely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#the-cache-attribute)

??? question "13. How do you produce a weak ETag with the Response API?"
    **✅ $response->setEtag('abc', weak: true)**

    The second boolean argument to setEtag() prefixes the value with W/. Conditional GET uses weak comparison regardless.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/validation.html)

??? question "14. With #[Cache(lastModified: 'post.getUpdatedAt()')], when can a 304 be returned?"
    **✅ Before the controller body runs, during kernel.controller_arguments**

    CacheAttributeListener evaluates the expression on CONTROLLER_ARGUMENTS (priority 10) and, if the request is up to date, replaces the controller so a 304 is returned without running the body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/CacheAttributeListener.php)

??? question "15. Which directive does a browser ignore when managing its own private cache?"
    **✅ s-maxage**

    The browser is a private cache; it honours max-age/Expires and ignores s-maxage, which targets shared caches.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)

??? question "16. A normal browser reload (not hard reload) typically sends which request directive?"
    **✅ Cache-Control: max-age=0 (revalidate)**

    A reload asks caches to revalidate via max-age=0 (a 304 is possible), whereas a hard reload sends no-cache to force a full refetch.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#request_directives)

??? question "17. What is the recommended header combination for a fingerprinted (content-hashed) asset?"
    **✅ public, max-age=31536000, immutable**

    A fingerprinted URL never changes content, so cache it long-term in every cache and skip revalidation with immutable. A new build yields a new URL.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

??? question "18. Which request is eligible to be served from the browser cache?"
    **✅ GET /page**

    Only safe methods (GET, HEAD) are cacheable; unsafe methods always hit the origin and may invalidate cached entries.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

??? question "19. What is Symfony\Component\HttpKernel\HttpCache\HttpCache?"
    **✅ A reverse-proxy kernel that wraps your application kernel**

    HttpCache implements HttpKernelInterface and TerminableInterface and wraps the real kernel, acting as an in-PHP shared gateway cache.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy)

??? question "20. By default, which request header makes the Symfony reverse proxy treat a request as private?"
    **✅ Cookie (and Authorization)**

    The private_headers option defaults to Authorization and Cookie; requests carrying them skip the shared cache, protecting authenticated responses.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php)

??? question "21. Which header lets you inspect whether the reverse proxy served a cache hit?"
    **✅ X-Symfony-Cache**

    HttpCache writes a trace to the trace_header (default X-Symfony-Cache), e.g. "GET /: fresh", "miss", or "store".

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

??? question "22. What is the simplest way to enable the reverse proxy in Symfony 8?"
    **✅ Set framework.http_cache: true in configuration**

    framework.http_cache: true wraps the kernel automatically. The alternative is wrapping it manually in public/index.php with the FrameworkBundle HttpCache subclass.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy)

??? question "23. When does the render_esi Twig function actually emit an <esi:include> tag?"
    **✅ Only when a surrogate advertises ESI capability; otherwise it renders the fragment inline**

    The ESI renderer checks the Surrogate-Capability. Without a surrogate it falls back to inline rendering so the same template works everywhere.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

??? question "24. What is the primary benefit of ESI over full-page caching?"
    **✅ Each fragment can be cached with its own independent lifetime**

    ESI caches fragments as separate entries, so a long-lived shell can coexist with short-lived or per-user fragments on one page.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

??? question "25. Which component processes <esi:include> tags?"
    **✅ The reverse proxy / surrogate (Symfony HttpCache or Varnish)**

    ESI is a surrogate feature; the gateway cache fetches each include as a sub-request and stitches the results, caching each on its own terms.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/Esi.php)

??? question "26. Why does Symfony sign _fragment URIs (UriSigner)?"
    **✅ To prevent attackers forging arbitrary fragment requests**

    Fragment URIs are signed with the application secret so only legitimately generated fragment calls are honoured by the kernel.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

---

<small>Back to [Flashcards](index.md) · [HTTP Caching](../../http-caching/index.md)</small>
