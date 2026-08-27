# Flashcards — HTTP

76 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

??? question "1. Which component decides whether a request is served over HTTP/2? (choose one)"
    **✅ The web server / reverse proxy via ALPN negotiation**

    Protocol negotiation happens at the TLS/web-server layer (ALPN). PHP only observes the negotiated version via $request->getProtocolVersion().

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

??? question "2. HTTP is best described as: (choose one)"
    **✅ A stateless, application-layer request/response protocol**

    HTTP is a stateless application-layer protocol; state is layered on with cookies/sessions, and TLS is optional (HTTPS).

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

??? question "3. Which Request method returns the negotiated HTTP protocol version (e.g. HTTP/2)? (choose one)"
    **✅ getProtocolVersion()**

    getScheme() returns http/https; getProtocolVersion() returns the version string from SERVER_PROTOCOL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "4. In a Symfony 8 app, HTTP/2 server push is the recommended way to preload sub-resources and 103 Early Hints should be avoided. True or false?"
    **✅ False**

    It is the reverse. HTTP/2 server push is effectively dead — browsers have dropped support — and the modern replacement for hinting sub-resources is the 103 Early Hints informational response. The claim also mislocates the decision: push/version selection is a web-server concern, not a PHP one.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103)

??? question "5. At the front controller, which call builds the Request object from PHP's superglobals? (choose one)"
    **✅ Request::createFromGlobals()**

    public/index.php calls Request::createFromGlobals(), which reads $_GET, $_POST, $_SERVER, $_COOKIE and $_FILES once into the typed bags. Request::create() builds a synthetic request from explicit arguments (used in tests/sub-requests), and there is no createFromRequest() factory for this purpose.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "6. An app sits behind a TLS-terminating reverse proxy that forwards X-Forwarded-Proto: https, yet $request->isSecure() returns false. What is the most likely cause? (choose one)"
    **✅ Trusted proxies were not declared, so Symfony ignores X-Forwarded-* headers**

    For security, Symfony trusts X-Forwarded-* (including -Proto) only from proxies registered via Request::setTrustedProxies() (or framework.trusted_proxies). Until then isSecure() reflects the direct connection (plain HTTP from the proxy) and returns false. PHP never terminates TLS; the edge does.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment/proxies.html)

??? question "7. On a keep-alive connection, why is the first request typically slower than the ones that follow it? (choose one)"
    **✅ It pays for DNS resolution plus the TCP and TLS handshakes before any HTTP byte flows; later requests reuse the warm connection**

    The first exchange must complete DNS → TCP 3-way handshake → TLS handshake before the HTTP request is even sent. Subsequent requests on the same keep-alive (HTTP/1.1) or multiplexed (HTTP/2/3) connection skip that setup. The HTTP version is fixed for the life of the connection, and body caching is a separate concern.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

??? question "8. A POST must be redirected while preserving its method and body. Which status code? (choose one)"
    **✅ 307 Temporary Redirect**

    307 (temporary) and 308 (permanent) preserve method and body; 301/302 may switch to GET, and 303 forces GET.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/307)

??? question "9. The user is authenticated but lacks permission for a resource. Which status? (choose one)"
    **✅ 403 Forbidden**

    401 means unauthenticated (send WWW-Authenticate); 403 means authenticated but not authorized — re-authenticating will not help.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)

??? question "10. Response::HTTP_UNPROCESSABLE_ENTITY corresponds to which numeric code? (choose one)"
    **✅ 422**

    The constant keeps the RFC 4918 name 'Unprocessable Entity' but is code 422, the correct code for validation errors on a well-formed body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "11. A rate limit is exceeded. Which status code and companion header are correct? (choose one)"
    **✅ 429 Too Many Requests with Retry-After**

    429 signals rate limiting; Retry-After advertises when the client may try again.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429)

