# Flashcards — HTTP Caching

58 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

## 🧠 Pour les nuls

**C'est quoi ?** Un jeu de **52 flashcards** (question au recto, réponse au verso) sur HTTP Caching. On lit la question, on répond mentalement, puis on tape pour révéler la réponse.

**Pourquoi ça existe ?** Se tester activement (essayer de répondre avant de voir la réponse) ancre l'information bien mieux que relire passivement un chapitre. Répété à intervalles espacés, c'est la technique de mémorisation la plus efficace connue.

**🏠 Analogie de la vraie vie :** Ce sont les **cartes-vocabulaire** utilisées pour apprendre une langue étrangère : un mot d'un côté, sa traduction de l'autre — on ne progresse qu'en essayant de deviner avant de retourner la carte.

**Symfony dans la vraie vie :** Recto de la carte → une question précise sur HTTP Caching / Verso → la réponse avec sa justification et un lien vers la doc officielle / Cartes marquées "ratées" → à revoir en priorité au prochain passage.

**⚠️ Erreur fréquente :** Taper pour révéler la réponse trop vite, sans avoir vraiment tenté de répondre — cela transforme l'exercice en simple lecture, avec un gain de mémorisation presque nul.

**🧠 Comment le mémoriser :** *« Je réponds avant de retourner la carte »* — et je note les cartes ratées pour les revoir plus souvent que les autres (répétition espacée).

??? question "1. Which Cache-Control value does a Symfony Response emit when you set no caching information at all?"
    **✅ no-cache, private**

    ResponseHeaderBag::computeCacheControlValue() defaults to "no-cache, private" when nothing is configured. It is safe (shared caches will not store it) but gives no caching benefit — you must opt in with public/max-age. It is not "no-store" (that forbids storage entirely) nor an empty header (Symfony always renders a value).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "2. Which caches honour the s-maxage directive?"
    **✅ Shared caches only (proxies and the reverse proxy)**

    s-maxage sets freshness for shared caches. Browsers (private caches) ignore it and fall back to max-age / Expires. It is a response directive, not a request one, and every cache honouring it would be max-age, not s-maxage.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

??? question "3. You call $response->setPublic() and then $response->setPrivate(). What is emitted?"
    **✅ Cache-Control: private (public is removed)**

    public and private are mutually exclusive; setPrivate() removes the public flag, so the later call wins. You can never emit "public, private", and no exception is thrown — the header bag simply keeps the last intent.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "4. What does the response header 'Vary: Accept-Language' instruct a cache to do?"
    **✅ Store a separate copy keyed by each distinct Accept-Language value**

    Vary adds the named request header(s) to the cache key, so each variant is stored and served independently. It never rejects requests or translates content. Vary:* or Vary:Cookie effectively disables shared caching by exploding the key space.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

??? question "5. Given #[Cache(public: true, maxage: 3600, vary: ['Accept-Language', 'Accept-Encoding'])] on an action, which raw headers result?"
    **✅ Cache-Control: public, max-age=3600 and Vary: Accept-Language, Accept-Encoding**

    maxage maps to max-age (all caches), public opts into shared caching, and vary is emitted verbatim as a comma-separated Vary header. maxage is not s-maxage (that is the smaxage option), the response stays public not private, and the attribute fully supports vary.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#the-cache-attribute)

??? question "6. Why is Vary: Cookie on a shared-cacheable response almost always a mistake? (choose 2)"
    **✅ Each distinct cookie value becomes its own cache entry, so session cookies yield near-zero shared hits ; It explodes the cache key space, defeating the purpose of a shared cache**

    Vary:Cookie adds the cookie value to the cache key; with per-user session cookies almost every request is unique, so the shared cache stores one entry per user and reuses nothing. It neither throws nor strips Set-Cookie. The right fix is to keep the shell public and isolate the per-user part with ESI.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

??? question "7. A reverse proxy (gateway cache) such as Symfony HttpCache or Varnish is a shared cache."
    **✅ True**

    A reverse proxy / gateway cache serves many users, so it is a shared cache you own and deploy in front of the app — it therefore honours s-maxage. Only the browser is a private cache.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "8. A page is marked public with s-maxage=60 but still calls $request->getSession() and reads a cookie. What is the risk behind a CDN?"
    **✅ The CDN may store one user's personalized page and serve it to other users**

    A public response with a shared TTL is storable by any shared cache regardless of the session it read; the CDN can leak one user's page to another. Symfony does not auto-add Vary:Cookie nor auto-downgrade to private. The Symfony reverse proxy protects you only because its private_headers default includes Cookie — a generic CDN does not. Keep such pages private/uncached or pull the personal part via ESI.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "9. What does the Cache-Control directive 'no-cache' mean?"
    **✅ The response may be stored but must be revalidated before every reuse**

    no-cache permits storage but forces revalidation on each reuse. The directive that forbids storing at all is no-store. It says nothing about freshness duration or private/shared scope.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

