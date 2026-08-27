# Chapter Exam — HTTP Caching

!!! abstract "How to use"
    52 questions spanning every subchapter of **HTTP Caching**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [HTTP Caching](../http-caching/index.md).

---

**Q1.** Which caches honour the s-maxage directive?  <small>_(easy · single)_</small>

- A. Shared caches only (proxies and the reverse proxy)
- B. The browser only
- C. Every cache including the browser
- D. None — it is a request-only directive

??? success "Answer Q1"
    **A**

    s-maxage sets freshness for shared caches. Browsers (private caches) ignore it and fall back to max-age / Expires. It is a response directive, not a request one, and every cache honouring it would be max-age, not s-maxage.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/expiration.html)

**Q2.** What does the response header 'Vary: Accept-Language' instruct a cache to do?  <small>_(easy · single)_</small>

- A. Store a separate copy keyed by each distinct Accept-Language value
- B. Reject requests that lack an Accept-Language header
- C. Translate the response body automatically
- D. Disable caching entirely

??? success "Answer Q2"
    **A**

    Vary adds the named request header(s) to the cache key, so each variant is stored and served independently. It never rejects requests or translates content. Vary:* or Vary:Cookie effectively disables shared caching by exploding the key space.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

**Q3.** A reverse proxy (gateway cache) such as Symfony HttpCache or Varnish is a shared cache.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q3"
    **A**

    A reverse proxy / gateway cache serves many users, so it is a shared cache you own and deploy in front of the app — it therefore honours s-maxage. Only the browser is a private cache.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q4.** What does the Cache-Control directive 'no-cache' mean?  <small>_(easy · single)_</small>

- A. The response may be stored but must be revalidated before every reuse
- B. The response must never be stored anywhere
- C. The response is fresh forever
- D. The response is private to the browser

??? success "Answer Q4"
    **A**

    no-cache permits storage but forces revalidation on each reuse. The directive that forbids storing at all is no-store. It says nothing about freshness duration or private/shared scope.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

**Q5.** Cache-Control: no-cache tells caches never to store the response.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q5"
    **B**

    False. no-cache permits storing but requires revalidation before every reuse. The directive that forbids storage entirely is no-store — the single most common Cache-Control misconception.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

**Q6.** A request carries both If-None-Match and If-Modified-Since. Which one decides the 304?  <small>_(easy · single)_</small>

- A. The ETag (If-None-Match) takes precedence
- B. The date (If-Modified-Since) takes precedence
- C. Whichever value is larger
- D. Both are ignored and a 200 is always returned

??? success "Answer Q6"
    **A**

    When an ETag is supplied it governs the comparison; Last-Modified alone only decides when no ETag is present. The two are not compared by magnitude, and a 200 is not forced.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q7.** A 304 Not Modified response must be sent without a message body.  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q7"
    **A**

    True. A 304 carries no message body — the client already holds the bytes. Symfony enforces this: isNotModified() strips the body and content headers when it sets the 304 status.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests)

**Q8.** Which conditional request header does a client send to revalidate an ETag?  <small>_(easy · single)_</small>

- A. If-None-Match
- B. If-Modified-Since
- C. If-Match
- D. If-Range

??? success "Answer Q8"
    **A**

    ETags round-trip via If-None-Match for a conditional GET. If-Modified-Since pairs with Last-Modified (a date), while If-Match and If-Range serve write concurrency and range requests, not cache revalidation of a GET.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests)

**Q9.** Which directive does a browser ignore when managing its own private cache?  <small>_(easy · single)_</small>

- A. s-maxage
- B. max-age
- C. no-store
- D. immutable

??? success "Answer Q9"
    **A**

    The browser is a private cache; it honours max-age/Expires, no-store and immutable, but ignores s-maxage, which targets shared caches only.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)

**Q10.** Which request is eligible to be served from the browser cache?  <small>_(easy · single)_</small>

- A. GET /page
- B. POST /orders
- C. DELETE /orders/5
- D. PATCH /orders/5

??? success "Answer Q10"
    **A**

    Only safe methods (GET, HEAD) are cacheable; unsafe methods (POST, PUT, PATCH, DELETE) always hit the origin and may invalidate cached entries for the target URL.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

**Q11.** What does the request directive Cache-Control: only-if-cached ask a cache to do?  <small>_(easy · single)_</small>

