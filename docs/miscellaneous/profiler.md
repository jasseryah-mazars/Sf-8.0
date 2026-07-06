# Web Profiler & Data Collectors

!!! tip "In a nutshell"
    The profiler stores one profile per request (timing, queries, logs) fed by
    data collectors and shows the debug toolbar. Exam gold: collection happens
    on `kernel.response` (late collectors at terminate), `$this->data` must be
    serializable, and it is a dev-only tool disabled in prod.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Explain the profiler/toolbar architecture and when data is collected.
    - [ ] Build a custom `DataCollectorInterface` + template panel.
    - [ ] Disable the profiler in prod and reason about its overhead.

    **Syllabus:** `Miscellaneous → Web Profiler` ·
    **Level:** Advanced ·
    **Est. time:** 35 min ·
    **Prerequisites:** [Request Handling](../architecture/request-handling.md)

---

## Theory

The **Web Profiler** stores a **profile** per request — timing, DB queries, logs,
events, security, cache — and renders the **Web Debug Toolbar** at the bottom of
HTML responses. Each panel is fed by a **data collector**. It is a dev tool,
disabled in prod. (For consuming profiles in tests, see
[The Profiler Object](../testing/profiler.md).)

## Deep Dive — how it works internally

!!! question "Predict first"
    Your custom collector stores the live PDO connection in `$this->data` so the
    panel can query it. The request errors with a serialization failure. Why?

??? note "Reveal"
    Profiles are **serialized** to storage (cloned via VarDumper). A live PDO
    connection/resource isn't serializable. Store scalar/array snapshots instead —
    exactly the data the panel will render.

### Collection lifecycle

The `Symfony\Bundle\FrameworkBundle`/`WebProfilerBundle` register a
`Symfony\Component\HttpKernel\Profiler\Profiler` and a listener on
`kernel.response`. Each registered collector implements
`Symfony\Component\HttpKernel\DataCollector\DataCollectorInterface`:

```php
public function collect(Request $request, Response $response, ?\Throwable $exception = null): void;
public function getName(): string;
public function reset(): void;
```

On `kernel.response`, `Profiler::collect()` calls every collector's `collect()`;
the resulting `Profile` (a set of collectors with their `$this->data`) is saved
to a storage backend (`FileProfilerStorage` by default) keyed by a token. The
toolbar is injected into the HTML by `WebDebugToolbarListener` (a sub-request
renders it). The full profiler UI at `/_profiler/{token}` reads stored profiles.

```mermaid
flowchart LR
    RESP[kernel.response] --> P[Profiler::collect]
    P --> C1[collect on each DataCollector]
    C1 --> PR[Profile stored by token]
    PR --> TB[Toolbar injected]
    PR --> UI[/_profiler UI/]
```

Collectors typically extend
`Symfony\Component\HttpKernel\DataCollector\DataCollector` (which provides a
`$this->data` array serialized via VarDumper's cloner, so it survives storage).
`reset()` clears state between requests in long-running workers.

!!! note "Source reference"
    `Symfony\Component\HttpKernel\DataCollector\DataCollectorInterface` and
    `Profiler` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/DataCollector/DataCollectorInterface.php).

### Late collectors

`LateDataCollectorInterface::lateCollect()` runs later (at `kernel.terminate`
via the profiler) for data not available during `kernel.response` (e.g. the final
list of dumps, cache calls). Implement it when your metric is only complete
post-response.

### Custom template

