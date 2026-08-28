---
tags:
  - Labs
  - HTTP
---

# Lab: HttpClient — An API Client Tested with `MockHttpClient`

!!! abstract "Practical Lab"
    **Objective:** construire un petit client d'API injectable basé sur `HttpClientInterface`
    et prouver — sans aucun accès réseau — qu'il envoie la *bonne* request et mappe la
    réponse JSON vers un DTO ·
    **Difficulty:** Medium ·
    **Theory:** [HttpClient Component](../http/httpclient.md) ·
    **Mode:** TDD

## 🧠 Pour les nuls

**C'est quoi ce lab ?** Construire un client qui appelle une API externe, et prouver qu'il envoie la bonne requête sans jamais réellement toucher au réseau pendant les tests.

**Pourquoi ça existe ?** Tester du vrai code réseau est lent et fragile (l'API externe peut être en panne pendant ton test) — `MockHttpClient` simule les réponses pour des tests rapides et fiables.

**🏠 Analogie de la vraie vie :** Répéter un appel téléphonique important avec un collègue qui joue le rôle de l'interlocuteur, plutôt que d'appeler le vrai client à chaque répétition.

**Symfony dans la vraie vie :** `new MockHttpClient([new MockResponse($json)])` remplace le vrai `HttpClientInterface` dans un test — ton code de production reste identique, seul le test simule la réponse.

**⚠️ Erreur fréquente :** type-hinter directement une classe concrète de transport au lieu de `HttpClientInterface` — ça empêche de substituer un mock dans les tests.

**🧠 Comment le mémoriser :** "Teste ton client sans jamais vraiment décrocher le téléphone — simule la réponse, ne l'attends pas."


## Objective

À l'issue de ce lab, vous saurez **écrire et tester unitairement une intégration d'API
sortante** sans toucher au réseau. Concrètement, vous serez capable de :

- Encapsuler une API JSON dans un service qui dépend du **contrat**
  `HttpClientInterface`, et non d'un transport concret.
- Vérifier la request sortante — méthode, URL résolue, headers, query string, corps
  JSON — grâce à `MockHttpClient` et un **callback**.
- Retourner des réponses préfabriquées avec `MockResponse` et les mapper vers un DTO `readonly`.
- Tester le comportement d'erreur par défaut : `toArray()`/`getContent()` **lèvent une exception sur les 4xx/5xx**.

## Prerequisites

- Chapitres : [HttpClient Component](../http/httpclient.md) ·
  [HTTP Response](../http/response.md)
- Compétences supposées acquises : bases de PHPUnit, injection par constructeur, encodage JSON, closures.

## TD Instructions

Travaillez en mode test-first. N'écrivez **pas** le client avant que son test n'existe.

1. Créez un DTO `readonly` `App\ApiClient\Dto\Product` avec `id`, `name`,
   `priceCents` et une factory statique `fromArray()` qui lit un payload d'API
   (`id`, `name`, `price_cents`).
2. Créez le test en échec `App\Tests\ApiClient\CatalogClientTest`. Instanciez un
   `MockHttpClient` dont le **premier argument est un callback**
   `function (string $method, string $url, array $options): MockResponse` et dont le
   **second argument est la base URI** (`'https://api.test'`).
3. Dans le callback, vérifiez la request : `GET`, l'URL résolue
   `https://api.test/products/42`, et le fait que `$options['headers']` contient
   `Accept: application/json`. Retournez une `MockResponse` avec un corps JSON.
4. Appelez `$sut->getProduct(42)` et vérifiez que le `Product` retourné porte bien les
   champs décodés. Lancez le test — il échoue (pas encore de `CatalogClient`). C'est **Red**.
5. Ajoutez un deuxième test pour `search()` : vérifiez que le callback voit la **query string**
   (`q=phone`, `page=2`) intégrée dans `$url`, et que le tableau `items` est mappé vers une
   `list<Product>`.
6. Ajoutez un troisième test pour `create()` : vérifiez que `$options['body']` est bien le
   **JSON** attendu (utilisez `assertJsonStringEqualsJsonString`).
7. Ajoutez un quatrième test : une `MockResponse` avec `['http_code' => 404]` doit faire
   lever une `ClientExceptionInterface` à `getProduct()`.
8. Écrivez maintenant `App\ApiClient\CatalogClient` (avec `HttpClientInterface`
   injecté par constructeur), le strict minimum pour passer au **Green**, puis **Refactor**.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · aucune bibliothèque hors du périmètre de la certification · respect
    des bonnes pratiques (promotion de constructeur, `readonly`, types stricts, syntaxe
    first-class callable).

## Implementation Guide (partial)

Des repères de haut niveau — pas le code complet :

- **Le contrat, pas le transport.** Typez sur
  `Symfony\Contracts\HttpClient\HttpClientInterface`. Le client concret
  (`MockHttpClient` dans les tests, `CurlHttpClient`/scoped client en production) est choisi par
  l'appelant/le framework.
- **La base URI dans le mock.** `new MockHttpClient($callbackOrResponses, 'https://api.test')`
  résout vos chemins relatifs, si bien que le callback reçoit l'URL *entièrement résolue* —
  query string déjà ajoutée.
- **Les options de la request sont normalisées.** Dans le callback, `$options['headers']` est une
  liste de chaînes `'Name: value'` (utilisez `assertContains`), et l'option `json`
  arrive sous forme de chaîne sérialisée dans `$options['body']`.
- **Le mapping du DTO** appartient au DTO (`Product::fromArray()`), pas au client —
  le client ne fait qu'orchestrer l'appel HTTP. Mappez une collection avec
  `array_map(Product::fromArray(...), $items)` (first-class callable).
- **Les erreurs sont gratuites.** Ne faites rien de spécial : `toArray()` et `getContent()` lèvent
  une exception sur les 3xx–5xx par défaut, donc un 404 se propage en `ClientExceptionInterface`.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** écrivez les quatre tests ci-dessous ; lancez-les et constatez l'échec (le client
       et le DTO n'existent pas encore).
    2. **Green :** écrivez `Product` puis `CatalogClient` — le minimum pour passer.
    3. **Refactor :** déplacez le mapping dans le DTO ; gardez un client qui reste un fin orchestrateur.

**Behaviour (Given/When/Then):**

- **Given** un `MockHttpClient` avec la base URI `https://api.test`,
  **When** `getProduct(42)` s'exécute, **Then** il émet `GET /products/42` avec
  `Accept: application/json` et retourne un `Product(42, 'Widget', 1999)`.
- **Given** une `MockResponse` `404`, **When** `getProduct()` lit le corps,
  **Then** une `ClientExceptionInterface` est levée.

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
    Lancez-le : `vendor/bin/phpunit tests/ApiClient/CatalogClientTest.php`.
    Fixtures clés : `MockHttpClient` (un callback **ou** une `MockResponse`/un tableau de celles-ci)
    et `MockResponse`. La signature du callback est
    `fn (string $method, string $url, array $options): MockResponse` ; le `$url` qu'il
    reçoit est **déjà résolu** par rapport à la base URI, query string comprise.
    Alternative « enregistreur » : gardez une référence vers une `MockResponse` et lisez
    `->getRequestMethod()`, `->getRequestUrl()`, `->getRequestOptions()` *après*
    l'appel.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/ApiClient/CatalogClientTest.php` est au vert (4 tests).
- [ ] Aucun accès réseau — la suite s'exécute hors ligne et instantanément.
- [ ] Modifiez temporairement `getProduct()` pour envoyer un `POST` ; le premier test passe au rouge sur
      la ligne `assertSame('GET', $method)`, preuve que le callback inspecte réellement
      la request.

## Review — Common Mistakes

- **Typer sur `MockHttpClient` / `CurlHttpClient` dans le client.** → Le service
  devient intestable/couplé. → Dépendez de `HttpClientInterface`.
- **Vérifier `$options['query']` dans le callback.** → Elle est vide ; la query est
  déjà fusionnée dans `$url`. → Faites l'assertion sur `$url` (ou lisez `getRequestUrl()`).
- **S'attendre à ce que `$options['headers']` soit un tableau associatif.** → C'est une *liste* normalisée de
  chaînes `'Name: value'`. → Utilisez `assertContains('Accept: application/json', ...)`.
- **Envelopper `toArray()` dans un try/catch qui avale les erreurs, puis tester une
  exception.** → Le test 4xx échoue. → Laissez le `throw: true` par défaut se propager.
- **Construire l'URL par concaténation de chaînes avec une query string faite à la main.** →
  Bugs d'encodage. → Passez l'option `query` ; HttpClient l'encode pour vous.
- **Mettre le décodage JSON + le mapping des champs dans le client.** → Le client cesse d'être
  un fin orchestrateur. → Mappez dans `Product::fromArray()`.

## Exam Connection

La certification teste trois réflexes que ce lab fait travailler :

- **Modèle lazy/async** — `request()` retourne immédiatement ; le transfert se termine à la
  première lecture du contenu (`toArray()`), et c'est précisément là que les erreurs apparaissent.
- **Sémantique des erreurs** — `getStatusCode()` ne lève jamais d'exception, mais `getContent()`/
  `toArray()` lèvent `ClientExceptionInterface` (4xx) / `ServerExceptionInterface`
  (5xx) sauf si vous passez `throw: false`. Le piège : le code qui « vérifie le statut
  après `toArray()` » ne s'exécute jamais, car `toArray()` a déjà levé l'exception.
- **Tester sans réseau** — `MockHttpClient` + `MockResponse` sont *les* outils
  officiels ; la forme callback est le moyen de faire des assertions sur la request elle-même.

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

    En production, configurez un **scoped client** pour que la base URI et l'authentification vivent dans la config,
    et laissez l'autowiring l'injecter par nom de variable :

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

- **Option A (simple) — tableau de `MockResponse`.** Oubliez le callback et passez
  `new MockHttpClient([$r1, $r2])` ; les réponses sont consommées dans l'ordre. Idéal quand seul
  le contenu de la *réponse* vous intéresse, pas la forme de la request.
- **Option B (enregistreur) — assertions après l'appel.** Gardez la `MockResponse` dans une
  variable et lisez `->getRequestMethod()`, `->getRequestUrl()`,
  `->getRequestOptions()` une fois le client exécuté. Cela garde les assertions hors de la
  closure.
- **Option C (exam-style / niveau supérieur) — lectures tolérantes.** Retournez `null` sur un 404
  au lieu de lever une exception, avec le pattern « statut d'abord » :

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