??? question "12. You issue a 302 (instead of 303) after a successful POST. What is the real-world risk? (choose one)"
    **✅ Some clients may re-issue the request as POST, causing a duplicate submission**

    302's method-handling is historically ambiguous, so a client may repeat the POST on the redirect. 303 See Other is unambiguous: it forces a GET to the target, implementing Post/Redirect/Get and preventing resubmission on refresh. 307 would also preserve POST — the opposite of what you want here.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/303)

??? question "13. Which status codes preserve the original request method and body when redirecting? (choose 2)"
    **✅ 307 Temporary Redirect ; 308 Permanent Redirect**

    307 (temporary) and 308 (permanent) are the method-and-body-preserving redirects. 302 may be downgraded to GET by clients and 303 always forces GET, so neither is safe when a non-GET method must survive the redirect.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/308)

??? question "14. You call new Response('', Response::HTTP_CREATED) without a reason phrase. How does Symfony fill the reason phrase? (choose one)"
    **✅ setStatusCode() looks the code up in the public static Response::$statusTexts map**

    Response::$statusTexts is a public static array mapping each known code to its reason phrase; setStatusCode() consults it when no explicit text is supplied. An unknown code simply yields an empty phrase (still valid). The HTTP_* constants are plain integers and carry no text themselves.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "15. What happens when you call $response->setStatusCode(600)? (choose one)"
    **✅ It throws \InvalidArgumentException because the code is outside 100–599**

    setStatusCode() validates that the code is within the HTTP range 100–599 and throws \\InvalidArgumentException otherwise — a common gotcha when a code is computed dynamically. It neither clamps nor stores out-of-range values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "16. 401 Unauthorized means the user is authenticated but lacks permission. True or false?"
    **✅ False**

    401 actually means *not authenticated* — credentials are missing or invalid, and the server must send a WWW-Authenticate header. The 'authenticated but not allowed' case is 403 Forbidden, where re-authenticating will not help. The name 'Unauthorized' is a long-standing misnomer.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401)

??? question "17. Where does the Router place matched route parameters on the Request? (choose one)"
    **✅ $request->attributes**

    The attributes bag (ParameterBag) holds framework/route data such as _route, _controller and path parameters — not the query string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "18. Which class backs $request->query, $request->request and $request->cookies? (choose one)"
    **✅ InputBag**

    query, request and cookies are InputBag (scalar-restricted); attributes is a plain ParameterBag, server is ServerBag, headers is HeaderBag.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

??? question "19. Which method reads the submitted body regardless of JSON vs form content type? (choose one)"
    **✅ $request->getPayload()**

    getPayload() returns an InputBag from the parsed body (decoding JSON or reading form data); getContent() returns the raw unparsed body string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#accessing-request-data)

??? question "20. Which method reports the request format derived from the body's Content-Type header in Symfony 8? (choose one)"
    **✅ getContentTypeFormat()**

    getContentType() was removed; the current method is getContentTypeFormat(), which maps the incoming Content-Type to a Symfony format (e.g. 'json'). getRequestFormat() reads the _format attribute, and getPreferredFormat() negotiates from the client's Accept header — different concerns entirely.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

??? question "21. Why does InputBag (query/request/cookies) reject reading an array where a scalar is expected? (choose one)"
    **✅ InputBag restricts values to scalars/arrays-of-scalars/null and throws BadRequestException on a type mismatch, hardening against malicious nested input**

    InputBag extends ParameterBag but narrows the contract to user-supplied data: get() accepts only scalars/null and raises a BadRequestException (HTTP 400) when handed an unexpected array, blocking parameter-pollution style attacks. A plain ParameterBag (used by attributes) imposes no such restriction. Use all('key') to intentionally read array values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

