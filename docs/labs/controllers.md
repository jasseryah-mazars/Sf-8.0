---
tags:
  - Labs
  - Controllers
---

# Lab: Custom Value Resolver — hydrate a controller argument from the Request

!!! abstract "Practical Lab"
    **Objective:** implement a custom `ValueResolverInterface` that hydrates a
    value object straight into a controller argument, declines cleanly for other
    types, and maps a broken invariant to a `400` ·
    **Difficulty:** Advanced ·
    **Theory:** [Argument Value Resolvers](../controllers/value-resolvers.md) ·
    **Mode:** TDD

## Objective

After this lab you can **write, test, and wire a production-grade value resolver**.
Concretely you will be able to:

- Turn query-string data into a typed, immutable `Pagination` value object that the
  kernel injects as a controller argument.
- Make the resolver **decline** (yield nothing) for any argument it does not own, so
  the built-in chain keeps working.
- Convert a domain invariant violation into a `BadRequestHttpException` (400).
- Let Symfony **autoconfigure** the resolver via the
  `controller.argument_value_resolver` tag, and optionally pin it with
  `#[ValueResolver(...)]`.

## Prerequisites

- Chapters: [Argument Value Resolvers](../controllers/value-resolvers.md),
  [The Request](../controllers/request.md),
  [Dependency Injection](../dependency-injection/index.md).
- Assumed skills: PHPUnit basics, PHP generators (`yield`), readonly classes and
  constructor promotion, the resolver priority chain.

## TD Instructions

Work test-first. Do **not** open the reference solution until you are green.

1. Create an immutable `App\Model\Pagination` value object with `int $page = 1` and
   `int $perPage = 20`, promoted and `readonly`. Enforce the invariants in the
   constructor: `page >= 1` and `1 <= perPage <= 100`, throwing
   `\InvalidArgumentException` otherwise. Add an `offset(): int` helper.
2. Write the failing test `App\Tests\Resolver\PaginationResolverTest` first. Build a
   `Request` with `Request::create('/items?page=3&perPage=25')` and an
   `ArgumentMetadata` describing a `Pagination`-typed argument. Assert that
   `resolve()` yields **exactly one** `Pagination` with the expected values.
3. Add a test proving the resolver **yields nothing** when the argument type is not
   `Pagination` (e.g. `string`) — the result must be an empty array.
4. Add a test for the **error path**: `?page=0` must raise an `HttpException` whose
   code is `400`. Remember `resolve()` is a generator — consume it (e.g.
   `iterator_to_array(...)`) or the body never runs.
5. Run the suite and watch it go **red**. Only now implement
   `App\Resolver\PaginationResolver implements ValueResolverInterface`.
6. In `resolve()`: guard `Pagination::class !== $argument->getType()` with a bare
   `return;` (empty generator). Read `page`/`perPage` via `$request->query->getInt()`
   with the same defaults, build the `Pagination`, and translate any
   `\InvalidArgumentException` into a `BadRequestHttpException`.
7. Go **green**. Then wire it into a controller argument and confirm autoconfiguration
   picks up the tag (`debug:container --tag=controller.argument_value_resolver`).

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · no libraries outside the certification scope · follow
    best practices (attributes, strict types, `readonly` where apt).

## Implementation Guide (partial)

High-level pointers only — not the full code.

- **Interface:** `Symfony\Component\HttpKernel\Controller\ValueResolverInterface`
  with the single method `resolve(Request $request, ArgumentMetadata $argument): iterable`.
  The old split `ArgumentValueResolverInterface` (`supports()` + `resolve()`) was
  **removed** in Symfony 8 — do not use it.
- **Metadata:** `Symfony\Component\HttpKernel\ControllerMetadata\ArgumentMetadata`.
  Its constructor is `(string $name, ?string $type, bool $isVariadic, bool
  $hasDefaultValue, mixed $defaultValue, bool $isNullable = false, array $attributes = [])`.
  Only `$type` matters here; inspect it with `$argument->getType()`.
- **Declining:** a resolver signals "not mine" by yielding nothing. In a generator, a
  bare `return;` produces an empty iterable — never `return null;` and never throw.
- **Reading input:** `$request->query` is an `InputBag`; `getInt('page', 1)` gives a
  typed default without casting boilerplate.
- **Errors:** `Symfony\Component\HttpKernel\Exception\BadRequestHttpException`
  carries a `400` status. Wrap the domain `\InvalidArgumentException` as its previous.
- **Wiring:** implementing the interface is enough — Symfony autoconfigures the
  `controller.argument_value_resolver` tag. Set an explicit `priority` only if you
  must run before a built-in resolver.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** write the failing test below; run it, watch it fail (no resolver yet).
    2. **Green:** write the minimum code to pass.
    3. **Refactor:** clean up with the test as your safety net.

