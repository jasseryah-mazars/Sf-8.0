# Service Locators

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain what a `ServiceLocator` is and how it differs from injecting all
          services.
    - [ ] Build one with `#[AutowireLocator]`.
    - [ ] Implement a service subscriber with `ServiceSubscriberInterface` /
          `#[SubscribedService]`.

    **Syllabus:** `Dependency Injection → Service Locators` ·
    **Level:** Expert ·
    **Est. time:** 35 min ·
    **Prerequisites:** [Tags](tags.md)

---

## Theory

A **service locator** is a small, container-like object holding a *fixed, declared*
set of services that it instantiates **lazily** on `get()`. It is the sanctioned
answer to "I might need one of several services, but not all, and not eagerly."
Unlike injecting the whole container (an anti-pattern), a locator exposes only an
explicit whitelist — dependencies stay honest and analysable.

## Deep Dive — how it works internally

### `ServiceLocator`

`Symfony\Component\DependencyInjection\ServiceLocator` implements PSR-11
`Psr\Container\ContainerInterface`. Its `get($id)` builds the service on first
access and caches it; `has($id)` checks membership. Because the set is declared at
compile time, the container knows exactly which services the locator can reach —
they are *not* removed as "unused", and each is created only if actually requested.

### Locator vs injecting everything

Injecting all candidate services eagerly instantiates them, even the ones you never
use in a given request. A locator defers construction until `get()`. This matters
when candidates are heavy (DB clients, HTTP clients) and only one is chosen per
request — e.g. a payment gateway selected by name.

```mermaid
flowchart LR
    C["Consumer"] --> L["ServiceLocator (PSR-11)"]
    L -->|"get('stripe')"| S1["Stripe (built now)"]
    L -.->|not requested| S2["PayPal (never built)"]
```

### Service subscribers

A **service subscriber** declares the services it *may* need via
`Symfony\Contracts\Service\ServiceSubscriberInterface::getSubscribedServices()`,
and the container injects a locator into a `$container` property (via
`ServiceSubscriberTrait` or a constructor arg). In Symfony 8 you annotate methods
with `#[SubscribedService]` and use the trait — the return type of the method is
the service type. This is how the base `AbstractController` gets `twig`, `router`,
etc. lazily.

### `#[AutowireLocator]`

The modern shortcut: `#[AutowireLocator([...])]` on a constructor parameter builds a
locator from a list of service ids/classes or from a **tag** (see [Tags](tags.md)),
optionally keyed by an index. No interface to implement.

!!! note "Source reference"
    `Symfony\Component\DependencyInjection\ServiceLocator` &
    `Symfony\Contracts\Service\ServiceSubscriberInterface` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/ServiceLocator.php).

## Configuration & code

=== "AutowireLocator"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Payment;

    use Psr\Container\ContainerInterface;
    use Symfony\Component\DependencyInjection\Attribute\AutowireLocator;

    final class PaymentProcessor
    {
        public function __construct(
            #[AutowireLocator([
                'stripe' => StripeGateway::class,
                'paypal' => PayPalGateway::class,
            ])]
            private readonly ContainerInterface $gateways,
        ) {}

        public function charge(string $name, int $amount): void
        {
            // Only the chosen gateway is instantiated.
            $this->gateways->get($name)->charge($amount);
        }
    }
    ```

=== "Service subscriber"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Payment;

    use Psr\Log\LoggerInterface;
    use Symfony\Contracts\Service\Attribute\SubscribedService;
    use Symfony\Contracts\Service\ServiceSubscriberInterface;
    use Symfony\Contracts\Service\ServiceMethodsSubscriberTrait;

    final class Reporter implements ServiceSubscriberInterface
    {
        use ServiceMethodsSubscriberTrait;

        #[SubscribedService]
        private function logger(): LoggerInterface
        {
            return $this->container->get(__FUNCTION__);
        }

        public function report(): void
        {
            $this->logger()->info('Report generated'); // lazily fetched
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/services.yaml
    services:
        App\Payment\PaymentProcessor:
            arguments:
                $gateways: !service_locator
                    stripe: '@App\Payment\StripeGateway'
                    paypal: '@App\Payment\PayPalGateway'
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Locator for pick-one-of-many | Injecting the whole container |
| Declare an explicit id list/tag | Hidden, undeclared dependencies |
| Use for heavy, rarely-used deps | Locator when you always use all |
| `#[AutowireLocator]` for brevity | Boilerplate subscriber when not needed |

## When (not) to use it / alternatives