??? question "22. Route parameters such as {id} are read from $request->query. True or false?"
    **✅ False**

    Route parameters live in $request->attributes (a ParameterBag), written by the Router — not in $request->query, which mirrors $_GET (the URL query string). Reading {id} via query returns null; use $request->attributes->get('id').

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "23. A request handler crashes with a TypeError only when the X-Trace-Id header is absent, on the line strtoupper($request->headers->get('X-Trace-Id')). What is the cause and fix? (choose one)"
    **✅ HeaderBag::get() returns null for a missing key; guard with ?? or supply a default before calling a string function**

    HeaderBag::get(string $key, mixed $default = null) returns null when the key is absent — a normal lookup miss, not an error. Passing null to strtoupper() triggers the TypeError. Guard with $request->headers->get('X-Trace-Id') ?? '' or pass a default. Typed InputBag getters (getString etc.) coalesce to a zero value, but HeaderBag::get() is nullable.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/HeaderBag.php)

??? question "24. Which Response class streams an on-disk file and supports HTTP range requests? (choose one)"
    **✅ BinaryFileResponse**

    BinaryFileResponse streams a file without buffering it in memory and supports Range requests and X-Sendfile.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#serving-files)

??? question "25. What does Response::prepare() do? (choose one)"
    **✅ Makes the response compliant with the request (charset, body for HEAD/304, protocol version)**

    prepare() normalises the response against the incoming Request; send() (sendHeaders + sendContent) actually transmits it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "26. $response->headers is an instance of which class? (choose one)"
    **✅ ResponseHeaderBag**

    ResponseHeaderBag extends HeaderBag and adds cookie management plus Cache-Control normalisation.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

??? question "27. You create new Response('hi') and set no cache headers. What Cache-Control does ResponseHeaderBag emit by default? (choose one)"
    **✅ no-cache, private**

    When you set no cache directives, ResponseHeaderBag computes a sensible default of 'no-cache, private', so a bare response is never stored by shared caches. Calling setPublic()/setMaxAge()/setSharedMaxAge() changes this. It is not 'no-store', and a Cache-Control header is always present.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

??? question "28. In Symfony 8, where does the makeDisposition() helper for a Content-Disposition header live? (choose one)"
    **✅ Symfony\Component\HttpFoundation\HeaderUtils::makeDisposition()**

    makeDisposition() now lives on HeaderUtils; the old ResponseHeaderBag::makeDisposition() was removed. For file responses you can also use BinaryFileResponse::setContentDisposition(), which delegates to the same logic — but the static helper itself is on HeaderUtils.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#serving-files)

??? question "29. You must serve a 2 GB file for download without exhausting memory. Which approach is correct? (choose one)"
    **✅ Return a BinaryFileResponse (or StreamedResponse) so the bytes are streamed, not buffered**

    new Response(file_get_contents(...)) loads the whole file into memory and will exhaust it. BinaryFileResponse streams a file already on disk (and adds Range and X-Sendfile support), while StreamedResponse streams generated output. Both keep memory flat regardless of size.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#serving-files)

??? question "30. Response::prepare() transmits the status line, headers and body to the client. True or false?"
    **✅ False**

    prepare() only normalises the response against the request (charset, Content-Type/Length, stripping the body for HEAD/204/304, aligning the protocol). Transmission is done by send(), which calls sendHeaders() then sendContent(). The kernel calls prepare() automatically before send().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "31. Which set contains only idempotent methods? (choose one)"
    **✅ GET, PUT, DELETE**

    GET, PUT and DELETE are idempotent (repeating yields the same state); POST and PATCH are not.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Idempotent)

??? question "32. By default in Symfony 8, is the _method parameter honoured? (choose one)"
    **✅ No — http_method_override defaults to false and must be enabled**

    You must enable framework.http_method_override (or call Request::enableHttpMethodParameterOverride()); it applies to POST only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

??? question "33. Which method is both safe and idempotent? (choose one)"
    **✅ GET**

    GET reads with no side effects (safe) and repeats identically (idempotent); PUT is idempotent but not safe.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Safe/HTTP)

