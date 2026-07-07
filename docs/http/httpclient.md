# HttpClient Component

!!! tip "In a nutshell"
    HttpClient is Symfony's *outgoing* HTTP layer — your app calling other APIs.
    Type-hint `HttpClientInterface`, never a concrete transport. Exam hook:
    `request()` is **lazy/async**; the transfer runs only on first read of the
    response (which makes concurrency free).

!!! example "Real-world analogy"
    If HttpFoundation handles the mail arriving at *your* office, HttpClient is
    **you posting letters to another office** and awaiting their reply. You write
    the request, hand it to the courier (`request()`), and — because the courier
    is async — you can send a whole stack at once and only wait when you actually
    open a reply (`getContent()`). A scoped client is a pre-addressed,
    pre-stamped envelope for one specific office.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Make requests through `HttpClientInterface` and read `ResponseInterface`.
    - [ ] Configure scoped/base-URI clients and per-request options.
    - [ ] Stream and run requests concurrently (async by default).
    - [ ] Add retries and mock the client in tests.

    **Syllabus:** `HTTP → HttpClient component` ·
    **Level:** Expert ·
    **Est. time:** 35 min ·
    **Prerequisites:** [HTTP Request](request.md) · [HTTP Response](response.md)

---

## Theory

`Symfony\Component\HttpClient` is the **outgoing** side of HTTP: your app as a
*client* calling other services/APIs. It provides a small, transport-agnostic
interface plus decorators for scoping, retry, logging and testing. It implements
Symfony's own `HttpClientInterface` **and** PSR-18 (`Psr18Client`).

Two transports back it:

- `Symfony\Component\HttpClient\CurlHttpClient` — uses ext-curl; supports HTTP/2,
  concurrency, push. Preferred when curl is available.
- `Symfony\Component\HttpClient\NativeHttpClient` — pure PHP streams; the fallback.

`HttpClient::create()` picks the best available automatically.

```php
use Symfony\Component\HttpClient\HttpClient;
use Symfony\Contracts\HttpClient\HttpClientInterface;

// CurlHttpClient when ext-curl is available, NativeHttpClient otherwise
$client = HttpClient::create();
assert($client instanceof HttpClientInterface); // always code against the contract
```

!!! question "Predict first"
    You call `$client->request('GET', $url)` three times in a loop without reading
    any response. How many HTTP transfers have completed?

??? note "Reveal"
    Zero from `request()` alone — it is **lazy**. The three transfers run
    concurrently in the background and each completes only on the first read of its
    status/headers/content. Batch first, read later, and concurrency is free.

## Deep Dive — how it works internally

### Interfaces and the lazy/async model

The contract lives in `Symfony\Contracts\HttpClient`:

- `HttpClientInterface::request(string $method, string $url, array $options = []): ResponseInterface`
- `ResponseInterface` — `getStatusCode()`, `getHeaders()`, `getContent()`,
  `toArray()`, `getInfo()`, `cancel()`.
- `ResponseStreamInterface` + `ChunkInterface` for streaming.

`request()` is **non-blocking**: it returns immediately with a lazy
`ResponseInterface`. The HTTP exchange is only *completed* when you first read the
status/headers/content. This makes concurrency free — fire many requests, then
read them:

```php
$response = $client->request('GET', 'https://api.example.com/users');

$response->getStatusCode();       // 200 — first read completes the transfer
$response->getHeaders();          // ['content-type' => ['application/json'], ...]
$response->getContent();          // raw body string
$response->toArray();             // JSON-decoded array
$response->getInfo('total_time'); // transport metadata

// ResponseStreamInterface yields ChunkInterface objects
foreach ($client->stream($response) as $chunk) {
    if ($chunk->isLast()) { /* transfer finished */ }
}

$client->request('GET', 'https://api.example.com/slow')->cancel(); // abort
```

```mermaid
sequenceDiagram
    participant App
    participant HC as HttpClient
    App->>HC: request() x3 (returns lazy responses)
    Note over HC: transfers run concurrently in the background
    App->>HC: $r1->getContent() (waits only for r1)
    App->>HC: $r2->getContent()
```

!!! note "Source reference"
    `Symfony\Contracts\HttpClient\HttpClientInterface`,
    `Symfony\Component\HttpClient\HttpClient`, `CurlHttpClient`,
    `NativeHttpClient` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpClient/HttpClient.php).

### Reading responses & error handling

`getStatusCode()` never throws. `getContent()` and `toArray()` **throw on 3xx/4xx/
5xx** by default (`throw: true`):

