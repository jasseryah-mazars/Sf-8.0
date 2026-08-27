# Conditional Request Matching

!!! tip "In a nutshell"
    A `condition` is an ExpressionLanguage boolean (over `context`/`request`, with
    `env()`/`service()`) that acts as a last-mile match filter when path, host, method and scheme aren't enough.
    Exam hook: conditions affect matching only (a false one is a 404, never affects `generateUrl()`).

!!! example "Real-world analogy"
    Think of a nightclub bouncer standing at the correct door of the correct building. You
    already found the right address (host) and the right entrance (path + method), and now
    the bouncer runs one last custom check — the wristband, the guest list, tonight's dress
    code. Fail it and you are simply turned away as if the door were not there (a 404), never
    "forbidden with a reason". And the bouncer never touches the printed invitations the club
    mails out: those addresses are produced regardless of who would actually be let in.

!!! abstract "Learning objectives"
    By the end of this chapter you can:

    - [ ] Restrict a route with a `condition` expression
    - [ ] Use the `context`, `request`, `env()` and `service()` variables/functions
    - [ ] Explain when a condition is evaluated and its cost
    - [ ] Know why conditions are excluded from URL generation

    **Syllabus:** `Routing → Conditional matching` ·
    **Level:** Expert ·
    **Est. time:** 20 min ·
    **Prerequisites:** [Host matching](host-matching.md)

    **Examen Symfony 8 :** OUI

---

## Pour les nuls

### L'idée en une phrase
Une `condition` est un dernier filtre custom, évalué seulement quand le chemin, l'host et la méthode ne suffisent pas déjà à décider.

### Imagine dans la vraie vie
Un videur de boîte de nuit posté à la bonne porte du bon bâtiment. Tu as déjà trouvé la bonne adresse (host) et la bonne entrée (chemin + méthode), et maintenant le videur fait un dernier contrôle sur mesure — le bracelet, la liste d'invités. Échoue ce contrôle et tu es simplement refoulé comme si la porte n'existait pas (un 404), jamais "interdit avec une raison".

### Dans Symfony
`condition: "request.headers.get('User-Agent') matches '/mobile/i'"` peut router les visiteurs mobiles vers un contrôleur dédié, sans jamais toucher au chemin de l'URL lui-même.

### Exemple simple
```yaml
api_beta:
    path: /api/data
    condition: "context.getMethod() === 'GET' and request.query.has('beta')"
```

### Comment le mémoriser 🧠
Une condition **n'affecte jamais** `generateUrl()` — seulement le matching entrant. Le videur ne touche jamais aux invitations imprimées que le club envoie par la poste.

When path, host, method and scheme are not expressive enough, a **`condition`** lets
you match on an arbitrary boolean **ExpressionLanguage** expression evaluated
against the request. Examples: only match when a specific header is present, when a
feature-flag env var is on, or when a query parameter has a value.

```php
// `condition` = a boolean ExpressionLanguage expression evaluated against the request
#[Route(
    '/beta',
    name: 'app_beta',
    // header present + feature-flag env var on + query parameter value
    condition: "request.headers.has('X-Beta') and env('FEATURE_BETA') == '1' and request.query.get('preview') == '1'",
)]
public function beta(): Response { /* ... */ }
```

A condition is a last-mile filter: the route is considered matched **only if** the
expression returns `true`. Because it can inspect anything on the request, it is
powerful — but it runs on every candidate match, so keep it cheap.

!!! question "Predict first"
    A route's `condition` evaluates to `false` at request time. Does
    `generateUrl()` for that same route also fail?

??? note "Reveal"
    No. Conditions affect **matching only** — there is no request to evaluate during
    generation, so the URL is produced normally. A false condition is a 404, and it
    is your job to ensure the target context will actually match.

## Deep Dive — how it works internally

`RouteCompiler` leaves the `condition` as an expression string on the `Route`. The
framework compiles all conditions ahead of time via
`Symfony\Component\ExpressionLanguage\ExpressionLanguage` and the routing
`ExpressionLanguageProvider`, so the dumped matcher contains **compiled PHP
closures**, not runtime `eval`. `UrlMatcher::handleRouteRequirements()` executes the
condition after the host and path have matched.

Available variables and functions in the expression:

| Name | Type | What it is |
|---|---|---|
| `context` | `RequestContext` | scheme, host, method, path info |
| `request` | `Request` | full HttpFoundation request |
| `env(name)` | function | value of an environment variable |
| `service(id)` | function | a service (must be tagged `routing.condition_service`) |