??? question "10. Besides setting s-maxage, what side effect does $response->setSharedMaxAge(600) have?"
    **✅ It marks the response public**

    A shared TTL is meaningless on a private response, so setSharedMaxAge() sets the public flag as well. It does not touch max-age (browsers still have no freshness), adds no must-revalidate, and sets no Expires.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "11. For a shared cache, which freshness source takes precedence?"
    **✅ s-maxage, then max-age, then Expires**

    Shared caches resolve freshness as s-maxage > max-age > Expires. A private cache starts at max-age since it ignores s-maxage. Expires is the lowest-priority HTTP/1.0 fallback, and header order is irrelevant.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

??? question "12. How do you emit a must-revalidate directive from a Response object?"
    **✅ $response->setCache(['must_revalidate' => true])**

    There is no dedicated setter; Response::mustRevalidate() is a getter returning bool (calling it with an argument is a type error, and it never mutates state). Use setCache(['must_revalidate' => true]) or #[Cache(mustRevalidate: true)]. no-cache does not imply must-revalidate.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "13. Which #[Cache] options accept a relative date string like '1 hour' as well as an integer?"
    **✅ maxage, smaxage, staleWhileRevalidate, staleIfError**

    Those numeric-duration options accept an int (seconds) or a relative date string parsed via DateTimeImmutable. expires is a date string (an absolute moment), while public/private are booleans, not durations.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#the-cache-attribute)

??? question "14. What happens when you call $response->setCache(['s_maxage' => 300, 'foo' => true])?"
    **✅ An InvalidArgumentException is thrown because 'foo' is not an allowed key**

    setCache() validates its keys against a fixed whitelist (etag, last_modified, max_age, s_maxage, public, private, immutable, must_revalidate, no_cache, no_store, no_transform, proxy_revalidate, stale_while_revalidate, stale_if_error). An unknown key throws InvalidArgumentException immediately — nothing is set and no header is added. This is unlike setting a raw stray header string.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "15. A controller explicitly calls $response->setMaxAge(0) and the action also has #[Cache(maxage: 3600)]. Which wins, and why?"
    **✅ max-age=0 wins — CacheAttributeListener runs late on RESPONSE (prio -10) and does not override headers already set explicitly**

    CacheAttributeListener applies expiration directives on KernelEvents::RESPONSE at priority -10 (late) but only fills in values the controller has not already set, so an explicit setMaxAge(0) stays. The attribute never blindly overrides, never throws for this, and Cache-Control cannot carry two max-age values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/CacheAttributeListener.php)

??? question "16. Cache-Control: no-cache tells caches never to store the response."
    **✅ False**

    False. no-cache permits storing but requires revalidation before every reuse. The directive that forbids storage entirely is no-store — the single most common Cache-Control misconception.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

??? question "17. What does Cache-Control: stale-while-revalidate=30 let a cache do?"
    **✅ Serve the stale response for up to 30 s while it revalidates in the background**

    stale-while-revalidate lets a cache immediately answer with a stale copy while it refreshes asynchronously, hiding origin latency. Serving stale only on origin errors is stale-if-error; it does not extend freshness nor schedule periodic revalidation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

??? question "18. When Response::isNotModified() returns true, what has it done to the response?"
    **✅ Set the status to 304 and removed the body and content headers**

    isNotModified() mutates the response in place (status 304, strips the body and content-related headers like Content-Type/Length) and returns a bool. It never throws or sends the response — you still return it yourself. Assuming it is pure (returns bool only) is the classic trap.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/validation.html)

??? question "19. A request carries both If-None-Match and If-Modified-Since. Which one decides the 304?"
    **✅ The ETag (If-None-Match) takes precedence**

    When an ETag is supplied it governs the comparison; Last-Modified alone only decides when no ETag is present. The two are not compared by magnitude, and a 200 is not forced.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "20. Using #[Cache(etag: 'post.getContent()')], what value is actually sent as the ETag?"
    **✅ The SHA-256 hash of the evaluated expression**

    CacheAttributeListener evaluates the expression on kernel.controller_arguments and SHA-256-hashes the result before using it as the ETag, so it can point at large content safely. The string is an expression (not a literal), and the raw value is never sent verbatim.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#the-cache-attribute)

