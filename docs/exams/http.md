# Chapter Exam — HTTP

!!! abstract "How to use"
    84 questions spanning every subchapter of **HTTP**, ordered easy → hard. Answer before revealing each key. For a timed, cross-topic paper use the [Mock Exams](../revision/mock-exam.md).

!!! danger "Not an official exam"
    Practice question, not an official exam question. This bank is community-authored and aligned with the syllabus — it is not sourced from, or reviewed by, the official Symfony 8 certification.

Full theory: [HTTP](../http/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Cette page est une **banque de 76 questions type QCM** sur HTTP, avec correction dépliable sous chaque question. Ce n'est pas un cours : c'est un entraînement, à faire après avoir lu le chapitre.

**Pourquoi ça existe ?** Lire un chapitre donne l'impression d'avoir compris, mais répondre à une question sous forme d'examen (sans relire ses notes) révèle les vraies lacunes — c'est ce que fera l'examen officiel.

**🏠 Analogie de la vraie vie :** C'est le **permis de conduire**. Le code de la route (le cours) explique les règles ; les séries de questions du permis blanc (cette page) vérifient que tu sais les appliquer sous forme de question piège, sans l'aide du livre.

**Symfony dans la vraie vie :** Cours du chapitre → code de la route appris / Question du QCM → question du permis blanc / Réponse dépliable → correction avec explication / Score obtenu → indicateur "prêt à passer l'examen ou pas".

**⚠️ Erreur fréquente :** Déplier la réponse avant d'avoir vraiment tranché son choix. Le cerveau retient beaucoup mieux une explication lue *après* s'être trompé (ou avoir hésité) que lue en passant, sans effort de rappel préalable.

**🧠 Comment le mémoriser :** *« Je réponds d'abord, je vérifie ensuite »* — jamais l'inverse. Note les questions ratées : ce sont exactement les pièges que l'examinateur pose aussi.

---

**Q1.** HTTP is best described as: (choose one)  <small>_(easy · single)_</small>

- A. A stateless, application-layer request/response protocol
- B. A stateful transport-layer protocol
- C. A protocol that always requires TLS
- D. A binary-only protocol since HTTP/1.1

??? success "Answer Q1"
    **A**

    HTTP is a stateless application-layer protocol; state is layered on with cookies/sessions, and TLS is optional (HTTPS).

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

**Q2.** Which Request method returns the negotiated HTTP protocol version (e.g. HTTP/2)? (choose one)  <small>_(easy · single)_</small>

- A. getProtocolVersion()
- B. getScheme()
- C. getMethod()
- D. getContentTypeFormat()

??? success "Answer Q2"
    **A**

    getScheme() returns http/https; getProtocolVersion() returns the version string from SERVER_PROTOCOL.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q3.** At the front controller, which call builds the Request object from PHP's superglobals? (choose one)  <small>_(easy · internals)_</small>

- A. Request::createFromGlobals()
- B. Request::create()
- C. new Request($_SERVER)
- D. Request::createFromRequest()

??? success "Answer Q3"
    **A**

    public/index.php calls Request::createFromGlobals(), which reads $_GET, $_POST, $_SERVER, $_COOKIE and $_FILES once into the typed bags. Request::create() builds a synthetic request from explicit arguments (used in tests/sub-requests), and there is no createFromRequest() factory for this purpose.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q4.** The user is authenticated but lacks permission for a resource. Which status? (choose one)  <small>_(easy · single)_</small>

- A. 403 Forbidden
- B. 401 Unauthorized
- C. 400 Bad Request
- D. 422 Unprocessable Content

??? success "Answer Q4"
    **A**

    401 means unauthenticated (send WWW-Authenticate); 403 means authenticated but not authorized — re-authenticating will not help.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)

**Q5.** Response::HTTP_UNPROCESSABLE_ENTITY corresponds to which numeric code? (choose one)  <small>_(easy · single)_</small>

- A. 422
- B. 400
- C. 409
- D. 429

??? success "Answer Q5"
    **A**

    The constant keeps the RFC 4918 name 'Unprocessable Entity' but is code 422, the correct code for validation errors on a well-formed body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q6.** 401 Unauthorized means the user is authenticated but lacks permission. True or false?  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q6"
    **A**

    401 actually means *not authenticated* — credentials are missing or invalid, and the server must send a WWW-Authenticate header. The 'authenticated but not allowed' case is 403 Forbidden, where re-authenticating will not help. The name 'Unauthorized' is a long-standing misnomer.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401)

**Q7.** Where does the Router place matched route parameters on the Request? (choose one)  <small>_(easy · single)_</small>

- A. $request->attributes
- B. $request->query
- C. $request->request
- D. $request->server

??? success "Answer Q7"
    **A**

    The attributes bag (ParameterBag) holds framework/route data such as _route, _controller and path parameters — not the query string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q8.** Route parameters such as {id} are read from $request->query. True or false?  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q8"
    **A**

    Route parameters live in $request->attributes (a ParameterBag), written by the Router — not in $request->query, which mirrors $_GET (the URL query string). Reading {id} via query returns null; use $request->attributes->get('id').

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q9.** $response->headers is an instance of which class? (choose one)  <small>_(easy · single)_</small>

- A. ResponseHeaderBag
- B. HeaderBag
- C. ParameterBag
- D. InputBag

??? success "Answer Q9"
    **A**

    ResponseHeaderBag extends HeaderBag and adds cookie management plus Cache-Control normalisation.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

**Q10.** Response::prepare() transmits the status line, headers and body to the client. True or false?  <small>_(easy · true-false)_</small>

- A. False
- B. True

??? success "Answer Q10"
    **A**

    prepare() only normalises the response against the request (charset, Content-Type/Length, stripping the body for HEAD/204/304, aligning the protocol). Transmission is done by send(), which calls sendHeaders() then sendContent(). The kernel calls prepare() automatically before send().

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q11.** Which set contains only idempotent methods? (choose one)  <small>_(easy · single)_</small>

- A. GET, PUT, DELETE
- B. GET, POST, PUT
- C. POST, PATCH, DELETE
- D. POST, PUT, PATCH

??? success "Answer Q11"
    **A**

    GET, PUT and DELETE are idempotent (repeating yields the same state); POST and PATCH are not.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Idempotent)

