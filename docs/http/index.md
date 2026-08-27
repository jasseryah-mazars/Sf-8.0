# HTTP

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[API Client (MockHttpClient)](../labs/http.md)** — a step-by-step TD with test-first guidance and a reference solution.

The Hypertext Transfer Protocol is the contract every Symfony application speaks.
Before you can reason about the kernel, controllers, security, or caching you must
have an exact mental model of how a **request** becomes a **response** — and how
Symfony's `Symfony\Component\HttpFoundation` and `Symfony\Component\HttpClient`
components turn that protocol into strongly-typed PHP objects.

This stage builds that foundation. Every later stage (Architecture, Controllers,
Routing, Security, HTTP Caching) assumes you already know it cold.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [PHP & Web Security](../php-web-security/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Stage 1 (PHP + threat model) |
    | **Revision priority** | **High** |
    | **Est. time** | 3–4 h |

## Why this stage matters

Symfony is, at heart, a machine that maps `Request → Response`. `HttpKernel`,
routing, controllers, events and caching are all layers on top of the two value
objects `Symfony\Component\HttpFoundation\Request` and
`Symfony\Component\HttpFoundation\Response`. The exam tests protocol details
(status-code semantics, safe/idempotent methods, cookie attributes, content
negotiation) *and* the Symfony API that models them. Get this stage right and the
rest of the syllabus becomes far easier.

## Micro-chapters

Work through them in order:

- [ ] [HTTP Specification (RFC 9110)](rfc-9110.md) — the formal, version-independent
  semantics spec every other chapter in this stage implements a slice of.
- [ ] [Client / Server Interaction](client-server.md) — the request/response
  cycle, TCP/TLS, HTTP/1.1 vs HTTP/2.
- [ ] [Status Codes](status-codes.md) — 1xx–5xx classes and the ones the exam
  loves (301/302/307/308, 401/403, 404/410, 422, 429).
- [ ] [HTTP Request](request.md) — request anatomy mapped to the Symfony
  `Request` bags.
- [ ] [HTTP Response](response.md) — response anatomy mapped to `Response` and
  its subclasses.
- [ ] [HTTP Methods](methods.md) — safe/idempotent semantics and method override.
- [ ] [Cookies](cookies.md) — attributes, the `Cookie` class, setting via the
  response.
- [ ] [Caching Overview](caching.md) — freshness vs validation (overview only).
- [ ] [Content Negotiation](content-negotiation.md) — `Accept*` headers and
  format handling.
- [ ] [Language Detection](language-detection.md) — guessing the user's locale.
- [ ] [HttpClient Component](httpclient.md) — `HttpClientInterface`, scoping,
  streaming, retry and mocking.

## How to study it

1. Read [Client / Server](client-server.md) and [Status Codes](status-codes.md)
   for the raw protocol.
2. Map the protocol onto Symfony with [Request](request.md) and
   [Response](response.md) — these two are the core of the whole stage.
3. Layer on [Methods](methods.md), [Cookies](cookies.md) and
   [Content Negotiation](content-negotiation.md).
4. Finish with the [HttpClient](httpclient.md) component (the *outgoing* side).

---

<small>Related: [PHP & Web Security](../php-web-security/index.md) ·
[Symfony Architecture](../architecture/index.md) ·
[Controllers](../controllers/index.md) · [HTTP Caching](../http-caching/index.md)</small>

## Official References

- [Symfony documentation — HttpFoundation component](https://symfony.com/doc/8.0/components/http_foundation.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
