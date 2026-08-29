# Bridges

!!! tip "In a nutshell"
    Un bridge est la colle qui permet à un composant Symfony de fonctionner avec une
    bibliothèque tierce spécifique, isolée dans son propre package pour que le composant
    reste sans dépendance. À retenir en priorité : les bridges vivent dans
    `src/Symfony/Bridge/`, fournissent des classes, et sont branchés dans une application
    par un **bundle**.

!!! example "Real-world analogy"
    Un bridge, c'est comme un adaptateur de voyage. Votre chargeur d'ordinateur portable
    (un composant Symfony) est conçu pour un standard de prise, et une prise murale
    étrangère (une bibliothèque tierce spécifique) pour un autre ; l'adaptateur existe
    uniquement pour marier ces deux formes. Il n'est ni le chargeur ni la prise, et vous
    l'achetez comme un article séparé précisément pour que le chargeur lui-même reste
    universel et ne porte aucun bagage propre à un pays. Mais l'adaptateur seul n'alimente
    rien — vous devez encore brancher l'ensemble au mur (activer le bundle d'intégration)
    avant que le courant ne passe.

!!! abstract "Learning objectives"
    À la fin de ce chapitre, vous saurez :

    - [ ] Définir ce qu'est un **bridge** Symfony et pourquoi il existe.
    - [ ] Localiser les bridges dans l'arborescence des sources et les distinguer des composants et des bundles.
    - [ ] Reconnaître les catégories de bridges sans considérer aucune bibliothèque tierce comme au programme.

    **Syllabus:** `Symfony Architecture → Bridges` ·
    **Level:** Advanced ·
    **Est. time:** 15 min ·
    **Prerequisites:** [Components](components.md)

---

## Pour les nuls

### L'idée en une phrase
Un bridge est un adaptateur qui fait parler entre eux un composant Symfony et une bibliothèque tierce précise — sans forcer le composant lui-même à dépendre de cette bibliothèque.

### Imagine dans la vraie vie
Un adaptateur de voyage électrique : ton chargeur (le composant Symfony) est conçu pour un standard de prise, la prise murale étrangère (une bibliothèque tierce précise) en utilise un autre — l'adaptateur existe uniquement pour faire correspondre les deux formes. Ce n'est ni le chargeur ni la prise ; tu l'achètes séparément justement pour que le chargeur reste universel.

### Dans Symfony
Le composant PropertyInfo reste indépendant de PHPStan, mais un bridge dédié permet de l'utiliser avec cet outil précis, sans forcer tous les utilisateurs de PropertyInfo à installer PHPStan.

### Exemple simple
Un bridge vit dans `src/Symfony/Bridge/` — par exemple, un bridge PSR-7 convertit entre les objets `Request`/`Response` de Symfony et les interfaces PSR-7 attendues par une bibliothèque tierce.

### Comment le mémoriser 🧠
L'adaptateur seul ne branche rien : il faut encore brancher l'ensemble dans le mur (activer le bundle qui l'intègre) avant que le courant ne passe.


## Theory

Un **bridge** est une couche d'intégration qui permet à un composant Symfony de
fonctionner harmonieusement avec une **bibliothèque tierce spécifique**. Il contient la
colle — adaptateurs, classes factory, configuration de dependency injection — qui
n'appartient *ni* au composant Symfony pur *ni* à la bibliothèque externe ; il vit donc
dans son propre package afin de garder les deux côtés découplés.

!!! info "Scope note"
    Ce chapitre explique le **concept** de bridge. Il n'enseigne délibérément **pas**
    comment utiliser une bibliothèque tierce donnée via son bridge — ces bibliothèques
    (moteurs de templates, ORM, loggers, etc.) sont hors du périmètre de cette
    plateforme.

## Deep Dive — how it works internally

!!! question "Predict first"
    Une classe d'un bridge Symfony n'est pas disponible dans votre application alors que
    le package du bridge est installé. Quelle est la raison la plus probable ?

??? note "Reveal"
    Un bridge ne fait que *fournir* des classes — c'est un **bundle** qui les enregistre
    comme services et expose la config. Sans le bundle d'intégration activé, les classes
    du bridge sont sur l'autoloader mais ne sont jamais branchées dans le container.

### Where bridges live

Les bridges vivent sous `src/Symfony/Bridge/` dans le monorepo et sont distribués comme
packages nommés `symfony/<name>-bridge`. Structurellement, un bridge n'est qu'un package
Composer de plus, qui dépend à la fois d'un composant Symfony (ou d'un contract) et de
la bibliothèque externe qu'il cible.

