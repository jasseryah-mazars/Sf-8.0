---
tags:
  - Labs
  - Controllers
---

# Lab: Custom Value Resolver — hydrate a controller argument from the Request

!!! abstract "Practical Lab"
    **Objective :** implémenter un `ValueResolverInterface` personnalisé qui hydrate
    un value object directement dans un argument de controller, se désiste proprement
    pour les autres types, et transforme un invariant violé en `400` ·
    **Difficulty:** Advanced ·
    **Theory:** [Argument Value Resolvers](../controllers/value-resolvers.md) ·
    **Mode:** TDD

## 🧠 Pour les nuls

**C'est quoi ce lab ?** Construire ton propre "traducteur" d'arguments de contrôleur — un composant qui transforme automatiquement des données brutes de la requête en un objet PHP typé prêt à l'emploi.

**Pourquoi ça existe ?** Les résolveurs intégrés couvrent les cas courants, mais un vrai projet a souvent besoin d'un type d'argument sur mesure — savoir en écrire un est un signe de maîtrise Expert.

**🏠 Analogie de la vraie vie :** Un traducteur spécialisé supplémentaire qu'on ajoute à une équipe existante : il ne remplace pas les autres, il prend en charge un cas précis (ici, transformer des paramètres de pagination) et laisse passer poliment tout le reste.

**Symfony dans la vraie vie :** Ton résolveur doit "décliner" (ne rien produire) pour tout argument qui n'est pas de son ressort, afin que la chaîne de résolveurs intégrés continue de fonctionner normalement pour les autres arguments.

**⚠️ Erreur fréquente :** oublier `#[ValueResolver(...)]` ou l'autoconfiguration par tag — sans ça, ton résolveur n'est jamais appelé, même s'il est parfaitement écrit.

**🧠 Comment le mémoriser :** "Un bon résolveur sait dire non poliment — il décline plutôt que de planter sur ce qui n'est pas de son ressort."


## Objective

À l'issue de ce lab, vous saurez **écrire, tester et brancher un value resolver de qualité production**.
Concrètement, vous serez capable de :

- Transformer les données de la query string en un value object `Pagination` typé et
  immuable que le kernel injecte comme argument de controller.
- Faire en sorte que le resolver **se désiste** (ne yield rien) pour tout argument qui
  ne le concerne pas, afin que la chaîne intégrée continue de fonctionner.
- Convertir la violation d'un invariant métier en `BadRequestHttpException` (400).
- Laisser Symfony **autoconfigurer** le resolver via le tag
  `controller.argument_value_resolver`, et éventuellement l'épingler avec
  `#[ValueResolver(...)]`.

## Prerequisites

- Chapitres : [Argument Value Resolvers](../controllers/value-resolvers.md),
  [The Request](../controllers/request.md),
  [Dependency Injection](../dependency-injection/index.md).
- Compétences supposées acquises : bases de PHPUnit, générateurs PHP (`yield`), classes
  readonly et promotion de constructeur, la chaîne de priorité des resolvers.

## TD Instructions

Travaillez en test-first. N'ouvrez **pas** la solution de référence avant d'être au vert.

1. Créez un value object immuable `App\Model\Pagination` avec `int $page = 1` et
   `int $perPage = 20`, promus et `readonly`. Faites respecter les invariants dans le
   constructeur : `page >= 1` et `1 <= perPage <= 100`, en levant
   `\InvalidArgumentException` sinon. Ajoutez un helper `offset(): int`.
2. Écrivez d'abord le test en échec `App\Tests\Resolver\PaginationResolverTest`. Construisez
   une `Request` avec `Request::create('/items?page=3&perPage=25')` et un
   `ArgumentMetadata` décrivant un argument typé `Pagination`. Vérifiez que
   `resolve()` yield **exactement un** `Pagination` avec les valeurs attendues.
3. Ajoutez un test prouvant que le resolver **ne yield rien** quand le type de l'argument
   n'est pas `Pagination` (par ex. `string`) — le résultat doit être un tableau vide.
4. Ajoutez un test pour le **chemin d'erreur** : `?page=0` doit lever une `HttpException`
   dont le code est `400`. Rappelez-vous que `resolve()` est un générateur — consommez-le
   (par ex. `iterator_to_array(...)`), sinon son corps ne s'exécute jamais.
5. Lancez la suite et regardez-la passer au **rouge**. Implémentez seulement maintenant
   `App\Resolver\PaginationResolver implements ValueResolverInterface`.