- `Symfony\Contracts\HttpClient\Exception\ClientExceptionInterface` (4xx)
- `ServerExceptionInterface` (5xx), `RedirectionExceptionInterface` (3xx),
  `TransportExceptionInterface` (network).

Pass `getContent(false)` (or the `throw` option) to inspect error bodies yourself.
`toArray()` JSON-decodes and returns an array.

```php
use Symfony\Contracts\HttpClient\Exception\ClientExceptionInterface;
use Symfony\Contracts\HttpClient\Exception\RedirectionExceptionInterface;
use Symfony\Contracts\HttpClient\Exception\ServerExceptionInterface;
use Symfony\Contracts\HttpClient\Exception\TransportExceptionInterface;

try {
    $data = $response->toArray(); // throws on 3xx/4xx/5xx (throw: true)
} catch (ClientExceptionInterface $e) {           // 4xx
    $body = $e->getResponse()->getContent(false); // inspect the error body
} catch (ServerExceptionInterface|RedirectionExceptionInterface $e) { // 5xx / 3xx
    throw $e;
} catch (TransportExceptionInterface $e) {        // network failure
    throw $e;
}

$response->getStatusCode(); // never throws
```

### Options that matter

Per-request or as client defaults via `withOptions()`:

| Option | Effect |
|---|---|
| `query` | Appended query params (array) |
| `headers` | Request headers |
| `json` | Body encoded as JSON + `Content-Type: application/json` |
| `body` | Raw/string/iterable/closure body (streamed) |
| `auth_basic` / `auth_bearer` | Authentication |
| `base_uri` | Prefixed to relative URLs |
| `timeout` / `max_duration` | Idle timeout / total cap |
| `max_redirects` | Follow limit |

```php
// client-wide defaults, then per-request options
$client = $client->withOptions(['base_uri' => 'https://api.example.com', 'timeout' => 4.0]);

$client->request('POST', '/articles', [
    'query'         => ['page' => 2],          // ?page=2
    'headers'       => ['Accept' => 'application/json'],
    'json'          => ['title' => 'Hello'],   // or 'body' for a raw/streamed payload
    'auth_bearer'   => $token,                 // or 'auth_basic' => 'user:pass'
    'max_duration'  => 10.0,                   // total cap, unlike idle 'timeout'
    'max_redirects' => 3,
]);
```

### Scoped clients & base URI

A **scoped client** applies options (base URI, auth, headers) only to URLs
matching a host/regexp — ideal for wrapping one API. Configure declaratively; the
framework injects a named client you autowire by variable name:

```mermaid
flowchart LR
    A[HttpClientInterface $githubClient] --> B[ScopingHttpClient]
    B -->|host matches api.github.com| C[base_uri + auth_bearer applied]
    B -->|other host| D[options NOT applied]
```

Programmatically, `ScopingHttpClient::forBaseUri($client, 'https://api.github.com')`
or `$client->withOptions(['base_uri' => '...'])`.

```php
use Symfony\Component\HttpClient\ScopingHttpClient;

// options apply only to URLs under this base URI
$github = ScopingHttpClient::forBaseUri($client, 'https://api.github.com', [
    'auth_bearer' => $token,
]);

// or derive a client with defaults bound to every request
$api = $client->withOptions(['base_uri' => 'https://api.example.com']);
```

### Retry & streaming decorators

- `Symfony\Component\HttpClient\RetryableHttpClient` wraps any client and retries
  failed/5xx/429 requests using a `GenericRetryStrategy` (honours `Retry-After`).
- `$client->stream($response)` returns a `ResponseStreamInterface`; iterate to get
  `ChunkInterface` pieces without buffering the whole body — for large downloads
  or Server-Sent Events (`EventSourceHttpClient`).

```php
use Symfony\Component\HttpClient\EventSourceHttpClient;
use Symfony\Component\HttpClient\Retry\GenericRetryStrategy;
use Symfony\Component\HttpClient\RetryableHttpClient;

// retries failed/5xx/429 responses, honouring Retry-After
$client = new RetryableHttpClient($inner, new GenericRetryStrategy(), 2);

$response = $client->request('GET', $bigFileUrl);
foreach ($client->stream($response) as $chunk) { // ResponseStreamInterface
    $fragment = $chunk->getContent();            // ChunkInterface piece
}

$sse = new EventSourceHttpClient($client); // Server-Sent Events wrapper
```

### Null behavior

`getContent()` returns a **string** — for a legitimately empty body (a `204 No
Content`, or a `200` with nothing to send) that string is simply `''`, **not
`null`**. Do not test the body with `=== null`; test `'' === $response->getContent()`
or check the status code first.

`toArray()` is stricter: on an empty body it throws a `JsonException` because `""`
is not valid JSON — there is no silent `null` return. Guard a possibly-empty
payload before decoding:

```php
$response = $client->request('GET', $url);
if (204 === $response->getStatusCode() || '' === $response->getContent(false)) {
    return [];
}

return $response->toArray();
```

To read a header that may be absent, header bags here are keyed arrays, so use
`$response->getHeaders()['x-total'][0] ?? null` rather than a nullable getter. The
common bug is calling `toArray()` on a `204` and being surprised by the decode
exception instead of receiving `null`.

```php
$headers = $response->getHeaders(false); // arrays keyed by lowercased name
$total = $headers['x-total'][0] ?? null; // null when the header is absent

// guard before decoding: toArray() throws on an empty 204 body
$data = 204 === $response->getStatusCode() ? [] : $response->toArray();
```

!!! note "Null in real life"
    An empty response is a **reply envelope that arrived empty** — the courier
    delivered it (status `204`), there just aren't any pages inside. That is a
    valid outcome, not a lost letter.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Service;

    use Symfony\Component\DependencyInjection\Attribute\Autowire;
    use Symfony\Contracts\HttpClient\HttpClientInterface;

    final readonly class GitHubApi
    {
        public function __construct(
            // Inject a scoped client defined in framework.yaml by its name.
            #[Autowire(service: 'github.client')]
            private HttpClientInterface $client,
        ) {}

        /** @return array<string, mixed> */
        public function repo(string $owner, string $name): array
        {
            $response = $this->client->request('GET', "/repos/{$owner}/{$name}");

            return $response->toArray(); // decodes JSON; throws on 4xx/5xx
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/packages/framework.yaml
    framework:
        http_client:
            scoped_clients:
                github.client:
                    base_uri: 'https://api.github.com/'
                    headers:
                        Accept: 'application/vnd.github+json'
                    auth_bearer: '%env(GITHUB_TOKEN)%'
                    retry_failed:
                        max_retries: 3
    ```

=== "Console"

    ```console
    $ php bin/console debug:container --tag=http_client.client
    ```

### Concurrency & streaming

```php
<?php
declare(strict_types=1);

use Symfony\Component\HttpClient\HttpClient;

$client = HttpClient::create();

// Fire concurrently — responses are lazy.
$responses = [];
foreach (['https://a.example', 'https://b.example'] as $url) {
    $responses[] = $client->request('GET', $url);
}

// Stream as chunks arrive across all responses.
foreach ($client->stream($responses) as $response => $chunk) {
    if ($chunk->isLast()) {
        // this $response finished
    }
}
```

### Mocking in tests

```php
<?php
declare(strict_types=1);

use Symfony\Component\HttpClient\MockHttpClient;
use Symfony\Component\HttpClient\Response\MockResponse;

$client = new MockHttpClient([
    new MockResponse('{"id":42}', ['http_code' => 200]),
]);

$data = $client->request('GET', 'https://api.test/thing')->toArray();
// $data === ['id' => 42] — no network traffic
```

`Symfony\Component\HttpClient\MockHttpClient` + `Response\MockResponse` return
canned responses (or a callback) with **zero network access** — the standard way
to test API integrations.

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Type-hint `HttpClientInterface` | Depending on `CurlHttpClient` directly |
| Scoped clients for each API | Repeating base URI + auth everywhere |
| `MockHttpClient` in tests | Real HTTP calls in tests |
| Batch + `stream()` for concurrency | Sequential blocking loops |
| `RetryableHttpClient` for flaky APIs | Hand-rolled retry loops |

## When (not) to use it / alternatives

Use HttpClient for any outbound HTTP. For fire-and-forget or heavy fan-out,
combine it with Messenger (async). It is **not** for serving inbound requests —
that is HttpFoundation/HttpKernel. Guzzle is unnecessary; HttpClient is
PSR-18-compatible if a library needs it.

!!! danger "Certification traps"
    - **`request()` is lazy/async** — the transfer completes on first read of
      status/headers/content, enabling free concurrency.
    - **`getContent()`/`toArray()` throw on 3xx/4xx/5xx by default**;
      `getStatusCode()` never throws. Pass `false` / `throw: false` to read error
      bodies.
    - Type-hint the **`HttpClientInterface`** (the contract), not a concrete
      transport.
    - **Scoped-client options apply only to matching hosts/base URI**; other URLs
      ignore them.
    - Mock with `MockHttpClient` + `MockResponse` — no network in tests.

!!! warning "Common mistakes"
    - Reading `getContent()` inside the request loop, killing concurrency.
    - Forgetting relative URLs need a `base_uri` (scoped) client.
    - Expecting `toArray()` to work on non-JSON responses.

## Exercises

1. **(Advanced)** Fetch JSON from an API and return it as a PHP array, handling a
   404 gracefully (no exception).
2. **(Expert)** Write a unit test that asserts your service parses `{"ok":true}`
   without any network call.

??? success "Solutions"

    **1.**
    ```php
    $response = $client->request('GET', $url);
    if (404 === $response->getStatusCode()) {
        return [];
    }
    return $response->toArray(); // safe: status already checked
    ```
    (Or `$response->toArray(false)` to suppress the exception and inspect.)

    **2.**
    ```php
    $client = new MockHttpClient(new MockResponse('{"ok":true}'));
    $service = new MyService($client);
    self::assertTrue($service->check());
    ```

## Certification questions

??? question "Q1. When is an HttpClient request actually performed?"
    - [ ] A. Immediately when `request()` is called
    - [x] B. Lazily, on first read of status/headers/content ✅
    - [ ] C. Only when `stream()` is called
    - [ ] D. When the kernel terminates

    **Why:** `request()` returns a lazy response; the transfer completes on first
    access, which is what enables concurrency.
    **Ref:** [HttpClient](https://symfony.com/doc/current/http_client.html).

??? question "Q2. What does `getContent()` do on a 500 response by default?"
    - [ ] A. Returns the body
    - [ ] B. Returns an empty string
    - [x] C. Throws a `ServerExceptionInterface` ✅
    - [ ] D. Returns null

    **Why:** By default errors throw; pass `false` to read the body without
    throwing.
    **Ref:** [HttpClient exceptions](https://symfony.com/doc/current/http_client.html#handling-exceptions).

??? question "Q3. Which type should you type-hint for autowiring an HTTP client?"
    - [x] A. `Symfony\Contracts\HttpClient\HttpClientInterface` ✅
    - [ ] B. `CurlHttpClient`
    - [ ] C. `NativeHttpClient`
    - [ ] D. `Psr18Client`

    **Why:** Depend on the contract; the transport is chosen by the framework.
    **Ref:** [HttpClient DI](https://symfony.com/doc/current/http_client.html).

??? question "Q4. Which class lets you test API code with no network?"
    - [ ] A. `RetryableHttpClient`
    - [ ] B. `ScopingHttpClient`
    - [x] C. `MockHttpClient` ✅
    - [ ] D. `EventSourceHttpClient`

    **Why:** `MockHttpClient` returns `MockResponse` objects without real
    requests.
    **Ref:** [Testing HttpClient](https://symfony.com/doc/current/http_client.html#testing).

## Key takeaways

- `HttpClientInterface::request()` is lazy/async; concurrency is free.
- `getContent()`/`toArray()` throw on 3xx–5xx by default; `getStatusCode()` never.
- Scoped clients bind base URI/auth to matching hosts.
- `RetryableHttpClient` for resilience; `MockHttpClient` for tests.

## Last-minute revision

!!! tip "Cheat sheet"
    - Contract: `HttpClientInterface` / `ResponseInterface`. Factory:
      `HttpClient::create()`.
    - Options: `json`, `query`, `headers`, `auth_bearer`, `base_uri`, `timeout`.
    - Concurrency: loop `request()`, then `$client->stream($responses)`.
    - Test: `MockHttpClient` + `MockResponse`. Resilience: `RetryableHttpClient`.

## Connections

- **Depends on:** [HTTP Response](response.md) — `ResponseInterface` mirrors the response model, one direction out.
- **Reused in:** [Messenger Component](../miscellaneous/messenger.md) — pair outbound calls with async fan-out and retries.
- **Confused with:** [HTTP Request](request.md) — HttpClient is the *outgoing* client; `Request` wraps the *incoming* exchange.

## Official References
- [Symfony docs — HttpClient](https://symfony.com/doc/current/http_client.html)
- [Symfony source — HttpClient](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpClient/HttpClient.php)
- [Symfony source — HttpClientInterface](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Contracts/HttpClient/HttpClientInterface.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "HTTP foundation" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/http_client.html) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** you type-hint `HttpClientInterface` instead of a concrete transport
- [ ] configure a scoped/base-URI client and send per-request options
- [ ] debug lost concurrency (reading inside the request loop) and empty-body decode errors
- [ ] spot the trick: `request()` is lazy, `getContent()`/`toArray()` throw on 3xx–5xx
- [ ] explain how `stream()`, `RetryableHttpClient` and `MockHttpClient` fit together

---

<small>Related: [HTTP Request](request.md) · [HTTP Response](response.md) ·
[Status Codes](status-codes.md) · [Messenger Component](../miscellaneous/messenger.md)</small>
