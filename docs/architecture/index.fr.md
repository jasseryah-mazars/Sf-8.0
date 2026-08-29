# Symfony Architecture

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Event Subscriber](../labs/architecture.md)** — un TD pas à pas avec une approche test-first et une solution de référence.

Le kernel, le cycle de vie de la request piloté par les events, le service
container, et la mécanique de releases/BC qui maintient la stabilité de
l'ensemble. C'est le **modèle mental** sur lequel repose tout le reste de la
certification : une fois que vous savez suivre une request depuis
`public/index.php` jusqu'à une `Response` et retour, chaque autre composant
trouve naturellement sa place.

!!! abstract "Stage at a glance"
    - **Prerequisites:** [HTTP](../http/index.md) (modèle request/response)
    - **Level:** Advanced → Expert
    - **Difficulty:** ★★★
    - **Est. time:** 5–7 h
    - **Dependencies:** s'appuie sur HTTP ; alimente
      [Dependency Injection](../dependency-injection/index.md) et
      [Controllers](../controllers/index.md)
    - **Revision priority:** **Critical** — l'étape la plus testée à l'examen ;
      l'ordre des kernel events et la politique BC/dépréciations apparaissent dans presque chaque examen.

## 🧠 Pour les nuls

**C'est quoi cette étape ?** L'architecture Symfony, c'est comment le framework s'assemble : un noyau (kernel) qui reçoit chaque requête, un système d'événements qui prévient tout le monde à chaque étape, et un container qui fabrique tes objets.

**Pourquoi ça existe ?** Sans cette organisation, ajouter une fonctionnalité obligerait à modifier le cœur du framework. Ici, tout composant peut "s'accrocher" au passage de la requête via des événements, sans jamais toucher au code du kernel.

**🏠 Analogie de la vraie vie :** Une chaîne de production d'usine avec des postes de contrôle fixes. Chaque poste (événement) peut inspecter ou modifier la pièce qui passe, sans que la chaîne elle-même ne change — on ajoute un inspecteur à un poste existant, on ne redessine pas toute l'usine.

**Symfony dans la vraie vie :** `HttpKernel::handle()` fait avancer la requête sur la chaîne ; chaque événement (`kernel.request`, `kernel.controller`...) est un poste de contrôle où tes propres listeners peuvent intervenir.

**⚠️ Erreur fréquente :** croire que Symfony est un bloc monolithique — c'est en réalité un ensemble de composants découplés, utilisables même sans le framework complet.

**🧠 Comment le mémoriser :** "Suis la chaîne : Request → Controller → Response, avec un poste de contrôle (événement) entre chaque étape."


## Why this stage is Critical

Symfony n'est pas un monolithe que l'on configure — c'est un ensemble de
**composants découplés** assemblés par un **service container** et pilotés par un
**event dispatcher** autour d'une classe : `HttpKernel`. Comprendre ce flux
explique *où* se brancher (events, resolvers, compiler passes) et *pourquoi* le
framework se comporte comme il le fait. L'examen sonde les détails sans
relâche : l'ordre exact des huit kernel events, ce que la promesse de Backward
Compatibility couvre ou non, et comment les dépréciations sont signalées puis
supprimées.

## Chapters

- [Symfony Flex](flex.md) — recipes, alias, `symfony.lock`, câblage automatique des bundles.
- [License](license.md) — la licence MIT, la marque Symfony, ce que MIT autorise.
- [Components](components.md) — la philosophie des composants découplés et les plus importants d'entre eux.
- [Bridges](bridges.md) — ce qu'est un bridge d'intégration et où il se trouve.
- [Code Organization](code-organization.md) — le squelette d'application et la structure d'un bundle.
- [Request Handling (HttpKernel)](request-handling.md) — **le cœur** : le flux
  complet de `handle()` et les huit kernel events dans l'ordre.
- [Exception Handling](exception-handling.md) — comment les exceptions deviennent des responses.
- [Event Dispatcher & Kernel Events](events.md) — listeners, subscribers,
  priorités, `#[AsEventListener]`, propagation.
- [Official Best Practices](best-practices.md) — la liste canonique des choses à faire et à éviter.
- [Release Management](release-management.md) — SemVer, standard vs LTS, maintenance.
- [Backward Compatibility Promise](bc-promise.md) — `@internal`, `@final`, experimental.
- [Deprecations Best Practices](deprecations.md) — `trigger_deprecation()`, détection, correction.
- [Framework Overloading](overloading.md) — surcharger services, templates, traductions, configuration.
- [Roadmap & Schedule](roadmap-schedule.md) — la cadence mai/novembre et le calendrier 8.x.
- [Interoperability & PSRs](psr.md) — quelles PSR Symfony implémente ou consomme.
- [Naming Conventions](naming-conventions.md) — classes, services, paramètres, routes, variables d'environnement.

## Suggested reading order

Commencez par [Request Handling](request-handling.md) et [Events](events.md)
pour construire le modèle mental du runtime, puis
[Exception Handling](exception-handling.md). Couvrez ensuite
[Components](components.md), [Bridges](bridges.md),
[Code Organization](code-organization.md) et [Flex](flex.md) pour la vue
d'ensemble de l'écosystème. Terminez par le bloc « politique » —
[Release Management](release-management.md),
[BC Promise](bc-promise.md), [Deprecations](deprecations.md),
[Roadmap](roadmap-schedule.md) — qui est du pur gain de points à l'examen.

## Official References

- [Symfony documentation — Symfony Architecture (HttpKernel)](https://symfony.com/doc/8.0/components/http_kernel.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