**Q12.** Which method is both safe and idempotent? (choose one)  <small>_(easy · single)_</small>

- A. GET
- B. POST
- C. PUT
- D. PATCH

??? success "Answer Q12"
    **A**

    GET reads with no side effects (safe) and repeats identically (idempotent); PUT is idempotent but not safe.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Safe/HTTP)

**Q13.** Which HTTP methods are considered safe? (choose 3)  <small>_(easy · multiple)_</small>

- A. GET
- B. HEAD
- C. OPTIONS
- D. POST

??? success "Answer Q13"
    **A, B, C**

    Safe methods do not change server state: GET, HEAD, OPTIONS (and TRACE). POST is neither safe nor idempotent. All safe methods are idempotent, but the converse is false — PUT and DELETE are idempotent yet not safe.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Safe/HTTP)

**Q14.** SameSite=None is only accepted by browsers when the cookie is also: (choose one)  <small>_(easy · single)_</small>

- A. Secure
- B. HttpOnly
- C. Domain-scoped
- D. a session cookie

??? success "Answer Q14"
    **A**

    SameSite=None requires the Secure attribute; otherwise browsers reject the cookie.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value)

**Q15.** Which attribute prevents JavaScript from reading a cookie? (choose one)  <small>_(easy · single)_</small>

- A. HttpOnly
- B. Secure
- C. SameSite
- D. Path

??? success "Answer Q15"
    **A**

    HttpOnly hides the cookie from document.cookie, mitigating XSS token theft.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

**Q16.** A cookie with neither Expires nor Max-Age is: (choose one)  <small>_(easy · single)_</small>

- A. a session cookie deleted when the browser closes
- B. permanent
- C. rejected by the browser
- D. valid for exactly 24 hours

??? success "Answer Q16"
    **A**

    With no lifetime attribute a cookie is a session cookie, removed when the browser session ends.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

**Q17.** Symfony's session cookie defaults to HttpOnly: true and SameSite: lax. True or false?  <small>_(easy · true-false)_</small>

- A. True
- B. False

??? success "Answer Q17"
    **A**

    Symfony ships secure session-cookie defaults: HttpOnly is true (JavaScript cannot read the session id) and SameSite is lax (mitigating most CSRF via cookies while still allowing top-level GET navigations). cookie_secure typically defaults to 'auto' (Secure when the request is HTTPS).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#cookie-httponly)

**Q18.** Which caching model can avoid contacting the server entirely? (choose one)  <small>_(easy · single)_</small>

- A. Expiration (freshness)
- B. Validation
- C. Both always
- D. Neither

??? success "Answer Q18"
    **A**

    While a copy is fresh (within max-age), the cache serves it with no request; validation always sends a conditional request.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

**Q19.** In an Accept header, what does q=0 mean for an option? (choose one)  <small>_(easy · single)_</small>

- A. Not acceptable (rejected)
- B. Highest priority
- C. The default weight
- D. A wildcard match

??? success "Answer Q19"
    **A**

    A quality value of 0 explicitly marks that media type or language as unacceptable.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Glossary/Quality_values)

**Q20.** Which response header ensures a shared cache stores one entry per representation? (choose one)  <small>_(easy · single)_</small>

- A. Vary
- B. Content-Type
- C. Cache-Control: private
- D. Accept

??? success "Answer Q20"
    **A**

    Vary lists the request headers that change the response, so caches key each variant separately.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

**Q21.** What does framework.enabled_locales configure? (choose one)  <small>_(easy · single)_</small>

- A. The whitelist of locales the application accepts and generates
- B. The single default locale
- C. Whether the Translator is enabled
- D. Whether content negotiation is on

??? success "Answer Q21"
    **A**

    enabled_locales restricts valid locales (routing _locale, translation compilation); default_locale sets the fallback.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html)

**Q22.** Which type should you type-hint to autowire an HTTP client? (choose one)  <small>_(easy · single)_</small>

- A. Symfony\Contracts\HttpClient\HttpClientInterface
- B. Symfony\Component\HttpClient\CurlHttpClient
- C. Symfony\Component\HttpClient\NativeHttpClient
- D. Symfony\Component\HttpClient\Psr18Client

??? success "Answer Q22"
    **A**

    Depend on the HttpClientInterface contract; the framework selects the concrete transport (curl or native).

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html)

**Q23.** Which class lets you test API integration code without any network traffic? (choose one)  <small>_(easy · single)_</small>

- A. MockHttpClient with MockResponse
- B. RetryableHttpClient
- C. ScopingHttpClient
- D. EventSourceHttpClient

??? success "Answer Q23"
    **A**

    MockHttpClient returns canned MockResponse objects (or a callback) with no real HTTP requests.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#testing)

**Q24.** Which component decides whether a request is served over HTTP/2? (choose one)  <small>_(medium · single)_</small>

- A. The web server / reverse proxy via ALPN negotiation
- B. The Symfony Request object
- C. public/index.php
- D. The PHP engine

??? success "Answer Q24"
    **A**

    Protocol negotiation happens at the TLS/web-server layer (ALPN). PHP only observes the negotiated version via $request->getProtocolVersion().

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

**Q25.** In a Symfony 8 app, HTTP/2 server push is the recommended way to preload sub-resources and 103 Early Hints should be avoided. True or false?  <small>_(medium · true-false)_</small>

- A. False
- B. True

??? success "Answer Q25"
    **A**

    It is the reverse. HTTP/2 server push is effectively dead — browsers have dropped support — and the modern replacement for hinting sub-resources is the 103 Early Hints informational response. The claim also mislocates the decision: push/version selection is a web-server concern, not a PHP one.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103)

**Q26.** On a keep-alive connection, why is the first request typically slower than the ones that follow it? (choose one)  <small>_(medium · scenario)_</small>

- A. It pays for DNS resolution plus the TCP and TLS handshakes before any HTTP byte flows; later requests reuse the warm connection
- B. PHP compiles the controller only on the first request
- C. The first request always uses HTTP/1.1 and later ones upgrade to HTTP/2
- D. The server caches the response body after the first hit

