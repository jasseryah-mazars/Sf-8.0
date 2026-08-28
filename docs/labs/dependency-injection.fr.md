---
tags:
  - Labs
  - Dependency Injection
---

# Lab: Compiler Pass — A Tag-Driven Handler Registry

<!-- TDD lab: code behaviour (a CompilerPass + registry you can compile and assert on). -->

!!! abstract "Practical Lab"
    **Objective :** collecter tous les services porteurs d'un tag et les injecter,
    par ordre de priorité, dans un registre — assemblé par votre propre compiler pass ·
    **Difficulty:** Advanced ·
    **Theory:** [Compiler passes](../dependency-injection/compiler-passes.md) ·
    [Tags](../dependency-injection/tags.md) ·
    **Mode:** TDD

## 🧠 Pour les nuls

**C'est quoi ce lab ?** Écrire un compiler pass qui collecte automatiquement tous les services portant une étiquette (tag) précise, et les assemble dans un registre — sans jamais lister ces services à la main.

**Pourquoi ça existe ?** Un projet peut avoir des dizaines de "handlers" ou de "providers" ajoutés au fil du temps — un compiler pass évite de maintenir une liste manuelle à jour à chaque ajout.

**🏠 Analogie de la vraie vie :** Un manager de cuisine qui fait sa ronde avant le service et rassemble toutes les fiches recettes portant l'étiquette "brunch" dans un même classeur — sans jamais avoir à connaître leur nombre exact à l'avance.

**Symfony dans la vraie vie :** `$container->findTaggedServiceIds('app.mon_tag')` retourne automatiquement tous les services tagués, même ceux ajoutés dans un bundle tiers après coup — ton registre reste toujours à jour.

**⚠️ Erreur fréquente :** oublier d'enregistrer le compiler pass dans `Kernel::build()` — sans cet enregistrement explicite, le pass n'est jamais exécuté, même s'il est parfaitement écrit.

**🧠 Comment le mémoriser :** "Un compiler pass rassemble à la compilation — jamais de liste à maintenir à la main."


## Objective

À l'issue de ce lab, vous saurez construire le point d'extension classique de Symfony :
un **registre** peuplé à partir de **services taggés** par un **compiler pass**.
Concrètement, vous serez capable de :

- Implémenter `CompilerPassInterface::process()` et lire les tags avec
  `findTaggedServiceIds()`.
- Réécrire une `Definition` collectrice avec `addMethodCall()` + `Reference`, ordonnée
  selon la `priority` du tag.
- Enregistrer le pass dans `Kernel::build()` — en vous prouvant à vous-même qu'il
  n'existe **aucun attribut `#[CompilerPass]`**.
- Piloter le tout depuis un `ContainerBuilder` dans un test unitaire : enregistrer des
  definitions, `->compile()`, vérifier que le registre a reçu les bons services dans
  le bon ordre.

## Prerequisites

- Chapitres : [Compiler passes](../dependency-injection/compiler-passes.md) ·
  [Tags](../dependency-injection/tags.md) ·
  [The Service Container](../dependency-injection/container.md)
- Compétences supposées acquises : PHP 8.4 (interfaces, `usort`, opérateur spaceship),
  bases de PHPUnit, ce que sont une `Definition` et une `Reference`.

## TD Instructions

Vous câblez un sous-système de messages/handlers. Les handlers implémentent une interface
commune et chacun est taggé `app.handler`. Un `HandlerRegistry` doit tous les recevoir,
triés de sorte que **la `priority` la plus élevée vienne en premier**. Pas de magie
d'autowiring dans `services.yaml` — vous assemblez le registre vous-même avec un compiler pass.

1. Définissez `App\Handler\HandlerInterface` avec `getName(): string` (statique) et
   `handle(string $payload): string`.
2. Définissez `App\Handler\HandlerRegistry` avec `add(HandlerInterface $h): void`, un
   accesseur `names(): array` (pour les assertions), et une recherche `get(string $name)`.
