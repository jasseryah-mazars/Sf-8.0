---
tags:
  - Labs
  - Architecture
---

# Lab: Custom Event + Prioritised Subscribers — Drive the EventDispatcher

!!! abstract "Practical Lab"
    **Objective:** dispatcher un event personnalisé à travers un vrai `EventDispatcher` et
    contrôler *qui réagit, dans quel ordre, et quand s'arrêter* à l'aide des priorités et de
    `stopPropagation()` ·
    **Difficulty:** Moyen ·
    **Theory:** [Event Dispatcher & Kernel Events](../architecture/events.md) ·
    **Mode:** TDD

## 🧠 Pour les nuls

**C'est quoi ce lab ?** Créer ton propre événement personnalisé et plusieurs écouteurs qui réagissent dans un ordre précis — pour comprendre comment le mécanisme d'événements de Symfony fonctionne de l'intérieur.

**Pourquoi ça existe ?** Comprendre la théorie des priorités et de `stopPropagation()` reste abstrait tant qu'on ne l'a pas vu s'exécuter réellement, avec plusieurs listeners qui se disputent l'ordre de passage.

**🏠 Analogie de la vraie vie :** Une alarme incendie que plusieurs personnes entendent en même temps, mais où celles avec le badge "responsable sécurité" (priorité plus haute) agissent en premier — et l'une d'elles peut décider d'arrêter l'alarme avant que les autres n'interviennent.

**Symfony dans la vraie vie :** `#[AsEventListener(priority: 100)]` s'exécute avant `#[AsEventListener(priority: 10)]` sur le même événement — exactement ce que ce lab te fait vérifier toi-même.

**⚠️ Erreur fréquente :** supposer que tous les listeners s'exécutent toujours, même après un `stopPropagation()` — un listener qui l'appelle empêche définitivement tous les listeners restants de s'exécuter.

**🧠 Comment le mémoriser :** "Priorité plus haute = passe en premier — et `stopPropagation()` ferme la porte aux suivants."


## Objective

À l'issue de ce lab, vous saurez :

- Modéliser un fait métier sous la forme d'une sous-classe d'`Event` personnalisée qui transporte des données que les listeners peuvent lire et modifier.
- Enregistrer des listeners à différentes **priorités** et prédire leur ordre d'invocation.
- Utiliser `stopPropagation()` pour court-circuiter délibérément les listeners restants.
- Câbler un **subscriber** sous forme de classe via `getSubscribedEvents()` — y compris
  plusieurs handlers pour le même event — et le prouver de bout en bout avec un test.
- Convertir un listener câblé à la main vers la forme à attribut `#[AsEventListener]`
  que le framework câble pour vous.

## Prerequisites

- Chapitres : [Event Dispatcher & Kernel Events](../architecture/events.md),
  [Request Handling](../architecture/request-handling.md).
- Compétences supposées acquises : bases de PHPUnit, closures / first-class callables,
  propriétés promues `readonly`.

## TD Instructions

Vous construisez un flux de notification *order placed* (commande passée), découplé via
des events. Suivez les étapes dans l'ordre ; écrivez le **test avant** chaque morceau de
code de production.

1. Créez l'event `App\Event\OrderPlacedEvent` étendant la classe de base des **contracts**
   `Event`. Promouvez la charge utile immuable (`orderId`, `totalCents`) en `readonly`,
   et ajoutez un petit accumulateur mutable `trace` afin que les tests puissent observer
   l'ordre des listeners.
2. Écrivez un premier test qui échoue : sur un vrai `EventDispatcher`, enregistrez trois closures
   pour `OrderPlacedEvent::class` avec les priorités `-10`, `100`, `0`, dispatchez, et
   vérifiez que la `trace` est ordonnée **high → mid → low**.
3. Écrivez un second test prouvant qu'un listener de haute priorité appelant
   `stopPropagation()` empêche un listener de priorité inférieure de s'exécuter, et
   qu'`isPropagationStopped()` vaut alors `true`.
4. Implémentez `App\EventListener\AuditListener` comme une classe simple avec une méthode
   invokable / nommée qui marque la trace. Enregistrez-la et confirmez l'ordre.
5. Implémentez `App\EventSubscriber\NotificationSubscriber` (un
   `EventSubscriberInterface`) qui abonne **deux** handlers au même event à
   des priorités différentes via `getSubscribedEvents()`. Écrivez un test qui
   l'ajoute avec `addSubscriber()` et vérifie que les deux handlers se sont exécutés dans
   l'ordre des priorités.