`service()` requires the target service to carry the
`routing.condition_service` tag (add it with the `#[AsRoutingConditionService]`
attribute) so the router knows it may be referenced. `env()` reads the resolved
container env value.

```php
use Symfony\Component\Routing\Attribute\AsRoutingConditionService;

// #[AsRoutingConditionService] applies the routing.condition_service tag
#[AsRoutingConditionService(alias: 'flags')]
final class FeatureFlags
{
    public function isOn(string $name): bool { return true; }
}

// service() calls the tagged service; env() reads the resolved container env value
#[Route('/beta', condition: "service('flags').isOn('beta') and env('APP_ENV') == 'dev'")]
```

```mermaid
flowchart TD
    A[candidate route] --> B{host + path match?}
    B -->|no| C[skip]
    B -->|yes| D{condition expr true?}
    D -->|no| C
    D -->|yes| E[matched]
```

!!! note "Source reference"
    Conditions compile through `ExpressionLanguage`; evaluated in
    `UrlMatcher::handleRouteRequirements()` —
    [symfony/symfony `8.0`](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Matcher/UrlMatcher.php).

### Why generation ignores conditions

`generateUrl()` **cannot** honour a condition — there is no request to evaluate it
against. Conditions therefore affect **matching only**; a route hidden behind a
condition still generates its URL normally, and it is your job to ensure the target
context will actually match.

## Configuration & code

=== "PHP Attributes"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Controller;

    use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\Routing\Attribute\Route;

    final class FeatureController extends AbstractController
    {
        // Match only for JSON-accepting clients on a feature-flagged env.
        #[Route(
            '/beta',
            name: 'app_beta',
            condition: "request.headers.get('Accept') matches '/application\\\\/json/' and env('FEATURE_BETA') == '1'",
            methods: ['GET'],
        )]
        public function beta(): Response
        {
            return $this->json(['beta' => true]);
        }
    }
    ```

=== "YAML"

    ```yaml
    # config/routes/feature.yaml
    app_beta:
        path: /beta
        controller: App\Controller\FeatureController::beta
        methods: [GET]
        condition: "context.getMethod() in ['GET', 'HEAD'] and request.query.has('preview')"
    ```

=== "service() in a condition"

    ```php
    <?php
    declare(strict_types=1);

    namespace App\Routing;

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\Routing\Attribute\AsRoutingConditionService;

    // Tag makes it callable as service('feature_checker') in a condition.
    #[AsRoutingConditionService(alias: 'feature_checker')]
    final class FeatureChecker
    {
        public function isEnabled(Request $request): bool
        {
            return $request->getClientIp() === '127.0.0.1';
        }
    }
    ```

    ```yaml
    app_internal:
        path: /internal
        controller: App\Controller\FeatureController::beta
        condition: "service('feature_checker').isEnabled(request)"
    ```

## Best practices & anti-patterns

| ✅ Do | ❌ Avoid |
|---|---|
| Keep conditions cheap and pure | Heavy DB/HTTP work in a condition |
| Prefer `methods`/`schemes`/`host` first | Re-implementing them in a condition |
| Tag services with `#[AsRoutingConditionService]` | Calling untagged services |
| Remember generation ignores conditions | Assuming a URL "won't be generated" |

## When (not) to use it / alternatives

Reach for `condition` only when the built-in constraints cannot express the rule.
For method/scheme/host, use the dedicated options — they are faster and appear in
`debug:router`. For authorization, use [Security](../security/index.md) voters, not
a routing condition (a failed condition is a 404, not a 403, and leaks less but
also cannot show a login page).

!!! danger "Certification traps"
    - Conditions affect **matching only** — **never** URL generation.
    - A failed condition yields **404** (route not matched), not 403.
    - `service()` targets **must be tagged** `routing.condition_service`
      (`#[AsRoutingConditionService]`).
    - Variables are `context` and `request`; functions are `env()` and `service()`.
    - Conditions are **compiled** into the matcher, not `eval`'d per request.

!!! warning "Common mistakes"
    - Using a condition for auth and wondering why there's no 403.
    - Referencing an untagged service in `service()`.
    - Expensive logic that runs on every candidate route.

## Exercises

1. **(Basic)** Match `/preview` only when the query string contains `preview`.
2. **(Intermediate)** Match `/internal` only when a tagged `feature_checker`
   service returns true for the request.

??? success "Solutions"

    **1.**

    ```php
    #[Route('/preview', name: 'app_preview',
        condition: "request.query.has('preview')", methods: ['GET'])]
    public function preview(): Response { /* ... */ }
    ```

    **2.** See the `service()` example above — tag the checker with
    `#[AsRoutingConditionService(alias: 'feature_checker')]` and reference
    `service('feature_checker').isEnabled(request)`.

