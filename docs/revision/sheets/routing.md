# Revision Sheet — Routing

Ultra-condensed, print-friendly recap of every subchapter (key takeaways + last-minute cheat). For the final days. Full detail: [Routing](../../routing/index.md).

## 🧠 Pour les nuls

**C'est quoi ?** Une **fiche imprimable, tenant sur une page**, qui résume chaque sous-chapitre de Routing en quelques puces "à retenir" suivies d'une ligne "Cheat" très dense.

**Pourquoi ça existe ?** Dans les derniers jours avant l'examen, on veut un support papier ou PDF unique par domaine — pas 10 onglets de navigateur ouverts. Cette fiche condense un domaine entier sur une seule page imprimable.

**🏠 Analogie de la vraie vie :** C'est la **fiche de révision recto-verso** qu'un étudiant prépare avant un examen universitaire : tout le cours du semestre réduit à une page, à relire dans le métro le matin de l'épreuve.

**Symfony dans la vraie vie :** Chaque puce "à retenir" → une règle déjà apprise en détail dans le chapitre / La ligne "Cheat:" → la version ultra-compacte, presque un aide-mémoire de syntaxe / Lien "Full detail" → retour au chapitre complet si un point ne "sonne" plus familier.

**⚠️ Erreur fréquente :** Imprimer cette fiche *avant* d'avoir étudié Routing en détail, en espérant apprendre directement dessus — le format est trop dense pour un premier apprentissage, il ne fonctionne qu'en rappel.

**🧠 Comment le mémoriser :** *« Une page, un domaine, la veille de l'examen »* — cette fiche est le tout dernier support à consulter, pas le premier.

## Conditional Request Matching
- `condition` matches on an ExpressionLanguage boolean over the request.
- Variables `context`/`request`; functions `env()`/`service()`.
- `service()` needs `#[AsRoutingConditionService]`.
- Matching-only; false = 404; ignored by generation; compiled (not eval).

**Cheat:** `condition: "request.headers.get('X') == 'y'"`. `context` (RequestContext), `request` (Request), `env()`, `service()`. False condition ⇒ 404. Generation ignores it. Tag: `#[AsRoutingConditionService(alias: '...')]`.

## Configuring Routes
- A route = **name + path + controller**; extras refine matching.
- Attributes and YAML both compile to one `RouteCollection`.
- Matching is **first-match-wins** in declaration order.
- Class-level `#[Route]` supplies path and name **prefixes**.

**Cheat:** Attribute: `Symfony\Component\Routing\Attribute\Route`. Compiled cache file: `{cache}/url_matching_routes.php`. Import types: `attribute`, `yaml`, `directory`; keys `prefix`, `name_prefix`. `debug:router` / `debug:router <name>` to inspect.

## Router Debugging
- `debug:router` lists/inspects; `router:match` simulates a request.
- `router:match` uses `TraceableUrlMatcher` and explains *why* routes fail.
- Prod route changes require a **cache rebuild**.
- Compiled files: `url_matching_routes.php`, `url_generating_routes.php`.

**Cheat:** `debug:router [name]` · `router:match <path> --method --host --scheme`. Prod: `cache:clear` after route edits. Profiler → Routing panel shows `_route`.

## Default Values & Optional Parameters
- A default makes a placeholder optional; **only trailing** ones qualify.
- Inline order: `{name<requirement>?default}`; `?` alone means `null`.
- Generation drops segments equal to their default (canonical URL).
- `defaults` also carries non-path values like `_format`/`_locale`.

**Cheat:** `{page<\d+>?1}` = digits, optional, default 1. `{slug?}` = optional, default null. Matches with & without the trailing segment. `generateUrl(default value)` ⇒ segment omitted.

## Domain Name (Host) Matching
- `host` constrains the request host; placeholders capture subdomains.
- Host compiles to a **separate regex**, checked before the path.
- Host tokens default to `[^.]+`; support `requirements`/`defaults`.
- Cross-host generation forces an absolute/network URL.

