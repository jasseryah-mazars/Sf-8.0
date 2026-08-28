# Routing

!!! tip "🧪 Practice this area"
    Ready to build it yourself? Do the hands-on lab: **[Match & Debug](../labs/routing.md)** — a step-by-step TD with test-first guidance and a reference solution.

The **Routing** component turns an incoming URL into a controller and, in
reverse, turns a route name back into a URL. It is the layer that sits between
the [Controllers](../controllers/index.md) stage and the HTTP request lifecycle:
a `RouteCollection` is compiled once, matched on every request by a `UrlMatcher`,
and inverted by a `UrlGenerator`. Master the compiled-router cache, requirement
regexes, and reference types and this stage is largely reading comprehension.

!!! info "Stage at a glance"
    | Field | Value |
    |---|---|
    | **Prerequisites** | [Controllers](../controllers/index.md), [HTTP](../http/index.md) |
    | **Level** | Advanced → Expert |
    | **Difficulty** | ★★☆ |
    | **Dependencies** | Controllers (stage 5) |
    | **Revision priority** | **High** |
    | **Est. time** | 3–4 h |

## 🧠 Pour les nuls

**C'est quoi cette étape ?** Le routeur est l'aiguilleur qui décide, pour chaque URL demandée, quel morceau de code (quel contrôleur) doit répondre.

**Pourquoi ça existe ?** Sans routeur, il faudrait écrire toi-même un immense `if/else` sur l'URL dans un seul fichier géant. Le routeur automatise cette correspondance URL → code, dans les deux sens (il sait aussi reconstruire une URL à partir d'un nom de route).

**🏠 Analogie de la vraie vie :** Un standard téléphonique d'entreprise. Tu composes une extension (l'URL), le standard (le routeur) regarde son annuaire et te connecte au bon bureau (le contrôleur). Et si un collègue change de bureau, le standard peut aussi te donner le nouveau numéro à composer (générer une URL à partir d'un nom).

**Symfony dans la vraie vie :** `#[Route('/produits/{id}')]` est l'entrée d'annuaire ; `UrlMatcher` est le standardiste qui trouve la bonne ligne ; `UrlGenerator` fait l'inverse (nom de route → URL réelle).

**⚠️ Erreur fréquente :** déclarer une route générique (`/produits/{id}`) avant une route spécifique (`/produits/nouveau`) — la première capture tout, la seconde n'est jamais atteinte.

**🧠 Comment le mémoriser :** "Le routeur ne devine jamais — il compare, dans l'ordre, jusqu'à trouver un match."

## Why routing pairs with controllers

A route is meaningless without a controller to run, and a controller is
unreachable without a route. Symfony expresses routes primarily as `#[Route]`
attributes on controller methods, with YAML as the declarative alternative. Under
the hood the component compiles every route to a `CompiledRoute` (a static regex
plus token list), dumps the whole collection to a single PHP file, and matches
against it with a generated, `opcache`-friendly matcher. Knowing that pipeline
explains every performance and precedence question the exam asks.

## Micro-chapters

- [Configuration (YAML & Attributes)](configuration.md) — define routes with
  `#[Route]` and YAML: name, path, controller mapping, prefixes, import.
- [Restrict URL Parameters](requirements.md) — `requirements`, inline
  `{id<\d+>}` regex, parameter constraints and precedence.
- [Default Values](defaults.md) — `defaults`, inline `{page<\d+>?1}`, optional
  trailing parameters.
- [Generate URLs](url-generation.md) — `UrlGeneratorInterface`, `generateUrl()`,
  reference types (absolute/relative/network), extra params as query string.
- [Trigger Redirects](redirects.md) — `RedirectController`, redirect-only routes,
  trailing-slash behaviour.
- [Special Internal Attributes](special-attributes.md) — `_controller`,
  `_format`, `_locale`, `_fragment`, `_route`, `_route_params`; stateless routes.
- [Domain Name Matching](host-matching.md) — `host`, host requirements/defaults,
  multi-domain routing.
- [Conditional Matching](conditions.md) — `condition` expressions with
  ExpressionLanguage: `context`, `request`, `env()`, `service()`.
- [HTTP Methods Matching](methods.md) — `methods`, combining with `schemes`.
- [Locale Guessing](locale.md) — `_locale`, prefixed localized paths, i18n
  routing, locale detection.
- [Router Debugging](debugging.md) — `debug:router`, `router:match`, cache
  implications.

## How to study this stage

1. Read [Configuration](configuration.md) then [Requirements](requirements.md)
   and [Defaults](defaults.md) as a trio — they share the matcher mental model.
2. Do the [URL generation](url-generation.md) exercises hands-on; reference-type
   questions are a certification favourite.
3. Treat [Special attributes](special-attributes.md), [conditions](conditions.md)
   and [host matching](host-matching.md) as the "expert" trap zone.
4. Finish with [debugging](debugging.md) to tie matching and generation together.

---

<small>Prev: [Controllers](../controllers/index.md) · Next: [Twig](../twig/index.md) · Related: [Locale & Intl](../miscellaneous/intl.md)</small>

## Official References

- [Symfony documentation — Routing](https://symfony.com/doc/8.0/routing.html)
- [Symfony documentation home](https://symfony.com/doc/8.0/)
- [Official certification syllabus](https://certification.symfony.com/exams/symfony.html)
