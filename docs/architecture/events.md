# Event Dispatcher & Kernel Events

!!! tip "In a nutshell"
    The EventDispatcher is how Symfony stays decoupled: code dispatches an event
    object and any number of listeners react. Highest-yield: **higher priority runs
    first**, `dispatch()` takes the **event object first** (PSR-14), and a subscriber
    declares its events in `getSubscribedEvents()`.

!!! example "Real-world analogy"
    The dispatcher is an **airport control tower**. When something happens it
    **broadcasts** to every listener tuned to that frequency — but not at random:
    higher-**priority** aircraft (listeners) are cleared first. Any listener can call
    `stopPropagation()` — like the tower closing the runway — and the ones still
    queued are grounded. The tower never flies the planes itself; it only
    coordinates who acts and in what order.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain how `EventDispatcher` stores, sorts and invokes listeners.
    - [ ] Choose between a **listener** and a **subscriber** and register both correctly.
    - [ ] Use priorities and `stopPropagation()` deliberately.
    - [ ] Recite the kernel-events catalogue and their event classes.

    **Syllabus:** `Symfony Architecture → Event Dispatcher` ·
    **Level:** Expert ·
    **Est. time:** 35 min ·
    **Prerequisites:** [Request Handling](request-handling.md)

---

## Theory

The **EventDispatcher** implements the *mediator* pattern: code dispatches a named
event object, and any number of decoupled **listeners** react. Symfony's whole
extensibility model — the kernel, security, forms, console — is built on it.

Two ways to attach behaviour:

- **Listener** — a callable registered against *one* event name.
- **Subscriber** — a class implementing `EventSubscriberInterface` that declares
  *all* the events it handles in one static method.

## Deep Dive — how it works internally

!!! question "Predict first"
    Three listeners are registered for `kernel.response` with priorities `10`, `0`
    and `-10`. In which order do they run, and what happens if the priority-`0` one
    calls `stopPropagation()`?

??? note "Reveal"
    High → low: `10`, then `0`, then `-10`. The check runs *before* each call, so
    the `0` listener still runs fully, but `stopPropagation()` means the `-10`
    listener is never invoked. Already-run listeners are not rewound.

### Classes & interfaces

| Role | FQCN |
|---|---|
| Dispatcher | `Symfony\Component\EventDispatcher\EventDispatcher` |
| Contract | `Symfony\Contracts\EventDispatcher\EventDispatcherInterface` (extends PSR-14) |
| Base event | `Symfony\Contracts\EventDispatcher\Event` |
| Subscriber | `Symfony\Component\EventDispatcher\EventSubscriberInterface` |
| Listener attribute | `Symfony\Component\EventDispatcher\Attribute\AsEventListener` |
| Kernel names | `Symfony\Component\HttpKernel\KernelEvents` |

`EventDispatcherInterface` extends the PSR-14 `Psr\EventDispatcher\EventDispatcherInterface`,
so `dispatch()` takes the **event object first**: `dispatch(object $event, ?string $eventName = null): object`.
When no name is given, the event's class name is used.

### How listeners are stored and sorted

Internally the dispatcher keeps `listeners[eventName][priority][] = callable` and a
parallel `sorted[eventName]` cache. On first dispatch for an event it sorts by
**priority descending** — *higher priority runs first*; equal priorities run in
registration order. The sorted list is memoised until a listener is added/removed.

```mermaid
flowchart LR
    A[dispatch event] --> B{sorted cache?}
    B -- no --> C[sort by priority desc]
    B -- yes --> D[iterate listeners]
    C --> D
    D --> E{propagation stopped?}
    E -- no --> D
    E -- yes --> F[return event]
```

### Stopping propagation

Any listener can call `$event->stopPropagation()`. Before invoking each listener
the dispatcher checks `$event->isPropagationStopped()` and stops the loop. The
event object itself carries this flag — it must extend the contracts `Event`.

```mermaid
sequenceDiagram
    participant Caller
    participant D as EventDispatcher
    participant A as Listener A (prio 10)
    participant B as Listener B (prio 0)
    participant C as Listener C (prio -10)
    Caller->>D: dispatch(event)
    D->>A: __invoke(event)
    A-->>D: returns (no stop)
    D->>B: __invoke(event)
    B-->>D: stopPropagation()
    Note over D: isPropagationStopped() → halt loop
    D--xC: never called
    D-->>Caller: same event object
```

Listeners run **high → low** priority; the check happens *before* each call, so
`B` still runs fully but `C` is skipped. The one already-invoked listeners are
never rewound — propagation only prevents the *remaining* listeners.

### Compile-time registration

You rarely call `addListener()` at runtime. The `RegisterListenersPass` compiler
pass scans services tagged `kernel.event_listener` / `kernel.event_subscriber`
(and `#[AsEventListener]` attributes) and wires them into the dispatcher **at
container compile time**. Listeners are instantiated **lazily** — the service is
only constructed when its event actually fires, which keeps boot cheap.