??? question "34. After a successful method override, what does getRealMethod() return for a POST+_method=PUT request? (choose one)"
    **✅ POST**

    getMethod() returns the overridden verb (PUT) while getRealMethod() returns the raw transport method (POST).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

??? question "35. A candidate claims PATCH is always idempotent like PUT. Why is this wrong? (choose one)"
    **✅ PATCH applies a partial change that may differ when repeated (e.g. an increment delta), so it is generally not idempotent**

    PUT replaces a resource wholesale, so sending the same body twice leaves the same state (idempotent). PATCH describes a partial modification; a delta such as 'add 1' applied twice yields a different result, so PATCH is generally not idempotent. Neither PATCH nor PUT is safe — both change state.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH)

??? question "36. Which configuration enables the _method override on POST forms? (choose one)"
    **✅ framework:
    http_method_override: true**

    The key is framework.http_method_override (default false). It makes Symfony honour a _method field (or X-HTTP-Method-Override header) on POST requests, rewriting the method to PUT/PATCH/DELETE. The other keys do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#http-method-override)

??? question "37. Which HTTP methods are considered safe? (choose 3)"
    **✅ GET ; HEAD ; OPTIONS**

    Safe methods do not change server state: GET, HEAD, OPTIONS (and TRACE). POST is neither safe nor idempotent. All safe methods are idempotent, but the converse is false — PUT and DELETE are idempotent yet not safe.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Safe/HTTP)

??? question "38. What are the exact conditions under which Symfony applies the method override? (choose one)"
    **✅ Only on a POST request, only when enabled, and only to the values PUT, PATCH or DELETE**

    The override fires only when http_method_override is enabled, only on a POST transport request, and rewrites the method solely to PUT/PATCH/DELETE. Other transports are never rewritten, which is why getRealMethod() still reports POST.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

??? question "39. SameSite=None is only accepted by browsers when the cookie is also: (choose one)"
    **✅ Secure**

    SameSite=None requires the Secure attribute; otherwise browsers reject the cookie.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value)

??? question "40. Which attribute prevents JavaScript from reading a cookie? (choose one)"
    **✅ HttpOnly**

    HttpOnly hides the cookie from document.cookie, mitigating XSS token theft.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

??? question "41. A cookie with neither Expires nor Max-Age is: (choose one)"
    **✅ a session cookie deleted when the browser closes**

    With no lifetime attribute a cookie is a session cookie, removed when the browser session ends.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

??? question "42. The Symfony Cookie object is immutable. What does Cookie::create('a')->withValue('b') require? (choose one)"
    **✅ Using the returned instance — with* returns a new Cookie**

    Cookie is immutable; every with* method returns a new instance, so the result must be captured or the change is lost.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Cookie.php)

??? question "43. A cookie set with Path=/app and Domain=.example.com is not deleted by $response->headers->clearCookie('session'). Why? (choose one)"
    **✅ clearCookie() defaults to path '/' and no domain, so the expiry targets a different scope and the original survives**

    A browser keys cookies by name plus path plus domain. clearCookie() emits a past-dated Set-Cookie, but with its default path '/' and no domain it does not match the original (Path=/app, Domain=.example.com), so the browser expires a non-existent cookie and keeps the real one. Fix: clearCookie('session', '/app', '.example.com').

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

??? question "44. Which framework configuration sets the session cookie's SameSite policy to Lax and hides it from JavaScript? (choose one)"
    **✅ framework:
    session:
        cookie_samesite: lax
        cookie_httponly: true**

    Session cookie behaviour is configured under framework.session with the cookie_* keys: cookie_samesite (strict|lax|none), cookie_httponly, and cookie_secure (often 'auto'). Symfony's defaults are already HttpOnly: true and SameSite: lax. The other key shapes do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#cookie-samesite)