??? question "21. How do you produce a weak ETag with the Response API?"
    **✅ $response->setEtag('abc', weak: true)**

    The second boolean argument to setEtag() prefixes the value with W/. There is no setWeakEtag() method and no weak_etag setCache key; passing 'W/abc' yourself would double the prefix. Conditional GET uses weak comparison regardless of which form you emit.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/validation.html)

??? question "22. With #[Cache(lastModified: 'post.getUpdatedAt()')], when can a 304 be returned?"
    **✅ Before the controller body runs, during kernel.controller_arguments**

    CacheAttributeListener evaluates the expression on CONTROLLER_ARGUMENTS (priority 10) and, if the request is up to date, replaces the controller so a 304 is returned without running the body. That is precisely the CPU/render saving the model exists for; it does not wait for RESPONSE or terminate.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/CacheAttributeListener.php)

??? question "23. Consider: $response->setEtag(sha1($post->getContent())); if ($response->isNotModified($request)) { return $response; } return $this->render('post.html.twig', ['post' => $post], $response); — what is the benefit when If-None-Match matches?"
    **✅ A bodyless 304 is returned and the template is never rendered**

    isNotModified() sets 304 and strips the body when the ETag matches, and the early return short-circuits before render() runs — so no template work happens at all. If you called render() first you would lose that saving. It never sends twice; you return the response once.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/validation.html)

??? question "24. A developer sets $response->setLastModified(new \DateTimeImmutable()) but 304s never happen. Why?"
    **✅ The validator is the current time, so it never equals the client's If-Modified-Since value**

    Using now() as the validator means every response looks freshly modified, so If-Modified-Since can never match and you always get 200. Use the resource's real modification time (e.g. an entity's updatedAt). setLastModified() accepts any \\DateTimeInterface (immutable included), and Last-Modified works without an ETag.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/validation.html)

??? question "25. A 304 Not Modified response must be sent without a message body."
    **✅ True**

    True. A 304 carries no message body — the client already holds the bytes. Symfony enforces this: isNotModified() strips the body and content headers when it sets the 304 status.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests)

??? question "26. Which conditional request header does a client send to revalidate an ETag?"
    **✅ If-None-Match**

    ETags round-trip via If-None-Match for a conditional GET. If-Modified-Since pairs with Last-Modified (a date), while If-Match and If-Range serve write concurrency and range requests, not cache revalidation of a GET.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests)

??? question "27. Which directive does a browser ignore when managing its own private cache?"
    **✅ s-maxage**

    The browser is a private cache; it honours max-age/Expires, no-store and immutable, but ignores s-maxage, which targets shared caches only.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)

??? question "28. A normal browser reload (not hard reload) typically sends which request directive?"
    **✅ Cache-Control: max-age=0 (revalidate)**

    A reload asks caches to revalidate via max-age=0 (a 304 is possible), whereas a hard reload sends no-cache to force a full refetch. no-store and only-if-cached are unrelated to reload behaviour. Confusing reload with hard reload is a common exam trap.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#request_directives)

??? question "29. What is the recommended header combination for a fingerprinted (content-hashed) asset?"
    **✅ public, max-age=31536000, immutable**

    A fingerprinted URL never changes content, so cache it long-term in every cache and skip revalidation with immutable. A new build yields a new URL. no-store/no-cache would defeat caching, and s-maxage alone would leave the browser uncached.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

??? question "30. Which request is eligible to be served from the browser cache?"
    **✅ GET /page**

    Only safe methods (GET, HEAD) are cacheable; unsafe methods (POST, PUT, PATCH, DELETE) always hit the origin and may invalidate cached entries for the target URL.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

??? question "31. To detect whether a client forced a revalidation, which reads the request's Cache-Control correctly?"
    **✅ $request->headers->hasCacheControlDirective('no-cache') || '0' === $request->headers->getCacheControlDirective('max-age')**

    HeaderBag exposes hasCacheControlDirective()/getCacheControlDirective() on request headers; the directive value is a string, so max-age is compared to '0'. There is no Request::isNoCache() or getCacheControl(), and get('Cache-Control') returns a plain string, not an object.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#request_directives)

