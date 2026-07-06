---
tags:
  - Labs
  - Dependency Injection
---

# Lab: Compiler Pass — A Tag-Driven Handler Registry

<!-- TDD lab: code behaviour (a CompilerPass + registry you can compile and assert on). -->

!!! abstract "Practical Lab"
    **Objective:** collect every service carrying a tag and inject it, in
    priority order, into a registry — assembled by your own compiler pass ·
    **Difficulty:** Advanced ·
    **Theory:** [Compiler passes](../dependency-injection/compiler-passes.md) ·
    [Tags](../dependency-injection/tags.md) ·
    **Mode:** TDD

## Objective

After this lab you can build the classic Symfony extension point: a **registry**
populated from **tagged services** by a **compiler pass**. Concretely you will be
able to:

- Implement `CompilerPassInterface::process()` and read tags with
  `findTaggedServiceIds()`.
- Rewrite a collector `Definition` with `addMethodCall()` + `Reference`, ordered by
  the tag's `priority`.
- Register the pass in `Kernel::build()` — proving to yourself there is **no
  `#[CompilerPass]` attribute**.
- Drive the whole thing from a `ContainerBuilder` in a unit test: register
  definitions, `->compile()`, assert the registry received the right services in
  the right order.

## Prerequisites

- Chapters: [Compiler passes](../dependency-injection/compiler-passes.md) ·
  [Tags](../dependency-injection/tags.md) ·
  [The Service Container](../dependency-injection/container.md)
- Assumed skills: PHP 8.4 (interfaces, `usort`, spaceship operator), basic PHPUnit,
  what a `Definition` and a `Reference` are.

## TD Instructions

You are wiring a message/handler subsystem. Handlers implement a common interface
and each is tagged `app.handler`. A `HandlerRegistry` must receive them all, sorted
so the **highest `priority` comes first**. No `services.yaml` autowiring magic — you
assemble the registry yourself with a compiler pass.

1. Define `App\Handler\HandlerInterface` with `getName(): string` (static) and
   `handle(string $payload): string`.
2. Define `App\Handler\HandlerRegistry` with `add(HandlerInterface $h): void`, a
   `names(): array` accessor (for assertions), and a `get(string $name)` lookup.
3. **Write the failing test first** (see the TDD block): build a `ContainerBuilder`,
   `register()` the registry + two handler `Definition`s tagged `app.handler` with
   different `priority` values, `addCompilerPass(...)`, then `compile()`.
4. Assert that `$registry->names()` returns the two handlers **in descending
   priority order**. Run it — it must fail (red): the pass does not exist yet.
5. Implement `App\DependencyInjection\HandlerCompilerPass` (implements
   `CompilerPassInterface`). Guard with `has()`, loop `findTaggedServiceIds(...)`,
   read `priority`, sort descending, and `addMethodCall('add', [new Reference($id)])`
   on the registry definition. Make the test pass (green).
6. Register the pass in `App\Kernel::build(ContainerBuilder $container)` with
   `addCompilerPass()`. Confirm there is **no attribute** that would do this for you.
7. **Refactor** with the test as a safety net (extract the sort, tidy names).

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · no libraries outside the certification scope · follow
    best practices (attributes, strict types, `readonly`/typed properties where apt).

## Implementation Guide (partial)

High-level pointers — not the full code:

- **Interface & registry** live under `App\Handler\`. The registry just accumulates
  `HandlerInterface` instances in an array; order is decided by the pass, not the
  registry.
- **The pass** implements
  `Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface`. Its only
  method is `process(ContainerBuilder $container): void`.
  - `findTaggedServiceIds('app.handler')` returns
    `['service_id' => [ ['priority' => 100], ... ], ...]` — the id mapped to **each
    occurrence** of the tag with its attributes.
  - Read the priority as `$tags[0]['priority'] ?? 0`, collect `[id, priority]`, then
    `usort()` descending on priority (spaceship `<=>`, reversed operands).
  - Mutate the collector: `$container->findDefinition(HandlerRegistry::class)
    ->addMethodCall('add', [new Reference($id)])`. Use a **`Reference`**, never a
    real instance — compilation deals with `Definition`s only.
- **Registration** is programmatic in `Kernel::build()`. Default phase
  (`TYPE_BEFORE_OPTIMIZATION`) is correct here.
- **Test wiring gotcha:** in a raw `ContainerBuilder`, autoconfiguration does *not*
  run, so tag the definitions **manually** with `->addTag()`. Mark the registry
  `->setPublic(true)` so you can `$container->get()` it after `compile()` prunes
  private services.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** write the failing test below; run it, watch it fail (no pass yet).
    2. **Green:** implement `HandlerCompilerPass` + `HandlerRegistry` to pass.
    3. **Refactor:** extract the priority sort; keep the test green.

**Behaviour (Given/When/Then):**

- **Given** a `ContainerBuilder` with a public `HandlerRegistry` and two services
  tagged `app.handler` (`handler.low` priority `10`, `handler.high` priority `100`),
- **When** the `HandlerCompilerPass` runs during `->compile()`,
- **Then** the registry has both handlers and `names()` returns
  `['high', 'low']` — highest priority first.

```php
<?php
declare(strict_types=1);