**Behaviour (Given/When/Then):**

- **Given** a request `/items?page=3&perPage=25` and a `Pagination`-typed argument,
  **When** `resolve()` runs, **Then** it yields one `Pagination(3, 25)`.
- **Given** a `string`-typed argument, **When** `resolve()` runs, **Then** it yields
  nothing (empty iterable) so the next resolver handles it.
- **Given** `/items?page=0`, **When** `resolve()` is consumed, **Then** it throws an
  `HttpException` with code `400`.

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
    Run it: `vendor/bin/phpunit tests/Resolver/PaginationResolverTest.php`. No mocks
    needed — `Request::create()` gives a real request and `ArgumentMetadata` is a
    plain value object you can `new`. To exercise `resolve()` you **must** iterate the
    generator (`iterator_to_array`), otherwise its body — including the throw — never
    executes.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/Resolver/PaginationResolverTest.php` is green (4 tests).
- [ ] `php bin/console debug:container --tag=controller.argument_value_resolver`
      lists `App\Resolver\PaginationResolver` (proof autoconfiguration tagged it).
- [ ] `curl -s 'http://localhost:8000/items?page=3&perPage=25'` →
      `{"page":3,"perPage":25,"offset":50}`.
- [ ] `curl -s -o /dev/null -w '%{http_code}\n' 'http://localhost:8000/items?page=0'`
      returns `400`.
- [ ] Profiler → *Request/Response* panel shows the argument was resolved by
      `PaginationResolver`.

## Review — Common Mistakes

- **Implementing `ArgumentValueResolverInterface`** → it was removed in Symfony 8, so
  the class won't be recognised. Fix: implement `ValueResolverInterface` with the
  single `resolve(): iterable` method.
- **`return null;` / `return false;` / `return [];` mixed with `yield`** → once a
  method contains `yield` it is a generator; a bare `return;` yields nothing. Do not
  `return $value;` from a generator (fatal) — `yield $value;` instead.
- **Testing `resolve()` without consuming it** → the assertion "passes" because the
  generator body never ran and no exception is thrown. Always
  `iterator_to_array(...)` (or `foreach`) the result.
- **Throwing when the type doesn't match** → that breaks every other controller
  argument. Decline by yielding nothing; only throw for *invalid data of your own
  type*.
- **Cranking `priority` to 999** → unnecessary here (the type is unique). High
  priorities are for shadowing a built-in, not routine resolvers.
- **Using `getInt` wrong** → `$request->query->getInt('page', 1)` returns the default
  only when the key is absent; `?page=0` is present and yields `0`, which your
  invariant must reject.

## Exam Connection

The certification probes value resolvers on exactly these points:

- The **interface name and shape** — `ValueResolverInterface::resolve(): iterable`,
  *not* the removed `supports()`/`resolve()` pair.
- **How a resolver declines** — by yielding nothing, never a `supports()` return.
- **Tag vs targeted** — `controller.argument_value_resolver` (chain, autoconfigured)
  vs `controller.targeted_value_resolver` (attribute-only, e.g.
  `#[MapRequestPayload]`). This lab uses the chain tag.
- **`#[ValueResolver(Resolver::class)]`** pins resolution to one resolver for an
  argument (and `disabled: true` opts out) — a favourite trap.
- **Status codes** — invariant/validation failures surface as `4xx` (here `400` via
  `BadRequestHttpException`; `#[MapRequestPayload]` uses `422`).

## Ideal Solution

??? success "Reference solution (compare only after you try)"

    **The value object** — `src/Model/Pagination.php`

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

    **The resolver** — `src/Resolver/PaginationResolver.php`

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

    **Using it in a controller** — `src/Controller/ItemController.php`

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

    **Wiring** — autoconfiguration is enough; the explicit tag is only needed to
    force a priority.

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

- **Option A (simple, built-in):** for two scalars, skip the custom resolver entirely
  — `list(#[MapQueryParameter] int $page = 1, #[MapQueryParameter] int $perPage = 20)`.
  Use a custom resolver only when the value object is reused across controllers.
- **Option B (advanced, validation via Serializer/Validator):** model `Pagination`
  as a DTO with `#[Assert\Range]` constraints and bind it with `#[MapQueryString]`;
  invalid input then yields `422` through `RequestPayloadValueResolver` instead of a
  hand-rolled `400`.
- **Option C (exam-style, targeted resolver):** define a `#[Paginated]` attribute and
  make the resolver read it via `$argument->getAttributes(Paginated::class)`, tagged
  `controller.targeted_value_resolver` so it fires only when the attribute is present.

---

<small>Theory: [Argument Value Resolvers](../controllers/value-resolvers.md) · Labs: [all labs](index.md)</small>
