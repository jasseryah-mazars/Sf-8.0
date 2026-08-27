# Revision Sheet — HTTP

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [HTTP](../../http/index.md).

## Caching Overview
- Two models: expiration (freshness) and validation.
- Freshness = `Cache-Control`/`Expires`; validation = `ETag`/`Last-Modified`.
- `public`/`private` and `s-maxage` control shared caches.
- Depth lives in the HTTP Caching stage.

**Cheat:** Fresh → no request. Validate → conditional GET → maybe **304**. `setMaxAge` (browser), `setSharedMaxAge` (CDN), `setPublic/Private`. `setEtag` + `isNotModified($request)` → 304. Full stage: `../http-caching/`.

## Client / Server Interaction
- A page load is many independent request/response pairs over DNS→TCP→TLS→HTTP.
- Symfony wraps the raw exchange in `Request`/`Response`; `Response::send()`
  writes it back.
- HTTP/2 multiplexes; HTTP/3 uses QUIC; server push is dead — use Early Hints.
- HTTP is stateless — cookies/sessions add state.

**Cheat:** Ports: HTTP **80**, HTTPS **443**. Scheme via `getScheme()`, version via `getProtocolVersion()`. Cycle: DNS → TCP → TLS → HTTP request → front controller → Response → send. HTTP/2 = binary + multiplex + HPACK; HTTP/3 = QUIC/UDP; push deprecated. Client IP behind a proxy → `setTrustedProxies()` + `getClientIp()`.

## Content Negotiation
- Client advertises `Accept*` with `q` values; server picks and echoes
  `Content-*`.
- `getPreferredFormat()` → format; `getAcceptableContentTypes()` → MIME types;
  `getPreferredLanguage($list)` → best locale.
- `AcceptHeader`/`AcceptHeaderItem` parse any `Accept*` header.
- Always `Vary` negotiated responses; gzip is the proxy's job.

**Cheat:** `Accept`→type, `Accept-Language`→locale, `Accept-Encoding`→compression. `q=0` = unacceptable; higher `q` wins. Formats: `getPreferredFormat`, `getRequestFormat`(`_format`), `getMimeTypes`. Negotiate → set `Vary`.

## Cookies
- Attributes: Domain, Path, Expires/Max-Age, Secure, HttpOnly, SameSite.
- `Cookie` is immutable — chain `with*` and use the result.
- Set via `$response->headers->setCookie()`, delete via `clearCookie()` with
  matching path/domain.
- `SameSite=None` ⇒ must be `Secure`; session default is `Lax`.

**Cheat:** `Cookie::create()->withValue()->withSecure()->withHttpOnly()->withSameSite()`. No expiry ⇒ session cookie. `SameSite=None` needs `Secure`. `clearCookie(name, path, domain)` must match the original scope. Read incoming: `$request->cookies->get('name')`.

## HttpClient Component
- `HttpClientInterface::request()` is lazy/async; concurrency is free.
- `getContent()`/`toArray()` throw on 3xx–5xx by default; `getStatusCode()` never.
- Scoped clients bind base URI/auth to matching hosts.
- `RetryableHttpClient` for resilience; `MockHttpClient` for tests.

**Cheat:** Contract: `HttpClientInterface` / `ResponseInterface`. Factory: `HttpClient::create()`. Options: `json`, `query`, `headers`, `auth_bearer`, `base_uri`, `timeout`. Concurrency: loop `request()`, then `$client->stream($responses)`. Test: `MockHttpClient` + `MockResponse`. Resilience: `RetryableHttpClient`.

## Language Detection
- Sources: `_locale` route param → user pref → `Accept-Language` → default.
- Guess safely with `getPreferredLanguage($whitelist)`.
- `LocaleListener` sets the request locale; `LocaleAwareListener` propagates it.
- Bound locales with `enabled_locales`; set `default_locale`.

**Cheat:** `_locale` attribute → `setLocale()` via `LocaleListener`. `getPreferredLanguage($list)` = safe; no-arg = client top choice. `framework.default_locale`, `enabled_locales`, `set_locale_from_accept_language`. Different languages at one URL ⇒ `Vary: Accept-Language`.