??? success "Answer Q26"
    **A**

    The first exchange must complete DNS → TCP 3-way handshake → TLS handshake before the HTTP request is even sent. Subsequent requests on the same keep-alive (HTTP/1.1) or multiplexed (HTTP/2/3) connection skip that setup. The HTTP version is fixed for the life of the connection, and body caching is a separate concern.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)

**Q27.** A POST must be redirected while preserving its method and body. Which status code? (choose one)  <small>_(medium · single)_</small>

- A. 307 Temporary Redirect
- B. 301 Moved Permanently
- C. 302 Found
- D. 303 See Other

??? success "Answer Q27"
    **A**

    307 (temporary) and 308 (permanent) preserve method and body; 301/302 may switch to GET, and 303 forces GET.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/307)

**Q28.** A rate limit is exceeded. Which status code and companion header are correct? (choose one)  <small>_(medium · single)_</small>

- A. 429 Too Many Requests with Retry-After
- B. 403 Forbidden with WWW-Authenticate
- C. 503 Service Unavailable with Allow
- D. 409 Conflict with Location

??? success "Answer Q28"
    **A**

    429 signals rate limiting; Retry-After advertises when the client may try again.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429)

**Q29.** You issue a 302 (instead of 303) after a successful POST. What is the real-world risk? (choose one)  <small>_(medium · trap)_</small>

- A. Some clients may re-issue the request as POST, causing a duplicate submission
- B. The browser will refuse the redirect entirely
- C. The body is always stripped, so nothing can go wrong
- D. The response becomes uncacheable

??? success "Answer Q29"
    **A**

    302's method-handling is historically ambiguous, so a client may repeat the POST on the redirect. 303 See Other is unambiguous: it forces a GET to the target, implementing Post/Redirect/Get and preventing resubmission on refresh. 307 would also preserve POST — the opposite of what you want here.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/303)

**Q30.** Which status codes preserve the original request method and body when redirecting? (choose 2)  <small>_(medium · multiple)_</small>

- A. 307 Temporary Redirect
- B. 308 Permanent Redirect
- C. 302 Found
- D. 303 See Other

??? success "Answer Q30"
    **A, B**

    307 (temporary) and 308 (permanent) are the method-and-body-preserving redirects. 302 may be downgraded to GET by clients and 303 always forces GET, so neither is safe when a non-GET method must survive the redirect.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/308)

**Q31.** Which class backs $request->query, $request->request and $request->cookies? (choose one)  <small>_(medium · single)_</small>

- A. InputBag
- B. ParameterBag
- C. HeaderBag
- D. ServerBag

??? success "Answer Q31"
    **A**

    query, request and cookies are InputBag (scalar-restricted); attributes is a plain ParameterBag, server is ServerBag, headers is HeaderBag.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

**Q32.** Which method reads the submitted body regardless of JSON vs form content type? (choose one)  <small>_(medium · single)_</small>

- A. $request->getPayload()
- B. $request->getContent()
- C. $request->query->all()
- D. $request->getContentTypeFormat()

??? success "Answer Q32"
    **A**

    getPayload() returns an InputBag from the parsed body (decoding JSON or reading form data); getContent() returns the raw unparsed body string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#accessing-request-data)

**Q33.** Which method reports the request format derived from the body's Content-Type header in Symfony 8? (choose one)  <small>_(medium · trap)_</small>

- A. getContentTypeFormat()
- B. getContentType()
- C. getRequestFormat()
- D. getPreferredFormat()

??? success "Answer Q33"
    **A**

    getContentType() was removed; the current method is getContentTypeFormat(), which maps the incoming Content-Type to a Symfony format (e.g. 'json'). getRequestFormat() reads the _format attribute, and getPreferredFormat() negotiates from the client's Accept header — different concerns entirely.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q34.** Which Response class streams an on-disk file and supports HTTP range requests? (choose one)  <small>_(medium · single)_</small>

- A. BinaryFileResponse
- B. Response
- C. JsonResponse
- D. RedirectResponse

??? success "Answer Q34"
    **A**

    BinaryFileResponse streams a file without buffering it in memory and supports Range requests and X-Sendfile.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#serving-files)

**Q35.** What does Response::prepare() do? (choose one)  <small>_(medium · single)_</small>

- A. Makes the response compliant with the request (charset, body for HEAD/304, protocol version)
- B. Sends the headers and body to the client
- C. Validates that the status code is in range
- D. JSON-encodes the content

??? success "Answer Q35"
    **A**

    prepare() normalises the response against the incoming Request; send() (sendHeaders + sendContent) actually transmits it.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q36.** In Symfony 8, where does the makeDisposition() helper for a Content-Disposition header live? (choose one)  <small>_(medium · trap)_</small>

- A. Symfony\Component\HttpFoundation\HeaderUtils::makeDisposition()
- B. ResponseHeaderBag::makeDisposition()
- C. Response::makeDisposition()
- D. BinaryFileResponse::makeDisposition()

??? success "Answer Q36"
    **A**

    makeDisposition() now lives on HeaderUtils; the old ResponseHeaderBag::makeDisposition() was removed. For file responses you can also use BinaryFileResponse::setContentDisposition(), which delegates to the same logic — but the static helper itself is on HeaderUtils.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#serving-files)

**Q37.** You must serve a 2 GB file for download without exhausting memory. Which approach is correct? (choose one)  <small>_(medium · scenario)_</small>

- A. Return a BinaryFileResponse (or StreamedResponse) so the bytes are streamed, not buffered
- B. Return new Response(file_get_contents($path))
- C. Base64-encode the file into a JsonResponse
- D. Increase memory_limit and use a plain Response

??? success "Answer Q37"
    **A**

    new Response(file_get_contents(...)) loads the whole file into memory and will exhaust it. BinaryFileResponse streams a file already on disk (and adds Range and X-Sendfile support), while StreamedResponse streams generated output. Both keep memory flat regardless of size.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#serving-files)

**Q38.** By default in Symfony 8, is the _method parameter honoured? (choose one)  <small>_(medium · single)_</small>

- A. No — http_method_override defaults to false and must be enabled
- B. Yes, always
- C. Only for GET requests
- D. Only for JSON requests

??? success "Answer Q38"
    **A**

    You must enable framework.http_method_override (or call Request::enableHttpMethodParameterOverride()); it applies to POST only.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/routing.html)

