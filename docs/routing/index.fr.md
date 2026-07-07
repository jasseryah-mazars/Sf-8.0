# Routing

!!! tip "🧪 Practice this area"
    Prêt à le construire vous-même ? Faites le lab pratique : **[Match & Debug](../labs/routing.md)** — un TD pas à pas avec une démarche test-first et une solution de référence.

Le composant **Routing** transforme une URL entrante en controller et, en sens
inverse, retransforme un nom de route en URL. C'est la couche située entre
l'étape [Controllers](../controllers/index.md) et le cycle de vie de la request HTTP :
une `RouteCollection` est compilée une seule fois, confrontée à chaque request par un `UrlMatcher`,
et inversée par un `UrlGenerator`. Maîtrisez le cache du router compilé, les regex de
requirements et les reference types, et cette étape relève en grande partie de la simple lecture.

!!! info "Stage at a glance"
    | Field | Value |
    |---|---|
    | **Prerequisites** | [Controllers](../controllers/index.md), [HTTP](../http/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Controllers (stage 5) |
    | **Revision priority** | **High** |
    | **Est. time** | 3–4 h |

## Why routing pairs with controllers

Une route n'a aucun sens sans un controller à exécuter, et un controller est
inaccessible sans route. Symfony exprime les routes principalement sous forme d'attributs `#[Route]`
sur les méthodes des controllers, le YAML étant l'alternative déclarative. Sous
le capot, le composant compile chaque route en une `CompiledRoute` (une regex statique
plus une liste de tokens), déverse toute la collection dans un unique fichier PHP, et effectue
le matching avec un matcher généré, compatible `opcache`. Connaître ce pipeline
explique toutes les questions de performance et de priorité posées à l'examen.

## Micro-chapters

- [Configuration (YAML & Attributes)](configuration.md) — définir des routes avec
  `#[Route]` et YAML : name, path, mapping vers le controller, préfixes, import.
- [Restrict URL Parameters](requirements.md) — `requirements`, regex inline
  `{id<\d+>}`, contraintes de paramètres et ordre de priorité.
- [Default Values](defaults.md) — `defaults`, `{page<\d+>?1}` inline, paramètres
  optionnels en fin de path.
- [Generate URLs](url-generation.md) — `UrlGeneratorInterface`, `generateUrl()`,
  reference types (absolute/relative/network), paramètres supplémentaires en query string.
- [Trigger Redirects](redirects.md) — `RedirectController`, routes de redirection pure,
  comportement du slash final.
- [Special Internal Attributes](special-attributes.md) — `_controller`,
  `_format`, `_locale`, `_fragment`, `_route`, `_route_params` ; routes stateless.
- [Domain Name Matching](host-matching.md) — `host`, requirements/defaults sur le host,
  routing multi-domaines.
- [Conditional Matching](conditions.md) — expressions `condition` avec
  ExpressionLanguage : `context`, `request`, `env()`, `service()`.
- [HTTP Methods Matching](methods.md) — `methods`, combinaison avec `schemes`.
- [Locale Guessing](locale.md) — `_locale`, paths localisés préfixés, routing
  i18n, détection de la locale.
- [Router Debugging](debugging.md) — `debug:router`, `router:match`, implications
  du cache.

## How to study this stage

1. Lisez [Configuration](configuration.md) puis [Requirements](requirements.md)
   et [Defaults](defaults.md) comme un trio — ils partagent le même modèle mental du matcher.
2. Faites les exercices de [URL generation](url-generation.md) en pratique ; les questions
   sur les reference types sont un grand classique de la certification.
3. Considérez [Special attributes](special-attributes.md), [conditions](conditions.md)
   et [host matching](host-matching.md) comme la zone de pièges « expert ».
4. Terminez par le [debugging](debugging.md) pour relier matching et génération.

---

<small>Prev: [Controllers](../controllers/index.md) · Next: [Twig](../twig/index.md) · Related: [Locale & Intl](../miscellaneous/intl.md)</small>

## Official References

- [Symfony documentation — Routing](https://symfony.com/doc/current/routing.html)
- [Symfony documentation home](https://symfony.com/doc/current/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