```console
# In the monorepo, bridges have their own top-level directory
$ ls src/Symfony/Bridge/
Doctrine/  Monolog/  PsrHttpMessage/  Twig/

# Each ships as a standalone Composer package named symfony/<name>-bridge
$ composer show 'symfony/*-bridge' --direct
symfony/monolog-bridge  v8.0.0  Provides integration for Monolog with various Symfony components
```

```mermaid
flowchart LR
    Lib[Third-party library] --- Bridge[symfony/*-bridge]
    Comp[Symfony component] --- Bridge
    Bridge --> App[Application via a bundle]
```

### Bridge vs component vs bundle

| Couche | Dépend de | Rôle |
|---|---|---|
| Composant | Rien d'externe | Bibliothèque Symfony réutilisable |
| **Bridge** | Composant **+** une bibliothèque tierce spécifique | Adaptateurs/colle pour cette bibliothèque |
| Bundle | Composants/bridges | Enregistre les services + la config dans le framework |

Un bridge est typiquement **activé par un bundle** : l'extension du bundle enregistre
les classes du bridge comme services et expose la configuration. Le bridge fournit donc
les classes ; un bundle les branche dans le container. Voir
[Components](components.md) et [Code Organization](code-organization.md).

### Why not put the glue in the component?

Parce qu'un composant doit rester **sans dépendance** envers toute bibliothèque externe
particulière, afin de rester utilisable par tous. Repousser le couplage dans un package
bridge séparé signifie que :

- le graphe de dépendances du composant reste minimal,
- la bibliothèque externe est une dépendance **optionnelle** (seul le bridge l'exige),
- le versioning de l'intégration est indépendant.

!!! note "Source reference"
    Packages bridge —
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
| Laisser le bundle concerné tirer le bridge transitivement | Exiger un bridge que vous n'utilisez pas |
| Comprendre qu'un bridge est de la *colle*, pas une fonctionnalité en soi | Traiter un bridge comme un framework applicatif autonome |
| Garder les composants exempts de dépendances tierces | Ajouter des dépendances de bibliothèques externes à un composant |

## When (not) to use it / alternatives

Vous installez rarement un bridge directement — un bundle qui intègre la bibliothèque
tierce déclare le bridge comme sa dépendance. Vous ne raisonnez sur les bridges que
lorsque vous construisez votre **propre** package d'intégration ou que vous déboguez
pourquoi une classe d'un bridge est (ou n'est pas) disponible.

!!! danger "Certification traps"
    - Un bridge couple un composant à **une seule** bibliothèque externe spécifique ; ce
      n'est pas un composant généraliste.
    - Les bridges vivent dans `src/Symfony/Bridge/`, séparés de `src/Symfony/Component/`
      et de `src/Symfony/Bundle/`.
    - Un bridge fournit des classes ; un **bundle** les enregistre comme services.

!!! warning "Common mistakes"
    - Confondre un bridge (bibliothèque de colle) avec un bundle (config du framework).
    - Attendre d'un bridge qu'il se configure lui-même sans bundle.

## Exercises

1. **(Advanced)** En une phrase chacun, distinguez composant, bridge et bundle.
2. **(Expert)** Expliquez pourquoi la bibliothèque externe est une dépendance
   *optionnelle* du composant mais une dépendance *requise* du bridge.