## Certification questions

*Question d'entraînement inspirée du syllabus — jamais une question officielle de l'examen.*

??? question "Q1. A route's `condition` returns false. What is the outcome?"
    - [ ] A. 403 Forbidden
    - [x] B. 404 — the route is not matched ✅
    - [ ] C. 405 Method Not Allowed
    - [ ] D. The controller runs anyway

    **Why:** a false condition means the route does not match; matching continues.
    **Ref:** [Matching conditions](https://symfony.com/doc/8.0/routing.html#matching-expressions).

??? question "Q2. Which are valid inside a routing condition?"
    - [x] A. `context`, `request`, `env()`, `service()` ✅
    - [ ] B. `session`, `token`, `user()`
    - [ ] C. `kernel`, `container`
    - [ ] D. `params`, `route()`

    **Why:** the routing expression provider exposes exactly these.
    **Ref:** [Routing](https://symfony.com/doc/8.0/routing.html#matching-expressions).

??? question "Q3. Do conditions affect `generateUrl()`?"
    - [ ] A. Yes, generation fails if the condition is false
    - [x] B. No — conditions are matching-only ✅
    - [ ] C. Only for absolute URLs
    - [ ] D. Only in debug mode

    **Why:** there is no request to evaluate; generation ignores conditions.
    **Ref:** [Routing](https://symfony.com/doc/8.0/routing.html#matching-expressions).

??? question "Q4. To call `service('x')` in a condition, service `x` must…"
    - [x] A. Be tagged `routing.condition_service` (`#[AsRoutingConditionService]`) ✅
    - [ ] B. Be public
    - [ ] C. Implement `RouterInterface`
    - [ ] D. Extend `AbstractController`

    **Why:** only tagged services are exposed to the routing expression.
    **Ref:** [Routing](https://symfony.com/doc/8.0/routing.html#matching-expressions).

## Key takeaways

- `condition` matches on an ExpressionLanguage boolean over the request.
- Variables `context`/`request`; functions `env()`/`service()`.
- `service()` needs `#[AsRoutingConditionService]`.
- Matching-only; false = 404; ignored by generation; compiled (not eval).

## Last-minute revision

!!! tip "Cheat sheet"
    - `condition: "request.headers.get('X') == 'y'"`.
    - `context` (RequestContext), `request` (Request), `env()`, `service()`.
    - False condition ⇒ 404. Generation ignores it.
    - Tag: `#[AsRoutingConditionService(alias: '...')]`.

## Connections

- **Depends on:** [Host matching](host-matching.md) — the condition runs only after host + path have matched.
- **Reused in:** [Config & ExpressionLanguage](../miscellaneous/configuration.md) — conditions are compiled ExpressionLanguage expressions.
- **Confused with:** [Security](../security/index.md) — a failed condition is a 404, not authorization (which is a 403 via voters).

## Official References
- [Official Symfony docs — Matching expressions](https://symfony.com/doc/8.0/routing.html#matching-expressions)
- [Symfony source — UrlMatcher](https://github.com/symfony/symfony/blob/8.0/src/Symfony/Component/Routing/Matcher/UrlMatcher.php)

## Video references

!!! tip "Watch & learn"
    These are official, continuously-updated video channels — search them for
    "Symfony routing" to reinforce this chapter. We link stable channels rather than
    individual videos so the references never rot.

    - [SymfonyCasts screencasts](https://symfonycasts.com/tracks/symfony) — scripted, code-along tutorials.
    - [Symfony official YouTube](https://www.youtube.com/@SymfonyOfficial) — SymfonyCon conference talks & keynotes.
    - [Official docs for this topic](https://symfony.com/doc/8.0/routing.html#matching-expressions) — some Symfony doc pages embed a screencast.

## Confidence check

I'm ready when I can:

- [ ] explain **why** conditions are matching-only and never affect generation
- [ ] implement a `condition` using `request`/`env()` and a tagged `service()` in Symfony 8
- [ ] debug a `service()` call that fails because the target isn't tagged
- [ ] spot that a false condition is 404 (not 403) and conditions are compiled (not `eval`'d)
- [ ] explain where `UrlMatcher::handleRouteRequirements()` runs the compiled closure

---

<small>Related: [Host matching](host-matching.md) · [Methods](methods.md) · [Special attributes](special-attributes.md) · [Config & ExpressionLanguage](../miscellaneous/configuration.md)</small>