!!! note "Source reference"
    `Symfony\Component\EventDispatcher\EventDispatcher::dispatch()` and
    `RegisterListenersPass` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/EventDispatcher/EventDispatcher.php).

### The kernel-events catalogue

| Constant | Event class | Fired when |
|---|---|---|
| `REQUEST` | `RequestEvent` | Start of every request |
| `CONTROLLER` | `ControllerEvent` | Controller resolved |
| `CONTROLLER_ARGUMENTS` | `ControllerArgumentsEvent` | Arguments resolved |
| `VIEW` | `ViewEvent` | Controller returned a non-Response |
| `RESPONSE` | `ResponseEvent` | Before returning the response |
| `FINISH_REQUEST` | `FinishRequestEvent` | End of each (sub)request |
| `EXCEPTION` | `ExceptionEvent` | An exception escaped |
| `TERMINATE` | `TerminateEvent` | After the response is sent |

See [Request Handling](request-handling.md) for their execution order.

### Null behavior

`dispatch(object $event, ?string $eventName = null): object` **always returns the
same event object** — even when *no* listener is registered and even when every
listener left it untouched. Passing `null` for (or omitting) `$eventName` is the
normal case: the dispatcher falls back to the event's class name. Listeners
themselves return `void`; the only way a result reaches the caller is by *mutating*
the event, so you read it off the returned object
(`$response = $dispatcher->dispatch($event)`). If a listener never calls a setter —
`setResponse()` on a kernel event, say — the event simply comes back unchanged: no
error, no `null` return. The common bug is expecting `dispatch()` to hand back a
listener's return value; it never does — it returns the event you passed in.

!!! note "Null in real life"
    An event with no listeners is a **tower radio call that nobody answers**: the
    message still goes out and comes back to you unchanged — silence is not an error.

!!! info "Expert note"
    Listeners are registered **lazily**: `RegisterListenersPass` stores the service
    *id*, not an instance, so the listener object is only constructed the first time
    its event actually fires. That is why an expensive constructor on a rarely-fired
    listener costs nothing on the hot path — and why you must never do real work in a
    subscriber's `getSubscribedEvents()` (it is called at container **compile time**).

??? example "Debugging story"
    **Symptom:** a security-header listener silently stopped adding headers after a
    refactor. **Diagnosis:** a new higher-priority `kernel.response` listener called
    `stopPropagation()` unconditionally, so lower-priority listeners never ran.
    `php bin/console debug:event-dispatcher kernel.response` revealed the real
    ordering and the offending high-priority entry. **Fix:** drop the blanket
    `stopPropagation()` (it only made sense on `kernel.request`) and set explicit
    priorities. **Avoid:** call `stopPropagation()` only on events you truly own.

??? abstract "Source-code tour"
    - `Symfony\Component\EventDispatcher\EventDispatcher::dispatch()` fetches the
      sorted listener list and invokes each until propagation stops.
    - `EventDispatcher::sortListeners()` orders `listeners[eventName][priority]`
      descending and memoises the result into `sorted[eventName]`.
    - `Symfony\Contracts\EventDispatcher\Event::stopPropagation()` /
      `isPropagationStopped()` carry the halt flag checked before each call.
    - `Symfony\Component\EventDispatcher\DependencyInjection\RegisterListenersPass`
      wires tagged services and `#[AsEventListener]` attributes at compile time.
    - `Symfony\Component\EventDispatcher\EventSubscriberInterface::getSubscribedEvents()`
      is read by the same pass to register a subscriber's handlers.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventListener;

    use Symfony\Component\EventDispatcher\Attribute\AsEventListener;
    use Symfony\Component\HttpKernel\Event\RequestEvent;
    use Symfony\Component\HttpKernel\KernelEvents;

    // Method-level attribute: no interface, no manual tagging.
    final class LocaleListener
    {
        #[AsEventListener(event: KernelEvents::REQUEST, priority: 15)]
        public function onRequest(RequestEvent $event): void
        {
            $event->getRequest()->setLocale('en');
        }
    }
    ```

=== "Subscriber"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\EventSubscriber;

    use Symfony\Component\EventDispatcher\EventSubscriberInterface;
    use Symfony\Component\HttpKernel\Event\ResponseEvent;
    use Symfony\Component\HttpKernel\KernelEvents;

    final class ResponseSubscriber implements EventSubscriberInterface
    {
        public static function getSubscribedEvents(): array
        {
            return [
                // event => [method, priority]
                KernelEvents::RESPONSE => ['onResponse', -10],
            ];
        }

        public function onResponse(ResponseEvent $event): void
        {
            $event->getResponse()->headers->set('X-App', '1');
        }
    }
    ```

=== "Console"

    ```console
    $ php bin/console debug:event-dispatcher kernel.response
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Use `#[AsEventListener]` for one-off listeners | Manual `addListener()` in app code |
| Use a subscriber when one class handles many events | Splitting related handlers across files |
| Set explicit priorities when order matters | Relying on registration order |
| `stopPropagation()` only when you truly own the event | Silently stopping others' listeners |

