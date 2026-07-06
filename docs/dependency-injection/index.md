# Dependency Injection

The **DependencyInjection** component is the backbone of Symfony: it builds and
wires the *service container* that every other component pulls from. Understanding
it — especially the split between **compilation (build time)** and **runtime**, and
the **compiled container cache** — is what separates an Advanced candidate from an
Expert one. Almost every exam question in later stages (Security, Console, Forms,
Messenger) assumes you already know how services are defined, resolved and injected.

!!! info "Stage at a glance"
    | Property | Value |
    |---|---|
    | **Prerequisites** | [Symfony Architecture](../architecture/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★★ |
    | **Dependencies** | Stage 3 (kernel, events, request lifecycle) |
    | **Revision priority** | **Critical** |
    | **Est. time** | 6–8 h |

## Why this stage matters

Symfony is a container that boots a kernel. The
`Symfony\Component\DependencyInjection\ContainerBuilder` reads your configuration,
runs **compiler passes**, resolves **autowiring**, freezes the result and dumps a
**compiled container** class to `var/cache/`. At runtime your app talks to that
dumped `Symfony\Component\DependencyInjection\ContainerInterface`, never to the
builder. The single biggest source of confusion — and exam traps — is not knowing
which of those two worlds a given feature lives in.

This stage teaches the mental model first (a service, the compilation lifecycle,
the compiled cache), then layers on parameters, registration, autowiring, tags,
decoration, factories, compiler passes and service locators.

## Micro-chapters

Work through them in order:

- [ ] [The Service Container](container.md) — what a service is, the compilation
  lifecycle, the compiled container, `get()`, public vs private services.
- [ ] [Built-in Services](built-in-services.md) — framework services and how to
  discover them with `debug:container`.
- [ ] [Configuration Parameters](parameters.md) — `%param%`, env vars &
  processors, `ParameterBagInterface`, `#[Autowire]` with params/env.
- [ ] [Service Registration](registration.md) — `services.yaml` defaults,
  resource/exclude, `#[Autoconfigure]`, manual definitions, arguments, calls,
  aliases.
- [ ] [Service Decoration](decoration.md) — `decorates`, priority,
  `.inner`, `#[AsDecorator]`, `#[AutowireDecorated]`.
- [ ] [Tags](tags.md) — tagged iterators & locators, priority, index methods,
  autoconfiguring interfaces to tags.
- [ ] [Semantic Configuration](semantic-config.md) — bundle `Configuration`,
  `TreeBuilder`, `Extension::load()`, `prependExtension()`.
- [ ] [Factories](factories.md) — static / instance / invokable factories,
  expression factories, passing arguments.
- [ ] [Compiler Passes](compiler-passes.md) — `CompilerPassInterface`, the
  `PassConfig` phases, `findTaggedServiceIds()`, when to use vs autoconfigure.
- [ ] [Autowiring](autowiring.md) — type-hint resolution, `#[Autowire]`,
  named aliases, `#[Target]`, binding, ambiguity errors.
- [ ] [Service Locators](service-locators.md) — `ServiceLocator`,
  `#[AutowireLocator]`, service subscribers, lazy on-demand access.

## How to study it

1. Nail the mental model with [The Service Container](container.md) — the
   compile-vs-runtime split is the key to everything else.
2. Learn how services get *defined*: [Parameters](parameters.md),
   [Registration](registration.md), [Autowiring](autowiring.md).
3. Add the *wiring* patterns: [Tags](tags.md), [Decoration](decoration.md),
   [Factories](factories.md), [Service Locators](service-locators.md).
4. Finish with the *build-time* hooks: [Compiler Passes](compiler-passes.md) and
   [Semantic Configuration](semantic-config.md), plus
   [Built-in Services](built-in-services.md) for orientation.

---

<small>Related: [Symfony Architecture](../architecture/index.md) ·
[Controllers](../controllers/index.md) · [Console](../console/index.md)</small>

## Official References

- [Symfony documentation — Service Container](https://symfony.com/doc/current/service_container.html)
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