**Q39.** After a successful method override, what does getRealMethod() return for a POST+_method=PUT request? (choose one)  <small>_(medium · single)_</small>

- A. POST
- B. PUT
- C. GET
- D. An empty string

??? success "Answer Q39"
    **A**

    getMethod() returns the overridden verb (PUT) while getRealMethod() returns the raw transport method (POST).

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q40.** Which configuration enables the _method override on POST forms? (choose one)  <small>_(medium · config)_</small>

- A. framework:
    http_method_override: true
- B. framework:
    method_override: true
- C. framework:
    router:
        method_override: true
- D. framework:
    request:
        enable_method: true

??? success "Answer Q40"
    **A**

    The key is framework.http_method_override (default false). It makes Symfony honour a _method field (or X-HTTP-Method-Override header) on POST requests, rewriting the method to PUT/PATCH/DELETE. The other keys do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#http-method-override)

**Q41.** The Symfony Cookie object is immutable. What does Cookie::create('a')->withValue('b') require? (choose one)  <small>_(medium · trap)_</small>

- A. Using the returned instance — with* returns a new Cookie
- B. Nothing; it mutates the original in place
- C. Calling save() afterwards
- D. Passing the value to the constructor only

??? success "Answer Q41"
    **A**

    Cookie is immutable; every with* method returns a new instance, so the result must be captured or the change is lost.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Cookie.php)

**Q42.** Which framework configuration sets the session cookie's SameSite policy to Lax and hides it from JavaScript? (choose one)  <small>_(medium · config)_</small>

- A. framework:
    session:
        cookie_samesite: lax
        cookie_httponly: true
- B. framework:
    cookie:
        samesite: lax
        httponly: true
- C. framework:
    session:
        samesite: lax
        httponly: true
- D. framework:
    session:
        cookie: { samesite: lax }

??? success "Answer Q42"
    **A**

    Session cookie behaviour is configured under framework.session with the cookie_* keys: cookie_samesite (strict|lax|none), cookie_httponly, and cookie_secure (often 'auto'). Symfony's defaults are already HttpOnly: true and SameSite: lax. The other key shapes do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#cookie-samesite)

**Q43.** The s-maxage directive applies to: (choose one)  <small>_(medium · single)_</small>

- A. shared caches (proxies/CDN) only
- B. the browser cache only
- C. both equally
- D. nothing unless ESI is enabled

??? success "Answer Q43"
    **A**

    s-maxage is honoured only by shared caches and overrides max-age there.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

**Q44.** What does Response::isNotModified($request) do on a validator match? (choose one)  <small>_(medium · single)_</small>

- A. Returns true and turns the response into a bodyless 304
- B. Returns a full 200 response
- C. Returns a 412 Precondition Failed
- D. Only reads headers without changing the response

??? success "Answer Q44"
    **A**

    It compares the request's conditional headers and, on a match, sets the status to 304 and removes the body.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q45.** Which statement correctly contrasts freshness and validation caching? (choose one)  <small>_(medium · trap)_</small>

- A. Freshness (max-age) can serve with no request; validation (ETag/Last-Modified) always sends a conditional request that may return 304
- B. Validation avoids the request while fresh; freshness always revalidates
- C. Both always contact the server on every request
- D. ETag is a freshness header and max-age is a validation header

??? success "Answer Q45"
    **A**

    Freshness uses Cache-Control: max-age/s-maxage (and Expires); while fresh the cache answers with zero round-trips. Validation uses ETag/If-None-Match and Last-Modified/If-Modified-Since — it always asks, but the server can reply 304 Not Modified with no body. The models are complementary, not interchangeable.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/validation.html)

**Q46.** Which attribute declaratively marks a controller's response public and cacheable for one hour in shared and private caches? (choose one)  <small>_(medium · config)_</small>

- A. #[Cache(public: true, maxage: 3600, smaxage: 3600)]
- B. #[HttpCache(ttl: 3600)]
- C. #[Cacheable(3600)]
- D. #[Route(cache: 3600)]

??? success "Answer Q46"
    **A**

    Symfony\\Component\\HttpKernel\\Attribute\\Cache exposes public, maxage, smaxage, expires, etag and lastModified. #[Cache(public: true, maxage: 3600, smaxage: 3600)] sets Cache-Control: public, max-age=3600, s-maxage=3600. The other attributes do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html#introducing-http-caching)

**Q47.** A default Symfony Response is storable by a shared cache (CDN/proxy) out of the box. True or false?  <small>_(medium · true-false)_</small>

- A. False
- B. True

??? success "Answer Q47"
    **A**

    A default response carries Cache-Control: no-cache, private, so shared caches will not store it. You must opt in with setPublic()/setSharedMaxAge() (or #[Cache(public: true)]). Marking user-specific responses public would leak data across users.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache.html)

**Q48.** getPreferredLanguage(['en','de']) returns: (choose one)  <small>_(medium · single)_</small>

- A. the best of en/de for this client
- B. the client's overall top language
- C. always en
- D. all acceptable languages

??? success "Answer Q48"
    **A**

    With a whitelist it intersects the client's ordered languages with your supported list and returns the best match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q49.** What does getAcceptableContentTypes() return? (choose one)  <small>_(medium · single)_</small>

- A. MIME types ordered by client preference
- B. Symfony format names
- C. locales
- D. content encodings

??? success "Answer Q49"
    **A**

    It returns raw MIME types best-first; getPreferredFormat() returns Symfony format names.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q50.** A proxy sometimes serves the JSON representation of /articles/7 to a browser expecting HTML. What is the most likely fix? (choose one)  <small>_(medium · debug)_</small>

- A. Add Vary: Accept (via $response->setVary(['Accept'])) so the cache keys each representation separately
- B. Set Cache-Control: private so the proxy never caches
- C. Send the Accept header on the response
- D. Switch to getRequestFormat() in the controller

??? success "Answer Q50"
    **A**

    Without Vary, a shared cache stores one entry for the URL and may replay the wrong representation. setVary(['Accept']) tells caches the response varies by the Accept header, so each variant is stored separately. Marking it private would just disable caching; Accept is a request header, not a response one.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary)

