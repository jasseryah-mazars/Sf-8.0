# Lab: Custom Event + Prioritised Subscribers — Drive the EventDispatcher

!!! abstract "Practical Lab"
    **Objective:** dispatch a custom event through a real `EventDispatcher` and
    control *who reacts, in what order, and when to stop* using priorities and
    `stopPropagation()` ·
    **Difficulty:** Medium ·
    **Theory:** [Event Dispatcher & Kernel Events](../architecture/events.md) ·
    **Mode:** TDD

## Objective

After this lab you can:

- Model a domain fact as a custom `Event` subclass that carries data listeners can read and mutate.
- Register listeners at different **priorities** and predict their invocation order.
- Use `stopPropagation()` to short-circuit the remaining listeners deliberately.
- Wire a class-based **subscriber** through `getSubscribedEvents()` — including
  several handlers for the same event — and prove it end-to-end with a test.
- Translate a manually-wired listener into the `#[AsEventListener]` attribute form
  the framework wires for you.

## Prerequisites

- Chapters: [Event Dispatcher & Kernel Events](../architecture/events.md),
  [Request Handling](../architecture/request-handling.md).
- Assumed skills: PHPUnit basics, closures / first-class callables, `readonly`
  promoted properties.

## TD Instructions

You are building an *order placed* notification flow, decoupled via events. Do the
steps in order; write the **test before** each piece of production code.

1. Create the event `App\Event\OrderPlacedEvent` extending the **contracts** base
   `Event`. Promote the immutable payload (`orderId`, `totalCents`) as `readonly`,
   and add a small mutable `trace` accumulator so tests can observe listener order.
2. Write a first failing test: on a real `EventDispatcher`, register three closures
   for `OrderPlacedEvent::class` with priorities `-10`, `100`, `0`, dispatch, and
   assert the `trace` is ordered **high → mid → low**.
3. Write a second test proving that a high-priority listener calling
   `stopPropagation()` prevents a lower-priority listener from ever running, and
   that `isPropagationStopped()` is then `true`.
4. Implement `App\EventListener\AuditListener` as a plain class with an invokable /
   named method that tags the trace. Register it and confirm ordering.
5. Implement `App\EventSubscriber\NotificationSubscriber` (an
   `EventSubscriberInterface`) that subscribes **two** handlers to the same event at
   different priorities via `getSubscribedEvents()`. Write a test that
   `addSubscriber()`s it and asserts both handlers ran in priority order.
6. Add a unit assertion directly on `NotificationSubscriber::getSubscribedEvents()`
   (a static array) — no dispatcher needed — to lock the wiring contract.
7. **Level up:** rewrite `AuditListener` using `#[AsEventListener]` and note why no
   manual registration is needed inside a Symfony application.

!!! info "Constraints"
    Symfony 8 · PHP 8.4 · no libraries outside the certification scope · follow
    best practices (attributes, strict types, `readonly` where apt).

## Implementation Guide (partial)

High-level pointers only — reach for these, don't copy a full solution:

- **Base class:** extend `Symfony\Contracts\EventDispatcher\Event` — it provides
  `stopPropagation()` / `isPropagationStopped()`. Do **not** extend the deprecated
  `Symfony\Component\EventDispatcher\Event`.
- **Dispatcher:** `new EventDispatcher()` needs no container. Register with
  `addListener(string $eventName, callable $listener, int $priority = 0)` and
  `addSubscriber(EventSubscriberInterface $subscriber)`.
- **Event name:** dispatch with the object only — `dispatch($event)` (PSR-14) — and
  the class name (`OrderPlacedEvent::class`) is used as the event name. Register
  your listeners under that same string.
- **Observing order:** because `dispatch()` returns the *same* event object, let
  each listener append a tag to a public `trace` array on the event; assert the array.
- **Subscriber shape:** `getSubscribedEvents()` returns
  `[EventName => [['method', priority], ['method', priority]]]` to attach several
  handlers of one event.
- **Introspection helpers:** `getListeners($name)`, `getListenerPriority($name, $cb)`,
  and `hasListeners($name)` are useful in tests.

## TDD — write the test first

