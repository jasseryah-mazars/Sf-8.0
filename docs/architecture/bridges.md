# Bridges

!!! tip "In a nutshell"
    A bridge is the glue that lets a Symfony component work with one specific
    third-party library, kept in its own package so the component stays
    dependency-free. Highest-yield: bridges live in `src/Symfony/Bridge/`, provide
    classes, and are wired into an app by a **bundle**.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Define what a Symfony **bridge** is and why it exists.
    - [ ] Locate bridges in the source tree and distinguish them from components and bundles.
    - [ ] Recognise the categories of bridge without treating any third-party library as in-scope.

    **Syllabus:** `Symfony Architecture → Bridges` ·
    **Level:** Advanced ·
    **Est. time:** 15 min ·
    **Prerequisites:** [Components](components.md)

---

## Theory

A **bridge** is an integration layer that lets a Symfony component work smoothly
with a **specific third-party library**. It contains the glue — adapters, factory
classes, DI configuration — that belongs to *neither* the pure Symfony component
*nor* the external library, so it lives in its own package to keep both sides
decoupled.

!!! info "Scope note"
    This chapter explains the **concept** of a bridge. It deliberately does **not**
    teach how to use any specific third-party library through its bridge — those
    libraries (templating engines, ORMs, loggers, etc.) are out of scope for this
    platform.

## Deep Dive — how it works internally

!!! question "Predict first"
    A class from a Symfony bridge isn't available in your app even though the bridge
    package is installed. What is the most likely reason?

??? note "Reveal"
    A bridge only *provides* classes — a **bundle** registers them as services and
    exposes config. Without the integrating bundle enabled, the bridge's classes are
    on the autoloader but never wired into the container.

### Where bridges live

Bridges live under `src/Symfony/Bridge/` in the monorepo and ship as packages
named `symfony/<name>-bridge`. Structurally a bridge is just another Composer
package that depends on both a Symfony component (or contract) and the external
library it targets.

```mermaid
flowchart LR
    Lib[Third-party library] --- Bridge[symfony/*-bridge]
    Comp[Symfony component] --- Bridge
    Bridge --> App[Application via a bundle]
```

### Bridge vs component vs bundle

| Layer | Depends on | Purpose |
|---|---|---|
| Component | Nothing external | Reusable Symfony library |
| **Bridge** | Component **+** a specific 3rd-party lib | Adapters/glue for that lib |
| Bundle | Components/bridges | Registers services + config in the framework |

A bridge is typically **activated by a bundle**: the bundle's extension registers
the bridge's classes as services and exposes configuration. So a bridge provides
the classes; a bundle wires them into the container. See
[Components](components.md) and [Code Organization](code-organization.md).

### Why not put the glue in the component?

Because a component must stay **dependency-free** of any particular external
library, so it remains usable by everyone. Pushing the coupling into a separate
bridge package means:

- the component's dependency graph stays minimal,
- the external library is an **optional** dependency (only the bridge requires it),
- versioning of the integration is independent.

!!! note "Source reference"
    Bridge packages —
    [symfony/symfony `8.0` `src/Symfony/Bridge`](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge).

## Configuration & code

=== "Conceptual dependency graph"

    ```json
    {
      "require": {
        "symfony/some-component": "^8.0",
        "vendor/some-library": "^3.0"
      }
    }
    ```

=== "Console"

    ```console
    $ composer show 'symfony/*-bridge' --direct
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Let the relevant bundle pull the bridge transitively | Requiring a bridge you don't use |
| Understand a bridge is *glue*, not a feature by itself | Treating a bridge as a standalone app framework |
| Keep components free of third-party deps | Adding external library deps to a component |

## When (not) to use it / alternatives

You seldom install a bridge directly — a bundle that integrates the third-party
library declares the bridge as its dependency. You only reason about bridges when
building your **own** integration package or debugging why a class from a bridge is
(not) available.

!!! danger "Certification traps"
    - A bridge couples a component to **one specific** external library; it is not a
      general-purpose component.
    - Bridges live in `src/Symfony/Bridge/`, separate from `src/Symfony/Component/`
      and `src/Symfony/Bundle/`.
    - A bridge provides classes; a **bundle** registers them as services.

!!! warning "Common mistakes"
    - Confusing a bridge (glue library) with a bundle (framework config).
    - Expecting a bridge to configure itself without a bundle.

## Exercises

1. **(Advanced)** In one sentence each, distinguish component, bridge and bundle.
2. **(Expert)** Explain why the external library is an *optional* dependency of the
   component but a *required* dependency of the bridge.

??? success "Solutions"

    **1.** Component = standalone Symfony library; bridge = adapter coupling a
    component to a specific third-party library; bundle = framework integration that
    registers services and configuration.

    **2.** Keeping it optional on the component preserves the component's minimal,
    reusable dependency graph; the bridge exists precisely to depend on that library,
    so it requires it.

## Certification questions

??? question "Q1. What is a Symfony bridge?"
    - [x] A. An integration layer between a component and a specific third-party library ✅
    - [ ] B. A configuration format
    - [ ] C. A replacement for the container

    **Why:** Bridges hold the glue that couples a component to one external library.
    **Ref:** [Bridges directory](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge).

??? question "Q2. Where do bridges live in the monorepo?"
    - [x] A. `src/Symfony/Bridge/` ✅
    - [ ] B. `src/Symfony/Component/`
    - [ ] C. `src/Symfony/Bundle/`

    **Why:** Bridges have their own top-level directory. **Ref:**
    [Symfony source layout](https://github.com/symfony/symfony/tree/8.0/src/Symfony).

??? question "Q3. What activates a bridge inside a framework app?"
    - [x] A. A bundle that registers the bridge's classes as services ✅
    - [ ] B. The bridge auto-registers itself
    - [ ] C. A Twig template

    **Why:** Bridges provide classes; a bundle wires them. **Ref:**
    [Bundles](https://symfony.com/doc/current/bundles.html).

## Key takeaways

- A bridge is glue between a component and one specific third-party library.
- It keeps components free of external dependencies.
- Bridges live in `src/Symfony/Bridge/` and are typically wired by a bundle.

## Last-minute revision

!!! tip "Cheat sheet"
    - Bridge = component + specific 3rd-party lib.
    - Package name: `symfony/<name>-bridge`; dir `src/Symfony/Bridge/`.
    - Classes come from the bridge, services from a bundle.

## Connections

- **Depends on:** [Components](components.md) — a bridge couples one component to a specific third-party library.
- **Reused in:** [Code Organization](code-organization.md) — a bundle wires a bridge's classes into the app; [Dependency Injection](../dependency-injection/index.md) is where that registration happens.
- **Confused with:** [Framework Overloading](overloading.md) — overriding customises a bundle, not gluing a component to an external library.

## Official References
- [Symfony source — Bridge](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)
- [Official docs — The Components](https://symfony.com/doc/current/components/index.html)
- [Official docs — Bundles](https://symfony.com/doc/current/bundles.html)

## Confidence check

I'm ready when I can:

- [ ] explain **why** glue lives in a bridge rather than inside the component
- [ ] locate bridges in the source tree (`src/Symfony/Bridge/`)
- [ ] debug a missing bridge class caused by the integrating bundle not being enabled
- [ ] spot the distinction between a bridge and a bundle
- [ ] explain why the external library is optional for the component but required for the bridge

---

<small>Related: [Components](components.md) · [Code Organization](code-organization.md) · [Framework Overloading](overloading.md)</small>