**Cheat:** `host: '{sub}.example.com'` + `requirements`/`defaults`. Host default regex `[^.]+`; matched before path. Cross-host `generateUrl` → absolute URL. Import-level `host:` groups routes.

## Locale Guessing & Localized Routes
- Localized `path` arrays expand into one route per locale.
- `_locale` (matched, sticky session, or `default_locale`) sets the request locale.
- `Accept-Language` guessing is **opt-in**, not automatic.
- Always constrain `_locale` and set `framework.default_locale`.

**Cheat:** `path: {en: /about, fr: /a-propos}`. `/{_locale}/...` + `requirements: {_locale: 'en|fr'}` + default. `generateUrl(name, {_locale: 'fr'})`. `framework.default_locale`; guess via `set_locale_from_accept_language`.

## HTTP Method Matching
- `methods` limits verbs; `GET` also matches `HEAD`.
- Wrong method on a matching path = **405 + Allow**, not 404.
- `schemes` mismatch = **redirect**, not rejection.
- `_method` override needs `enableHttpMethodParameterOverride()`.

**Cheat:** `methods: ['GET','POST']`, `schemes: ['https']`. GET ⇒ HEAD. Wrong verb ⇒ 405. Wrong scheme ⇒ redirect. Override: `Request::enableHttpMethodParameterOverride()`.

## Triggering Redirects from Routing
- `RedirectController` gives config-only redirects: `redirectAction` (route),
  `urlRedirectAction` (path/URL).
- `permanent: true` = 301; default 302.
- Trailing-slash mismatch → **301 for GET/HEAD**, **405 for POST**.
- Logic-driven redirects belong in a controller (`redirectToRoute()`).

**Cheat:** `redirectAction` → `route`; `urlRedirectAction` → `path`. `permanent`, `keepQueryParams`, `keepRequestMethod`, `scheme`. Slash mismatch: 301 (safe) / 405 (POST).

## Restricting URL Parameters (Requirements)
- Requirements are compiled into the route regex; violations mean **no match**.
- Default token regex is `[^/]+`; use `.+` to cross slashes.
- Inline `{id<\d+>}` ≡ `requirements: {id: '\d+'}`.
- Regexes are auto-anchored — no `^`/`$`, no capturing groups.

**Cheat:** Inline: `{name<regex>}`. Array: `requirements: {name: 'regex'}`. Default: `[^/]+`. Catch-all: `<.+>`. Fail = 404 (no match), not 400. Order numeric routes before slug routes.

## Special Internal Routing Attributes
- Reserved attributes: `_controller`, `_format`, `_locale`, `_fragment` (inputs);
  `_route`, `_route_params` (outputs).
- `RouterListener` copies matcher output into request attributes.
- `_format` drives content negotiation; `_locale` sets the request locale.
- `stateless: true` asserts no session use (debug-time warning).

**Cheat:** Inputs: `_controller`, `_format`, `_locale`, `_fragment`. Outputs: `_route`, `_route_params` (read via `request->attributes`). `stateless: true` = no session (debug assertion). Populated by `RouterListener` on `kernel.request`.

## Generating URLs
- Generate URLs from **names**; never hard-code paths.
- Reference-type constants live on `UrlGeneratorInterface`; default is
  `ABSOLUTE_PATH`.
- Extra params → query string; requirement mismatch → exception.
- Absolute URLs need a `RequestContext`/`default_uri` outside web requests.

**Cheat:** `$this->generateUrl(name, params, UrlGeneratorInterface::ABSOLUTE_URL)`. Twig: `path()` = path, `url()` = absolute. Types: `ABSOLUTE_PATH` (default), `ABSOLUTE_URL`, `NETWORK_PATH`, `RELATIVE_PATH`. CLI links → set `framework.router.default_uri`.
