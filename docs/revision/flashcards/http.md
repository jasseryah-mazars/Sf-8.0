# Flashcards — HTTP

35 cards. **Read the question, answer in your head, then tap to reveal.** Mark the ones you miss and cycle them again.

!!! tip "How to drill"
    First pass: reveal every card. Later passes: only the ones you missed. Spread passes over days.

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

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

??? question "4. A POST must be redirected while preserving its method and body. Which status code? (choose one)"
    **✅ 307 Temporary Redirect**

    307 (temporary) and 308 (permanent) preserve method and body; 301/302 may switch to GET, and 303 forces GET.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/307)

??? question "5. The user is authenticated but lacks permission for a resource. Which status? (choose one)"
    **✅ 403 Forbidden**

    401 means unauthenticated (send WWW-Authenticate); 403 means authenticated but not authorized — re-authenticating will not help.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)

??? question "6. Response::HTTP_UNPROCESSABLE_ENTITY corresponds to which numeric code? (choose one)"
    **✅ 422**

    The constant keeps the RFC 4918 name 'Unprocessable Entity' but is code 422, the correct code for validation errors on a well-formed body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "7. A rate limit is exceeded. Which status code and companion header are correct? (choose one)"
    **✅ 429 Too Many Requests with Retry-After**

    429 signals rate limiting; Retry-After advertises when the client may try again.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429)

??? question "8. Where does the Router place matched route parameters on the Request? (choose one)"
    **✅ $request->attributes**

    The attributes bag (ParameterBag) holds framework/route data such as _route, _controller and path parameters — not the query string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

??? question "9. Which class backs $request->query, $request->request and $request->cookies? (choose one)"
    **✅ InputBag**

    query, request and cookies are InputBag (scalar-restricted); attributes is a plain ParameterBag, server is ServerBag, headers is HeaderBag.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

??? question "10. Which method reads the submitted body regardless of JSON vs form content type? (choose one)"
    **✅ $request->getPayload()**

    getPayload() returns an InputBag from the parsed body (decoding JSON or reading form data); getContent() returns the raw unparsed body string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#accessing-request-data)

??? question "11. Which Response class streams an on-disk file and supports HTTP range requests? (choose one)"
    **✅ BinaryFileResponse**

    BinaryFileResponse streams a file without buffering it in memory and supports Range requests and X-Sendfile.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html#serving-files)

??? question "12. What does Response::prepare() do? (choose one)"
    **✅ Makes the response compliant with the request (charset, body for HEAD/304, protocol version)**

    prepare() normalises the response against the incoming Request; send() (sendHeaders + sendContent) actually transmits it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "13. $response->headers is an instance of which class? (choose one)"
    **✅ ResponseHeaderBag**

    ResponseHeaderBag extends HeaderBag and adds cookie management plus Cache-Control normalisation.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

??? question "14. Which set contains only idempotent methods? (choose one)"
    **✅ GET, PUT, DELETE**

    GET, PUT and DELETE are idempotent (repeating yields the same state); POST and PATCH are not.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Idempotent)

??? question "15. By default in Symfony 8, is the _method parameter honoured? (choose one)"
    **✅ No — http_method_override defaults to false and must be enabled**

    You must enable framework.http_method_override (or call Request::enableHttpMethodParameterOverride()); it applies to POST only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/routing.html)

??? question "16. Which method is both safe and idempotent? (choose one)"
    **✅ GET**

    GET reads with no side effects (safe) and repeats identically (idempotent); PUT is idempotent but not safe.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Safe/HTTP)

??? question "17. After a successful method override, what does getRealMethod() return for a POST+_method=PUT request? (choose one)"
    **✅ POST**

    getMethod() returns the overridden verb (PUT) while getRealMethod() returns the raw transport method (POST).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

??? question "18. SameSite=None is only accepted by browsers when the cookie is also: (choose one)"
    **✅ Secure**

    SameSite=None requires the Secure attribute; otherwise browsers reject the cookie.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value)

??? question "19. Which attribute prevents JavaScript from reading a cookie? (choose one)"
    **✅ HttpOnly**

    HttpOnly hides the cookie from document.cookie, mitigating XSS token theft.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