6. Ajoutez une assertion unitaire directement sur `NotificationSubscriber::getSubscribedEvents()`
   (un tableau statique) — aucun dispatcher nécessaire — pour verrouiller le contrat de câblage.
7. **Pour aller plus loin :** réécrivez `AuditListener` avec `#[AsEventListener]` et notez
   pourquoi aucun enregistrement manuel n'est nécessaire dans une application Symfony.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · aucune bibliothèque hors du périmètre de la certification · suivez
    les bonnes pratiques (attributs, strict types, `readonly` là où c'est pertinent).

## Implementation Guide (partial)

Uniquement des repères de haut niveau — appuyez-vous dessus, ne copiez pas une solution complète :

- **Classe de base :** étendez `Symfony\Contracts\EventDispatcher\Event` — elle fournit
  `stopPropagation()` / `isPropagationStopped()`. N'étendez **pas** la classe dépréciée
  `Symfony\Component\EventDispatcher\Event`.
- **Dispatcher :** `new EventDispatcher()` ne nécessite aucun container. Enregistrez avec
  `addListener(string $eventName, callable $listener, int $priority = 0)` et
  `addSubscriber(EventSubscriberInterface $subscriber)`.
- **Nom de l'event :** dispatchez avec l'objet seul — `dispatch($event)` (PSR-14) — et
  le nom de classe (`OrderPlacedEvent::class`) sert de nom d'event. Enregistrez
  vos listeners sous cette même chaîne.
- **Observer l'ordre :** comme `dispatch()` retourne le *même* objet event, faites
  ajouter à chaque listener un marqueur dans un tableau public `trace` sur l'event ; vérifiez le tableau.
- **Forme du subscriber :** `getSubscribedEvents()` retourne
  `[EventName => [['method', priority], ['method', priority]]]` pour attacher plusieurs
  handlers à un même event.
- **Aides d'introspection :** `getListeners($name)`, `getListenerPriority($name, $cb)`
  et `hasListeners($name)` sont utiles dans les tests.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red :** écrivez le test ci-dessous ; lancez-le, regardez-le échouer (les classes
       n'existent pas encore).
    2. **Green :** écrivez le minimum de code — l'event, le listener, le subscriber.
    3. **Refactor :** extrayez le listener vers `#[AsEventListener]`, les tests restent verts.

**Comportement (Given/When/Then) :**

- **Given** un vrai `EventDispatcher` avec des listeners aux priorités `100`, `0`, `-10`
  **When** un `OrderPlacedEvent` est dispatché **Then** ils s'exécutent high → mid → low.
- **Given** un listener de haute priorité qui appelle `stopPropagation()` **When**
  l'event est dispatché **Then** les listeners de priorité inférieure ne s'exécutent jamais.
- **Given** un `NotificationSubscriber` ajouté via `addSubscriber()` **When** l'event
  est dispatché **Then** les deux handlers déclarés dans `getSubscribedEvents()` s'exécutent
  dans l'ordre des priorités.

```php
<?php
declare(strict_types=1);

namespace App\Tests\Event;

use App\Event\OrderPlacedEvent;
use App\EventListener\AuditListener;
use App\EventSubscriber\NotificationSubscriber;
use PHPUnit\Framework\TestCase;
use Symfony\Component\EventDispatcher\EventDispatcher;

final class OrderPlacedEventTest extends TestCase
{
    public function testListenersRunInPriorityOrderDescending(): void
    {
        $dispatcher = new EventDispatcher();
        $dispatcher->addListener(
            OrderPlacedEvent::class,
            static fn (OrderPlacedEvent $e) => $e->tag('low'),
            -10,
        );
        $dispatcher->addListener(
            OrderPlacedEvent::class,
            static fn (OrderPlacedEvent $e) => $e->tag('high'),
            100,
        );
        $dispatcher->addListener(
            OrderPlacedEvent::class,
            static fn (OrderPlacedEvent $e) => $e->tag('mid'),
            0,
        );

        $event = $dispatcher->dispatch(new OrderPlacedEvent('ORD-1', 4_999));

        // Higher priority runs first; equal priority would keep
        // registration order.
        self::assertSame(['high', 'mid', 'low'], $event->trace);
    }

    public function testStopPropagationSkipsLowerPriorityListeners(): void
    {
        $dispatcher = new EventDispatcher();
        $dispatcher->addListener(
            OrderPlacedEvent::class,
            static function (OrderPlacedEvent $e): void {
                $e->tag('guard');
                $e->stopPropagation();
            },
            100,
        );
        $dispatcher->addListener(
            OrderPlacedEvent::class,
            static fn (OrderPlacedEvent $e) => $e->tag('never'),
            0,
        );

        $event = $dispatcher->dispatch(new OrderPlacedEvent('ORD-2', 100));

        self::assertSame(['guard'], $event->trace);
        self::assertTrue($event->isPropagationStopped());
    }

    public function testPlainListenerObjectIsInvoked(): void
    {
        $dispatcher = new EventDispatcher();
        $dispatcher->addListener(
            OrderPlacedEvent::class,
            [new AuditListener(), 'onOrderPlaced'],
            50,
        );

        $event = $dispatcher->dispatch(new OrderPlacedEvent('ORD-3', 250));

        self::assertSame(['audit'], $event->trace);
    }

    public function testSubscriberIsWiredThroughGetSubscribedEvents(): void
    {
        $dispatcher = new EventDispatcher();
        $dispatcher->addSubscriber(new NotificationSubscriber());

        // Two handlers were declared for the same event name.
        self::assertCount(
            2,
            $dispatcher->getListeners(OrderPlacedEvent::class),
        );

        $event = $dispatcher->dispatch(new OrderPlacedEvent('ORD-4', 999));

        self::assertSame(['notify.early', 'notify.late'], $event->trace);
    }

    public function testGetSubscribedEventsContractShape(): void
    {
        // Pure unit check — no dispatcher needed to lock the wiring contract.
        $map = NotificationSubscriber::getSubscribedEvents();

        self::assertArrayHasKey(OrderPlacedEvent::class, $map);
        self::assertSame(
            [['onOrderPlacedEarly', 200], ['onOrderPlacedLate', -100]],
            $map[OrderPlacedEvent::class],
        );
    }
}
```

!!! tip "Setup hints"
    Lancez-le : `vendor/bin/phpunit tests/Event/OrderPlacedEventTest.php`. Pas de container,
    pas de kernel — `new EventDispatcher()` suffit. Utilisez des closures pour les tests
    de priorité et les vraies classes pour les tests de câblage. Souvenez-vous que `dispatch()`
    retourne la **même** instance d'event : lisez donc `->trace` sur la valeur de retour.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/Event/OrderPlacedEventTest.php` est vert (5 tests).
- [ ] Dans une application complète, `php bin/console debug:event-dispatcher "App\\Event\\OrderPlacedEvent"`
      liste les deux handlers du subscriber avec leurs priorités, triés par ordre décroissant.
- [ ] Échangez temporairement deux priorités et regardez un test passer au rouge — la preuve
      que l'assertion sur l'ordre est significative, et non accidentelle.

## Review — Common Mistakes

- **Étendre la mauvaise classe de base `Event`.** Utilisez
  `Symfony\Contracts\EventDispatcher\Event`, pas la classe dépréciée du composant.
  Un mauvais import → une sémantique de `stopPropagation()` manquante/dupliquée.
- **Enregistrer sous un nom différent de celui dispatché.** Avec `dispatch($event)`,
  le nom vaut par défaut `$event::class` ; la clé de votre `addListener()` / `getSubscribedEvents()`
  doit être exactement ce FQCN. Un décalage → le listener ne s'exécute jamais, silencieusement.
- **S'attendre à ce que le plus petit nombre passe en premier.** La priorité est triée par ordre
  **décroissant** ; `100` s'exécute avant `0`, avant `-10`. La priorité par défaut est `0`.
- **Un `getSubscribedEvents()` retournant la map à l'envers.** C'est
  `nom d'event → handler(s)`, et non `handler → event`.
- **Croire que `stopPropagation()` annule l'opération.** Il n'arrête que les listeners
  restants de *cet* event ; les listeners déjà exécutés et l'appelant ne sont pas affectés.
- **Affirmer un ordre sans l'observer.** Un tableau `trace` (ou des spies) est ce qui transforme
  « je pense que c'est ordonné » en une véritable assertion.

## Exam Connection

La certification sonde exactement ces pièges : *la priorité la plus haute s'exécute en premier*,
l'ordre des arguments PSR-14 `dispatch(object $event, ?string $eventName = null)`, le
contrat statique `getSubscribedEvents(): array` et ses trois formes de valeurs
(`'method'`, `['method', prio]`, `[['method', prio], …]`), et la portée précise de
`stopPropagation()`. Construire et tester le flux à la main — plutôt que via le seul
câblage automatique du framework — est ce qui rend ces réponses réflexes sous la pression du temps.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    L'event personnalisé — étendez la classe de base des **contracts** :

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Event;

    use Symfony\Contracts\EventDispatcher\Event;

    /**
     * Dispatched once an order is successfully placed.
     * Immutable payload + a mutable trace so listeners' order is observable.
     */
    final class OrderPlacedEvent extends Event
    {
        /** @var list<string> */
        public array $trace = [];

        public function __construct(
            public readonly string $orderId,
            public readonly int $totalCents,
        ) {
        }

        public function tag(string $name): void
        {
            $this->trace[] = $name;
        }
    }
    ```

    Une classe listener simple (enregistrement manuel ou câblage automatique via le tag) :

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventListener;

    use App\Event\OrderPlacedEvent;

    final class AuditListener
    {
        public function onOrderPlaced(OrderPlacedEvent $event): void
        {
            $event->tag('audit');
        }
    }
    ```

    Le subscriber — deux handlers pour un même event à des priorités différentes :

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventSubscriber;

    use App\Event\OrderPlacedEvent;
    use Symfony\Component\EventDispatcher\EventSubscriberInterface;

    final class NotificationSubscriber implements EventSubscriberInterface
    {
        /**
         * event name => list of [method, priority] pairs.
         */
        public static function getSubscribedEvents(): array
        {
            return [
                OrderPlacedEvent::class => [
                    ['onOrderPlacedEarly', 200],
                    ['onOrderPlacedLate', -100],
                ],
            ];
        }

        public function onOrderPlacedEarly(OrderPlacedEvent $event): void
        {
            $event->tag('notify.early');
        }

        public function onOrderPlacedLate(OrderPlacedEvent $event): void
        {
            $event->tag('notify.late');
        }
    }
    ```

    Pour aller plus loin : le même listener avec l'attribut que le framework câble pour vous
    (aucune entrée dans `services.yaml`, aucun appel à `addListener()` nécessaire dans une application Symfony) :

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventListener;

    use App\Event\OrderPlacedEvent;
    use Symfony\Component\EventDispatcher\Attribute\AsEventListener;

    // The attribute wires the listener at compile time (no YAML).
    #[AsEventListener(
        event: OrderPlacedEvent::class,
        method: 'onOrderPlaced',
        priority: 50,
    )]
    final class AuditListener
    {
        public function onOrderPlaced(OrderPlacedEvent $event): void
        {
            $event->tag('audit');
        }
    }
    ```

    Le dispatch depuis un service (ordre PSR-14 — l'objet event en premier) :

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Service;

    use App\Event\OrderPlacedEvent;
    use Psr\EventDispatcher\EventDispatcherInterface;

    final readonly class OrderPlacer
    {
        public function __construct(private EventDispatcherInterface $dispatcher)
        {
        }

        public function place(string $orderId, int $totalCents): OrderPlacedEvent
        {
            // ... persist the order ...
            // dispatch() returns the same event instance (PSR-14).
            return $this->dispatcher->dispatch(
                new OrderPlacedEvent($orderId, $totalCents),
            );
        }
    }
    ```

## Alternative Approaches (optional)

- **Option A (simple) :** un `#[AsEventListener]` par méthode — zéro configuration, idéal
  pour quelques réactions sans lien entre elles ; le `RegisterListenersPass` du framework les
  câble à la compilation.
- **Option B (subscriber) :** `EventSubscriberInterface` quand une classe possède plusieurs
  handlers ou que vous voulez un câblage visible dans le code et testable unitairement en isolation
  (voir `testGetSubscribedEventsContractShape`).
- **Option C (façon examen) :** câblez tout à la main avec `addListener()` /
  `addSubscriber()` sur un `EventDispatcher` nu, puis utilisez `getListenerPriority()`
  et `debug:event-dispatcher` pour raisonner sur l'ordre — exactement la façon dont les
  questions sont formulées.

---

<small>Theory: [Event Dispatcher & Kernel Events](../architecture/events.md) · Labs: [all labs](index.md)</small>
