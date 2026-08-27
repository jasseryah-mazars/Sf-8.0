# Dependency Injection

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Compiler Pass Registry](../labs/dependency-injection.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Le composant **DependencyInjection** est la colonne vertébrale de Symfony : il construit
et câble le *service container* dans lequel tous les autres composants puisent. Le
comprendre — en particulier la séparation entre **compilation (build time)** et
**runtime**, ainsi que le **cache du container compilé** — est ce qui distingue un
candidat Advanced d'un candidat Expert. Presque toutes les questions d'examen des
étapes suivantes (Security, Console, Forms, Messenger) supposent que vous savez déjà
comment les services sont définis, résolus et injectés.

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

Symfony est un container qui démarre un kernel. Le
`Symfony\Component\DependencyInjection\ContainerBuilder` lit votre configuration,
exécute les **compiler passes**, résout l'**autowiring**, fige le résultat et écrit
une classe de **container compilé** dans `var/cache/`. À l'exécution, votre
application dialogue avec cette `Symfony\Component\DependencyInjection\ContainerInterface`
dumpée, jamais avec le builder. La plus grande source de confusion — et de pièges à
l'examen — est de ne pas savoir dans lequel de ces deux mondes vit une fonctionnalité
donnée.

Cette étape enseigne d'abord le modèle mental (un service, le cycle de vie de la
compilation, le cache compilé), puis ajoute couche par couche les parameters,
l'enregistrement, l'autowiring, les tags, la décoration, les factories, les compiler
passes et les service locators.

## Micro-chapters

Parcourez-les dans l'ordre :

- [ ] [The Service Container](container.md) — ce qu'est un service, le cycle de vie
  de la compilation, le container compilé, `get()`, services publics vs privés.
- [ ] [Built-in Services](built-in-services.md) — les services du framework et
  comment les découvrir avec `debug:container`.
- [ ] [Configuration Parameters](parameters.md) — `%param%`, variables d'environnement
  et processors, `ParameterBagInterface`, `#[Autowire]` avec params/env.
- [ ] [Service Registration](registration.md) — les defaults de `services.yaml`,
  resource/exclude, `#[Autoconfigure]`, définitions manuelles, arguments, calls,
  aliases.
- [ ] [Service Decoration](decoration.md) — `decorates`, priorité,
  `.inner`, `#[AsDecorator]`, `#[AutowireDecorated]`.
- [ ] [Tags](tags.md) — tagged iterators et locators, priorité, index methods,
  autoconfiguration d'interfaces vers des tags.
- [ ] [Semantic Configuration](semantic-config.md) — `Configuration` de bundle,
  `TreeBuilder`, `Extension::load()`, `prependExtension()`.
- [ ] [Factories](factories.md) — factories statiques / d'instance / invokables,
  expression factories, passage d'arguments.
- [ ] [Compiler Passes](compiler-passes.md) — `CompilerPassInterface`, les phases de
  `PassConfig`, `findTaggedServiceIds()`, quand les utiliser vs autoconfigure.
- [ ] [Autowiring](autowiring.md) — résolution par type-hint, `#[Autowire]`,
  named aliases, `#[Target]`, binding, erreurs d'ambiguïté.
- [ ] [Service Locators](service-locators.md) — `ServiceLocator`,
  `#[AutowireLocator]`, service subscribers, accès lazy à la demande.

## How to study it

1. Ancrez le modèle mental avec [The Service Container](container.md) — la
   séparation compile-vs-runtime est la clé de tout le reste.
2. Apprenez comment les services sont *définis* : [Parameters](parameters.md),
   [Registration](registration.md), [Autowiring](autowiring.md).
3. Ajoutez les patterns de *câblage* : [Tags](tags.md), [Decoration](decoration.md),
   [Factories](factories.md), [Service Locators](service-locators.md).
4. Terminez par les hooks du *build-time* : [Compiler Passes](compiler-passes.md) et
   [Semantic Configuration](semantic-config.md), plus
   [Built-in Services](built-in-services.md) pour vous orienter.

---

<small>Related: [Symfony Architecture](../architecture/index.md) ·
[Controllers](../controllers/index.md) · [Console](../console/index.md)</small>

## Official References

- [Symfony documentation — Service Container](https://symfony.com/doc/8.0/service_container.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