**Q51.** What is the safe way to pick a locale from the browser's Accept-Language? (choose one)  <small>_(medium · single)_</small>

- A. getPreferredLanguage(['en','fr']) with a whitelist
- B. getLocale()
- C. getLanguages()[0]
- D. reading $_SERVER['HTTP_ACCEPT_LANGUAGE']

??? success "Answer Q51"
    **A**

    The whitelist form guarantees a supported locale; the others may return one you do not support.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html#the-locale-used-in-translations)

**Q52.** What sets the request locale when a route defines {_locale}? (choose one)  <small>_(medium · single)_</small>

- A. LocaleListener calls Request::setLocale() on kernel.request
- B. The Router sets it directly
- C. Twig sets it during rendering
- D. The Translator sets it

??? success "Answer Q52"
    **A**

    LocaleListener reads the _locale attribute and calls setLocale(); LocaleAwareListener then propagates it to LocaleAware services.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleListener.php)

**Q53.** Which configuration makes Symfony guess the request locale from Accept-Language automatically, bounded to en and fr, with no custom listener? (choose one)  <small>_(medium · config)_</small>

- A. framework:
    enabled_locales: ['en', 'fr']
    set_locale_from_accept_language: true
- B. framework:
    default_locale: en|fr
    detect_locale: true
- C. framework:
    translator:
        accept_language: true
- D. framework:
    locale_from_header: true

??? success "Answer Q53"
    **A**

    set_locale_from_accept_language: true tells Symfony to set the request locale from Accept-Language when no _locale is present, constrained to enabled_locales. No custom kernel.request listener is needed. The other keys do not exist.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/reference/configuration/framework.html#set-locale-from-accept-language)

**Q54.** The browser sends Accept-Language: es, en;q=0.8 and the app supports only ['en','fr']. What does getPreferredLanguage(['en','fr']) return? (choose one)  <small>_(medium · scenario)_</small>

- A. en — es is unsupported, so the next acceptable option in the whitelist (en, q=0.8) wins
- B. es — the client's top choice always wins
- C. fr — the first entry of the whitelist is always returned
- D. null — no exact match exists

??? success "Answer Q54"
    **A**

    getPreferredLanguage intersects the client's ordered languages with your whitelist. es is not supported, so it is skipped; en (q=0.8) is the best remaining acceptable option and is returned. With a whitelist it never returns an unsupported locale, and it falls back to the first list entry only if none match.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q55.** Why is calling getPreferredLanguage() with no argument risky for locale detection? (choose one)  <small>_(medium · trap)_</small>

- A. It returns the client's top language unfiltered, which may be a locale you do not support (e.g. pt-BR)
- B. It always throws when Accept-Language is present
- C. It ignores the Accept-Language header entirely
- D. It returns an array instead of a string

??? success "Answer Q55"
    **A**

    Without a whitelist, getPreferredLanguage() returns the client's single highest-ranked language regardless of what your app supports, so you may get an unsupported locale and break translations/routing. Always pass your supported list so the result is bounded.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/translation.html#the-locale-used-in-translations)

**Q56.** When is an HttpClient request actually performed? (choose one)  <small>_(medium · single)_</small>

- A. Lazily, on first read of status/headers/content
- B. Immediately when request() is called
- C. Only when stream() is called
- D. When the kernel terminates

??? success "Answer Q56"
    **A**

    request() returns a lazy ResponseInterface; the transfer completes on first access, which enables free concurrency.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html)

**Q57.** What does ResponseInterface::getContent() do on a 500 response by default? (choose one)  <small>_(medium · single)_</small>

- A. Throws a ServerExceptionInterface
- B. Returns the response body
- C. Returns an empty string
- D. Returns null

??? success "Answer Q57"
    **A**

    By default getContent()/toArray() throw on 3xx/4xx/5xx; pass false (or the throw option) to read the body without throwing. getStatusCode() never throws.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#handling-exceptions)

**Q58.** What does this test assert? $client = new MockHttpClient(new MockResponse('{"id":42}')); $data = $client->request('GET', 'https://api.test/x')->toArray(); (choose one)  <small>_(medium · code)_</small>

- A. $data === ['id' => 42], produced from the canned body with no network call
- B. It performs a real GET to api.test and decodes the live body
- C. It throws because MockResponse needs an explicit http_code
- D. $data is the raw JSON string '{"id":42}'

??? success "Answer Q58"
    **A**

    MockHttpClient serves the supplied MockResponse without any network; toArray() JSON-decodes the body to ['id' => 42]. MockResponse defaults to HTTP 200, so no exception is thrown, and toArray() returns an array, not the raw string.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#testing)

**Q59.** Which framework configuration defines a scoped client that prefixes a base URI and bearer token for one API? (choose one)  <small>_(medium · config)_</small>

- A. framework:
    http_client:
        scoped_clients:
            github.client:
                base_uri: 'https://api.github.com/'
                auth_bearer: '%env(GITHUB_TOKEN)%'
- B. framework:
    http_client:
        clients:
            github: { url: 'https://api.github.com/' }
- C. framework:
    clients:
        github.client:
            base_uri: 'https://api.github.com/'
- D. services:
    github.client:
        base_uri: 'https://api.github.com/'

??? success "Answer Q59"
    **A**

    Scoped clients are declared under framework.http_client.scoped_clients; each named entry (e.g. github.client) applies its base_uri, headers and auth only to matching URLs. The framework registers a service you autowire by variable name ($githubClient). The other shapes are invalid.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#scoping-client)

**Q60.** Which of the following statements are true about HTTP methods? (select all that apply)  <small>_(medium · multiple)_</small>

- A. PUT and DELETE are idempotent but not safe
- B. GET and HEAD are the methods that are cacheable by default
- C. The _method override only applies to POST requests and is disabled by default
- D. POST is idempotent, so repeating it is always harmless
- E. Request::getMethod() returns the raw method and ignores any method override

??? success "Answer Q60"
    **A, B, C**

    Safe methods are a subset of idempotent ones: PUT/DELETE change state but repeating them yields the same result, and only GET/HEAD are cacheable by default. The _method override requires http_method_override to be enabled and only fires on POST. POST (like PATCH) is neither safe nor idempotent, and getMethod() is the override-aware effective method — getRealMethod() returns the raw one.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#identifying-a-request)