A collector's panel is a Twig template extending
`@WebProfiler/Profiler/layout.html.twig`, associated via the
`data_collector` service tag's `template` attribute. It renders the toolbar
badge (`block toolbar`) and the panel (`block panel`).

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\DataCollector;

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\HttpKernel\DataCollector\DataCollector;

    final class TenantCollector extends DataCollector
    {
        public function collect(Request $request, Response $response, ?\Throwable $exception = null): void
        {
            $this->data = ['tenant' => $request->headers->get('X-Tenant', 'none')];
        }

        public function getTenant(): string
        {
            return $this->data['tenant'];
        }

        public function getName(): string
        {
            return 'app.tenant';
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/services.yaml (autoconfigure tags the collector automatically)
    services:
        App\DataCollector\TenantCollector:
            tags:
                - { name: data_collector, template: 'data_collector/tenant.html.twig', id: 'app.tenant' }
    ```

=== "Console"

    ```console
    $ php bin/console debug:container --tag=data_collector
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Store only serializable data in `$this->data` | Keeping live objects/resources |
| Implement `reset()` for worker reuse | Accumulating state across requests |
| Use `LateDataCollectorInterface` for post-response data | Collecting incomplete data early |
| Keep the profiler **off** in prod | Shipping `web-profiler-bundle` to prod as non-dev |

## When (not) to use it / alternatives

Add a custom collector to surface app-specific diagnostics (current tenant,
feature flags, external API timings) during development. Never enable the
profiler in production — it adds storage + memory overhead and can leak internal
data. For prod observability use proper metrics/tracing.

!!! danger "Certification traps"
    - Collection happens on **`kernel.response`**; late collectors run at terminate.
    - The profiler is a **dev** tool — disabled in prod (`framework.profiler` off).
    - `$this->data` must be serializable (cloned via VarDumper) to survive storage.
    - `data_collector` tag needs a `template` for a toolbar/panel to appear.

!!! warning "Common mistakes"
    - Storing a PDO/entity in `$this->data` → serialization failure.
    - Expecting profiler data in prod responses.

## Exercises

1. **(Advanced)** Write a collector capturing the `X-Tenant` header and expose it.
2. **(Advanced)** Explain why `$this->data` cannot hold a database connection.

??? success "Solutions"

    **1.** See `TenantCollector` above plus the `data_collector` tag with a template.

    **2.** Profiles are serialized to storage; a live connection/resource is not
    serializable, so store scalar/array data (VarDumper-clonable) instead.

## Certification questions

??? question "Q1. When does the profiler collect data for a request?"
    - [x] A. On `kernel.response` (late collectors at terminate) ✅
    - [ ] B. On `kernel.request`
    - [ ] C. Only in the CLI

    **Why:** `Profiler::collect()` runs on the response event; late collection at
    terminate. **Ref:** [Profiler](https://symfony.com/doc/current/profiler.html).

??? question "Q2. Which tag registers a custom data collector?"
    - [x] A. `data_collector` ✅
    - [ ] B. `kernel.collector`
    - [ ] C. `profiler.panel`

    **Why:** The `data_collector` tag (with a `template`) wires the collector +
    panel. **Ref:** [Creating a data collector](https://symfony.com/doc/current/profiler/data_collector.html).

??? question "Q3. Should the profiler run in production?"
    - [ ] A. Yes, for monitoring
    - [x] B. No — it is a dev tool and is disabled in prod ✅
    - [ ] C. Only for admins

    **Why:** It adds overhead and exposes internals; keep it off in prod.
    **Ref:** [Profiler](https://symfony.com/doc/current/profiler.html).

## Key takeaways

- Collectors implement `DataCollectorInterface`; data stored in `$this->data`.
- Collection on `kernel.response`; `LateDataCollectorInterface` at terminate.
- Register with the `data_collector` tag + a Twig panel template.
- Dev-only; disable in prod for performance and safety.

## Last-minute revision

!!! tip "Cheat sheet"
    - `collect(Request, Response, ?Throwable)`, `getName()`, `reset()`.
    - Extend `DataCollector`; store serializable `$this->data`.
    - Tag `data_collector` + `template:`; profiler UI at `/_profiler`.
    - `LateDataCollectorInterface::lateCollect()` for post-response data.

## Connections

- **Depends on:** [Request Handling](../architecture/request-handling.md) — collection hooks `kernel.response`; [Debugging](debugging.md) — dumps feed the Debug panel.
- **Reused in:** [The Profiler Object](../testing/profiler.md) — functional tests read stored profiles to assert queries/emails.
- **Confused with:** production observability — the profiler is a dev-only tool, not a metrics backend.

## Official References
- [Official docs — Profiler](https://symfony.com/doc/current/profiler.html)
- [Official docs — Custom data collector](https://symfony.com/doc/current/profiler/data_collector.html)
- [Symfony source — DataCollectorInterface](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/HttpKernel/DataCollector/DataCollectorInterface.php)

## Confidence check

I'm ready when I can:

- [ ] explain **why** profiles are stored per request keyed by token
- [ ] write a `DataCollector` + panel template and tag it in Symfony 8
- [ ] debug a serialization failure from non-serializable `$this->data`
- [ ] spot the trick: collection on `kernel.response`, late collectors at terminate; dev-only
- [ ] describe when to use `LateDataCollectorInterface`

---

<small>Related: [Debugging](debugging.md) · [The Profiler Object](../testing/profiler.md) · [Error Handling](error-handling.md)</small>