namespace App\Tests\DependencyInjection;

use App\DependencyInjection\HandlerCompilerPass;
use App\Handler\HandlerInterface;
use App\Handler\HandlerRegistry;
use PHPUnit\Framework\TestCase;
use Symfony\Component\DependencyInjection\ContainerBuilder;

final class HandlerCompilerPassTest extends TestCase
{
    public function testTaggedHandlersAreCollectedInPriorityOrder(): void
    {
        // Arrange: a real ContainerBuilder — the pass acts on Definitions.
        $container = new ContainerBuilder();

        // The collector — public so we can fetch it after compilation.
        $container->register(HandlerRegistry::class, HandlerRegistry::class)
            ->setPublic(true);

        // Two tagged handlers. In a raw ContainerBuilder autoconfiguration does
        // NOT run, so we tag the definitions by hand. Higher priority = first.
        $container->register('handler.low', LowHandler::class)
            ->addTag('app.handler', ['priority' => 10]);

        $container->register('handler.high', HighHandler::class)
            ->addTag('app.handler', ['priority' => 100]);

        // Act: register the pass and compile.
        $container->addCompilerPass(new HandlerCompilerPass());
        $container->compile();

        /** @var HandlerRegistry $registry */
        $registry = $container->get(HandlerRegistry::class);

        // Assert: collected AND ordered high-priority first.
        self::assertSame(['high', 'low'], $registry->names());
        self::assertSame('handled:x', $registry->get('high')->handle('x'));
    }
}

// --- Test fixtures ---------------------------------------------------------

final class HighHandler implements HandlerInterface
{
    public static function getName(): string
    {
        return 'high';
    }

    public function handle(string $payload): string
    {
        return 'handled:'.$payload;
    }
}

final class LowHandler implements HandlerInterface
{
    public static function getName(): string
    {
        return 'low';
    }