**Q61.** Which of the following statements are true about HTTP status codes? (select all that apply)  <small>_(medium · multiple)_</small>

- A. 307 and 308 redirects preserve the original request method and body
- B. A 303 See Other redirect always forces the follow-up request to use GET
- C. 401 means the user is authenticated but lacks permission for the resource
- D. 422 Unprocessable Entity is meant for syntactically malformed requests
- E. Response::setStatusCode() accepts any integer, including 999

??? success "Answer Q61"
    **A, B**

    307/308 are the method-preserving redirects (unlike 301/302, which user agents may rewrite to GET), and 303 explicitly forces GET — the classic POST/redirect/GET pattern. 401 means unauthenticated (403 is the not-authorized case), 422 targets well-formed but semantically invalid requests (malformed syntax is 400), and setStatusCode() throws for codes outside 100–599.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#response)

**Q62.** Which of the following statements are true about cookies in Symfony/HTTP? (select all that apply)  <small>_(medium · multiple)_</small>

- A. A cookie with SameSite=None must also be marked Secure, or browsers drop it
- B. The Symfony Cookie object is immutable — each with*() call returns a new instance
- C. Omitting both Expires and Max-Age produces a session cookie deleted when the browser closes
- D. clearCookie() deletes the cookie no matter which path/domain it was set with
- E. Symfony session cookies default to SameSite=Strict

??? success "Answer Q62"
    **A, B, C**

    SameSite=None is only valid together with Secure; the immutable Cookie API means forgetting to reassign a with*() result is a silent no-op; and without Expires/Max-Age the cookie only lives for the browser session. clearCookie() must match the original path/domain or the cookie survives, and Symfony's session cookie defaults are HttpOnly: true with SameSite=Lax, not Strict.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#setting-cookies)

**Q63.** An app sits behind a TLS-terminating reverse proxy that forwards X-Forwarded-Proto: https, yet $request->isSecure() returns false. What is the most likely cause? (choose one)  <small>_(hard · trap)_</small>

- A. Trusted proxies were not declared, so Symfony ignores X-Forwarded-* headers
- B. isSecure() only reads getScheme(), which is always http
- C. isSecure() requires HTTP/2 to return true
- D. PHP terminated TLS but did not tell Symfony

??? success "Answer Q63"
    **A**

    For security, Symfony trusts X-Forwarded-* (including -Proto) only from proxies registered via Request::setTrustedProxies() (or framework.trusted_proxies). Until then isSecure() reflects the direct connection (plain HTTP from the proxy) and returns false. PHP never terminates TLS; the edge does.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/deployment/proxies.html)

**Q64.** You call new Response('', Response::HTTP_CREATED) without a reason phrase. How does Symfony fill the reason phrase? (choose one)  <small>_(hard · internals)_</small>

- A. setStatusCode() looks the code up in the public static Response::$statusTexts map
- B. It queries the web server for the canonical phrase
- C. It always leaves the reason phrase empty
- D. It reads the phrase from the HTTP_* constant name

??? success "Answer Q64"
    **A**

    Response::$statusTexts is a public static array mapping each known code to its reason phrase; setStatusCode() consults it when no explicit text is supplied. An unknown code simply yields an empty phrase (still valid). The HTTP_* constants are plain integers and carry no text themselves.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q65.** What happens when you call $response->setStatusCode(600)? (choose one)  <small>_(hard · code)_</small>

- A. It throws \InvalidArgumentException because the code is outside 100–599
- B. It silently clamps the value to 599
- C. It stores 600 with an empty reason phrase
- D. It returns false

??? success "Answer Q65"
    **A**

    setStatusCode() validates that the code is within the HTTP range 100–599 and throws \\InvalidArgumentException otherwise — a common gotcha when a code is computed dynamically. It neither clamps nor stores out-of-range values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Response.php)

**Q66.** Why does InputBag (query/request/cookies) reject reading an array where a scalar is expected? (choose one)  <small>_(hard · internals)_</small>

- A. InputBag restricts values to scalars/arrays-of-scalars/null and throws BadRequestException on a type mismatch, hardening against malicious nested input
- B. PHP forbids arrays in $_GET
- C. ParameterBag also throws in the same case
- D. It silently casts the array to its first element

??? success "Answer Q66"
    **A**

    InputBag extends ParameterBag but narrows the contract to user-supplied data: get() accepts only scalars/null and raises a BadRequestException (HTTP 400) when handed an unexpected array, blocking parameter-pollution style attacks. A plain ParameterBag (used by attributes) imposes no such restriction. Use all('key') to intentionally read array values.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/InputBag.php)

**Q67.** A request handler crashes with a TypeError only when the X-Trace-Id header is absent, on the line strtoupper($request->headers->get('X-Trace-Id')). What is the cause and fix? (choose one)  <small>_(hard · debug)_</small>

- A. HeaderBag::get() returns null for a missing key; guard with ?? or supply a default before calling a string function
- B. get() throws when the header is missing; wrap it in try/catch
- C. Headers are only readable via $_SERVER; the bag is empty
- D. get() returns an empty array, breaking strtoupper()

??? success "Answer Q67"
    **A**

    HeaderBag::get(string $key, mixed $default = null) returns null when the key is absent — a normal lookup miss, not an error. Passing null to strtoupper() triggers the TypeError. Guard with $request->headers->get('X-Trace-Id') ?? '' or pass a default. Typed InputBag getters (getString etc.) coalesce to a zero value, but HeaderBag::get() is nullable.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/HeaderBag.php)

**Q68.** You create new Response('hi') and set no cache headers. What Cache-Control does ResponseHeaderBag emit by default? (choose one)  <small>_(hard · internals)_</small>

- A. no-cache, private
- B. public, max-age=0
- C. no-store
- D. no header is sent at all

??? success "Answer Q68"
    **A**

    When you set no cache directives, ResponseHeaderBag computes a sensible default of 'no-cache, private', so a bare response is never stored by shared caches. Calling setPublic()/setMaxAge()/setSharedMaxAge() changes this. It is not 'no-store', and a Cache-Control header is always present.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

**Q69.** A candidate claims PATCH is always idempotent like PUT. Why is this wrong? (choose one)  <small>_(hard · trap)_</small>