!!! note "Red → Green → Refactor"
    1. **Red:** write the failing test below; run it, watch it fail (the classes
       don't exist yet).
    2. **Green:** write the minimum code — the event, the listener, the subscriber.
    3. **Refactor:** extract the listener to `#[AsEventListener]`, tests still green.

**Behaviour (Given/When/Then):**

- **Given** a real `EventDispatcher` with listeners at priorities `100`, `0`, `-10`
  **When** an `OrderPlacedEvent` is dispatched **Then** they run high → mid → low.
- **Given** a high-priority listener that calls `stopPropagation()` **When** the
  event is dispatched **Then** lower-priority listeners never run.
- **Given** a `NotificationSubscriber` added via `addSubscriber()` **When** the
  event is dispatched **Then** both handlers declared in `getSubscribedEvents()` run
  in priority order.

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
        $dispatcher->addListener(OrderPlacedEvent::class, static fn (OrderPlacedEvent $e) => $e->tag('low'), -10);
        $dispatcher->addListener(OrderPlacedEvent::class, static fn (OrderPlacedEvent $e) => $e->tag('high'), 100);
        $dispatcher->addListener(OrderPlacedEvent::class, static fn (OrderPlacedEvent $e) => $e->tag('mid'), 0);

        $event = $dispatcher->dispatch(new OrderPlacedEvent('ORD-1', 4_999));

        // Higher priority runs first; equal priority would keep registration order.
        self::assertSame(['high', 'mid', 'low'], $event->trace);
    }

    public function testStopPropagationSkipsLowerPriorityListeners(): void
    {
        $dispatcher = new EventDispatcher();
        $dispatcher->addListener(OrderPlacedEvent::class, static function (OrderPlacedEvent $e): void {
            $e->tag('guard');
            $e->stopPropagation();
        }, 100);
        $dispatcher->addListener(OrderPlacedEvent::class, static fn (OrderPlacedEvent $e) => $e->tag('never'), 0);

        $event = $dispatcher->dispatch(new OrderPlacedEvent('ORD-2', 100));

        self::assertSame(['guard'], $event->trace);
        self::assertTrue($event->isPropagationStopped());
    }

    public function testPlainListenerObjectIsInvoked(): void
    {
        $dispatcher = new EventDispatcher();
        $dispatcher->addListener(OrderPlacedEvent::class, [new AuditListener(), 'onOrderPlaced'], 50);

        $event = $dispatcher->dispatch(new OrderPlacedEvent('ORD-3', 250));

        self::assertSame(['audit'], $event->trace);
    }

    public function testSubscriberIsWiredThroughGetSubscribedEvents(): void
    {
        $dispatcher = new EventDispatcher();
        $dispatcher->addSubscriber(new NotificationSubscriber());

        // Two handlers were declared for the same event name.
        self::assertCount(2, $dispatcher->getListeners(OrderPlacedEvent::class));

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
    Run it: `vendor/bin/phpunit tests/Event/OrderPlacedEventTest.php`. No container,
    no kernel — `new EventDispatcher()` is enough. Use closures for the priority
    tests and the real classes for the wiring tests. Remember `dispatch()` returns
    the **same** event instance, so read `->trace` off the return value.

## Validation Steps

- [ ] `vendor/bin/phpunit tests/Event/OrderPlacedEventTest.php` is green (5 tests).
- [ ] In a full app, `php bin/console debug:event-dispatcher "App\\Event\\OrderPlacedEvent"`
      lists the subscriber's two handlers with their priorities, sorted descending.
- [ ] Temporarily swap two priorities and watch a test go red — proof the ordering
      assertion is meaningful, not accidental.

## Review — Common Mistakes

- **Extending the wrong base `Event`.** Use
  `Symfony\Contracts\EventDispatcher\Event`, not the component's deprecated class.
  Wrong import → missing/duplicated `stopPropagation()` semantics.
- **Registering under a different name than dispatched.** With `dispatch($event)`
  the name defaults to `$event::class`; your `addListener()` / `getSubscribedEvents()`
  key must be that exact FQCN. Mismatch → listener silently never runs.
- **Expecting lower number = first.** Priority is sorted **descending**; `100` runs
  before `0` before `-10`. Default priority is `0`.
- **`getSubscribedEvents()` returning the map backwards.** It is
  `event name → handler(s)`, not `handler → event`.
- **Thinking `stopPropagation()` cancels the operation.** It only halts *this*
  event's remaining listeners; already-run listeners and the caller are unaffected.
- **Asserting order without observing it.** A `trace` array (or spies) is what turns
  "I think it's ordered" into a real assertion.

## Exam Connection

The certification probes exactly these traps: *higher priority runs first*, the
PSR-14 `dispatch(object $event, ?string $eventName = null)` argument order, the
static `getSubscribedEvents(): array` contract and its three value shapes
(`'method'`, `['method', prio]`, `[['method', prio], …]`), and the precise scope of
`stopPropagation()`. Building and testing the flow by hand — rather than only via
the framework's auto-wiring — is what makes these answers reflexive under time.

## Ideal Solution

??? success "Reference solution (compare only after you try)"
    The custom event — extend the **contracts** base class:

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

    A plain listener class (manual registration or auto-wired via the tag):

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

    The subscriber — two handlers for one event at different priorities:

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

    Level-up: the same listener with the attribute the framework wires for you
    (no `services.yaml` entry, no `addListener()` call needed in a Symfony app):

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventListener;

    use App\Event\OrderPlacedEvent;
    use Symfony\Component\EventDispatcher\Attribute\AsEventListener;

    #[AsEventListener(event: OrderPlacedEvent::class, method: 'onOrderPlaced', priority: 50)]
    final class AuditListener
    {
        public function onOrderPlaced(OrderPlacedEvent $event): void
        {
            $event->tag('audit');
        }
    }
    ```

    Dispatching it from a service (PSR-14 order — event object first):

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
            return $this->dispatcher->dispatch(new OrderPlacedEvent($orderId, $totalCents));
        }
    }
    ```

## Alternative Approaches (optional)

- **Option A (simple):** one `#[AsEventListener]` per method — zero config, ideal
  for a couple of unrelated reactions; the framework's `RegisterListenersPass` wires
  them at compile time.
- **Option B (subscriber):** `EventSubscriberInterface` when one class owns many
  handlers or you want the wiring visible in code and unit-testable in isolation
  (see `testGetSubscribedEventsContractShape`).
- **Option C (exam-style):** wire everything by hand with `addListener()` /
  `addSubscriber()` on a bare `EventDispatcher`, then use `getListenerPriority()`
  and `debug:event-dispatcher` to reason about ordering — exactly how questions
  frame it.

---

<small>Theory: [Event Dispatcher & Kernel Events](../architecture/events.md) · Labs: [all labs](index.md)</small>