## HTTP Methods
- Safe: GET/HEAD/OPTIONS/TRACE. Idempotent adds PUT/DELETE. POST & PATCH: neither.
- Cacheable by default: GET, HEAD.
- `_method` override is POST-only and **off by default**.
- `getMethod()` = effective; `getRealMethod()` = raw; helper `isMethodSafe()` etc.

**Cheat:** Idempotent = repeat → same state: GET HEAD OPTIONS PUT DELETE. Not idempotent: **POST, PATCH**. Not safe: everything that writes. Override: `framework.http_method_override: true`, POST only, values PUT/PATCH/DELETE. Route match: `#[Route('/x', methods: ['POST'])]`.

## HTTP Request
- `Request` wraps superglobals via `createFromGlobals()`; use bags, never `$_GET`.
- Bags: `query`/`request`/`cookies` = `InputBag`, `attributes` = `ParameterBag`,
  `server` = `ServerBag`, `headers` = `HeaderBag`, `files` = `FileBag`.
- Route params live in `attributes`; typed getters (`getInt`, `getBoolean`) parse.
- `getPayload()` is the content-type-agnostic body reader.

**Cheat:** `query`→GET, `request`→POST body, `attributes`→route/app, `cookies`, `files`, `server`, `headers`. `InputBag` = scalar-only; `getInt/getBoolean/getString/all`. `getMethod()` vs `getRealMethod()`; `getPathInfo()` vs `getRequestUri()`. `getPayload()` reads JSON or form body uniformly; `getContent()` is raw.

## HTTP Response
- Base `Response` + subclasses: `JsonResponse`, `RedirectResponse`,
  `BinaryFileResponse`, `StreamedResponse`.
- `$response->headers` is a `ResponseHeaderBag` (cookies + Cache-Control).
- `prepare()` normalises, `send()` = `sendHeaders()` + `sendContent()`.
- Stream large output; never buffer huge files into memory.

**Cheat:** `new Response($body, $status, $headers)`; default `Cache-Control: no-cache, private`. `JsonResponse::fromJsonString()`, `RedirectResponse(url, 302)`. `BinaryFileResponse` = files on disk (range/X-Sendfile); `StreamedResponse` = generated output. Disposition via `HeaderUtils::makeDisposition()`.

## HTTP Specification (RFC 9110)
- RFC 9110 defines HTTP **semantics** (methods, status codes, headers,
  negotiation, conditional/range requests), independent of HTTP version.
- RFC 9112/9113/9114 define the **wire format** per HTTP version; RFC 9111
  defines **caching** — both separate from RFC 9110.
- Symfony's `Request`/`Response` model the RFC 9110 layer, which is why they
  don't change shape across HTTP/1.1, /2, /3.
- An absent header and an empty header value are distinct under RFC 9110.

**Cheat:** **9110** = Semantics (methods, status, headers, negotiation, conditional/range). **9111** = Caching. **9112** = HTTP/1.1. **9113** = HTTP/2. **9114** = HTTP/3. 9110 replaced 7231/7232/7233/7235/7538 — **not** 7230 (→9112) or 7234 (→9111). Safe / idempotent / cacheable = per-method RFC 9110 properties, not framework rules.

## Status Codes
- 1xx info, 2xx success, 3xx redirect, 4xx client error, 5xx server error.
- 307/308 keep the method; 303 forces GET; 301/308 are permanent (cached).
- 401 = unauthenticated (+`WWW-Authenticate`); 403 = not authorized.
- 404 (maybe later) vs 410 (deliberately gone); 422 validation; 429 rate limit.

**Cheat:** **Redirects:** 301 perm, 302 temp, 303 →GET, 307 temp keep-method, 308 perm keep-method. **Auth:** 401 no creds, 403 no rights. **Missing:** 404 unknown, 410 gone-forever. **API:** 422 validation, 429 rate-limit (+`Retry-After`), 405 (+`Allow`). `Response::$statusTexts[$code]` → reason phrase; `Response::HTTP_*` constants.