- A. PATCH applies a partial change that may differ when repeated (e.g. an increment delta), so it is generally not idempotent
- B. PATCH is safe, so idempotency is irrelevant
- C. PATCH is never allowed to have a body
- D. PATCH and PUT are identical in every respect

??? success "Answer Q69"
    **A**

    PUT replaces a resource wholesale, so sending the same body twice leaves the same state (idempotent). PATCH describes a partial modification; a delta such as 'add 1' applied twice yields a different result, so PATCH is generally not idempotent. Neither PATCH nor PUT is safe — both change state.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH)

**Q70.** What are the exact conditions under which Symfony applies the method override? (choose one)  <small>_(hard · internals)_</small>

- A. Only on a POST request, only when enabled, and only to the values PUT, PATCH or DELETE
- B. On any request whenever a _method field is present
- C. On GET and POST, to any value including GET
- D. Automatically for all JSON requests

??? success "Answer Q70"
    **A**

    The override fires only when http_method_override is enabled, only on a POST transport request, and rewrites the method solely to PUT/PATCH/DELETE. Other transports are never rewritten, which is why getRealMethod() still reports POST.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q71.** A cookie set with Path=/app and Domain=.example.com is not deleted by $response->headers->clearCookie('session'). Why? (choose one)  <small>_(hard · debug)_</small>

- A. clearCookie() defaults to path '/' and no domain, so the expiry targets a different scope and the original survives
- B. clearCookie() cannot delete HttpOnly cookies
- C. Cookies can only be deleted client-side via JavaScript
- D. You must call setCookie() with an empty value instead

??? success "Answer Q71"
    **A**

    A browser keys cookies by name plus path plus domain. clearCookie() emits a past-dated Set-Cookie, but with its default path '/' and no domain it does not match the original (Path=/app, Domain=.example.com), so the browser expires a non-existent cookie and keeps the real one. Fix: clearCookie('session', '/app', '.example.com').

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/ResponseHeaderBag.php)

**Q72.** What does the __Host- cookie name prefix force the browser to require? (choose one)  <small>_(hard · internals)_</small>

- A. Secure, no Domain attribute, and Path=/ — the strictest scoping the browser enforces
- B. HttpOnly and SameSite=Strict only
- C. A matching Domain attribute and Max-Age
- D. Nothing; the prefix is purely cosmetic

??? success "Answer Q72"
    **A**

    A cookie named __Host-... is accepted only if it is Secure, has no Domain attribute (so it is locked to the exact host), and uses Path=/. This is the strongest same-origin scoping the browser guarantees, preventing subdomain injection. The related __Secure- prefix only requires the Secure flag.

    :material-book-open-variant: [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#cookie_prefixes)

**Q73.** To cache a public page in a CDN for 10 minutes without letting the browser cache it long-term, which setter do you use? (choose one)  <small>_(hard · internals)_</small>

- A. setSharedMaxAge(600) (plus setPublic()), which emits s-maxage honoured only by shared caches
- B. setMaxAge(600), which targets shared caches only
- C. setPrivate(), which enables CDN caching
- D. setExpires(), which only affects the browser

??? success "Answer Q73"
    **A**

    setSharedMaxAge() writes s-maxage, obeyed only by shared caches (CDN/proxy) and it implies public. setMaxAge() targets any cache including the browser, so it is the wrong tool here. setPrivate() would forbid shared caching entirely.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_cache/expiration.html)

**Q74.** What is the key difference between getPreferredFormat() and getAcceptableContentTypes()? (choose one)  <small>_(hard · trap)_</small>

- A. getPreferredFormat() returns a Symfony format name (e.g. 'json'); getAcceptableContentTypes() returns raw MIME types
- B. They are aliases returning the same value
- C. getPreferredFormat() returns MIME types; getAcceptableContentTypes() returns formats
- D. getPreferredFormat() reads Accept-Language, not Accept

??? success "Answer Q74"
    **A**

    getPreferredFormat() maps the client's Accept header to a short Symfony format (html, json, xml, csv...), best for a match expression. getAcceptableContentTypes() returns the raw MIME strings ordered by preference. Confusing format names with MIME types is a classic trap.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/Request.php)

**Q75.** Given AcceptHeader::fromString('text/html;q=0.9, application/json;q=1.0'), what does $accept->first()?->getQuality() return? (choose one)  <small>_(hard · code)_</small>

- A. 1.0 — first() returns the highest-quality item (application/json)
- B. 0.9 — items are returned in string order
- C. null — first() only works on a single-value header
- D. true — first() returns a boolean like has()

??? success "Answer Q75"
    **A**

    AcceptHeader parses and sorts items by quality (descending), so first() returns the AcceptHeaderItem for application/json (q=1.0) and getQuality() gives 1.0. The nullsafe operator guards the empty-header case where first() would return null.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpFoundation/AcceptHeader.php)

**Q76.** How does getRequestFormat() differ from getPreferredFormat()? (choose one)  <small>_(hard · internals)_</small>

- A. getRequestFormat() returns the format from the _format attribute (e.g. a route suffix); getPreferredFormat() negotiates from the client's Accept header
- B. They both read the Accept header
- C. getRequestFormat() reads Accept; getPreferredFormat() reads _format
- D. getRequestFormat() returns a MIME type, getPreferredFormat() a locale

??? success "Answer Q76"
    **A**

    getRequestFormat(?string $default = 'html') returns the format stored in the _format request attribute (set e.g. by a /path.{_format} route), while getPreferredFormat() computes the best format from the client's Accept header. Mixing the two is a common mistake.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html)

**Q77.** After the request locale is set, how does it reach services like the Translator? (choose one)  <small>_(hard · internals)_</small>

- A. LocaleAwareListener pushes it into every service implementing LocaleAwareInterface
- B. Each service reads $_SERVER['HTTP_ACCEPT_LANGUAGE'] itself
- C. Twig broadcasts it during template rendering
- D. The Router injects it into the container parameters

??? success "Answer Q77"
    **A**

    LocaleListener sets the request locale; LocaleAwareListener then calls setLocale() on every service tagged/implementing Symfony\\Contracts\\Translation\\LocaleAwareInterface (e.g. the Translator). For a scoped switch you use LocaleSwitcher. Services do not read superglobals.

    :material-book-open-variant: [Docs](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/EventListener/LocaleAwareListener.php)