## When (not) to use it / alternatives

Use events for **cross-cutting, decoupled** reactions where you don't control (or
don't want to couple to) the caller. When you *do* control both sides and need a
return value, a direct service call or the **Messenger** component (for async) is
clearer than an event.

!!! danger "Certification traps"
    - **Higher priority = earlier.** Default priority is `0`.
    - `dispatch()` is PSR-14: **event object first**, name optional.
    - A subscriber's array value can be a string method, `[method, priority]`, or a
      list of `[method, priority]` pairs for multiple handlers of the same event.
    - Listeners are **lazy** — the service isn't built until its event fires.

!!! warning "Common mistakes"
    - Implementing `EventSubscriberInterface` but forgetting `getSubscribedEvents()`
      returns event **names → handlers** (not the reverse).
    - Expecting `stopPropagation()` to cancel the request — it only stops *this*
      event's remaining listeners.

## Exercises

1. **(Advanced)** Convert a two-event subscriber into two `#[AsEventListener]`
   methods and confirm identical behaviour with `debug:event-dispatcher`.
2. **(Expert)** Given three `kernel.response` listeners with priorities `10`, `0`,
   `-10`, state the invocation order.

??? success "Solutions"

    **1.** Move each handler onto a public method annotated with
    `#[AsEventListener(event: ..., priority: ...)]` and delete the interface. The
    `RegisterListenersPass` wires attribute-based listeners identically.

    **2.** `10` → `0` → `-10` (descending priority).

## Certification questions

??? question "Q1. What does a higher listener priority mean?"
    - [x] A. It runs earlier ✅
    - [ ] B. It runs later
    - [ ] C. It cannot be stopped

    **Why:** Listeners are sorted by priority **descending**. **Ref:**
    [EventDispatcher](https://symfony.com/doc/current/components/event_dispatcher.html#connecting-listeners).

??? question "Q2. What is the signature of `dispatch()` in Symfony 8?"
    - [x] A. `dispatch(object $event, ?string $eventName = null)` ✅
    - [ ] B. `dispatch(string $eventName, Event $event)`
    - [ ] C. `dispatch(Event $event, string $eventName)` (name required)

    **Why:** Symfony follows PSR-14: event object first, name optional. **Ref:**
    [Generic events](https://symfony.com/doc/current/components/event_dispatcher.html).

??? question "Q3. Which method must a subscriber implement?"
    - [x] A. `public static function getSubscribedEvents(): array` ✅
    - [ ] B. `public function subscribe(): array`
    - [ ] C. `#[AsEventSubscriber]`

    **Why:** `EventSubscriberInterface` defines the static method. **Ref:**
    [Event subscribers](https://symfony.com/doc/current/event_dispatcher.html#creating-an-event-subscriber).

## Key takeaways

- Dispatcher sorts by priority (desc), memoises, and invokes lazily-built listeners.
- Listener = one event; subscriber = many events in `getSubscribedEvents()`.
- `dispatch(object, ?name)` — PSR-14 order.
- `stopPropagation()` halts only the current event's remaining listeners.

## Last-minute revision

!!! tip "Cheat sheet"
    - Register: `#[AsEventListener]`, tag `kernel.event_listener`, or subscriber.
    - `getSubscribedEvents(): array` → `[EventName => 'method' | ['method', prio] | [['m',prio],…]]`.
    - Default priority `0`; higher first.
    - Compiled by `RegisterListenersPass`.

## Connections

- **Depends on:** [Dependency Injection](../dependency-injection/index.md) — listeners and subscribers are compiled into the dispatcher by `RegisterListenersPass`.
- **Reused in:** [Request Handling](request-handling.md) — the kernel lifecycle is dispatched through this component; [Exception Handling](exception-handling.md) hooks `kernel.exception`.
- **Confused with:** [Interoperability & PSRs](psr.md) — Symfony's dispatcher *implements* PSR-14 but adds priorities and `stopPropagation()` on top.

## Official References
- [Official docs — EventDispatcher](https://symfony.com/doc/current/components/event_dispatcher.html)
- [Official docs — Events reference](https://symfony.com/doc/current/reference/events.html)
- [Symfony source — EventDispatcher](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/EventDispatcher/EventDispatcher.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony architecture" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/current/components/event_dispatcher.html#connecting-listeners) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** the dispatcher decouples callers from reactions (the mediator pattern)
- [ ] implement both a `#[AsEventListener]` and an `EventSubscriberInterface`
- [ ] debug a listener that never runs because of priority or `stopPropagation()`
- [ ] spot that `dispatch()` returns the **event object**, not a listener's value
- [ ] explain how listeners are stored, sorted by priority and invoked lazily

---

<small>Related: [Request Handling](request-handling.md) · [Exception Handling](exception-handling.md) · [Components](components.md)</small>