- A. Return a cached copy if available, otherwise respond 504 without contacting the origin
- B. Always revalidate the cached copy with the origin
- C. Store the response only if it is cacheable
- D. Accept a stale response up to a given age

??? success "Answer Q11"
    **A**

    only-if-cached forbids any origin request: the cache serves a stored entry or returns 504 (Gateway Timeout). Revalidating is no-cache/ max-age=0, and accepting stale up to N seconds is max-stale=N.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#request_directives)

**Q12.** Which header lets you inspect whether the reverse proxy served a cache hit?  <small>_(easy · single)_</small>

- A. X-Symfony-Cache
- B. X-Cache-Status
- C. X-Debug-Cache
- D. Age (must be 0)

??? success "Answer Q12"
    **A**

    HttpCache writes a trace to the trace_header (default X-Symfony-Cache), e.g. "GET /: fresh", "miss", or "store". Age reports elapsed seconds, not hit/miss, and the other header names are invented.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q13.** What is the simplest way to enable the reverse proxy in Symfony 8?  <small>_(easy · config)_</small>

- A. Set framework.http_cache: true in configuration
- B. Register a compiler pass
- C. Install Varnish
- D. Add #[AsHttpCache] to the Kernel

??? success "Answer Q13"
    **A**

    framework.http_cache: true wraps the kernel automatically. The alternative is wrapping it manually in public/index.php with the FrameworkBundle HttpCache subclass. There is no compiler pass or #[AsHttpCache] attribute, and Varnish is a separate external proxy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy)

**Q14.** What is the primary benefit of ESI over full-page caching?  <small>_(easy · single)_</small>

- A. Each fragment can be cached with its own independent lifetime
- B. It encrypts fragments end to end
- C. It removes the need for any reverse proxy
- D. It compresses the HTML automatically

??? success "Answer Q14"
    **A**

    ESI caches fragments as separate entries, so a long-lived shell can coexist with short-lived or per-user fragments on one page. It provides no encryption or compression, and it actually requires a surrogate (reverse proxy) to work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

**Q15.** Which component processes <esi:include> tags?  <small>_(easy · single)_</small>

- A. The reverse proxy / surrogate (Symfony HttpCache or Varnish)
- B. The Twig compiler
- C. The PHP engine at render time
- D. The browser

??? success "Answer Q15"
    **A**

    ESI is a surrogate feature; the gateway cache fetches each include as a sub-request and stitches the results, caching each on its own terms. Twig/PHP only emit the tag, and the browser never sees or resolves it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/Esi.php)

**Q16.** What is the near-identical alternative to ESI for servers like nginx or Varnish that speak Server Side Includes?  <small>_(easy · single)_</small>

- A. SSI, via render_ssi(), the Ssi surrogate and framework.ssi
- B. AJAX with hinclude, via render_hinclude()
- C. Server push, via framework.http2
- D. PSR-6 tag-based invalidation

??? success "Answer Q16"
    **A**

    SSI is the sibling of ESI: same mixed-freshness idea, exposed through render_ssi(), the Ssi surrogate class and framework.ssi. hinclude is a pure client-side AJAX approach (no caching goal), and the others are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

**Q17.** Which Cache-Control value does a Symfony Response emit when you set no caching information at all?  <small>_(medium · internals)_</small>

- A. no-cache, private
- B. public, max-age=0
- C. no-store
- D. (no Cache-Control header)

??? success "Answer Q17"
    **A**

    ResponseHeaderBag::computeCacheControlValue() defaults to "no-cache, private" when nothing is configured. It is safe (shared caches will not store it) but gives no caching benefit — you must opt in with public/max-age. It is not "no-store" (that forbids storage entirely) nor an empty header (Symfony always renders a value).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q18.** You call $response->setPublic() and then $response->setPrivate(). What is emitted?  <small>_(medium · trap)_</small>

- A. Cache-Control: private (public is removed)
- B. Cache-Control: public, private
- C. Cache-Control: public
- D. An InvalidArgumentException is thrown

??? success "Answer Q18"
    **A**

    public and private are mutually exclusive; setPrivate() removes the public flag, so the later call wins. You can never emit "public, private", and no exception is thrown — the header bag simply keeps the last intent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q19.** Given #[Cache(public: true, maxage: 3600, vary: ['Accept-Language', 'Accept-Encoding'])] on an action, which raw headers result?  <small>_(medium · config)_</small>