??? question "32. What does the immutable directive buy for a fresh, fingerprinted asset in the browser?"
    **✅ The browser skips revalidation while the response is still fresh, even on a normal reload**

    immutable tells the browser the body will not change during its freshness window, so even F5 (which normally sends max-age=0) will not revalidate. It does not extend caching beyond max-age, does not block shared caches, and has nothing to do with TLS.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

??? question "33. A user says 'I reloaded but still see the old CSS.' What is the cache-level cause and the real fix?"
    **✅ A normal reload only revalidates (max-age=0); a 304 keeps the old bytes. Fix by serving the CSS under a content-hashed URL**

    A normal reload sends max-age=0, so the browser revalidates; an unchanged ETag/Last-Modified yields 304 and the stale bytes stay. A hard reload (no-cache) would refetch, but the durable fix is cache busting via a new (fingerprinted) URL. s-maxage is ignored by the browser, and no-store throws away all caching benefit.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)

??? question "34. What does the request directive Cache-Control: only-if-cached ask a cache to do?"
    **✅ Return a cached copy if available, otherwise respond 504 without contacting the origin**

    only-if-cached forbids any origin request: the cache serves a stored entry or returns 504 (Gateway Timeout). Revalidating is no-cache/ max-age=0, and accepting stale up to N seconds is max-stale=N.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#request_directives)

??? question "35. What is Symfony\Component\HttpKernel\HttpCache\HttpCache?"
    **✅ A reverse-proxy kernel that wraps your application kernel**

    HttpCache implements HttpKernelInterface and TerminableInterface and wraps the real kernel, acting as an in-PHP shared gateway cache. It is not a PSR-6 pool, a Twig extension, or a compiler pass.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#symfony-reverse-proxy)

??? question "36. By default, which request header makes the Symfony reverse proxy treat a request as private?"
    **✅ Cookie (and Authorization)**

    The private_headers option defaults to Authorization and Cookie; requests carrying them skip the shared cache, protecting authenticated responses. Accept/User-Agent/Referer have no such role by default.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php)

??? question "37. Which header lets you inspect whether the reverse proxy served a cache hit?"
    **✅ X-Symfony-Cache**

    HttpCache writes a trace to the trace_header (default X-Symfony-Cache), e.g. "GET /: fresh", "miss", or "store". Age reports elapsed seconds, not hit/miss, and the other header names are invented.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "38. What is the simplest way to enable the reverse proxy in Symfony 8?"
    **✅ Set framework.http_cache: true in configuration**

    framework.http_cache: true wraps the kernel automatically. The alternative is wrapping it manually in public/index.php with the FrameworkBundle HttpCache subclass. There is no compiler pass or #[AsHttpCache] attribute, and Varnish is a separate external proxy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#symfony-reverse-proxy)

??? question "39. Which interfaces does HttpCache implement, and what is its constructor shape?"
    **✅ HttpKernelInterface and TerminableInterface; __construct(HttpKernelInterface $kernel, StoreInterface $store, ?SurrogateInterface $surrogate = null, array $options = [])**

    HttpCache is both an HttpKernelInterface (so it can handle requests) and TerminableInterface (so terminate() propagates). Its constructor takes the wrapped kernel, a StoreInterface, an optional SurrogateInterface (Esi/Ssi) and an options array. It is not a PSR-6 pool nor an event subscriber.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php)

??? question "40. A visitor sends Cache-Control: no-cache to force a reload through the Symfony reverse proxy. What happens by default?"
    **✅ It is ignored — allow_reload defaults to false, so the client cannot force a bypass**

    allow_reload (client no-cache) and allow_revalidate (client max-age=0) both default to false, because letting any client force a bypass invites abuse. So a hard reload does not blow past the shared cache unless you opt in. Nothing is deleted and no error is raised.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/HttpCache.php)

??? question "41. What does this config do? framework: { http_cache: { enabled: true, trace_header: X-Symfony-Cache, default_ttl: 0 } }"
    **✅ Wraps the kernel with HttpCache, sets the trace header name, and applies no default freshness when a response gives none**

    enabled: true wraps the kernel; trace_header sets the debug header name; default_ttl is the TTL used ONLY when a response carries no freshness info — 0 means such responses are not cached by default, but responses that do set s-maxage/max-age are still cached normally. It does not override explicit freshness nor disable caching.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#symfony-reverse-proxy)