3. **Écrivez d'abord le test en échec** (voir le bloc TDD) : construisez un `ContainerBuilder`,
   `register()` le registre + deux `Definition`s de handlers taggées `app.handler` avec
   des valeurs de `priority` différentes, `addCompilerPass(...)`, puis `compile()`.
4. Vérifiez que `$registry->names()` retourne les deux handlers **par ordre de priorité
   décroissante**. Lancez le test — il doit échouer (rouge) : le pass n'existe pas encore.
5. Implémentez `App\DependencyInjection\HandlerCompilerPass` (implémente
   `CompilerPassInterface`). Protégez avec `has()`, bouclez sur `findTaggedServiceIds(...)`,
   lisez la `priority`, triez en décroissant, et appelez `addMethodCall('add', [new Reference($id)])`
   sur la definition du registre. Faites passer le test (vert).
6. Enregistrez le pass dans `App\Kernel::build(ContainerBuilder $container)` avec
   `addCompilerPass()`. Vérifiez qu'il n'existe **aucun attribut** qui le ferait pour vous.
7. **Refactorez** avec le test comme filet de sécurité (extrayez le tri, soignez les noms).

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · aucune bibliothèque hors du périmètre de la certification ·
    respectez les bonnes pratiques (attributs, strict types, propriétés `readonly`/typées
    quand c'est pertinent).

## Implementation Guide (partial)

Des repères de haut niveau — pas le code complet :

- **L'interface et le registre** vivent sous `App\Handler\`. Le registre se contente
  d'accumuler des instances de `HandlerInterface` dans un tableau ; l'ordre est décidé
  par le pass, pas par le registre.
- **Le pass** implémente
  `Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface`. Son unique
  méthode est `process(ContainerBuilder $container): void`.
  - `findTaggedServiceIds('app.handler')` retourne
    `['service_id' => [ ['priority' => 100], ... ], ...]` — l'id associé à **chaque
    occurrence** du tag avec ses attributs.
  - Lisez la priorité via `$tags[0]['priority'] ?? 0`, collectez `[id, priority]`, puis
    faites un `usort()` décroissant sur la priorité (spaceship `<=>`, opérandes inversés).
  - Mutez le collecteur : `$container->findDefinition(HandlerRegistry::class)
    ->addMethodCall('add', [new Reference($id)])`. Utilisez une **`Reference`**, jamais
    une vraie instance — la compilation ne manipule que des `Definition`s.
- **L'enregistrement** est programmatique dans `Kernel::build()`. La phase par défaut
  (`TYPE_BEFORE_OPTIMIZATION`) est la bonne ici.
- **Piège de câblage dans le test :** dans un `ContainerBuilder` brut, l'autoconfiguration
  ne s'exécute *pas* ; taggez donc les definitions **manuellement** avec `->addTag()`.
  Marquez le registre `->setPublic(true)` pour pouvoir faire `$container->get()` après que
  `compile()` a élagué les services privés.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** écrivez le test en échec ci-dessous ; lancez-le, regardez-le échouer (pas encore de pass).
    2. **Green :** implémentez `HandlerCompilerPass` + `HandlerRegistry` pour le faire passer.
    3. **Refactor :** extrayez le tri par priorité ; gardez le test au vert.

**Comportement (Given/When/Then) :**

- **Given** un `ContainerBuilder` avec un `HandlerRegistry` public et deux services
  taggés `app.handler` (`handler.low` priorité `10`, `handler.high` priorité `100`),
- **When** le `HandlerCompilerPass` s'exécute pendant `->compile()`,
- **Then** le registre contient les deux handlers et `names()` retourne
  `['high', 'low']` — la priorité la plus haute en premier.

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
    Lancez-le avec `vendor/bin/phpunit tests/DependencyInjection/HandlerCompilerPassTest.php`.
    Pas de kernel, pas de `KernelTestCase` — un simple `ContainerBuilder` suffit, car un
    compiler pass est de la pure logique de build. Gardez les fixtures dans le fichier de
    test (même namespace) pour que le test soit autonome.

## Validation Steps

Au-delà du test au vert, vérifiez le câblage dans une vraie application :

- [ ] `php bin/console debug:container --tag=app.handler` liste les deux services.
- [ ] `php bin/console debug:container HandlerRegistry --show-arguments` montre les
      appels de méthode `add()` ajoutés par le pass.
- [ ] Retirez la ligne `addCompilerPass()` de `Kernel::build()` → les appels de méthode
      disparaissent (preuve que *rien* ne les câble automatiquement — il n'y a pas d'attribut).

## Review — Common Mistakes

- **Chercher `#[CompilerPass]`.** Il n'existe pas. → Enregistrez avec
  `$container->addCompilerPass(new HandlerCompilerPass())` dans `Kernel::build()` (ou le
  `build()` d'un bundle).
- **`$container->get($id)` à l'intérieur de `process()`.** À la compilation, rien n'est
  instancié. → Passez une `new Reference($id)` ; le container la résoudra plus tard.
- **Oublier la garde `has()`.** Si le registre est absent (bundle désactivé), le pass
  plante. → `if (!$container->has(HandlerRegistry::class)) { return; }`.
- **Registre privé dans le test.** Après `compile()`, le pass de suppression élague les
  services privés, donc `$container->get()` lève une exception. → `->setPublic(true)` dans le test.
- **Attendre l'autoconfiguration dans un `ContainerBuilder` brut.** `#[AutoconfigureTag]`
  ne s'applique qu'au sein d'un kernel démarré. → Dans le test unitaire, `->addTag()` à la main.
- **Priorité triée dans le mauvais sens.** La priorité la plus élevée doit venir **en
  premier**. → Triez en décroissant : `$b['priority'] <=> $a['priority']`.

## Exam Connection

C'est LE pattern de DI le plus pertinent pour l'examen. La certification adore vérifier :

- **Aucun attribut `#[CompilerPass]`** — l'enregistrement est toujours programmatique dans
  `build()`.
- **`findTaggedServiceIds()` retourne id → tableau d'ensembles d'attributs de tag**, pas
  des instances et pas un locator.
- **Une `priority` plus élevée passe plus tôt** dans la collection résultante.
- **Les passes manipulent des `Definition`s à la compilation** — `Reference`, jamais `get()`.
- La phase par défaut est **`TYPE_BEFORE_OPTIMIZATION`**.

Si vous savez écrire ce pass de mémoire et expliquer chaque choix, le sujet est à vous.

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

- **Option A (la plus simple) — `tagged_iterator`.** Si vous voulez seulement
  *« injecter tous les services portant ce tag, triés par priorité »*, vous n'avez pas
  besoin de pass du tout. Donnez au registre un argument
  `#[AutowireIterator('app.handler')] iterable $handlers` (ou un
  `!tagged_iterator app.handler` en YAML). Les passes du core font la collecte et le tri.
  Voir [Tags](../dependency-injection/tags.md).
- **Option B (pass idiomatique) — `findAndSortTaggedServices()`.** Au lieu de trier à la
  main, ajoutez un `use` du trait
  `Symfony\Component\DependencyInjection\Compiler\PriorityTaggedServiceTrait` de Symfony et appelez
  `$this->findAndSortTaggedServices('app.handler', $container)` — il retourne des
  `Reference`s déjà triées par priorité décroissante. Bouclez dessus pour les passer à
  `addMethodCall('add', [$ref])`.
- **Option C (variante style examen) — registre à clés.** Lisez un attribut de tag
  personnalisé (par ex. `['key' => 'sms']`) dans `process()` et construisez une map à clés,
  ou exposez les handlers via un `ServiceLocator` avec `#[AutowireLocator('app.handler',
  defaultIndexMethod: 'getName')]` pour une recherche lazy par clé.

---

<small>Theory: [Compiler passes](../dependency-injection/compiler-passes.md) ·
[Tags](../dependency-injection/tags.md) · Labs: [all labs](index.md)</small>
