# Lab: HttpClient — An API Client Tested with `MockHttpClient`

!!! abstract "Practical Lab"
    **Objective:** Build a small, injectable API client on `HttpClientInterface`
    and prove — with zero network — that it sends the *right* request and maps the
    JSON reply to a DTO ·
    **Difficulty:** Medium ·
    **Theory:** [HttpClient Component](../http/httpclient.md) ·
    **Mode:** TDD

## Objective

After this lab you can **write and unit-test an outbound API integration** without
touching the network. Concretely, you will be able to:

- Wrap one JSON API in a service that depends on the **contract**
  `HttpClientInterface`, not a concrete transport.
- Assert the outgoing request — method, resolved URL, headers, query string, JSON
  body — using `MockHttpClient` with a **callback**.
- Return canned replies with `MockResponse` and map them onto a `readonly` DTO.
- Test the default error behaviour: `toArray()`/`getContent()` **throw on 4xx/5xx**.

## Prerequisites

- Chapters: [HttpClient Component](../http/httpclient.md) ·
  [HTTP Response](../http/response.md)
- Assumed skills: PHPUnit basics, constructor injection, JSON encoding, closures.

## TD Instructions

Work test-first. Do **not** write the client before its test exists.

1. Create a `readonly` DTO `App\ApiClient\Dto\Product` with `id`, `name`,
   `priceCents` and a static `fromArray()` factory that reads an API payload
   (`id`, `name`, `price_cents`).
2. Create the failing test `App\Tests\ApiClient\CatalogClientTest`. Instantiate a
   `MockHttpClient` whose **first argument is a callback**
   `function (string $method, string $url, array $options): MockResponse` and whose
   **second argument is the base URI** (`'https://api.test'`).
3. Inside the callback, assert the request: `GET`, the resolved URL
   `https://api.test/products/42`, and that `$options['headers']` contains
   `Accept: application/json`. Return a `MockResponse` with a JSON body.
4. Call `$sut->getProduct(42)` and assert the returned `Product` carries the
   decoded fields. Run it — watch it fail (no `CatalogClient` yet). This is **Red**.
5. Add a second test for `search()`: assert the callback sees the **query string**
   (`q=phone`, `page=2`) baked into `$url`, and that the `items` array maps to a
   `list<Product>`.
6. Add a third test for `create()`: assert `$options['body']` is the expected
   **JSON** (use `assertJsonStringEqualsJsonString`).
7. Add a fourth test: a `MockResponse` with `['http_code' => 404]` must make
   `getProduct()` throw a `ClientExceptionInterface`.
8. Now write `App\ApiClient\CatalogClient` (constructor-injected
   `HttpClientInterface`) with the minimum to go **Green**, then **Refactor**.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · no libraries outside the certification scope · follow
    best practices (constructor promotion, `readonly`, strict types, first-class
    callable syntax).

## Implementation Guide (partial)

High-level pointers — not the full code:

- **Contract, not transport.** Type-hint
  `Symfony\Contracts\HttpClient\HttpClientInterface`. The concrete client
  (`MockHttpClient` in tests, `CurlHttpClient`/scoped client in prod) is chosen by
  the caller/framework.
- **Base URI in the mock.** `new MockHttpClient($callbackOrResponses, 'https://api.test')`
  resolves your relative paths, so the callback receives the *fully resolved* URL —
  query string already appended.
- **Request options are normalized.** In the callback, `$options['headers']` is a
  list of `'Name: value'` strings (use `assertContains`), and the `json` option
  arrives as a serialized string in `$options['body']`.
- **DTO mapping** belongs in the DTO (`Product::fromArray()`), not in the client —
  the client only orchestrates the HTTP call. Map a collection with
  `array_map(Product::fromArray(...), $items)` (first-class callable).
- **Errors are free.** Do nothing special: `toArray()` and `getContent()` throw on
  3xx–5xx by default, so a 404 propagates as `ClientExceptionInterface`.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** write the four tests below; run them, watch them fail (the client
       and DTO do not exist yet).
    2. **Green:** write `Product` then `CatalogClient` — the minimum to pass.
    3. **Refactor:** push mapping into the DTO; keep the client a thin orchestrator.

**Behaviour (Given/When/Then):**

- **Given** a `MockHttpClient` with base URI `https://api.test`,
  **When** `getProduct(42)` runs, **Then** it issues `GET /products/42` with
  `Accept: application/json` and returns a `Product(42, 'Widget', 1999)`.
- **Given** a `404` `MockResponse`, **When** `getProduct()` reads the body,
  **Then** a `ClientExceptionInterface` is thrown.