??? question "45. What does the __Host- cookie name prefix force the browser to require? (choose one)"
    **✅ Secure, no Domain attribute, and Path=/ — the strictest scoping the browser enforces**

    A cookie named __Host-... is accepted only if it is Secure, has no Domain attribute (so it is locked to the exact host), and uses Path=/. This is the strongest same-origin scoping the browser guarantees, preventing subdomain injection. The related __Secure- prefix only requires the Secure flag.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#cookie_prefixes)

??? question "46. Symfony's session cookie defaults to HttpOnly: true and SameSite: lax. True or false?"
    **✅ True**

    Symfony ships secure session-cookie defaults: HttpOnly is true (JavaScript cannot read the session id) and SameSite is lax (mitigating most CSRF via cookies while still allowing top-level GET navigations). cookie_secure typically defaults to 'auto' (Secure when the request is HTTPS).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#cookie-httponly)

??? question "47. Which caching model can avoid contacting the server entirely? (choose one)"
    **✅ Expiration (freshness)**

    While a copy is fresh (within max-age), the cache serves it with no request; validation always sends a conditional request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "48. The s-maxage directive applies to: (choose one)"
    **✅ shared caches (proxies/CDN) only**

    s-maxage is honoured only by shared caches and overrides max-age there.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

??? question "49. What does Response::isNotModified($request) do on a validator match? (choose one)"
    **✅ Returns true and turns the response into a bodyless 304**

    It compares the request's conditional headers and, on a match, sets the status to 304 and removes the body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "50. Which statement correctly contrasts freshness and validation caching? (choose one)"
    **✅ Freshness (max-age) can serve with no request; validation (ETag/Last-Modified) always sends a conditional request that may return 304**

    Freshness uses Cache-Control: max-age/s-maxage (and Expires); while fresh the cache answers with zero round-trips. Validation uses ETag/If-None-Match and Last-Modified/If-Modified-Since — it always asks, but the server can reply 304 Not Modified with no body. The models are complementary, not interchangeable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/validation.html)

??? question "51. Which attribute declaratively marks a controller's response public and cacheable for one hour in shared and private caches? (choose one)"
    **✅ #[Cache(public: true, maxage: 3600, smaxage: 3600)]**

    Symfony\\Component\\HttpKernel\\Attribute\\Cache exposes public, maxage, smaxage, expires, etag and lastModified. #[Cache(public: true, maxage: 3600, smaxage: 3600)] sets Cache-Control: public, max-age=3600, s-maxage=3600. The other attributes do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#introducing-http-caching)

??? question "52. To cache a public page in a CDN for 10 minutes without letting the browser cache it long-term, which setter do you use? (choose one)"
    **✅ setSharedMaxAge(600) (plus setPublic()), which emits s-maxage honoured only by shared caches**

    setSharedMaxAge() writes s-maxage, obeyed only by shared caches (CDN/proxy) and it implies public. setMaxAge() targets any cache including the browser, so it is the wrong tool here. setPrivate() would forbid shared caching entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

??? question "53. A default Symfony Response is storable by a shared cache (CDN/proxy) out of the box. True or false?"
    **✅ False**

    A default response carries Cache-Control: no-cache, private, so shared caches will not store it. You must opt in with setPublic()/setSharedMaxAge() (or #[Cache(public: true)]). Marking user-specific responses public would leak data across users.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

??? question "54. getPreferredLanguage(['en','de']) returns: (choose one)"
    **✅ the best of en/de for this client**

    With a whitelist it intersects the client's ordered languages with your supported list and returns the best match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "55. What does getAcceptableContentTypes() return? (choose one)"
    **✅ MIME types ordered by client preference**

    It returns raw MIME types best-first; getPreferredFormat() returns Symfony format names.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

??? question "56. In an Accept header, what does q=0 mean for an option? (choose one)"
    **✅ Not acceptable (rejected)**

    A quality value of 0 explicitly marks that media type or language as unacceptable.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Quality_values)

??? question "57. Which response header ensures a shared cache stores one entry per representation? (choose one)"
    **✅ Vary**

    Vary lists the request headers that change the response, so caches key each variant separately.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