**Q78.** Reading each response's getContent() inside the loop that fires the requests makes the batch slow. Why? (choose one)  <small>_(hard · debug)_</small>

- A. Reading the body blocks until that transfer completes, so requests run sequentially instead of concurrently
- B. getContent() opens a second connection per call
- C. request() is synchronous, so the loop cannot help
- D. toArray() must be used to enable concurrency

??? success "Answer Q78"
    **A**

    request() is lazy/async: firing them all first lets transfers overlap. But calling getContent() on a response forces that transfer to finish before the next request() runs, serialising the batch. Fire all requests first, then read (or iterate $client->stream($responses)) to keep concurrency.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#concurrent-requests)

**Q79.** You call toArray() on a 204 No Content response (empty body). What happens? (choose one)  <small>_(hard · trap)_</small>

- A. It throws a JsonException because an empty string is not valid JSON — guard by checking the status/empty body first
- B. It returns null for the empty body
- C. It returns an empty array []
- D. It returns the empty string ''

??? success "Answer Q79"
    **A**

    getContent() on an empty body returns '' (not null), but toArray() tries to JSON-decode that '' and throws JsonException. There is no silent null. Guard with a 204/empty check before decoding, e.g. if (204 === $r->getStatusCode() || '' === $r->getContent(false)) return [];.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html#processing-responses)

**Q80.** Which of the following statements are true about the Symfony Request object and its parameter bags? (select all that apply)  <small>_(hard · multiple)_</small>

- A. Route parameters are stored in the attributes bag, not in query
- B. query, request and cookies are InputBag instances, while attributes is a ParameterBag
- C. getPayload() reads the request body regardless of its content type
- D. $request->request contains the $_GET query-string parameters
- E. getContentType() is the current method for reading the request's format

??? success "Answer Q80"
    **A, B, C**

    Route/application data lives in attributes (a ParameterBag), while the user-input bags query/request/cookies are scalar-only InputBag instances, and getPayload() is the content-type-agnostic body reader. $request->request maps to the $_POST body (query maps to $_GET), and getContentType() was removed in favour of getContentTypeFormat().

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#request)

**Q81.** Which of the following statements are true about the Symfony Response object? (select all that apply)  <small>_(hard · multiple)_</small>

- A. prepare() strips the body for HEAD requests and for 204/304 responses
- B. A freshly created Response gets Cache-Control: no-cache, private by default
- C. send() delegates to sendHeaders() and then sendContent()
- D. $response->headers is a plain HeaderBag with no special cookie handling
- E. makeDisposition() is a method on ResponseHeaderBag

??? success "Answer Q81"
    **A, B, C**

    prepare() normalises the response against the request — including removing the body for HEAD/204/304 — the conservative default Cache-Control is no-cache, private, and send() is sendHeaders() followed by sendContent(). $response->headers is actually a ResponseHeaderBag that manages cookies and normalises Cache-Control, and makeDisposition() lives on HeaderUtils.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#response)

**Q82.** Which of the following statements are true about HTTP content negotiation? (select all that apply)  <small>_(hard · multiple)_</small>

- A. A q=0 quality value in an Accept header means that representation is unacceptable
- B. getPreferredLanguage($locales) returns the best match within the list you pass, not just the client's top language
- C. getPreferredFormat() returns a raw MIME type string such as application/json
- D. Shared caches parse the Accept header themselves, so a Vary header is unnecessary on negotiated responses
- E. Response gzip compression should normally be implemented inside your PHP controllers

??? success "Answer Q82"
    **A, B**

    q=0 explicitly marks a representation as unacceptable rather than merely low priority, and getPreferredLanguage() intersects the client's preferences with the locale list you provide. getPreferredFormat() maps Accept to a Symfony format name (json, html) — raw MIME types come from getAcceptableContentTypes() — negotiated responses must send Vary or shared caches will mis-serve, and gzip is typically handled by the web server/proxy.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/components/http_foundation.html#accessing-accept-headers)

**Q83.** Which of the following statements are true about the Symfony HttpClient component? (select all that apply)  <small>_(hard · multiple)_</small>

- A. request() is lazy/asynchronous — the transfer only completes when you first read the status, headers or content
- B. getContent() and toArray() throw on 3xx–5xx responses by default, while getStatusCode() never throws
- C. MockHttpClient with MockResponse lets you test HTTP interactions without any network access
- D. You should type-hint the concrete CurlHttpClient class in your services for best performance
- E. Options defined on a scoped client apply to every request the client makes, whatever the URL

??? success "Answer Q83"
    **A, B, C**

    Responses are lazy so firing several requests before reading gives free concurrency; the content readers throw HTTP exceptions by default (pass false / throw: false to read error bodies) while getStatusCode() is always safe; and MockHttpClient keeps tests offline. You should depend on the HttpClientInterface contract, not a concrete transport, and scoped-client options only apply to URLs matching the scope/base URI.

    :material-book-open-variant: [Docs](https://symfony.com/doc/8.0/http_client.html)

**Q84.** A teammate cites 'RFC 7231' to justify a status-code semantics decision in a Symfony 8 review. What is the accurate correction?  <small>_(hard · trap)_</small>

- A. RFC 7231 was obsoleted by RFC 9110, which now defines HTTP semantics (methods, status codes, headers)
- B. RFC 7231 is still current; RFC 9110 only covers HTTP/2
- C. RFC 7231 was replaced by RFC 9111, which covers all of HTTP semantics
- D. RFC 7231 was merged into RFC 9112, the wire-format spec

??? success "Answer Q84"
    **A**

    In 2022, RFC 9110 (HTTP Semantics) replaced RFC 7231/7232/7233/7235/7538. Wire format became RFC 9112 (HTTP/1.1), and caching became its own document, RFC 9111 — semantics and caching are deliberately separate specs, and neither citation should still point at the 2014 RFCs.

    :material-book-open-variant: [Docs](https://www.rfc-editor.org/rfc/rfc9110.html)

---

<small>Back to [Chapter Exams](index.md) · [HTTP](../http/index.md)</small>