- A. Cache-Control: public, max-age=3600 and Vary: Accept-Language, Accept-Encoding
- B. Cache-Control: private, s-maxage=3600 and Vary: *
- C. Cache-Control: public, s-maxage=3600 only (Vary is ignored by the attribute)
- D. Only Vary is set; maxage on the attribute is dev-only

??? success "Answer Q19"
    **A**

    maxage maps to max-age (all caches), public opts into shared caching, and vary is emitted verbatim as a comma-separated Vary header. maxage is not s-maxage (that is the smaxage option), the response stays public not private, and the attribute fully supports vary.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#the-cache-attribute)

**Q20.** Why is Vary: Cookie on a shared-cacheable response almost always a mistake? (choose 2)  <small>_(medium · trap)_</small>

- A. Each distinct cookie value becomes its own cache entry, so session cookies yield near-zero shared hits
- B. It explodes the cache key space, defeating the purpose of a shared cache
- C. It causes the reverse proxy to throw an InvalidArgumentException
- D. It automatically strips the Set-Cookie header

??? success "Answer Q20"
    **A, B**

    Vary:Cookie adds the cookie value to the cache key; with per-user session cookies almost every request is unique, so the shared cache stores one entry per user and reuses nothing. It neither throws nor strips Set-Cookie. The right fix is to keep the shell public and isolate the per-user part with ESI.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

**Q21.** Besides setting s-maxage, what side effect does $response->setSharedMaxAge(600) have?  <small>_(medium · internals)_</small>

- A. It marks the response public
- B. It also sets max-age=600 for the browser
- C. It adds a must-revalidate directive
- D. It sets an Expires header

??? success "Answer Q21"
    **A**

    A shared TTL is meaningless on a private response, so setSharedMaxAge() sets the public flag as well. It does not touch max-age (browsers still have no freshness), adds no must-revalidate, and sets no Expires.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q22.** For a shared cache, which freshness source takes precedence?  <small>_(medium · single)_</small>

- A. s-maxage, then max-age, then Expires
- B. Expires over everything else
- C. max-age over s-maxage
- D. Whichever header appears first

??? success "Answer Q22"
    **A**

    Shared caches resolve freshness as s-maxage > max-age > Expires. A private cache starts at max-age since it ignores s-maxage. Expires is the lowest-priority HTTP/1.0 fallback, and header order is irrelevant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/expiration.html)

**Q23.** Which #[Cache] options accept a relative date string like '1 hour' as well as an integer?  <small>_(medium · internals)_</small>

- A. maxage, smaxage, staleWhileRevalidate, staleIfError
- B. public and private
- C. Only expires
- D. None — all durations must be integers

??? success "Answer Q23"
    **A**

    Those numeric-duration options accept an int (seconds) or a relative date string parsed via DateTimeImmutable. expires is a date string (an absolute moment), while public/private are booleans, not durations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#the-cache-attribute)

**Q24.** What does Cache-Control: stale-while-revalidate=30 let a cache do?  <small>_(medium · single)_</small>

- A. Serve the stale response for up to 30 s while it revalidates in the background
- B. Extend the fresh lifetime by 30 s
- C. Serve stale for 30 s only if the origin returns an error
- D. Force revalidation every 30 s regardless of freshness

??? success "Answer Q24"
    **A**

    stale-while-revalidate lets a cache immediately answer with a stale copy while it refreshes asynchronously, hiding origin latency. Serving stale only on origin errors is stale-if-error; it does not extend freshness nor schedule periodic revalidation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/expiration.html)

**Q25.** When Response::isNotModified() returns true, what has it done to the response?  <small>_(medium · internals)_</small>

- A. Set the status to 304 and removed the body and content headers
- B. Nothing — it only returns a boolean
- C. Thrown a NotModifiedHttpException
- D. Sent the response to the client immediately

??? success "Answer Q25"
    **A**

    isNotModified() mutates the response in place (status 304, strips the body and content-related headers like Content-Type/Length) and returns a bool. It never throws or sends the response — you still return it yourself. Assuming it is pure (returns bool only) is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/validation.html)

**Q26.** How do you produce a weak ETag with the Response API?  <small>_(medium · trap)_</small>

- A. $response->setEtag('abc', weak: true)
- B. $response->setWeakEtag('abc')
- C. $response->setEtag('W/abc')
- D. $response->setCache(['weak_etag' => 'abc'])

??? success "Answer Q26"
    **A**

    The second boolean argument to setEtag() prefixes the value with W/. There is no setWeakEtag() method and no weak_etag setCache key; passing 'W/abc' yourself would double the prefix. Conditional GET uses weak comparison regardless of which form you emit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/validation.html)