```php
<?php
declare(strict_types=1);

namespace App\Tests\ApiClient;

use App\ApiClient\CatalogClient;
use App\ApiClient\Dto\Product;
use PHPUnit\Framework\TestCase;
use Symfony\Component\HttpClient\MockHttpClient;
use Symfony\Component\HttpClient\Response\MockResponse;
use Symfony\Contracts\HttpClient\Exception\ClientExceptionInterface;

final class CatalogClientTest extends TestCase
{
    public function testGetProductBuildsRequestAndMapsResponse(): void
    {
        // Arrange: the callback inspects the OUTGOING request,
        // then hands back a canned reply — zero network access.
        $client = new MockHttpClient(function (string $method, string $url, array $options): MockResponse {
            self::assertSame('GET', $method);
            self::assertSame('https://api.test/products/42', $url);
            self::assertContains('Accept: application/json', $options['headers']);

            return new MockResponse(
                json_encode(['id' => 42, 'name' => 'Widget', 'price_cents' => 1999]),
                ['http_code' => 200, 'response_headers' => ['Content-Type' => 'application/json']],
            );
        }, 'https://api.test');

        $sut = new CatalogClient($client);

        // Act
        $product = $sut->getProduct(42);

        // Assert: the JSON response was mapped onto the DTO.
        self::assertInstanceOf(Product::class, $product);
        self::assertSame(42, $product->id);
        self::assertSame('Widget', $product->name);
        self::assertSame(1999, $product->priceCents);
    }

    public function testSearchEncodesQueryString(): void
    {
        $client = new MockHttpClient(function (string $method, string $url): MockResponse {
            self::assertSame('GET', $method);
            self::assertStringContainsString('q=phone', $url);
            self::assertStringContainsString('page=2', $url);

            return new MockResponse(json_encode(['items' => [
                ['id' => 1, 'name' => 'Phone A', 'price_cents' => 500],
                ['id' => 2, 'name' => 'Phone B', 'price_cents' => 700],
            ]]));
        }, 'https://api.test');

        $products = (new CatalogClient($client))->search('phone', page: 2);

        self::assertCount(2, $products);
        self::assertSame('Phone A', $products[0]->name);
    }

    public function testCreateSendsJsonBody(): void
    {
        $client = new MockHttpClient(function (string $method, string $url, array $options): MockResponse {
            self::assertSame('POST', $method);
            self::assertJsonStringEqualsJsonString(
                '{"name":"New","price_cents":250}',
                (string) $options['body'],
            );

            return new MockResponse(
                json_encode(['id' => 99, 'name' => 'New', 'price_cents' => 250]),
                ['http_code' => 201],
            );
        }, 'https://api.test');

        $product = (new CatalogClient($client))->create('New', 250);

        self::assertSame(99, $product->id);
    }

    public function testNotFoundResponseThrows(): void
    {
        // A bare MockResponse (no callback) is the simplest way to script a status.
        $client = new MockHttpClient(
            new MockResponse('{"error":"not found"}', ['http_code' => 404]),
            'https://api.test',
        );

        $this->expectException(ClientExceptionInterface::class);

        (new CatalogClient($client))->getProduct(404); // toArray() throws on 4xx
    }
}
```