??? success "Solutions"

    **1.** Composant = bibliothèque Symfony autonome ; bridge = adaptateur couplant un
    composant à une bibliothèque tierce spécifique ; bundle = intégration au framework
    qui enregistre services et configuration.

    **2.** La garder optionnelle côté composant préserve le graphe de dépendances
    minimal et réutilisable du composant ; le bridge existe précisément pour dépendre de
    cette bibliothèque, il l'exige donc.

## Certification questions

??? question "Q1. What is a Symfony bridge?"
    - [x] A. An integration layer between a component and a specific third-party library ✅
    - [ ] B. A configuration format
    - [ ] C. A replacement for the container

    **Why:** Les bridges contiennent la colle qui couple un composant à une bibliothèque
    externe.
    **Ref:** [Bridges directory](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge).

??? question "Q2. Where do bridges live in the monorepo?"
    - [x] A. `src/Symfony/Bridge/` ✅
    - [ ] B. `src/Symfony/Component/`
    - [ ] C. `src/Symfony/Bundle/`

    **Why:** Les bridges ont leur propre répertoire de premier niveau. **Ref:**
    [Symfony source layout](https://github.com/symfony/symfony/tree/8.0/src/Symfony).

??? question "Q3. What activates a bridge inside a framework app?"
    - [x] A. A bundle that registers the bridge's classes as services ✅
    - [ ] B. The bridge auto-registers itself
    - [ ] C. A Twig template

    **Why:** Les bridges fournissent des classes ; un bundle les branche. **Ref:**
    [Bundles](https://symfony.com/doc/8.0/bundles.html).

## Key takeaways

- Un bridge est de la colle entre un composant et une bibliothèque tierce spécifique.
- Il garde les composants exempts de dépendances externes.
- Les bridges vivent dans `src/Symfony/Bridge/` et sont typiquement branchés par un bundle.

## Last-minute revision

!!! tip "Cheat sheet"
    - Bridge = composant + bibliothèque tierce spécifique.
    - Nom de package : `symfony/<name>-bridge` ; répertoire `src/Symfony/Bridge/`.
    - Les classes viennent du bridge, les services d'un bundle.

## Connections

- **Depends on:** [Components](components.md) — un bridge couple un composant à une bibliothèque tierce spécifique.
- **Reused in:** [Code Organization](code-organization.md) — un bundle branche les classes d'un bridge dans l'application ; [Dependency Injection](../dependency-injection/index.md) est l'endroit où cet enregistrement a lieu.
- **Confused with:** [Framework Overloading](overloading.md) — surcharger personnalise un bundle, sans coller un composant à une bibliothèque externe.

## Official References
- [Symfony source — Bridge](https://github.com/symfony/symfony/tree/8.0/src/Symfony/Bridge)
- [Official docs — The Components](https://symfony.com/doc/8.0/components/index.html)
- [Official docs — Bundles](https://symfony.com/doc/8.0/bundles.html)

## Video references

!!! tip "Watch & learn"
    Voici des chaînes vidéo officielles, mises à jour en continu — cherchez-y
    « Symfony architecture » pour consolider ce chapitre. Nous lions des chaînes stables
    plutôt que des vidéos individuelles afin que les références ne périment jamais.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — tutoriels scénarisés à suivre en codant.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — conférences et keynotes SymfonyCon.
    - [Official docs for this topic](https://symfony.com/doc/8.0/bundles.html) — certaines pages de la documentation Symfony intègrent un screencast.

## Confidence check

Je suis prêt quand je peux :

- [ ] expliquer **pourquoi** la colle vit dans un bridge plutôt qu'à l'intérieur du composant
- [ ] localiser les bridges dans l'arborescence des sources (`src/Symfony/Bridge/`)
- [ ] déboguer une classe de bridge manquante causée par le bundle d'intégration non activé
- [ ] repérer la distinction entre un bridge et un bundle
- [ ] expliquer pourquoi la bibliothèque externe est optionnelle pour le composant mais requise pour le bridge

---

<small>Related: [Components](components.md) · [Code Organization](code-organization.md) · [Framework Overloading](overloading.md)</small>