??? question "58. What is the key difference between getPreferredFormat() and getAcceptableContentTypes()? (choose one)"
    **✅ getPreferredFormat() returns a Symfony format name (e.g. 'json'); getAcceptableContentTypes() returns raw MIME types**

    getPreferredFormat() maps the client's Accept header to a short Symfony format (html, json, xml, csv...), best for a match expression. getAcceptableContentTypes() returns the raw MIME strings ordered by preference. Confusing format names with MIME types is a classic trap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

??? question "59. Given AcceptHeader::fromString('text/html;q=0.9, application/json;q=1.0'), what does $accept->first()?->getQuality() return? (choose one)"
    **✅ 1.0 — first() returns the highest-quality item (application/json)**

    AcceptHeader parses and sorts items by quality (descending), so first() returns the AcceptHeaderItem for application/json (q=1.0) and getQuality() gives 1.0. The nullsafe operator guards the empty-header case where first() would return null.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/AcceptHeader.php)

??? question "60. A proxy sometimes serves the JSON representation of /articles/7 to a browser expecting HTML. What is the most likely fix? (choose one)"
    **✅ Add Vary: Accept (via $response->setVary(['Accept'])) so the cache keys each representation separately**

    Without Vary, a shared cache stores one entry for the URL and may replay the wrong representation. setVary(['Accept']) tells caches the response varies by the Accept header, so each variant is stored separately. Marking it private would just disable caching; Accept is a request header, not a response one.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

??? question "61. How does getRequestFormat() differ from getPreferredFormat()? (choose one)"
    **✅ getRequestFormat() returns the format from the _format attribute (e.g. a route suffix); getPreferredFormat() negotiates from the client's Accept header**

    getRequestFormat(?string $default = 'html') returns the format stored in the _format request attribute (set e.g. by a /path.{_format} route), while getPreferredFormat() computes the best format from the client's Accept header. Mixing the two is a common mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "62. What is the safe way to pick a locale from the browser's Accept-Language? (choose one)"
    **✅ getPreferredLanguage(['en','fr']) with a whitelist**

    The whitelist form guarantees a supported locale; the others may return one you do not support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html#the-locale-used-in-translations)

??? question "63. What sets the request locale when a route defines {_locale}? (choose one)"
    **✅ LocaleListener calls Request::setLocale() on kernel.request**

    LocaleListener reads the _locale attribute and calls setLocale(); LocaleAwareListener then propagates it to LocaleAware services.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleListener.php)

??? question "64. What does framework.enabled_locales configure? (choose one)"
    **✅ The whitelist of locales the application accepts and generates**

    enabled_locales restricts valid locales (routing _locale, translation compilation); default_locale sets the fallback.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html)

??? question "65. Which configuration makes Symfony guess the request locale from Accept-Language automatically, bounded to en and fr, with no custom listener? (choose one)"
    **✅ framework:
    enabled_locales: ['en', 'fr']
    set_locale_from_accept_language: true**

    set_locale_from_accept_language: true tells Symfony to set the request locale from Accept-Language when no _locale is present, constrained to enabled_locales. No custom kernel.request listener is needed. The other keys do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#set-locale-from-accept-language)

??? question "66. The browser sends Accept-Language: es, en;q=0.8 and the app supports only ['en','fr']. What does getPreferredLanguage(['en','fr']) return? (choose one)"
    **✅ en — es is unsupported, so the next acceptable option in the whitelist (en, q=0.8) wins**

    getPreferredLanguage intersects the client's ordered languages with your whitelist. es is not supported, so it is skipped; en (q=0.8) is the best remaining acceptable option and is returned. With a whitelist it never returns an unsupported locale, and it falls back to the first list entry only if none match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