    public function handle(string $payload): string
    {
        return 'handled:'.$payload;
    }
}
```

!!! tip "Setup hints"
    Run it with `vendor/bin/phpunit tests/DependencyInjection/HandlerCompilerPassTest.php`.
    No kernel, no `KernelTestCase` — a plain `ContainerBuilder` is enough because a
    compiler pass is pure build-time logic. Keep fixtures in the test file (same
    namespace) so the test is self-contained.

## Validation Steps

Beyond the green test, sanity-check the wiring in a real app:

- [ ] `php bin/console debug:container --tag=app.handler` lists both services.
- [ ] `php bin/console debug:container HandlerRegistry --show-arguments` shows the
      `add()` method calls the pass added.
- [ ] Remove the `addCompilerPass()` line from `Kernel::build()` → the method calls
      disappear (proving *nothing* wires them automatically — there is no attribute).

## Review — Common Mistakes

- **Looking for `#[CompilerPass]`.** It does not exist. → Register with
  `$container->addCompilerPass(new HandlerCompilerPass())` in `Kernel::build()` (or a
  bundle's `build()`).
- **`$container->get($id)` inside `process()`.** At compile time nothing is
  instantiated. → Pass a `new Reference($id)`; the container resolves it later.
- **Forgetting the `has()` guard.** If the registry is absent (bundle disabled), the
  pass crashes. → `if (!$container->has(HandlerRegistry::class)) { return; }`.
- **Registry private in the test.** After `compile()` the removing pass prunes
  private services, so `$container->get()` throws. → `->setPublic(true)` in the test.
- **Expecting autoconfiguration in a raw `ContainerBuilder`.** `#[AutoconfigureTag]`
  only applies inside a booted kernel. → In the unit test, `->addTag()` manually.
- **Priority sorted the wrong way.** Higher priority must come **first**. → Sort
  descending: `$b['priority'] <=> $a['priority']`.

## Exam Connection

This is the single most exam-relevant DI pattern. The certification loves to check:

- **No `#[CompilerPass]` attribute** — registration is always programmatic in
  `build()`.
- **`findTaggedServiceIds()` returns id → array of tag-attribute sets**, not
  instances and not a locator.
- **Higher `priority` runs earlier** in the resulting collection.
- **Passes manipulate `Definition`s at compile time** — `Reference`, never `get()`.
- The default phase is **`TYPE_BEFORE_OPTIMIZATION`**.

If you can write this pass from memory and explain each choice, you own the topic.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    ```php
    <?php
    declare(strict_types=1);

    // src/Handler/HandlerInterface.php
    namespace App\Handler;

    use Symfony\Component\DependencyInjection\Attribute\AutoconfigureTag;

    // In a real kernel this attribute auto-applies the tag to every implementor.
    // (In the unit test we tag definitions manually — autoconfigure doesn't run there.)
    #[AutoconfigureTag('app.handler')]
    interface HandlerInterface
    {
        public static function getName(): string;

        public function handle(string $payload): string;
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    // src/Handler/HandlerRegistry.php
    namespace App\Handler;

    final class HandlerRegistry
    {
        /** @var list<HandlerInterface> */
        private array $handlers = [];

        public function add(HandlerInterface $handler): void
        {
            $this->handlers[] = $handler;
        }

        /** @return list<string> handler names in registration (priority) order */
        public function names(): array
        {
            return array_map(
                static fn (HandlerInterface $h): string => $h::getName(),
                $this->handlers,
            );
        }

        public function get(string $name): HandlerInterface
        {
            foreach ($this->handlers as $handler) {
                if ($handler::getName() === $name) {
                    return $handler;
                }
            }

            throw new \InvalidArgumentException(\sprintf('No handler named "%s".', $name));
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    // src/DependencyInjection/HandlerCompilerPass.php
    namespace App\DependencyInjection;

    use App\Handler\HandlerRegistry;
    use Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface;
    use Symfony\Component\DependencyInjection\ContainerBuilder;
    use Symfony\Component\DependencyInjection\Reference;

    final class HandlerCompilerPass implements CompilerPassInterface
    {
        public function process(ContainerBuilder $container): void
        {
            // Guard: the collector may be absent (bundle disabled, test isolation).
            if (!$container->has(HandlerRegistry::class)) {
                return;
            }

            $registry = $container->findDefinition(HandlerRegistry::class);

            // findTaggedServiceIds() => [ 'service_id' => [ ['priority' => N], ... ] ]
            $handlers = [];
            foreach ($container->findTaggedServiceIds('app.handler') as $id => $tags) {
                $handlers[] = ['id' => $id, 'priority' => $tags[0]['priority'] ?? 0];
            }

            // Higher priority runs FIRST — sort descending.
            usort(
                $handlers,
                static fn (array $a, array $b): int => $b['priority'] <=> $a['priority'],
            );

            foreach ($handlers as $handler) {
                // A Reference, never an instance: this is build time.
                $registry->addMethodCall('add', [new Reference($handler['id'])]);
            }
        }
    }
    ```

    ```php
    <?php
    declare(strict_types=1);

    // src/Kernel.php
    namespace App;

    use App\DependencyInjection\HandlerCompilerPass;
    use Symfony\Bundle\FrameworkBundle\Kernel\MicroKernelTrait;
    use Symfony\Component\DependencyInjection\Compiler\PassConfig;
    use Symfony\Component\DependencyInjection\ContainerBuilder;
    use Symfony\Component\HttpKernel\Kernel as BaseKernel;

    final class Kernel extends BaseKernel
    {
        use MicroKernelTrait;

        // Register the pass HERE — there is NO #[CompilerPass] attribute.
        protected function build(ContainerBuilder $container): void
        {
            $container->addCompilerPass(
                new HandlerCompilerPass(),
                PassConfig::TYPE_BEFORE_OPTIMIZATION,
                priority: 0,
            );
        }
    }
    ```

## Alternative Approaches

- **Option A (simplest) — `tagged_iterator`.** If you only need *"inject all
  services with this tag, priority-ordered"*, you do not need a pass at all. Give the
  registry a `#[AutowireIterator('app.handler')] iterable $handlers` argument (or a
  `!tagged_iterator app.handler` in YAML). Core passes do the collection and sorting.
  See [Tags](../dependency-injection/tags.md).
- **Option B (idiomatic pass) — `findAndSortTaggedServices()`.** Instead of sorting
  by hand, `use` Symfony's
  `Symfony\Component\DependencyInjection\Compiler\PriorityTaggedServiceTrait` and call
  `$this->findAndSortTaggedServices('app.handler', $container)` — it returns
  `Reference`s already ordered by descending priority. Loop them into
  `addMethodCall('add', [$ref])`.
- **Option C (exam-style twist) — keyed registry.** Read a custom tag attribute
  (e.g. `['key' => 'sms']`) in `process()` and build a keyed map, or expose the
  handlers as a `ServiceLocator` via `#[AutowireLocator('app.handler',
  defaultIndexMethod: 'getName')]` for lazy, keyed lookup.

---

<small>Theory: [Compiler passes](../dependency-injection/compiler-passes.md) ·
[Tags](../dependency-injection/tags.md) · Labs: [all labs](index.md)</small>