**Q27.** A developer sets $response->setLastModified(new \DateTimeImmutable()) but 304s never happen. Why?  <small>_(medium · debug)_</small>

- A. The validator is the current time, so it never equals the client's If-Modified-Since value
- B. setLastModified() requires a string, not a DateTimeImmutable
- C. Last-Modified is ignored unless an ETag is also set
- D. DateTimeImmutable is not supported; only DateTime works

??? success "Answer Q27"
    **A**

    Using now() as the validator means every response looks freshly modified, so If-Modified-Since can never match and you always get 200. Use the resource's real modification time (e.g. an entity's updatedAt). setLastModified() accepts any \\DateTimeInterface (immutable included), and Last-Modified works without an ETag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/validation.html)

**Q28.** A normal browser reload (not hard reload) typically sends which request directive?  <small>_(medium · trap)_</small>

- A. Cache-Control: max-age=0 (revalidate)
- B. Cache-Control: no-store
- C. Cache-Control: only-if-cached
- D. No Cache-Control header

??? success "Answer Q28"
    **A**

    A reload asks caches to revalidate via max-age=0 (a 304 is possible), whereas a hard reload sends no-cache to force a full refetch. no-store and only-if-cached are unrelated to reload behaviour. Confusing reload with hard reload is a common exam trap.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#request_directives)

**Q29.** What is the recommended header combination for a fingerprinted (content-hashed) asset?  <small>_(medium · single)_</small>

- A. public, max-age=31536000, immutable
- B. private, no-store
- C. no-cache, must-revalidate
- D. s-maxage=31536000 only

??? success "Answer Q29"
    **A**

    A fingerprinted URL never changes content, so cache it long-term in every cache and skip revalidation with immutable. A new build yields a new URL. no-store/no-cache would defeat caching, and s-maxage alone would leave the browser uncached.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

**Q30.** To detect whether a client forced a revalidation, which reads the request's Cache-Control correctly?  <small>_(medium · code)_</small>

- A. $request->headers->hasCacheControlDirective('no-cache') || '0' === $request->headers->getCacheControlDirective('max-age')
- B. $request->isNoCache()
- C. $request->getCacheControl() === 'no-cache'
- D. $request->headers->get('Cache-Control')->noCache

??? success "Answer Q30"
    **A**

    HeaderBag exposes hasCacheControlDirective()/getCacheControlDirective() on request headers; the directive value is a string, so max-age is compared to '0'. There is no Request::isNoCache() or getCacheControl(), and get('Cache-Control') returns a plain string, not an object.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#request_directives)

**Q31.** What does the immutable directive buy for a fresh, fingerprinted asset in the browser?  <small>_(medium · trap)_</small>

- A. The browser skips revalidation while the response is still fresh, even on a normal reload
- B. The asset is cached forever regardless of max-age
- C. Shared caches refuse to store it
- D. It forces the connection to HTTPS

??? success "Answer Q31"
    **A**

    immutable tells the browser the body will not change during its freshness window, so even F5 (which normally sends max-age=0) will not revalidate. It does not extend caching beyond max-age, does not block shared caches, and has nothing to do with TLS.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

**Q32.** What is Symfony\Component\HttpKernel\HttpCache\HttpCache?  <small>_(medium · single)_</small>

- A. A reverse-proxy kernel that wraps your application kernel
- B. A PSR-6 cache pool
- C. A Twig extension for cache tags
- D. A compiler pass that caches the container

??? success "Answer Q32"
    **A**

    HttpCache implements HttpKernelInterface and TerminableInterface and wraps the real kernel, acting as an in-PHP shared gateway cache. It is not a PSR-6 pool, a Twig extension, or a compiler pass.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy)

**Q33.** By default, which request header makes the Symfony reverse proxy treat a request as private?  <small>_(medium · internals)_</small>

- A. Cookie (and Authorization)
- B. Accept
- C. User-Agent
- D. Referer

??? success "Answer Q33"
    **A**

    The private_headers option defaults to Authorization and Cookie; requests carrying them skip the shared cache, protecting authenticated responses. Accept/User-Agent/Referer have no such role by default.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php)

**Q34.** A visitor sends Cache-Control: no-cache to force a reload through the Symfony reverse proxy. What happens by default?  <small>_(medium · trap)_</small>