Use a locator when only *one* of several services is needed per call and building
all would be wasteful, or to break a construction-time dependency cycle. If you
always iterate every service, inject a [`tagged_iterator`](tags.md). If you need
exactly one dependency, inject it directly — a locator adds needless indirection.

!!! danger "Certification traps"
    - A locator is **lazy**: services are built on `get()`, not up front.
    - It implements **PSR-11** (`Psr\Container\ContainerInterface`), not the
      Symfony container interface.
    - Its service set is **fixed at compile time** — you cannot fetch an id not in
      the list (throws not-found).
    - `getSubscribedServices()` declares *what may be needed*; the locator is
      injected, not the whole container.

!!! warning "Common mistakes"
    - Injecting `Symfony\..\ContainerInterface` to grab arbitrary services (the
      service-locator anti-pattern).
    - Expecting a locator to expose services you never declared.
    - Using a locator where a single constructor injection would do.

## Exercises

1. **(Expert)** Wire a `PaymentProcessor` that can build either a Stripe or PayPal
   gateway on demand, instantiating only the chosen one.
2. **(Expert)** Convert a class that eagerly injects `LoggerInterface` and `Twig`
   but rarely uses Twig into a service subscriber.

??? success "Solutions"

    **1.** Use `#[AutowireLocator(['stripe' => StripeGateway::class, 'paypal' =>
    PayPalGateway::class])] ContainerInterface $gateways`, then
    `$this->gateways->get($name)->charge(...)`. Only the requested gateway is built.

    **2.** Implement `ServiceSubscriberInterface` with
    `ServiceMethodsSubscriberTrait`, add `#[SubscribedService]` methods returning
    `LoggerInterface` and `Environment`, and fetch via `$this->container->get(...)`
    only when needed — Twig is never built unless used.

## Certification questions

??? question "Q1. How is a `ServiceLocator` different from injecting the container?"
    - [x] A. It exposes only a declared, whitelisted set of services ✅
    - [ ] B. It is eager, the container is lazy
    - [ ] C. It cannot instantiate services
    - [ ] D. There is no difference

    **Why:** A locator's set is explicit and analysable; injecting the whole
    container hides dependencies. **Ref:** [Service subscribers & locators](https://symfony.com/doc/current/service_container/service_subscribers_locators.html).

??? question "Q2. When are locator services instantiated?"
    - [ ] A. All at construction
    - [x] B. Lazily, on `get()` ✅
    - [ ] C. At compile time
    - [ ] D. On kernel boot

    **Why:** A locator defers construction until a service is actually requested.
    **Ref:** [Service locators](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators).

??? question "Q3. What does `getSubscribedServices()` return?"
    - [x] A. A map/list of services the subscriber may lazily use ✅
    - [ ] B. Instantiated services
    - [ ] C. Compiler passes
    - [ ] D. The whole container

    **Why:** It declares the whitelist; the container injects a matching locator.
    **Ref:** [Service subscribers](https://symfony.com/doc/current/service_container/service_subscribers_locators.html).

??? question "Q4. `ServiceLocator` implements which interface?"
    - [x] A. `Psr\Container\ContainerInterface` (PSR-11) ✅
    - [ ] B. `Symfony\...\ContainerInterface`
    - [ ] C. `IteratorAggregate` only
    - [ ] D. `CompilerPassInterface`

    **Why:** It is a PSR-11 container exposing `get()`/`has()`.
    **Ref:** [Service locators](https://symfony.com/doc/current/service_container/service_subscribers_locators.html#service-locators).

## Key takeaways

- A locator lazily builds a fixed, declared set of services (PSR-11).
- Prefer it over injecting the whole container.
- `#[AutowireLocator]` is the quick way; subscribers declare via
  `getSubscribedServices()` / `#[SubscribedService]`.
- Use for pick-one-of-many or heavy, rarely-used deps.

## Last-minute revision

!!! tip "Cheat sheet"
    - `#[AutowireLocator([...])]` → PSR-11 `ContainerInterface`.
    - `!service_locator` in YAML.
    - Subscriber: `ServiceSubscriberInterface` + `ServiceMethodsSubscriberTrait` +
      `#[SubscribedService]`.
    - Lazy, whitelisted, not the whole container.

## Official References
- [Official Symfony docs — Service Subscribers & Locators](https://symfony.com/doc/current/service_container/service_subscribers_locators.html)
- [Symfony source — ServiceLocator](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/DependencyInjection/ServiceLocator.php)

---

<small>Related: [Tags](tags.md) · [Autowiring](autowiring.md) ·
[The Service Container](container.md)</small>