??? question "42. A page sets s-maxage=60 but logged-in users never get a shared-cache hit from HttpCache. Why, and how do you still cache the anonymous view?"
    **✅ Their session Cookie is in private_headers, so the request is treated as private; move per-user parts into ESI so the shell stays anonymous/cacheable**

    Logged-in requests carry a session Cookie, which is in the default private_headers, so HttpCache treats them as private and neither serves from nor stores in the shared cache. Anonymous requests are cached. Raising s-maxage changes nothing, HttpCache caches any cacheable response, and private means no shared caching at all — instead isolate per-user bits with ESI fragments.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#symfony-reverse-proxy)

??? question "43. The default HttpCache Store is a distributed store shared across servers out of the box."
    **✅ False**

    False. The default Store (Symfony\\Component\\HttpKernel\\HttpCache\\Store) is a filesystem store keyed by URL + Vary, using digest and lock files. There is no built-in distributed/shared store — that is a reason to use Varnish or a CDN at scale.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/Store.php)

??? question "44. When does the render_esi Twig function actually emit an <esi:include> tag?"
    **✅ Only when a surrogate advertises ESI capability; otherwise it renders the fragment inline**

    The ESI renderer checks the Surrogate-Capability header. Without a surrogate it falls back to inline rendering so the same template works everywhere. It is not always-on, not dev-only, and not tied to content type.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "45. What is the primary benefit of ESI over full-page caching?"
    **✅ Each fragment can be cached with its own independent lifetime**

    ESI caches fragments as separate entries, so a long-lived shell can coexist with short-lived or per-user fragments on one page. It provides no encryption or compression, and it actually requires a surrogate (reverse proxy) to work.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "46. Which component processes <esi:include> tags?"
    **✅ The reverse proxy / surrogate (Symfony HttpCache or Varnish)**

    ESI is a surrogate feature; the gateway cache fetches each include as a sub-request and stitches the results, caching each on its own terms. Twig/PHP only emit the tag, and the browser never sees or resolves it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/HttpCache/Esi.php)

??? question "47. Why does Symfony sign _fragment URIs (UriSigner)?"
    **✅ To prevent attackers forging arbitrary fragment requests**

    Fragment URIs are signed with the application secret (via UriSigner) so only legitimately generated fragment calls are honoured by the kernel. Signing is a security measure, not compression, push, or ETag computation.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "48. What is the minimal config to make render_esi emit real ESI tags that get processed?"
    **✅ framework.esi: true AND a running surrogate (framework.http_cache: true or Varnish)**

    You need ESI enabled (framework.esi: true) AND a surrogate to advertise the capability and process the includes — the Symfony reverse proxy (framework.http_cache: true) or Varnish. Enabling only one of them means render_esi falls back to inline rendering; ESI is not on by default.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "49. Without ESI, adding a #[Cache(smaxage: 5)] fragment to an s-maxage=3600 page collapses the whole page to a 5-second TTL. Which mechanism causes this?"
    **✅ ResponseCacheStrategy reduces the master TTL to the minimum of all embedded (inline) fragment TTLs**

    When a fragment is rendered inline into the master response, ResponseCacheStrategy merges freshness by taking the MINIMUM TTL, so the 5-second fragment caps the page. ESI avoids this by caching the fragment as a separate entry, leaving the shell's long TTL intact. It is not an attribute override, a kernel discard, or Twig stripping headers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "50. Which Twig call embeds a controller as an ESI fragment?"
    **✅ {{ render_esi(controller('App\\Controller\\FragmentController::userGreeting')) }}**

    render_esi() wraps a controller() reference and delegates to the fragment handler, which emits <esi:include> when a surrogate is present (else inline). There is no esi(), include_esi(), or 'esi:' render prefix in Twig — the pair is render()/render_esi()/render_ssi().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "51. What is the near-identical alternative to ESI for servers like nginx or Varnish that speak Server Side Includes?"
    **✅ SSI, via render_ssi(), the Ssi surrogate and framework.ssi**

    SSI is the sibling of ESI: same mixed-freshness idea, exposed through render_ssi(), the Ssi surrogate class and framework.ssi. hinclude is a pure client-side AJAX approach (no caching goal), and the others are unrelated.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "52. You set framework.esi: true but run no reverse proxy. A page uses render_esi for a fragment. What happens?"
    **✅ The fragment renders inline on every request — no separate caching, no benefit, but the page still works**

    With no surrogate advertising ESI capability, render_esi silently falls back to inline rendering, so the fragment is embedded and re-rendered each request — correct output, but none of the per-fragment caching benefit. No exception is thrown and no raw <esi:include> reaches the browser (that only happens if a broken proxy fails to process it).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "53. Which of the following statements are true about cache types and Cache-Control? (select all that apply)"
    **✅ A Symfony response with no explicit caching headers defaults to Cache-Control: no-cache, private ; s-maxage is honoured only by shared caches — the browser ignores it ; setPublic() and setPrivate() are mutually exclusive: the last call wins and removes the other directive**

    Symfony's conservative default is no-cache, private, so shared caching is strictly opt-in; s-maxage targets shared caches only; and you can never end up with both public and private on one response. Vary: Cookie makes a shared cache near-useless because nearly every user has a distinct key, and max-age applies to all caches — s-maxage is the shared-only directive.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "54. Which of the following statements are true about the expiration caching model? (select all that apply)"
    **✅ setSharedMaxAge() also marks the response public — no separate setPublic() call is needed ; For a shared cache the freshness precedence is s-maxage > max-age > Expires**

    setSharedMaxAge() implies public since s-maxage only makes sense for shared caches, and shared caches resolve freshness as s-maxage > max-age > Expires. no-cache means "revalidate before reuse" (never-store is no-store), mustRevalidate() is only a getter — emit the directive via setCache(['must_revalidate' => true]) or #[Cache] — and the #[Cache] attribute is applied late without overriding explicit controller headers.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