- A. It is ignored — allow_reload defaults to false, so the client cannot force a bypass
- B. The proxy always refetches from the backend on no-cache
- C. The proxy throws an error for unauthorized reload
- D. The cached entry is deleted

??? success "Answer Q34"
    **A**

    allow_reload (client no-cache) and allow_revalidate (client max-age=0) both default to false, because letting any client force a bypass invites abuse. So a hard reload does not blow past the shared cache unless you opt in. Nothing is deleted and no error is raised.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php)

**Q35.** The default HttpCache Store is a distributed store shared across servers out of the box.  <small>_(medium · true-false)_</small>

- A. True
- B. False

??? success "Answer Q35"
    **B**

    False. The default Store (Symfony\\Component\\HttpKernel\\HttpCache\\Store) is a filesystem store keyed by URL + Vary, using digest and lock files. There is no built-in distributed/shared store — that is a reason to use Varnish or a CDN at scale.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/Store.php)

**Q36.** When does the render_esi Twig function actually emit an <esi:include> tag?  <small>_(medium · trap)_</small>

- A. Only when a surrogate advertises ESI capability; otherwise it renders the fragment inline
- B. Always, in every environment
- C. Only in the dev environment
- D. Only for JSON responses

??? success "Answer Q36"
    **A**

    The ESI renderer checks the Surrogate-Capability header. Without a surrogate it falls back to inline rendering so the same template works everywhere. It is not always-on, not dev-only, and not tied to content type.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

**Q37.** Why does Symfony sign _fragment URIs (UriSigner)?  <small>_(medium · internals)_</small>

- A. To prevent attackers forging arbitrary fragment requests
- B. To compress the URI
- C. To enable HTTP/2 server push
- D. To compute the response ETag

??? success "Answer Q37"
    **A**

    Fragment URIs are signed with the application secret (via UriSigner) so only legitimately generated fragment calls are honoured by the kernel. Signing is a security measure, not compression, push, or ETag computation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

**Q38.** What is the minimal config to make render_esi emit real ESI tags that get processed?  <small>_(medium · config)_</small>

- A. framework.esi: true AND a running surrogate (framework.http_cache: true or Varnish)
- B. framework.esi: true alone is enough
- C. framework.http_cache: true alone is enough
- D. Nothing — ESI is on by default in Symfony 8

??? success "Answer Q38"
    **A**

    You need ESI enabled (framework.esi: true) AND a surrogate to advertise the capability and process the includes — the Symfony reverse proxy (framework.http_cache: true) or Varnish. Enabling only one of them means render_esi falls back to inline rendering; ESI is not on by default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

**Q39.** Which Twig call embeds a controller as an ESI fragment?  <small>_(medium · code)_</small>

- A. {{ render_esi(controller('App\\Controller\\FragmentController::userGreeting')) }}
- B. {{ esi('App\\Controller\\FragmentController::userGreeting') }}
- C. {{ include_esi('user-greeting') }}
- D. {{ render('esi:App\\Controller\\FragmentController::userGreeting') }}

??? success "Answer Q39"
    **A**

    render_esi() wraps a controller() reference and delegates to the fragment handler, which emits <esi:include> when a surrogate is present (else inline). There is no esi(), include_esi(), or 'esi:' render prefix in Twig — the pair is render()/render_esi()/render_ssi().

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

**Q40.** You set framework.esi: true but run no reverse proxy. A page uses render_esi for a fragment. What happens?  <small>_(medium · debug)_</small>

- A. The fragment renders inline on every request — no separate caching, no benefit, but the page still works
- B. An exception is thrown because no surrogate is configured
- C. The <esi:include> tag is sent raw to the browser
- D. The whole page becomes uncacheable

??? success "Answer Q40"
    **A**

    With no surrogate advertising ESI capability, render_esi silently falls back to inline rendering, so the fragment is embedded and re-rendered each request — correct output, but none of the per-fragment caching benefit. No exception is thrown and no raw <esi:include> reaches the browser (that only happens if a broken proxy fails to process it).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

**Q41.** A page is marked public with s-maxage=60 but still calls $request->getSession() and reads a cookie. What is the risk behind a CDN?  <small>_(hard · scenario)_</small>

- A. The CDN may store one user's personalized page and serve it to other users
- B. Nothing — sessions automatically add Vary: Cookie
- C. The response is silently downgraded to private by Symfony
- D. The CDN refuses to cache any response that touched the session