??? question "67. After the request locale is set, how does it reach services like the Translator? (choose one)"
    **✅ LocaleAwareListener pushes it into every service implementing LocaleAwareInterface**

    LocaleListener sets the request locale; LocaleAwareListener then calls setLocale() on every service tagged/implementing Symfony\\Contracts\\Translation\\LocaleAwareInterface (e.g. the Translator). For a scoped switch you use LocaleSwitcher. Services do not read superglobals.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleAwareListener.php)

??? question "68. Why is calling getPreferredLanguage() with no argument risky for locale detection? (choose one)"
    **✅ It returns the client's top language unfiltered, which may be a locale you do not support (e.g. pt-BR)**

    Without a whitelist, getPreferredLanguage() returns the client's single highest-ranked language regardless of what your app supports, so you may get an unsupported locale and break translations/routing. Always pass your supported list so the result is bounded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html#the-locale-used-in-translations)

??? question "69. When is an HttpClient request actually performed? (choose one)"
    **✅ Lazily, on first read of status/headers/content**

    request() returns a lazy ResponseInterface; the transfer completes on first access, which enables free concurrency.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html)

??? question "70. What does ResponseInterface::getContent() do on a 500 response by default? (choose one)"
    **✅ Throws a ServerExceptionInterface**

    By default getContent()/toArray() throw on 3xx/4xx/5xx; pass false (or the throw option) to read the body without throwing. getStatusCode() never throws.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#handling-exceptions)

??? question "71. Which type should you type-hint to autowire an HTTP client? (choose one)"
    **✅ Symfony\Contracts\HttpClient\HttpClientInterface**

    Depend on the HttpClientInterface contract; the framework selects the concrete transport (curl or native).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html)

??? question "72. Which class lets you test API integration code without any network traffic? (choose one)"
    **✅ MockHttpClient with MockResponse**

    MockHttpClient returns canned MockResponse objects (or a callback) with no real HTTP requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#testing)

??? question "73. What does this test assert? $client = new MockHttpClient(new MockResponse('{"id":42}')); $data = $client->request('GET', 'https://api.test/x')->toArray(); (choose one)"
    **✅ $data === ['id' => 42], produced from the canned body with no network call**

    MockHttpClient serves the supplied MockResponse without any network; toArray() JSON-decodes the body to ['id' => 42]. MockResponse defaults to HTTP 200, so no exception is thrown, and toArray() returns an array, not the raw string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#testing)

??? question "74. Which framework configuration defines a scoped client that prefixes a base URI and bearer token for one API? (choose one)"
    **✅ framework:
    http_client:
        scoped_clients:
            github.client:
                base_uri: 'https://api.github.com/'
                auth_bearer: '%env(GITHUB_TOKEN)%'**

    Scoped clients are declared under framework.http_client.scoped_clients; each named entry (e.g. github.client) applies its base_uri, headers and auth only to matching URLs. The framework registers a service you autowire by variable name ($githubClient). The other shapes are invalid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#scoping-client)

??? question "75. Reading each response's getContent() inside the loop that fires the requests makes the batch slow. Why? (choose one)"
    **✅ Reading the body blocks until that transfer completes, so requests run sequentially instead of concurrently**

    request() is lazy/async: firing them all first lets transfers overlap. But calling getContent() on a response forces that transfer to finish before the next request() runs, serialising the batch. Fire all requests first, then read (or iterate $client->stream($responses)) to keep concurrency.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#concurrent-requests)

??? question "76. You call toArray() on a 204 No Content response (empty body). What happens? (choose one)"
    **✅ It throws a JsonException because an empty string is not valid JSON — guard by checking the status/empty body first**

    getContent() on an empty body returns '' (not null), but toArray() tries to JSON-decode that '' and throws JsonException. There is no silent null. Guard with a 204/empty check before decoding, e.g. if (204 === $r->getStatusCode() || '' === $r->getContent(false)) return [];.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#processing-responses)

---

<small>Back to [Flashcards](index.md) · [HTTP](../../http/index.md)</small>