??? question "55. Which of the following statements are true about the validation caching model? (select all that apply)"
    **✅ isNotModified() mutates the response into a 304, strips the body, and returns a bool — you must still return the response yourself ; When both If-None-Match and If-Modified-Since are sent, the ETag comparison takes precedence ; A 304 Not Modified response must not carry a message body**

    isNotModified() only mutates the Response (304 + stripped body/content headers) and reports a bool — returning it to the kernel is still your job — ETag beats Last-Modified when both conditional headers are present, and 304 responses are bodiless by definition (Symfony enforces it). The #[Cache] etag expression is SHA-256 hashed before becoming the header, and nothing is sent automatically by isNotModified().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/validation.html)

??? question "56. Which of the following statements are true about Edge Side Includes (ESI)? (select all that apply)"
    **✅ When no surrogate advertises ESI capability, render_esi() silently renders the fragment inline ; Each ESI fragment can carry its own TTL, allowing mixed freshness on a single page ; Fragment URIs are signed with the UriSigner to prevent forged _fragment requests**

    render_esi() degrades gracefully to inline rendering without a surrogate, ESI's whole point is per-fragment TTLs instead of the shortest fragment capping the page's TTL, and _fragment URIs are signed for security. Processing happens in the reverse proxy — either Symfony's own HttpCache (via the Esi surrogate) or Varnish — never in the browser.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/esi.html)

??? question "57. Which of the following statements are true about Symfony's HttpCache reverse proxy? (select all that apply)"
    **✅ HttpCache is a shared cache, so it prefers s-maxage over max-age when computing freshness ; Requests carrying a Cookie or Authorization header are treated as private by default and bypass the shared cache**

    As a shared/gateway cache HttpCache follows s-maxage first, and its private_headers default (Cookie, Authorization) keeps authenticated traffic out of the shared cache. allow_reload/allow_revalidate are off by default, the default Store writes to the filesystem, and HttpCache is a kernel wrapper (framework.http_cache: true or wrapping in public/index.php), implementing HttpKernelInterface and TerminableInterface.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#symfony-reverse-proxy)

??? question "58. Which of the following statements are true about client-side (browser) caching? (select all that apply)"
    **✅ The browser's private cache ignores s-maxage; only max-age and Expires govern it ; Cache-Control is also a request header — clients can send directives like no-cache, max-age=0 or only-if-cached ; Only responses to safe methods are cached — a POST response is never served from the browser cache**

    s-maxage is shared-cache-only so the browser ignores it, Cache-Control request directives let the client steer caches independently of response semantics, and browser caching is restricted to safe methods. A normal reload roughly means max-age=0 (revalidate) while a hard reload means no-cache (full refetch), and bfcache restores the page instantly from memory without a network round trip.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

---

<small>Back to [Flashcards](index.md) · [HTTP Caching](../../http-caching/index.md)</small>