??? success "Answer Q41"
    **A**

    A public response with a shared TTL is storable by any shared cache regardless of the session it read; the CDN can leak one user's page to another. Symfony does not auto-add Vary:Cookie nor auto-downgrade to private. The Symfony reverse proxy protects you only because its private_headers default includes Cookie — a generic CDN does not. Keep such pages private/uncached or pull the personal part via ESI.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q42.** How do you emit a must-revalidate directive from a Response object?  <small>_(hard · trap)_</small>

- A. $response->setCache(['must_revalidate' => true])
- B. $response->setMustRevalidate()
- C. $response->mustRevalidate(true)
- D. It is added automatically by no-cache

??? success "Answer Q42"
    **A**

    There is no dedicated setter; Response::mustRevalidate() is a getter returning bool (calling it with an argument is a type error, and it never mutates state). Use setCache(['must_revalidate' => true]) or #[Cache(mustRevalidate: true)]. no-cache does not imply must-revalidate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

**Q43.** What happens when you call $response->setCache(['s_maxage' => 300, 'foo' => true])?  <small>_(hard · code)_</small>

- A. An InvalidArgumentException is thrown because 'foo' is not an allowed key
- B. s-maxage=300 is set and 'foo' is silently ignored
- C. A custom header Foo: true is added
- D. A deprecation is triggered but the call succeeds

??? success "Answer Q43"
    **A**

    setCache() validates its keys against a fixed whitelist (etag, last_modified, max_age, s_maxage, public, private, immutable, must_revalidate, no_cache, no_store, no_transform, proxy_revalidate, stale_while_revalidate, stale_if_error). An unknown key throws InvalidArgumentException immediately — nothing is set and no header is added. This is unlike setting a raw stray header string.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q44.** A controller explicitly calls $response->setMaxAge(0) and the action also has #[Cache(maxage: 3600)]. Which wins, and why?  <small>_(hard · internals)_</small>

- A. max-age=0 wins — CacheAttributeListener runs late on RESPONSE (prio -10) and does not override headers already set explicitly
- B. max-age=3600 wins — the attribute always overrides controller code
- C. An exception is thrown for the conflict
- D. Both are emitted as max-age=0, max-age=3600

??? success "Answer Q44"
    **A**

    CacheAttributeListener applies expiration directives on KernelEvents::RESPONSE at priority -10 (late) but only fills in values the controller has not already set, so an explicit setMaxAge(0) stays. The attribute never blindly overrides, never throws for this, and Cache-Control cannot carry two max-age values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/CacheAttributeListener.php)

**Q45.** Using #[Cache(etag: 'post.getContent()')], what value is actually sent as the ETag?  <small>_(hard · internals)_</small>

- A. The SHA-256 hash of the evaluated expression
- B. The literal string 'post.getContent()'
- C. The raw return value of getContent()
- D. A weak ETag of the whole rendered body

??? success "Answer Q45"
    **A**

    CacheAttributeListener evaluates the expression on kernel.controller_arguments and SHA-256-hashes the result before using it as the ETag, so it can point at large content safely. The string is an expression (not a literal), and the raw value is never sent verbatim.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#the-cache-attribute)

**Q46.** With #[Cache(lastModified: 'post.getUpdatedAt()')], when can a 304 be returned?  <small>_(hard · internals)_</small>

- A. Before the controller body runs, during kernel.controller_arguments
- B. Only after the controller has fully rendered the response
- C. Only inside a kernel.terminate listener
- D. Never — expressions cannot short-circuit

??? success "Answer Q46"
    **A**

    CacheAttributeListener evaluates the expression on CONTROLLER_ARGUMENTS (priority 10) and, if the request is up to date, replaces the controller so a 304 is returned without running the body. That is precisely the CPU/render saving the model exists for; it does not wait for RESPONSE or terminate.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/CacheAttributeListener.php)

**Q47.** Consider: $response->setEtag(sha1($post->getContent())); if ($response->isNotModified($request)) { return $response; } return $this->render('post.html.twig', ['post' => $post], $response); — what is the benefit when If-None-Match matches?  <small>_(hard · code)_</small>

- A. A bodyless 304 is returned and the template is never rendered
- B. The template is rendered, then discarded, and a 304 is sent
- C. A 200 with the full body is always returned
- D. The response is sent twice

??? success "Answer Q47"
    **A**

    isNotModified() sets 304 and strips the body when the ETag matches, and the early return short-circuits before render() runs — so no template work happens at all. If you called render() first you would lose that saving. It never sends twice; you return the response once.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/validation.html)