??? question "20. A cookie with neither Expires nor Max-Age is: (choose one)"
    **✅ a session cookie deleted when the browser closes**

    With no lifetime attribute a cookie is a session cookie, removed when the browser session ends.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

??? question "21. The Symfony Cookie object is immutable. What does Cookie::create('a')->withValue('b') require? (choose one)"
    **✅ Using the returned instance — with* returns a new Cookie**

    Cookie is immutable; every with* method returns a new instance, so the result must be captured or the change is lost.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Cookie.php)

??? question "22. Which caching model can avoid contacting the server entirely? (choose one)"
    **✅ Expiration (freshness)**

    While a copy is fresh (within max-age), the cache serves it with no request; validation always sends a conditional request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache.html)

??? question "23. The s-maxage directive applies to: (choose one)"
    **✅ shared caches (proxies/CDN) only**

    s-maxage is honoured only by shared caches and overrides max-age there.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_cache/expiration.html)

??? question "24. What does Response::isNotModified($request) do on a validator match? (choose one)"
    **✅ Returns true and turns the response into a bodyless 304**

    It compares the request's conditional headers and, on a match, sets the status to 304 and removes the body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

??? question "25. getPreferredLanguage(['en','de']) returns: (choose one)"
    **✅ the best of en/de for this client**

    With a whitelist it intersects the client's ordered languages with your supported list and returns the best match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/components/http_foundation.html)

??? question "26. What does getAcceptableContentTypes() return? (choose one)"
    **✅ MIME types ordered by client preference**

    It returns raw MIME types best-first; getPreferredFormat() returns Symfony format names.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

??? question "27. In an Accept header, what does q=0 mean for an option? (choose one)"
    **✅ Not acceptable (rejected)**

    A quality value of 0 explicitly marks that media type or language as unacceptable.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Quality_values)

??? question "28. Which response header ensures a shared cache stores one entry per representation? (choose one)"
    **✅ Vary**

    Vary lists the request headers that change the response, so caches key each variant separately.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

??? question "29. What is the safe way to pick a locale from the browser's Accept-Language? (choose one)"
    **✅ getPreferredLanguage(['en','fr']) with a whitelist**

    The whitelist form guarantees a supported locale; the others may return one you do not support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html#the-locale-used-in-translations)

??? question "30. What sets the request locale when a route defines {_locale}? (choose one)"
    **✅ LocaleListener calls Request::setLocale() on kernel.request**

    LocaleListener reads the _locale attribute and calls setLocale(); LocaleAwareListener then propagates it to LocaleAware services.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleListener.php)

??? question "31. What does framework.enabled_locales configure? (choose one)"
    **✅ The whitelist of locales the application accepts and generates**

    enabled_locales restricts valid locales (routing _locale, translation compilation); default_locale sets the fallback.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/translation.html)

??? question "32. When is an HttpClient request actually performed? (choose one)"
    **✅ Lazily, on first read of status/headers/content**

    request() returns a lazy ResponseInterface; the transfer completes on first access, which enables free concurrency.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_client.html)

??? question "33. What does ResponseInterface::getContent() do on a 500 response by default? (choose one)"
    **✅ Throws a ServerExceptionInterface**

    By default getContent()/toArray() throw on 3xx/4xx/5xx; pass false (or the throw option) to read the body without throwing. getStatusCode() never throws.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_client.html#handling-exceptions)

??? question "34. Which type should you type-hint to autowire an HTTP client? (choose one)"
    **✅ Symfony\Contracts\HttpClient\HttpClientInterface**

    Depend on the HttpClientInterface contract; the framework selects the concrete transport (curl or native).

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_client.html)

??? question "35. Which class lets you test API integration code without any network traffic? (choose one)"
    **✅ MockHttpClient with MockResponse**

    MockHttpClient returns canned MockResponse objects (or a callback) with no real HTTP requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/current/http_client.html#testing)

---

<small>Back to [Flashcards](index.md) · [HTTP](../../http/index.md)</small>
