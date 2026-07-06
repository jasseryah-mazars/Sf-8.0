# Routing

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