**Q48.** A user says 'I reloaded but still see the old CSS.' What is the cache-level cause and the real fix?  <small>_(hard · debug)_</small>

- A. A normal reload only revalidates (max-age=0); a 304 keeps the old bytes. Fix by serving the CSS under a content-hashed URL
- B. The browser cache is corrupt; the fix is to disable caching entirely
- C. s-maxage is too high; lower it so the browser refreshes
- D. The server must send no-store on every asset

??? success "Answer Q48"
    **A**

    A normal reload sends max-age=0, so the browser revalidates; an unchanged ETag/Last-Modified yields 304 and the stale bytes stay. A hard reload (no-cache) would refetch, but the durable fix is cache busting via a new (fingerprinted) URL. s-maxage is ignored by the browser, and no-store throws away all caching benefit.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)

**Q49.** Which interfaces does HttpCache implement, and what is its constructor shape?  <small>_(hard · internals)_</small>

- A. HttpKernelInterface and TerminableInterface; __construct(HttpKernelInterface $kernel, StoreInterface $store, ?SurrogateInterface $surrogate = null, array $options = [])
- B. Only HttpKernelInterface; __construct(StoreInterface $store)
- C. CacheItemPoolInterface (PSR-6); __construct(array $config)
- D. EventSubscriberInterface; __construct(EventDispatcherInterface $dispatcher)

??? success "Answer Q49"
    **A**

    HttpCache is both an HttpKernelInterface (so it can handle requests) and TerminableInterface (so terminate() propagates). Its constructor takes the wrapped kernel, a StoreInterface, an optional SurrogateInterface (Esi/Ssi) and an options array. It is not a PSR-6 pool nor an event subscriber.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php)

**Q50.** What does this config do? framework: { http_cache: { enabled: true, trace_header: X-Symfony-Cache, default_ttl: 0 } }  <small>_(hard · config)_</small>

- A. Wraps the kernel with HttpCache, sets the trace header name, and applies no default freshness when a response gives none
- B. Disables caching because default_ttl is 0
- C. Forces a 0-second TTL on every response regardless of its headers
- D. Only renames the trace header without enabling caching

??? success "Answer Q50"
    **A**

    enabled: true wraps the kernel; trace_header sets the debug header name; default_ttl is the TTL used ONLY when a response carries no freshness info — 0 means such responses are not cached by default, but responses that do set s-maxage/max-age are still cached normally. It does not override explicit freshness nor disable caching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy)

**Q51.** A page sets s-maxage=60 but logged-in users never get a shared-cache hit from HttpCache. Why, and how do you still cache the anonymous view?  <small>_(hard · scenario)_</small>

- A. Their session Cookie is in private_headers, so the request is treated as private; move per-user parts into ESI so the shell stays anonymous/cacheable
- B. s-maxage is too low; raising it will cache logged-in requests
- C. HttpCache never caches HTML, only assets
- D. The response must be marked private to be cached

??? success "Answer Q51"
    **A**

    Logged-in requests carry a session Cookie, which is in the default private_headers, so HttpCache treats them as private and neither serves from nor stores in the shared cache. Anonymous requests are cached. Raising s-maxage changes nothing, HttpCache caches any cacheable response, and private means no shared caching at all — instead isolate per-user bits with ESI fragments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html#symfony-reverse-proxy)

**Q52.** Without ESI, adding a #[Cache(smaxage: 5)] fragment to an s-maxage=3600 page collapses the whole page to a 5-second TTL. Which mechanism causes this?  <small>_(hard · internals)_</small>

- A. ResponseCacheStrategy reduces the master TTL to the minimum of all embedded (inline) fragment TTLs
- B. The #[Cache] attribute overrides the parent controller's headers
- C. The kernel discards s-maxage whenever a sub-request runs
- D. Twig strips Cache-Control from embedded responses

??? success "Answer Q52"
    **A**

    When a fragment is rendered inline into the master response, ResponseCacheStrategy merges freshness by taking the MINIMUM TTL, so the 5-second fragment caps the page. ESI avoids this by caching the fragment as a separate entry, leaving the shell's long TTL intact. It is not an attribute override, a kernel discard, or Twig stripping headers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/esi.html)

---

<small>Back to [Chapter Exams](index.md) · [HTTP Caching](../http-caching/index.md)</small>