6. Dans `resolve()` : protégez `Pagination::class !== $argument->getType()` avec un simple
   `return;` (générateur vide). Lisez `page`/`perPage` via `$request->query->getInt()`
   avec les mêmes valeurs par défaut, construisez le `Pagination`, et traduisez toute
   `\InvalidArgumentException` en `BadRequestHttpException`.
7. Passez au **vert**. Branchez-le ensuite sur un argument de controller et vérifiez que
   l'autoconfiguration a bien appliqué le tag (`debug:container --tag=controller.argument_value_resolver`).

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · aucune bibliothèque hors du périmètre de la certification ·
    respectez les bonnes pratiques (attributs, strict types, `readonly` quand c'est pertinent).

## Implementation Guide (partial)

Uniquement des repères de haut niveau — pas le code complet.

- **Interface :** `Symfony\Component\HttpKernel\Controller\ValueResolverInterface`
  avec l'unique méthode `resolve(Request $request, ArgumentMetadata $argument): iterable`.
  L'ancienne interface scindée `ArgumentValueResolverInterface` (`supports()` + `resolve()`)
  a été **supprimée** en Symfony 8 — ne l'utilisez pas.
- **Métadonnées :** `Symfony\Component\HttpKernel\ControllerMetadata\ArgumentMetadata`.
  Son constructeur est `(string $name, ?string $type, bool $isVariadic, bool
  $hasDefaultValue, mixed $defaultValue, bool $isNullable = false, array $attributes = [])`.
  Seul `$type` compte ici ; inspectez-le avec `$argument->getType()`.
- **Se désister :** un resolver signale « pas pour moi » en ne yieldant rien. Dans un
  générateur, un simple `return;` produit un iterable vide — jamais `return null;` et
  jamais d'exception.
- **Lire l'entrée :** `$request->query` est un `InputBag` ; `getInt('page', 1)` fournit
  une valeur par défaut typée sans code de cast superflu.
- **Erreurs :** `Symfony\Component\HttpKernel\Exception\BadRequestHttpException`
  porte un statut `400`. Enveloppez la `\InvalidArgumentException` métier comme son previous.
- **Câblage :** implémenter l'interface suffit — Symfony autoconfigure le tag
  `controller.argument_value_resolver`. Ne définissez une `priority` explicite que si
  vous devez passer avant un resolver intégré.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** écrivez le test en échec ci-dessous ; lancez-le, regardez-le échouer (pas encore de resolver).
    2. **Green :** écrivez le minimum de code pour le faire passer.
    3. **Refactor :** nettoyez avec le test comme filet de sécurité.

**Comportement (Given/When/Then) :**

- **Given** une request `/items?page=3&perPage=25` et un argument typé `Pagination`,
  **When** `resolve()` s'exécute, **Then** il yield un `Pagination(3, 25)`.
- **Given** un argument typé `string`, **When** `resolve()` s'exécute, **Then** il ne
  yield rien (iterable vide) afin que le resolver suivant s'en charge.
- **Given** `/items?page=0`, **When** `resolve()` est consommé, **Then** il lève une
  `HttpException` avec le code `400`.

```php
<?php
declare(strict_types=1);

namespace App\Tests\Resolver;

use App\Model\Pagination;
use App\Resolver\PaginationResolver;
use PHPUnit\Framework\TestCase;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpKernel\ControllerMetadata\ArgumentMetadata;
use Symfony\Component\HttpKernel\Exception\HttpException;

final class PaginationResolverTest extends TestCase
{
    private PaginationResolver $resolver;

    protected function setUp(): void
    {
        $this->resolver = new PaginationResolver();
    }

    /** Build the metadata the kernel would pass for a `Pagination $p` argument. */
    private function metadataForType(?string $type): ArgumentMetadata
    {
        return new ArgumentMetadata('pagination', $type, false, false, null);
    }

    public function testResolvesPaginationFromQueryString(): void
    {
        $request = Request::create('/items?page=3&perPage=25');

        $resolved = iterator_to_array(
            $this->resolver->resolve($request, $this->metadataForType(Pagination::class))
        );

        self::assertCount(1, $resolved);
        self::assertInstanceOf(Pagination::class, $resolved[0]);
        self::assertSame(3, $resolved[0]->page);
        self::assertSame(25, $resolved[0]->perPage);
        self::assertSame(50, $resolved[0]->offset());
    }

    public function testFallsBackToDefaultsWhenAbsent(): void
    {
        $request = Request::create('/items');

        $resolved = iterator_to_array(
            $this->resolver->resolve($request, $this->metadataForType(Pagination::class))
        );

        self::assertSame(1, $resolved[0]->page);
        self::assertSame(20, $resolved[0]->perPage);
    }

    public function testYieldsNothingForUnsupportedType(): void
    {
        $request = Request::create('/items?page=3');

        $resolved = iterator_to_array(
            $this->resolver->resolve($request, $this->metadataForType('string'))
        );

        self::assertSame([], $resolved); // declined → next resolver handles it
    }

    public function testRejectsOutOfRangeValuesWith400(): void
    {
        $request = Request::create('/items?page=0');

        $this->expectException(HttpException::class);
        $this->expectExceptionCode(400);

        // resolve() is a generator: it only runs when consumed.
        iterator_to_array(
            $this->resolver->resolve($request, $this->metadataForType(Pagination::class))
        );
    }
}
```

!!! tip "Setup hints"
    Lancez-le : `vendor/bin/phpunit tests/Resolver/PaginationResolverTest.php`. Aucun mock
    nécessaire — `Request::create()` fournit une vraie request et `ArgumentMetadata` est un
    simple value object que vous pouvez instancier avec `new`. Pour exercer `resolve()`, vous
    **devez** itérer le générateur (`iterator_to_array`), sinon son corps — y compris le
    throw — ne s'exécute jamais.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/Resolver/PaginationResolverTest.php` est au vert (4 tests).
- [ ] `php bin/console debug:container --tag=controller.argument_value_resolver`
      liste `App\Resolver\PaginationResolver` (preuve que l'autoconfiguration l'a taggé).
- [ ] `curl -s 'http://localhost:8000/items?page=3&perPage=25'` →
      `{"page":3,"perPage":25,"offset":50}`.
- [ ] `curl -s -o /dev/null -w '%{http_code}\n' 'http://localhost:8000/items?page=0'`
      retourne `400`.
- [ ] Profiler → le panneau *Request/Response* montre que l'argument a été résolu par
      `PaginationResolver`.

## Review — Common Mistakes

- **Implémenter `ArgumentValueResolverInterface`** → elle a été supprimée en Symfony 8, la
  classe ne sera donc pas reconnue. Correction : implémentez `ValueResolverInterface` avec
  l'unique méthode `resolve(): iterable`.
- **`return null;` / `return false;` / `return [];` mélangés avec `yield`** → dès qu'une
  méthode contient `yield`, c'est un générateur ; un simple `return;` ne yield rien. Ne faites
  pas `return $value;` depuis un générateur (erreur fatale) — utilisez `yield $value;` à la place.
- **Tester `resolve()` sans le consommer** → l'assertion « passe » parce que le corps du
  générateur ne s'est jamais exécuté et qu'aucune exception n'est levée. Faites toujours
  `iterator_to_array(...)` (ou `foreach`) sur le résultat.
- **Lever une exception quand le type ne correspond pas** → cela casse tous les autres
  arguments de controller. Désistez-vous en ne yieldant rien ; ne levez une exception que pour
  des *données invalides de votre propre type*.
- **Pousser `priority` à 999** → inutile ici (le type est unique). Les priorités élevées
  servent à masquer un resolver intégré, pas aux resolvers ordinaires.
- **Mal utiliser `getInt`** → `$request->query->getInt('page', 1)` ne retourne la valeur par
  défaut que si la clé est absente ; `?page=0` est présent et donne `0`, que votre invariant
  doit rejeter.

## Exam Connection

La certification sonde les value resolvers exactement sur ces points :

- Le **nom et la forme de l'interface** — `ValueResolverInterface::resolve(): iterable`,
  et *non* la paire supprimée `supports()`/`resolve()`.
- **Comment un resolver se désiste** — en ne yieldant rien, jamais via un retour de `supports()`.
- **Tag vs targeted** — `controller.argument_value_resolver` (chaîne, autoconfiguré)
  vs `controller.targeted_value_resolver` (attribut uniquement, par ex.
  `#[MapRequestPayload]`). Ce lab utilise le tag de la chaîne.
- **`#[ValueResolver(Resolver::class)]`** épingle la résolution d'un argument à un seul
  resolver (et `disabled: true` permet de s'en exclure) — un piège favori.
- **Codes de statut** — les échecs d'invariant/de validation ressortent en `4xx` (ici `400`
  via `BadRequestHttpException` ; `#[MapRequestPayload]` utilise `422`).

## Ideal Solution

??? success "Reference solution (compare only after you try)"

    **Le value object** — `src/Model/Pagination.php`

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Model;

    /**
     * Immutable pagination window derived from the request query string.
     * Invariants are enforced in the constructor.
     */
    final readonly class Pagination
    {
        public function __construct(
            public int $page = 1,
            public int $perPage = 20,
        ) {
            if ($page < 1) {
                throw new \InvalidArgumentException(\sprintf('page must be >= 1, got %d.', $page));
            }
            if ($perPage < 1 || $perPage > 100) {
                throw new \InvalidArgumentException(\sprintf('perPage must be between 1 and 100, got %d.', $perPage));
            }
        }

        public function offset(): int
        {
            return ($this->page - 1) * $this->perPage;
        }
    }
    ```

    **Le resolver** — `src/Resolver/PaginationResolver.php`

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Resolver;

    use App\Model\Pagination;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpKernel\Controller\ValueResolverInterface;
    use Symfony\Component\HttpKernel\ControllerMetadata\ArgumentMetadata;
    use Symfony\Component\HttpKernel\Exception\BadRequestHttpException;

    final class PaginationResolver implements ValueResolverInterface
    {
        /**
         * @return iterable<Pagination>
         */
        public function resolve(Request $request, ArgumentMetadata $argument): iterable
        {
            // Not our type? Yield nothing so the chain continues.
            if (Pagination::class !== $argument->getType()) {
                return;
            }

            $page = $request->query->getInt('page', 1);
            $perPage = $request->query->getInt('perPage', 20);

            try {
                yield new Pagination($page, $perPage);
            } catch (\InvalidArgumentException $e) {
                // Turn a domain invariant into a 400 the kernel understands.
                throw new BadRequestHttpException($e->getMessage(), $e);
            }
        }
    }
    ```

    **Utilisation dans un controller** — `src/Controller/ItemController.php`

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use App\Model\Pagination;
    use App\Resolver\PaginationResolver;
    use Symfony\Component\HttpFoundation\JsonResponse;
    use Symfony\Component\HttpKernel\Attribute\ValueResolver;
    use Symfony\Component\Routing\Attribute\Route;

    final class ItemController
    {
        // Autoconfigured: the resolver matches by type, no attribute required.
        #[Route('/items', name: 'items_list', methods: ['GET'])]
        public function list(Pagination $pagination): JsonResponse
        {
            return new JsonResponse([
                'page' => $pagination->page,
                'perPage' => $pagination->perPage,
                'offset' => $pagination->offset(),
            ]);
        }

        // Optional: pin the exact resolver for this argument.
        #[Route('/pinned', name: 'items_pinned', methods: ['GET'])]
        public function pinned(
            #[ValueResolver(PaginationResolver::class)] Pagination $pagination,
        ): JsonResponse {
            return new JsonResponse(['offset' => $pagination->offset()]);
        }
    }
    ```

    **Câblage** — l'autoconfiguration suffit ; le tag explicite n'est nécessaire que pour
    forcer une priorité.

    === "Autoconfiguration (default)"

        ```yaml
        # config/services.yaml
        services:
            _defaults:
                autowire: true
                autoconfigure: true   # implements ValueResolverInterface → tagged automatically

            App\:
                resource: '../src/'
        ```

    === "Explicit tag / priority"

        ```yaml
        # config/services.yaml — only if you must run before a built-in resolver
        services:
            App\Resolver\PaginationResolver:
                tags:
                    - { name: controller.argument_value_resolver, priority: 150 }
        ```

    === "Console check"

        ```console
        $ php bin/console debug:container --tag=controller.argument_value_resolver
         ------------------------------------------- ----------
          Service ID                                  priority
         ------------------------------------------- ----------
          App\Resolver\PaginationResolver             0
          ...built-in resolvers...
         ------------------------------------------- ----------
        ```

## Alternative Approaches (optional)

- **Option A (simple, intégrée) :** pour deux scalaires, faites l'économie du resolver
  personnalisé — `list(#[MapQueryParameter] int $page = 1, #[MapQueryParameter] int $perPage = 20)`.
  N'écrivez un resolver personnalisé que lorsque le value object est réutilisé dans plusieurs controllers.
- **Option B (avancée, validation via Serializer/Validator) :** modélisez `Pagination`
  comme un DTO avec des contraintes `#[Assert\Range]` et liez-le avec `#[MapQueryString]` ;
  une entrée invalide produit alors un `422` via `RequestPayloadValueResolver` au lieu d'un
  `400` fait main.
- **Option C (style examen, targeted resolver) :** définissez un attribut `#[Paginated]` et
  faites-le lire par le resolver via `$argument->getAttributes(Paginated::class)`, taggé
  `controller.targeted_value_resolver` afin qu'il ne se déclenche que lorsque l'attribut est présent.

---

<small>Theory: [Argument Value Resolvers](../controllers/value-resolvers.md) · Labs: [all labs](index.md)</small>