!!! tip "Setup hints"
    Run it: `vendor/bin/phpunit tests/ApiClient/CatalogClientTest.php`.
    Key fixtures: `MockHttpClient` (callback **or** a `MockResponse`/array of them)
    and `MockResponse`. The callback signature is
    `fn (string $method, string $url, array $options): MockResponse`; the `$url` it
    receives is **already resolved** against the base URI, query string included.
    Alternative recorder: keep a reference to a `MockResponse` and read
    `->getRequestMethod()`, `->getRequestUrl()`, `->getRequestOptions()` *after* the
    call.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/ApiClient/CatalogClientTest.php` is green (4 tests).
- [ ] No network is hit — the suite runs offline and instantly.
- [ ] Temporarily change `getProduct()` to send `POST`; the first test goes red on
      the `assertSame('GET', $method)` line, proving the callback really inspects
      the request.

## Review — Common Mistakes

- **Type-hinting `MockHttpClient` / `CurlHttpClient` in the client.** → The service
  becomes untestable/coupled. → Depend on `HttpClientInterface`.
- **Asserting `$options['query']` in the callback.** → It is empty; the query is
  already merged into `$url`. → Assert on `$url` (or read `getRequestUrl()`).
- **Expecting `$options['headers']` to be a map.** → It is a normalized *list* of
  `'Name: value'` strings. → Use `assertContains('Accept: application/json', ...)`.
- **Wrapping `toArray()` in a try/catch that swallows errors, then testing for an
  exception.** → The 4xx test fails. → Let the default `throw: true` propagate.
- **Building the URL with string concatenation and a hand-rolled query string.** →
  Encoding bugs. → Pass the `query` option; HttpClient encodes it.
- **Putting JSON-decoding + field mapping in the client.** → The client stops being
  a thin orchestrator. → Map inside `Product::fromArray()`.

## Exam Connection

The certification probes three reflexes this lab drills:

- **Lazy/async model** — `request()` returns immediately; the transfer completes on
  the first content read (`toArray()`), which is exactly where errors surface.
- **Error semantics** — `getStatusCode()` never throws, but `getContent()`/
  `toArray()` throw `ClientExceptionInterface` (4xx) / `ServerExceptionInterface`
  (5xx) unless you pass `throw: false`. The trap: code that "checks the status
  after `toArray()`" never runs, because `toArray()` already threw.
- **Testing without network** — `MockHttpClient` + `MockResponse` are *the*
  sanctioned tools; the callback form is how you assert on the request itself.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    ```php
    <?php
    declare(strict_types=1);

    namespace App\ApiClient\Dto;

    /**
     * Immutable representation of one API resource.
     */
    final readonly class Product
    {
        public function __construct(
            public int $id,
            public string $name,
            public int $priceCents,
        ) {}

        /** @param array<string, mixed> $data */
        public static function fromArray(array $data): self
        {
            return new self(
                (int) $data['id'],
                (string) $data['name'],
                (int) $data['price_cents'],
            );
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    namespace App\ApiClient;

    use App\ApiClient\Dto\Product;
    use Symfony\Contracts\HttpClient\HttpClientInterface;

    /**
     * Thin, transport-agnostic wrapper around one JSON API.
     * Depends on the CONTRACT, never on a concrete transport.
     */
    final readonly class CatalogClient
    {
        public function __construct(
            private HttpClientInterface $client,
        ) {}

        public function getProduct(int $id): Product
        {
            $response = $this->client->request('GET', "/products/{$id}", [
                'headers' => ['Accept' => 'application/json'],
            ]);

            // toArray() completes the transfer, JSON-decodes, and THROWS on 3xx-5xx.
            return Product::fromArray($response->toArray());
        }

        /**
         * @return list<Product>
         */
        public function search(string $term, int $page = 1): array
        {
            $response = $this->client->request('GET', '/products', [
                'query' => ['q' => $term, 'page' => $page],
            ]);

            return array_map(
                Product::fromArray(...),
                $response->toArray()['items'] ?? [],
            );
        }

        public function create(string $name, int $priceCents): Product
        {
            $response = $this->client->request('POST', '/products', [
                'json' => ['name' => $name, 'price_cents' => $priceCents],
            ]);

            return Product::fromArray($response->toArray());
        }
    }
    ```

    In production, wire a **scoped client** so the base URI and auth live in config,
    and autowire it by variable name:

    ```yaml
    # config/packages/framework.yaml
    framework:
        http_client:
            scoped_clients:
                catalog.client:
                    base_uri: '%env(CATALOG_BASE_URI)%'
                    auth_bearer: '%env(CATALOG_TOKEN)%'
    ```

    ```php
    // The framework injects the named client into $client automatically.
    public function __construct(
        private HttpClientInterface $catalogClient,
    ) {}
    ```

## Alternative Approaches (optional)

- **Option A (simple) — array of `MockResponse`.** Skip the callback and pass
  `new MockHttpClient([$r1, $r2])`; responses are consumed in order. Good when you
  only care about the *reply*, not the request shape.
- **Option B (recorder) — assert after the call.** Keep the `MockResponse` in a
  variable and read `->getRequestMethod()`, `->getRequestUrl()`,
  `->getRequestOptions()` once the client has run. Keeps assertions out of the
  closure.
- **Option C (exam-style / level up) — tolerant reads.** Return `null` on 404
  instead of throwing, using the status-first pattern:

    ```php
    <?php
    declare(strict_types=1);

    namespace App\ApiClient;

    use App\ApiClient\Dto\Product;
    use Symfony\Contracts\HttpClient\HttpClientInterface;

    final readonly class CatalogClientLenient
    {
        public function __construct(
            private HttpClientInterface $client,
        ) {}

        public function findProduct(int $id): ?Product
        {
            $response = $this->client->request('GET', "/products/{$id}");

            // getStatusCode() NEVER throws; only content readers do.
            if (404 === $response->getStatusCode()) {
                return null;
            }

            // throw: false suppresses the exception so we can inspect the body.
            return Product::fromArray($response->toArray(throw: false));
        }
    }
    ```

---

<small>Theory: [HttpClient Component](../http/httpclient.md) · Labs: [all labs](index.md)</small>
